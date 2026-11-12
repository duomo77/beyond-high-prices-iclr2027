# Beyond High Prices: Auditing Information-Mediated Enforcement in Recurrent Pricing Agents

수정된 ICLR 2027 논문 원고, 보충자료(Supplementary Material), 이론 검증 보고서(영문/국문), 및 실험 아카이브(`acrl_suite_v4_research`)를 저장한 저장소입니다.

## 2026-11-12 재검증 및 수정

현재 검증 기록은 [재검증 보고서](referee/2026-11-12/report.md)와 [재계산 결과](referee/2026-11-12/archive-results.json)에 있습니다. Threshold 가정, welfare 정의와 저장 지표의 구분, 가격 기준값, rival-response area/CI, tail 인덱스, 문헌 비교를 수정했습니다. 160개 probe 행과 20개 seed 결과를 대조하고 20개 최종 checkpoint 해시를 확인했습니다. 그림은 저장 CSV/JSON에서 재생성합니다.

이 저장소는 **실험 결과 아카이브**입니다. 원래 trainer/simulator 소스·native binary·posterior·calibration 원자료·rollout 원자료가 없어 훈련 및 MCMC를 독립 재현할 수 없습니다. 해시는 파일 무결성 확인이며 구현이나 실험 결과 자체의 검증을 대신하지 않습니다. 기존 `THEORY_VERIFICATION_REPORT*.md`는 이전 검토 기록으로 보존합니다.

```bash
python3 scripts/verify_theory.py
python3 scripts/verify_archive.py --root . --output /tmp/bhp-archive-results.json
python3 scripts/render_figures.py
```

검증 스크립트는 Python 3와 NumPy, 그림 재생성은 Matplotlib을 사용합니다. 새로 학습하거나 checkpoint를 역직렬화하지 않습니다.

## Repository Structure / 폴더 구조

- **`main_corrected.tex` / `main_corrected.pdf`** — 수정 완료된 메인 논문 (8페이지 분량, Section 1.1 Research Gap 및 수정된 Proposition 2–3, Eqs. (6)–(11) 반영)
- **`main_paper_src/`** — 메인 논문 컴파일 가능한 LaTeX 전체 소스 (`main.tex`, `main.pdf`, ICLR 2027 스타일 파일, 그림 파일 `media/`, `rId27.png`, `rId31.png`)
- **`supplement_corrected.tex` / `supplement_corrected.pdf`** — 수정 완료된 보충자료 (Supplementary Material: 확장 증명, 문헌 비교표, GRU+PPO 세부 설정, 160개 counterfactual probe 결과 등)
- **`supplement_src/`** — 보충자료 컴파일 가능한 LaTeX 전체 소스 (`main.tex`, `main.pdf`, ICLR 2027 스타일 파일)
- **`THEORY_VERIFICATION_REPORT.md`** — 영문 이론 검증 및 3개 관점(게임이론·수학·MARL) 적대적 리뷰 보고서
- **`THEORY_VERIFICATION_REPORT_KO.md`** — 국문 이론 검증 및 수정사항 요약 보고서
- **`PROOF_PROGRESS.md` / `PROOF_STATE.md`** — 단계별(Step 1–6) 검증 진행 로그 및 상태 파일
- **`Beyond_High_Prices_P1_Theoretical_Correction_EN.md`** — 이론 수정 기준 문서(EN)
- **`notes/`** — 이론·수식 검토 및 심사평 반영 노트 (`Beyond High Prices Theory Corrections.md`, `Beyond High Prices Theory Corrections (1).md`)
- **`originals/`** — 수정 전 원본 PDF 및 원본 LaTeX zip 아카이브 (`Beyond High Prices Audit.pdf`, `Beyond High Prices Audit Supplementary Material.pdf`, `PPO Information Channel ICLR.pdf`, `PPO Information Channel.zip`, `Appendix ICLR.zip`)
- **`acrl_suite_v4_research/`** — 실험 스위트 아카이브 (`suite_manifest.json`, `summary.json`, `ppo_baseline/`, `ppo_ablated/`, `sac_baseline/` 포함 179개 파일)

## Compiling LaTeX Sources

```bash
cd main_paper_src && pdflatex main.tex && pdflatex main.tex
cd ../supplement_src && pdflatex main.tex && pdflatex main.tex
```
