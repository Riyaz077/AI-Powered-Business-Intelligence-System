
import os
from pathlib import Path

import pandas as pd
import streamlit as st

from src.analytics import analyze_dataset, load_dataset, generate_demo_data


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="Intellix AI | Business Intelligence",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Intellix AI")
st.subheader("AI-Powered Business Intelligence System")

st.markdown(
    "Transform business data into actionable insights through "
    "analytics, machine learning and intelligent recommendations."
)

# --------------------------------------------------
# DIRECTORIES
# --------------------------------------------------

DATA_DIR = Path("data")
UPLOAD_DIR = DATA_DIR / "uploads"

DATA_DIR.mkdir(exist_ok=True)
UPLOAD_DIR.mkdir(exist_ok=True)

DEMO_PATH = DATA_DIR / "demo_business_data.csv"


# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

st.sidebar.title("Intellix AI")
st.sidebar.caption("Business Intelligence Platform")

page = st.sidebar.radio(
    "Navigation",
    [
        "Dashboard",
        "Upload Dataset",
        "About"
    ]
)


# --------------------------------------------------
# ANALYTICS FUNCTION
# --------------------------------------------------

def display_analysis(path, filename):

    try:
        df = load_dataset(str(path))
        result = analyze_dataset(df)

        st.success(f"Successfully analyzed: {filename}")

        # Dataset overview
        st.markdown("### Dataset Overview")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Total Rows", f"{len(df):,}")

        with col2:
            st.metric("Total Columns", f"{len(df.columns):,}")

        with col3:
            st.metric("Missing Values", f"{df.isna().sum().sum():,}")

        st.markdown("### Dataset Preview")
        st.dataframe(df.head(10), use_container_width=True)

        st.markdown("### Analytics Results")

        if isinstance(result, pd.DataFrame):
            st.dataframe(result, use_container_width=True)

        elif isinstance(result, dict):
            for key, value in result.items():
                st.markdown(f"#### {str(key).replace('_', ' ').title()}")

                if isinstance(value, pd.DataFrame):
                    st.dataframe(value, use_container_width=True)
                elif isinstance(value, (dict, list)):
                    st.json(value)
                else:
                    st.write(value)

        else:
            st.write(result)

        st.download_button(
            label="Download Dataset",
            data=Path(path).read_bytes(),
            file_name=filename,
            mime="text/csv"
        )

    except Exception as exc:
        st.error(f"Unable to analyze the dataset: {exc}")


# --------------------------------------------------
# DASHBOARD
# --------------------------------------------------

if page == "Dashboard":

    st.markdown("## Business Intelligence Dashboard")

    st.write(
        "Explore the sample business dataset and discover "
        "meaningful patterns through automated analytics."
    )

    if st.button("Generate Demo Analysis", type="primary"):

        with st.spinner("Generating demo dataset and analyzing data..."):

            if not DEMO_PATH.exists():
                generate_demo_data(str(DEMO_PATH))

            st.session_state["analyze_demo"] = True

    if st.session_state.get("analyze_demo", False):

        if DEMO_PATH.exists():
            display_analysis(
                DEMO_PATH,
                "demo_business_data.csv"
            )

    if DEMO_PATH.exists():

        st.download_button(
            label="Download Demo Dataset",
            data=DEMO_PATH.read_bytes(),
            file_name="demo_business_data.csv",
            mime="text/csv"
        )


# --------------------------------------------------
# UPLOAD DATASET
# --------------------------------------------------

elif page == "Upload Dataset":

    st.markdown("## Upload Your Business Dataset")

    uploaded_file = st.file_uploader(
        "Choose a CSV file",
        type=["csv"]
    )

    if uploaded_file is not None:

        if st.button("Analyze Dataset", type="primary"):

            filename = Path(uploaded_file.name).name
            file_path = UPLOAD_DIR / filename

            file_path.write_bytes(uploaded_file.getvalue())

            with st.spinner("Analyzing your business dataset..."):

                display_analysis(file_path, filename)


# --------------------------------------------------
# ABOUT
# --------------------------------------------------

elif page == "About":

    st.markdown("## About Intellix AI")

    st.write(
        """
        Intellix AI is an intelligent business analytics platform
        designed to transform raw datasets into meaningful insights.

        **Core capabilities:**
        - Business dataset analysis
        - CSV upload and processing
        - Automated analytics
        - Dataset exploration
        - Intelligent business insights
        """
    )

    st.info(
        "Powered by Python, Pandas, Scikit-learn and Streamlit."
    )
