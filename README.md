# Beyond High Prices: Auditing Information-Mediated Enforcement in Recurrent Pricing Agents

수정된 ICLR 2027 논문 원고, 보충자료(Supplementary Material), 이론 검증 보고서(영문/국문), 및 실험 아카이브(`acrl_suite_v4_research`)를 저장한 저장소입니다.

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
