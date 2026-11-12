# Empirical verifier findings

Input archive: `duomo77/beyond-high-prices-iclr2027`, tree `b119bdce823da664f1fdc577efa82241e1042631`.
The manuscript snapshots reviewed are `/private/tmp/bhp-audit-inputs/main.tex` and `supplement.tex`.
No previous verification reports were read. No checkpoint was deserialized.

## Confirmed errors and qualifications

1. Main text signed rival-response area and confidence interval are incorrect. Average each seed's eight probe areas, then average/resample ten seeds, as specified in supplement Section E: **-0.000013628784654429182**, 95% percentile bootstrap CI **[-0.0000252983136306284, -0.0000034169651189586147]**. Reusing the 2,000 x 10 whole-seed bootstrap matrix from NumPy default_rng(20260920) reproduces the published other intervals. The published -3.7e-6 / [-1.1e-5, 3.2e-6] do not describe this stated area estimand. The corrected interval excludes zero, although the response is economically tiny.
2. The empirical normalized elevation uses grid references **pN=1.473 and pJ=1.925**, not the continuous roots rounded to 1.472927 and 1.924981 in main Equation E. The maximum residual across the 20 reported E values is 5.1e-16 under the grid normalization, versus 0.00016523 under the displayed continuous-reference normalization. Report grid and continuous roots distinctly and retain the executed grid references in the normalization.
3. The immediate share of mean informative full deviation loss is **99.89827997% for cut 0.1** and **99.98971257% for cut 0.3**. Thus the statement that both are "over 99.9%" is false as a strict inequality; report the rounded percentages or at least 99.89%.
4. Main total-surplus formula `(v-c)(q1+q2)` cannot equal the archived values (~1.1596), because it is at most 1 for the stated primitives. The standard logit CS + profit formula is a plausible interpretation, already proposed in supplement, but the missing simulator source and evaluation price paths prevent direct verification that it generated the archived welfare field. Safest correction separates the mathematical welfare definition from the legacy archived field, with its implementation unverified.
5. Early price elevation is measured at **12,288 training interactions**, not initialization. Attributing it to initial parameterization has not been established. Mean elevation declines overall; the checkpoint mean rises on **38 of 99 transitions** for baseline and **42 of 99** for ablation, contradicting a literal monotone or steady decline.
6. Reproducibility claims overstate this repository's contents. The 13 Python implementation files are listed as hashes only. No Python/C++ simulator/trainer source, native binary, posterior draws, posterior diagnostic summary, calibration observations, or `experiments/research.json` are distributed. Both original ZIP archives contain only manuscript/style/media. Hashes cannot establish absent source bytes, algorithm implementation, Gaussian calibration, report timing, architecture, PPO loss details, or deterministic execution. The recorded MCMC gate is metadata, not independent recomputation. Reproduction commands require external material.

## Independently verified

- All **20** PPO jobs completed with finite metrics and the same intended 10 seeds in each condition; all **20 SHA256 checkpoint hashes** match job files.
- All **160 probe identities**, four probe types per cut/seed/condition, and 128 paired repetitions each are present. All **800 printed numerical probe cells** (impact, full, two mean CI limits, response area) match the archive to published precision. All **100 printed final seed outcome cells** match.
- Full gain/impact/response areas recorded in each job agree with corresponding audit file entries. Recomputing each area from its mean impulse-response path matches the stored area. No internal inconsistencies detected.
- Main final outcome means and paired CIs and supplement cut-specific full/continuation CIs reproduce independently with default_rng seed 20260920 and 2,000 whole-seed resamples.
- Baseline small-cut positive conditional means: seed 20261001/firm 0/time 64 = 0.0005733491302; seed 20261005/firm 0/time 64 = 0.0038461615908; seed 20261005/firm 0/time 256 = 0.0029902521695. Ablated positive mean: seed 20261008/firm 0/time 256 = 0.0001222647261. All four stored conditional mean intervals exclude zero individually; none of 80 large-cut probes is positive. This does not adjust multiplicity.
- Every stored ablation mean response path is exactly zero. Ablation full and immediate gains differ only through subtraction/aggregation roundoff, max absolute difference 5.27e-16; conditional invariance theorem remains consistent with these summaries.
- Recorded total interactions **58,174,720**, comprising training 20,000,000; training diagnostics 16,384,000; trainer final evaluation 163,840; suite final evaluation 655,360; paired audits 20,971,520. Recorded PPO runtime **44.05644763 h** (baseline 21.97767609 h, ablated 22.07877154 h).
- The three PPO previous-attempt JSON records are marked running; filename `previous_failure` does not establish an actual numerical failure.

## Scope and unavailable inputs

This is archive postprocessing and provenance checking, not reproduction of training or an audit of absent simulator code. Individual-rollout prices, payoffs, gains and response matrices are not distributed; stored within-policy bootstrap intervals and rollout quantiles cannot be regenerated independently. Calibration labeled observations, settings, retained draws and diagnostics are absent; the MCMC likelihood, posterior, Gaussian observation law and gate cannot be rerun. Checkpoint hashing authenticates byte consistency with job metadata but does not prove how those bytes were trained. The implementation-specific causal interpretation is conditional on the manuscript's stated actor inputs and simulator design.

Reproduce these checks:

```sh
python3 verify_archive.py --root /path/to/beyond-high-prices-iclr2027 --output results.json
```

The script uses NumPy 2.1.2 here; the recorded training environment states NumPy 2.1.3. No training dependencies were installed or run.
