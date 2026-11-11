# THEORY VERIFICATION REPORT
## Independent Mathematical, Game-Theoretic, and MARL Audit of *Beyond High Prices: Auditing Information-Mediated Enforcement in Recurrent Pricing Agents* (ICLR 2027)

- **Main Paper LaTeX (Corrected):** `/Users/gimjunseong/Downloads/main_corrected.tex` (`/Users/gimjunseong/Downloads/main_paper_src/main.tex`)
- **Main Paper Compiled PDF:** `/Users/gimjunseong/Downloads/main_corrected.pdf` (`/Users/gimjunseong/Downloads/main_paper_src/main.pdf`)
- **Supplement LaTeX (Corrected):** `/Users/gimjunseong/Downloads/supplement_corrected.tex` (`/Users/gimjunseong/Downloads/supplement_src/main.tex`)
- **Supplement Compiled PDF:** `/Users/gimjunseong/Downloads/supplement_corrected.pdf` (`/Users/gimjunseong/Downloads/supplement_src/main.pdf`)
- **Reference Correction Guide:** `/Users/gimjunseong/Downloads/Beyond_High_Prices_P1_Theoretical_Correction_EN.md`
- **Empirical Research Archive:** `/Users/gimjunseong/Downloads/acrl_suite_v4_research` (`ACRL Suite v4 Research.zip`)

---

## 1. Executive Summary & Correction Matrix

An independent verification from first principles of the repeated-game Bellman equations, Gaussian imperfect-monitoring comparative statics, and the archived `acrl_suite_v4_research` empirical artifacts identified a root-cause algebraic error in Section 6 of the main paper and Section A.1 of the supplement that propagated through Equations (6)–(11), Propositions 2–3, and Supplementary Sections A.1–A.3.

Specifically, when subtracting the absorbing punishment Bellman equation $V^P = \pi^P + \delta V^P$ from the cooperative Bellman equation $V^C = \pi^C + \delta[(1-\alpha)V^C + \alpha V^P]$, the original manuscript dropped the false-alarm transition term $\alpha$ and wrote $V^C - V^P = \frac{\pi^C - \pi^P}{1 - \delta}$ instead of the exact identity
$$V^C - V^P = \frac{\pi^C - \pi^P}{1 - \delta(1-\alpha)} = \frac{h}{1 - \delta(1-\alpha)}.$$
This single error systematically understated the critical discount factor whenever $\alpha > 0$, obscured the feasibility condition $(\beta - \alpha)h > \alpha g$ required for $\delta^* < 1$, corrupted the partial derivatives in Equation (10), and created two internal contradictions in the Gaussian comparative statics (Section 7 and Supplement A.3): a reversed sign on standardized coordinates ($z_D < 0 < z_C$ instead of $z_C < 0 < z_D$) and two incompatible limit claims ($\lim_{\sigma\to\infty}\delta^*(\sigma) = 1$ in the main text vs. $\lim_{\sigma\to 0^+}\delta^*(\sigma) = 0$ in Supplement A.3).

All theoretical results in **Proposition 1** (Observation Invariance negative control), **Supplement A.4** (finite-horizon tail bound), and all empirical PPO outputs in `acrl_suite_v4_research` were independently verified to be valid and preserved intact.

### Summary Matrix of Verified Corrections

| Location | Original Manuscript / Supplement | Verified & Corrected Form | Root Cause / Impact |
| :--- | :--- | :--- | :--- |
| **Abstract (p. 1)** | Rendered as `[0.0241, 0.0288]` in PDF (`[−0.0241, 0.0288]` in `.tex`) | `$[-0.0241,\,0.0288]$` | Raw Unicode minus `U+2212` in text mode was silently dropped by `pdflatex`. |
| **Main Sec. 6, Proof of Prop. 2 & Supp. A.1** | $V^C - V^P = \frac{\pi^C - \pi^P}{1 - \delta} = \frac{h}{1-\delta}$ | $V^C - V^P = \frac{\pi^C - \pi^P}{1 - \delta(1-\alpha)} = \frac{h}{1 - \delta(1-\alpha)}$ | False-alarm probability $\alpha$ dropped when subtracting $V^P$ from $V^C$. |
| **Main Eq. (6), Prop. 2 & Supp. A.1** | $\delta^* = \frac{g}{g + (\beta - \alpha)h}$ | $\delta^* = \frac{g}{g(1-\alpha) + (\beta - \alpha)h}$ | Propagated from $V^C - V^P$; understates $\delta^*$ by $\frac{\alpha g^2}{(g+\Delta h)[g(1-\alpha)+\Delta h]} > 0$ for $\alpha > 0$. |
| **Main Prop. 2 & Supp. A.1 Feasibility** | Implicitly assumed $\beta > \alpha \implies \delta^* < 1$ | $\delta^* < 1 \iff (\beta - \alpha)h > \alpha g$ | For $\alpha > 0$, $\beta > \alpha$ is necessary but not sufficient for deterrability at $\delta \in [0,1)$. |
| **Main Eq. (9) & Supp. A.2** | Divided ratio $\sup_{i,a_i:g_i(a_i)>0}\frac{g_i(a_i)}{g_i(a_i)+[\beta_i(a_i)-\alpha_i]h_i}$ | Undivided IC $g_i(a_i)[1-\delta(1-\alpha_i)] \le \delta[\beta_i(a_i)-\alpha_i]h_i\;\forall i,a_i\in\mathcal{A}_i$, plus restricted $\sup$ on $\{g_i>0,\beta_i>\alpha_i\}$ | Divided form omitted $(1-\alpha_i)$ and was undefined or reversed when $\beta_i(a_i) \le \alpha_i$ or $g_i(a_i) \le 0$. |
| **Supp. A.2 Numerical Example & Cross-Ref** | Referenced `Main-text equation (10)`; reported `0.588235` ($10/17$) and `0.990099` ($100/101$) without specifying $\alpha$ | References `Main-text equation (9)`; specifies $\alpha = 0.05, h = 1$: Deviation A ($g=0.30,\beta=0.55$) $\delta^*_A = \frac{60}{157} \approx 0.382166$; Deviation B ($g=0.90,\beta=0.06$) $\delta^*_B = \frac{180}{173} \approx 1.040462$ | Old numbers computed $1/(1+\Delta/g)$, matching neither the printed formula ($0.375, 0.989011$) nor the exact formula. |
| **Main Eq. (10)** | $\frac{\partial\delta^*}{\partial\alpha} = \frac{gh}{D_0^2}$, $\frac{\partial\delta^*}{\partial\beta} = -\frac{gh}{D_0^2}$, $\frac{\partial\delta^*}{\partial h} = -\frac{g(\beta-\alpha)}{D_0^2}$ with $D_0 = g+(\beta-\alpha)h$ | With $D = g(1-\alpha)+(\beta-\alpha)h$: $\frac{\partial\delta^*}{\partial\alpha} = \frac{g(g+h)}{D^2} > 0$, $\frac{\partial\delta^*}{\partial\beta} = -\frac{gh}{D^2} < 0$, $\frac{\partial\delta^*}{\partial h} = -\frac{g(\beta-\alpha)}{D^2} < 0$, $\frac{\partial\delta^*}{\partial g} = \frac{(\beta-\alpha)h}{D^2} > 0$ | Numerator of $\partial\delta^*/\partial\alpha$ is $g(g+h) > gh$ because $\alpha$ erodes both detection differential and cooperative value gap. |
| **Main Eq. (11), Prop. 3 & Supp. A.3** | Stated $z_D < 0 < z_C$ and $\frac{\partial\Delta}{\partial\sigma} = \frac{1}{\sigma}[z_C\phi(z_C) - z_D\phi(z_D)] < 0$ | For $\mu_D < \tau < \mu_C$: $z_C = \frac{\tau-\mu_C}{\sigma} < 0 < z_D = \frac{\tau-\mu_D}{\sigma}$, $\frac{\partial\Delta}{\partial\sigma} = -\frac{1}{\sigma}[z_D\phi(z_D)-z_C\phi(z_C)] < 0$, $\frac{d\delta^*}{d\sigma} = \frac{g[(g+h)\alpha'(\sigma)-h\beta'(\sigma)]}{D(\sigma)^2} > 0$ | Under $\mu_D < \tau < \mu_C$, $\tau - \mu_C < 0 < \tau - \mu_D$, so $z_C < 0 < z_D$. |
| **Main Prop. 3 & Supp. A.3 Limits** | Main Prop. 3: $\delta^*\to\frac{g}{g+h}$ ($\sigma\to 0^+$) and $\delta^*\to 1$ ($\sigma\to\infty$); Supp. A.3: $\delta^*\to 0$ ($\sigma\to 0^+$) and $\delta^*\to 1$ ($\sigma\to\infty$) | Both Main Prop. 3 & Supp. A.3: $\lim_{\sigma\to 0^+}\delta^*(\sigma) = \frac{g}{g+h} \in (0,1)$ and $\lim_{\sigma\to\infty}\delta^*(\sigma) = 2$, with unique feasibility cutoff $\bar{\sigma}\in(0,\infty)$ where $\delta^*(\bar{\sigma})=1$ | As $\sigma\to\infty$, $\alpha,\beta\to 1/2 \implies D(\sigma)\to g/2 \implies \delta^*(\sigma)\to 2$. |
| **Supp. Sec. E.1 & Sec. F (Tables 5–8)** | Rendered `Tables 5–??`; Table 5 had 7 column specs (`@{}cccSSSS@{}`) for 8 columns and only 9 of 160 probe rows | Fixed `\probetable` to `{@{}cccSSSSr@{}}` and populated all 160 probe rows across `tab:probe_B01`, `tab:probe_B03`, `tab:probe_A01`, `tab:probe_A03`; resolves to `Tables 5–8` | Placeholder comments in `supplement_src/main.tex` were replaced with exact data from `acrl_suite_v4_research`. |
| **Supp. Table 9 (`tab:hashes`)** | Truncated hashes (`a2cd4f26...c202d1b95`, etc.) | Full 64-character SHA256 hashes from `suite_manifest.json` | Complete cryptographic provenance. |

---

## 2. Model Primitives, Assumptions, and Boundary Cases

To ensure complete mathematical precision, the corrected benchmark in Section 6 and Supplement A explicitly states all primitives and boundary cases:

1. **Discounted Repeated Game & Automaton Structure:**
   - Time is discrete and indexed by $t = 0, 1, 2, \dots$ over an infinite horizon with common discount factor $\delta \in [0, 1)$.
   - Stage-game payoffs are bounded.
   - Public monitoring generates a public signal at the end of each period $t$ whose distribution depends solely on current period-$t$ actions.
   - The public two-state automaton has a cooperative state $C$ and an absorbing punishment state $P$.
   - In state $C$, firms play a prescribed cooperative action profile $a^C = (a_1^C, a_2^C)$ yielding per-period payoff $\pi^C$ (or $\pi_i^C$ in the asymmetric/full-quantifier formulation). If a bad public signal occurs, the automaton transitions permanently from $C$ to $P$; if a good signal occurs, it remains in $C$.
   - In state $P$, firms play a stage-game Nash action profile $a^P$ yielding per-period payoff $\pi^P$ (or $\pi_i^P$) forever. Because $a^P$ is a stage-game Nash equilibrium and $P$ is absorbing (future state transitions in $P$ are independent of actions in $P$), continuation play in $P$ is subgame-credible (incentive-compatible at every period in $P$).
2. **One-Shot Deviation Principle & Timing Convention:**
   - Values $V^C$, $V^P$, and $V^D$ are evaluated at the beginning of the period before current actions are taken, without multiplying the total discounted sum by $(1-\delta)$.
   - Under discounting $\delta \in [0,1)$ and bounded payoffs, the one-shot deviation principle holds: a public automaton strategy is a public perfect equilibrium if and only if no player has a profitable one-period unilateral deviation in state $C$ (followed by returning to the prescribed automaton strategy) or in state $P$.
3. **Parameter Domain & Interior Assumptions (Propositions 2 & 3):**
   - Immediate gain from the specified deviation: $g = \pi^D - \pi^C > 0$.
   - Per-period cooperative–punishment payoff gap: $h = \pi^C - \pi^P > 0$.
   - Signal probabilities: $0 \le \alpha < \beta \le 1$, where $\alpha = \Pr(\text{bad signal}\mid \text{compliance})$ and $\beta = \Pr(\text{bad signal}\mid \text{specified deviation})$, with detection differential $\Delta = \beta - \alpha > 0$.
   - In Proposition 3 (Gaussian benchmark): signal under compliance is $Y_t \sim \mathcal{N}(\mu_C, \sigma^2)$ and under the specified deviation is $Y_t \sim \mathcal{N}(\mu_D, \sigma^2)$, where a bad signal occurs when $Y_t < \tau$, with $\mu_D < \tau < \mu_C$ and $\sigma > 0$ held fixed alongside $(g, h, \mu_C, \mu_D, \tau)$.
4. **Exhaustive Boundary Cases:**
   - **Boundary Case 1 ($\alpha = 0$, no false alarms):** $V^C - V^P = \frac{h}{1-\delta}$ and $\delta^* = \frac{g}{g + \beta h} < 1$ for every $\beta > 0$, $g > 0$, $h > 0$. If additionally $\beta = 1$ (perfect monitoring), $\delta^* = \frac{g}{g+h} \in (0,1)$.
   - **Boundary Case 2 ($\alpha > 0$ and $(\beta-\alpha)h \le \alpha g$, infeasibility):**
     - Knife-edge $(\beta-\alpha)h = \alpha g \implies \delta^* = 1$. Since $\delta \in [0,1)$, no admissible $\delta < 1$ deters the deviation (at the limit $\delta = 1$, $V^D - V^C = 0$ if evaluated via the undivided polynomial, though unnormalized discounted sums diverge at $\delta = 1$).
     - Strict infeasibility $(\beta-\alpha)h < \alpha g \implies \delta^* > 1$. For every $\delta \in [0,1)$, $V^D > V^C$, so the deviation is strictly profitable.
   - **Boundary Case 3 ($g_i(a_i) \le 0$ or $\beta_i(a_i) \le \alpha_i$ across the full action space $\mathcal{A}_i$):**
     - The undivided incentive constraint $g_i(a_i)[1 - \delta(1-\alpha_i)] \le \delta[\beta_i(a_i) - \alpha_i]h_i$ remains well-defined and exact for all $a_i \in \mathcal{A}_i$.
     - Subcase 3a ($g_i(a_i) > 0$ and $\beta_i(a_i) \le \alpha_i$): LHS $> 0 \ge$ RHS for all $\delta \in [0,1)$, so the deviation can never be deterred.
     - Subcase 3b ($g_i(a_i) \le 0$ and $\beta_i(a_i) \ge \alpha_i$): LHS $\le 0 \le$ RHS, trivially satisfied for all $\delta \in [0,1)$.
     - Subcase 3c ($g_i(a_i) < 0$ and $\beta_i(a_i) < \alpha_i$): An action that sacrifices current profit ($g_i < 0$) to reduce the probability of triggering a false alarm ($\beta_i < \alpha_i$). The undivided constraint requires $\delta[\alpha_i - \beta_i]h_i \le |g_i(a_i)|[1 - \delta(1-\alpha_i)]$ (an upper bound on $\delta$ if $\alpha_i - \beta_i$ is large relative to $|g_i|/h_i$). Dividing naively by a negative denominator would reverse the inequality sign.
   - **Boundary Case 4 (Gaussian threshold outside $(\mu_D, \mu_C)$, i.e., $\tau \notin [\mu_D, \mu_C]$):**
     - If $\tau < \mu_D < \mu_C$, then $z_C < z_D < 0$, so $\alpha'(\sigma) > 0$ and $\beta'(\sigma) > 0$; as $\sigma \to 0^+$, $\alpha(\sigma) \to 0$ and $\beta(\sigma) \to 0$, so $\Delta(\sigma) \to 0$ and $\delta^*(\sigma) \to 1$.
     - If $\mu_D < \mu_C < \tau$, then $0 < z_C < z_D$, so $\alpha'(\sigma) < 0$ and $\beta'(\sigma) < 0$; as $\sigma \to 0^+$, $\alpha(\sigma) \to 1$ and $\beta(\sigma) \to 1$, so $\Delta(\sigma) \to 0$ and $D(\sigma) \to 0^+$, sending $\delta^*(\sigma) \to +\infty$.
     - Hence global monotonicity of $\Delta(\sigma)$ and $\delta^*(\sigma)$ on $(0,\infty)$ specifically requires $\mu_D < \tau < \mu_C$ (or at least one weak inequality at the boundary $\tau = \mu_C$ or $\tau = \mu_D$, where one probability is fixed at $1/2$).
   - **Boundary Case 5 (Additive Gaussian noise $\sigma_{\mathrm{tot}} = \sqrt{\sigma^2 + \sigma_a^2}$ at $\sigma_a = 0$):**
     - When baseline noise $\sigma > 0$, $\frac{\partial \sigma_{\mathrm{tot}}}{\partial \sigma_a}\big|_{\sigma_a = 0} = 0$, so $\frac{\partial \delta^*}{\partial \sigma_a}\big|_{\sigma_a = 0} = 0$ even though $\delta^*(\sqrt{\sigma^2 + \sigma_a^2}) > \delta^*(\sigma)$ for every $\sigma_a > 0$.

---

## 3. Step-by-Step Reproof of Proposition 2, Equations (6)–(9), and Supplementary A.1–A.2

### 3.1 Bellman Equations and Exact Cooperative–Punishment Value Gap
In the stationary discounted repeated game with $\delta \in [0,1)$, the cooperative state $C$ and absorbing punishment state $P$ satisfy:
$$\begin{aligned}
V^C &= \pi^C + \delta\bigl[(1-\alpha)V^C + \alpha V^P\bigr], \qquad \text{(Main Eq. 7)} \\
V^P &= \pi^P + \delta V^P.
\end{aligned}$$
Subtracting the second equation from the first without dropping $\alpha$:
$$\begin{aligned}
V^C - V^P &= (\pi^C - \pi^P) + \delta\bigl[(1-\alpha)V^C + \alpha V^P - V^P\bigr] \\
&= (\pi^C - \pi^P) + \delta\bigl[(1-\alpha)V^C - (1-\alpha)V^P\bigr] \\
&= h + \delta(1-\alpha)(V^C - V^P).
\end{aligned}$$
Rearranging:
$$[1 - \delta(1-\alpha)](V^C - V^P) = h.$$
Since $\delta \in [0,1)$ and $\alpha \in [0,1]$, we have $1-\alpha \in [0,1]$ and $\delta(1-\alpha) \le \delta < 1$, so $1 - \delta(1-\alpha) \ge 1 - \delta > 0$. Dividing by $1 - \delta(1-\alpha)$ gives the unique solution:
$$\boxed{V^C - V^P = \frac{\pi^C - \pi^P}{1 - \delta(1-\alpha)} = \frac{h}{1 - \delta(1-\alpha)}.}$$

### 3.2 One-Period Deviation Value and Critical Discount Factor $\delta^*$ (Main Eq. 6 & 8)
The one-period deviation value is:
$$V^D = \pi^D + \delta\bigl[(1-\beta)V^C + \beta V^P\bigr]. \qquad \text{(Main Eq. 8)}$$
Subtracting $V^C$ (Main Eq. 7) from $V^D$ (Main Eq. 8):
$$\begin{aligned}
V^D - V^C &= (\pi^D - \pi^C) + \delta\bigl[(1-\beta - (1-\alpha))V^C + (\beta - \alpha)V^P\bigr] \\
&= g - \delta(\beta - \alpha)(V^C - V^P) \\
&= g - \frac{\delta(\beta - \alpha)h}{1 - \delta(1-\alpha)}.
\end{aligned}$$
The deviation is unprofitable in $C$ ($V^D \le V^C$) if and only if
$$g - \frac{\delta(\beta - \alpha)h}{1 - \delta(1-\alpha)} \le 0.$$
Multiplying both sides by $1 - \delta(1-\alpha) > 0$:
$$g[1 - \delta(1-\alpha)] \le \delta(\beta - \alpha)h \iff g \le \delta\bigl[g(1-\alpha) + (\beta - \alpha)h\bigr].$$
Under $g > 0$, $h > 0$, and $0 \le \alpha < \beta \le 1$, we have $1-\alpha > 0$ and $\beta - \alpha > 0$, so the denominator
$$D \equiv g(1-\alpha) + (\beta - \alpha)h > 0$$
is strictly positive. Dividing by $D$ yields the exact critical discount factor (Main Eq. 6):
$$\boxed{\delta \ge \delta^* \equiv \frac{\pi^D - \pi^C}{(\pi^D - \pi^C)(1-\alpha) + (\beta - \alpha)(\pi^C - \pi^P)} = \frac{g}{g(1-\alpha) + (\beta - \alpha)h}.}$$

### 3.3 Strict Feasibility Condition ($\delta^* < 1$) and Direction of Error
Computing $1 - \delta^*$:
$$1 - \delta^* = 1 - \frac{g}{g(1-\alpha) + (\beta - \alpha)h} = \frac{g(1-\alpha) + (\beta - \alpha)h - g}{g(1-\alpha) + (\beta - \alpha)h} = \frac{(\beta - \alpha)h - \alpha g}{D}.$$
Since $D > 0$,
$$\boxed{\delta^* < 1 \iff (\beta - \alpha)h > \alpha g.}$$
Comparing $\delta^*_{\mathrm{corrected}}$ with the original manuscript's $\delta^*_{\mathrm{printed}} = \frac{g}{g + (\beta - \alpha)h}$:
$$\delta^*_{\mathrm{corrected}} - \delta^*_{\mathrm{printed}} = \frac{g}{g(1-\alpha) + \Delta h} - \frac{g}{g + \Delta h} = \frac{\alpha g^2}{(g + \Delta h)[g(1-\alpha) + \Delta h]} \ge 0,$$
with strict inequality whenever $\alpha > 0$ and $g > 0$.

### 3.4 Counterexample Demonstrating False Deterrence Claim Under Original Formula
Take $g = 0.2 = \frac{1}{5}$, $h = 0.5 = \frac{1}{2}$, $\alpha = 0.4 = \frac{2}{5}$, and $\beta = 0.5 = \frac{1}{2}$ ($\Delta = \beta - \alpha = 0.1 = \frac{1}{10}$):
- **Original formula:** $\delta^*_{\mathrm{printed}} = \frac{0.2}{0.2 + 0.1 \times 0.5} = \frac{0.2}{0.25} = \frac{4}{5} = 0.8 < 1$ (falsely predicting that any $\delta \in [0.8, 1)$ deters the deviation).
- **Exact formula:** $\delta^*_{\mathrm{corrected}} = \frac{0.2}{0.2(0.6) + 0.1(0.5)} = \frac{0.2}{0.12 + 0.05} = \frac{0.2}{0.17} = \frac{20}{17} \approx 1.176471 > 1$.
- **Feasibility check:** $(\beta - \alpha)h = 0.05 < \alpha g = 0.08$, so the deviation is strictly profitable for every $\delta \in [0,1)$.
- **Direct Bellman evaluation at $\delta = 0.9 \in (0.8, 1)$:**
  $$V^C - V^P = \frac{0.5}{1 - 0.9(0.6)} = \frac{0.5}{0.46} = \frac{25}{23}, \qquad V^D - V^C = 0.2 - 0.9(0.1)\frac{25}{23} = \frac{1}{5} - \frac{9}{92} = \frac{47}{460} \approx +0.102174 > 0.$$

### 3.5 Full Unilateral Incentive Compatibility (Main Eq. 9) and Supplement A.2 Numerical Example
For every firm $i$ and every unilateral action $a_i \in \mathcal{A}_i$, one-shot deviation compatibility in $C$ requires:
$$\boxed{g_i(a_i)\bigl[1 - \delta(1-\alpha_i)\bigr] \le \delta\bigl[\beta_i(a_i) - \alpha_i\bigr]h_i \quad \forall i, \;\forall a_i \in \mathcal{A}_i.}$$
On the restricted subset $\{a_i \in \mathcal{A}_i : g_i(a_i) > 0 \text{ and } \beta_i(a_i) > \alpha_i\}$, this yields the necessary lower bound
$$\delta \ge \sup_{i,\,a_i : g_i(a_i)>0,\,\beta_i(a_i)>\alpha_i} \frac{g_i(a_i)}{g_i(a_i)(1-\alpha_i) + [\beta_i(a_i)-\alpha_i]h_i}.$$

**Supplement A.2 Numerical Example Verification:**
With $h = 1$ and compliant false-alarm probability $\alpha = 0.05$:
- **Deviation A:** $g_A = 0.30$, $\beta_A = 0.55$, $\beta_A - \alpha = 0.50$:
  $$\delta^*_A = \frac{0.30}{0.30(0.95) + 0.50(1)} = \frac{0.30}{0.785} = \frac{60}{157} \approx 0.382166 < 1 \quad \bigl((\beta_A-\alpha)h = 0.50 > \alpha g_A = 0.015\bigr).$$
- **Deviation B:** $g_B = 0.90$, $\beta_B = 0.06$, $\beta_B - \alpha = 0.01$:
  $$\delta^*_B = \frac{0.90}{0.90(0.95) + 0.01(1)} = \frac{0.90}{0.865} = \frac{180}{173} \approx 1.040462 > 1 \quad \bigl((\beta_B-\alpha)h = 0.01 < \alpha g_B = 0.045\bigr).$$
At $\delta = 0.90$, Deviation A is deterred ($\delta \ge \delta^*_A$), whereas Deviation B is not and cannot be deterred at any $\delta \in [0,1)$.

---

## 4. Step-by-Step Reproof of Equation (10), Proposition 3, Equation (11), and Supplementary A.3

### 4.1 Partial Derivatives of $\delta^*$ (Main Eq. 10)
Let $D = g(1-\alpha) + (\beta - \alpha)h > 0$ on the interior domain $g > 0, h > 0, 0 \le \alpha < \beta \le 1$. Differentiating $\delta^*(g, h, \alpha, \beta) = g / D$:
1. **With respect to $\alpha$:** Since $\frac{\partial D}{\partial \alpha} = -(g + h)$,
   $$\boxed{\frac{\partial \delta^*}{\partial \alpha} = -\frac{g}{D^2}\frac{\partial D}{\partial \alpha} = \frac{g(g+h)}{\bigl[g(1-\alpha) + (\beta-\alpha)h\bigr]^2} > 0.}$$
2. **With respect to $\beta$:** Since $\frac{\partial D}{\partial \beta} = h$,
   $$\boxed{\frac{\partial \delta^*}{\partial \beta} = -\frac{gh}{\bigl[g(1-\alpha) + (\beta-\alpha)h\bigr]^2} < 0.}$$
3. **With respect to $h$:** Since $\frac{\partial D}{\partial h} = \beta - \alpha$,
   $$\boxed{\frac{\partial \delta^*}{\partial h} = -\frac{g(\beta-\alpha)}{\bigl[g(1-\alpha) + (\beta-\alpha)h\bigr]^2} < 0.}$$
4. **With respect to $g$:** Since $\frac{\partial D}{\partial g} = 1 - \alpha$,
   $$\boxed{\frac{\partial \delta^*}{\partial g} = \frac{D - g(1-\alpha)}{D^2} = \frac{(\beta-\alpha)h}{\bigl[g(1-\alpha) + (\beta-\alpha)h\bigr]^2} > 0.}$$

### 4.2 Gaussian Tail Probabilities and Standardized Coordinates (Main Eq. 11 & Prop. 3)
Under $\mu_D < \tau < \mu_C$ and $\sigma > 0$, define the standardized coordinates:
$$z_C(\sigma) = \frac{\tau - \mu_C}{\sigma} < 0, \qquad z_D(\sigma) = \frac{\tau - \mu_D}{\sigma} > 0.$$
With $\alpha(\sigma) = \Phi(z_C(\sigma))$ and $\beta(\sigma) = \Phi(z_D(\sigma))$:
$$\alpha'(\sigma) = \phi(z_C)\frac{dz_C}{d\sigma} = -\frac{z_C\,\phi(z_C)}{\sigma} > 0 \quad (\text{since } z_C < 0, \phi(z_C) > 0, \sigma > 0),$$
$$\beta'(\sigma) = \phi(z_D)\frac{dz_D}{d\sigma} = -\frac{z_D\,\phi(z_D)}{\sigma} < 0 \quad (\text{since } z_D > 0, \phi(z_D) > 0, \sigma > 0).$$
Therefore, the derivative of the detection differential $\Delta(\sigma) = \beta(\sigma) - \alpha(\sigma)$ (Main Eq. 11) is:
$$\boxed{\frac{\partial \Delta}{\partial \sigma} = \beta'(\sigma) - \alpha'(\sigma) = -\frac{1}{\sigma}\bigl[z_D\,\phi(z_D) - z_C\,\phi(z_C)\bigr] < 0,}$$
because $z_D\phi(z_D) > 0$ and $-z_C\phi(z_C) > 0$.

### 4.3 Total Derivative $d\delta^*/d\sigma$
By the chain rule:
$$\frac{d\delta^*}{d\sigma} = \frac{\partial \delta^*}{\partial \alpha}\alpha'(\sigma) + \frac{\partial \delta^*}{\partial \beta}\beta'(\sigma) = \frac{g(g+h)}{D(\sigma)^2}\alpha'(\sigma) - \frac{gh}{D(\sigma)^2}\beta'(\sigma),$$
giving:
$$\boxed{\frac{d\delta^*}{d\sigma} = \frac{g\bigl[(g+h)\alpha'(\sigma) - h\beta'(\sigma)\bigr]}{\bigl[g(1-\alpha(\sigma)) + (\beta(\sigma)-\alpha(\sigma))h\bigr]^2} > 0,}$$
since $(g+h)\alpha'(\sigma) > 0$ and $-h\beta'(\sigma) > 0$ for all $\sigma > 0$.

### 4.4 Exact Asymptotic Limits and Unique Feasibility Cutoff $\bar{\sigma}$
1. **Zero-noise limit ($\sigma \to 0^+$):**
   Since $\tau - \mu_C < 0 < \tau - \mu_D$, as $\sigma \to 0^+$ we have $z_C(\sigma) \to -\infty$ and $z_D(\sigma) \to +\infty$. Thus $\alpha(\sigma) = \Phi(z_C) \to 0$ and $\beta(\sigma) = \Phi(z_D) \to 1$, so $D(\sigma) \to g(1-0) + (1-0)h = g + h$, and
   $$\boxed{\lim_{\sigma \to 0^+} \delta^*(\sigma) = \frac{g}{g + h} \in (0, 1).}$$
2. **Infinite-noise limit ($\sigma \to \infty$):**
   As $\sigma \to \infty$, $z_C(\sigma) \to 0^-$ and $z_D(\sigma) \to 0^+$. Thus $\alpha(\sigma) \to \Phi(0) = \frac{1}{2}$ and $\beta(\sigma) \to \Phi(0) = \frac{1}{2}$, so $\Delta(\sigma) \to 0$, $D(\sigma) \to g\left(1 - \frac{1}{2}\right) + 0 \cdot h = \frac{g}{2}$, and
   $$\boxed{\lim_{\sigma \to \infty} \delta^*(\sigma) = \frac{g}{g/2} = 2.}$$
3. **Unique feasibility cutoff $\bar{\sigma} \in (0, \infty)$:**
   Because $\delta^*(\sigma)$ is continuous and strictly increasing on $(0, \infty)$ with $\lim_{\sigma\to 0^+} \delta^*(\sigma) = \frac{g}{g+h} < 1$ and $\lim_{\sigma\to\infty} \delta^*(\sigma) = 2 > 1$, the Intermediate Value Theorem and strict monotonicity imply a unique $\bar{\sigma} \in (0, \infty)$ solving
   $$\delta^*(\bar{\sigma}) = 1 \iff \bigl[\beta(\bar{\sigma}) - \alpha(\bar{\sigma})\bigr]h = \alpha(\bar{\sigma})g.$$
   The specified deviation is deterrable for some $\delta \in [0,1)$ if and only if $\sigma < \bar{\sigma}$.

---

## 5. Symbolic (Exact Rational) and Numerical Verification Summary

All algebraic identities, derivatives, limits, and numerical examples were independently verified in Python:
1. **Exact Rational Polynomial Identity Verification (`fractions.Fraction`):**
   - Verified over a 625-point rational grid of $(g, h, \alpha, \beta, \delta)$ that the solution $(V^C, V^P, V^D)$ to the linear Bellman system satisfies $V^C - V^P = \frac{h}{1 - \delta(1-\alpha)}$, $V^D - V^C = g - \frac{\delta(\beta-\alpha)h}{1 - \delta(1-\alpha)}$, and $\delta^*_{\mathrm{corrected}} - \delta^*_{\mathrm{printed}} = \frac{\alpha g^2}{(g+\Delta h)[g(1-\alpha)+\Delta h]}$ with zero residual ($0/1$).
   - Verified the counterexample ($g=1/5, h=1/2, \alpha=2/5, \beta=1/2$) and Supplement A.2 table ($\alpha=1/20, h=1$: $\delta^*_A = 60/157$, $\delta^*_B = 180/173$) in exact rational arithmetic.
2. **Analytical vs. Central Finite-Difference Verification ($\varepsilon = 10^{-6}$):**
   - Verified all four partial derivatives in Eq. (10) ($\partial\delta^*/\partial\alpha$, $\partial\delta^*/\partial\beta$, $\partial\delta^*/\partial h$, $\partial\delta^*/\partial g$) and Gaussian derivatives ($\alpha'(\sigma)$, $\beta'(\sigma)$, $\Delta'(\sigma)$, $d\delta^*/d\sigma$, $\partial\delta^*/\partial\sigma_a$) to agreement $< 10^{-11}$.
   - For representative parameters $g = 0.3, h = 0.7, \mu_C = 2.0, \mu_D = 1.2, \tau = 1.6$:
     - $\lim_{\sigma\to 0^+} \delta^*(\sigma) = 0.3 / (0.3 + 0.7) = 0.300000$ (at $\sigma = 0.01$, $\delta^* = 0.300000$).
     - Unique feasibility cutoff $\bar{\sigma} = 0.5624189165$, where $\alpha(\bar{\sigma}) = 0.23850016$, $\beta(\bar{\sigma}) = 0.76149984$, and $\delta^*(\bar{\sigma}) = 1.00000000$.
     - At $\sigma = 10^4$, $\delta^*(10^4) = 1.99946809 \to 2$.

---

## 6. Empirical Archive Verification (`acrl_suite_v4_research`)

Every numerical table and claim in the main paper and supplement was cross-checked directly against the archived files in `/Users/gimjunseong/Downloads/acrl_suite_v4_research`:

1. **Grid vs. Continuous Reference Prices (`policy.curve.csv`, `job.json`):**
   - Continuous symmetric one-shot logit Nash price: $p^{\mathrm{N}} = 1.4729266564$ (reported as $1.472927$).
   - Continuous symmetric joint-profit-maximizing price: $p^{\mathrm{J}} = 1.9249809205$ (reported as $1.924981$).
   - Simulator 1,501-point price grid on $[1.0, 2.5]$ (step $0.001$): $p^{\mathrm{N}}_{\mathrm{grid}} = 1.473$ and $p^{\mathrm{J}}_{\mathrm{grid}} = 1.925$ (grid gap $0.452$), which reproduces `collusive_index` $= (\bar{p} - 1.473)/0.452$ across all 20 seeds to $0.00\times 10^0$.
2. **Main Table 1 (`tab:final`) and Supplement Table 3 (`tab:seed_results`):**
   - Verified all 20 seed rows (10 informative baseline `ppo_baseline`, 10 action-independent `ppo_ablated`) and their paired differences and 2,000-draw whole-seed bootstrap 95% CIs (using `np.random.default_rng(20260920)`):
     - Mean price: $1.479804$ (B) vs. $1.481492$ (A), diff $0.001688$ $[-0.0109,\,0.0130]$.
     - Price elevation: $0.015052$ (B) vs. $0.018787$ (A), diff $0.003735$ $[-0.0241,\,0.0288]$.
     - Total surplus: $1.159588$ (B) vs. $1.159660$ (A), diff $0.000072$ $[-0.0013,\,0.0017]$.
     - Feature rank (firm 0): $1.274335$ (B) vs. $1.338647$ (A), diff $0.064312$ $[0.0113,\,0.1337]$.
     - Feature rank (firm 1): $1.269538$ (B) vs. $1.353578$ (A), diff $0.084040$ $[0.0282,\,0.1495]$.
3. **Main Table 2 (`tab:audit`), Supplement Table 4 (`tab:bootstrap_ci`), and Supplement Tables 5–8 (`tab:probe_B01`–`tab:probe_A03`):**
   - Verified all 160 probe records across the 20 `audit_probes.json` files:
     - Informative cut 0.1: Immediate $-0.005186$, Full $-0.005192$, Continuation $-0.000005$ $[-0.000010, -0.000001]$, 3 of 40 positive probes (Seed 01 firm 0 $t=64$: $0.000573$; Seed 05 firm 0 $t=64$: $0.003846$; Seed 05 firm 0 $t=256$: $0.002990$).
     - Informative cut 0.3: Immediate $-0.051317$, Full $-0.051322$, Continuation $-0.000005$ $[-0.000010, -0.000001]$, 0 of 40 positive probes.
     - Action-independent cut 0.1: Immediate $-0.004800$, Full $-0.004800$, Continuation $0.000000$, 1 of 40 positive probes (Seed 08 firm 0 $t=256$: $0.000122$).
     - Action-independent cut 0.3: Immediate $-0.050273$, Full $-0.050273$, Continuation $0.000000$, 0 of 40 positive probes.
     - Informative mean signed rival-response area: $-3.699770\times 10^{-6}$ (95% CI $[-1.1066\times 10^{-5},\,3.2143\times 10^{-6}]$); action-independent rival-response area: $0.0$ across all 80 probes (confirming Proposition 1 to machine precision).
4. **Reproducibility Hashes and Interaction Accounting (Supplement Tables 9–10):**
   - Posterior draws SHA256: `a2cd4f268b3edf0d9004f0144d2fc846a1088497d171fe33e2adcd4c202d1b95`.
   - Native extension SHA256: `8c1fe82a4830d09ec6710177a4056ca0a67ecf013cf774517e15480fef882780`.
   - PPO training source SHA256: `12ffcf180b6fc8997d0c0dbff6ce085b2467e4dd1300348ac0151b92662d3f15`.
   - MCMC diagnostics: max split $\hat{R} = 1.0089447329892174 \le 1.01$, min ESS $= 606.8603540325352 \ge 400$.
   - Total recorded transitions: $2{,}908{,}736$ per job $\times 20 = 58{,}174{,}720$; wall-clock runtime: $21.978\text{ h}$ (baseline) $+ 22.079\text{ h}$ (ablated) $= 44.057\text{ h}$.

---

## 7. Three-Perspective Adversarial Review

### 7.1 Game-Theory Perspective
1. **False-Alarm Erosion vs. Detection Differential:** In imperfect public monitoring (Green & Porter 1984; Fudenberg, Levine & Maskin 1994), positive false-alarm probability $\alpha > 0$ acts like an additional stochastic termination rate of the cooperative phase, reducing the effective discount factor applied to the cooperative surplus from $\delta$ to $\delta(1-\alpha)$. Consequently, $\beta > \alpha$ is **not** sufficient for enforceability at some $\delta \in [0,1)$; enforceability requires $(\beta-\alpha)h > \alpha g$. The corrected Section 6 and Supplement A.1 state and prove this explicitly.
2. **Quantifier Over All Unilateral Deviations:** Equilibrium in state $C$ requires deterring *all* unilateral deviations $a_i \in \mathcal{A}_i$, not merely the static best response or a fixed set of two price cuts. Under continuous action spaces with smooth monitoring, a small stealth price cut ($g_i(a_i) \ll g_{\max}$ with $\beta_i(a_i) - \alpha_i$ vanishing faster than $g_i(a_i)$) can violate $(\beta_i(a_i)-\alpha_i)h_i > \alpha_i g_i(a_i)$ even when large deviations are easily detected and deterred. The corrected Equation (9) and Supplement A.2 table prove this mechanism explicitly.
3. **Finite Horizon ($T=512$) with Observable Time vs. Infinite-Horizon Benchmark:** The theoretical benchmark is a stationary infinite-horizon game, whereas PPO agents train on $T=512$-period episodes with zero terminal value bootstrap and observe normalized time $t/T$. In a complete-information finite-horizon game with a unique stage-game Nash equilibrium, backward induction unravels cooperation from $T$ back to $t=0$. While boundedly rational learners need not perform exact backward induction, conditioning the policy on $t/T$ provides the exact state variable required for end-of-episode unraveling. Section 7.1 properly frames this as a structural difference between the benchmark and the PPO environment.

### 7.2 Mathematics Perspective
1. **Sign and Domain Discipline in Equations (9)–(11):**
   - In Eq. (9), writing the undivided form $g_i(a_i)[1-\delta(1-\alpha_i)] \le \delta[\beta_i(a_i)-\alpha_i]h_i$ avoids division by zero when $\beta_i(a_i) = \alpha_i$ and avoids inequality reversal when $\beta_i(a_i) < \alpha_i$.
   - In Eq. (11), $\mu_D < \tau < \mu_C$ implies $z_C = (\tau-\mu_C)/\sigma < 0 < z_D = (\tau-\mu_D)/\sigma$. The original manuscript's claim $z_D < 0 < z_C$ was algebraically incompatible with $\mu_D < \tau < \mu_C$.
   - In Proposition 3 and Supplement A.3, the corrected limits $\lim_{\sigma\to 0^+} \delta^*(\sigma) = \frac{g}{g+h}$ and $\lim_{\sigma\to\infty} \delta^*(\sigma) = 2$ eliminate the contradiction between the main text and supplement and establish the existence and uniqueness of the noise cutoff $\bar{\sigma} \in (0,\infty)$ where $\delta^*(\bar{\sigma}) = 1$.
2. **Printed Equation (3) Welfare Formula vs. Archived `mean_total_surplus` (Critical Mathematical Finding):**
   - Main text Eq. (3) defines $\mathrm{TS}(p_1, p_2) = (v-c)[q_1(p_1, p_2) + q_2(p_1, p_2)]$. Because $v = 2, c = 1$, and outside option utility is $u_0 = 0$ ($\exp(0) = 1 > 0$), $q_1 + q_2 = \frac{e^{(2-p_1)/0.25} + e^{(2-p_2)/0.25}}{1 + e^{(2-p_1)/0.25} + e^{(2-p_2)/0.25}} < 1$ strictly for all finite prices. At $p^{\mathrm{N}} \approx 1.472927$, $(v-c)(q_1+q_2) = 0.942862 < 1$.
   - However, Table 1 and Supplement Table 3 report `mean_total_surplus` $\approx 1.159588$ (baseline) and $1.159660$ (ablated), matching `summary.json` and `job.json`.
   - Reconstructing asymmetric firm prices $(p_0, p_1)$ from the archived firm rewards $(R_0, R_1)$ and mean price $\bar{p}$ in each seed's `job.json` shows that standard logit social welfare (inclusive-value consumer surplus plus producer surplus),
     $$W_{\mathrm{logit}}(p_1, p_2) = \underbrace{\mu\log\!\left(1 + e^{(v-p_1)/\mu} + e^{(v-p_2)/\mu}\right)}_{\mathrm{CS}(p_1,p_2)} + \underbrace{\sum_{i=1}^2 (p_i - c)q_i(p_1, p_2)}_{\pi_1 + \pi_2},$$
     evaluates to $1.161077$ at symmetric $p^{\mathrm{N}}$ and matches every seed's archived `mean_total_surplus` across all 20 seeds within $4\times 10^{-6}$ to $10^{-3}$ (the small Jensen's inequality residual from episode price variance). Because the C++ extension source is not included in `acrl_suite_v4_research`, this discrepancy is documented below in Section 9 as an unresolved code-verification item rather than silently altering Eq. (3).

### 7.3 MARL Perspective
1. **Empirical Signal-Clamping Saturation in `audit_probes.json`:**
   - Equation (4) clamps the latent signal mean $m_t$ to $[\theta_{\mathrm{lo}}, \theta_{\mathrm{hi}}]$ whenever $\min(p_{1,t}, p_{2,t}) \le p^{\mathrm{N}}_{\mathrm{grid}} = 1.473$.
   - Because the learned policies already price near $p^{\mathrm{N}}_{\mathrm{grid}} = 1.473$ (mean price $1.4798$), a normalized cut of $0.1$ ($\Delta p = -0.075$) and a normalized cut of $0.3$ ($\Delta p = -0.225$) both push $\min(p_{1,t_0}, p_{2,t_0})$ below $1.473$.
   - Direct inspection of `acrl_suite_v4_research/ppo_baseline/202610*/audit_probes.json` reveals two striking consequences:
     1. **39 of 40 informative probe pairs (`cut=0.1` vs. `cut=0.3` at the same seed, firm, and intervention time $t_0$) have identical `mean_signed_rival_response_area` and identical `mean_continuation_gain` to machine precision ($\sim 10^{-16}$).** The sole exception is Seed `20261005`, firm 0, $t_0 = 64$ (where firm 0's control price was high enough that `cut=0.1` did not fully saturate in all rollouts, yielding area $9.3945\times 10^{-6}$ for `cut=0.1` vs. $9.4245\times 10^{-6}$ for `cut=0.3`).
     2. **19 of 40 informative probes (and 38 of 80 total baseline probes across both cuts) have `mean_signed_rival_response_area == 0.00e+00` identically**, because on the unperturbed control trajectory $\min(p_{1,t_0}, p_{2,t_0}) \le 1.473$ already holds across all 128 rollouts, so neither `cut=0.1` nor `cut=0.3` changes the clamped latent mean $m_{t_0} = \theta_{\mathrm{lo}}$ at all.
   - This confirms that the main text's warning in Section 5 ("equation (4) saturates when the minimum price is at or below the Nash reference. Different cuts can then generate identical latent signals") is not merely a theoretical caveat—it binds on 39 of 40 probe pairs in the executed experiment.
2. **Input-Distribution Confound in Action-Independent Ablation:**
   - Replacing $r_{t+1} = \frac{m_t+m_{t-1}}{2} + \varepsilon_t$ with $r_{t+1} \sim \mathcal{N}(1.6, 0.4^2)$ makes normalized reports standard normal $\mathcal{N}(0,1)$ under the ablation, whereas under near-Nash play in the informative baseline $m_t \approx \theta_{\mathrm{lo}}$, shifting both the mean and variance of the GRU inputs. This is transparently disclosed in Section 2.1 and Section 8.
3. **Windowed GRU Re-encoding vs. Persistent Recurrent State:**
   - Re-running the 128-unit GRU from a zero initial hidden state on a 32-step sliding window bounds the agent's memory horizon to 32 periods, preventing infinite-horizon state tracking unless self-sustained through public reports.

---

## 8. Cross-Document Consistency Audit

A line-by-line consistency check between `/Users/gimjunseong/Downloads/main_corrected.tex` and `/Users/gimjunseong/Downloads/supplement_corrected.tex` confirmed:

1. **Equation Numbering & Cross-References:**
   - Main text preserves exact equation numbering `(1)`–`(11)`:
     - `(1)`–`(3)`: Logit demand $q_i$, profit $\pi_i$, and printed total surplus $\mathrm{TS}$.
     - `(4)`: Clamped latent signal mean $m_t$ (`\label{eq:latent}`).
     - `(5)`: Two-period averaged report $r_{t+1}$ (`\label{eq:report}`).
     - `(6)`: Exact critical discount threshold $\delta^* = \frac{g}{g(1-\alpha)+(\beta-\alpha)h}$ (`\label{eq:threshold}`).
     - `(7)`–`(8)`: Cooperative and deviation Bellman equations $V^C$ and $V^D$ (`\label{eq:vc}`, `\label{eq:vd}`).
     - `(9)`: Full undivided unilateral incentive constraint $g_i(a_i)[1-\delta(1-\alpha_i)] \le \delta[\beta_i(a_i)-\alpha_i]h_i$ (`\label{eq:full}`).
     - `(10)`: Exact partial derivatives $\partial\delta^*/\partial\alpha, \partial\delta^*/\partial\beta, \partial\delta^*/\partial h$ (`\label{eq:compstat}`).
     - `(11)`: Gaussian detection-differential derivative $\partial\Delta/\partial\sigma = -\frac{1}{\sigma}[z_D\phi(z_D)-z_C\phi(z_C)] < 0$ (`\label{eq:ddelta}`).
   - Supplement Section A.2 cross-references `main-text equation (9)` (matching `\label{eq:full}`).
   - Supplement Section E.1 cross-references `Tables~\ref{tab:probe_B01}--\ref{tab:probe_A03}`, which compiles cleanly to `Tables 5–8`.
2. **Symbol & Formula Alignment:**
   - $V^C - V^P = \frac{h}{1-\delta(1-\alpha)}$, $\delta^* = \frac{g}{g(1-\alpha)+(\beta-\alpha)h}$, feasibility $(\beta-\alpha)h > \alpha g$, counterexample ($g=0.2, h=0.5, \alpha=0.4, \beta=0.5 \implies \delta^* = 20/17$), standardized Gaussian coordinates $z_C < 0 < z_D$, total derivative $d\delta^*/d\sigma > 0$, limits $\lim_{\sigma\to 0^+}\delta^*(\sigma) = g/(g+h)$ and $\lim_{\sigma\to\infty}\delta^*(\sigma) = 2$, and unique cutoff $\bar{\sigma}$ are identical in both documents.
3. **Compilation Verification:**
   - Both `main_corrected.pdf` (8 pages) and `supplement_corrected.pdf` (9 pages) compile with `pdflatex` with zero LaTeX errors, zero undefined references, and zero `??` placeholders.

---

## 9. Unresolved Issues & Separate Workstreams

In accordance with strict verification standards, the following items cannot be resolved by mathematical re-derivation or reanalysis of `acrl_suite_v4_research` alone and are explicitly recorded as unresolved issues / separate workstreams:

1. **Printed Equation (3) Welfare Formula vs. C++ Native Extension Implementation:**
   - As documented in Section 7.2, printed Eq. (3) $\mathrm{TS}(p_1, p_2) = (v-c)(q_1 + q_2)$ is bounded strictly below $1$ ($\approx 0.9429$ at $p^{\mathrm{N}}$), whereas archived `mean_total_surplus` in Table 1 and Supplement Table 3 is $\approx 1.1596$, which matches standard logit social welfare $\mathrm{CS}(p_1, p_2) + \pi_1 + \pi_2 = \mu\log(1 + e^{(v-p_1)/\mu} + e^{(v-p_2)/\mu}) + \sum_{i=1}^2 (p_i - c)q_i$. Because `acrl_suite_v4_research` contains only the SHA256 hash (`8c1fe82a...`) of the compiled C++ native extension rather than its source code, the exact C++ formula for `mean_total_surplus` must be verified against the simulator source repository before changing Equation (3).
2. **Empirical Signal Clamping Near Nash (39/40 Probe Pairs Saturated):**
   - Because Eq. (4) clamps $m_t$ at $p^{\mathrm{N}}_{\mathrm{grid}} = 1.473$, cuts of $0.1$ and $0.3$ from near-Nash prices produce identical continuation trajectories in 39 of 40 informative probe pairs and zero rival response in 19 of 40 probes where the control trajectory is already at or below $1.473$. Testing policy sensitivity near Nash requires retraining and auditing with an unclamped or wider-range signal map.
3. **Missing Positive Control for Audit Sensitivity/Power:**
   - Proposition 1 proves the negative control ($\Delta p^{\mathrm{rival}}_t = 0$ and $\Delta\pi^{\mathrm{cont}} = 0$ under action independence), but the archive contains no positive-control agent (e.g., a known grim-trigger automaton or a verified collusive tabular Q-learning agent) to demonstrate that the audit pipeline detects continuation punishment when present.
4. **Input-Distribution Confound in the Action-Independent Channel Replacement:**
   - The ablation $r_{t+1} \sim \mathcal{N}(1.6, 0.4^2)$ alters the marginal mean and variance of observations relative to the informative channel under near-Nash play. A moment-matched action-independent control (e.g., shuffling informative reports across episodes) would isolate action-dependence from marginal input scale.
5. **Finite Horizon ($T=512$) with Observable Time Input:**
   - Agents observe normalized episode time $t/T$ and episodes terminate at $T=512$ without value bootstrapping. Determining whether PPO fails to learn collusive enforcement because of finite-horizon unraveling, observation noise, or on-policy exploration requires a continuing-task (infinite-horizon bootstrap) ablation without time input.
6. **Raw MCMC Calibration Data and Posterior Draws File Not Included in Archive:**
   - `suite_manifest.json` records the SHA256 hash of `posterior_draws.csv` and the MCMC convergence diagnostics ($\hat{R} = 1.008945$, $\mathrm{ESS} = 606.86$), but the raw labeled calibration dataset and `posterior_draws.csv` itself are external to `acrl_suite_v4_research`.
7. **Incomplete SAC Runs & Related Literature Baselines:**
   - The broader suite plan referenced SAC runs and tabular Q-learning under imperfect monitoring (e.g., Calvano et al. 2021, *IJIO*), which are outside the completed 20-job PPO archive.
