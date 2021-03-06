import numpy as np
import density, estimators, rates, helper


def estimator_rate(est_type, ns, ss, alpha, beta, d=1, iters=50, fast=True):
    """
    Experiment for the rate of convergence of the estimator for T(p,q) = \int p^\alpha q^\beta.
    est_type -- which estimator, "linear" "plugin" or "quadratic"
    ns -- which ns should we run the experiment on. Try np.logspace(1, 4, 20)
    ss -- which smoothnesses should we run the experiment on
    alpha -- the exponent for p
    beta -- the exponent for q
    d -- the dimension
    iters -- how many iterations should we use

    Returns nothing but writes log files with the results of the experiments to ./data/
    """
    E = None
    if est_type == "plugin":
        E = estimators.PluginEstimator
    elif est_type == "linear":
        E = estimators.LinearEstimator
    elif est_type == "quadratic":
        E = estimators.QuadraticEstimator
    else:
        print "Estimator %s not supported" % (est_type)
        return

    for s in ss:
        print "s = %s" % (str(s))
        if d == 1:
            Dp = density.UniTrigDensity(s, 1)
            Dq = density.UniTrigDensity(s, 1)
        else:
            Dp = density.TrigDensity(s, 1, d)
            Dq = density.TrigDensity(s, 1, d)
        (new_ns, ms, vs) = rates.estimator_rate(E, Dp, Dq, ns, alpha=alpha, beta=beta, iters=iters, fast=fast)
        f = open("./data/%s_error_d=%d_s=%s.out" % (est_type, d, str(s)), "w")
        f.write("ns " + " ".join([str(n) for n in ns]) + "\n")
        f.write("ms " + " ".join([str(m) for m in ms]) + "\n")
        f.write("vs " + " ".join([str(v) for v in vs]))
        f.close()
    return

def kde_rate(ns, ss, d=1, iters=50, fast=True):
    """
    Experiment for the KDE rate of convergence. 
    ns -- which ns should we run the experiment on. Try np.logspace(1, 4, 20)
    ss -- which smoothnesses should we run the experiment on
    d -- the dimension
    iters -- how many iterations should we use

    Returns nothing but writes log files with the results of the experiments to ./data/
    """
    ps = [1,2,3]
    for s in ss:
        print "s = %s" % (str(s))
        if d == 1:
            D = density.UniTrigDensity(s, 1)
        else:
            D = density.TrigDensity(s, 1, d)
        
        (new_ns, ms, vs) = rates.kde_rate(D, ns, ps, iters=iters)
        for i in range(len(ps)):
            f = open("./data/kde_error_d=%d_p=%d_s=%s.out" % (d, ps[i], str(s)), "w")
            f.write("ns " + " ".join([str(n) for n in ns]) + "\n")
            f.write("ms " + " ".join([str(m) for m in ms[i]]) + "\n")
            f.write("vs " + " ".join([str(v) for v in vs[i]]))
            f.close()
    return 

if __name__=="__main__":
    ss = [3.0, 4.0]
    ns = np.logspace(1, 4.0, 30)

    estimator_rate("plugin", ns, ss, 0.5, 0.5, d=2)
    estimator_rate("linear", ns, ss, 0.5, 0.5, d=2)

#     ss = [1.0, 2.0]
#     ns = np.logspace(1, 2.6990, 20)
#     estimator_rate("quadratic", ns, ss, 0.5, 0.5, iters=20)
#     kde_rate(ns, ss, d=1)
