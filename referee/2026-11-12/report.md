# Summary

2026-11-12에 Git revision `b119bdce823da664f1fdc577efa82241e1042631`의 메인 논문과 supplement 전체를 검토했다. 공개 신호에 따른 반복게임의 유인 조건, Gaussian noise 비교정태, frozen-policy 불변성 증명, 20개 PPO job, 160개 probe, 2,000개 checkpoint 행을 대상으로 했다. 확인된 오류는 두 원고와 컴파일용 사본에 반영했다.

수학 검토와 저장 결과 재계산은 별도 에이전트가 수행했고, 통합 담당자가 근거와 수정 구간을 다시 확인했다. 수정된 수학 구간도 재검토했다. 이는 동일 모델 계열의 별도 검토이며, 독립적인 인간 심사나 원 실험의 재현을 의미하지 않는다. 모델/추론 설정은 기본 상속을 사용했고 호스트가 확인하지 않은 실제 설정값은 기록하지 않았다.

`main/`과 `supplement/`에는 수정 전 원문의 해시·section snapshot을 보존했다. 별도 에이전트의 임시 입력은 Git 원본과 마지막 개행 하나만 다르다는 점을 바이트 비교로 확인했다. 이전 `THEORY_VERIFICATION_REPORT*.md`는 과거 기록이며 이번 결과가 현재 검증 상태를 대체한다.

# Main mathematical concerns

1. **[Major, 수정] Proposition 2의 나눗셈 조건.** 원문은 `\beta\in(0,1]`을 허용하면서 $D=g(1-\alpha)+(\beta-\alpha)\Delta V$로 나눈다. $\alpha=.9,\beta=.1,g=\Delta V=1,\delta=.5$이면 $D=-.7$이므로 표시된 threshold는 만족하지만 실제 deviation gain은 $27/19>0$이다. 본문과 A.1에 $\beta>\alpha$를 명시했다. $\beta\leq\alpha$이면 양의 현재 이득을 억제할 수 없다는 예외도 별도로 기재했다. 이 제한 아래 Bellman 유도, feasibility 조건, Gaussian 미분과 극한은 재계산과 수식 검토에 부합한다.
2. **[Major, 수정 및 미확인 분리] 총잉여 정의.** 원문 Equation (3)의 `(v-c)(q1+q2)`는 항상 1보다 작지만 저장 지표는 약 1.1596이다. 이론적 총잉여를 outside option으로 정규화한 logit inclusive value와 생산자 이윤의 합으로 고쳤다. 저장값은 `mean_total_surplus` 필드에서 가져온 **archived welfare index**로 표·그림에 명시했다. simulator source가 없어 두 지표가 실제 구현에서 일치한다고 단정하지 않는다. 집계 평균값만으로 비선형 기간별 welfare를 복원할 수도 없다.
3. **[Major, 수정] 상대방 반응 누적 면적과 CI.** 원문의 `-3.7\times10^{-6}` 및 0을 포함하는 CI는 명시된 estimand와 맞지 않는다. 각 seed의 8개 probe 면적을 평균한 뒤 10개 seed를 resample하면 평균은 **−1.3628784654×10⁻⁵**, 95% CI는 **[−2.5298313631×10⁻⁵, −3.4169651190×10⁻⁶]**이다. 각 저장 면적은 impulse-response 경로의 합과도 일치한다. 수정 CI는 0을 제외하므로 “작은 하락 반응은 통계적으로 확인되지만, continuation deterrence를 입증하지 않는다”로 해석을 고쳤다.

# Other mathematical concerns

- **[Moderate, 수정] Grid/continuous benchmark 혼용:** 저장된 모든 elevation은 $p^N=1.473,p^J=1.925$를 사용한다. 이 정의의 최대 잔차는 $5.1\times10^{-16}$이다. 연속 FOC 해 $1.4729266600,1.9249809190$는 별도 검산값으로 구분했다. 실험 수치는 다시 정규화하지 않았다.
- **[Moderate, 수정] A.4 종료 인덱스:** 기간을 $0,\ldots,T-1$로 정의하고 omitted-tail 합의 상한을 $T-1$로 고쳤다. 이제 $H=T-t_0-1$일 때 합이 빈 합이다.
- **[Minor, 수정] 즉시 손실 비율:** informative cut 0.1과 0.3의 비율은 각각 **99.89827997%, 99.98971257%**다. 양쪽 모두 엄밀히 “over 99.9%”라는 문장을 근삿값 표현으로 고쳤다.
- **[Moderate, 수정] A.2 예시:** 가장 큰 현재 이득의 deviation을 억제해도 더 작은 deviation이 남을 수 있다는 논점에 맞게 예시를 고쳤다. threshold는 각각 $180/271$과 $60/59$이며, $\delta=.9$에서 전자만 억제된다. 이는 예시이며 새 실험 결과가 아니다.

Observation invariance는 기재된 frozen deterministic actor 입력·action independence·stationary payoff 가정하에 induction으로 성립한다. 전체 unilateral-action IC는 undivided 형태를 유지한다. 계산 스크립트의 유한 범위 검사는 이러한 보편 명제의 증명을 대신하지 않는다.

# Exposition and organization

본문과 supplement의 기준값·가정·기호를 일치시키고, full gain의 기준 시점과 discount exponent를 명시했다. 첫 checkpoint는 초기화가 아닌 **12,288 interactions 이후**이므로 초기 parameterization 때문이라는 단정을 삭제했다. 학습 곡선은 중간 상승이 있어 “declines overall”로 수정했다. 표의 음수 열과 문헌 비교표 폭을 고치고 그림은 CSV/JSON에서 재생성했다. 두 source 사본과 PDF 사본을 동기화했다.

# Claim and scope assessment

- Feature rank 증가를 report variance의 인과효과로 설명하던 문장을 descriptive 결과로 제한했다. CI가 0을 포함한다는 이유만으로 큰 효과가 없다고 단정하던 표현도 수정했다.
- Calvano et al. (2021)을 discrete-price 모형으로 소개하고 intervention을 observational path로만 설명한 것은 부정확하다. 확인한 저자 원고는 Cournot 수량 선택과 강제 output deviation을 사용한다. 본문·문헌 비교표를 고쳤다. 원문의 선행연구와 차별성에 대한 과장도 줄였다. [저자 원고, November 2020, §§3–4](https://ase.uva.nl/binaries/content/assets/subsites/amsterdam-school-of-economics/2020/calvano-calzolari-denicolo-and-pastorello-2020-algorithmic-collusion-with-imperfect-monitoring.pdf), [출판 논문 요약, 2021](https://www.sciencedirect.com/science/article/pii/S0167718721000059/pdfft?md5=9ef52fba38c4daa46dc1b5846f1455f7&pid=1-s2.0-S0167718721000059-main.pdf).
- Deng et al.의 비교 실험은 PPO도 **discrete-action variant**를 사용한다. 표에서 continuous/episodic으로 읽힐 수 있던 설명을 수정했다. 확인 범위는 [arXiv:2503.11270v1, §§4.2–5](https://arxiv.org/html/2503.11270v1)이다. 모든 인용문헌의 정리·prior art를 전수 재심사한 것은 아니다.
- 최종 paired CI, 160 probe의 800개 인쇄 수치 셀, 20 seed의 100개 최종 수치 셀은 원 저장 결과와 일치했다. 20개 최종 checkpoint SHA256도 모두 일치했다. Interaction **58,174,720**, 기록된 runtime **44.05644763시간** 역시 재집계됐다. 해시 일치는 파일과 metadata의 일관성을 의미한다.

# Questions for the authors

아래 입력은 저장소와 원본 ZIP에 없으므로 실제 구현·훈련·calibration 검증은 완료할 수 없다.

1. `acrl` Python package, native simulator source/binary, build instructions와 원래 실험 plan을 제공해야 report timing, GRU/PPO loss, welfare 구현을 검증할 수 있다.
2. `added_sigma=0.1`과 posterior $\sigma$가 effective innovation scale에 결합되는 규칙은 무엇인가? 현재 원고는 이 규칙을 미확인으로 표시하며 quadrature 등을 추측하지 않는다.
3. 원래 calibration labels/settings, retained posterior draws와 diagnostic summary가 있어야 posterior와 MCMC gate를 재계산할 수 있다. 현재 $\hat R$·ESS는 기록값만 확인했다.
4. 개별 rollout의 gain·가격·이윤·response 행렬이 있어야 within-policy conditional CI를 재생성할 수 있다. 이번에는 저장된 CI가 표와 일치하는지만 확인했다.

# Suggested revisions

확정된 원고 오류는 이 변경에 반영했다. 남은 우선순위는 위의 미공개 입력을 복원하고 해시와 구현을 확인하는 것이다. Positive control, moment-matched placebo, adaptive deviations 등은 기존 원고의 후속 실험 범위로 남겼으며 수행했다고 주장하지 않는다.

재계산 명령:

```sh
python3 scripts/verify_theory.py
python3 scripts/verify_archive.py --root . --output /tmp/bhp-archive-results.json
python3 scripts/render_figures.py
cd main_paper_src
pdflatex -no-shell-escape -interaction=nonstopmode -halt-on-error main.tex
pdflatex -no-shell-escape -interaction=nonstopmode -halt-on-error main.tex
cd ../supplement_src
pdflatex -no-shell-escape -interaction=nonstopmode -halt-on-error main.tex
pdflatex -no-shell-escape -interaction=nonstopmode -halt-on-error main.tex
```

# Overall assessment

가정하의 이론 결과와 공개된 실험 요약의 내부 일관성은 확인했고 발견한 오류를 수정했다. 작은 통계적 가격 반응을 continuation punishment와 구분한 핵심 결론은 유지된다. 다만 이 저장소만으로는 simulator·훈련·posterior의 독립 재현이나 논문 전체의 보편적 정확성을 보증할 수 없다. 최종 컴파일·시각 검수 기록과 해시는 `validation.json`에 보관한다.
