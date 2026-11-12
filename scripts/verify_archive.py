#!/usr/bin/env python3
"""Recompute the PPO manuscript summaries from archived JSON/CSV, without loading checkpoints.

Run: python verify_archive.py --root /path/to/repository --output /path/to/results.json
NumPy is the only nonstandard dependency. Bootstrap draws use one deterministic,
reused whole-seed resampling matrix (2000 x 10; default_rng seed 20260920).
This checks recorded outputs and their consistency, not simulator correctness or
reproduction of the missing training/calibration implementation.
"""
import argparse
import csv
import hashlib
import json
import platform
from pathlib import Path
import re
import zipfile

import numpy as np

SEEDS = list(range(20261001, 20261011))
ARMS = ["ppo_baseline", "ppo_ablated"]
OUTCOMES = ["mean_price", "price_elevation", "mean_total_surplus",
            "agent_0_effective_rank", "agent_1_effective_rank"]
INDEX = np.random.default_rng(20260920).integers(0, 10, size=(2000, 10))


def load(path):
    return json.loads(path.read_text())


def stat(values):
    values = np.asarray(values, dtype=float)
    assert values.shape[0] == 10
    assert np.isfinite(values).all()
    draws = values[INDEX].mean(axis=1)
    return {"mean": values.mean(axis=0).tolist(),
            "sample_std": values.std(axis=0, ddof=1).tolist(),
            "ci95": np.quantile(draws, [.025, .975], axis=0).tolist()}


def close(a, b, atol=1e-13):
    return bool(np.allclose(a, b, rtol=0, atol=atol))


def finite_tree(obj):
    if isinstance(obj, dict):
        return all(finite_tree(v) for v in obj.values())
    if isinstance(obj, list):
        return all(finite_tree(v) for v in obj)
    if isinstance(obj, (float, int)):
        return bool(np.isfinite(obj))
    return True


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--root", type=Path, required=True)
    ap.add_argument("--main", type=Path)
    ap.add_argument("--supplement", type=Path)
    ap.add_argument("--output", type=Path, required=True)
    args = ap.parse_args()
    root = args.root.resolve()
    suite = root / "experiment_results"
    mainpath = args.main or root / "main.tex"
    supppath = args.supplement or root / "supplement.tex"
    # Read the selected manuscripts; numerical table comparisons are in supplement.
    mainpath.read_text()
    supplement = supppath.read_text()
    manifest = load(suite / "suite_manifest.json")
    archived_summary = load(suite / "summary.json")
    jobs, probes, curves = {}, {}, {}
    hashes = []
    consistency_errors = []
    all_probes = []
    for arm in ARMS:
        for seed in SEEDS:
            folder = suite / arm / str(seed)
            job = load(folder / "job.json")
            audit = load(folder / "audit_probes.json")
            curve = list(csv.DictReader((folder / "policy.curve.csv").open()))
            assert job["status"] == "completed", (arm, seed, job["status"])
            assert job["seed"] == seed and job["condition"] == arm
            assert finite_tree(job) and finite_tree(audit)
            assert len(curve) == 100, (arm, seed, len(curve))
            assert all(np.isfinite(float(v)) for row in curve for v in row.values())
            expected = {(f, t, c) for f in [0, 1] for t in [64, 256] for c in [.1, .3]}
            observed = {(p["firm"], p["time"], p["cut"]) for p in audit}
            assert len(audit) == 8 and observed == expected
            for p in audit:
                result = p["result"]
                assert result["replications"] == 128
                assert result["finite_horizon"] == 512 - p["time"]
                assert result["gamma"] == .99
                assert result["common_random_numbers"] is True
                path = np.asarray(result["mean_impulse_response"])
                assert len(path) == 512 - p["time"]
                # Impact and lag-one responses vanish because the report arrives later.
                assert np.array_equal(path[:2], [0., 0.])
                area = float(path[1:].sum())
                downward = float(np.maximum(-path[1:], 0).sum())
                if not close(area, result["mean_signed_rival_response_area"]):
                    consistency_errors.append([arm, seed, p["firm"], p["time"], p["cut"], "signed area"])
                if not close(downward, result["punishment_area"]):
                    consistency_errors.append([arm, seed, p["firm"], p["time"], p["cut"], "downward area"])
                for metric in ["mean_deviation_gain", "mean_immediate_deviation_gain",
                               "mean_signed_rival_response_area", "punishment_area",
                               "mean_realized_normalized_action_cut"]:
                    jk = f'audit_f{p["firm"]}_t{p["time"]}_cut{p["cut"]}_{metric}'
                    if not close(job["metrics"][jk], result[metric]):
                        consistency_errors.append([arm, seed, jk, "job vs probe"])
                full = result["mean_deviation_gain"]
                immediate = result["mean_immediate_deviation_gain"]
                row = {"arm": arm, "seed": seed, "firm": p["firm"], "time": p["time"],
                       "cut": p["cut"], "immediate": immediate, "full": full,
                       "continuation": full - immediate, "ci95": result["mean_gain_ci95"],
                       "area": area, "downward_area": downward,
                       "max_abs_mean_response": float(np.max(np.abs(path))),
                       "response": path.tolist()}
                if arm == "ppo_ablated":
                    assert abs(full - immediate) < 1e-14 and np.array_equal(path, np.zeros(len(path)))
                all_probes.append(row)
            cp = folder / "policy.pt"
            computed = hashlib.sha256(cp.read_bytes()).hexdigest()
            hashes.append({"path": str(cp.relative_to(root)), "sha256": computed,
                           "expected": job["checkpoint_sha256"],
                           "matches": computed == job["checkpoint_sha256"]})
            jobs[arm, seed], probes[arm, seed], curves[arm, seed] = job, audit, curve

    # Recompute final outcomes and comparisons from the job metrics.
    final = {arm: {metric: stat([jobs[arm, s]["metrics"][metric] for s in SEEDS])
                   for metric in OUTCOMES} for arm in ARMS}
    paired = {metric: stat([jobs[ARMS[1], s]["metrics"][metric] - jobs[ARMS[0], s]["metrics"][metric]
                            for s in SEEDS]) for metric in OUTCOMES}
    sc = next(c for c in archived_summary["comparisons"] if c["left"] == ARMS[0] and c["right"] == ARMS[1])
    for metric in OUTCOMES:
        saved = sc["metrics"][metric]
        if not close(saved["mean"], paired[metric]["mean"]) or not close(saved["pointwise_seed_bootstrap_ci95"], paired[metric]["ci95"]):
            consistency_errors.append(["suite comparison", metric])

    # Check the reported normalization against its implied grid endpoints.
    endpoint_residuals = [(jobs[a, s]["metrics"]["mean_price"] - 1.473) / (.452)
                          - jobs[a, s]["metrics"]["price_elevation"] for a in ARMS for s in SEEDS]
    continuous_residuals = [(jobs[a, s]["metrics"]["mean_price"] - 1.472927) / (1.924981-1.472927)
                            - jobs[a, s]["metrics"]["price_elevation"] for a in ARMS for s in SEEDS]

    # Curves use rounded rollout boundaries, with a distinct final evaluation stream.
    curve_metrics = list(curves[ARMS[0], SEEDS[0]][0])
    curve_summary = {"column_names": curve_metrics}
    for arm in ARMS:
        key = "price_elevation"
        arr = np.array([[float(row[key]) for row in curves[arm, s]] for s in SEEDS])
        st = stat(arr)
        step_key = next(k for k in curve_metrics if k in ["step", "steps", "interactions", "total_steps", "environment_steps"])
        steps = [int(float(row[step_key])) for row in curves[arm, SEEDS[0]]]
        assert all([int(float(row[step_key])) for row in curves[arm, s]] == steps for s in SEEDS)
        curve_summary[arm] = {"steps": steps, **st, "increase_count_in_seed_mean": int(np.sum(np.diff(arr.mean(axis=0)) > 0))}

    audit_summary = {}
    for arm in ARMS:
        arm_rows = [p for p in all_probes if p["arm"] == arm]
        arm_stats = {}
        for cut in [.1, .3]:
            selected = [p for p in arm_rows if p["cut"] == cut]
            per_seed = {field: [np.mean([p[field] for p in selected if p["seed"] == s]) for s in SEEDS]
                        for field in ["immediate", "full", "continuation", "area", "downward_area"]}
            full, impact = np.mean(per_seed["full"]), np.mean(per_seed["immediate"])
            arm_stats[str(cut)] = {field: stat(v) for field, v in per_seed.items()}
            arm_stats[str(cut)]["positive_probes"] = [
                {k: v for k, v in p.items() if k != "response"} for p in selected if p["full"] > 0]
            arm_stats[str(cut)]["immediate_share_of_mean_full_loss_pct"] = float(100*impact/full)
        arm_stats["overall_area"] = stat([np.mean([p["area"] for p in arm_rows if p["seed"] == s]) for s in SEEDS])
        arm_stats["overall_downward_area"] = stat([np.mean([p["downward_area"] for p in arm_rows if p["seed"] == s]) for s in SEEDS])
        # Use the common supported response lags for the cross-probe seed-level figure.
        path_arr = np.array([np.mean([p["response"][:256] for p in arm_rows if p["seed"] == s], axis=0) for s in SEEDS])
        arm_stats["response_first_256_lags"] = stat(path_arr)
        audit_summary[arm] = arm_stats

    # Every printed supplement probe cell must match the corresponding archived summary.
    printed_rows = []
    mismatches = []
    for label, arm, cut in [("B01", ARMS[0], .1), ("B03", ARMS[0], .3),
                             ("A01", ARMS[1], .1), ("A03", ARMS[1], .3)]:
        table = supplement.rsplit("{tab:probe_" + label + "}", 1)[1]
        table = table.split("\\probetable", 1)[0]
        rows = re.findall(r"^(\d\d)\s*&\s*([01])\s*&\s*(64|256)\s*&\s*(.*?)\\\\", table, re.M)
        assert len(rows) == 40, (label, len(rows))
        for suffix, firm, time, numbers in rows:
            values = [float(v.strip()) for v in numbers.split("&")]
            seed = 20261000 + int(suffix)
            raw = next(p for p in all_probes if (p["arm"], p["seed"], p["firm"], p["time"], p["cut"]) == (arm, seed, int(firm), int(time), cut))
            wanted = [raw["immediate"], raw["full"], *raw["ci95"], raw["area"]]
            for field, actual, expected in zip(["immediate", "full", "lower", "upper", "area"], values, wanted):
                formatted = f"{expected:.2e}" if field == "area" else f"{expected:.6f}"
                if actual != float(formatted):
                    mismatches.append([label, suffix, firm, time, field, actual, formatted])
            printed_rows.append((arm, seed, firm, time, cut))
    assert len(set(printed_rows)) == 160

    # The seed table uses six decimals; check every one of its 100 outcome cells.
    seed_mismatches = []
    rows = re.findall(r"^(\d\d) & ([AB]) & (.*?)\\\\", supplement, re.M)
    assert len(rows) == 20
    for suffix, arm_code, values in rows:
        arm, seed = (ARMS[0] if arm_code == "B" else ARMS[1]), 20261000 + int(suffix)
        for metric, value in zip(OUTCOMES, values.split("&")):
            if float(value.strip()) != float(f'{jobs[arm, seed]["metrics"][metric]:.6f}'):
                seed_mismatches.append([suffix, arm_code, metric])

    # Sum the recorded interaction and wall-clock totals rather than extrapolating.
    interactions = {k: sum(j["interactions"][k] for j in jobs.values())
                    for k in jobs[ARMS[0], SEEDS[0]]["interactions"]}
    runtimes = {a: sum(jobs[a, s]["elapsed_seconds"] for s in SEEDS)/3600 for a in ARMS}
    runtimes["total_hours"] = sum(runtimes.values())
    previous = [{"path": str(p.relative_to(root)), "record": load(p)}
                for arm in ARMS for p in (suite / arm).glob("*/previous_failure*.json")]

    # Enumerate actual implementation/calibration files and ZIP contents, not named hashes.
    files = [p for p in root.rglob("*") if p.is_file() and ".git" not in p.parts]
    relevant = [str(p.relative_to(root)) for p in files
                if not any(part in ["scripts", "referee", "verification"] for part in p.relative_to(root).parts)
                and (p.suffix in [".py", ".cpp", ".c", ".h", ".so", ".toml", ".yaml"]
                     or p.name in ["posterior_draws.csv", "posterior_summary.csv", "research.json"])]
    zips = {}
    for p in files:
        if p.suffix == ".zip":
            with zipfile.ZipFile(p) as z:
                zips[str(p.relative_to(root))] = z.namelist()
    metadata = {"source_hash_count": len(manifest["identity"]["source_sha256"]),
                "distributed_implementation_or_calibration_files": relevant,
                "zip_members": zips,
                "posterior_hash_recorded": manifest["identity"]["posterior_sha256"],
                "native_hash_recorded": manifest["identity"]["native_sha256"],
                "calibration_gate_recorded": manifest["mcmc_gate"]}
    results = {"scope": "Postprocessing consistency of 20 PPO jobs, 160 probes, 2000 checkpoints; no checkpoint deserialization, training rerun or calibration replication.",
               "python_version": platform.python_version(), "numpy_version": np.__version__, "bootstrap_seed": 20260920, "resamples": 2000,
               "final_outcomes": final, "paired_differences": paired,
               "normalization": {"grid_pN": 1.473, "grid_pJ": 1.925,
                                 "max_abs_grid_elevation_residual": max(map(abs, endpoint_residuals)),
                                 "max_abs_rounded_continuous_elevation_residual": max(map(abs, continuous_residuals))},
               "learning_curves": curve_summary, "audit_summary": audit_summary,
               "printed_probe_row_count": len(printed_rows), "printed_probe_mismatches": mismatches,
               "printed_seed_row_count": len(rows), "printed_seed_mismatches": seed_mismatches,
               "archive_consistency_errors": consistency_errors, "checkpoint_hashes": hashes,
               "interactions": interactions, "runtimes_hours": runtimes,
               "previous_attempt_records": previous, "provenance": metadata}
    source_paths = [suite / "suite_manifest.json", suite / "summary.json", mainpath, supppath]
    source_paths += [suite / a / str(seed) / f for a in ARMS for seed in SEEDS
                    for f in ["job.json", "audit_probes.json", "policy.curve.csv", "policy.pt"]]
    results["input_sha256"] = {str(p.relative_to(root)): hashlib.sha256(p.read_bytes()).hexdigest()
                               for p in source_paths}
    results["assertion_tested"] = "Internal consistency of all 20 completed PPO jobs, 160 stored probe summaries, printed probe/seed tables, paired bootstrap and checkpoint integrity; no underlying simulator or training validation"
    errors = consistency_errors + mismatches + seed_mismatches
    errors += [["checkpoint hash", h["path"]] for h in hashes if not h["matches"]]
    if max(map(abs, endpoint_residuals)) > 1e-12:
        errors.append(["grid normalization"])
    results["run_status"] = "failed" if errors else "completed"
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(results, indent=2) + "\n")
    print(json.dumps({k: results[k] for k in ["paired_differences", "normalization", "printed_probe_row_count", "printed_probe_mismatches", "printed_seed_mismatches", "archive_consistency_errors", "interactions", "runtimes_hours"]}, indent=2))
    print("Checkpoint hashes matched:", sum(h["matches"] for h in hashes), "/", len(hashes))
    if errors:
        raise SystemExit(1)
    assert all(h["matches"] for h in hashes), "Checkpoint hash mismatch"
    assert not consistency_errors, "Inconsistent archived summaries"
    assert not mismatches and not seed_mismatches, "Manuscript table cell mismatch"


if __name__ == "__main__":
    main()
