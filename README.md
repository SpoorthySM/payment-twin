# ⚡ Payment Twin

<p align="center">
  <h1 align="center">Payment Twin</h1>
  <p align="center"><strong>Counterfactual AI for Payment Recovery</strong></p>
  <p align="center">
    Don't just predict whether a failed payment will recover.<br>
    <strong>Decide what to do next — and whether it's worth doing.</strong>
  </p>
</p>

<p align="center">
  <code>Predict</code> → <code>Simulate</code> → <code>Compare</code> → <code>Decide</code> → <code>Prioritize</code>
</p>

---

## 🎯 The Idea

Payment recovery is not simply a prediction problem.

When a payment fails, there can be several possible next actions:

- 🔄 **Retry** the payment
- ⏳ **Wait** and attempt recovery later
- 🔀 **Switch Method** and recover through another payment method

The best action can depend on the payment method, bank, failure reason, transaction amount, timing, and other payment characteristics.

So instead of asking only:

> **"Will this payment recover?"**

Payment Twin asks:

> **"What is the best action to take for this payment right now?"**

Payment Twin evaluates multiple hypothetical interventions for the **same failed payment**, estimates recovery probability for each, converts those predictions into expected economic value, and recommends the action with the highest decision score.

---

# 🧠 What Payment Twin Does

For every failed payment, Payment Twin creates three counterfactual scenarios:

| Intervention | What Payment Twin asks |
|:---|:---|
| 🔄 **RETRY** | What if we retry this payment? |
| ⏳ **WAIT** | What if we wait before attempting recovery? |
| 🔀 **SWITCH_METHOD** | What if we switch the payment method? |

Each scenario is evaluated by the recovery model.

The resulting probabilities are translated into expected recovered value and adjusted for the simulated cost of taking the action.

### The output

> **One recommended recovery action backed by an economic rationale.**

---

# ⚙️ Decision Pipeline

```text
                         FAILED PAYMENT
                               │
                               ▼
                    ┌────────────────────┐
                    │   Input Validation │
                    └─────────┬──────────┘
                              │
                              ▼
                    ┌────────────────────┐
                    │    Preprocessing   │
                    └─────────┬──────────┘
                              │
                              ▼
                    ┌────────────────────┐
                    │      XGBoost       │
                    │   Recovery Model   │
                    └─────────┬──────────┘
                              │
                              ▼
                    ┌────────────────────┐
                    │ 5-Fold Probability │
                    │    Calibration     │
                    └─────────┬──────────┘
                              │
                 ┌────────────┼────────────┐
                 ▼            ▼            ▼
              RETRY         WAIT      SWITCH_METHOD
                 │            │            │
                 └────────────┼────────────┘
                              │
                              ▼
                    ┌────────────────────┐
                    │ Expected Recovered │
                    │       Value        │
                    └─────────┬──────────┘
                              │
                              ▼
                    ┌────────────────────┐
                    │ Economic Decision  │
                    │       Score        │
                    └─────────┬──────────┘
                              │
                              ▼
                    ┌────────────────────┐
                    │ Recommended Action │
                    └─────────┬──────────┘
                              │
                              ▼
                    ┌────────────────────┐
                    │ Recovery Priority  │
                    └────────────────────┘
```

---

# 🔮 Counterfactual Recovery

The core idea behind Payment Twin is **what-if analysis**.

Instead of making three unrelated predictions, the system holds the payment characteristics constant and changes only the proposed intervention.

### Example

```text
                         PAYMENT P001
                              │
              ┌───────────────┼───────────────┐
              ▼               ▼               ▼
            RETRY            WAIT        SWITCH_METHOD
              │               │               │
            66.1%            77.2%            43.6%
              │               │               │
              ▼               ▼               ▼
        Expected Value   Expected Value   Expected Value
              │               │               │
              ▼               ▼               ▼
            − Cost          − Cost          − Cost
              │               │               │
              └───────────────┼───────────────┘
                              ▼
                       HIGHEST SCORE
                              │
                              ▼
                            WAIT
```

The model therefore becomes a **decision component**, not merely a probability generator.

---

# 💰 From Probability → Value → Action

Payment Twin does not stop at predicting a recovery probability.

For every candidate intervention:

### Expected Recovered Value

```text
Recovery Probability × Payment Amount
```

### Economic Decision Score

```text
Expected Recovered Value − Intervention Cost
```

The intervention with the highest score becomes the recommendation.

## Prototype Intervention Costs

| Action | Simulated Cost |
|:---|---:|
| 🔄 RETRY | 20 |
| ⏳ WAIT | 10 |
| 🔀 SWITCH_METHOD | 35 |

> **Important:** These are illustrative prototype assumptions used to demonstrate economic decisioning. They are not claims about actual Razorpay or payment-provider costs.

---

# 📊 Recovery Prioritization

A real recovery system may have limited intervention capacity.

So Payment Twin answers two questions:

### 01 — What should we do?

The decision engine selects the best intervention for each payment.

### 02 — Which payment should we act on first?

The prioritization layer ranks payments by their expected recovery opportunity and economic value.

```text
                 FAILED PAYMENTS
                        │
                        ▼
              ┌──────────────────┐
              │ Individual       │
              │ Decisions        │
              └────────┬─────────┘
                       │
                       ▼
              ┌──────────────────┐
              │ Expected         │
              │ Incremental Value│
              └────────┬─────────┘
                       │
                       ▼
              ┌──────────────────┐
              │ Priority Ranking │
              └────────┬─────────┘
                       │
             ┌─────────┼─────────┐
             ▼         ▼         ▼
           HIGH      MEDIUM      LOW
```

This creates a recovery queue that can be used when intervention capacity is constrained.

---

# 🔍 Explainable AI

A recovery recommendation should not be a black box.

Payment Twin uses **SHAP** to explain the underlying XGBoost recovery model for an individual payment.

The application surfaces:

- Top contributing features
- Positive and negative contributions
- Human-readable feature names
- Feature-level reasoning behind the model output

This makes it possible to inspect:

> **"Why did the model arrive at this recovery prediction?"**

### Technical note

SHAP explains the underlying XGBoost estimator.

The final recovery probabilities used by the decision engine come from the **calibrated classifier**.

---

# 🤖 Model Architecture

```text
                       RAW PAYMENT DATA
                              │
                              ▼
                    ┌───────────────────┐
                    │   Preprocessing   │
                    │                   │
                    │ Categorical       │
                    │ → One-Hot Encode  │
                    │                   │
                    │ Numerical         │
                    │ → Passthrough     │
                    └─────────┬─────────┘
                              │
                              ▼
                    ┌───────────────────┐
                    │     XGBoost       │
                    │    Classifier     │
                    └─────────┬─────────┘
                              │
                              ▼
                    ┌───────────────────┐
                    │   5-Fold          │
                    │   Calibration     │
                    └─────────┬─────────┘
                              │
                              ▼
                  CALIBRATED RECOVERY
                      PROBABILITY
                              │
                              ▼
                  COUNTERFACTUAL ENGINE
                              │
                              ▼
                   ECONOMIC DECISION
```

## Model Facts

| Component | Implementation |
|:---|:---|
| Model | XGBoost |
| Calibration | 5-fold probability calibration |
| Transformed features | 20 |
| Candidate interventions | 3 |
| Explainability | SHAP |
| Interface | Streamlit |

---

# 🧩 Feature Space

Payment Twin uses seven business-level inputs.

### Payment Context

| Feature | Description |
|:---|:---|
| Payment Method | UPI, Card, or Net Banking |
| Bank | Associated bank |
| Failure Reason | Reason for the failed payment |

### Transaction Characteristics

| Feature | Description |
|:---|:---|
| Amount | Transaction amount |
| Hour | Hour of transaction |
| Response Time | Payment response time |

### Decision Context

| Feature | Description |
|:---|:---|
| Intervention | Candidate recovery action |

These inputs are transformed into the model's **20-feature representation**.

---

# 🖥️ Product Experience

Payment Twin is presented as an end-to-end decision product rather than a standalone model.

## Overview

A high-level view of the payment recovery problem and the Payment Twin decision framework.

## Analyze Payment

Inspect an individual failed payment and see:

- Recommended intervention
- Recovery probability
- Probability margin
- Economic margin
- Expected incremental value
- Counterfactual intervention comparison
- SHAP explanation

## Recovery Queue

View and rank recovery opportunities across multiple failed payments.

The queue surfaces:

- Payment value
- Recommended action
- Predicted recovery
- Expected incremental value
- Priority

## Model Intelligence

Understand the system underneath the interface:

- Model architecture
- Feature space
- Calibration
- Decision pipeline
- Economic decisioning

## Methodology

Documents the decision framework, assumptions, and limitations behind the system.

---

# 📸 Product Preview

> Screenshots of the live Payment Twin interface can be added here.

Recommended showcase:

| View | Purpose |
|:---|:---|
| **Overview** | Product concept and recovery decision framework |
| **Analyze Payment** | Individual payment decision and explanation |
| **Recovery Queue** | Portfolio-level prioritization |
| **Model Intelligence** | Technical model architecture |
| **Methodology** | Decision methodology and assumptions |

---

# 🏗️ Project Architecture

```text
Payment-Twin/
│
├── app.py
│
├── payment_twin.py
├── decision_engine.py
├── prioritization.py
├── portfolio.py
├── validation.py
├── explain.py
│
├── models/
│   ├── calibrated_model.pkl
│   ├── feature_names.pkl
│   └── preprocessor.pkl
│
├── components/
│   ├── __init__.py
│   ├── charts.py
│   ├── metrics.py
│   ├── navigation.py
│   └── styles.py
│
├── views/
│   ├── __init__.py
│   ├── overview.py
│   ├── analyze.py
│   ├── recovery_queue.py
│   ├── model_intelligence.py
│   └── methodology.py
│
├── test_decision.py
├── test_explain.py
├── test_model.py
├── test_payment_twin.py
├── test_portfolio.py
├── test_prioritization.py
├── test_validation.py
│
├── requirements.txt
├── .gitignore
└── README.md
```

---

# 🧪 Testing

The project includes tests covering the major components of the decision system.

```text
✓ Input validation
✓ Recovery model prediction
✓ Counterfactual action evaluation
✓ Economic decisioning
✓ SHAP explanations
✓ Payment Twin integration
✓ Recovery prioritization
✓ Recovery queue construction
✓ Portfolio capacity evaluation
```

Run the complete test suite:

```bash
for f in test_*.py; do
    echo "===== $f ====="
    python "$f"
done
```

---

# 🚀 Run Locally

## 1. Clone the repository

```bash
git clone <repository-url>
cd Payment-Twin
```

## 2. Create a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate
```

On Windows:

```bash
.venv\Scripts\activate
```

## 3. Install dependencies

```bash
pip install -r requirements.txt
```

## 4. Launch Payment Twin

```bash
streamlit run app.py
```

---

# 🛡️ Responsible Use & Limitations

Payment Twin is a **prototype decision-support system**.

## Counterfactual analysis is not causal inference

The system evaluates model predictions under different intervention inputs.

This does **not** establish that changing the intervention will causally produce the predicted difference in recovery.

A production system should use randomized experimentation, causal inference, or treatment-effect modeling to estimate true intervention impact.

## Simulated intervention costs

The economic decision engine currently uses illustrative costs.

A production implementation would require real operational cost estimates and business constraints.

## Model dependence

The usefulness of the system depends on the quality and representativeness of the training data.

A production deployment would require monitoring for:

- Data drift
- Feature drift
- Calibration drift
- Recovery performance
- Changing payment behavior
- Intervention outcomes

---

# 💡 Why Payment Twin?

Traditional payment recovery can focus on:

> **"What is likely to happen?"**

Payment Twin focuses on:

> ## **"What should we do next?"**

The system connects:

```text
             CALIBRATED PREDICTION
                       │
                       ▼
            COUNTERFACTUAL EVALUATION
                       │
                       ▼
              ECONOMIC DECISIONING
                       │
                       ▼
             RECOVERY PRIORITIZATION
                       │
                       ▼
                 EXPLAINABILITY
```

into one decision loop.

The goal is to move from **prediction as an endpoint** to **prediction as a decision input**.

---

# 🛠️ Tech Stack

| Layer | Technology |
|:---|:---|
| Application | Streamlit |
| Language | Python |
| ML Model | XGBoost |
| ML Framework | Scikit-learn |
| Explainability | SHAP |
| Data Processing | Pandas |
| Model Serialization | Joblib |

---

# 📌 Project Status

**Prototype — Razorpay AI Buildathon 2026**

Payment Twin demonstrates an end-to-end AI decision system for payment recovery, including:

- Recovery prediction
- Counterfactual intervention analysis
- Economic decisioning
- Recovery prioritization
- Explainability
- Portfolio capacity evaluation

---

<div align="center">

# ⚡ Payment Twin

### Predict less. Decide better.

**Built for the Razorpay AI Buildathon 2026**

</div>
