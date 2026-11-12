#!/usr/bin/env python3
"""Bounded arithmetic checks for the manuscript audit; not a universal proof.

Run: python3 scripts/verify_theory.py
Uses exact fractions for counterexamples and bisection for static logit roots.
"""
from fractions import Fraction as F
import json
import math


def bisect(fn, lo=1., hi=2.5):
    assert fn(lo) > 0 and fn(hi) < 0
    for _ in range(100):
        mid = (lo + hi)/2
        if fn(mid) > 0:
            lo = mid
        else:
            hi = mid
    return (lo + hi)/2


def share(p):
    x = math.exp((2-p)/.25)
    return x/(1+2*x)


def normal_cdf(x):
    return .5*math.erfc(-x/math.sqrt(2))


def main():
    # The original domain allowed beta<alpha and thus a negative denominator.
    alpha, beta, g, h, delta = F(9,10), F(1,10), F(1), F(1), F(1,2)
    denominator = g*(1-alpha)+(beta-alpha)*h
    gain = g-delta*(beta-alpha)*h/(1-delta*(1-alpha))
    assert delta >= g/denominator and gain == F(27,19) and gain > 0
    # Corrected A.2: deterring the largest current gain is insufficient.
    big = F(9,10)/(F(9,10)*F(19,20)+F(1,2))
    small = F(3,10)/(F(3,10)*F(19,20)+F(1,100))
    assert big == F(180,271) < F(9,10) < small == F(60,59)
    pn = bisect(lambda p: 1-(p-1)/.25*(1-share(p)))
    pj = bisect(lambda p: 1-(p-1)/.25*(1-2*share(p)))
    q = share(pn)
    old_welfare = 2*q
    logit_welfare = .25*math.log1p(2*math.exp((2-pn)/.25))+2*(pn-1)*q
    assert old_welfare < 1 < logit_welfare
    # Sampled checks corroborate the algebra in the report. This is 1000 cases,
    # not proof of the all-parameter incentive or Gaussian statements.
    ic_cases = 0
    for a in [0., .05, .4, .9]:
        for b in [(1+a)/2, 1.]:
            for gain_now in [.01, .3, .9, 2., 10.]:
                for gap in [.01, .5, 1., 4., 10.]:
                    threshold = gain_now/(gain_now*(1-a)+(b-a)*gap)
                    for d in [0., .25, .5, .9, .99]:
                        value_diff = gain_now-d*(b-a)*gap/(1-d*(1-a))
                        assert (value_diff <= 1e-13) == (d+1e-13 >= threshold)
                        ic_cases += 1
    noise_checks = []
    for s in [.01, .05, .1, .5, 1., 2., 10., 100.]:
        a, b = normal_cdf(-1/s), normal_cdf(1/s)
        dstar = 1/((1-a)+(b-a))
        noise_checks.append({'sigma': s, 'alpha': a, 'beta': b, 'delta_star': dstar})
    # Extremely small tails round to zero in float arithmetic at small sigma.
    assert all(x['delta_star'] <= y['delta_star'] for x,y in zip(noise_checks,noise_checks[1:]))
    assert all(x['delta_star'] < y['delta_star'] for x,y in zip(noise_checks[3:],noise_checks[4:]))
    print(json.dumps({'scope': 'Exact counterexamples, logit roots, finite IC/noise checks; no training or universal computational proof',
                      'original_domain_counterexample': {'denominator': str(denominator),
                           'displayed_threshold': str(g/denominator), 'actual_gain': str(gain)},
                      'corrected_example': {'largest_gain_threshold': str(big),
                                            'smaller_gain_threshold': str(small)},
                      'continuous_nash': pn, 'continuous_joint_profit': pj,
                      'old_welfare_at_nash': old_welfare,
                      'logit_welfare_at_nash': logit_welfare,
                      'sampled_ic_cases': ic_cases, 'sampled_noise_cases': noise_checks}, indent=2))


if __name__ == '__main__':
    main()
