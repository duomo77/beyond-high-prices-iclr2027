# Beyond High Prices

**Auditing Information-Mediated Enforcement in Recurrent Pricing Agents**

현재 원고는 **[본문 PDF](main.pdf)**와 **[Supplementary PDF](supplement.pdf)**입니다. 본문은 참고문헌과 AI 사용 문구를 포함해 전체 8페이지이며, 공식 ICLR 2027 스타일의 글자 크기·여백·본문 영역을 변경하지 않았습니다. Supplementary는 본문의 논리와 수식을 단계별로 확장하고 모든 seed/probe 표를 보존합니다. 마지막에 이 저장소 주소가 있습니다.

## 현재 파일

| 파일 / 폴더 | 내용 |
|---|---|
| `main.tex`, `main.pdf` | 쉽게 풀어쓴 8페이지 본문과 컴파일 소스 |
| `supplement.tex`, `supplement.pdf` | 확장 증명·설정·통계·160개 probe·상세 해설·저장소 주소 |
| `figures/` | 기록된 CSV/JSON에서 생성한 두 그림 |
| `iclr2027_conference.sty`, `.bst`, `natbib.sty`, `fancyhdr.sty` | 공식 ICLR 2027 배포본의 스타일 파일 |
| `acrl_suite_v4_research/` | 기존 실험 결과와 checkpoint; 이번 글 수정으로 변경하지 않음 |
| `scripts/` | 결과 재집계, 유한 산술 검산, 그림 생성 스크립트 |
| `verification/` | 현재 원고에 대한 검산 결과, 파일 해시, 설명 범위와 검수 기록 |

이전 PDF·ZIP, 중복 `*_corrected` 원고, 이전 소스 폴더와 오래된 검토 초안은 현재 파일 목록에서 삭제했습니다. 이전 revision은 Git 이력에서 복구할 수 있습니다.

## 읽는 순서

본문은 높은 가격과 동적 처벌의 차이, 시장과 관측, 가격 인하 실험, 실험 결과, 반복게임 기준, 해석과 한계 순서입니다. Supplementary의 첫 안내표가 각 주제를 A--I절의 자세한 설명에 연결합니다. I절은 수요 미분, 신호 지연, GRU/PPO, 반사실적 이익 분해, bootstrap, threshold 유도, 실제 probe 사례와 welfare를 독립적으로 풀어 설명합니다. J절에 저장소와 사용 가능한 자료를 기재했습니다.

## 컴파일과 검산

LaTeX이 설치된 환경에서 저장소 루트에서 실행합니다. Overleaf에서는 전체 파일을 올리고 `main.tex` 또는 `supplement.tex`를 main document로 선택하면 됩니다.

```bash
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
latexmk -pdf -interaction=nonstopmode -halt-on-error supplement.tex
python3 scripts/verify_theory.py
python3 scripts/verify_archive.py --root . --output verification/archive-results.json
python3 scripts/render_figures.py
```

Archive 검산은 NumPy, 그림 생성은 NumPy와 Matplotlib을 사용합니다. 모든 160개 probe 행, 20개 seed 결과, 20개 최종 checkpoint 해시를 확인합니다. 새로 훈련하거나 checkpoint를 역직렬화하지 않습니다.

## 확인 가능한 범위

이 저장소는 원 실험의 **결과 아카이브**입니다. 원래 trainer/simulator 소스·native binary·posterior·calibration 원자료·개별 rollout 자료는 제공되지 않습니다. 따라서 표·bootstrap 요약·파일 무결성을 검산할 수 있지만 실제 훈련·MCMC 재현, simulator의 welfare 계산과 `added_sigma` 결합 규칙까지 확인한 것은 아닙니다. 이 경계는 두 원고에 명시했습니다.

공식 ICLR 2027 지침은 [Author Guidelines](https://iclr.cc/Conferences/2027/AuthorGuidelines)에 있습니다. 제출 시 본문 상한은 9페이지이고 참고문헌은 제외되지만, 이 원고는 요청에 따라 PDF 전체를 8페이지로 맞췄습니다. 공개 저장소 주소는 소유자를 식별하므로, 익명 심사에 제출할 때는 supplementary 마지막 주소를 익명 artifact 링크로 바꿔야 합니다. 공식 스타일 원본은 [ICLR 2027 style files](https://media.iclr.cc/Conferences/ICLR2027/iclr-2027-style-files.zip)입니다.
