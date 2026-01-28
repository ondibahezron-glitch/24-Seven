# Customer Churn Prediction System

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://mokaya.streamlit.app)

A production-ready machine learning system for predicting customer churn, built with statistical rigor and business interpretability in mind. This project demonstrates end-to-end data science capabilities: from handling messy real-world data to deploying an interactive analytics dashboard.

## Quick Links

| Resource | Link |
|----------|------|
| **Live Demo** | [Streamlit App](https://mokaya.streamlit.app) |
| **Portfolio** | [mokaya.netlify.app](https://mokaya.netlify.app) |
| **Author** | [Hezron Mokaya](https://linkedin.com/in/hezron-mokaya) |

---

## Table of Contents

1. [Business Problem](#business-problem)
2. [Data Challenges](#data-challenges)
3. [Statistical Approach](#statistical-approach)
4. [Feature Engineering](#feature-engineering)
5. [Modeling Decisions](#modeling-decisions)
6. [Results](#results)
7. [Business Recommendations](#business-recommendations)
8. [Production Deployment](#production-deployment)
9. [How to Run](#how-to-run)
10. [Project Structure](#project-structure)

---

## Business Problem

### The Challenge

Customer churn costs businesses 5-25x more than customer retention. For a telecommunications company with 12,000 customers and 27% annual churn rate, this represents:

- **3,240 lost customers per year**
- **Estimated revenue loss:** KES 200M+ annually (assuming KES 5,000/month average)
- **Hidden costs:** Negative word-of-mouth, market share erosion

### The Solution

A predictive analytics system that:
1. **Identifies at-risk customers** before they churn
2. **Explains why** each customer is at risk (interpretable AI)
3. **Recommends specific actions** to retain them
4. **Quantifies the business impact** of each intervention

### Key Question

> "Which customers are most likely to churn in the next 30 days, and what can we do about it?"

---

## Data Challenges

Real-world data is messy. This project addresses **8 common data quality issues** that practitioners encounter:

| Issue | Prevalence | Solution |
|-------|------------|----------|
| **Missing values** | 6% in billing fields | Service-type stratified median imputation |
| **Inconsistent categories** | 15% label variants | Standardization mappings (22 payment variants → 5) |
| **Outliers** | 2% extreme charges | IQR-based winsorization |
| **Invalid records** | 0.3% negative tenure | Business rule validation (set to 0) |
| **Duplicates** | 0.2% duplicate IDs | Deduplication (keep first) |
| **Data leakage risk** | total_charges ↔ tenure | Derived ratios instead of raw values |
| **Class imbalance** | 27% churn vs 73% retained | Stratified sampling + class weights |
| **Multicollinearity** | 3 feature pairs |r| > 0.85 | Separate feature sets for different models |

### Data Quality Pipeline

```
Raw Data (12,000 records)
    │
    ├── Remove duplicates (24 records)
    ├── Fix invalid values (96 records)
    ├── Standardize categories (1,800 records)
    ├── Impute missing values (1,827 records)
    ├── Treat outliers (914 records)
    │
    ▼
Clean Data (11,976 records) → Train/Test Split (80/20 stratified)
```

---

## Statistical Approach

### Why Statistics, Not Just ML?

Many churn models are black boxes. This project emphasizes **statistical interpretability**:

1. **Hypothesis-driven features**: Each engineered feature has a testable business hypothesis
2. **Effect sizes**: Coefficients translate to odds ratios (e.g., "Month-to-month contracts increase churn odds by 75%")
3. **Uncertainty quantification**: Bayesian inference provides credible intervals, not just point estimates
4. **Validation**: 5-fold cross-validation ensures results generalize

### Statistical Framework

```
                    ┌─────────────────────────────────────┐
                    │     STATISTICAL FRAMEWORK           │
                    └─────────────────────────────────────┘
                                    │
         ┌──────────────────────────┼──────────────────────────┐
         │                          │                          │
         ▼                          ▼                          ▼
┌─────────────────┐      ┌─────────────────┐      ┌─────────────────┐
│  DESCRIPTIVE    │      │   PREDICTIVE    │      │   INFERENTIAL   │
│                 │      │                 │      │                 │
│ • EDA           │      │ • Logistic Reg  │      │ • Bayesian      │
│ • Distributions │      │ • XGBoost       │      │   estimation    │
│ • Correlations  │      │ • Cross-valid   │      │ • Credible      │
│ • Anomalies     │      │ • SHAP values   │      │   intervals     │
└─────────────────┘      └─────────────────┘      └─────────────────┘
```

---

## Feature Engineering

### Philosophy: Interpretable Over Complex

Instead of 500 auto-generated features, we created **33 carefully designed features** organized into business-meaningful categories:

### Feature Categories

| Category | Features | Example | Business Rationale |
|----------|----------|---------|-------------------|
| **Tenure-Based** | 4 | `is_new_customer` | Customers < 6 months have +25% churn risk |
| **Financial** | 4 | `price_sensitivity` | Relative cost vs. tier peers indicates value perception |
| **Behavioral** | 6 | `support_intensity` | High support calls signal dissatisfaction |
| **Engagement** | 3 | `loyalty_score` | Composite of referrals + tenure + autopay |
| **Contract Risk** | 4 | `contract_risk` | Month-to-month = 2, One Year = 1, Two Year = 0 |
| **Interactions** | 5 | `high_value_mtm` | High-paying + no contract = flight risk |
| **Encoded** | 7 | One-hot for categoricals | Payment method, location |

### Top Predictive Features (by SHAP importance)

```
contract_risk         ████████████████████████████████████████  0.495
support_intensity     ███████████████                           0.193
loyalty_score         ██████████████                            0.188
tenure_log            ████████████                              0.159
monthly_charges_log   ██████████                                0.133
```

### Feature Engineering Code Example

```python
# Example: Interaction feature capturing compounded risk
df['high_value_mtm'] = (
    (df['monthly_charges'] > df['monthly_charges'].quantile(0.75)) &
    (df['contract_type'] == 'Month-to-Month')
).astype(int)
# Result: 42.7% churn rate for this segment vs. 27% baseline
```

---

## Modeling Decisions

### Why Two Models?

| Aspect | Logistic Regression | XGBoost |
|--------|---------------------|---------|
| **Interpretability** | HIGH (coefficients = odds ratios) | MEDIUM (requires SHAP) |
| **Performance** | Good baseline | Slightly better |
| **Training speed** | Fast | Moderate |
| **Regulatory compliance** | Preferred | Needs explanation layer |
| **Use case** | Stakeholder reports | Production scoring |

### Key Design Decisions

1. **Class imbalance handling**: `class_weight='balanced'` instead of SMOTE
   - Rationale: 27% minority is moderate; synthetic data can introduce noise

2. **Multicollinearity handling**: Different feature sets per model
   - LR: 29 features (dropped correlated pairs)
   - XGBoost: 35 features (trees handle collinearity)

3. **Hyperparameter tuning**: RandomizedSearchCV (50 iterations)
   - More efficient than GridSearch for 35 features

4. **Threshold selection**: 0.5 for classification
   - Business can adjust based on intervention costs

---

## Results

### Model Performance (Test Set: n=2,396)

| Metric | Logistic Regression | XGBoost | Interpretation |
|--------|---------------------|---------|----------------|
| **ROC-AUC** | 0.720 | **0.722** | Discriminative ability |
| **Precision** | 0.405 | **0.409** | Of predicted churners, 41% actually churn |
| **Recall** | 0.674 | **0.733** | Catches 73% of actual churners |
| **F1-Score** | 0.506 | **0.525** | Balanced precision-recall |

### Cross-Validation (5-Fold)

```
Logistic Regression: 0.713 ± 0.013
XGBoost:             0.710 ± 0.015
```

Low variance indicates stable, generalizable models.

### Confusion Matrix (XGBoost)

```
                 Predicted
              No Churn  Churn
Actual  No     1,063     686
        Churn    173     474

True Positives:  474 (churners correctly identified)
False Negatives: 173 (missed churners - critical!)
```

### Business Impact Simulation

With 10,000 customers and 27% churn rate:
- **Without model**: 2,700 customers churn
- **With model (73% recall)**: Identify 1,971 at-risk customers
- **If 20% retained through intervention**: 394 customers saved
- **At KES 60,000 annual value**: **KES 23.6M revenue preserved**

---

## Business Recommendations

### Top Churn Drivers & Actions

| Risk Factor | Churn Impact | Recommended Action | Expected Outcome |
|-------------|--------------|-------------------|------------------|
| **Month-to-Month contract** | +75% odds | Offer 12-month contract with 15% discount | -75% churn odds |
| **New customer (<6 mo)** | +25% odds | Dedicated onboarding specialist | Reduce early churn |
| **High support calls** | +14%/call | Escalate to customer success manager | Resolve issues proactively |
| **No autopay** | +8% odds | Enable autopay with KES 500 credit | Reduce payment friction |
| **Late payments** | +16% odds | Flexible payment plan | Address financial stress |

### Retention Playbook by Risk Level

**HIGH RISK (>50% probability):**
```
1. Immediate retention call from manager
2. Personalized discount offer (15-20%)
3. Service upgrade at no cost for 3 months
4. Dedicated support line
```

**MEDIUM RISK (35-50%):**
```
1. Proactive outreach email
2. Loyalty points bonus
3. Contract upgrade incentive
4. Usage tips and engagement content
```

**LOW RISK (<35%):**
```
1. Regular NPS surveys
2. Referral program invitation
3. Cross-sell opportunities
4. Community engagement
```

---

## Production Deployment

### How a Company Would Use This System

```
┌─────────────────────────────────────────────────────────────────────┐
│                    PRODUCTION ARCHITECTURE                          │
└─────────────────────────────────────────────────────────────────────┘

  ┌──────────┐     ┌──────────┐     ┌──────────┐     ┌──────────┐
  │  CRM     │     │ Billing  │     │ Support  │     │ Usage    │
  │  System  │     │  System  │     │ Tickets  │     │  Logs    │
  └────┬─────┘     └────┬─────┘     └────┬─────┘     └────┬─────┘
       │                │                │                │
       └────────────────┴────────────────┴────────────────┘
                                │
                                ▼
                    ┌───────────────────────┐
                    │   ETL Pipeline        │
                    │   (Daily refresh)     │
                    └───────────┬───────────┘
                                │
                                ▼
                    ┌───────────────────────┐
                    │   Feature Store       │
                    │   (33 features)       │
                    └───────────┬───────────┘
                                │
                                ▼
                    ┌───────────────────────┐
                    │   ML Scoring Engine   │
                    │   (XGBoost model)     │
                    └───────────┬───────────┘
                                │
         ┌──────────────────────┼──────────────────────┐
         │                      │                      │
         ▼                      ▼                      ▼
┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐
│  Daily Risk     │  │  Real-time      │  │  Monthly        │
│  Dashboard      │  │  Alerts         │  │  Reports        │
│  (Streamlit)    │  │  (Slack/Email)  │  │  (PDF/Excel)    │
└─────────────────┘  └─────────────────┘  └─────────────────┘
         │                      │                      │
         └──────────────────────┴──────────────────────┘
                                │
                                ▼
                    ┌───────────────────────┐
                    │   Retention Team      │
                    │   Action Queue        │
                    └───────────────────────┘
```

### Integration Points

1. **Daily batch scoring**: Score all customers overnight, populate CRM with risk flags
2. **Real-time API**: Score new customers at signup for immediate onboarding triggers
3. **Automated alerts**: Slack notifications when high-value customers hit HIGH risk
4. **A/B testing**: Measure intervention effectiveness by comparing treated vs. control

### Monitoring & Maintenance

```python
# Model drift detection
if current_auc < baseline_auc - 0.05:
    trigger_retraining_pipeline()
    alert_data_science_team()

# Feature drift detection
for feature in critical_features:
    if ks_test(current_dist, baseline_dist) < 0.05:
        flag_distribution_shift(feature)
```

---

## How to Run

### Prerequisites

```bash
Python 3.9+
pip install -r requirements.txt
```

### Quick Start

```bash
# Clone repository
git clone https://github.com/ondibahezron-glitch/24-Seven.git
cd Seven24

# Install dependencies
pip install -r requirements.txt

# Run the full pipeline
python src/data_generation.py      # Generate synthetic data
python src/data_cleaning.py        # Clean and preprocess
python src/feature_engineering.py  # Engineer features
python src/modeling.py             # Train models

# Launch dashboard
streamlit run streamlit_app.py
```

### Using the Dashboard

1. Open http://localhost:8501
2. Upload a customer CSV or click "Use Sample Data"
3. View individual risk scores in "Single Customer" tab
4. Analyze portfolio in "Batch Analysis" tab
5. Download PDF reports for stakeholders

### Streamlit Cloud Deployment

To deploy to Streamlit Community Cloud:

```bash
# 1. Push your code to GitHub (including data/models/ folder)
git add .
git commit -m "Ready for Streamlit Cloud deployment"
git push origin main

# 2. Go to share.streamlit.io
# 3. Click "New app"
# 4. Select your repository and branch
# 5. Set main file path: streamlit_app.py
# 6. For lighter deployment, rename requirements_streamlit.txt to requirements.txt
```

**Deployment files included:**
- `.streamlit/config.toml` - Brand theme configuration
- `requirements_streamlit.txt` - Minimal dependencies for production

---

## Project Structure

```
Seven24/
├── data/
│   ├── raw/                          # Original data
│   │   └── customer_churn_raw.csv    # 12,000 records with quality issues
│   ├── processed/                    # Cleaned, feature-engineered data
│   │   ├── customer_churn_cleaned.csv
│   │   ├── customer_churn_train_features.csv
│   │   ├── customer_churn_test_features.csv
│   │   ├── feature_stats.json        # Fitted statistics
│   │   └── correlation_matrix.png
│   └── models/                       # Trained models
│       ├── churn_models.joblib
│       ├── model_results.json
│       ├── lr_coefficients.csv
│       ├── shap_summary_xgboost.png
│       └── modeling_report.txt
├── src/
│   ├── data_generation.py            # Synthetic data with realistic issues
│   ├── data_cleaning.py              # Comprehensive cleaning pipeline
│   ├── feature_engineering.py        # 33 interpretable features
│   ├── modeling.py                   # LR + XGBoost with CV
│   └── visualize_data_quality.py     # EDA visualizations
├── .streamlit/
│   └── config.toml                   # Streamlit theme configuration
├── .gitignore                        # Git ignore rules
├── streamlit_app.py                  # Interactive dashboard
├── requirements.txt                  # Production dependencies (Streamlit Cloud)
├── requirements_dev.txt              # Full dependencies (local development)
├── CLAUDE.md                         # Project context
└── README_DATA_PROJECT.md            # This file
```

---

## Technologies Used

| Category | Tools |
|----------|-------|
| **Data Processing** | Pandas, NumPy |
| **Machine Learning** | Scikit-learn, XGBoost |
| **Interpretability** | SHAP |
| **Visualization** | Plotly, Seaborn, Matplotlib |
| **Dashboard** | Streamlit |
| **PDF Reports** | ReportLab |
| **Statistical Analysis** | SciPy, Statsmodels |

---

## Key Takeaways

1. **Data quality matters more than model complexity** - 80% of effort went into cleaning and feature engineering

2. **Interpretability enables action** - Knowing *why* a customer will churn is more valuable than knowing *that* they will

3. **Simple baselines are powerful** - Logistic regression achieved 97% of XGBoost's performance with full interpretability

4. **Business context drives decisions** - Risk thresholds and recommendations were calibrated to intervention costs

5. **Production readiness requires more than accuracy** - Monitoring, drift detection, and maintainability matter

---

## Project Status

- [x] **Dataset Generated** - 12,000 records with realistic quality issues
- [x] **Data Cleaning Pipeline** - Handles all 8 data quality issues
- [x] **Feature Engineering** - 33 interpretable business features
- [x] **Model Training** - Logistic Regression + XGBoost with CV
- [x] **SHAP Integration** - Feature importance visualizations
- [x] **Streamlit Dashboard** - Interactive risk assessment
- [x] **PDF Reports** - Client-ready deliverables
- [x] **Streamlit Cloud Deployment** - Ready for deployment (see instructions below)

---

## Author

**Hezron Mokaya** - Statistics Expert & Data Consultant

- Portfolio: [mokaya.netlify.app](https://mokaya.netlify.app)
- LinkedIn: [Hezron Mokaya](https://linkedin.com/in/hezron-mokaya)
- X/Twitter: [@Datadetective10](https://twitter.com/Datadetective10)
- Email: ondibahezron@gmail.com

---

## License

This project is for portfolio demonstration purposes. The synthetic dataset was generated to simulate real-world data quality challenges without exposing actual customer information.

---

*"Academic rigor meets business speed" - Seven24*
