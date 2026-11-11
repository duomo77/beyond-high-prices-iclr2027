# P1 — Correct the Theoretical Benchmark and Its Proofs

**Paper:** *Beyond High Prices: Auditing Information-Mediated Enforcement in Recurrent Pricing Agents*  
**Target:** ICLR 2027 reviewer response, revised main manuscript, and revised supplementary material  
**Scope:** Theoretical correctness (Propositions 2–3; main-text Eqs. (6)–(11); Supplementary §§A.1–A.3).  
**Status:** Mathematically checked replacement text; **not** a claim that the submitted paper, code, or OpenReview response has already been revised.  
**Priority:** P0 / blocking correctness issue.

---

## 1. Objective and reviewer-facing diagnosis

Two reviewers identified the same substantive issue in Proposition 2, and Reviewer `qamv` independently noted it: the calculation of the cooperative–punishment continuation-value difference omits the false-alarm probability. The omission propagates into the incentive threshold, the condition for a feasible discount factor, the full-deviation discussion, and the Gaussian-noise comparative statics.

We should **acknowledge the mathematical error without qualification**, replace the derivation in both the main text and supplement, and carefully distinguish the consequences for the fixed-trigger analytical benchmark from the separately executed PPO simulations.

### Exact correction map

| Location in submitted paper | Existing problem | Required action |
|---|---|---|
| Main §6, Proposition 2 / Eq. (6) | Incorrect threshold denominator | Replace proposition, condition, and proof |
| Main §6, Eqs. (7)–(8) | Bellman equations correct; the subsequent subtraction is not | Retain the equations; replace the value-difference calculation |
| Main §6, Eq. (9) | Inherits incorrect threshold and can obscure the hardest-to-deter action | State an inequality for **every** unilateral action |
| Main §6, Eq. (10) | Sign conclusions correct but derived from an incorrect expression | Re-derive from the corrected threshold |
| Main §7, Proposition 3 / Eq. (11) | Eq. (11) is correct; the sign of standardized Gaussian variables is reversed in its proof | Correct the sign argument, threshold derivative, and limits |
| Supplementary A.1 | Repeats the omitted false-alarm term | Replace the entire proof and feasibility statement |
| Supplementary A.2 | Numerical thresholds do not follow from the printed formula; false-alarm probability unspecified | Replace with a fully specified, verified example |
| Supplementary A.3 | Incorrect zero-noise limit and inconsistency with the printed threshold | Replace derivative and both limits |
| Main §7.1 | Fixed infinite-horizon trigger theory differs from finite-horizon recurrent PPO | Clarify the restricted interpretation; do **not** claim a theorem for PPO |

**Out of scope for this P1 file:** The welfare-definition mismatch (Eq. (3)), positive controls, moment-matched signal ablation, related-work coverage, and architecture justification. Those are distinct review-response workstreams, not issues cured by the proof correction.

---

## 2. Assumptions and notation (must be explicit)

Consider a discounted, stationary repeated stage game with two public states:

- **C (cooperation):** both firms use a fixed prescribed action profile.
- **P (punishment):** an absorbing public state prescribing a credible stage-game Nash action profile.
- A bad public signal transitions the automaton from **C** to **P**; otherwise it stays in **C**.
- Payoffs are bounded; the discount factor is \(\delta\in[0,1)\).
- A **specified one-period unilateral deviation** is followed by adherence to the prescribed automaton.

For one firm, define

\[
\begin{aligned}
\pi^C&=\text{current prescribed cooperative payoff},\\
\pi^P&=\text{per-period payoff in absorbing punishment},\\
\pi^D&=\text{current payoff from the specified deviation},\\
g&=\pi^D-\pi^C>0,\\
h&=\pi^C-\pi^P>0,\\
\alpha&=\Pr(\text{bad signal}\mid\text{compliance}),\\
\beta&=\Pr(\text{bad signal}\mid\text{specified deviation}),\\
\Delta&=\beta-\alpha.
\end{aligned}
\]

For the scalar discount-threshold corollary assume \(0\leq\alpha<\beta\leq1\), so \(\Delta>0\). When considering **all** actions, do not assume each action necessarily yields \(g>0\) or \(\Delta>0\); retain an undivided incentive inequality instead.

**Important distinction:** The benchmark uses a **fixed infinite-horizon public trigger automaton**. The empirical PPO environment uses **512-period episodes**, time as an actor input, delayed continuous signals, and frozen deterministic deployment in the audit. The benchmark is not a characterization of learned PPO equilibria.

---

## 3. Mathematical correction: the continuation-value gap

The submitted Bellman equations are correct:

\[
V^C=\pi^C+\delta\big[(1-\alpha)V^C+\alpha V^P\big],
\tag{B1}
\]

\[
V^P=\pi^P+\delta V^P.
\tag{B2}
\]

Subtract (B2) from (B1) **without dropping the false-alarm transition**:

\[
\begin{aligned}
V^C-V^P
&=\pi^C-\pi^P
+\delta\big[(1-\alpha)V^C+\alpha V^P-V^P\big]\\
&=h+\delta(1-\alpha)(V^C-V^P).
\end{aligned}
\]

Hence

\[
\boxed{V^C-V^P=\frac{h}{1-\delta(1-\alpha)}}.
\tag{C1}
\]

The submitted manuscript and Supplementary A.1 instead use \(h/(1-\delta)\), which is **only valid when \(\alpha=0\)** in this model. The error concerns how mistaken punishment shortens the expected duration of cooperation.

---

## 4. Replacement main-text Proposition 2 and proof (ready to adapt)

> **Proposition 2 (Incentive threshold with false alarms).**  
> Consider the stationary repeated game with a cooperative public state \(C\) and an absorbing, credible punishment state \(P\). Suppose a specified one-period unilateral deviation yields a current payoff gain \(g=\pi^D-\pi^C>0\), and the cooperative–punishment per-period payoff gap is \(h=\pi^C-\pi^P>0\). Let \(\alpha\) and \(\beta\) be the probabilities of a bad public signal following compliance and this deviation, respectively, with \(0\leq\alpha<\beta\leq1\). For \(\delta\in[0,1)\), the deviation is unprofitable if and only if
>
> \[
> \boxed{\delta\geq\delta^* \equiv
> \frac{g}{g(1-\alpha)+(\beta-\alpha)h}}.
> \tag{6, corrected}
> \]
>
> A discount factor **strictly below one** deterring the specified deviation exists if and only if
>
> \[
> \boxed{(\beta-\alpha)h>\alpha g}.
> \tag{F}
> \]
>
> **Proof.** Under the fixed public trigger, cooperative and punishment values solve
>
> \[
> V^C=\pi^C+\delta[(1-\alpha)V^C+\alpha V^P],\qquad
> V^P=\pi^P+\delta V^P.
> \]
>
> Subtraction gives \(V^C-V^P=h/[1-\delta(1-\alpha)]\). The one-period deviation has value
>
> \[
> V^D=\pi^D+\delta[(1-\beta)V^C+\beta V^P].
> \]
>
> Consequently,
>
> \[
> \begin{aligned}
> V^D-V^C
> &=g-\delta(\beta-\alpha)(V^C-V^P)\\
> &=g-\frac{\delta(\beta-\alpha)h}{1-\delta(1-\alpha)}.
> \end{aligned}
> \]
>
> Since \(1-\delta(1-\alpha)>0\), the inequality \(V^D\leq V^C\) is equivalent to
>
> \[
> g[1-\delta(1-\alpha)]\leq\delta(\beta-\alpha)h,
> \]
>
> or, under the stated positive-gain and detection assumptions,
>
> \[
> \delta\geq\frac{g}{g(1-\alpha)+(\beta-\alpha)h}.
> \]
>
> This threshold is strictly less than one if and only if \((\beta-\alpha)h>\alpha g\). \(\square\)

### Interpretation to retain

- Deterrence depends on the one-period gain \(g\), the **incremental** detection probability \(\beta-\alpha\), and the endogenous continuation-value gap \(V^C-V^P\).
- False alarms do **two** things: they alter the probability differential and erode the continuation value of cooperation.
- \(\beta>\alpha\) is **necessary but not sufficient** for a feasible \(\delta<1\) when \(g>0\), \(h>0\), and \(\alpha>0\).
- The proposition only tests **one specified unilateral deviation** in the cooperative state. It is not a sufficient equilibrium certificate across continuous actions and all public histories.

### Why the correction matters in direction, not merely magnitude

Define the printed and corrected formulas under \(g>0\), \(h>0\), \(\Delta>0\):

\[
\delta^*_{\mathrm{printed}}=\frac{g}{g+\Delta h},\qquad
\delta^*_{\mathrm{corrected}}=\frac{g}{g(1-\alpha)+\Delta h}.
\]

Their difference is

\[
\boxed{
\delta^*_{\mathrm{corrected}}-\delta^*_{\mathrm{printed}}
=\frac{\alpha g^2}{(g+\Delta h)[g(1-\alpha)+\Delta h]}
\geq0.}
\tag{D}
\]

For \(\alpha>0\), the corrected threshold is **strictly higher**: false alarms make enforcement harder, not easier. One reviewer describes the threshold as becoming lower after correction; acknowledge the substantive error while stating the mathematical direction precisely and respectfully. The two thresholds coincide for \(\alpha=0\); **\(\alpha=0\) alone does not require \(\beta=1\)**.

---

## 5. Counterexample that demonstrates materiality

Choose mathematically admissible illustrative values

\[
g=0.2,\qquad h=0.5,\qquad\alpha=0.4,\qquad\beta=0.5,
\]

so \(\Delta=0.1\). Then

\[
\delta^*_{\mathrm{printed}}=\frac{0.2}{0.2+0.1(0.5)}=0.8,
\]

but

\[
\delta^*_{\mathrm{corrected}}
=\frac{0.2}{0.2(0.6)+0.1(0.5)}
=\frac{0.2}{0.17}\approx1.17647.
\]

Thus the printed criterion would classify \(\delta=0.9\) as sufficient, while the true model does not permit the deviation to be deterred at any \(\delta<1\). Directly, at \(\delta=0.9\),

\[
V^D-V^C
=0.2-\frac{0.9(0.1)(0.5)}{1-0.9(0.6)}
\approx0.10217>0.
\]

This is a **counterexample for the paper's printed formula**, not an estimate from the PPO experiments.

---

## 6. Replacement for the full incentive-compatibility discussion (main Eq. (9))

For each firm \(i\) and each unilateral action \(a_i\) in its continuous action set, define

\[
\begin{aligned}
g_i(a_i)&=\pi_i(a_i,a_{-i}^C)-\pi_i^C,\\
\beta_i(a_i)&=\Pr(\text{bad public signal}\mid a_i,a_{-i}^C),\\
\alpha_i&=\Pr(\text{bad public signal}\mid a_i^C,a_{-i}^C),\\
h_i&=\pi_i^C-\pi_i^P.
\end{aligned}
\]

The correct one-period deviation condition is

\[
\boxed{
 g_i(a_i)[1-\delta(1-\alpha_i)]
 \leq\delta[\beta_i(a_i)-\alpha_i]h_i
\quad\text{for every }i\text{ and }a_i.}
\tag{9, corrected}
\]

**Why use the undivided form?** It remains valid when a deviation has a negative immediate gain or a negative incremental detection probability. Such deviations cannot automatically be discarded: an action that sacrifices current profit but reduces future punishment risk may still be attractive. Testing only the action with the largest immediate gain is insufficient.

For the restricted set of actions with \(g_i(a_i)>0\) and \(\beta_i(a_i)>\alpha_i\), a convenient necessary threshold is

\[
\delta\geq
\sup_{i,a_i:\,g_i(a_i)>0,\,\beta_i(a_i)>\alpha_i}
\frac{g_i(a_i)}{g_i(a_i)(1-\alpha_i)+[\beta_i(a_i)-\alpha_i]h_i}.
\]

This restricted supremum **does not replace** the all-actions condition above. Where \(g_i(a_i)>0\) but \(\beta_i(a_i)\leq\alpha_i\), deterrence is impossible within this positive-payoff-gap trigger model. Credibility of punishment and deviations after all relevant public histories must also be checked before claiming a public equilibrium.

**Recommended replacement sentence:**

> The largest current-gain deviation need not be the hardest to deter because its detectability may differ from that of less profitable actions. Accordingly, the cooperative state's incentive-compatibility condition must be verified for every unilateral action, rather than only for a finite family of price-cut probes. Our audits provide finite behavioral diagnostics and do not certify this global condition.

---

## 7. Corrected comparative statics (main Eq. (10))

Let

\[
D=g(1-\alpha)+(\beta-\alpha)h,\qquad
\delta^*=\frac{g}{D},
\]

with \(g,h>0\) and \(\beta>\alpha\). Holding the other primitive quantities fixed,

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
\tag{10, corrected derivation}
\]

The **signs** printed in the paper remain correct; the algebraic foundation and derivative magnitudes must be replaced.

---

## 8. Replacement main-text Proposition 3: Gaussian monitoring

> **Proposition 3 (Restricted Gaussian-noise comparative statics).**  
> Maintain the assumptions of Proposition 2. Suppose that, conditional on compliance or a specified one-period deviation, the public monitoring statistic is Gaussian with a common standard deviation \(\sigma>0\), respective means \(\mu_C\) and \(\mu_D\), and a fixed bad-signal threshold \(\tau\) satisfying \(\mu_D<\tau<\mu_C\). Hold the means, threshold, prescribed actions, current gains, and punishment payoff gap fixed. Then the corrected algebraic incentive threshold \(\delta^*(\sigma)\) is strictly increasing in \(\sigma\).
>
> **Proof.** Let \(\Phi\) and \(\phi\) denote the standard normal CDF and PDF and set
>
> \[
> z_C=\frac{\tau-\mu_C}{\sigma}<0,\qquad
> z_D=\frac{\tau-\mu_D}{\sigma}>0.
> \]
>
> The false-alarm and detection probabilities are
>
> \[
> \alpha(\sigma)=\Phi(z_C),\qquad
> \beta(\sigma)=\Phi(z_D).
> \]
>
> The Gaussian identities give
>
> \[
> \alpha'(\sigma)=-\frac{z_C\phi(z_C)}{\sigma}>0,
> \qquad
> \beta'(\sigma)=-\frac{z_D\phi(z_D)}{\sigma}<0.
> \]
>
> Equivalently, with \(\Delta=\beta-\alpha\),
>
> \[
> \boxed{\Delta'(\sigma)
> =-\frac{z_D\phi(z_D)-z_C\phi(z_C)}{\sigma}<0.}
> \tag{11, corrected sign explanation}
> \]
>
> Write
>
> \[
> D(\sigma)=g[1-\alpha(\sigma)]
> +[\beta(\sigma)-\alpha(\sigma)]h.
> \]
>
> Since \(D>0\), differentiation yields
>
> \[
> \boxed{
> \frac{d\delta^*}{d\sigma}
> =\frac{g}{D(\sigma)^2}
> \left[(g+h)\alpha'(\sigma)-h\beta'(\sigma)\right]>0.}
> \]
>
> As \(\sigma\to0^+\), we have \(\alpha\to0\), \(\beta\to1\), and
>
> \[
> \boxed{\delta^*(\sigma)\to\frac{g}{g+h}.}
> \]
>
> As \(\sigma\to\infty\), we have \(\alpha,\beta\to\tfrac12\), and
>
> \[
> \boxed{\delta^*(\sigma)\to2.}
> \]
>
> Thus sufficiently noisy monitoring eventually makes the specified trigger deterrence condition infeasible for every \(\delta<1\). \(\square\)

### Corrections to the submitted explanation

1. **Keep the derivative formula** for \(\Delta'(\sigma)\); correct the sign assertion to \(z_D>0>z_C\).
2. Supplementary A.3's statement \(\lim_{\sigma\to0}\delta^*=0\) is **incorrect** for fixed \(g>0\); the correct limit is \(g/(g+h)\).
3. Under the **printed erroneous threshold**, the infinite-noise limit would be \(1\), not \(2\). The limit \(2\) is correct **for the repaired threshold**.
4. This is a comparative static for the **specified fixed trigger**, not an empirical conclusion that retrained PPO prices rise or fall monotonically with monitoring noise.
5. If an independent additional Gaussian noise of standard deviation \(\sigma_a\) is introduced with base standard deviation \(\sigma_0>0\), then \(\sigma_{\rm tot}=\sqrt{\sigma_0^2+\sigma_a^2}\), so

\[
\frac{d\delta^*}{d\sigma_a}
=\frac{d\delta^*}{d\sigma_{\rm tot}}
\frac{\sigma_a}{\sigma_{\rm tot}}.
\]

The derivative equals zero **at** \(\sigma_a=0\) and is strictly positive for \(\sigma_a>0\), under the proposition's fixed-primitive assumptions.

---

## 9. Replacement text for Supplementary A.1–A.3

### A.1 — Value difference and discount threshold (replace entire current subsection)

> The two-state automaton has a cooperative state \(C\) and an absorbing, credible punishment state \(P\). Let \(g=\pi^D-\pi^C>0\) and \(h=\pi^C-\pi^P>0\). Bad-signal probabilities after compliance and the specified one-period deviation are \(\alpha\) and \(\beta\), with \(0\leq\alpha<\beta\leq1\). All values are evaluated before the current action. The Bellman equations imply
>
> \[
> V^C=\pi^C+\delta[(1-\alpha)V^C+\alpha V^P],\qquad
> V^P=\pi^P+\delta V^P,
> \]
>
> hence \(V^C-V^P=h/[1-\delta(1-\alpha)]\), not \(h/(1-\delta)\). For a one-period deviation followed by the prescribed strategy,
>
> \[
> V^D-V^C=g-\frac{\delta(\beta-\alpha)h}{1-\delta(1-\alpha)}.
> \]
>
> Consequently, deterrence is equivalent to
>
> \[
> \delta\geq\frac{g}{g(1-\alpha)+(\beta-\alpha)h}.
> \]
>
> A feasible \(\delta<1\) exists precisely when \((\beta-\alpha)h>\alpha g\). The inequality must be assessed for each relevant unilateral action; the proposition itself concerns one specified deviation.

### A.2 — Why the quantifier matters (replace illustrative example)

> To illustrate why the largest immediate gain need not be the hardest deviation to deter, let the cooperative–punishment payoff gap be \(h=1\) and the compliant false-alarm probability be \(\alpha=0.05\). Consider deviations A and B:
>
> | Deviation | Immediate gain \(g\) | Incremental bad-signal probability \(\beta-\alpha\) | Correct \(\delta^*\) |
> |---|---:|---:|---:|
> | A | 0.30 | 0.50 | \(0.30/[0.30(0.95)+0.50]=0.382166\) |
> | B | 0.90 | 0.01 | \(0.90/[0.90(0.95)+0.01]=1.040462\) |
>
> At \(\delta=0.90\), A is deterred and B is not. This example is purely algebraic and is not a measurement from the PPO agents. It illustrates that current gain and detectability must be evaluated jointly for each unilateral action. In particular, B cannot be deterred by the specified trigger for any admissible \(\delta<1\).

### A.3 — Gaussian noise and its boundaries (replace incorrect paragraph)

> Suppose \(\mu_D<\tau<\mu_C\) and let \(z_D=(\tau-\mu_D)/\sigma>0\), \(z_C=(\tau-\mu_C)/\sigma<0\). Then \(\alpha=\Phi(z_C)\), \(\beta=\Phi(z_D)\), and
>
> \[
> \frac{d(\beta-\alpha)}{d\sigma}
> =-\frac{z_D\phi(z_D)-z_C\phi(z_C)}{\sigma}<0.
> \]
>
> Using the **corrected** discount threshold gives
>
> \[
> \frac{d\delta^*}{d\sigma}
> =\frac{g[(g+h)\alpha'(\sigma)-h\beta'(\sigma)]}
> {[g(1-\alpha(\sigma))+(\beta(\sigma)-\alpha(\sigma))h]^2}>0.
> \]
>
> The limiting thresholds are \(g/(g+h)\) as \(\sigma\to0^+\) and \(2\) as \(\sigma\to\infty\). The result concerns a fixed trigger threshold and fixed payoff primitives; it does not establish comparative statics for policies retrained by PPO. For independently added Gaussian noise of standard deviation \(\sigma_a\), the chain-rule derivative at \(\sigma_a=0\) is zero when baseline noise is positive.

---

## 10. Reviewer response — concise English draft for the theoretical error

**Use only after the corrected text has actually been incorporated into the revised submission; otherwise replace completion claims with explicit proposed revisions.**

> **Response to the concern about Proposition 2.** We thank the reviewers for identifying an error in the continuation-value calculation. We agree that our original derivation omitted the false-alarm transition probability. In the specified absorbing-punishment automaton, the correct Bellman equations yield
>
> \[
> V^C-V^P=\frac{\pi^C-\pi^P}{1-\delta(1-\alpha)}.
> \]
>
> For a one-period deviation with current gain \(g>0\), incremental detection probability \(\beta-\alpha>0\), and cooperative–punishment payoff gap \(h>0\), the incentive condition becomes
>
> \[
> \delta\geq\frac{g}{g(1-\alpha)+(\beta-\alpha)h}.
> \]
>
> The correct condition for an admissible deterrence threshold below one is \((\beta-\alpha)h>\alpha g\). We will replace the proof and update the full-deviation discussion and Gaussian comparative statics consistently in the main text and supplementary material. The correction makes the deterrence requirement **more demanding** when false alarms occur. The benchmark remains conditional on a fixed public trigger strategy; it does not establish that learned PPO policies implement that strategy. We apologize for the error and appreciate the reviewers' careful reading.

### If responding to the reviewer's threshold-direction comment

Do not make the direction discrepancy the centerpiece of the rebuttal. If relevant, state neutrally:

> Under the original model assumptions, the corrected discount threshold is weakly higher than the printed one (strictly so for \(\alpha>0\)), because the correct denominator is smaller by \(\alpha g\). Thus the correction strengthens rather than relaxes the patience requirement.

### Claims **not** to make

- “This was only a typographical mistake.” It is a consequential algebraic mistake.
- “The corrected theory validates PPO enforcement.” It does not.
- “Fixing Proposition 2 resolves the reviewers' soundness concerns.” The welfare inconsistency, unvalidated audit sensitivity, confounded signal ablation, and algorithm choice remain.
- “The reviewers have been answered experimentally.” The mathematical derivation and PPO evidence are distinct.

---

## 11. Independent verification: small exact numerical checks

The following Python snippet checks the algebraic counterexample, the corrected Supplementary A.2 example, and the sign of the threshold difference.

```python
from math import isclose

def old_threshold(g, alpha, beta, h):
    return g / (g + (beta - alpha) * h)

def corrected_threshold(g, alpha, beta, h):
    assert g > 0 and h > 0 and 0 <= alpha < beta <= 1
    return g / (g * (1 - alpha) + (beta - alpha) * h)

# Main counterexample
g, h, alpha, beta = 0.2, 0.5, 0.4, 0.5
old = old_threshold(g, alpha, beta, h)
new = corrected_threshold(g, alpha, beta, h)
assert isclose(old, 0.8, abs_tol=1e-12)
assert isclose(new, 1.176470588235294, abs_tol=1e-12)
assert new > old

delta = 0.9
net_deviation_gain = g - delta * (beta - alpha) * h / (1 - delta * (1 - alpha))
assert net_deviation_gain > 0

# Revised Supplementary A.2 example
alpha, h = 0.05, 1.0
A = corrected_threshold(0.3, alpha, 0.55, h)
B = corrected_threshold(0.9, alpha, 0.06, h)
assert isclose(A, 0.3821656050955414, abs_tol=1e-12)
assert isclose(B, 1.0404624277456649, abs_tol=1e-12)
assert A < 0.9 < B

print("All numerical checks passed.")
```

### Additional verification required before submitting a revised PDF

- [ ] Run a symbolic algebra check of the Bellman solution against the proposed threshold.
- [ ] Recompile the main PDF and supplement; search for the **obsolete** expression `g + (beta-alpha) h` without the `g(1-alpha)` factor in threshold denominators.
- [ ] Search the entire manuscript for the obsolete claim that `beta > alpha` **alone** guarantees feasible deterrence.
- [ ] Verify the sign statements `z_D > 0 > z_C` and both noise limits.
- [ ] Confirm that every equation reference and proposition number matches the final LaTeX build.
- [ ] Retain archived PPO experiment results unchanged unless an actual dependency of the implementation on the theoretical threshold is found.
- [ ] Treat welfare, positive-control, and signal-ablation corrections as separate mandatory workstreams.

---

## 12. Scope note: what the correction does and does not establish

**Established by the corrected mathematics:** For the specified stationary, infinite-horizon, two-state public trigger with absorbing credible punishment and a particular one-shot unilateral deviation, the exact deterrence condition includes false-alarm risk through the cooperative continuation value. Fixed-threshold Gaussian monitoring becomes less capable of deterring that deviation as its standard deviation increases, holding the stated primitives fixed.

**Not established:** That recurrent PPO has learned this trigger; that no other collusive mechanism is possible; that near-Nash average prices prove equilibrium; that finite price-cut probes certify all unilateral incentive constraints; or that action-independent channel replacement identifies a pure information effect. Those questions require separate modeling assumptions or experiments.

**Suggested commit message:** `fix(theory): correct false-alarm continuation values and Gaussian incentive thresholds`

**Working reference documents:** The submitted main manuscript (pp. 5–7), submitted Supplementary Material (pp. 1–2), and the three reviewer reports supplied in the conversation. This document is a **proposed correction package**, not an account of already-executed modifications to the submitted materials.
