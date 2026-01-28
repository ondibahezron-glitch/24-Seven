# Customer Churn Dataset - Data Dictionary

**Generated:** 2026-01-28
**Project:** Customer Churn Analytics
**Dataset:** `data/raw/customer_churn_raw.csv`

---

## Dataset Overview

This synthetic dataset represents customer data from a telecommunications/internet service provider in Kenya. It contains **12,000 customer records** with a **~27% churn rate**, designed to mirror real-world churn prediction scenarios.

**Target Variable:** `churn` (1 = customer churned, 0 = customer retained)

---

## Column Descriptions

### 1. **customer_id**
- **Type:** String
- **Description:** Unique identifier for each customer (format: CUST000001 to CUST012000)
- **Data Quality Issues:** ~0.2% duplicate IDs (data entry errors in CRM system)
- **Use Case:** Primary key for customer records

---

### 2. **tenure_months**
- **Type:** Integer
- **Description:** Number of months the customer has been with the company
- **Range:** -5 to 72 months (negative values are data errors)
- **Distribution:** Right-skewed (exponential distribution, mean ~18 months)
- **Data Quality Issues:**
  - ~0.3% negative values (impossible but occurs in real data due to system bugs)
  - Right-skewed: More new customers than long-term customers (realistic)
- **Churn Relationship:** Strong negative correlation (longer tenure → lower churn)

---

### 3. **contract_type**
- **Type:** Categorical
- **Description:** Type of customer contract agreement
- **Categories:**
  - `Month-to-Month` (55%)
  - `One Year` (30%)
  - `Two Year` (15%)
- **Data Quality Issues:** ~10% inconsistent labels
  - Variations: "Month to Month", "month-to-month", "MTM", "Monthly"
  - Variations: "One year", "1 Year", "1-Year", "12 Months"
  - Variations: "Two year", "2 Year", "2-Year", "24 Months"
- **Churn Relationship:** Month-to-month contracts have ~40% higher churn rate

---

### 4. **service_type**
- **Type:** Categorical
- **Description:** Tier of service subscribed by customer
- **Categories:**
  - `Basic` (35%) - Entry-level service
  - `Standard` (45%) - Mid-tier service
  - `Premium` (20%) - High-end service
- **Churn Relationship:** Premium customers churn more if price-sensitive

---

### 5. **monthly_charges**
- **Type:** Float
- **Description:** Monthly subscription fee in Kenya Shillings (KES)
- **Range:** 1,500 to 25,000 KES
- **Distribution:**
  - Basic: 1,500–3,000 KES
  - Standard: 3,500–6,500 KES
  - Premium: 7,000–12,000 KES
  - Outliers: 15,000–25,000 KES (~2% of records, VIP/enterprise customers or data errors)
- **Data Quality Issues:**
  - **5-7% missing values** (billing system errors, payment disputes)
  - Outliers present (some extremely high charges)
- **Churn Relationship:** Positive correlation (higher charges → higher churn risk)

---

### 6. **total_charges**
- **Type:** Float
- **Description:** Total amount charged to customer over entire tenure (KES)
- **Calculation:** Approximately `tenure_months × monthly_charges × variance_factor`
- **Data Quality Issues:**
  - ~1% of records have `total_charges < monthly_charges` (impossible, indicates data error)
  - Some new customers (tenure=0) have non-zero total charges due to setup fees
- **Churn Relationship:** Indirect (through tenure and monthly_charges)

---

### 7. **payment_method**
- **Type:** Categorical
- **Description:** Method customer uses to pay monthly bills
- **Categories (Kenya-specific):**
  - `M-Pesa` (45%) - Mobile money platform
  - `Bank Transfer` (25%)
  - `Credit Card` (12%)
  - `Debit Card` (10%)
  - `Cash` (8%)
- **Data Quality Issues:** ~2-3% missing values + ~15% inconsistent labels
  - M-Pesa variations: "M-pesa", "MPESA", "mpesa", "Mpesa"
  - Bank Transfer variations: "Bank transfer", "bank transfer", "Bank_Transfer"
  - Credit/Debit card variations: capitalization inconsistencies
- **Churn Relationship:** Cash/manual payment methods may correlate with higher churn

---

### 8. **location_type**
- **Type:** Categorical
- **Description:** Customer's location category (proxy for demographic)
- **Categories:**
  - `Urban` (45%) - City centers (Nairobi, Mombasa, Kisumu)
  - `Suburban` (35%) - Peri-urban areas
  - `Rural` (20%) - Rural towns and villages
- **Data Quality Issues:** ~1-2% missing values (privacy concerns, data collection gaps)
- **Churn Relationship:** Rural customers may churn more due to service quality issues

---

### 9. **num_services**
- **Type:** Integer
- **Description:** Number of additional services bundled with main subscription
- **Range:** 0 to 5 additional services
- **Examples:** Cloud storage, antivirus, premium support, device insurance, streaming
- **Distribution:** Poisson distribution (λ=1.5)
- **Churn Relationship:** More bundled services → lower churn (stickiness)

---

### 10. **data_usage_gb**
- **Type:** Float
- **Description:** Average monthly data usage in gigabytes
- **Range:** 0 to 500 GB
- **Distribution:** Gamma distribution, varies by service type:
  - Basic: 10-50 GB (light users)
  - Standard: 50-150 GB (moderate users)
  - Premium: 100-300 GB (heavy users)
- **Data Quality Issues:** ~3-5% missing values (tracking system downtime, opt-out users)
- **Churn Relationship:** Very low usage may indicate dissatisfaction; very high usage indicates engagement

---

### 11. **support_calls**
- **Type:** Integer
- **Description:** Number of customer support interactions in last 3 months
- **Range:** -1 to 15 calls (negative values are data errors)
- **Distribution:** Poisson distribution (λ=2.5)
- **Data Quality Issues:** ~0.5% negative values (data entry error)
- **Churn Relationship:** Strong positive correlation (many calls = problems = churn risk)

---

### 12. **autopay_enabled**
- **Type:** Categorical (Binary)
- **Description:** Whether customer has automatic payment enabled
- **Categories:**
  - `Yes` (60%)
  - `No` (40%)
- **Data Quality Issues:** ~8% inconsistent labels
  - Variations: "yes", "YES", "Y", "True", "1" for Yes
  - Variations: "no", "NO", "N", "False", "0" for No
- **Churn Relationship:** Autopay reduces churn (convenience, no payment friction)

---

### 13. **late_payment_count**
- **Type:** Integer
- **Description:** Number of late or missed payments in last 12 months
- **Range:** 0 to 10
- **Distribution:** Poisson distribution (λ=1.2)
- **Churn Relationship:** Strong positive correlation (financial stress or dissatisfaction)

---

### 14. **referral_count**
- **Type:** Integer
- **Description:** Number of new customers referred by this customer
- **Range:** 0 to 5
- **Distribution:** Poisson distribution (λ=0.8)
- **Churn Relationship:** Strong negative correlation (happy customers refer others and stay)

---

### 15. **churn** (TARGET VARIABLE)
- **Type:** Binary Integer
- **Description:** Whether the customer churned (left the service)
- **Values:**
  - `1` = Customer churned
  - `0` = Customer retained
- **Distribution:** ~27% churn rate (3,240 churned out of 12,000)
- **Prediction Goal:** Build model to predict churn based on features above

---

## Intentional Data Quality Issues - Justification

### Why These Issues Reflect Real-World Churn Datasets:

#### 1. **Missing Values (5-10% in key columns)**
**Real-World Causes:**
- Billing system downtime or migration issues (`monthly_charges`)
- Customer privacy concerns or incomplete sign-up forms (`payment_method`, `location_type`)
- Tracking system failures or opt-out users (`data_usage_gb`)
- CRM data import/export errors

**Impact on Analysis:**
- Forces data cleaning decisions (imputation vs. deletion)
- Tests ability to handle missingness in production pipelines
- Requires missing data pattern analysis (MCAR, MAR, MNAR)

---

#### 2. **Inconsistent Categorical Labels (~10-15%)**
**Real-World Causes:**
- Manual data entry by customer service agents
- Multiple data sources with different naming conventions
- UI/UX issues allowing freeform text entry
- Legacy system integration (old vs. new formats)

**Examples:**
- "M-Pesa" vs. "MPESA" vs. "M-pesa"
- "Month-to-Month" vs. "MTM" vs. "Monthly"
- "Yes" vs. "yes" vs. "Y" vs. "1"

**Impact on Analysis:**
- Requires text standardization and cleaning
- Can cause model errors if not handled (dummy variable explosion)
- Tests string manipulation and preprocessing skills

---

#### 3. **Outliers in Charges (~2%)**
**Real-World Causes:**
- VIP or enterprise customers with custom pricing
- Data entry errors (decimal point mistakes: 5000 → 50000)
- Promotional pricing or lifetime discounts
- One-time charges incorrectly logged as monthly

**Impact on Analysis:**
- Tests outlier detection methods (IQR, Z-score, isolation forest)
- Requires decisions on winsorization vs. capping vs. removal
- Can skew model performance if not addressed

---

#### 4. **Invalid Records (~1-2%)**
**Real-World Causes:**
- System bugs or data migration errors (negative tenure, negative support calls)
- Calculation errors (total_charges < monthly_charges for long-tenure customers)
- Test data accidentally mixed with production data
- Timezone or date parsing issues

**Impact on Analysis:**
- Requires business logic validation rules
- Tests ability to identify and handle impossible values
- Simulates need for data quality pipelines

---

#### 5. **Duplicate Customer IDs (~0.2%)**
**Real-World Causes:**
- CRM system glitches
- Customer re-registration after account deletion
- Data warehouse ETL pipeline errors
- Manual data merging mistakes

**Impact on Analysis:**
- Requires deduplication strategy (keep first, last, or aggregate)
- Tests understanding of unique constraints
- Can inflate model training data if not caught

---

#### 6. **Correlated Features**
**Real-World Reality:**
- `tenure_months` and `total_charges` are naturally correlated
- `service_type` and `monthly_charges` are related
- `autopay_enabled` and `late_payment_count` are related

**Impact on Analysis:**
- Tests multicollinearity detection and handling
- Requires feature engineering decisions
- Affects model interpretation (coefficients, feature importance)

---

## Churn Drivers (Built into Data Generation Logic)

The dataset reflects realistic churn patterns observed in telecom/subscription businesses:

| **Risk Factor** | **Effect on Churn** | **Magnitude** |
|-----------------|---------------------|---------------|
| Month-to-month contract | Increases | +20% probability |
| High monthly charges | Increases | +12% probability |
| New customer (tenure < 6 months) | Increases | +25% probability |
| Many support calls | Increases | +3% per call (capped) |
| Late payments | Increases | +4% per late payment |
| No autopay | Increases | +8% probability |
| Long tenure (>24 months) | Decreases | -8% probability |
| Multi-year contract | Decreases | -15% probability |
| Active referrals | Decreases | -5% per referral |

---

## Usage Recommendations

### Data Cleaning Pipeline Should:
1. Standardize categorical labels (case normalization, fuzzy matching)
2. Handle missing values (imputation vs. deletion based on missingness pattern)
3. Detect and treat outliers (domain knowledge + statistical methods)
4. Validate business logic (tenure ≥ 0, total ≥ monthly × tenure, etc.)
5. Remove or deduplicate invalid records
6. Feature engineering (tenure bins, charge-to-income ratio, engagement score)

### Model Development Should:
1. Perform EDA to understand churn drivers
2. Test missing data handling strategies (MICE, KNN, mean/mode)
3. Feature engineering (interaction terms, binning)
4. Address class imbalance (~27% churn) with SMOTE, class weights, or stratified sampling
5. Cross-validation with stratification
6. Evaluate with precision, recall, F1, AUC-ROC (not just accuracy)

---

## Citation

**Dataset Generator:** Seven24
**Date:** 2026-01-28
**Purpose:** Portfolio demonstration for churn analytics and machine learning
**License:** Proprietary (for Seven24 portfolio use only)

---

**Questions or Issues?**
Contact: ondibahezron@gmail.com | @Datadetective10
