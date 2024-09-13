There are two codes in this repositories, one is the Social Architecture Model's code. (https://arxiv.org/pdf/cond-mat/0401053)  It is an implementation of Ian Wright's paper. It was used w.r.t to test some emperical data in India. The other one is the game theoretic model for healthcare systems in India, it's incomplete mostly, but was used for more emeprical work. Some of the parameters and modelling are below 
Patient Utility Function: $$U_{\theta} = B(q) - \beta_{\theta}P$$
Healthcare Provider Utility Function: $$U_{HCP} = E[\pi] = [p \cdot I_H + (1 - p) \cdot I_L] \cdot (P - C(q))$$
Probability of Patient Types:
$$P(H) = p$$
$$P(L) = 1 - p$$
Regulation Constraints:

$$q \geq q_{min}$$
$$P \leq P_{max}$$
Subsidy for Low-Income Patients:

$$P_{effective} = P - S \quad \text{(for low-income patients)}$$

Where:
- $B(q)$ is the benefit from care of quality $q$
- $\beta_{\theta}$ is the price sensitivity for patient type $\theta$
- $P$ is the price set by the healthcare provider
- $C(q)$ is the cost of providing care of quality $q$
- $I_H$ and $I_L$ are indicators if high-income or low-income patients accept care
- $S$ is the subsidy amount for low-income patients
