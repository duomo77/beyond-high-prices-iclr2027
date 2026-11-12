#!/usr/bin/env python3
"""Render manuscript figures directly from archived PPO CSV/JSON summaries.

Run from the repository: python3 scripts/render_figures.py
Requires NumPy and Matplotlib. No smoothing, interpolation, or new simulations.
The 2000 whole-seed bootstrap draws use default_rng(20260920).
"""
import csv
import json
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
SUITE = ROOT / 'experiment_results'
OUT = ROOT / 'figures'
SEEDS = range(20261001, 20261011)
ARMS = [('ppo_baseline', 'Informative', '#2166ac'),
        ('ppo_ablated', 'Action independent', '#b35806')]
INDEX = np.random.default_rng(20260920).integers(0, 10, (2000, 10))
plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 10,
                     'axes.spines.top': False, 'axes.spines.right': False,
                     'axes.labelsize': 10, 'legend.fontsize': 9,
                     'savefig.dpi': 300})


def interval(values):
    return np.quantile(values[INDEX].mean(axis=1), [.025, .975], axis=0)


def style(ax):
    ax.grid(alpha=.22, linewidth=.6)
    ax.set_axisbelow(True)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    fig, axes = plt.subplots(1, 2, figsize=(9, 3.1), layout='constrained')
    for arm, label, color in ARMS:
        curves = []
        for seed in SEEDS:
            with (SUITE / arm / str(seed) / 'policy.curve.csv').open() as f:
                curves.append(list(csv.DictReader(f)))
        steps = np.array([float(r['environment_steps']) for r in curves[0]]) / 1e6
        for ax, metric in zip(axes, ['price_elevation', 'mean_total_surplus']):
            values = np.array([[float(r[metric]) for r in rows] for rows in curves])
            lo, hi = interval(values)
            ax.plot(steps, values.mean(0), color=color, label=label, lw=1.6)
            ax.fill_between(steps, lo, hi, color=color, alpha=.17, lw=0)
    axes[0].axhline(0, color='.4', ls='--', lw=.8)
    axes[0].set_ylabel('Normalized price elevation')
    axes[1].set_ylabel('Archived welfare index per period')
    axes[0].legend(frameon=False, loc='upper right')
    for ax in axes:
        ax.set_xlabel('Training interactions (millions)')
        style(ax)
    fig.savefig(OUT / 'image1.png')
    plt.close(fig)

    fig, axes = plt.subplots(1, 2, figsize=(9, 3.1), layout='constrained')
    for arm, label, color in ARMS:
        all_probes = [json.loads((SUITE / arm / str(s) / 'audit_probes.json').read_text())
                      for s in SEEDS]
        # Average eight types within each seed before resampling the ten seeds.
        paths = np.array([np.mean([p['result']['mean_impulse_response'][:36]
                                  for p in probes], axis=0) for probes in all_probes])
        lo, hi = interval(paths)
        lag = np.arange(36)
        axes[0].plot(lag, paths.mean(0)*1e6, label=label, color=color, lw=1.6)
        axes[0].fill_between(lag, lo*1e6, hi*1e6, color=color, alpha=.17, lw=0)
        for cut, marker in [(.1, 'o'), (.3, 's')]:
            impact, full = [], []
            for probes in all_probes:
                selected = [p['result'] for p in probes if p['cut'] == cut]
                impact.append(np.mean([r['mean_immediate_deviation_gain'] for r in selected]))
                full.append(np.mean([r['mean_deviation_gain'] for r in selected]))
            axes[1].scatter(impact, full, marker=marker, s=27, facecolor='none',
                            edgecolor=color, linewidth=1, zorder=3)
    axes[0].set_xlabel('Periods after intervention')
    axes[0].set_ylabel(r'Rival price response ($10^{-6}$)')
    axes[0].legend(frameon=False, loc='lower right')
    lim = [-.066, .005]
    axes[1].plot(lim, lim, color='.45', ls='--', lw=.8)
    axes[1].set(xlim=lim, ylim=lim, xlabel='Immediate profit gain',
                ylabel='Full remaining-episode gain')
    axes[1].legend(handles=[Line2D([], [], marker=m, color='.3', linestyle='none',
                                  markerfacecolor='none', label=f'Action cut {c}')
                             for c, m in [(.1, 'o'), (.3, 's')]],
                   frameon=False, loc='upper left')
    for ax in axes:
        style(ax)
    fig.savefig(OUT / 'image_2.png')
    plt.close(fig)
    print('Rendered two figures from 20 learning curves and 160 probe summaries.')


if __name__ == '__main__':
    main()
