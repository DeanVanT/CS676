# Private Equity Valuation

# 1. Foundations of Option Theory

## 1.1 What an Option Is

**Call Option Payoff:**
$$\text{Payoff} = \max(S_T - K, 0)$$

**Put Option Payoff:**
$$\text{Payoff} = \max(K - S_T, 0)$$

Where $S_T$ is stock price at expiration, $K$ is strike price.

* Definitions: call, put
* Payoff structure
* European vs American

## 1.2 Risk-Neutral Framework

**Risk-Neutral Pricing Formula:**
$$V_0 = e^{-rT} \mathbb{E}^Q[\text{Payoff}]$$

Where $\mathbb{E}^Q$ is expectation under risk-neutral measure $Q$.

* Risk-neutral measure (RN)
* Expected discounted payoff
* Why real-world drift doesn't matter for pricing

## 1.3 Forward Prices & No-Arbitrage

**Forward Price Formula:**
$$F = S_0 e^{(r-q)T}$$

**Present Value of Forward:**
$$PV = e^{-rT}(F - K)$$

Where $q$ is dividend yield, $r$ is risk-free rate.

* Forward price formula
* Discounting logic

## 1.4 Probability Distributions

**Normal Distribution PDF:**
$$f(x) = \frac{1}{\sqrt{2\pi\sigma^2}} e^{-\frac{(x-\mu)^2}{2\sigma^2}}$$

**Lognormal Distribution (Stock Prices):**
$$S_T = S_0 e^{(\mu - \frac{\sigma^2}{2})T + \sigma\sqrt{T}Z}$$

Where $Z \sim N(0,1)$ is standard normal.

* Normal distribution
* Lognormal distribution  
* Volatility as annualized standard deviation

---

# 2. Black–Scholes (B&S) Core

## 2.1 Geometric Brownian Motion (GBM)

### **Black–Scholes Core Formulas**

**Call Option (European):**
$$C = S_0 \cdot N(d_1) - K \cdot e^{-rT} \cdot N(d_2)$$

**Put Option (European):**
$$P = K \cdot e^{-rT} \cdot N(-d_2) - S_0 \cdot N(-d_1)$$

**Where:**
$$d_1 = \frac{\ln(S_0/K) + (r + \frac{1}{2}\sigma^2)T}{\sigma\sqrt{T}}$$

$$d_2 = d_1 - \sigma\sqrt{T}$$

**With Dividend Yield (q) Adjustment:**
$$C = S_0 \cdot e^{-qT} \cdot N(d_1) - K \cdot e^{-rT} \cdot N(d_2)$$

**Geometric Brownian Motion (GBM)**
* GBM intuition
* Price path properties

## 2.2 SDE (Stochastic Differential Equation) View (light)

**Geometric Brownian Motion SDE:**
$$dS = \mu S dt + \sigma S dW$$

Where $\mu$ is drift, $\sigma$ is volatility, $dW$ is Wiener process.

* Structure of an SDE

## 2.3 PDE (Partial Differential Equation) Intuition Only

**Black-Scholes PDE:**
$$\frac{\partial V}{\partial t} + \frac{1}{2}\sigma^2 S^2 \frac{\partial^2 V}{\partial S^2} + rS\frac{\partial V}{\partial S} - rV = 0$$

* What a PDE is
* Why the Black–Scholes PDE exists
* Why you don't need the math to *use* Black–Scholes

## 2.4 The Black–Scholes Formula

**Greeks:**

**Delta (Price Sensitivity):**
$$\Delta = \frac{\partial V}{\partial S} = N(d_1) \text{ (for calls)}$$

**Gamma (Delta Sensitivity):**
$$\Gamma = \frac{\partial^2 V}{\partial S^2} = \frac{n(d_1)}{S_0\sigma\sqrt{T}}$$

**Vega (Volatility Sensitivity):**
$$\nu = \frac{\partial V}{\partial \sigma} = S_0 n(d_1) \sqrt{T}$$

**Theta (Time Decay):**
$$\Theta = \frac{\partial V}{\partial T}$$

Where $n(x)$ is standard normal PDF.

* d1, d2 definitions
* Call and put formulas
* Risk-free rate (r)
* Time to expiry (T)
* Volatility (σ)
* Normal CDF (N(d1), N(d2))

## 2.5 Greeks (Optional but helpful)

* Delta, Gamma, Vega
* Why auditors sometimes reference them

---

# 3. Structural Credit / Merton Model (Conceptual)

## 3.1 Firm Value As Underlying Asset

**Merton Model Setup:**
$$V_A = D + E$$

Where $V_A$ is asset value, $D$ is debt, $E$ is equity value.

* Assets = underlying S
* Debt = strike K

## 3.2 Equity as a Call Option on Assets

**Equity Value Formula:**
$$E = V_A N(d_1) - De^{-rT}N(d_2)$$

**Where:**
$$d_1 = \frac{\ln(V_A/D) + (r + \frac{\sigma_A^2}{2})T}{\sigma_A\sqrt{T}}$$

* Merton insight
* Implications for leverage

## 3.3 Asset Vol vs Equity Vol

**Volatility Relationship:**
$$\sigma_E = \frac{V_A}{E} \cdot N(d_1) \cdot \sigma_A$$

Where $\sigma_A$ is asset volatility, $\sigma_E$ is equity volatility.

* Relationship between σ_V and σ_E
* High-level mapping

---

# 4. Option Pricing Method (OPM)

## 4.1 Purpose of OPM

**OPM Core Concept:**
$$\text{Security Value} = \sum_{i} \text{Option Slice}_i$$

Where each slice represents rights between breakpoints.

* Allocating value across share classes
* When OPM is appropriate

## 4.2 Breakpoints (Core of OPM)

**Breakpoint Calculation:**
$$BP_i = \sum_{j=1}^{i} \text{Senior Claims}_j$$

* What breakpoints represent
* Debt repayment levels
* Liquidation preferences (LP)
* Participation caps
* Conversion triggers
* Warrant/option strikes

## 4.3 Slicing the Capital Structure

**Option Slice Value:**
$$\text{Slice}_i = BS_{call}(S_0, BP_i, T, r, \sigma) - BS_{call}(S_0, BP_{i-1}, T, r, \sigma)$$

* Breakpoints define economic regions
* Each region = an option interval

## 4.4 Applying Black–Scholes to Each Slice

**Incremental Call Value:**
$$\Delta C_i = C(K_{i-1}) - C(K_i)$$

Where $K_i$ are strikes (breakpoints) in ascending order.

* Underlying = TIC or equity value
* Strike = breakpoint
* Value = BS call on upside

## 4.5 Allocating Incremental Option Value

**Class Allocation Formula:**
$$\text{Class Value} = \sum_{i} \Delta C_i \times \text{Allocation Ratio}_{i,class}$$

* Per-class rights
* Participation rules
* Conversion rules
* Adjusting for dividends (PIK)

## 4.6 Per-Share Value Computation

**Price Per Share:**
$$PPS_{class} = \frac{\text{Total Class Value}}{\text{Shares Outstanding}_{class}}$$

* Total value per class
* Divide by class shares
* Class PPS (price per share)

## 4.7 OPM vs Other Methods

**Method Comparison:**
- **OPM:** Uses option theory for complex securities
- **CVM:** Simple waterfall with current value
- **PWERM:** Probability-weighted scenarios
- **CSE:** Treats everything as common stock

* OPM vs CVM (Current Value Method)
* OMP vs CSE (Common Stock Equivalent)
* OPM vs PWERM (Probability Weighted Expected Return Method)

---

# 5. PWERM (Probability Weighted Expected Return Method)

## 5.1 Purpose and Use Cases

**PWERM Formula:**
$$E[V] = \sum_{i=1}^n p_i \cdot \frac{V_i}{(1+r_i)^{t_i}}$$

Where $p_i$ is probability, $V_i$ is scenario value, $r_i$ is discount rate, $t_i$ is time.

* Scenario-based valuation
* When future exit paths differ dramatically

## 5.2 Scenario Specification

**Present Value per Scenario:**
$$PV_i = \frac{\text{Exit Value}_i}{(1 + \text{Discount Rate}_i)^{\text{Time}_i}}$$

* Exit equity value
* Timing
* Probability
* Discount rate

## 5.3 Allocating Within Each Scenario

**Waterfall Allocation:**
$$\text{Class Payment} = \min(\text{Class Claim}, \text{Available Proceeds})$$

Applied sequentially by seniority.

* Waterfall
* CSE pre-conversion
* CSE post-conversion

## 5.4 Present Value and Weighted Results

**Final PWERM Value:**
$$\text{PWERM PPS} = \frac{\sum_{i} p_i \cdot PV_i \cdot \text{Class Shares}_i}{\text{Total Shares Outstanding}}$$

* Per-scenario PPS
* Weighting
* Comparing to OPM

---

# 6. CVM (Current Value Method)

## 6.1 What CVM Is

**CVM Waterfall:**
$$\text{Proceeds} = \text{Current Equity Value}$$
$$\text{Distribution} = \text{Apply Waterfall}(\text{Proceeds})$$

* Straight waterfall using today's equity value

## 6.2 When To Use CVM

**CVM Application Criteria:**
- Late-stage companies with stable values
- Minimal optionality in securities
- Simple liquidation preferences

* Late-stage companies
* Debt ignored in waterfall calculation

## 6.3 CVM Output

**CVM Per-Share Value:**
$$PPS = \frac{\text{Waterfall Allocation to Class}}{\text{Shares Outstanding}}$$

* Per-class allocation based on current value only

---

# 7. CSE (Common Stock Equivalent)

## 7.1 Core Idea

**CSE Conversion:**
$$\text{Total CSE Shares} = \sum_{i} \text{Shares}_i \times \text{Conversion Ratio}_i$$

* Treat everything as converted to common

## 7.2 Pre-Conversion vs Post-Conversion

**Pre-Conversion Method:**
- Use current liquidation preferences and rights
- No conversion assumed

**Post-Conversion Method:**  
- Convert all securities to common equivalent
- Apply conversion ratios

* Differences in share count computations
* Treatment of conversion ratios

## 7.3 Options/Warrants

**Treasury Method (Cash Exercise):**
$$\text{Net Shares Added} = N - \frac{N \times K}{S}$$

Where $N$ is options exercised, $K$ is strike, $S$ is current price.

**Cashless Exercise:**
$$\text{Shares Received} = N \times \frac{S - K}{S}$$

* Cash exercise
* Cashless (treasury method)

---

# 8. DLOM (Discount for Lack of Marketability)

## 8.1 Purpose

**DLOM Application:**
$$\text{Discounted Value} = \text{Marketable Value} \times (1 - \text{DLOM})$$

* Adjusting for illiquidity

## 8.2 Methods

**Protective Put DLOM:**
$$DLOM = \frac{P(S_0, S_0, T, r, \sigma)}{S_0}$$

Where $P$ is put option value with strike = current price.

**Finnerty Model (Simplified):**
$$DLOM = f(\text{Size}, \text{Profitability}, \text{Volatility}, \text{Time to Liquidity})$$

* Finnerty
* Protective Put
* Longstaff  
* Asian Put

## 8.3 Differential and Incremental DLOM

**Class-Specific DLOM:**
$$DLOM_{class} = \text{Base DLOM} \times \text{Class Adjustment Factor}$$

* Adjusting by class
* When to apply

---

# 9. Backsolve (Key Tool in PE/VC)

## 9.1 When Backsolve Applies

* Recent arm's-length financing round

## 9.2 Backsolve Logic

* Select class with known price
* Solve for TIC (or equity value) such that OMP PPS = transaction price

## 9.3 Goal Seek → Python root finding

The backsolve method is crucial when you have a recent financing round at a known price. You work backwards to determine what the total equity value must be for the OMP model to produce that known price per share.

**Mathematical Approach:**
$$\text{Find } V \text{ such that } \text{OMP\_PPS}(V) = \text{Transaction\_Price}$$

Where $V$ is the total equity value we're solving for.

---

# 10. Mapping Excel OPM → Python OPM

## 10.1 Inputs Needed

* Cap table
* Security terms  
* OPM parameters
* Risk-free rate
* Volatility
* Exit term

## 10.2 Rebuilding Breakpoints

* Transform Excel ranges → Python objects

## 10.3 Implementing BS in Python

* scipy or manual

## 10.4 Allocating Tranches

* Vectorized per-class allocation

## 10.5 Backsolve in Python

* Use fsolve or Newton

## 10.6 Output

* Class values
* PPS grid
* Breakpoint tables
* Audit-ready dumps

---

# 11. Final Assembly: Full Python Engine

## 11.1 Architecture

* Input validation
* Core valuation engine  
* Output serialization

## 11.2 FastAPI Integration

* Endpoints for: OPM, PWERM, CVM, Backsolve

## 11.3 Database Integration

* Cap table storage
* Valuation snapshots

## 11.4 Frontend Expectations

* Parameters to UI
* Data shapes returned

---

# 12. Appendix – Jargon Glossary (Expanded)

## 12.1 Mathematical Terms

* **PDE (Partial Differential Equation)** - Mathematical equation involving partial derivatives
* **SDE (Stochastic Differential Equation)** - Differential equation with random components  
* **GBM (Geometric Brownian Motion)** - Mathematical model for stock price movements

## 12.2 Valuation Terms

* **LP (Liquidation Preference)** - Amount preferred shareholders receive before common
* **PIK (Paid-In-Kind dividend)** - Dividend paid in additional shares rather than cash
* **TIC (Total Invested Capital)** - Total capital invested in the company
* **CVM (Current Value Method)** - Valuation using current equity value in waterfall
* **PWERM (Probability Weighted Expected Return Method)** - Scenario-based valuation approach
* **CSE (Common Stock Equivalent)** - Treating all securities as converted to common stock
* **DLOM (Discount for Lack of Marketability)** - Discount for illiquid securities

## 12.3 Financial Terms

* **Breakpoints** - Key value levels in capital structure where economics change
* **Waterfall** - Sequential distribution of proceeds according to seniority
* **Participation Rights** - Right to receive additional proceeds beyond liquidation preference
* **Anti-dilution** - Protection against ownership dilution in down rounds
* **Conversion Ratio** - Number of common shares received per preferred share upon conversion

---