# Current revision: readable eight-page ICLR paper

This revision replaces the previous manuscript files in the repository tree. The current public artifacts are `main.tex` / `main.pdf` and `supplement.tex` / `supplement.pdf`. Earlier PDF/ZIP packages, duplicated compile sources, notes and superseded review snapshots were removed from the current tree. Git history was cleaned into a single English-only release commit; no experimental-data deletion was performed.

The main PDF has **8 total pages**, including references and the AI use statement. The text uses the official ICLR 2027 style without changing its body font, line spacing, margins, or text area. This is a stricter total-PDF budget chosen for this release, rather than a statement that ICLR itself imposes an eight-page limit. The official submission limit is nine pages of main text with references excluded: [ICLR 2027 Author Guidelines](https://iclr.cc/Conferences/2027/AuthorGuidelines).

The supplement has **20 total pages**. It preserves all 160 probe rows and 20 seed outcome rows. Its opening map connects each main-paper topic to full details. Section I adds twelve explanations: the economic distinction; demand and static benchmarks; signal timing and saturation; GRU/PPO and action units; paired gains; invariance; bootstrap units; Bellman derivation; Gaussian derivatives; worked probe cases; welfare accounting; and the scope of the evidence. Section J ends with the public GitHub repository URL. The public URL identifies the repository owner, so a double-blind submission requires an anonymized artifact link instead.

## Mathematical and editorial checks

The rewrite retains the positive-denominator restriction `beta > alpha`, the explicit `beta <= alpha` case, the grid references 1.473/1.925, the corrected response-area estimate and CI, and the finite tail endpoint `T-1`. The period-payoff gap is called `h` in the main text and is explicitly identified with `Delta V` in the expanded derivation. Actor inputs, price/action units, finite horizon, statistical units, welfare provenance, and the missing added-noise combination rule remain explicit. Describing additional feedback pathways as potentially breaking invariance does not claim that every policy using such inputs must break it.

This was a self-review of the rewritten passages, using the prior verified arithmetic and archive results. No new independent-review claim or complete implementation audit is made. The supplied finite computation checks corroborate numerical examples; they are not a computational proof over all model parameters. No new policies were trained and no missing experimental outputs were invented.

## Rechecking available outputs

```bash
python3 scripts/verify_theory.py
python3 scripts/verify_archive.py --root . --output verification/archive-results.json
python3 scripts/render_figures.py
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
latexmk -pdf -interaction=nonstopmode -halt-on-error supplement.tex
```

The archive check compares all 800 printed probe-number cells, all 100 printed seed-outcome cells, the stored impulse-path area sums, paired/continuation bootstrap summaries and 20 final checkpoint SHA256 identities. It records input hashes and returns nonzero on detected inconsistencies. The raw experiment directory is unchanged. Within-policy intervals can only be compared to saved summaries because individual rollout arrays are absent.

Both PDFs were rendered and inspected, including the formulas, tables, reference page, expanded explanations and final repository page. Compiled labels/citations resolve, and final logs have no overfull boxes or unstable-reference warnings. Only the harmless disabled-shell-escape notice from `epstopdf` remains. On this host, `latexmk` needed `LC_ALL=C LANG=C` to avoid an unavailable locale; this did not change document layout.

`archive-results.json` records bounded archive postprocessing; `theory-results.json` records finite arithmetic checks. `validation.json` records the final artifact hashes, official-style identity, page counts, cleanup and coverage checks. Original simulator/training source, posterior/calibration inputs and individual rollout data remain unavailable, so full training/MCMC replication and simulator welfare semantics remain unverified.
