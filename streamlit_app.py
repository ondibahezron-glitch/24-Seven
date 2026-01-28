"""
Seven24 Churn Analytics Demo
Statistics Expert-Powered Customer Retention Insights

A professional Streamlit application for predicting customer churn risk,
providing business recommendations, and generating client deliverables.

Author: Seven24 Data Science Team
Date: 2026-01-28
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import joblib
import json
from pathlib import Path
from datetime import datetime
from io import BytesIO

# PDF generation
try:
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import letter, A4
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
    from reportlab.lib.enums import TA_CENTER, TA_LEFT
    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False

# =============================================================================
# CONFIGURATION
# =============================================================================
BASE_PATH = Path(__file__).parent
DATA_PATH = BASE_PATH / 'data'
MODELS_PATH = DATA_PATH / 'models'
PROCESSED_PATH = DATA_PATH / 'processed'

# Feature sets from modeling.py
LR_FEATURE_SET = [
    'tenure_log', 'is_new_customer', 'is_established',
    'service_encoded', 'avg_monthly_revenue', 'is_high_value', 'price_sensitivity',
    'financial_stress', 'support_intensity', 'is_heavy_support',
    'usage_efficiency', 'usage_tier_ratio',
    'autopay_binary', 'referral_flag', 'loyalty_score',
    'contract_risk', 'contract_tenure_mismatch', 'payment_friction', 'is_mpesa',
    'high_value_mtm', 'new_no_autopay', 'support_late_combo',
    'premium_low_usage', 'bundled_loyal',
    'pay_bank', 'pay_credit', 'pay_debit', 'pay_cash',
    'loc_suburban', 'loc_rural',
    'num_services', 'charges_anomaly_flag'
]

XGBOOST_FEATURE_SET = [
    'tenure_bin', 'is_new_customer', 'is_established', 'tenure_log',
    'avg_monthly_revenue', 'is_high_value', 'price_sensitivity', 'monthly_charges_log',
    'support_intensity', 'is_heavy_support', 'late_payment_flag', 'financial_stress',
    'usage_efficiency', 'usage_tier_ratio',
    'autopay_binary', 'referral_flag', 'loyalty_score',
    'contract_risk', 'contract_tenure_mismatch', 'payment_friction', 'is_mpesa',
    'high_value_mtm', 'new_no_autopay', 'support_late_combo',
    'premium_low_usage', 'bundled_loyal',
    'service_encoded', 'pay_bank', 'pay_credit', 'pay_debit', 'pay_cash',
    'loc_suburban', 'loc_rural',
    'num_services', 'charges_anomaly_flag'
]

# Required input columns
REQUIRED_COLUMNS = [
    'customer_id', 'tenure_months', 'contract_type', 'service_type',
    'monthly_charges', 'total_charges', 'payment_method', 'location_type',
    'num_services', 'data_usage_gb', 'support_calls', 'autopay_enabled',
    'late_payment_count', 'referral_count'
]

# Risk thresholds
HIGH_RISK_THRESHOLD = 0.50
MEDIUM_RISK_THRESHOLD = 0.35


# =============================================================================
# DATA LOADING (CACHED)
# =============================================================================
@st.cache_resource
def load_models():
    """Load trained models from disk."""
    try:
        models = joblib.load(MODELS_PATH / 'churn_models.joblib')
        return models
    except FileNotFoundError:
        st.error("Models not found. Please ensure models are trained first.")
        return None


@st.cache_resource
def load_feature_engineer():
    """Load fitted feature engineer stats from disk."""
    try:
        # Try JSON first (preferred for portability)
        import json
        with open(PROCESSED_PATH / 'feature_stats.json', 'r') as f:
            stats = json.load(f)
        # Return a simple object with stats attribute
        class FeatureStats:
            pass
        fe = FeatureStats()
        fe.stats = stats
        return fe
    except FileNotFoundError:
        try:
            # Fallback to joblib
            fe = joblib.load(PROCESSED_PATH / 'feature_engineer.joblib')
            return fe
        except:
            st.error("Feature engineer not found.")
            return None


@st.cache_data
def load_lr_coefficients():
    """Load logistic regression coefficients for interpretation."""
    try:
        coef_df = pd.read_csv(MODELS_PATH / 'lr_coefficients.csv')
        return coef_df
    except FileNotFoundError:
        return None


@st.cache_data
def load_sample_data():
    """Load sample data for demo."""
    try:
        df = pd.read_csv(DATA_PATH / 'raw' / 'customer_churn_raw.csv', nrows=100)
        return df
    except FileNotFoundError:
        return None


# =============================================================================
# DATA CLEANING & PREPROCESSING
# =============================================================================
def standardize_categoricals(df):
    """Standardize categorical variable labels."""
    df = df.copy()

    # Contract type mapping
    contract_map = {
        'Month-to-Month': 'Month-to-Month', 'month-to-month': 'Month-to-Month',
        'MTM': 'Month-to-Month', 'Monthly': 'Month-to-Month',
        'Month to Month': 'Month-to-Month', 'month to month': 'Month-to-Month',
        'One Year': 'One Year', 'One year': 'One Year', 'one year': 'One Year',
        '1 Year': 'One Year', '1-Year': 'One Year', '12 Months': 'One Year',
        'Two Year': 'Two Year', 'Two year': 'Two Year', 'two year': 'Two Year',
        '2 Year': 'Two Year', '2-Year': 'Two Year', '24 Months': 'Two Year'
    }
    if 'contract_type' in df.columns:
        df['contract_type'] = df['contract_type'].map(
            lambda x: contract_map.get(str(x).strip(), 'Month-to-Month')
        )

    # Payment method mapping
    payment_map = {
        'M-Pesa': 'M-Pesa', 'M-pesa': 'M-Pesa', 'MPESA': 'M-Pesa',
        'mpesa': 'M-Pesa', 'Mpesa': 'M-Pesa',
        'Bank Transfer': 'Bank Transfer', 'Bank transfer': 'Bank Transfer',
        'bank transfer': 'Bank Transfer', 'Bank_Transfer': 'Bank Transfer',
        'Credit Card': 'Credit Card', 'Credit card': 'Credit Card',
        'credit card': 'Credit Card',
        'Debit Card': 'Debit Card', 'Debit card': 'Debit Card',
        'debit card': 'Debit Card',
        'Cash': 'Cash', 'cash': 'Cash', 'CASH': 'Cash'
    }
    if 'payment_method' in df.columns:
        df['payment_method'] = df['payment_method'].map(
            lambda x: payment_map.get(str(x).strip(), 'M-Pesa')
        )

    # Autopay mapping
    autopay_map = {
        'Yes': 'Yes', 'yes': 'Yes', 'YES': 'Yes', 'Y': 'Yes',
        'True': 'Yes', 'true': 'Yes', '1': 'Yes', 1: 'Yes',
        'No': 'No', 'no': 'No', 'NO': 'No', 'N': 'No',
        'False': 'No', 'false': 'No', '0': 'No', 0: 'No'
    }
    if 'autopay_enabled' in df.columns:
        df['autopay_enabled'] = df['autopay_enabled'].map(
            lambda x: autopay_map.get(x if isinstance(x, (int, float)) else str(x).strip(), 'No')
        )

    # Service type - ensure valid
    if 'service_type' in df.columns:
        valid_services = ['Basic', 'Standard', 'Premium']
        df['service_type'] = df['service_type'].apply(
            lambda x: x if x in valid_services else 'Standard'
        )

    # Location type - ensure valid
    if 'location_type' in df.columns:
        valid_locations = ['Urban', 'Suburban', 'Rural']
        df['location_type'] = df['location_type'].apply(
            lambda x: x if x in valid_locations else 'Urban'
        )

    return df


def handle_missing_values(df, fe_stats):
    """Handle missing values using fitted statistics."""
    df = df.copy()

    # Numeric columns - use median
    if 'monthly_charges' in df.columns and df['monthly_charges'].isna().any():
        median = fe_stats.get('service_type_median_charges', {}).get('Standard', 5000)
        df['monthly_charges'] = df['monthly_charges'].fillna(median)

    if 'data_usage_gb' in df.columns and df['data_usage_gb'].isna().any():
        median = fe_stats.get('service_type_median_usage', {}).get('Standard', 70)
        df['data_usage_gb'] = df['data_usage_gb'].fillna(median)

    if 'total_charges' in df.columns and df['total_charges'].isna().any():
        df['total_charges'] = df['total_charges'].fillna(
            df['monthly_charges'] * df['tenure_months'].clip(lower=1)
        )

    # Fill other numeric columns with 0
    numeric_cols = ['tenure_months', 'num_services', 'support_calls',
                    'late_payment_count', 'referral_count']
    for col in numeric_cols:
        if col in df.columns:
            df[col] = df[col].fillna(0)

    # Fix negative values
    if 'tenure_months' in df.columns:
        df['tenure_months'] = df['tenure_months'].clip(lower=0)
    if 'support_calls' in df.columns:
        df['support_calls'] = df['support_calls'].clip(lower=0)

    return df


def detect_anomalies(df):
    """Detect charge anomalies."""
    df = df.copy()
    df['charges_anomaly_flag'] = 0

    if 'total_charges' in df.columns and 'monthly_charges' in df.columns:
        df.loc[df['total_charges'] < df['monthly_charges'], 'charges_anomaly_flag'] = 1

    return df


def engineer_features(df, fe):
    """Apply feature engineering using fitted transformer."""
    df = df.copy()

    # Tenure features
    df['tenure_bin'] = pd.cut(
        df['tenure_months'],
        bins=[-np.inf, 5, 12, 24, np.inf],
        labels=[0, 1, 2, 3]
    ).astype(int)
    df['is_new_customer'] = (df['tenure_months'] < 6).astype(int)
    df['is_established'] = (df['tenure_months'] > 24).astype(int)
    df['tenure_log'] = np.log1p(df['tenure_months'])

    # Financial features
    df['avg_monthly_revenue'] = df['total_charges'] / np.maximum(df['tenure_months'], 1)
    df['is_high_value'] = (df['monthly_charges'] > fe.stats['monthly_charges_p75']).astype(int)

    # Price sensitivity
    df['price_sensitivity'] = df.apply(
        lambda row: row['monthly_charges'] / fe.stats['service_type_median_charges'].get(
            row['service_type'], row['monthly_charges']
        ),
        axis=1
    )
    df['monthly_charges_log'] = np.log(df['monthly_charges'].clip(lower=1))

    # Behavioral features
    df['support_intensity'] = df['support_calls'] / np.maximum(df['tenure_months'], 1)
    df['is_heavy_support'] = (df['support_calls'] > 5).astype(int)
    df['late_payment_flag'] = (df['late_payment_count'] > 0).astype(int)
    df['financial_stress'] = pd.cut(
        df['late_payment_count'],
        bins=[-np.inf, 0, 2, np.inf],
        labels=[0, 1, 2]
    ).astype(int)
    df['usage_efficiency'] = df['data_usage_gb'] / (df['num_services'] + 1)
    df['usage_tier_ratio'] = df.apply(
        lambda row: row['data_usage_gb'] / fe.stats['service_type_median_usage'].get(
            row['service_type'], max(row['data_usage_gb'], 1)
        ),
        axis=1
    )

    # Engagement features
    df['autopay_binary'] = (df['autopay_enabled'] == 'Yes').astype(int)
    df['referral_flag'] = (df['referral_count'] > 0).astype(int)
    df['loyalty_score'] = df['referral_count'] + df['is_established'] + df['autopay_binary']

    # Contract features
    contract_risk_map = {'Month-to-Month': 2, 'One Year': 1, 'Two Year': 0}
    df['contract_risk'] = df['contract_type'].map(contract_risk_map)
    df['contract_tenure_mismatch'] = (
        (df['contract_type'] == 'Month-to-Month') & (df['tenure_months'] > 12)
    ).astype(int)
    df['payment_friction'] = (
        (df['payment_method'] == 'Cash') & (df['autopay_enabled'] == 'No')
    ).astype(int)
    df['is_mpesa'] = (df['payment_method'] == 'M-Pesa').astype(int)

    # Interaction features
    df['high_value_mtm'] = (
        (df['is_high_value'] == 1) & (df['contract_type'] == 'Month-to-Month')
    ).astype(int)
    df['new_no_autopay'] = (
        (df['is_new_customer'] == 1) & (df['autopay_binary'] == 0)
    ).astype(int)
    df['support_late_combo'] = (
        (df['support_calls'] > 3) & (df['late_payment_count'] > 1)
    ).astype(int)
    df['premium_low_usage'] = (
        (df['service_type'] == 'Premium') & (df['data_usage_gb'] < fe.stats['data_usage_p25'])
    ).astype(int)
    df['bundled_loyal'] = (
        (df['num_services'] >= 3) & (df['tenure_months'] > 12)
    ).astype(int)

    # Categorical encoding
    service_map = {'Basic': 0, 'Standard': 1, 'Premium': 2}
    df['service_encoded'] = df['service_type'].map(service_map)
    df['pay_bank'] = (df['payment_method'] == 'Bank Transfer').astype(int)
    df['pay_credit'] = (df['payment_method'] == 'Credit Card').astype(int)
    df['pay_debit'] = (df['payment_method'] == 'Debit Card').astype(int)
    df['pay_cash'] = (df['payment_method'] == 'Cash').astype(int)
    df['loc_suburban'] = (df['location_type'] == 'Suburban').astype(int)
    df['loc_rural'] = (df['location_type'] == 'Rural').astype(int)

    return df


# =============================================================================
# PREDICTION FUNCTIONS
# =============================================================================
def predict_churn(df, models, fe, model_type='xgboost'):
    """Generate churn predictions."""
    # Preprocess
    df_clean = standardize_categoricals(df)
    df_clean = handle_missing_values(df_clean, fe.stats)
    df_clean = detect_anomalies(df_clean)
    df_features = engineer_features(df_clean, fe)

    if model_type == 'xgboost':
        X = df_features[XGBOOST_FEATURE_SET]
        model = models['xgboost']['model']
        proba = model.predict_proba(X)[:, 1]
    else:
        X = df_features[LR_FEATURE_SET]
        scaler = models['logistic_regression']['scaler']
        X_scaled = scaler.transform(X)
        model = models['logistic_regression']['model']
        proba = model.predict_proba(X_scaled)[:, 1]

    return proba, df_features


def get_risk_level(proba):
    """Classify risk level based on probability."""
    if proba > HIGH_RISK_THRESHOLD:
        return 'HIGH', '#FF4B4B'
    elif proba > MEDIUM_RISK_THRESHOLD:
        return 'MEDIUM', '#FFA500'
    else:
        return 'LOW', '#00CC66'


def get_recommendations(customer_data, churn_proba):
    """Generate personalized business recommendations."""
    recommendations = []

    # High probability - urgent
    if churn_proba > HIGH_RISK_THRESHOLD:
        recommendations.append({
            'priority': 'URGENT',
            'action': 'Schedule immediate retention call',
            'impact': 'Direct intervention for high-risk customer'
        })

    # Contract-based
    if customer_data.get('contract_type') == 'Month-to-Month':
        recommendations.append({
            'priority': 'HIGH',
            'action': 'Offer 12-month contract with 15% discount',
            'impact': 'Reduces churn odds by ~75%'
        })

    # Tenure-based
    if customer_data.get('tenure_months', 12) < 6:
        recommendations.append({
            'priority': 'HIGH',
            'action': 'Assign dedicated onboarding specialist',
            'impact': 'New customers have +25% churn risk'
        })

    # Payment-based
    if customer_data.get('autopay_enabled') == 'No':
        recommendations.append({
            'priority': 'MEDIUM',
            'action': 'Enable autopay with KES 500 credit incentive',
            'impact': 'Reduces churn odds by ~8%'
        })

    # Support-based
    if customer_data.get('support_calls', 0) > 3:
        recommendations.append({
            'priority': 'HIGH',
            'action': 'Escalate to customer success manager',
            'impact': 'Heavy support users have +15% churn risk'
        })

    # Value-based
    if customer_data.get('monthly_charges', 0) > 6200:
        recommendations.append({
            'priority': 'HIGH',
            'action': 'VIP retention call + loyalty reward program',
            'impact': 'High-value customers need special attention'
        })

    # Late payments
    if customer_data.get('late_payment_count', 0) > 2:
        recommendations.append({
            'priority': 'MEDIUM',
            'action': 'Offer flexible payment plan',
            'impact': 'Financial stress increases churn risk'
        })

    return recommendations


def get_top_drivers(customer_data, df_features, coef_df):
    """Get top churn drivers for a specific customer."""
    drivers = []

    # Check each feature's contribution
    if customer_data.get('contract_type') == 'Month-to-Month':
        drivers.append(('Month-to-Month Contract', 'HIGH', '+75% churn odds'))

    if customer_data.get('tenure_months', 12) < 6:
        drivers.append(('New Customer (<6 months)', 'HIGH', '+25% churn odds'))

    if customer_data.get('monthly_charges', 0) > 6200:
        drivers.append(('High-Value Customer', 'MEDIUM', '+27% churn odds'))

    if customer_data.get('support_calls', 0) > 3:
        drivers.append(('High Support Usage', 'MEDIUM', '+14% churn odds'))

    if customer_data.get('late_payment_count', 0) > 0:
        drivers.append(('Late Payments', 'MEDIUM', '+16% churn odds'))

    if customer_data.get('autopay_enabled') == 'No':
        drivers.append(('No Autopay', 'LOW', '+8% churn odds'))

    # Positive factors (reduce churn)
    if customer_data.get('tenure_months', 0) > 24:
        drivers.append(('Established Customer', 'POSITIVE', '-8% churn odds'))

    if customer_data.get('referral_count', 0) > 0:
        drivers.append(('Has Made Referrals', 'POSITIVE', '-15% churn odds'))

    return drivers[:6]  # Return top 6


# =============================================================================
# PDF REPORT GENERATION
# =============================================================================
def generate_pdf_report(customer_data, churn_proba, recommendations, drivers):
    """Generate PDF report using ReportLab."""
    if not REPORTLAB_AVAILABLE:
        return None

    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4,
                            rightMargin=50, leftMargin=50,
                            topMargin=50, bottomMargin=50)

    styles = getSampleStyleSheet()
    story = []

    # Title
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        spaceAfter=30,
        alignment=TA_CENTER,
        textColor=colors.HexColor('#007BFF')
    )
    story.append(Paragraph("Seven24 Churn Risk Report", title_style))
    story.append(Paragraph("Statistics Expert-Powered Analytics", styles['Normal']))
    story.append(Spacer(1, 20))

    # Date
    story.append(Paragraph(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}", styles['Normal']))
    story.append(Spacer(1, 20))

    # Customer Summary
    story.append(Paragraph("Customer Summary", styles['Heading2']))
    customer_table_data = [
        ['Customer ID', str(customer_data.get('customer_id', 'N/A'))],
        ['Tenure', f"{customer_data.get('tenure_months', 0)} months"],
        ['Contract Type', str(customer_data.get('contract_type', 'N/A'))],
        ['Service Type', str(customer_data.get('service_type', 'N/A'))],
        ['Monthly Charges', f"KES {customer_data.get('monthly_charges', 0):,.0f}"],
        ['Location', str(customer_data.get('location_type', 'N/A'))],
    ]
    customer_table = Table(customer_table_data, colWidths=[2*inch, 3*inch])
    customer_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#F0F0F0')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
    ]))
    story.append(customer_table)
    story.append(Spacer(1, 20))

    # Risk Assessment
    story.append(Paragraph("Risk Assessment", styles['Heading2']))
    risk_level, risk_color = get_risk_level(churn_proba)

    risk_style = ParagraphStyle(
        'RiskLevel',
        parent=styles['Heading1'],
        fontSize=36,
        alignment=TA_CENTER,
        textColor=colors.HexColor(risk_color)
    )
    story.append(Paragraph(f"{churn_proba:.1%}", risk_style))
    story.append(Paragraph(f"Risk Level: {risk_level}", styles['Normal']))
    story.append(Spacer(1, 20))

    # Top Drivers
    if drivers:
        story.append(Paragraph("Top Churn Drivers", styles['Heading2']))
        driver_data = [['Factor', 'Priority', 'Impact']]
        for factor, priority, impact in drivers:
            driver_data.append([factor, priority, impact])

        driver_table = Table(driver_data, colWidths=[2.5*inch, 1*inch, 1.5*inch])
        driver_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#007BFF')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ]))
        story.append(driver_table)
        story.append(Spacer(1, 20))

    # Recommendations
    if recommendations:
        story.append(Paragraph("Recommended Actions", styles['Heading2']))
        for i, rec in enumerate(recommendations, 1):
            story.append(Paragraph(
                f"<b>{i}. [{rec['priority']}]</b> {rec['action']}",
                styles['Normal']
            ))
            story.append(Paragraph(f"   Impact: {rec['impact']}", styles['Normal']))
            story.append(Spacer(1, 8))

    # Footer
    story.append(Spacer(1, 30))
    footer_style = ParagraphStyle(
        'Footer',
        parent=styles['Normal'],
        fontSize=8,
        textColor=colors.grey,
        alignment=TA_CENTER
    )
    story.append(Paragraph(
        "This report was generated by Seven24 Churn Analytics. "
        "For questions, contact ondibahezron@gmail.com",
        footer_style
    ))

    doc.build(story)
    buffer.seek(0)
    return buffer


# =============================================================================
# VISUALIZATION FUNCTIONS
# =============================================================================
def create_risk_gauge(probability):
    """Create a risk gauge visualization."""
    risk_level, color = get_risk_level(probability)

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=probability * 100,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Churn Risk Score", 'font': {'size': 20}},
        number={'suffix': "%", 'font': {'size': 40}},
        gauge={
            'axis': {'range': [0, 100], 'tickwidth': 1},
            'bar': {'color': color},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "gray",
            'steps': [
                {'range': [0, 35], 'color': '#E8F5E9'},
                {'range': [35, 50], 'color': '#FFF3E0'},
                {'range': [50, 100], 'color': '#FFEBEE'}
            ],
            'threshold': {
                'line': {'color': "black", 'width': 4},
                'thickness': 0.75,
                'value': probability * 100
            }
        }
    ))

    fig.update_layout(
        height=300,
        margin=dict(l=20, r=20, t=50, b=20)
    )

    return fig


def create_risk_distribution(df_results):
    """Create risk distribution pie chart."""
    risk_counts = df_results['risk_level'].value_counts()

    colors_map = {'HIGH': '#FF4B4B', 'MEDIUM': '#FFA500', 'LOW': '#00CC66'}
    colors_list = [colors_map.get(level, '#808080') for level in risk_counts.index]

    fig = px.pie(
        values=risk_counts.values,
        names=risk_counts.index,
        title='Customer Risk Distribution',
        color_discrete_sequence=colors_list
    )
    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.update_layout(height=350)

    return fig


def create_feature_importance_chart(coef_df):
    """Create feature importance bar chart."""
    if coef_df is None:
        return None

    top_features = coef_df.head(15)

    colors = ['#FF4B4B' if c > 0 else '#00CC66' for c in top_features['coefficient']]

    fig = px.bar(
        top_features,
        x='coefficient',
        y='feature',
        orientation='h',
        title='Top 15 Features by Impact on Churn',
        color=top_features['coefficient'] > 0,
        color_discrete_map={True: '#FF4B4B', False: '#00CC66'}
    )
    fig.update_layout(
        height=500,
        showlegend=False,
        yaxis={'categoryorder': 'total ascending'},
        xaxis_title='Coefficient (positive = increases churn)',
        yaxis_title=''
    )

    return fig


# =============================================================================
# STREAMLIT APP
# =============================================================================
def main():
    # Page config
    st.set_page_config(
        page_title="Seven24 Churn Analytics",
        page_icon="📊",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # Custom CSS
    st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #007BFF;
        margin-bottom: 0;
    }
    .sub-header {
        font-size: 1rem;
        color: #666;
        margin-top: 0;
    }
    .metric-card {
        background-color: #f8f9fa;
        padding: 20px;
        border-radius: 10px;
        border-left: 4px solid #007BFF;
    }
    .risk-high { color: #FF4B4B; font-weight: bold; }
    .risk-medium { color: #FFA500; font-weight: bold; }
    .risk-low { color: #00CC66; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

    # Sidebar
    with st.sidebar:
        st.markdown("### 📊 Seven24")
        st.markdown("*Data & AI for Better Decisions*")
        st.markdown("---")

        # Model selector
        model_type = st.selectbox(
            "Select Model",
            ['XGBoost (Recommended)', 'Logistic Regression (Interpretable)'],
            help="XGBoost has higher accuracy. Logistic Regression provides interpretable coefficients."
        )
        model_key = 'xgboost' if 'XGBoost' in model_type else 'logistic_regression'

        st.markdown("---")

        # File upload
        st.markdown("### 📁 Upload Data")
        uploaded_file = st.file_uploader(
            "Upload customer CSV",
            type=['csv'],
            help="CSV with columns: customer_id, tenure_months, contract_type, etc."
        )

        # Sample data button
        use_sample = st.button("📋 Use Sample Data", use_container_width=True)

        st.markdown("---")

        # Help section
        with st.expander("ℹ️ Help"):
            st.markdown("""
            **Required CSV Columns:**
            - customer_id
            - tenure_months
            - contract_type
            - service_type
            - monthly_charges
            - total_charges
            - payment_method
            - location_type
            - num_services
            - data_usage_gb
            - support_calls
            - autopay_enabled
            - late_payment_count
            - referral_count

            **Risk Levels:**
            - 🔴 HIGH: >50% churn probability
            - 🟡 MEDIUM: 35-50%
            - 🟢 LOW: <35%
            """)

    # Main content
    st.markdown('<p class="main-header">Churn Analytics Dashboard</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Statistics Expert-Powered Customer Retention Insights</p>',
                unsafe_allow_html=True)

    # Load resources
    models = load_models()
    fe = load_feature_engineer()
    coef_df = load_lr_coefficients()

    if models is None or fe is None:
        st.error("⚠️ Required models not found. Please train models first using `python src/modeling.py`")
        return

    # Handle data input
    df = None
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.success(f"✅ Loaded {len(df)} customers from uploaded file")
    elif use_sample:
        df = load_sample_data()
        if df is not None:
            st.success(f"✅ Loaded {len(df)} sample customers")
        else:
            st.warning("Sample data not found")

    # Create tabs
    tab1, tab2, tab3 = st.tabs([
        "🎯 Single Customer",
        "📊 Batch Analysis",
        "💡 Business Insights"
    ])

    # =========================================================================
    # TAB 1: Single Customer Prediction
    # =========================================================================
    with tab1:
        st.markdown("### Individual Customer Risk Assessment")

        if df is not None and len(df) > 0:
            # Customer selector
            customer_ids = df['customer_id'].tolist() if 'customer_id' in df.columns else list(range(len(df)))
            selected_id = st.selectbox("Select Customer", customer_ids)

            # Get customer data
            if 'customer_id' in df.columns:
                customer_row = df[df['customer_id'] == selected_id].iloc[0]
            else:
                customer_row = df.iloc[selected_id]

            customer_data = customer_row.to_dict()

            # Make prediction
            customer_df = pd.DataFrame([customer_data])
            proba, features_df = predict_churn(customer_df, models, fe, model_key)
            churn_prob = proba[0]
            risk_level, risk_color = get_risk_level(churn_prob)

            # Display results
            col1, col2 = st.columns([1, 1])

            with col1:
                # Risk gauge
                fig = create_risk_gauge(churn_prob)
                st.plotly_chart(fig, use_container_width=True)

                # Risk badge
                st.markdown(f"""
                <div style="text-align: center; padding: 10px; background-color: {risk_color}20;
                            border-radius: 10px; border: 2px solid {risk_color};">
                    <h2 style="color: {risk_color}; margin: 0;">⚠️ {risk_level} RISK</h2>
                </div>
                """, unsafe_allow_html=True)

            with col2:
                # Customer info
                st.markdown("#### Customer Profile")
                info_col1, info_col2 = st.columns(2)
                with info_col1:
                    st.metric("Tenure", f"{customer_data.get('tenure_months', 0)} months")
                    st.metric("Contract", customer_data.get('contract_type', 'N/A'))
                    st.metric("Service", customer_data.get('service_type', 'N/A'))
                with info_col2:
                    st.metric("Monthly Charges", f"KES {customer_data.get('monthly_charges', 0):,.0f}")
                    st.metric("Support Calls", customer_data.get('support_calls', 0))
                    st.metric("Late Payments", customer_data.get('late_payment_count', 0))

            # Drivers and recommendations
            st.markdown("---")
            col3, col4 = st.columns([1, 1])

            with col3:
                st.markdown("#### 🔍 Top Churn Drivers")
                drivers = get_top_drivers(customer_data, features_df, coef_df)
                for factor, priority, impact in drivers:
                    if priority == 'POSITIVE':
                        st.markdown(f"✅ **{factor}** - {impact}")
                    elif priority == 'HIGH':
                        st.markdown(f"🔴 **{factor}** - {impact}")
                    elif priority == 'MEDIUM':
                        st.markdown(f"🟡 **{factor}** - {impact}")
                    else:
                        st.markdown(f"🟢 **{factor}** - {impact}")

            with col4:
                st.markdown("#### 💡 Recommended Actions")
                recommendations = get_recommendations(customer_data, churn_prob)
                for rec in recommendations:
                    priority_icon = "🚨" if rec['priority'] == 'URGENT' else "⚡" if rec['priority'] == 'HIGH' else "📌"
                    st.markdown(f"{priority_icon} **{rec['action']}**")
                    st.caption(f"Impact: {rec['impact']}")

            # PDF Download
            st.markdown("---")
            if REPORTLAB_AVAILABLE:
                pdf_buffer = generate_pdf_report(customer_data, churn_prob, recommendations, drivers)
                if pdf_buffer:
                    st.download_button(
                        label="📄 Download PDF Report",
                        data=pdf_buffer,
                        file_name=f"churn_report_{selected_id}_{datetime.now().strftime('%Y%m%d')}.pdf",
                        mime="application/pdf",
                        use_container_width=True
                    )
            else:
                st.info("Install reportlab for PDF export: `pip install reportlab`")

        else:
            st.info("👆 Upload a CSV file or click 'Use Sample Data' to get started")

    # =========================================================================
    # TAB 2: Batch Analysis
    # =========================================================================
    with tab2:
        st.markdown("### Batch Customer Analysis")

        if df is not None and len(df) > 0:
            with st.spinner("Analyzing customers..."):
                # Predict for all customers
                probas, features_df = predict_churn(df, models, fe, model_key)

                # Create results dataframe
                df_results = df.copy()
                df_results['churn_probability'] = probas
                df_results['risk_level'] = df_results['churn_probability'].apply(
                    lambda p: 'HIGH' if p > HIGH_RISK_THRESHOLD else 'MEDIUM' if p > MEDIUM_RISK_THRESHOLD else 'LOW'
                )

            # Summary metrics
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Total Customers", len(df_results))
            with col2:
                high_risk = (df_results['risk_level'] == 'HIGH').sum()
                st.metric("High Risk", high_risk, delta=f"{high_risk/len(df_results)*100:.1f}%")
            with col3:
                medium_risk = (df_results['risk_level'] == 'MEDIUM').sum()
                st.metric("Medium Risk", medium_risk)
            with col4:
                avg_prob = df_results['churn_probability'].mean()
                st.metric("Avg. Churn Prob", f"{avg_prob:.1%}")

            # Charts
            st.markdown("---")
            chart_col1, chart_col2 = st.columns(2)

            with chart_col1:
                fig = create_risk_distribution(df_results)
                st.plotly_chart(fig, use_container_width=True)

            with chart_col2:
                # Risk by contract type
                risk_by_contract = df_results.groupby('contract_type')['churn_probability'].mean()
                fig = px.bar(
                    x=risk_by_contract.index,
                    y=risk_by_contract.values,
                    title='Average Churn Risk by Contract Type',
                    labels={'x': 'Contract Type', 'y': 'Avg. Churn Probability'}
                )
                fig.update_traces(marker_color=['#FF4B4B' if v > 0.3 else '#00CC66' for v in risk_by_contract.values])
                st.plotly_chart(fig, use_container_width=True)

            # Results table
            st.markdown("---")
            st.markdown("#### 📋 Customer Risk Table")

            # Filter
            risk_filter = st.multiselect(
                "Filter by Risk Level",
                ['HIGH', 'MEDIUM', 'LOW'],
                default=['HIGH', 'MEDIUM', 'LOW']
            )

            filtered_df = df_results[df_results['risk_level'].isin(risk_filter)]

            # Display columns
            display_cols = ['customer_id', 'churn_probability', 'risk_level',
                           'contract_type', 'tenure_months', 'monthly_charges']
            display_cols = [c for c in display_cols if c in filtered_df.columns]

            st.dataframe(
                filtered_df[display_cols].sort_values('churn_probability', ascending=False),
                use_container_width=True,
                height=400
            )

            # Export
            csv = filtered_df.to_csv(index=False)
            st.download_button(
                label="📥 Download Results CSV",
                data=csv,
                file_name=f"churn_analysis_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv"
            )

        else:
            st.info("👆 Upload a CSV file or click 'Use Sample Data' to analyze")

    # =========================================================================
    # TAB 3: Business Insights
    # =========================================================================
    with tab3:
        st.markdown("### Model Insights & Feature Importance")

        # Feature importance
        if coef_df is not None:
            st.markdown("#### 📊 Feature Impact on Churn (Logistic Regression)")
            fig = create_feature_importance_chart(coef_df)
            if fig:
                st.plotly_chart(fig, use_container_width=True)

            st.markdown("""
            **Interpretation:**
            - 🔴 **Red bars** = Features that INCREASE churn risk
            - 🟢 **Green bars** = Features that DECREASE churn risk
            - Longer bars = Stronger impact on prediction
            """)

        # Model comparison
        st.markdown("---")
        st.markdown("#### 🔬 Model Performance Comparison")

        try:
            with open(MODELS_PATH / 'model_results.json', 'r') as f:
                results = json.load(f)

            metrics_df = pd.DataFrame(results['metrics']).T
            metrics_df.index = ['Logistic Regression', 'XGBoost']

            col1, col2 = st.columns(2)
            with col1:
                st.dataframe(metrics_df.style.format("{:.4f}"), use_container_width=True)

            with col2:
                fig = px.bar(
                    metrics_df.reset_index().melt(id_vars='index'),
                    x='variable', y='value', color='index',
                    barmode='group',
                    title='Model Metrics Comparison',
                    labels={'variable': 'Metric', 'value': 'Score', 'index': 'Model'}
                )
                st.plotly_chart(fig, use_container_width=True)

        except FileNotFoundError:
            st.info("Model results not found. Run modeling.py first.")

        # Key insights
        st.markdown("---")
        st.markdown("#### 🎯 Key Business Insights")

        insights_col1, insights_col2 = st.columns(2)

        with insights_col1:
            st.markdown("""
            **Top Churn Drivers:**
            1. **Month-to-Month contracts** (+75% churn odds)
            2. **New customers** (<6 months tenure, +25%)
            3. **High-value customers** (>75th percentile, +27%)
            4. **Support intensity** (+14% per call)
            5. **Late payments** (+16% per occurrence)
            """)

        with insights_col2:
            st.markdown("""
            **Retention Levers:**
            1. **Contract upgrades** (Two Year = -75% churn)
            2. **Loyalty programs** (referrals = -15%)
            3. **Autopay enrollment** (-8% churn)
            4. **Early onboarding** (first 6 months critical)
            5. **Proactive support** (reduce escalations)
            """)


if __name__ == "__main__":
    main()
