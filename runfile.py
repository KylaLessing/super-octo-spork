import streamlit as st
import pandas as pd
import numpy as np
import io
import tempfile
import os

# Safe import for profiling
try:
    from ydata_profiling import ProfileReport
    PROFILING_AVAILABLE = True
except ImportError:
    PROFILING_AVAILABLE = False

# Sweetviz
try:
    import sweetviz as sv
    SWEETVIZ_AVAILABLE = True
except ImportError:
    SWEETVIZ_AVAILABLE = False

# Visualization
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="CSV Analyzer", layout="wide")

st.title("📊 CSV Data Analyzer App")

# File uploader
uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)
        st.success("File uploaded successfully!")

        # =========================
        # BASIC INFO
        # =========================
        st.subheader("🔍 Dataset Preview")
        st.dataframe(df.head())

        st.subheader("📈 Dataset Summary")
        st.write(df.describe())

        st.subheader("ℹ️ Dataset Info")
        buffer = io.StringIO()
        df.info(buf=buffer)
        st.text(buffer.getvalue())

        # =========================
        # MISSING VALUES
        # =========================
        st.subheader("❗ Missing Values")
        st.dataframe(df.isnull().sum())

        # =========================
        # VISUALIZATIONS
        # =========================
        st.subheader("📊 Visualizations")

        numeric_cols = df.select_dtypes(include=np.number).columns

        if len(numeric_cols) > 0:
            selected_col = st.selectbox("Select column for histogram", numeric_cols)

            fig, ax = plt.subplots()
            sns.histplot(df[selected_col], kde=True, ax=ax)
            st.pyplot(fig)

            st.subheader("🔥 Correlation Heatmap")
            fig2, ax2 = plt.subplots()
            sns.heatmap(df[numeric_cols].corr(), annot=True, cmap="coolwarm", ax=ax2)
            st.pyplot(fig2)
        else:
            st.warning("No numeric columns available.")

        # =========================
        # REPORT GENERATION
        # =========================
        st.subheader("📄 Generate Full Reports")

        if st.button("Generate Reports"):

            # -------- YData Profiling --------
            if PROFILING_AVAILABLE:
                with st.spinner("Generating YData Profiling report..."):
                    profile = ProfileReport(df, title="EDA Report", explorative=True)
                    profile_html = profile.to_html()

                st.download_button(
                    label="📥 Download YData Profiling Report",
                    data=profile_html,
                    file_name="ydata_report.html",
                    mime="text/html"
                )
            else:
                st.warning("ydata-profiling is not installed.")

            # -------- Sweetviz --------
            if SWEETVIZ_AVAILABLE:
                with st.spinner("Generating Sweetviz report..."):
                    temp_dir = tempfile.mkdtemp()
                    path = os.path.join(temp_dir, "sweetviz.html")

                    report = sv.analyze(df)
                    report.show_html(path, open_browser=False)

                    with open(path, "r", encoding="utf-8") as f:
                        sweetviz_html = f.read()

                st.download_button(
                    label="📥 Download Sweetviz Report",
                    data=sweetviz_html,
                    file_name="sweetviz_report.html",
                    mime="text/html"
                )
            else:
                st.warning("Sweetviz is not installed.")

            st.success("Report generation completed!")

    except Exception as e:
        st.error(f"Error processing file: {e}")

else:
    st.info("Please upload a CSV file to begin.")
