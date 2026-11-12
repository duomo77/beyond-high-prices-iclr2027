# Beyond High Prices

**Auditing Information-Mediated Enforcement in Recurrent Pricing Agents**

The current manuscripts are the **[Main Paper PDF](main.pdf)** and the **[Supplementary Material PDF](supplement.pdf)**. The main paper is 8 total pages—including references and the AI Use Statement—and leaves the font size, margins, and text area of the official ICLR 2027 style unchanged. The supplement expands the main paper's reasoning and equations step by step and preserves all seed and probe tables. The URL of this repository is listed at the end of the supplement.

## Current Files

| File / Folder | Contents |
|---|---|
| [`main.tex`](main.tex), [`main.pdf`](main.pdf) | Plain-English 8-page main paper and its compilation source |
| [`supplement.tex`](supplement.tex), [`supplement.pdf`](supplement.pdf) | Expanded proofs, configuration, statistics, all 160 probes, detailed walkthrough, and repository URL |
| [`figures/`](figures) | Two figures generated directly from recorded CSV and JSON files |
| [`iclr2027_conference.sty`](iclr2027_conference.sty), [`.bst`](iclr2027_conference.bst), [`natbib.sty`](natbib.sty), [`fancyhdr.sty`](fancyhdr.sty) | Style files from the official ICLR 2027 distribution |
| [`experiment_results/`](experiment_results) | Existing experiment outputs and checkpoints; left unchanged by these text revisions |
| [`scripts/`](scripts) | Scripts for re-aggregating results, running finite arithmetic checks, and rendering figures |
| [`verification/`](verification) | Verification outputs for the current manuscripts, file hashes, evidence scope, and review records |

Earlier PDFs and ZIP files, duplicate `*_corrected` manuscripts, previous source folders, and superseded review drafts have been removed from the repository.

## Reading Order

The main paper follows this order: the difference between high prices and dynamic punishment, the market and observation channel, the price-cut audit, experimental results, the repeated-game benchmark, and interpretation and limits. The opening guide table in the supplement links each topic to detailed explanations in Sections A–I. Section I walks through demand derivatives, signal delay, GRU and PPO, counterfactual profit decomposition, bootstrap intervals, threshold derivations, concrete probe cases, and welfare so each part stands on its own. Section J lists this repository and the available artifacts.

## Compiling and Verification

Run these commands from the repository root in an environment with LaTeX installed. On Overleaf, upload all repository files and choose `main.tex` or `supplement.tex` as the main document.

```bash
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
latexmk -pdf -interaction=nonstopmode -halt-on-error supplement.tex
python3 scripts/verify_theory.py
python3 scripts/verify_archive.py --root . --output verification/archive-results.json
python3 scripts/render_figures.py
```

Archive verification uses NumPy, and figure generation uses NumPy and Matplotlib. The verification checks all 160 probe rows, all 20 seed outcomes, and all 20 final checkpoint SHA-256 hashes. It does not train new policies or deserialize checkpoints.

## Scope of Verification

This repository is a **results archive** of the original experiments. The original trainer and simulator source code, native binary, posterior draws, raw calibration inputs, and individual rollout files are not included. You can therefore recheck tables, bootstrap summaries, and file integrity, but you cannot re-run actual training or MCMC calibration, nor verify the simulator's welfare formula or how `added_sigma` is combined with posterior noise. Both manuscripts state these boundaries explicitly.

Official ICLR 2027 instructions are available in the [Author Guidelines](https://iclr.cc/Conferences/2027/AuthorGuidelines). At submission, the official page limit is 9 pages of main text excluding references, whereas this manuscript is intentionally formatted so the entire PDF fits within 8 pages. Because this public repository URL identifies its owner, replace the repository address at the end of the supplement with an anonymized artifact link before submitting for double-blind review. The official style package comes from [ICLR 2027 style files](https://media.iclr.cc/Conferences/ICLR2027/iclr-2027-style-files.zip).
