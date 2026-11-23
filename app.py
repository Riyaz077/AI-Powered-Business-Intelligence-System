from __future__ import annotations

import io
from pathlib import Path
import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

from src.analytics import (
    profile_dataset, prepare_regression, evaluate_regression,
    detect_anomalies, build_recommendations, format_number
)

st.set_page_config(
    page_title="IntelliX | Business Intelligence",
    page_icon="assets/favicon.png",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------- Visual system ----------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@400;500;600;700;800&display=swap');
:root { --bg:#080d18; --panel:#101827; --panel2:#141f31; --line:rgba(148,163,184,.15);
        --muted:#8b9bb2; --text:#edf3fc; --cyan:#56d7e8; --violet:#9b8cff; }
html, body, [class*="css"] { font-family:'DM Sans',sans-serif; }
.stApp { background: radial-gradient(ellipse at 82% 0%, rgba(48,75,130,.22), transparent 38%), var(--bg); color:var(--text); }
[data-testid="stHeader"] { background:transparent; }
[data-testid="stSidebar"] { background:#0b1220; border-right:1px solid var(--line); }
[data-testid="stSidebar"] * { color:#dbe6f5; }
.block-container { padding-top:2.1rem; padding-bottom:3rem; max-width:1500px; }
h1,h2,h3 { font-family:'Manrope',sans-serif !important; letter-spacing:-.035em; color:#f4f7ff; }
h1 { font-size:2.2rem !important; font-weight:800 !important; }
h2 { font-size:1.35rem !important; font-weight:750 !important; }
h3 { font-size:1.02rem !important; font-weight:700 !important; }
p, label, .stMarkdown { color:#c4d0e0; }
small, .muted { color:var(--muted); }
div[data-testid="stMetric"] { background:linear-gradient(145deg,#141f31,#101827); border:1px solid var(--line);
 border-radius:15px; padding:17px 18px; min-height:112px; }
div[data-testid="stMetricLabel"] { color:#94a6bf; font-size:.78rem; }
div[data-testid="stMetricValue"] { color:#f2f7ff; font-family:'Manrope'; font-weight:800; }
div[data-testid="stMetricDelta"] { font-size:.75rem; }
div[data-testid="stFileUploader"] { background:#111c2c; border:1px dashed #40516c; border-radius:14px; padding:12px; }
.stButton>button, .stDownloadButton>button { border-radius:10px; border:1px solid rgba(86,215,232,.35);
 background:linear-gradient(110deg,#1b879b,#5367bd); color:white; font-weight:700; padding:.55rem 1rem; }
.stButton>button:hover, .stDownloadButton>button:hover { border-color:#72e5f1; color:white; }
div[data-testid="stSelectbox"]>div, div[data-testid="stTextInput"]>div { background:#111c2c; }
hr { border-color:var(--line); }
.hero { background:linear-gradient(115deg,rgba(27,135,155,.19),rgba(83,103,189,.16)),#101827;
 border:1px solid rgba(117,153,207,.2); border-radius:20px; padding:26px 28px; margin-bottom:22px; }
.eyebrow { color:#67dce8; font-size:.72rem; letter-spacing:.18em; text-transform:uppercase; font-weight:800; }
.hero-title { font-family:'Manrope'; font-size:2rem; line-height:1.18; font-weight:800; color:#f5f8ff; margin:.35rem 0 .5rem; }
.hero-sub { color:#aebdd1; max-width:850px; line-height:1.6; }
.section-head { display:flex; align-items:center; justify-content:space-between; margin:1.4rem 0 .75rem; }
.panel { background:linear-gradient(145deg,#131e2e,#0f1827); border:1px solid var(--line); border-radius:16px; padding:18px 20px; }
.pill { display:inline-block; border:1px solid rgba(86,215,232,.3); background:rgba(86,215,232,.08); color:#77e3ee;
 padding:4px 9px; border-radius:30px; font-size:.7rem; font-weight:700; }
.insight { border-left:3px solid #56d7e8; background:#111d2c; padding:12px 15px; border-radius:0 10px 10px 0; margin:.55rem 0; color:#cbd7e7; }
[data-testid="stDataFrame"] { border:1px solid var(--line); border-radius:12px; }
.stTabs [data-baseweb="tab-list"] { gap:8px; }
.stTabs [data-baseweb="tab"] { background:#111c2c; border-radius:8px; padding:8px 14px; }
.stTabs [aria-selected="true"] { background:#1c3448 !important; }
footer { visibility:hidden; }
</style>
""", unsafe_allow_html=True)

def chart_theme(fig, height=340):
    fig.update_layout(
        height=height, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="DM Sans", color="#aebdd1", size=11),
        margin=dict(l=10,r=10,t=35,b=10),
        legend=dict(bgcolor="rgba(0,0,0,0)", orientation="h", y=1.12),
        xaxis=dict(showgrid=False, linecolor="rgba(148,163,184,.15)"),
        yaxis=dict(gridcolor="rgba(148,163,184,.10)", zeroline=False),
    )
    return fig

def money_or_number(v):
    return format_number(v)

def load_demo():
    p = Path(__file__).parent / "data" / "demo_business_data.csv"
    return pd.read_csv(p, parse_dates=["date"])

if "df" not in st.session_state:
    st.session_state.df = load_demo()
    st.session_state.dataset_name = "demo_business_data.csv"
if "analysis_ready" not in st.session_state:
    st.session_state.analysis_ready = True

# ---------- Sidebar ----------
with st.sidebar:
    st.markdown("<div style='padding:8px 4px 22px'><div style='font-size:1.55rem;font-weight:800;font-family:Manrope;color:#f4f8ff'>✦ Intelli<span style='color:#56d7e8'>X</span></div><div style='font-size:.68rem;letter-spacing:.16em;color:#8193ad'>BUSINESS INTELLIGENCE</div></div>", unsafe_allow_html=True)
    page = st.radio("WORKSPACE", ["Executive Overview", "Data Explorer", "Predictive Analytics", "Anomaly Detection", "Decision Support"], label_visibility="visible")
    st.markdown("---")
    st.markdown("**ACTIVE DATASET**")
    st.markdown(f"<div class='panel'><div style='font-weight:700;color:#eef4ff'>{st.session_state.dataset_name}</div><div style='font-size:.76rem;color:#8b9bb2;margin-top:5px'>{len(st.session_state.df):,} records · {st.session_state.df.shape[1]} fields</div></div>", unsafe_allow_html=True)
    uploaded = st.file_uploader("Replace dataset · CSV", type=["csv"], label_visibility="collapsed")
    if uploaded is not None:
        try:
            new_df = pd.read_csv(uploaded)
            if new_df.empty:
                st.error("The uploaded CSV contains no records.")
            else:
                st.session_state.df = new_df
                st.session_state.dataset_name = uploaded.name
                st.session_state.analysis_ready = True
                st.success("Dataset loaded successfully.")
        except Exception as e:
            st.error(f"Could not read CSV: {e}")
    if st.button("↻ Load demo dataset", use_container_width=True):
        st.session_state.df = load_demo()
        st.session_state.dataset_name = "demo_business_data.csv"
        st.rerun()
    st.markdown("---")
    st.caption("INTELLIX ANALYTICS SUITE · v1.0")
    st.caption("Local-first · CSV-powered")

df = st.session_state.df.copy()
profile = profile_dataset(df)
numeric_cols = df.select_dtypes(include=np.number).columns.tolist()
categorical_cols = df.select_dtypes(exclude=np.number).columns.tolist()

# ---------- Header ----------
st.markdown(f"""
<div class="hero">
 <div class="eyebrow">BUSINESS PERFORMANCE INTELLIGENCE / {page.upper()}</div>
 <div class="hero-title">Turn business data into<br><span style="color:#65dce8">decisive action.</span></div>
 <div class="hero-sub">A unified workspace for performance analysis, predictive modelling, anomaly discovery and practical decision support.</div>
</div>
""", unsafe_allow_html=True)

# ---------- Executive Overview ----------
if page == "Executive Overview":
    st.markdown("## Executive snapshot")
    st.caption("A live summary of the currently selected dataset.")
    c1,c2,c3,c4 = st.columns(4)
    c1.metric("Total records", f"{len(df):,}")
    c2.metric("Data fields", f"{df.shape[1]:,}")
    c3.metric("Missing cells", f"{profile['missing_cells']:,}", delta=f"{profile['missing_pct']:.1f}% of dataset", delta_color="inverse")
    c4.metric("Duplicate rows", f"{profile['duplicates']:,}", delta="Review recommended" if profile['duplicates'] else "No duplicates detected", delta_color="off")
    st.markdown("---")
    left,right = st.columns([1.55,1])
    with left:
        st.markdown("### Business metric distribution")
        if numeric_cols:
            metric = st.selectbox("Choose a metric", numeric_cols, key="overview_metric")
            fig = px.histogram(df, x=metric, nbins=28, marginal="box", color_discrete_sequence=["#56d7e8"])
            st.plotly_chart(chart_theme(fig,380), use_container_width=True)
        else:
            st.info("No numeric columns found. Add numeric business measures to unlock metric analysis.")
    with right:
        st.markdown("### Dataset health")
        health = max(0, 100 - profile["missing_pct"] - min(profile["duplicate_pct"], 30))
        fig = go.Figure(go.Indicator(mode="gauge+number", value=health, number={"suffix":"%","font":{"color":"#eef4ff","size":34}},
            title={"text":"Data quality score","font":{"color":"#9fb0c6","size":13}},
            gauge={"axis":{"range":[0,100],"tickcolor":"#8193ad"},"bar":{"color":"#56d7e8"},"bgcolor":"#182438",
                   "borderwidth":0,"steps":[{"range":[0,60],"color":"#2a1e2a"},{"range":[60,85],"color":"#2b2b27"},{"range":[85,100],"color":"#183239"}]}))
        fig.update_layout(height=260,paper_bgcolor="rgba(0,0,0,0)",font={"color":"#aebdd1"},margin=dict(t=35,b=10,l=15,r=15))
        st.plotly_chart(fig,use_container_width=True)
        st.caption("Indicative score based on missing and duplicate records; not a formal certification.")
    st.markdown("### At-a-glance business metrics")
    if numeric_cols:
        cols = st.columns(min(4,len(numeric_cols)))
        for i,col in enumerate(numeric_cols[:4]):
            val = pd.to_numeric(df[col],errors="coerce").sum()
            cols[i].metric(f"{col.replace('_',' ').title()} · total", money_or_number(val))
    st.markdown("### Recent records")
    st.dataframe(df.head(8), use_container_width=True, hide_index=True)
    st.download_button("↓ Download current dataset", df.to_csv(index=False).encode("utf-8"), file_name="business_dataset.csv", mime="text/csv")

# ---------- Data Explorer ----------
elif page == "Data Explorer":
    st.markdown("## Explore your data")
    st.caption("Inspect structure, completeness and relationships before modelling.")
    t1,t2,t3 = st.tabs(["Dataset preview","Data quality","Relationships"])
    with t1:
        st.markdown(f"**{df.shape[0]:,} rows × {df.shape[1]} columns**")
        st.dataframe(df, use_container_width=True, height=430)
        st.download_button("Download cleaned-format CSV",df.to_csv(index=False).encode(), "dataset_export.csv","text/csv")
    with t2:
        q1,q2,q3 = st.columns(3)
        q1.metric("Missing cells",f"{profile['missing_cells']:,}")
        q2.metric("Duplicate rows",f"{profile['duplicates']:,}")
        q3.metric("Completeness",f"{100-profile['missing_pct']:.1f}%")
        quality = pd.DataFrame({"Column":df.columns,"Data type":[str(x) for x in df.dtypes],
            "Missing":[int(df[c].isna().sum()) for c in df.columns],
            "Missing %":[round(df[c].isna().mean()*100,2) for c in df.columns],
            "Unique values":[int(df[c].nunique(dropna=True)) for c in df.columns]})
        st.dataframe(quality,use_container_width=True,hide_index=True)
        if profile["missing_cells"]:
            fig=px.bar(quality.sort_values("Missing",ascending=False),x="Column",y="Missing",color="Missing",color_continuous_scale=["#24485c","#56d7e8"])
            st.plotly_chart(chart_theme(fig,300),use_container_width=True)
        else: st.success("No missing values detected.")
    with t3:
        if len(numeric_cols)>=2:
            corr=df[numeric_cols].corr(numeric_only=True)
            fig=px.imshow(corr,text_auto=".2f",aspect="auto",color_continuous_scale="Tealgrn",zmin=-1,zmax=1)
            st.plotly_chart(chart_theme(fig,480),use_container_width=True)
        else: st.info("At least two numeric columns are needed for a correlation matrix.")

# ---------- Predictive Analytics ----------
elif page == "Predictive Analytics":
    st.markdown("## Predictive analytics")
    st.caption("Train a transparent Random Forest regression baseline on a selected numeric outcome.")
    if len(numeric_cols)<2:
        st.warning("At least two numeric columns are required: one target and at least one feature.")
    else:
        default_target = next((c for c in ["sales","revenue","profit","quantity","units","amount","orders"] if c in numeric_cols),numeric_cols[-1])
        target=st.selectbox("Prediction target",numeric_cols,index=numeric_cols.index(default_target))
        test_size=st.slider("Test set proportion",0.15,0.40,0.20,0.05)
        n_estimators=st.select_slider("Random Forest trees",options=[100,150,200,300,400],value=200)
        if st.button("Train baseline model",type="primary"):
            with st.spinner("Preparing data and training model..."):
                try:
                    X_train,X_test,y_train,y_test,feature_names=prepare_regression(df,target,test_size)
                    result=evaluate_regression(X_train,X_test,y_train,y_test,n_estimators)
                    st.session_state.model_result=result
                    st.session_state.model_target=target
                except Exception as e:
                    st.error(f"Model could not be trained: {e}")
        if "model_result" in st.session_state and st.session_state.get("model_target")==target:
            r=st.session_state.model_result
            st.markdown("---")
            a,b,c=st.columns(3)
            a.metric("Mean Absolute Error",format_number(r["mae"]))
            b.metric("Root Mean Squared Error",format_number(r["rmse"]))
            c.metric("R² score",f"{r['r2']:.3f}" if np.isfinite(r["r2"]) else "N/A")
            actual=pd.DataFrame({"Actual":r["y_test"],"Predicted":r["predictions"]})
            fig=px.scatter(actual,x="Actual",y="Predicted",opacity=.75,color_discrete_sequence=["#56d7e8"])
            lo=min(actual.min()); hi=max(actual.max())
            fig.add_shape(type="line",x0=lo,y0=lo,x1=hi,y1=hi,line=dict(color="#9b8cff",dash="dash"))
            st.markdown("### Actual vs predicted")
            st.plotly_chart(chart_theme(fig,380),use_container_width=True)
            if r["importance"] is not None:
                st.markdown("### Feature importance")
                imp=r["importance"].sort_values("Importance",ascending=True)
                fig=px.bar(imp,x="Importance",y="Feature",orientation="h",color="Importance",color_continuous_scale=["#385b82","#56d7e8"])
                st.plotly_chart(chart_theme(fig,350),use_container_width=True)
            st.caption("Baseline model uses a random train/test split and median imputation. It is not a time-series forecasting model.")
        else:
            st.info("Choose a target and train the model to view evaluation metrics and feature importance.")

# ---------- Anomaly Detection ----------
elif page == "Anomaly Detection":
    st.markdown("## Anomaly detection")
    st.caption("Surface unusual rows for investigation using Isolation Forest.")
    if len(numeric_cols)<1:
        st.warning("No numeric columns are available for anomaly detection.")
    else:
        selected=st.multiselect("Analysis features",numeric_cols,default=numeric_cols[:min(5,len(numeric_cols))])
        contamination=st.slider("Expected anomaly fraction",0.01,0.20,0.05,0.01)
        if st.button("Detect unusual observations",type="primary"):
            try:
                result=detect_anomalies(df,selected,contamination)
                st.session_state.anomaly_result=result
            except Exception as e: st.error(str(e))
        if "anomaly_result" in st.session_state:
            out=st.session_state.anomaly_result
            x,y,z=st.columns(3)
            x.metric("Rows analysed",f"{len(out):,}")
            y.metric("Flagged observations",f"{int((out['Anomaly']=='Anomaly').sum()):,}")
            z.metric("Flag rate",f"{(out['Anomaly']=='Anomaly').mean()*100:.1f}%")
            st.dataframe(out[out["Anomaly"]=="Anomaly"],use_container_width=True,hide_index=True)
            st.download_button("Download anomaly results",out.to_csv(index=False).encode(),"anomaly_results.csv","text/csv")
            st.caption("An anomaly is statistically unusual; it is not automatically an error, fraud, or negative outcome.")

# ---------- Decision Support ----------
elif page == "Decision Support":
    st.markdown("## Decision support")
    st.caption("Translate data-quality signals and descriptive patterns into review prompts.")
    recommendations=build_recommendations(df)
    if recommendations:
        for item in recommendations:
            st.markdown(f"<div class='insight'><b>{item['title']}</b><br><span style='color:#aebdd1'>{item['detail']}</span></div>",unsafe_allow_html=True)
    else:
        st.success("No major rule-based review prompts were triggered by the current dataset.")
    st.markdown("### Key numeric indicators")
    if numeric_cols:
        chosen=st.selectbox("Business indicator",numeric_cols)
        s=pd.to_numeric(df[chosen],errors="coerce").dropna()
        if len(s):
            a,b,c,d=st.columns(4)
            a.metric("Average",format_number(s.mean()))
            b.metric("Median",format_number(s.median()))
            c.metric("Minimum",format_number(s.min()))
            d.metric("Maximum",format_number(s.max()))
            fig=px.line(x=np.arange(len(s)),y=s.values,labels={"x":"Record index","y":chosen},color_discrete_sequence=["#56d7e8"])
            st.plotly_chart(chart_theme(fig,320),use_container_width=True)
    st.info("Recommendations are generated from predefined rules. Validate them against business context before acting.")

# ================= DEVELOPER FOOTER =================

st.html("""
<style>
.developer-footer {
    background: linear-gradient(145deg, #0b1b2c, #071525);
    border: 1px solid rgba(56,189,248,0.22);
    border-radius: 20px;
    padding: 38px 25px 25px;
    margin-top: 65px;
    text-align: center;
    position: relative;
}

.developer-footer:before {
    content: "";
    position: absolute;
    top: 0;
    left: 12%;
    width: 76%;
    height: 3px;
    background: linear-gradient(
        90deg, transparent, #06d6f5, #647cff, transparent
    );
}

.footer-project-title {
    color: #20d9f5;
    font-size: 19px;
    font-weight: 750;
    margin-bottom: 34px;
}

.footer-label {
    color: #8eb9e8;
    font-size: 15px;
    margin-bottom: 18px;
}

.footer-name {
    color: white;
    font-size: 35px;
    font-weight: 800;
    margin-bottom: 20px;
}

.footer-details {
    color: #91b9e8;
    font-size: 16px;
    line-height: 2.4;
}

.footer-divider {
    border: 0;
    border-top: 1px solid rgba(110,160,210,0.18);
    margin: 35px 10% 25px;
}

.footer-copyright {
    color: #78a8d8;
    font-size: 13px;
}
</style>

<div class="developer-footer">

    <div class="footer-project-title">
        INTELLIX — AI-Powered Business Intelligence
        and Predictive Analytics System
    </div>

    <div class="footer-label">
        DESIGNED &amp; DEVELOPED BY
    </div>

    <div class="footer-name">
        Mohamed Riyaz S.
    </div>

    <div class="footer-details">
        Integrated M.Tech CSE | Business Analytics<br>
        VIT Chennai<br>
        AI · Machine Learning · Business Intelligence
    </div>

    <hr class="footer-divider">

    <div class="footer-copyright">
        © 2026 Mohamed Riyaz S. | All Rights Reserved.
    </div>

</div>
""")