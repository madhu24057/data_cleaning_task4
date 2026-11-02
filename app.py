import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# 1. Page Configuration
st.set_page_config(
    page_title="Data Cleaning & Reporting Automation",
    page_icon="🧹",
    layout="wide"
)

# 2. Custom Light Theme CSS & Toolbar Styling
st.markdown("""
    <style>
    .stApp {
        background-color: #f8fafc;
        color: #0f172a !important;
    }
    h1, h2, h3, h4, h5, h6, p, span, label, .stMarkdown {
        color: #0f172a !important;
    }
    .metric-card {
        background: linear-gradient(135deg, #ffffff 0%, #f1f5f9 100%);
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
        border: 1px solid #cbd5e1;
        text-align: center;
        margin-bottom: 10px;
    }
    .metric-title {
        color: #64748b !important;
        font-size: 14px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 8px;
    }
    .metric-value {
        color: #0f172a !important;
        font-size: 26px;
        font-weight: 700;
    }
    .stTabs [data-baseweb="tab-list"] { gap: 8px; }
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        padding: 10px 20px;
        background-color: #f1f5f9;
        border: 1px solid #cbd5e1;
        color: #334155 !important;
    }
    .stTabs [aria-selected="true"] {
        background-color: #2563eb !important;
        color: #ffffff !important;
        border-color: #2563eb !important;
    }
    [data-testid="stDataFrame"] {
        background-color: #ffffff;
        border: 1px solid #cbd5e1;
        border-radius: 8px;
        padding: 5px;
    }
    </style>
""", unsafe_allow_html=True)

# 3. Header Section
st.markdown("""
    <div style="background: linear-gradient(90deg, #e0e7ff 0%, #dbeafe 100%); padding: 25px; border-radius: 12px; color: #0f172a; margin-bottom: 25px; border: 1px solid #cbd5e1;">
        <h1 style="margin:0; font-size: 32px; color: #0f172a !important;">🧹 Data Cleaning & Reporting Automation</h1>
        <p style="margin-top: 8px; margin-bottom: 0; font-size: 16px; color: #334155 !important;">
            Automated workflow for anomaly detection, missing value imputation, duplicate removal, and visual summary reporting.
        </p>
    </div>
""", unsafe_allow_html=True)

# 4. Load Dataset Safely
@st.cache_data
def load_data():
    try:
        return pd.read_csv("messy_data.csv")
    except Exception as e:
        return None

raw_df = load_data()

if raw_df is None:
    st.error("⚠️ 'messy_data.csv' not found. Please ensure the CSV file is in your project directory.")
    st.stop()

# 5. Automated Data Cleaning Pipeline Function
def clean_dataset(df):
    cleaned = df.copy()
    
    # Remove duplicate rows
    cleaned = cleaned.drop_duplicates()
    
    # Clean string columns (strip whitespace, standardize title/lower casing)
    for col in cleaned.select_dtypes(include=['object']).columns:
        if col != 'Date':
            cleaned[col] = cleaned[col].astype(str).str.strip().str.title()
            
    # Handle missing values for numerical columns (fill with median)
    for col in cleaned.select_dtypes(include=[np.number]).columns:
        cleaned[col] = cleaned[col].fillna(cleaned[col].median())
        
    # Handle missing values for categorical/string columns (fill with 'Unknown')
    for col in cleaned.select_dtypes(include=['object']).columns:
        cleaned[col] = cleaned[col].fillna('Unknown')
        
    return cleaned

cleaned_df = clean_dataset(raw_df)

# 6. Executive Diagnostics Metrics
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">Raw Records</div>
            <div class="metric-value" style="color: #2563eb !important;">{len(raw_df)}</div>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">Cleaned Records</div>
            <div class="metric-value" style="color: #059669 !important;">{len(cleaned_df)}</div>
        </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">Duplicates Removed</div>
            <div class="metric-value" style="color: #dc2626 !important;">{len(raw_df) - len(cleaned_df)}</div>
        </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">Missing Values Fixed</div>
            <div class="metric-value" style="color: #d97706 !important;">{raw_df.isnull().sum().sum()}</div>
        </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# 7. Tabbed Automated Reporting Interface
tab1, tab2, tab3 = st.tabs(["📊 Automated Visual Summary", "📋 Data Comparison Viewer", "📥 Export Clean Report"])

with tab1:
    st.subheader("Automated Operational Summary")
    
    col_a, col_b = st.columns(2)
    
    with col_a:
        if 'Region' in cleaned_df.columns and 'Sales' in cleaned_df.columns:
            fig_region = px.bar(
                cleaned_df, x='Region', y='Sales', color='Region',
                title="Sales Distribution by Region", template="plotly_white"
            )
            fig_region.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig_region, use_container_width=True)
            
    with col_b:
        if 'Status' in cleaned_df.columns:
            status_counts = cleaned_df['Status'].value_counts().reset_index()
            status_counts.columns = ['Status', 'Count']
            fig_status = px.pie(
                status_counts, names='Status', values='Count',
                title="Customer Status Proportions", template="plotly_white", hole=0.4
            )
            fig_status.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig_status, use_container_width=True)

with tab2:
    col_t1, col_t2 = st.columns(2)
    with col_t1:
        st.subheader("Raw Dataset (Before Cleaning)")
        st.dataframe(raw_df, use_container_width=True)
    with col_t2:
        st.subheader("Automated Cleaned Dataset")
        st.dataframe(cleaned_df, use_container_width=True)

with tab3:
    st.subheader("Download Automated Report")
    st.markdown("Export your sanitized dataset ready for downstream analysis and reporting pipelines.")
    
    csv_data = cleaned_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download Cleaned CSV Report",
        data=csv_data,
        file_name="automated_cleaned_report.csv",
        mime="text/csv",
    )