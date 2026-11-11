# 이론 검증 보고서 (THEORY VERIFICATION REPORT - 한국어판)
## *Beyond High Prices: Auditing Information-Mediated Enforcement in Recurrent Pricing Agents* (ICLR 2027) 논문 및 부록에 대한 독립적 수학·게임이론·MARL 감사 보고서

- **원문 영문 보고서:** `/Users/gimjunseong/Downloads/THEORY_VERIFICATION_REPORT.md`
- **본문 수정 LaTeX 소스:** `/Users/gimjunseong/Downloads/main_corrected.tex` (`/Users/gimjunseong/Downloads/main_paper_src/main.tex`)
- **본문 컴파일 PDF:** `/Users/gimjunseong/Downloads/main_corrected.pdf` (`/Users/gimjunseong/Downloads/main_paper_src/main.pdf`)
- **부록 수정 LaTeX 소스:** `/Users/gimjunseong/Downloads/supplement_corrected.tex` (`/Users/gimjunseong/Downloads/supplement_src/main.tex`)
- **부록 컴파일 PDF:** `/Users/gimjunseong/Downloads/supplement_corrected.pdf` (`/Users/gimjunseong/Downloads/supplement_src/main.pdf`)
- **이론 수정 기준 문서:** `/Users/gimjunseong/Downloads/Beyond_High_Prices_P1_Theoretical_Correction_EN.md`
- **실험 아카이브:** `/Users/gimjunseong/Downloads/acrl_suite_v4_research` (`ACRL Suite v4 Research.zip`)

---

## 1. 핵심 요약 및 수정 매트릭스

반복게임의 벨만 방정식(Bellman equations), 가우시안 불완전 모니터링의 비교정학(comparative statics), 그리고 아카이브된 `acrl_suite_v4_research` 실험 산출물을 원리로부터 독립적으로 검증한 결과, 본문 6절(Section 6)과 부록 A.1(Supplement A.1)에 존재하던 하나의 근본적인 대수 오류가 식 (6)–(11), 명제(Proposition) 2–3, 그리고 부록 A.1–A.3 전반으로 전파되었음을 확인하였다.

구체적으로, 협력 상태 벨만 방정식 $V^C = \pi^C + \delta[(1-\alpha)V^C + \alpha V^P]$에서 흡수적(absorbing) 처벌 상태 벨만 방정식 $V^P = \pi^P + \delta V^P$를 뺄 때, 기존 원고는 오경보(false-alarm) 전이 확률 항 $\alpha$를 누락하여 $V^C - V^P = \frac{\pi^C - \pi^P}{1 - \delta}$라고 잘못 적었다. 정확한 항등식은 다음과 같다.
$$V^C - V^P = \frac{\pi^C - \pi^P}{1 - \delta(1-\alpha)} = \frac{h}{1 - \delta(1-\alpha)}.$$
이 단일 오류로 인해 $\alpha > 0$인 모든 경우에서 임계 할인인자 $\delta^*$가 체계적으로 과소평가되었고, $\delta^* < 1$을 위한 실행 가능성(feasibility) 조건 $(\beta - \alpha)h > \alpha g$가 가려졌으며, 식 (10)의 편미분 계수가 왜곡되었다. 나아가 본문 7절과 부록 A.3의 가우시안 비교정학에서는 두 가지 내부 모순이 발생했다: 표준화 좌표의 부호가 반대로 표기되었으며($z_C < 0 < z_D$ 대신 $z_D < 0 < z_C$로 표기), 극한값 주장도 서로 충돌하였다(본문은 $\lim_{\sigma\to\infty}\delta^*(\sigma) = 1$, 부록 A.3은 $\lim_{\sigma\to 0^+}\delta^*(\sigma) = 0$으로 주장).

한편, **명제 1(Proposition 1)**(관측 불변성 음성 대조군, Observation Invariance negative control), **부록 A.4**(유한 구간 꼬리 오차 상계, finite-horizon tail bound), 그리고 `acrl_suite_v4_research`의 모든 PPO 실험 수치 결과는 독립 검증을 통해 유효함이 확인되어 그대로 보존되었다.

### 검증된 수정 사항 요약 매트릭스

| 위치 | 기존 원고 / 부록 | 검증 및 수정된 내용 | 근본 원인 / 영향 |
| :--- | :--- | :--- | :--- |
| **초록 (Abstract, 1쪽)** | PDF에 `[0.0241, 0.0288]`로 출력됨 (`.tex`에는 `[−0.0241, 0.0288]`) | `$[-0.0241,\,0.0288]$` | 텍스트 모드에서 사용된 유니코드 마이너스 `U+2212`를 `pdflatex`가 누락시켜 음수 부호가 사라졌음. |
| **본문 6절, 명제 2 증명 & 부록 A.1** | $V^C - V^P = \frac{\pi^C - \pi^P}{1 - \delta} = \frac{h}{1-\delta}$ | $V^C - V^P = \frac{\pi^C - \pi^P}{1 - \delta(1-\alpha)} = \frac{h}{1 - \delta(1-\alpha)}$ | $V^C$에서 $V^P$를 뺄 때 오경보 확률 $\alpha$가 누락됨. |
| **본문 식 (6), 명제 2 & 부록 A.1** | $\delta^* = \frac{g}{g + (\beta - \alpha)h}$ | $\delta^* = \frac{g}{g(1-\alpha) + (\beta - \alpha)h}$ | $V^C - V^P$ 오류가 전파됨; $\alpha > 0$일 때 $\delta^*$를 $\frac{\alpha g^2}{(g+\Delta h)[g(1-\alpha)+\Delta h]} > 0$만큼 과소평가함. |
| **본문 명제 2 & 부록 A.1 실행 가능성** | $\beta > \alpha \implies \delta^* < 1$로 암묵적으로 가정함 | $\delta^* < 1 \iff (\beta - \alpha)h > \alpha g$ | $\alpha > 0$이면 $\beta > \alpha$는 $\delta \in [0,1)$에서 이탈 억제가 가능하기 위한 필요조건일 뿐 충분조건이 아님. |
| **본문 식 (9) & 부록 A.2** | 나눗셈 형태의 상한 $\sup_{i,a_i:g_i(a_i)>0}\frac{g_i(a_i)}{g_i(a_i)+[\beta_i(a_i)-\alpha_i]h_i}$ | 나눗셈 없는 유인양립조건 $g_i(a_i)[1-\delta(1-\alpha_i)] \le \delta[\beta_i(a_i)-\alpha_i]h_i\;\forall i,a_i\in\mathcal{A}_i$, 및 $\{g_i>0,\beta_i>\alpha_i\}$ 부분집합에 대한 제한된 $\sup$ | 분모에 $(1-\alpha_i)$가 누락되었고, $\beta_i(a_i) \le \alpha_i$ 또는 $g_i(a_i) \le 0$일 때 정의되지 않거나 부등호 방향이 뒤집히는 문제가 있었음. |
| **부록 A.2 수치 예시 & 교차 참조** | `Main-text equation (10)` 참조; $\alpha$ 명시 없이 `0.588235`($10/17$)와 `0.990099`($100/101$) 보고 | `Main-text equation (9)` 참조로 수정; $\alpha = 0.05, h = 1$ 명시: Deviation A($g=0.30,\beta=0.55$) $\delta^*_A = \frac{60}{157} \approx 0.382166$; Deviation B($g=0.90,\beta=0.06$) $\delta^*_B = \frac{180}{173} \approx 1.040462$ | 기존 수치는 $1/(1+\Delta/g)$를 계산한 것으로, 구(오류) 공식($0.375, 0.989011$)과 신(정확한) 공식 어느 쪽과도 일치하지 않았음. |
| **본문 식 (10)** | $D_0 = g+(\beta-\alpha)h$ 기준 $\frac{\partial\delta^*}{\partial\alpha} = \frac{gh}{D_0^2}$, $\frac{\partial\delta^*}{\partial\beta} = -\frac{gh}{D_0^2}$, $\frac{\partial\delta^*}{\partial h} = -\frac{g(\beta-\alpha)}{D_0^2}$ | $D = g(1-\alpha)+(\beta-\alpha)h$ 기준 $\frac{\partial\delta^*}{\partial\alpha} = \frac{g(g+h)}{D^2} > 0$, $\frac{\partial\delta^*}{\partial\beta} = -\frac{gh}{D^2} < 0$, $\frac{\partial\delta^*}{\partial h} = -\frac{g(\beta-\alpha)}{D^2} < 0$, $\frac{\partial\delta^*}{\partial g} = \frac{(\beta-\alpha)h}{D^2} > 0$ | $\alpha$가 탐지 격차 $\Delta$와 협력 가치 격차 $V^C-V^P$를 동시에 잠식하므로 $\partial\delta^*/\partial\alpha$의 분자는 $gh$가 아니라 $g(g+h) > gh$임. |
| **본문 식 (11), 명제 3 & 부록 A.3** | $z_D < 0 < z_C$ 및 $\frac{\partial\Delta}{\partial\sigma} = \frac{1}{\sigma}[z_C\phi(z_C) - z_D\phi(z_D)] < 0$로 기술 | $\mu_D < \tau < \mu_C$일 때 $z_C = \frac{\tau-\mu_C}{\sigma} < 0 < z_D = \frac{\tau-\mu_D}{\sigma}$, $\frac{\partial\Delta}{\partial\sigma} = -\frac{1}{\sigma}[z_D\phi(z_D)-z_C\phi(z_C)] < 0$, $\frac{d\delta^*}{d\sigma} = \frac{g[(g+h)\alpha'(\sigma)-h\beta'(\sigma)]}{D(\sigma)^2} > 0$ | $\mu_D < \tau < \mu_C$ 가정 하에서는 $\tau - \mu_C < 0 < \tau - \mu_D$이므로 반드시 $z_C < 0 < z_D$임. |
| **본문 명제 3 & 부록 A.3 극한값** | 본문 명제 3: $\sigma\to 0^+$에서 $\frac{g}{g+h}$, $\sigma\to\infty$에서 $1$; 부록 A.3: $\sigma\to 0^+$에서 $0$, $\sigma\to\infty$에서 $1$ | 본문 명제 3 및 부록 A.3 모두: $\lim_{\sigma\to 0^+}\delta^*(\sigma) = \frac{g}{g+h} \in (0,1)$ 및 $\lim_{\sigma\to\infty}\delta^*(\sigma) = 2$, $\delta^*(\bar{\sigma})=1$을 만족하는 유일한 차단 잡음 수준 $\bar{\sigma}\in(0,\infty)$ 존재 | $\sigma\to\infty$일 때 $\alpha,\beta\to 1/2 \implies D(\sigma)\to g/2 \implies \delta^*(\sigma)\to 2$. |
| **부록 E.1 & F절 (표 5–8)** | 본문에 `Tables 5–??`로 깨져 출력됨; 표 5가 8열인데 열 사양 7개(`@{}cccSSSS@{}`)만 지정되어 컴파일 오류 및 160행 중 9행만 수록 | `\probetable`을 8열(`@{}cccSSSSr@{}`)로 수정하고 `tab:probe_B01`, `tab:probe_B03`, `tab:probe_A01`, `tab:probe_A03`에 160개 프로브 전체 행 수록; `Tables 5–8`로 정상 참조 | `supplement_src/main.tex`의 주석(placeholder)을 `acrl_suite_v4_research` 실측 데이터로 완전히 채움. |
| **부록 표 9 (`tab:hashes`)** | 축약 해시(`a2cd4f26...c202d1b95` 등) 표기 | `suite_manifest.json`의 64자리 전체 SHA256 해시 수록 | 완전한 암호학적 재현성 검증 정보 제공. |

---

## 2. 모형 원형, 가정 및 경계 사례(Boundary Cases)

완전한 수학적 엄밀성을 확보하기 위해, 수정된 본문 6절과 부록 A는 모든 기본 가정과 경계 사례를 명시적으로 규정한다.

1. **할인 반복게임 및 오토마톤(Automaton) 구조:**
   - 시간은 이산적이며 $t = 0, 1, 2, \dots$의 무한 지평(infinite horizon)을 가지고, 공통 할인인자는 $\delta \in [0, 1)$이다.
   - 각 기(stage game)의 보수는 유계(bounded)이다.
   - 불완전 공적 모니터링 하에서 매기 $t$ 말에 공적 신호가 생성되며, 그 분포는 오직 당기 $t$의 행동에만 의존한다.
   - 공적 2-상태 오토마톤은 협력 상태 $C$와 흡수적 처벌 상태 $P$로 구성된다.
   - 상태 $C$에서 기업들은 지정된 협력 행동 프로필 $a^C = (a_1^C, a_2^C)$를 선택해 매기 보수 $\pi^C$(또는 비대칭/전칭 정식화에서는 $\pi_i^C$)를 얻는다. 나쁜(bad) 공적 신호가 관측되면 오토마톤은 영구적으로 $C$에서 $P$로 전이하며, 그렇지 않으면 $C$에 머문다.
   - 상태 $P$에서 기업들은 일회성 내시(Nash) 행동 프로필 $a^P$를 영구히 플레이하며 매기 보수 $\pi^P$(또는 $\pi_i^P$)를 얻는다. $a^P$는 단계 게임의 내시 균형이고 $P$는 흡수 상태(이후 전이가 행동과 무관)이므로, 상태 $P$에서의 계속 플레이는 부분게임 신빙성(subgame-credible)을 갖는다.

2. **일회 이탈 원리(One-Shot Deviation Principle)와 평가 시점:**
   - 가치함수 $V^C$, $V^P$, $V^D$는 당기 행동이 선택되기 직전(기초 시점)에 평가하며, 전체 할인합에 $(1-\delta)$를 곱하지 않은 비정규화(unnormalized) 총현재가치이다.
   - $\delta \in [0,1)$ 및 유계 보수 가정 하에서 일회 이탈 원리가 성립한다: 공적 오토마톤 전략이 공적 완전균형(public perfect equilibrium)이 될 필요충분조건은 어느 플레이어도 상태 $C$(또는 $P$)에서 1기간 일방 이탈 후 다시 지정 전략으로 복귀하더라도 이득을 볼 수 없다는 것이다.

3. **매개변수 영역 및 내부 가정 (명제 2 & 3):**
   - 지정 이탈의 즉각 이득: $g = \pi^D - \pi^C > 0$.
   - 협력–처벌 기당 보수 격차: $h = \pi^C - \pi^P > 0$.
   - 신호 확률: $0 \le \alpha < \beta \le 1$. 여기서 $\alpha = \Pr(\text{bad signal}\mid \text{준수})$, $\beta = \Pr(\text{bad signal}\mid \text{지정 이탈})$, 탐지 격차는 $\Delta = \beta - \alpha > 0$이다.
   - 명제 3(가우시안 벤치마크): 준수 시 공적 통계량은 $Y_t \sim \mathcal{N}(\mu_C, \sigma^2)$, 지정 이탈 시 $Y_t \sim \mathcal{N}(\mu_D, \sigma^2)$이며, 고정 임계치 $\tau$에 대해 $Y_t < \tau$이면 나쁜 신호로 판정한다. 이때 $\mu_D < \tau < \mu_C$이며 $\sigma > 0$이고 $(g, h, \mu_C, \mu_D, \tau)$는 고정한다.

4. **모든 경계 사례 (Exhaustive Boundary Cases):**
   - **경계 사례 1 ($\alpha = 0$, 오경보 없음):** $V^C - V^P = \frac{h}{1-\delta}$이고, 모든 $\beta > 0, g > 0, h > 0$에 대해 $\delta^* = \frac{g}{g + \beta h} < 1$이다. 추가로 $\beta = 1$(완전 모니터링)이면 $\delta^* = \frac{g}{g+h} \in (0,1)$가 된다.
   - **경계 사례 2 ($\alpha > 0$ 이면서 $(\beta-\alpha)h \le \alpha g$, 실행 불가능 영역):**
     - 경계점 $(\beta-\alpha)h = \alpha g \implies \delta^* = 1$: 허용 영역 $\delta \in [0,1)$에는 이탈을 억제할 수 있는 할인인자가 존재하지 않는다.
     - 엄격한 실행 불가능 영역 $(\beta-\alpha)h < \alpha g \implies \delta^* > 1$: 모든 $\delta \in [0,1)$에서 $V^D > V^C$이므로 이탈이 항상 엄격하게 이득이다.
   - **경계 사례 3 (전체 행동 공간 $\mathcal{A}_i$ 상에서 $g_i(a_i) \le 0$ 또는 $\beta_i(a_i) \le \alpha_i$인 경우):**
     - 나눗셈 없는 유인양립조건 $g_i(a_i)[1 - \delta(1-\alpha_i)] \le \delta[\beta_i(a_i) - \alpha_i]h_i$는 모든 $a_i \in \mathcal{A}_i$에서 잘 정의되며 정확하다.
     - 하위 사례 3a ($g_i(a_i) > 0$ 이고 $\beta_i(a_i) \le \alpha_i$): 모든 $\delta \in [0,1)$에서 좌변 $> 0 \ge$ 우변이므로 어떤 $\delta < 1$로도 억제할 수 없다.
     - 하위 사례 3b ($g_i(a_i) \le 0$ 이고 $\beta_i(a_i) \ge \alpha_i$): 좌변 $\le 0 \le$ 우변이므로 모든 $\delta \in [0,1)$에서 자명하게 성립한다.
     - 하위 사례 3c ($g_i(a_i) < 0$ 이고 $\beta_i(a_i) < \alpha_i$): 당기 이윤을 희생($g_i < 0$)하는 대신 오경보 발생 확률을 낮추는($\beta_i < \alpha_i$) 행동. 나눗셈 없는 부등식은 $\delta[\alpha_i - \beta_i]h_i \le |g_i(a_i)|[1 - \delta(1-\alpha_i)]$를 요구하며(오경보 감소 폭이 크면 오히려 $\delta$에 상한을 부과함), 음수 분모로 무작정 나누면 부등호 방향이 반대로 뒤집힌다.
   - **경계 사례 4 (가우시안 임계치 $\tau \notin [\mu_D, \mu_C]$):**
     - 만약 $\tau < \mu_D < \mu_C$이면 $z_C < z_D < 0$이므로 $\alpha'(\sigma) > 0, \beta'(\sigma) > 0$이고, $\sigma \to 0^+$일 때 $\alpha(\sigma)\to 0, \beta(\sigma)\to 0$이 되어 $\Delta(\sigma) \to 0$ 및 $\delta^*(\sigma) \to 1$이 된다.
     - 만약 $\mu_D < \mu_C < \tau$이면 $0 < z_C < z_D$이므로 $\alpha'(\sigma) < 0, \beta'(\sigma) < 0$이고, $\sigma \to 0^+$일 때 $\alpha(\sigma)\to 1, \beta(\sigma)\to 1$이 되어 $\Delta(\sigma) \to 0, D(\sigma) \to 0^+$로 $\delta^*(\sigma) \to +\infty$로 발산한다.
     - 따라서 $(0,\infty)$ 전역에서 $\Delta(\sigma)$와 $\delta^*(\sigma)$의 단조성을 얻으려면 $\mu_D < \tau < \mu_C$(또는 한쪽 경계등호) 가정이 필수적이다.
   - **경계 사례 5 (추가 독립 가우시안 잡음 $\sigma_{\mathrm{tot}} = \sqrt{\sigma^2 + \sigma_a^2}$ 의 $\sigma_a = 0$ 경계 미분):**
     - 기저 잡음 $\sigma > 0$일 때 $\frac{\partial \sigma_{\mathrm{tot}}}{\partial \sigma_a}\big|_{\sigma_a = 0} = 0$이므로 $\frac{\partial \delta^*}{\partial \sigma_a}\big|_{\sigma_a = 0} = 0$이다. 그럼에도 모든 $\sigma_a > 0$에 대해 $\delta^*(\sqrt{\sigma^2 + \sigma_a^2}) > \delta^*(\sigma)$는 엄격히 성립한다.

---

## 3. 명제 2, 식 (6)–(9), 및 부록 A.1–A.2 단계별 재증명

### 3.1 벨만 방정식과 정확한 협력–처벌 가치 격차 $V^C - V^P$
$\delta \in [0,1)$인 정상적 할인 반복게임에서 협력 상태 $C$와 흡수적 처벌 상태 $P$의 벨만 방정식은 다음과 같다.
$$\begin{aligned}
V^C &= \pi^C + \delta\bigl[(1-\alpha)V^C + \alpha V^P\bigr], \qquad \text{(본문 식 7)} \\
V^P &= \pi^P + \delta V^P.
\end{aligned}$$
첫 번째 식에서 두 번째 식을 오경보 항 $\alpha$를 누락하지 않고 그대로 빼면 다음과 같다.
$$\begin{aligned}
V^C - V^P &= (\pi^C - \pi^P) + \delta\bigl[(1-\alpha)V^C + \alpha V^P - V^P\bigr] \\
&= (\pi^C - \pi^P) + \delta\bigl[(1-\alpha)V^C - (1-\alpha)V^P\bigr] \\
&= h + \delta(1-\alpha)(V^C - V^P).
\end{aligned}$$
이를 이항해 정리하면
$$[1 - \delta(1-\alpha)](V^C - V^P) = h.$$
$\delta \in [0,1)$이고 $\alpha \in [0,1]$이므로 $1-\alpha \in [0,1]$, $\delta(1-\alpha) \le \delta < 1$이며 $1 - \delta(1-\alpha) \ge 1 - \delta > 0$이다. 양변을 $1 - \delta(1-\alpha) > 0$으로 나누면 유일해를 얻는다.
$$\boxed{V^C - V^P = \frac{\pi^C - \pi^P}{1 - \delta(1-\alpha)} = \frac{h}{1 - \delta(1-\alpha)}.}$$

### 3.2 일회 이탈 가치와 임계 할인인자 $\delta^*$ (본문 식 6 및 8)
일회 이탈 후 오토마톤 전략으로 복귀할 때의 기대할인가치는 다음과 같다.
$$V^D = \pi^D + \delta\bigl[(1-\beta)V^C + \beta V^P\bigr]. \qquad \text{(본문 식 8)}$$
식 (8)에서 식 (7)을 빼면:
$$\begin{aligned}
V^D - V^C &= (\pi^D - \pi^C) + \delta\bigl[(1-\beta - (1-\alpha))V^C + (\beta - \alpha)V^P\bigr] \\
&= g - \delta(\beta - \alpha)(V^C - V^P) \\
&= g - \frac{\delta(\beta - \alpha)h}{1 - \delta(1-\alpha)}.
\end{aligned}$$
따라서 상태 $C$에서 이탈이 비수익적($V^D \le V^C$)일 필요충분조건은
$$g - \frac{\delta(\beta - \alpha)h}{1 - \delta(1-\alpha)} \le 0.$$
양변에 양수 $1 - \delta(1-\alpha) > 0$을 곱하면 부등호 방향이 보존된다:
$$g[1 - \delta(1-\alpha)] \le \delta(\beta - \alpha)h \iff g \le \delta\bigl[g(1-\alpha) + (\beta - \alpha)h\bigr].$$
$g > 0$, $h > 0$, $0 \le \alpha < \beta \le 1$ 하에서 분모
$$D \equiv g(1-\alpha) + (\beta - \alpha)h > 0$$
은 엄격히 양수이므로 $D$로 나누면 정확한 임계 할인인자(본문 식 6)를 얻는다.
$$\boxed{\delta \ge \delta^* \equiv \frac{\pi^D - \pi^C}{(\pi^D - \pi^C)(1-\alpha) + (\beta - \alpha)(\pi^C - \pi^P)} = \frac{g}{g(1-\alpha) + (\beta - \alpha)h}.}$$

### 3.3 엄격한 실행 가능성 조건 ($\delta^* < 1$) 및 기존 오류의 방향
$1 - \delta^*$를 계산하면:
$$1 - \delta^* = 1 - \frac{g}{g(1-\alpha) + (\beta - \alpha)h} = \frac{g(1-\alpha) + (\beta - \alpha)h - g}{g(1-\alpha) + (\beta - \alpha)h} = \frac{(\beta - \alpha)h - \alpha g}{D}.$$
$D > 0$이므로
$$\boxed{\delta^* < 1 \iff (\beta - \alpha)h > \alpha g.}$$
수정된 $\delta^*_{\mathrm{corrected}}$와 기존 원고의 오류 식 $\delta^*_{\mathrm{printed}} = \frac{g}{g + (\beta - \alpha)h}$의 차이는 다음과 같다.
$$\delta^*_{\mathrm{corrected}} - \delta^*_{\mathrm{printed}} = \frac{g}{g(1-\alpha) + \Delta h} - \frac{g}{g + \Delta h} = \frac{\alpha g^2}{(g + \Delta h)[g(1-\alpha) + \Delta h]} \ge 0,$$
이는 $\alpha > 0, g > 0$일 때 항상 엄격히 양수다.

### 3.4 기존 공식의 오판정을 보여주는 반례
$g = 0.2 = \frac{1}{5}$, $h = 0.5 = \frac{1}{2}$, $\alpha = 0.4 = \frac{2}{5}$, $\beta = 0.5 = \frac{1}{2}$($\Delta = \beta - \alpha = 0.1 = \frac{1}{10}$)로 두자:
- **기존 오류 공식:** $\delta^*_{\mathrm{printed}} = \frac{0.2}{0.2 + 0.1 \times 0.5} = \frac{0.2}{0.25} = \frac{4}{5} = 0.8 < 1$ ($\delta \in [0.8, 1)$이면 이탈이 억제된다고 잘못 예측함).
- **정확한 공식:** $\delta^*_{\mathrm{corrected}} = \frac{0.2}{0.2(0.6) + 0.1(0.5)} = \frac{0.2}{0.12 + 0.05} = \frac{0.2}{0.17} = \frac{20}{17} \approx 1.176471 > 1$.
- **실행 가능성 검사:** $(\beta - \alpha)h = 0.05 < \alpha g = 0.08$이므로 $\delta \in [0,1)$ 전체에서 이탈이 엄격히 유리하다.
- **$\delta = 0.9 \in (0.8, 1)$에서의 직접 벨만 계산:**
  $$V^C - V^P = \frac{0.5}{1 - 0.9(0.6)} = \frac{0.5}{0.46} = \frac{25}{23}, \qquad V^D - V^C = 0.2 - 0.9(0.1)\frac{25}{23} = \frac{1}{5} - \frac{9}{92} = \frac{47}{460} \approx +0.102174 > 0.$$

### 3.5 완전한 일방 유인양립조건 (본문 식 9) 및 부록 A.2 수치 예시 검증
모든 기업 $i$와 모든 일방 행동 $a_i \in \mathcal{A}_i$에 대하여, 상태 $C$에서의 일회 이탈 유인양립조건은 다음과 같다.
$$\boxed{g_i(a_i)\bigl[1 - \delta(1-\alpha_i)\bigr] \le \delta\bigl[\beta_i(a_i) - \alpha_i\bigr]h_i \quad \forall i, \;\forall a_i \in \mathcal{A}_i.}$$
이 중 $g_i(a_i) > 0$이고 $\beta_i(a_i) > \alpha_i$인 제한된 부분집합 위에서는 다음의 필요 하한을 얻는다.
$$\delta \ge \sup_{i,\,a_i : g_i(a_i)>0,\,\beta_i(a_i)>\alpha_i} \frac{g_i(a_i)}{g_i(a_i)(1-\alpha_i) + [\beta_i(a_i)-\alpha_i]h_i}.$$

**부록 A.2 수치 예시 검증:**
$h = 1$, 준수 시 오경보 확률 $\alpha = 0.05$일 때:
- **이탈 A (Deviation A):** $g_A = 0.30$, $\beta_A = 0.55$, $\beta_A - \alpha = 0.50$:
  $$\delta^*_A = \frac{0.30}{0.30(0.95) + 0.50(1)} = \frac{0.30}{0.785} = \frac{60}{157} \approx 0.382166 < 1 \quad \bigl((\beta_A-\alpha)h = 0.50 > \alpha g_A = 0.015\bigr).$$
- **이탈 B (Deviation B):** $g_B = 0.90$, $\beta_B = 0.06$, $\beta_B - \alpha = 0.01$:
  $$\delta^*_B = \frac{0.90}{0.90(0.95) + 0.01(1)} = \frac{0.90}{0.865} = \frac{180}{173} \approx 1.040462 > 1 \quad \bigl((\beta_B-\alpha)h = 0.01 < \alpha g_B = 0.045\bigr).$$
할인인자 $\delta = 0.90$에서 이탈 A는 억제되지만($\delta \ge \delta^*_A$), 이탈 B는 억제되지 않으며 $\delta < 1$인 어떤 할인인자로도 억제할 수 없다.

---

## 4. 식 (10), 명제 3, 식 (11), 및 부록 A.3 단계별 재증명

### 4.1 $\delta^*$의 편미분 (본문 식 10)
내부 영역 $g > 0, h > 0, 0 \le \alpha < \beta \le 1$에서 $D = g(1-\alpha) + (\beta - \alpha)h > 0$이다. $\delta^*(g, h, \alpha, \beta) = g / D$를 각 모수로 편미분하면:
1. **$\alpha$에 대한 편미분:** $\frac{\partial D}{\partial \alpha} = -(g + h)$이므로,
   $$\boxed{\frac{\partial \delta^*}{\partial \alpha} = -\frac{g}{D^2}\frac{\partial D}{\partial \alpha} = \frac{g(g+h)}{\bigl[g(1-\alpha) + (\beta-\alpha)h\bigr]^2} > 0.}$$
2. **$\beta$에 대한 편미분:** $\frac{\partial D}{\partial \beta} = h$이므로,
   $$\boxed{\frac{\partial \delta^*}{\partial \beta} = -\frac{gh}{\bigl[g(1-\alpha) + (\beta-\alpha)h\bigr]^2} < 0.}$$
3. **$h$에 대한 편미분:** $\frac{\partial D}{\partial h} = \beta - \alpha$이므로,
   $$\boxed{\frac{\partial \delta^*}{\partial h} = -\frac{g(\beta-\alpha)}{\bigl[g(1-\alpha) + (\beta-\alpha)h\bigr]^2} < 0.}$$
4. **$g$에 대한 편미분:** $\frac{\partial D}{\partial g} = 1 - \alpha$이므로,
   $$\boxed{\frac{\partial \delta^*}{\partial g} = \frac{D - g(1-\alpha)}{D^2} = \frac{(\beta-\alpha)h}{\bigl[g(1-\alpha) + (\beta-\alpha)h\bigr]^2} > 0.}$$

### 4.2 가우시안 꼬리 확률과 표준화 좌표 (본문 식 11 및 명제 3)
$\mu_D < \tau < \mu_C$, $\sigma > 0$일 때 표준화 좌표를 다음과 같이 정의한다.
$$z_C(\sigma) = \frac{\tau - \mu_C}{\sigma} < 0, \qquad z_D(\sigma) = \frac{\tau - \mu_D}{\sigma} > 0.$$
$\alpha(\sigma) = \Phi(z_C(\sigma))$와 $\beta(\sigma) = \Phi(z_D(\sigma))$를 $\sigma$로 미분하면:
$$\alpha'(\sigma) = \phi(z_C)\frac{dz_C}{d\sigma} = -\frac{z_C\,\phi(z_C)}{\sigma} > 0 \quad (z_C < 0,\; \phi(z_C) > 0,\; \sigma > 0),$$
$$\beta'(\sigma) = \phi(z_D)\frac{dz_D}{d\sigma} = -\frac{z_D\,\phi(z_D)}{\sigma} < 0 \quad (z_D > 0,\; \phi(z_D) > 0,\; \sigma > 0).$$
따라서 탐지 격차 $\Delta(\sigma) = \beta(\sigma) - \alpha(\sigma)$의 도함수(본문 식 11)는 다음과 같다.
$$\boxed{\frac{\partial \Delta}{\partial \sigma} = \beta'(\sigma) - \alpha'(\sigma) = -\frac{1}{\sigma}\bigl[z_D\,\phi(z_D) - z_C\,\phi(z_C)\bigr] < 0,}$$
이는 $z_D\phi(z_D) > 0$이고 $-z_C\phi(z_C) > 0$이기 때문이다.

### 4.3 전미분 $d\delta^*/d\sigma$
연쇄법칙(chain rule)에 의해:
$$\frac{d\delta^*}{d\sigma} = \frac{\partial \delta^*}{\partial \alpha}\alpha'(\sigma) + \frac{\partial \delta^*}{\partial \beta}\beta'(\sigma) = \frac{g(g+h)}{D(\sigma)^2}\alpha'(\sigma) - \frac{gh}{D(\sigma)^2}\beta'(\sigma),$$
따라서:
$$\boxed{\frac{d\delta^*}{d\sigma} = \frac{g\bigl[(g+h)\alpha'(\sigma) - h\beta'(\sigma)\bigr]}{\bigl[g(1-\alpha(\sigma)) + (\beta(\sigma)-\alpha(\sigma))h\bigr]^2} > 0,}$$
모든 $\sigma > 0$에서 $(g+h)\alpha'(\sigma) > 0$이고 $-h\beta'(\sigma) > 0$이므로 항상 엄격히 양수이다.

### 4.4 정확한 점근 극한값과 유일한 실행 가능 차단점 $\bar{\sigma}$
1. **무잡음 극한 ($\sigma \to 0^+$):**
   $\tau - \mu_C < 0 < \tau - \mu_D$이므로 $\sigma \to 0^+$일 때 $z_C(\sigma) \to -\infty$, $z_D(\sigma) \to +\infty$이다. 따라서 $\alpha(\sigma) = \Phi(z_C) \to 0$, $\beta(\sigma) = \Phi(z_D) \to 1$이고, $D(\sigma) \to g(1-0) + (1-0)h = g + h$이므로
   $$\boxed{\lim_{\sigma \to 0^+} \delta^*(\sigma) = \frac{g}{g + h} \in (0, 1).}$$
2. **무한 잡음 극한 ($\sigma \to \infty$):**
   $\sigma \to \infty$일 때 $z_C(\sigma) \to 0^-$, $z_D(\sigma) \to 0^+$이다. 따라서 $\alpha(\sigma) \to \Phi(0) = \frac{1}{2}$, $\beta(\sigma) \to \Phi(0) = \frac{1}{2}$이고, $\Delta(\sigma) \to 0$, $D(\sigma) \to g\left(1 - \frac{1}{2}\right) + 0 \cdot h = \frac{g}{2}$이므로
   $$\boxed{\lim_{\sigma \to \infty} \delta^*(\sigma) = \frac{g}{g/2} = 2.}$$
3. **유일한 실행 가능 차단 잡음 수준 $\bar{\sigma} \in (0, \infty)$:**
   $\delta^*(\sigma)$는 $(0, \infty)$에서 연속이며 엄격히 증가하고, $\lim_{\sigma\to 0^+} \delta^*(\sigma) = \frac{g}{g+h} < 1$, $\lim_{\sigma\to\infty} \delta^*(\sigma) = 2 > 1$이다. 따라서 중간값 정리와 엄격한 단조성에 의해 다음을 만족하는 $\bar{\sigma} \in (0, \infty)$가 유일하게 존재한다.
   $$\delta^*(\bar{\sigma}) = 1 \iff \bigl[\beta(\bar{\sigma}) - \alpha(\bar{\sigma})\bigr]h = \alpha(\bar{\sigma})g.$$
   즉, $\delta \in [0,1)$에서 지정 이탈이 억제 가능할 필요충분조건은 $\sigma < \bar{\sigma}$이다.

---

## 5. 기호(정확 유리수) 및 수치 교차검증 요약

모든 대수적 항등식, 도함수, 극한값, 수치 예시는 Python으로 독립 교차검증되었다:
1. **정확 유리수 다항식 항등식 검증 (`fractions.Fraction`):**
   - $(g, h, \alpha, \beta, \delta)$의 625개 유리수 격자점 전체에서 선형 벨만 연립방정식의 해 $(V^C, V^P, V^D)$가 $V^C - V^P = \frac{h}{1 - \delta(1-\alpha)}$, $V^D - V^C = g - \frac{\delta(\beta-\alpha)h}{1 - \delta(1-\alpha)}$, 그리고 $\delta^*_{\mathrm{corrected}} - \delta^*_{\mathrm{printed}} = \frac{\alpha g^2}{(g+\Delta h)[g(1-\alpha)+\Delta h]}$를 잔차 $0/1$로 만족함을 확인하였다.
   - 반례($g=1/5, h=1/2, \alpha=2/5, \beta=1/2$) 및 부록 A.2 표($\alpha=1/20, h=1$: $\delta^*_A = 60/157$, $\delta^*_B = 180/173$)를 정확 유리수 연산으로 확인하였다.
2. **해석적 미분 vs. 중앙 유한차분 검증 ($\varepsilon = 10^{-6}$):**
   - 식 (10)의 4개 편미분($\partial\delta^*/\partial\alpha$, $\partial\delta^*/\partial\beta$, $\partial\delta^*/\partial h$, $\partial\delta^*/\partial g$) 및 가우시안 도함수($\alpha'(\sigma)$, $\beta'(\sigma)$, $\Delta'(\sigma)$, $d\delta^*/d\sigma$, $\partial\delta^*/\partial\sigma_a$)가 오차 $< 10^{-11}$ 이내로 일치함을 확인하였다.
   - 대표 매개변수 $g = 0.3, h = 0.7, \mu_C = 2.0, \mu_D = 1.2, \tau = 1.6$에 대해:
     - $\lim_{\sigma\to 0^+} \delta^*(\sigma) = 0.3 / (0.3 + 0.7) = 0.300000$ ($\sigma = 0.01$에서 $\delta^* = 0.300000$).
     - 유일한 차단점 $\bar{\sigma} = 0.5624189165$ ($\alpha(\bar{\sigma}) = 0.23850016$, $\beta(\bar{\sigma}) = 0.76149984$, $\delta^*(\bar{\sigma}) = 1.00000000$).
     - $\sigma = 10^4$에서 $\delta^*(10^4) = 1.99946809 \to 2$.

---

## 6. 실험 아카이브(`acrl_suite_v4_research`) 대조 검증

본문과 부록의 모든 수치 표와 통계 주장을 `/Users/gimjunseong/Downloads/acrl_suite_v4_research` 내 실제 파일과 1:1 대조하였다:

1. **격자 vs. 연속 기준 가격 (`policy.curve.csv`, `job.json`):**
   - 연속 대칭 일회성 로짓 내시 가격: $p^{\mathrm{N}} = 1.4729266564$ (논문 보고값 $1.472927$).
   - 연속 대칭 공동이윤 극대화 가격: $p^{\mathrm{J}} = 1.9249809205$ (논문 보고값 $1.924981$).
   - 시뮬레이터 $[1.0, 2.5]$ 구간 $1{,}501$개 가격 격자(간격 $0.001$): $p^{\mathrm{N}}_{\mathrm{grid}} = 1.473$, $p^{\mathrm{J}}_{\mathrm{grid}} = 1.925$ (격자 간격 $0.452$). 20개 시드 전체에서 `collusive_index` $= (\bar{p} - 1.473)/0.452$가 오차 $0.00\times 10^0$으로 일치함.
2. **본문 표 1 (`tab:final`) 및 부록 표 3 (`tab:seed_results`):**
   - 20개 시드 행(`ppo_baseline` 10개, `ppo_ablated` 10개)과 쌍대 차이(paired diff.) 및 `np.random.default_rng(20260920)` 기반 2,000회 전체 시드 부트스트랩 95% 신뢰구간이 정확히 일치함을 검증:
     - 평균 가격(Mean price): $1.479804$ (B) vs. $1.481492$ (A), 차이 $0.001688$ $[-0.0109,\,0.0130]$.
     - 가격 상승도(Price elevation): $0.015052$ (B) vs. $0.018787$ (A), 차이 $0.003735$ $[-0.0241,\,0.0288]$.
     - 총잉여(Total surplus): $1.159588$ (B) vs. $1.159660$ (A), 차이 $0.000072$ $[-0.0013,\,0.0017]$.
     - 특징 유효 랭크(Feature rank, 기업 0): $1.274335$ (B) vs. $1.338647$ (A), 차이 $0.064312$ $[0.0113,\,0.1337]$.
     - 특징 유효 랭크(Feature rank, 기업 1): $1.269538$ (B) vs. $1.353578$ (A), 차이 $0.084040$ $[0.0282,\,0.1495]$.
3. **본문 표 2 (`tab:audit`), 부록 표 4 (`tab:bootstrap_ci`) 및 부록 표 5–8 (`tab:probe_B01`–`tab:probe_A03`):**
   - 20개 `audit_probes.json` 파일의 총 160개 프로브 기록 전체를 대조 검증:
     - 정보 채널(B), 인하폭 0.1: 즉각 이득 $-0.005186$, 전체 이득 $-0.005192$, 계속 이득 $-0.000005$ $[-0.000010, -0.000001]$, 양(+)의 프로브 40개 중 3개 (Seed 01 firm 0 $t=64$: $0.000573$; Seed 05 firm 0 $t=64$: $0.003846$; Seed 05 firm 0 $t=256$: $0.002990$).
     - 정보 채널(B), 인하폭 0.3: 즉각 이득 $-0.051317$, 전체 이득 $-0.051322$, 계속 이득 $-0.000005$ $[-0.000010, -0.000001]$, 양(+)의 프로브 40개 중 0개.
     - 행동 무관(A), 인하폭 0.1: 즉각 이득 $-0.004800$, 전체 이득 $-0.004800$, 계속 이득 $0.000000$, 양(+)의 프로브 40개 중 1개 (Seed 08 firm 0 $t=256$: $0.000122$).
     - 행동 무관(A), 인하폭 0.3: 즉각 이득 $-0.050273$, 전체 이득 $-0.050273$, 계속 이득 $0.000000$, 양(+)의 프로브 40개 중 0개.
     - 정보 채널 평균 부호화 경쟁자 반응 면적: $-3.699770\times 10^{-6}$ (95% CI $[-1.1066\times 10^{-5},\,3.2143\times 10^{-6}]$); 행동 무관 채널 80개 프로브 전체에서는 기계 정밀도 수준으로 정확히 $0.0$ (명제 1 실증 확인).
4. **재현성 해시 및 상호작용 회계 (부록 표 9–10):**
   - 사후표본(Posterior draws) SHA256: `a2cd4f268b3edf0d9004f0144d2fc846a1088497d171fe33e2adcd4c202d1b95`.
   - 네이티브 확장(Native extension) SHA256: `8c1fe82a4830d09ec6710177a4056ca0a67ecf013cf774517e15480fef882780`.
   - PPO 학습 소스(PPO training source) SHA256: `12ffcf180b6fc8997d0c0dbff6ce085b2467e4dd1300348ac0151b92662d3f15`.
   - MCMC 진단: 최대 split $\hat{R} = 1.0089447329892174 \le 1.01$, 최소 ESS $= 606.8603540325352 \ge 400$.
   - 총 기록 상호작용: 작업당 $2{,}908{,}736 \times 20 = 58{,}174{,}720$회; 총 실행 시간: $21.978\text{ h}$(baseline) $+ 22.079\text{ h}$(ablated) $= 44.057\text{ h}$.

---

## 7. 3대 관점 적대적 검토 (Adversarial Review)

### 7.1 게임이론 관점
1. **오경보의 가치 잠식 vs. 탐지 격차:** 불완전 공적 모니터링(Green & Porter 1984; Fudenberg, Levine & Maskin 1994)에서 양(+)의 오경보 확률 $\alpha > 0$은 협력 국면의 확률적 종료율처럼 작동하여 협력 잉여에 적용되는 유효 할인인자를 $\delta$에서 $\delta(1-\alpha)$로 낮춘다. 따라서 $\beta > \alpha$만으로는 $\delta \in [0,1)$에서 담합이 집행 가능하지 않으며, 반드시 $(\beta-\alpha)h > \alpha g$가 성립해야 한다. 수정된 본문 6절과 부록 A.1은 이를 명확히 진술하고 증명하였다.
2. **모든 일방 이탈에 대한 전칭 양화(Quantifier):** 상태 $C$에서의 균형은 정태적 최적반응이나 두 가지 고정 인하폭만 억제하는 것이 아니라, 연속 행동공간 $\mathcal{A}_i$의 *모든* 일방 이탈 $a_i$를 억제해야 한다. 매끄러운 모니터링 하에서는 탐지 격차 $\beta_i(a_i)-\alpha_i$가 즉각 이득 $g_i(a_i)$보다 빠르게 감소하는 미세한 은닉 이탈(small stealth cut)이 대규모 이탈보다 억제하기 훨씬 어려울 수 있다. 수정된 식 (9)와 부록 A.2 표는 이 메커니즘을 명확히 규명한다.
3. **관측 가능한 시간 변수가 있는 유한 구간 ($T=512$) vs. 무한 지평 벤치마크:** 이론 벤치마크는 정상적 무한 지평 게임이지만, PPO 에이전트는 종단 가치 부트스트랩 없이 $T=512$ 유한 에피소드에서 정규화 시간 $t/T$를 입력으로 받아 학습한다. 유일한 기 내시 균형을 갖는 완비정보 유한 반복게임에서는 역진귀납(backward induction)이 협력을 붕괴시킨다. 제한된 합리성의 학습 에이전트가 정확한 역진귀납을 수행하지 않더라도 $t/T$의 입력은 말기 붕괴를 가능하게 하는 상태 변수를 제공한다. 본문 7.1절은 이를 구조적 차이로 적절히 구분하였다.

### 7.2 수학 관점
1. **식 (9)–(11)의 부호 및 정의역 엄밀성:**
   - 식 (9)를 나눗셈 없는 형태 $g_i(a_i)[1-\delta(1-\alpha_i)] \le \delta[\beta_i(a_i)-\alpha_i]h_i$로 작성함으로써 $\beta_i(a_i)=\alpha_i$에서의 0으로 나누기 및 $\beta_i(a_i)<\alpha_i$에서의 부등호 역전을 완전히 방지하였다.
   - 식 (11)에서 $\mu_D < \tau < \mu_C$는 $z_C = (\tau-\mu_C)/\sigma < 0 < z_D = (\tau-\mu_D)/\sigma$를 함의한다. 기존 원고의 $z_D < 0 < z_C$는 $\mu_D < \tau < \mu_C$와 대수적으로 양립 불가능했다.
   - 명제 3과 부록 A.3의 극한을 $\lim_{\sigma\to 0^+} \delta^*(\sigma) = \frac{g}{g+h}$와 $\lim_{\sigma\to\infty} \delta^*(\sigma) = 2$로 바로잡아 본문–부록 모순을 해소하고 유일한 차단점 $\bar{\sigma} \in (0,\infty)$를 확정하였다.
2. **논문 식 (3) 후생 정의 vs. 아카이브 `mean_total_surplus` 불일치 (중요 수학적 발견):**
   - 본문 식 (3)은 총잉여를 $\mathrm{TS}(p_1, p_2) = (v-c)[q_1(p_1, p_2) + q_2(p_1, p_2)]$로 정의한다. 그러나 $v=2, c=1$이고 외부옵션 효용이 $u_0=0$($\exp(0)=1>0$)이므로 모든 유한 가격에서 $q_1 + q_2 < 1$이 되어, 내시 가격 $p^{\mathrm{N}} \approx 1.472927$에서도 $(v-c)(q_1+q_2) = 0.942862 < 1$을 넘지 못한다.
   - 반면 표 1과 부록 표 3은 `summary.json` 및 `job.json`의 실측치인 `mean_total_surplus` $\approx 1.159588$(B) 및 $1.159660$(A)을 보고한다.
   - 각 시드 `job.json`에 기록된 두 기업의 보수 $(R_0, R_1)$와 평균 가격 $\bar{p}$로부터 비대칭 가격 $(p_0, p_1)$을 역산해 대입해 본 결과, 표준 로짓 사회후생(포괄가치 소비자잉여 + 생산자이윤),
     $$W_{\mathrm{logit}}(p_1, p_2) = \underbrace{\mu\log\!\left(1 + e^{(v-p_1)/\mu} + e^{(v-p_2)/\mu}\right)}_{\mathrm{CS}(p_1,p_2)} + \underbrace{\sum_{i=1}^2 (p_i - c)q_i(p_1, p_2)}_{\pi_1 + \pi_2}$$
     이 대칭 $p^{\mathrm{N}}$에서 $1.161077$이며 20개 시드 전체의 `mean_total_surplus`와 $4\times 10^{-6}\text{–}10^{-3}$ 범위(에피소드 가격 분산에 의한 젠센 부등식 잔차) 내에서 정확히 일치함을 확인하였다. 다만 `acrl_suite_v4_research`에 C++ 확장 모듈의 원본 소스 코드가 포함되어 있지 않으므로, 임의로 식 (3)을 고치지 않고 9절의 미해결 코드 확인 항목으로 명시하였다.

### 7.3 MARL 관점
1. **`audit_probes.json`에서의 실증적 신호 클램핑 포화(Clamping Saturation) 발견:**
   - 식 (4)는 $\min(p_{1,t}, p_{2,t}) \le p^{\mathrm{N}}_{\mathrm{grid}} = 1.473$일 때마다 잠재 신호 평균 $m_t$를 $[\theta_{\mathrm{lo}}, \theta_{\mathrm{hi}}]$ 구간 하한 $\theta_{\mathrm{lo}}$에 클램핑한다.
   - 학습된 PPO 정책들이 이미 $p^{\mathrm{N}}_{\mathrm{grid}} = 1.473$ 부근(평균 $1.4798$)에서 가격을 책정하므로, 인하폭 $0.1$($\Delta p = -0.075$)과 인하폭 $0.3$($\Delta p = -0.225$) 모두가 $\min(p_{1,t_0}, p_{2,t_0})$를 $1.473$ 아래로 떨어뜨린다.
   - `acrl_suite_v4_research/ppo_baseline/202610*/audit_probes.json`을 전수 조사한 결과 다음 두 가지가 직접 확인되었다:
     1. **정보 채널 40개 프로브 쌍(`cut=0.1` vs. `cut=0.3`) 중 39쌍에서 `mean_signed_rival_response_area`와 `mean_continuation_gain`이 기계 정밀도($\sim 10^{-16}$) 수준까지 완전히 동일하다.** 유일한 예외는 Seed `20261005`, 기업 0, $t_0=64$(면적 $9.3945\times 10^{-6}$ vs. $9.4245\times 10^{-6}$)뿐이다.
     2. **정보 채널 40개 프로브 중 19개(양쪽 인하폭 합계 80개 중 38개)는 `mean_signed_rival_response_area == 0.00e+00`으로 완전히 0이다.** 이는 대조군(control) 궤적에서 이미 모든 128회 롤아웃에 걸쳐 $\min(p_{1,t_0}, p_{2,t_0}) \le 1.473$이 성립해 가격 인하 개입이 잠재 신호 $m_{t_0} = \theta_{\mathrm{lo}}$ 자체를 전혀 변화시키지 못했기 때문이다.
   - 이는 본문 5절에 명시된 한계("식 (4)는 최저가격이 내시 기준 이하일 때 포화되므로 상이한 인하폭이 동일한 잠재 신호를 생성할 수 있다")가 실행된 실험 40쌍 중 39쌍에서 실제로 발생했음을 뒷받침한다.
2. **행동 무관 제거 실험에서의 입력 분포 교란(Confound):**
   - $r_{t+1} = \frac{m_t+m_{t-1}}{2} + \varepsilon_t$를 $r_{t+1} \sim \mathcal{N}(1.6, 0.4^2)$로 대체하면 정규화 관측치가 $\mathcal{N}(0,1)$이 되는 반면, 내시 근방에서의 정보 채널 기준선에서는 $m_t \approx \theta_{\mathrm{lo}}$이므로 GRU 입력의 평균과 분산이 함께 달라진다. 이는 본문 2.1절과 8절에 투명하게 서술되어 있다.
3. **창(Window) 재인코딩 GRU vs. 지속적 순환 상태:**
   - 32-스텝 슬라이딩 창마다 영(0) 초기 은닉 상태로 128-유닛 GRU를 다시 실행하는 구조는 에이전트의 기억 지평을 32기로 제한한다.

---

## 8. 문서 간 일관성 감사 (Cross-Document Consistency Audit)

`/Users/gimjunseong/Downloads/main_corrected.tex`와 `/Users/gimjunseong/Downloads/supplement_corrected.tex`를 행 단위로 대조 검사한 결과는 다음과 같다:

1. **수식 번호 및 상호 참조:**
   - 본문의 식 번호 `(1)`–`(11)`이 정확히 유지되었다: `(1)`–`(3)`(수요, 이윤, 인쇄된 총잉여), `(4)`(클램핑 잠재 신호 평균), `(5)`(2기 평균 보고서), `(6)`(정확한 임계 할인인자 $\delta^*$), `(7)`–`(8)`(협력 및 이탈 벨만 방정식), `(9)`(나눗셈 없는 전칭 유인양립조건), `(10)`(편미분 비교정학), `(11)`(가우시안 탐지 격차 도함수).
   - 부록 A.2는 `main-text equation (9)`(`\label{eq:full}`)를 정확히 참조한다.
   - 부록 E.1의 `Tables~\ref{tab:probe_B01}--\ref{tab:probe_A03}`은 `Tables 5–8`로 오류 없이 컴파일된다.
2. **기호 및 공식 정합성:**
   - $V^C - V^P = \frac{h}{1-\delta(1-\alpha)}$, $\delta^* = \frac{g}{g(1-\alpha)+(\beta-\alpha)h}$, 실행 가능성 $(\beta-\alpha)h > \alpha g$, 반례($20/17$), 가우시안 표준화 좌표 $z_C < 0 < z_D$, 전미분 $d\delta^*/d\sigma > 0$, 극한 $g/(g+h)$ 및 $2$, 유일 차단점 $\bar{\sigma}$가 본문과 부록에서 100% 일치한다.
3. **LaTeX 컴파일 검증:**
   - `main_corrected.pdf`(8페이지)와 `supplement_corrected.pdf`(9페이지) 모두 `pdflatex` 컴파일 시 LaTeX 오류 0건, 미정의 참조 0건, `??` 표기 0건으로 정상 생성되었다.

---

## 9. 미해결 과제 및 별도 후속 작업 (Unresolved Issues)

엄격한 검증 원칙에 따라, 수학적 재증명이나 `acrl_suite_v4_research` 재분석만으로는 해결할 수 없는 다음 항목들을 미해결 과제/별도 작업으로 명확히 기록한다:

1. **본문 식 (3) 후생 정의 vs. C++ 네이티브 확장 구현 확인:**
   - 인쇄된 식 (3) $\mathrm{TS} = (v-c)(q_1+q_2)$는 항상 $1$ 미만($p^{\mathrm{N}}$에서 $\approx 0.9429$)이나 아카이브 `mean_total_surplus`($\approx 1.1596$)는 표준 로짓 사회후생 $\mathrm{CS}(p_1, p_2) + \pi_1 + \pi_2$와 일치한다. 아카이브에는 컴파일된 C++ 확장의 SHA256 해시만 존재하므로 원본 C++ 소스 코드 확인 후 식 (3) 수정 여부를 결정해야 한다.
2. **내시 가격 부근에서의 신호 클램핑 포화 (40쌍 중 39쌍 포화):**
   - 비포화(nonsaturating) 신호 매핑 또는 더 넓은 가격 구간에서 재학습 및 감사가 필요하다.
3. **감사 절차의 탐지력(Power) 검증을 위한 양성 대조군(Positive Control) 부재:**
   - 명제 1로 음성 대조군은 증명되었으나, 실제로 처벌 전이를 수행하는 알려진 트리거 정책이나 담합 Q-learning 에이전트에 대한 양성 대조군 테스트는 아카이브에 없다.
4. **행동 무관 채널 대체의 입력 분포 교란 분리:**
   - 모멘트를 일치시킨(moment-matched) 행동 무관 대조군 실험이 필요하다.
5. **관측 가능한 시간 $t/T$를 가진 유한 구간 ($T=512$) 영향 분리:**
   - 시간 입력이 없고 종단 부트스트랩이 있는 연속 과제(continuing-task) 제거 실험이 필요하다.
6. **원본 MCMC 보정(Calibration) 데이터 및 `posterior_draws.csv` 미수록:**
   - 아카이브에는 해시와 수렴 진단치($\hat{R}=1.008945$, $\mathrm{ESS}=606.86$)만 포함되며 원본 라벨 데이터와 표본 CSV 파일 자체는 외부에 있다.
7. **미완료 SAC 실행 및 선행 문헌 베이스라인:**
   - 전체 계획에 있던 미완료 SAC 조건 및 Calvano et al. (2021, *IJIO*) 계열 불완전 모니터링 표형(tabular) Q-learning 비교는 본 PPO 아카이브 범위 밖이다.
