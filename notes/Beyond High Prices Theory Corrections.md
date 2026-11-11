# Beyond High Prices — 이론·수식 전수 검토 및 수정 지침서

> **대상 원고:** *Beyond High Prices: Auditing Information-Mediated Enforcement in Recurrent Pricing Agents*  
> **대상 보충자료:** *Beyond High Prices: ... Supplementary Material*  
> **작성 기준일:** 2026-11-11  
> **목적:** ICLR 2027 저자 수정·rebuttal·재투고에 사용할 수 있도록, **확인된 수학적 오류**, **코드 확인이 필요한 불일치**, **실험적 한계**를 구분하고 수식·증명·원고 문구의 수정 방향을 제시한다.
>
> **검증 범위:** 제출된 메인 PDF 8쪽과 Supplementary PDF 8쪽. 원시 실험 데이터, 실제 소스코드, posterior draws 및 전체 실행 archive는 제공되지 않았으므로, PDF의 수치와 수식의 내적 정합성까지 검토한다. 아래에 제안한 수식·수치 검산은 원고에 제시된 가정에 대한 독립 계산이며, 코드 수준 재현을 의미하지 않는다.

---

## 0. 핵심 결론 — 먼저 수정할 사항

| 우선순위 | 대상 | 판정 | 조치 |
|---|---|---|---|
| **P0** | 메인 Proposition 2, 식 (6), 증명 | **수학적 오류 확인** | 협력–처벌 가치 차이의 분모와 할인인자 임계값을 재유도 |
| **P0** | 메인 Proposition 2의 실행가능성 주장 | **필요충분조건 오류** | `β − α > 0`을 더 강한 조건으로 교체 |
| **P0** | 메인 식 (9) | **일탈 전체에 대한 조건 불완전** | 모든 기업·모든 행동에 대한 비나눗셈형 IC를 제시 |
| **P0** | Supplementary A.1·A.2·A.3 | **오류 반복 및 예제 산술 불일치** | 메인과 일치하는 새 증명·예제로 전면 교체 |
| **P0** | 메인 식 (3) 및 Table 1의 총잉여 | **수식–보고값 모순** | 실행코드의 실제 후생함수 확인 후 수식 또는 지표명 수정 |
| **P0** | 메인 Abstract의 95% CI | **부호 오기** | `[0.0241, 0.0288]` → `[-0.0241, 0.0288]` |
| **P1** | 메인 Proposition 3, 식 (10)–(11) | **중간 부호 및 극한 해석 오류** | Gaussian 표준화 부호 수정, 새로운 δ*로 비교정태 증명 |
| **P1** | 이론–PPO 연결 | **모형 범위 차이** | 무한기간·즉시 트리거 대 유한기간·지연 신호의 차이를 명시 |
| **P1** | 반사실적 감사의 타당성 | **검출력 미확인** | 실제 트리거 처벌을 삽입한 positive control을 새 실험으로 수행 |
| **P1** | 정보채널 비교 | **입력분포 교란 가능성** | moment-matched 행동독립 placebo 및 민감도 분석 검토 |
| **P2** | Supplementary의 전수표·해시 | **제시 범위/완성도 확인 필요** | PDF에 약속된 전체 probe 결과, 표 번호, 완전한 hash 정리 |

**중요한 구분:** 이론의 할인인자 임계값을 수정한다고 해서 기존 PPO 훈련 결과가 자동으로 무효가 되는 것은 아니다. Supplementary B.1은 이론적 임계 할인인자가 PPO 보상으로 들어가지 않으며 이윤은 logit 수요와 실제 가격으로 계산된다고 기술한다(보충자료 p.3). 다만 실험적 후생지표를 계산한 코드와 후처리 결과는 별도로 확인해야 한다.

---

## 1. 공통 표기와 정확한 가정

이론 부분은 **정상적 무한기간 반복게임**, **고정 공적 트리거 전략**, **흡수적 처벌 상태**를 가정한다.

| 표기 | 의미 |
|---|---|
| \(C\) | 협력(cooperation) 공적 상태 |
| \(P\) | 일단 진입하면 머무르는 흡수적 처벌(punishment) 상태 |
| \(\pi^C\) | 협력 상태에서 정해진 행동을 수행하는 기간당 이윤 |
| \(\pi^P\) | 처벌 상태의 기간당 이윤 (본문에서는 정태적 Nash 행동을 처벌로 사용) |
| \(\pi^D\) | 협력 상태에서 **한 기간만** 일탈한 경우의 현재 이윤 |
| \(g=\pi^D-\pi^C\) | 현재 일탈이익. 핵심 임계값 정리에서는 \(g>0\) |
| \(h=\pi^C-\pi^P\) | 협력–처벌 이윤격차. 핵심 정리에서는 \(h>0\) |
| \(\alpha\) | 협력을 지켰는데 나쁜 신호가 발생하는 확률(오경보) |
| \(\beta\) | 특정 일탈 후 나쁜 신호가 발생하는 확률 |
| \(\Delta=\beta-\alpha\) | 일탈로 인해 증가한 나쁜 신호 확률 |
| \(\delta\) | 할인인자, \(0\le\delta<1\) |
| \(V^C,V^P,V^D\) | 현재 행동 결정 **직전**의 협력·처벌·한 기간 일탈 가치 |

여기서 핵심 임계값 식의 증명은 \(g>0\), \(h>0\), \(\Delta>0\)에서 간결해진다. 모든 가능한 일탈에 관한 조건은 부호 제약 없이 표현하는 편이 정확하다.

**출처:** 메인 pp.5–6, Proposition 2, 식 (6)–(9); Supplementary p.1, A.1.

---

## 2. 메인 원고: 수식 (1)부터 순서대로 수정

### 2.1 식 (1): Logit 수요 — 수학적으로 유지

원문:

\[
q_i(p_i,p_j)=\frac{\exp((v-p_i)/\mu)}{1+\exp((v-p_i)/\mu)+\exp((v-p_j)/\mu)}.
\]

원고 모수: \(v=2\), \(c=1\), \(\mu=0.25\), 가격범위 \([1,2.5]\).

직접 미분하면

\[
\frac{\partial q_i}{\partial p_i}=-\frac{q_i(1-q_i)}{\mu},\qquad
\frac{\partial q_i}{\partial p_j}=\frac{q_iq_j}{\mu}.
\]

- **판정:** 식 자체는 맞다.
- **수정:** 불필요. 다만 실제 데이터에서 추정한 수요가 아니라 모수로 지정한 시뮬레이션 수요라는 사실을 유지한다.
- **근거:** 메인 p.2, 식 (1).

### 2.2 식 (2): 기업 이윤 — 수학적으로 유지

\[
\pi_i(p_i,p_j)=(p_i-c)q_i(p_i,p_j).
\]

내부 최적가격의 일차조건은

\[
\frac{\partial\pi_i}{\partial p_i}=q_i\left[1-\frac{p_i-c}{\mu}(1-q_i)\right]=0,
\]

따라서

\[
p_i=c+\frac{\mu}{1-q_i}.
\]

이 조건을 대칭적으로 수치해석하면 \(p^N\approx1.47292666\), 공동이윤 극대화 대칭가격은 \(p^J\approx1.92498092\)로, 원문 수치와 일치한다.

- **판정:** 식 자체는 맞다.
- **실험상의 함의:** 최종 평균가격 \(\bar p\approx1.479804\)는 \(p^N\) 근처다. 이 가격에서 강제 인하를 하면 미래 보복이 없어도 즉시 이윤이 감소한다.
- **독립 계산:** 상대 가격을 1.479804로 고정하면, 자기 가격을 0.075 인하할 때 즉시 이윤 변화는 약 `−0.00500129`, 0.225 인하할 때 약 `−0.05096403`이다. 이는 **평균가격을 대칭적으로 대입한 예시**이며 실제 seed·시점별 이윤을 재현한 값은 아니다.
- **근거:** 메인 p.2, 식 (2), pp.4–5, Tables 1–2.

### 2.3 식 (3): 총잉여 — **보고된 결과와 모순, 코드 대조 필수**

원문:

\[
TS_{\text{printed}}=(v-c)(q_1+q_2).
\]

현재 모수에서 \(v-c=1\), logit에 외부 대안이 있으므로 \(q_1+q_2<1\). 따라서 원문 수식은 항상 \(TS_{\text{printed}}<1\)이다.

그런데 메인 Table 1은 `1.159588` 및 `1.159660`을 보고한다. **수식이 적힌 그대로라면 불가능하다.**

코드가 통상적인 logit 소비자잉여와 기업이윤을 합했다면, 적절한 표준 공식은

\[
CS(p_1,p_2)=\mu\log\left(1+\sum_{i=1}^2e^{(v-p_i)/\mu}\right),
\]

\[
\boxed{TS=CS+\sum_{i=1}^2(p_i-c)q_i.}
\]

이는 선택확률 \(q_0=1-q_1-q_2\)를 두면

\[
TS=(v-c)(q_1+q_2)-\mu\sum_{k=0}^2 q_k\log q_k
\]

와 동치이다(외부 대안의 결정적 효용을 0으로 정규화한 표준 logit 표현).

**수치 진단:** \(p_1=p_2=1.479804\)를 위 표준 공식에 넣으면 `TS ≈ 1.16023510`으로 본문 결과와 규모가 유사하다. 그러나 평균가격에 함수를 대입한 값은 이질적 에피소드별 TS의 평균과 같을 필요가 없으므로 이는 **코드 사용 공식을 시사하는 근거이지 증명은 아니다**.

**수정 절차**
1. 이윤과 소비자잉여를 산출한 실제 실행 함수 및 후처리 함수를 연다.
2. 각 시점 TS가 `log-sum + profits`인지, `(v-c)*(q1+q2)`인지, 다른 정규화인지 확인한다.
3. 실제 계산에 사용한 수식으로 본문 식 (3)을 교체한다. 둘이 다르면 결과표 또는 코드도 적절히 재계산한다.
4. 동일 입력가격으로 코드–원고 수식의 단위테스트를 작성한다.
5. 본문 Table 1과 Supplementary Table 3의 surplus 열까지 동일한 정의로 검산한다.

**금지:** 코드를 보지 않고 무조건 `TS=CS+Π`를 실제 구현 공식이었다고 단정하지 말 것.

### 2.4 번호 없는 정규화 가격상승도 \(E\) — 유지

\[
E=\frac{\bar p-p^N}{p^J-p^N}.
\]

- **판정:** 정상적인 기준가격 정규화.
- **주의:** 확률, 합법적 담합 판정, 균형 인증 지표가 아니다. \(E<0\), \(E>1\)도 가능한 비절단 지표이다.
- **근거:** 메인 p.2, 정의; Supplementary p.4의 음의 elevation 사례.

### 2.5 식 (4): 신호 평균의 가격 매핑 — 수식은 유지, 검출 민감도 경고

원문(하한·상한 클램핑 포함):

\[
m_t=\theta_{lo}+(\theta_{hi}-\theta_{lo})\frac{\min(p_{1,t},p_{2,t})-p^N}{p^J-p^N},
\qquad m_t\in[\theta_{lo},\theta_{hi}].
\]

- \(\min(p_1,p_2)\le p^N\)이면 \(m_t=\theta_{lo}\).
- \(p^N<\min(p_1,p_2)<p^J\)에서만 해당 최소가격에 대한 기울기가 존재하고 양수일 수 있다.
- \(\min(p_1,p_2)\ge p^J\)이면 \(m_t=\theta_{hi}\).
- `min`의 두 인수가 같은 지점과 clipping 경계에서는 일반적인 의미의 미분가능성이 없을 수 있다.

**문제:** 최종 정책이 Nash 근처이면 강제 가격인하의 일부 구간에서 신호 평균이 하한에 포화된다. 크기가 다른 두 일탈을 관측 신호로 구별하기 어려울 수 있다.

**조치:** `nonsaturating map`, `small/adaptive cuts`, 유의미하게 높은 협력가격의 positive control을 추가한다. 수학적 오기는 아니므로 필수 *이론 수정*과 *추가 실험*을 구분한다.

### 2.6 식 (5): 잡음 신호 — 식은 유지, 조건부/주변분포 및 시차 구분

\[
r_{t+1}=\frac{m_t+m_{t-1}}{2}+\varepsilon_t,\qquad\varepsilon_t\sim N(0,\sigma_\varepsilon^2).
\]

- **판정:** 조건부 생성식은 맞다. 잡음이 없는 두 평균을 합친 후 **잡음 한 번**을 넣는다.
- **주의:** posterior에서 신호 모수를 에피소드 단위로 무작위 추출하므로 모수를 적분한 주변 신호분포는 일반적으로 단일 Gaussian일 필요가 없다.
- **시차:** Supplementary B.2 설명에 따르면 \(t\)기의 가격개입이 \(t+2\)기의 행동에 처음 반영될 수 있다. 무한기간 이론의 즉시 트리거와 그대로 동일시하지 말 것.
- **비교실험:** ablation은 \(N(1.6,0.4^2)\) 행동독립 신호로 대체하지만 신호의 주변 평균·분산·분포 전체를 정확히 보존하지는 않는다. 따라서 **순수한 정보량 제거 효과**로 단정하면 안 된다.

---

## 3. Proposition 2 — 메인 핵심 정리의 완전한 수정

### 3.1 어디서 오류가 발생하는가?

원문 식 (7), (8)은 다음과 같다.

\[
\tag{7} V^C=\pi^C+\delta[(1-\alpha)V^C+\alpha V^P],
\]

\[
\tag{8} V^D=\pi^D+\delta[(1-\beta)V^C+\beta V^P].
\]

그리고 처벌 상태는 흡수적이므로

\[
V^P=\pi^P+\delta V^P.
\]

**이 Bellman 방정식들 자체는 맞다.** 문제는 원문 p.6에서 이 식들로부터

\[
V^C-V^P=\frac{\pi^C-\pi^P}{1-\delta}
\]

라고 계산한 부분이다. \(\alpha>0\)이면 이것은 틀린 식이다.

### 3.2 올바른 가치 차이의 단계별 증명

협력식에서 처벌식을 뺀다.

\[
\begin{aligned}
V^C-V^P
&=\pi^C-\pi^P\\
&\quad+\delta[(1-\alpha)V^C+\alpha V^P-V^P]\\
&=h+\delta(1-\alpha)(V^C-V^P).
\end{aligned}
\]

따라서

\[
\boxed{V^C-V^P=\frac{h}{1-\delta(1-\alpha)}.}\tag{A}
\]

여기서 \(\delta<1\)이므로 \(1-\delta(1-\alpha)>0\).

일탈식을 협력식에서 빼면

\[
\begin{aligned}
V^D-V^C
&=\pi^D-\pi^C
+\delta[(1-\beta)-(1-\alpha)]V^C
+\delta(\beta-\alpha)V^P\\
&=g-\delta(\beta-\alpha)(V^C-V^P)\\
&=g-\delta\Delta\frac{h}{1-\delta(1-\alpha)}.
\end{aligned}
\]

이 일탈이 불리하려면 \(V^D\le V^C\), 즉

\[
\boxed{g[1-\delta(1-\alpha)]\le\delta\Delta h.}\tag{IC-single}
\]

**이 식이 가장 안전한 원형 유인제약이다.** \(\Delta\)나 \(g\)의 부호가 바뀌어도 부적절한 나눗셈을 피할 수 있다.

### 3.3 수정된 임계 할인인자 (식 6 교체)

\(g>0\), \(h>0\), \(\Delta>0\)라면 위 조건은

\[
g\le\delta[g(1-\alpha)+\Delta h]
\]

와 동치이므로

\[
\boxed{
\delta\ge\delta^*_{\rm corrected}
=\frac{g}{g(1-\alpha)+(\beta-\alpha)h}.
}\tag{6-revised}
\]

**인쇄된 기존 식**

\[
\delta^*_{\rm printed}=\frac{g}{g+(\beta-\alpha)h}
\]

은 오경보가 협력 상태의 존속가치에 미치는 영향을 누락한다.

### 3.4 실행가능성 조건(존재 명제) 반드시 교체

원문은 \(\delta^*<1\)일 필요충분조건을 \(\beta>\alpha\)로 서술한다. 실제로는

\[
\delta^*<1
\iff g<g(1-\alpha)+\Delta h
\iff\boxed{\Delta h>\alpha g}.
\]

즉,

\[
\boxed{(\beta-\alpha)(\pi^C-\pi^P)>
\alpha(\pi^D-\pi^C)}
\]

가 \(\delta<1\)인 할인인자로 **해당 특정 일탈**을 억제할 수 있기 위한 필요충분조건이다(위의 양의 이익 및 확률가정 아래).

- `>`: 어떤 \(\delta<1\)에서 억제가 가능하다.
- `=`: 임계값이 1이므로 \(\delta<1\)에서는 불가능하다.
- `<`: 임계값이 1보다 크므로 불가능하다.

**경제학적 의미:** 단지 일탈의 적발확률이 협력의 오경보확률보다 큰 것만으로는 부족하다. 협력이 잘못 종료될 위험까지 상쇄할 미래 이익 격차가 필요하다.

### 3.5 반례: 원문과 수정식은 서로 다른 결론을 낸다

\[
g=0.2,\qquad h=0.5,\qquad \alpha=0.4,\qquad\beta=0.5.
\]

원문 계산:

\[
\delta^*_{\rm printed}=\frac{0.2}{0.2+0.1\cdot0.5}=0.8.
\]

수정 계산:

\[
\delta^*_{\rm corrected}=
\frac{0.2}{0.2(1-0.4)+0.1\cdot0.5}
=\frac{0.2}{0.17}\approx1.176470588.
\]

따라서 원문은 \(\delta=0.9\)라면 억제된다고 판단하지만, 수정된 이론에서는 **어떤 \(\delta<1\)도 그 일탈을 억제할 수 없다**.

### 3.6 수정 후 주장 가능한 범위

- **증명 가능:** 정의된 고정 트리거 전략에서 **명시한 한 기간 일탈**에 대한 정확한 유인제약.
- **아직 증명되지 않음:** PPO가 그 트리거 전략을 학습했다는 것.
- **아직 증명되지 않음:** 모든 일탈행동·모든 공적 이력에서 완전한 반복게임 균형이라는 것.
- **증명되지 않음:** 높은 평균가격 자체가 담합의 충분조건이라는 것.

---

## 4. 식 (9): 단일 일탈에서 모든 행동으로 확장

기업 \(i\)의 협력행동이 \(a_i^C\)일 때, 모든 일탈 \(a_i\in\mathcal A_i\)에 대해

\[
g_i(a_i)=\pi_i(a_i,a_{-i}^C)-\pi_i^C,
\]

\[
\beta_i(a_i)=\Pr(\text{bad public signal}\mid a_i,a_{-i}^C),
\quad \Delta_i(a_i)=\beta_i(a_i)-\alpha_i,
\]

\[
h_i=\pi_i^C-\pi_i^P
\]

로 정의하자. 그때 협력 상태에서 한 기간의 일탈이 모두 억제되기 위한 직접적 조건은

\[
\boxed{
\forall i,\ \forall a_i\in\mathcal A_i:\quad
 g_i(a_i)[1-\delta(1-\alpha_i)]
 \le\delta\Delta_i(a_i)h_i.
}\tag{9-revised / full-IC}
\]

**왜 원문 식 (9)가 부족한가?** 가장 큰 \(g_i\)를 갖는 행동이 가장 탐지하기 어려운 행동과 같을 필요가 없다. 억제의 난이도는 현재 이익과 탐지확률 증가분의 조합으로 결정된다.

\(g_i(a_i)>0\), \(\Delta_i(a_i)>0\), \(h_i>0\)인 일부 행동군에 한정하면

\[
\delta\ge\sup_{i,a_i:g_i>0,\Delta_i>0}
\frac{g_i(a_i)}{g_i(a_i)(1-\alpha_i)+\Delta_i(a_i)h_i}
\]

라고 쓸 수 있다. **그러나 이것만으로 일반적인 full-IC와 동치라고 쓰지 말 것.** 특히 \(g_i\le0\)이면서 \(\Delta_i<0\)인 행동은 즉시 이익은 적어도 미래의 오경보 위험을 줄여 유리해질 수 있다. 따라서 안전한 정식화는 먼저 제시한 비나눗셈형 불등식이다.

추가 조건: 처벌 상태의 행동이 실제로 최적반응인지, 다른 공적 이력에서 일탈 유인이 없는지 확인해야 반복게임 균형을 주장할 수 있다. 흡수적 처벌에 정태적 Nash 프로필을 지정했다는 가정은 이 일부를 뒷받침하지만, 협력 상태의 모든 가능한 행동은 별도의 검증 대상이다.

---

## 5. 식 (10) 및 Proposition 3: Gaussian 잡음 비교정태

### 5.1 수정된 할인인자에 대한 편미분

\[
D=g(1-\alpha)+(\beta-\alpha)h,
\qquad \delta^*=g/D.
\]

\(g,h>0\), \(\beta>\alpha\)를 고정한 편미분은

\[
\boxed{\frac{\partial\delta^*}{\partial\alpha}
=\frac{g(g+h)}{D^2}>0,}
\]

\[
\boxed{\frac{\partial\delta^*}{\partial\beta}
=-\frac{gh}{D^2}<0,}
\]

\[
\boxed{\frac{\partial\delta^*}{\partial h}
=-\frac{g(\beta-\alpha)}{D^2}<0.}
\]

**판정:** 메인 식 (10)의 **부호 결론은 맞다.** 단, 정확한 임계값에서 다시 유도한 위 미분식으로 증명을 교체해야 한다.

### 5.2 식 (11)의 미분식은 맞지만, 증명 속 표준화 변수 부호는 반대

가정:

\[
S\mid C\sim N(\mu_C,\sigma^2),\quad
S\mid D\sim N(\mu_D,\sigma^2),\quad
\mu_D<\tau<\mu_C.
\]

나쁜 신호를 \(S<\tau\)로 정의하면

\[
\alpha(\sigma)=\Phi(z_C),\qquad
\beta(\sigma)=\Phi(z_D),
\]

\[
z_C=\frac{\tau-\mu_C}{\sigma}<0,\qquad
z_D=\frac{\tau-\mu_D}{\sigma}>0.
\]

**원문 증명에 적힌** `z_D < 0 < z_C`는 오류이며 정확히 `z_D > 0 > z_C`로 교체해야 한다.

\[
\Delta(\sigma)=\Phi(z_D)-\Phi(z_C)
\]

이므로

\[
\boxed{
\frac{\partial\Delta}{\partial\sigma}
=-\frac{1}{\sigma}[z_D\phi(z_D)-z_C\phi(z_C)]<0.
}\tag{11: retained formula, corrected sign argument}
\]

여기서 식 (11) **자체는 맞고 부호를 설명한 문장이 틀렸다.**

### 5.3 수정된 \(\delta^*(\sigma)\)의 정확한 전미분

\[
\alpha'(\sigma)=-\frac{z_C\phi(z_C)}{\sigma}>0,
\qquad
\beta'(\sigma)=-\frac{z_D\phi(z_D)}{\sigma}<0.
\]

그러므로

\[
\begin{aligned}
\frac{d\delta^*}{d\sigma}
&=-\frac{g}{D^2}\frac{dD}{d\sigma}\\
&=\boxed{\frac{g}{D^2}\big[(g+h)\alpha'(\sigma)-h\beta'(\sigma)\big]>0.}
\end{aligned}
\]

즉, **평균·문턱·행동·이윤격차가 고정된 Gaussian 트리거 모형에서** 신호 잡음이 증가하면 임계 할인인자는 엄격히 증가한다. 이 결론은 맞으며 정확하게 다시 증명할 수 있다.

### 5.4 극한값 수정 (메인 p.6, Supplementary A.3)

\(\sigma\to0\)에서는 \(\alpha\to0\), \(\beta\to1\). 따라서

\[
\boxed{\lim_{\sigma\to0}\delta^*(\sigma)=\frac{g}{g+h}>0.}
\]

Supplementary A.3의 `threshold tends to 0`은 **틀림**. 현재 이익 \(g>0\)을 미래 손실이 억제하려면 감시가 완벽해도 일정 수준의 인내심이 필요하다.

\(\sigma\to\infty\)에서는 \(\alpha,\beta\to1/2\)이므로

\[
\boxed{\lim_{\sigma\to\infty}\delta^*(\sigma)=2.}
\]

이 `2`라는 극한은 **수정된 임계값 수식과 일치**한다. 반면 원문에 인쇄된 잘못된 \(g/[g+\Delta h]\)를 그대로 사용하면 극한은 1이므로 서로 불일치한다.

\(\delta^*(\sigma)>1\)은 경제적으로 가능한 할인인자가 1보다 크다는 뜻이 아니라 **해당 고정 트리거 전략으로 일탈을 억제할 수 없다는 수학적 판정**이다.

### 5.5 추가적인 독립 Gaussian 잡음의 표준편차

Supplementary A.3은 \(\sigma_{tot}=\sqrt{\sigma^2+\sigma_a^2}\)를 제시한다. \(\sigma>0\)이면

\[
\frac{d\sigma_{tot}}{d\sigma_a}=\frac{\sigma_a}{\sigma_{tot}}.
\]

따라서

\[
\frac{d\delta^*}{d\sigma_a}
=\frac{d\delta^*}{d\sigma_{tot}}\frac{\sigma_a}{\sigma_{tot}}.
\]

이는 \(\sigma_a>0\)에서 양수이고, \(\sigma_a=0\) 경계에서는 0이다. **본문–보충자료 간 이 부분은 유지 가능하되 새 \(\delta^*\)를 사용해야 한다.**

---

## 6. Supplementary의 직접 수정 지점

### 6.1 A.1 — 메인과 같은 Bellman 오류가 반복됨 (p.1)

| 교체 위치 | 기존 | 수정 |
|---|---|---|
| 가치차이 | \((\pi^C-\pi^P)/(1-\delta)\) | \((\pi^C-\pi^P)/[1-\delta(1-\alpha)]\) |
| 임계값 | \(g/[g+\Delta h]\) | \(g/[g(1-\alpha)+\Delta h]\) |
| 실행가능성 | \(\beta>\alpha\) | \(\Delta h>\alpha g\), \(g,h>0\) |
| 설명 | 단순 탐지 격차 | 오경보가 협력가치를 직접 낮추는 효과 포함 |

**주의:** 바꾼 결과를 재검산하지 않은 채 원문의 `proof`를 그대로 보존하지 말 것.

### 6.2 A.2 — 숫자 예시 산술 불일치 및 \(\alpha\) 누락 (p.1)

원문은 \(h=1\)인 두 일탈에 대해:

1. \(g=0.3\), \(\Delta=0.5\), 본문 주장 임계값 `0.588235`.
2. \(g=0.9\), \(\Delta=0.01\), 본문 주장 임계값 `0.990099`.

그러나 **원문 인쇄식 자체**에 대입해도 각각

\[
\frac{0.3}{0.3+0.5}=0.375,
\qquad
\frac{0.9}{0.9+0.01}=0.989010989\ldots
\]

이다. 따라서 두 주장 모두 원문 산술과 일치하지 않는다.

한편 **수정된 임계값**을 계산하려면 \(\alpha\)를 추가로 지정해야 한다. 예시로 \(\alpha=0.05\)로 고정하고 \(\beta_1=0.55\), \(\beta_2=0.06\)를 쓰면

\[
\delta_1^*=\frac{0.3}{0.3(0.95)+0.5}=0.382165605\ldots,
\]

\[
\delta_2^*=\frac{0.9}{0.9(0.95)+0.01}=1.040462428\ldots.
\]

두 번째 일탈은 \(\delta<1\)로 억제할 수 없다. 이 예시는 **새로 제안한 설명용 수치**이며 실제 실험자료에서 추정한 값이 아니다.

**수정 권고:** A.2에 `α=0.05`를 명시하고 위 수치를 사용하거나, 다른 일관된 확률·이윤 파라미터로 전면 교체한다.

### 6.3 A.3 — 잡음 비교정태의 양끝 극한 수정 (p.2)

- `as σ→0, threshold tends to 0` → **`threshold tends to g/(g+h)`**.
- `as σ→∞, threshold tends to 2` → **올바른 새 임계값 기준으로 유지**.
- 잡음 증가의 미분 증명 → 위 **5.3절**의 \(D\) 기반 미분으로 교체.
- 추가 Gaussian 잡음에 관한 \(\sigma_a=0\) 경계 논의 → **유지**.

### 6.4 A.4 — 관측 불변성·유한 감사기간 bound는 조건부로 유지 (p.2)

행동독립적 신호, 동일한 초기 history/난수, 고정 결정론적 정책, 신호 외의 행동 의존적 입력 없음이 성립하면, 개입 후 미래의 정책입력이 같아지는 귀납증명은 타당하다.

또한 \(\pi\in[0,B]\)에서 두 분기의 한 기간 이윤 차이 절댓값은 \(B\) 이하이므로 누락 꼬리의 할인합 bound

\[
\left|\sum_{t=t_0+H+1}^{T}\delta^{t-t_0}(\pi_t^{cut}-\pi_t^{ctrl})\right|
\le \frac{B\delta^{H+1}}{1-\delta}
\]

는 올바른 상계이다. 본문 및 Supplementary의 설정은 \(B=1.5\)를 정당화한다(가격–비용 ≤1.5, 수요 ≤1). 다만 **이 bound가 전체 연속행동공간에서의 균형을 증명하는 것은 아니다.**

### 6.5 기타 Supplementary 완성도 수정

- p.5에 `Tables 5–??`라는 미완성 교차참조가 남아 있다. 정확한 표 번호로 교체.
- p.1에서 `all 160 conditional price-cut estimates`를 수록한다고 하지만, 첨부된 PDF p.6 Table 5는 일부 행만 제시하고 있다. **실제 전체 수록 또는 명확한 archive 링크/범위 설명**이 필요.
- p.6 SHA256 표는 해시 중간이 `...`로 축약돼 있다. 독립 검증을 주장하려면 전체 해시를 별도 텍스트/manifest로 제공하고 PDF에서 이를 참조하는 편이 좋다.
- 원시 posterior calibration 관측치와 실제 실행 binary는 제공되지 않았다고 명시되어 있으므로, 완전 재현을 주장하지 말 것.

---

## 7. 이론과 PPO 결과 사이의 연결을 어떻게 다시 쓸 것인가

### 7.1 관측 불변성(메인 Proposition 1): 유지 가능

독립 신호, 결합된 동일 난수, 고정 결정론적 정책, 보고 history와 시간만을 입력받는 조건에서는 한 시점의 가격개입 후 다음부터 관측이 동일하므로 미래 행동도 동일하다. 이는 **exact negative control**로 적절하다.

단, 이는 **구조상 0이 되는 결과**이지, 그 자체로 담합 감지기의 검출력(sensitivity)을 증명하지 않는다.

### 7.2 메인 Proposition 2–3는 PPO에 직접 적용한 정리가 아님

이론에서는 무한기간, 흡수적 처벌 상태, 즉시 반영되는 공적 이진 트리거를 가정한다. 실제 PPO 실험은

- 512기간 유한 에피소드;
- 종료시점 정보가 들어오는 정책;
- 연속 Gaussian 신호, 평균 및 delivery delay;
- 매 관측에서 32개 window로 재계산되는 GRU;
- posterior-conditional 신호 모수;
- frozen deterministic deployment;

를 사용한다.

따라서 **`Proposition 3 proves PPO noise weakens collusion`**과 같은 문장은 사용하면 안 된다. 정확한 표현은 **`The propositions characterize a fixed trigger benchmark; the PPO experiments audit learned policies separately.`**이다.

### 7.3 가장 강한 추가 실험: Positive control

**목적:** 현재 감사 절차가 **실제로 집행이 존재할 때** 감지할 능력이 있는지 검증.

1. 정태적 Nash보다 높은 협력 가격을 고정하고, 가격인하의 즉시 이익 \(g>0\)를 확인.
2. \(\alpha,\beta\) 및 할인인자를 선택하여 **수정된 IC**를 만족하는 트리거 정책을 구성.
3. 개입 후 현재 이익이 양수이고 미래 이익 차이가 음수이며 총 일탈이익이 비양수인지 확인.
4. signal saturation에 걸리지 않는 probe와 걸리는 probe를 모두 검사.
5. 비교를 위해 보복이 없는 정책을 negative control로 포함.
6. 검출률·오탐률을 다수 parameter settings에 걸쳐 보고.

**주의:** 이것은 아직 수행되지 않은 새로운 실험 제안이지 기존 PDF에 들어 있는 결과가 아니다.

### 7.4 정보채널에 대한 주장 수준

기존 실험은 `informative`와 `action-independent N(1.6,0.4²)`를 비교한다. 행동 의존성을 제거하면서 신호 분포도 바뀔 수 있다. 따라서

- **현재 주장 가능:** 정의한 *channel replacement*와 재학습에 따른 실험적 차이.
- **현재 주장 곤란:** 입력의 모든 분포적 특성을 고정한 순수 정보량 효과.
- **권고:** 독립 신호의 marginal moment/distribution matching, history/architecture control, 여러 noise-scale sweep.

### 7.5 추론 강도를 정확히 서술

- Informative 조건의 continuation loss는 Supplementary Table 4에서 작은 음수로 추정되며 반올림된 구간이 0을 포함하지 않는다. **정확히 0이라고 주장하지 않는다.**
- 다만 전체 가격인하 손익에 비해 크기가 매우 작고, 상대방 보복의 독립적인 인과효과라고 바로 해석할 수 없다.
- 가격상승도 차이의 95% 신뢰구간은 0을 포함하므로, **통계적으로 차이를 분해하지 못했다**고 말해야 한다. `no effect proven`, `equivalence established`라고 쓰면 안 된다.
- 10개 시드가 독립적인 학습 반복 단위다. 128 paired rollouts나 100개 checkpoint를 독립 학습 관측치로 계산하지 말 것.

---

## 8. 실제 원고에 바로 교체할 수 있는 영문 문안

> **주의:** 아래는 저자가 수학적 검산을 완료했다는 전제 아래에 사용할 수 있는 **제안 교체문**이다. 아직 수정하지 않은 원고나 제출하지 않은 결과에 대해 `we have fixed`처럼 완료를 주장하지 말 것.

### 8.1 Main Proposition 2 — replacement theorem and proof

```text
Proposition 2 (Corrected incentive threshold under false alarms).
Consider a stationary repeated game with a cooperative public state C
and an absorbing punishment state P. Let the per-period payoffs be
pi^C and pi^P, with h = pi^C - pi^P > 0. A specified one-period
deviation yields immediate gain g = pi^D - pi^C > 0. Let alpha denote
the probability of a bad public signal after compliance, and beta the
probability after the deviation. Assume 0 <= alpha < beta <= 1 and
0 <= delta < 1. The specified deviation is unprofitable in C if and
only if

    delta >= g / [g(1 - alpha) + (beta - alpha) h].

A discount factor strictly below one satisfying this condition exists
if and only if (beta - alpha) h > alpha g.

Proof. The Bellman equations are

    V^C = pi^C + delta[(1 - alpha)V^C + alpha V^P],
    V^P = pi^P + delta V^P.

Therefore,

    V^C - V^P = h/[1 - delta(1 - alpha)].

The one-period deviation obeys

    V^D - V^C = g - delta(beta - alpha)(V^C - V^P).

Thus V^D <= V^C is equivalent to

    g[1 - delta(1 - alpha)] <= delta(beta - alpha)h,

which yields the stated threshold. The threshold is below one exactly
when (beta - alpha)h > alpha g. QED.

This result is conditional on the specified deviation and the fixed
trigger automaton. Incentive compatibility for the full action space
requires checking every unilateral deviation for every firm.
```

### 8.2 Full-IC condition — replacement paragraph

```text
For every firm i and every unilateral action a_i, define its current
gain g_i(a_i), the bad-signal probability beta_i(a_i), the compliant
false-alarm probability alpha_i, and the cooperative-punishment payoff
gap h_i. The cooperative state is one-shot-deviation compatible only
if, for all i and a_i,

    g_i(a_i)[1 - delta(1 - alpha_i)]
      <= delta[beta_i(a_i) - alpha_i] h_i.

This undivided inequality also covers actions with nonpositive current
gains or changes in signal probabilities of either sign. Checking only
the deviation with the largest immediate gain is insufficient.
```

### 8.3 Main Proposition 3 — replacement theorem and proof

```text
Proposition 3 (Restricted Gaussian-noise comparative statics).
Maintain the assumptions of Proposition 2. For a fixed public-signal
threshold tau with mu_D < tau < mu_C, let

    alpha(sigma) = Phi((tau - mu_C)/sigma),
    beta(sigma)  = Phi((tau - mu_D)/sigma), sigma > 0.

Holding both means, the threshold, actions, and payoff differences
fixed, the corrected incentive threshold delta*(sigma) strictly
increases in sigma wherever defined by the formula.

Proof. Put z_C = (tau - mu_C)/sigma < 0 and
z_D = (tau - mu_D)/sigma > 0. Then

    alpha'(sigma) = -z_C phi(z_C)/sigma > 0,
    beta'(sigma)  = -z_D phi(z_D)/sigma < 0.

Let D(sigma) = g[1 - alpha(sigma)]
               + [beta(sigma) - alpha(sigma)]h.
Then

    d delta*/d sigma
      = (g/D(sigma)^2)[(g + h)alpha'(sigma) - h beta'(sigma)] > 0.

As sigma tends to zero, delta* tends to g/(g + h).
As sigma tends to infinity, delta* tends to 2. Consequently, the
specified trigger deviation becomes infeasible for delta < 1
when the threshold reaches or exceeds one. QED.

This comparative static does not describe how retrained PPO policies
respond to noise changes; it applies to the stated fixed trigger rule.
```

### 8.4 Welfare definition — conditional replacement only after code verification

```text
If the implementation computes logit consumer surplus plus total
firm profits, replace equation (3) by

    CS(p1,p2) = mu log[1 + exp((v-p1)/mu) + exp((v-p2)/mu)],
    TS(p1,p2) = CS(p1,p2) + sum_i (p_i - c)q_i(p1,p2).

Verify this formula against the actual implementation and all reported
surplus columns before treating it as the executed welfare measure.
```

---

## 9. 최소 재검산 코드 (원고·보충자료 수치 검사용)

아래 코드는 **원고의 발표 숫자가 내부 수식과 맞는지 확인하는 간단한 검산**이며, 논문의 PPO/MCMC 실행코드를 대체하지 않는다. Python 표준 라이브러리만 사용한다.

```python
import math

v, c, mu = 2.0, 1.0, 0.25


def demand(p1, p2):
    a = math.exp((v - p1) / mu)
    b = math.exp((v - p2) / mu)
    den = 1.0 + a + b
    return a / den, b / den


def profit1(p1, p2):
    q1, _ = demand(p1, p2)
    return (p1 - c) * q1


def printed_TS(p1, p2):
    return (v - c) * sum(demand(p1, p2))


def standard_logit_TS(p1, p2):
    q1, q2 = demand(p1, p2)
    cs = mu * math.log1p(math.exp((v - p1) / mu)
                         + math.exp((v - p2) / mu))
    return cs + (p1 - c) * q1 + (p2 - c) * q2


def delta_correct(g, h, alpha, beta):
    den = g * (1.0 - alpha) + (beta - alpha) * h
    return g / den


def delta_printed(g, h, alpha, beta):
    return g / (g + (beta - alpha) * h)


def Phi(x):
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


# 1) 원문 후생식은 1을 넘을 수 없음
p = 1.479804
assert printed_TS(p, p) < 1.0
assert abs(standard_logit_TS(p, p) - 1.1602350956576126) < 1e-10

# 2) 정태적 이윤: Nash 부근의 가격인하 손실
assert abs(profit1(p - 0.075, p) - profit1(p, p)
           - (-0.00500129122538)) < 1e-10
assert abs(profit1(p - 0.225, p) - profit1(p, p)
           - (-0.05096402514482)) < 1e-10

# 3) Proposition 2: 기존 식과 수정 식의 서로 다른 판정
assert abs(delta_printed(.2, .5, .4, .5) - .8) < 1e-12
assert abs(delta_correct(.2, .5, .4, .5)
           - 1.176470588235294) < 1e-12

# 4) Supplementary A.2 예시 (새로 지정한 alpha=0.05)
assert abs(delta_correct(.3, 1, .05, .55) - .3821656050955414) < 1e-12
assert abs(delta_correct(.9, 1, .05, .06) - 1.0404624277456649) < 1e-12

# 5) Gaussian 비교정태가 증가하는지 예시 확인

def delta_gauss(sig, g=.2, h=.5, mc=2.0, md=1.0, tau=1.5):
    alpha = Phi((tau - mc) / sig)
    beta = Phi((tau - md) / sig)
    return delta_correct(g, h, alpha, beta)

sigs = [.1, .3, .5, 1, 3, 10]
deltas = [delta_gauss(s) for s in sigs]
assert all(x < y for x, y in zip(deltas, deltas[1:]))
print("Gaussian thresholds:", list(zip(sigs, deltas)))
print("Checked: algebraic and numerical consistency")
```

---

## 10. 실제 편집 순서 및 완료 체크리스트

### Phase 0 — 즉시 수정: 제출 PDF와 보충자료의 정확성

- [ ] **메인 p.5–6:** Proposition 2, 식 (6)을 `g/[g(1−α)+(β−α)h]`로 교체.
- [ ] **메인 p.6:** 가치차이 `h/[1−δ(1−α)]` 재유도.
- [ ] **메인 p.6:** `β>α iff feasible` 문장을 `Δh>αg iff feasible`로 교체.
- [ ] **메인 p.6:** 식 (9)을 모든 행동에 대한 비나눗셈형 IC로 교체.
- [ ] **메인 p.6:** 식 (10)의 미분을 새 임계값에서 재유도.
- [ ] **메인 p.6:** Proposition 3의 `z_D>0>z_C` 부호 및 극한 정리 수정.
- [ ] **Supplementary A.1:** 동일한 증명 오류와 실행가능성 조건 수정.
- [ ] **Supplementary A.2:** 예제의 \(\alpha\) 지정 및 산술값 재계산.
- [ ] **Supplementary A.3:** \(\sigma\to0\)의 극한을 `g/(g+h)`로 수정.
- [ ] **메인 p.2 및 p.4:** 식 (3)과 총잉여 결과표를 실제 계산코드와 대조.
- [ ] **메인 Abstract:** 신뢰구간 첫 항의 마이너스 부호 수정.
- [ ] **Supplementary p.5–6:** `Tables 5–??`와 전수 probe 표 수록 범위 수정.

### Phase 1 — 저자 답변과 해석의 정확성

- [ ] Proposition 2–3가 *fixed-trigger benchmark*라는 점을 명시.
- [ ] 유한기간 PPO와 무한기간 반복게임의 구별을 유지.
- [ ] `no enforcement observed`를 `no economically material evidence of enforcement under specified audits`처럼 조건부로 표현.
- [ ] 정보채널 ablation을 순수 정보효과가 아닌 **channel replacement**로 기술.
- [ ] 10개 seed를 실질적 독립 반복 단위로 사용하고 rollout 수준 bootstrap을 무조건적 학습 변동성으로 해석하지 않음.
- [ ] 이론 변경이 실제 PPO 보상/훈련 구현에 사용되는지 코드로 확인.

### Phase 2 — 가능하면 신규 실험

- [ ] 알려진 collusive trigger 정책에 대한 positive control.
- [ ] 현재 일탈이익 \(g>0\)인 가격구간에서 감사.
- [ ] 포화되지 않는 감시신호와 더 작은·적응적 일탈 probe.
- [ ] marginal moment가 맞는 행동독립 신호 placebo.
- [ ] 추가 알고리즘/훈련 시드와 기간 민감도 분석(연구 범위에 따라 선택).

---

## 11. ICLR Rebuttal 작성 시 유의점

**정확하게 수정할 수 있는 오류**와 **새 실험 없이는 해결할 수 없는 한계**를 분리해서 응답한다.

1. **이론 오류를 지적받았다면:** 오류를 인정하고, 수정된 정리와 5–10줄 이내의 새로운 증명 및 실행가능성 조건을 제시한다. 잘못된 원래 임계값을 고수하지 않는다.
2. **후생수치 불일치를 지적받았다면:** 코드로 실제 계산 정의를 확인하고 표와 수식을 맞춘 뒤, 해당 사실만 진술한다. 확인되지 않은 코드를 사용했다고 추측해 답하지 않는다.
3. **positive control 요구를 받았다면:** 완료한 실험의 실측값과 아직 계획 중인 실험을 분명히 구분한다. 계획만으로 검출력을 입증했다고 주장하지 않는다.
4. **정보채널 인과성 비판을 받았다면:** 현 결과의 해석을 channel replacement의 효과로 제한하고, 추가 control이 없다면 그 한계를 명시한다.
5. **이론 수정의 경험적 영향:** 임계 할인인자가 PPO 보상에 사용되지 않았다는 보충자료 기술을 근거로 실험의 직접 영향과 별개임을 설명하되, 코드를 대조해 재확인한다.

---

## 12. 근거 위치 인덱스

| 항목 | 메인 PDF | Supplementary PDF |
|---|---|---|
| 수요·이윤·총잉여 | p.2, 식 (1)–(3) | p.4 Table 3 (surplus 결과) |
| 신호 매핑·Gaussian 리포트 | p.2, 식 (4)–(5) | pp.2–3, B.1–B.2 |
| 관측 불변성 | p.3, Proposition 1 | p.2, A.4 |
| 최종 결과·신뢰구간 | p.4, Table 1 | p.4 Table 3, p.5 Table 4 |
| 가격인하 감사 | pp.3–5, Table 2 | pp.4–6, E.1·F |
| 임계 할인인자 | pp.5–6, Proposition 2, 식 (6)–(9) | p.1, A.1–A.2 |
| Gaussian 비교정태 | p.6, Proposition 3, 식 (10)–(11) | p.2, A.3 |
| 이론과 PPO의 연결 제약 | p.7, §7.1, §8 | pp.2–3, B·C |
| 재현 및 미완료 실험 | p.8, §8.1 | pp.6–7, G·H |

---

## 최종 요약

- **틀린 것을 고쳐도 남는 결론:** 불완전한 감시와 오경보가 고정 트리거 전략의 동태적 집행을 약화시키는 비교정태는 성립한다.
- **바뀌는 결론:** 임계 할인인자의 정확한 식과 `어떤 δ<1이 존재하는가`에 관한 필요충분조건.
- **당장 다시 실행할 필요가 없는 부분:** 수식 정리만 바꾸는 데 PPO 전체 재학습이 필요하지는 않다. 단, 실제 코드에서 이론값을 사용했는지 확인해야 한다.
- **코드 없이 확정할 수 없는 부분:** 결과표의 후생함수 산출 방식, 전체 raw probe 결과 및 완전한 재현가능성.
- **논문 채택 가능성과 연결되는 다음 검증:** 실제 담합 집행이 존재하는 정책을 현재 감사 방법이 감지할 수 있는지를 positive control로 확인하는 일.

> **저자 실무 지침:** 우선 `Proposition 2 → full-IC 식 (9) → Proposition 3 → Supplementary A.1–A.3 → 후생함수 코드 대조 → PDF/표의 정합성` 순서로 수정한다. 그 후 긍정적 대조 실험 및 비교채널 통제로 방법론의 검출력을 보강한다.
