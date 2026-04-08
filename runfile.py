import streamlit as st
import pandas as pd
import numpy as np
import io
import tempfile
import os

# Profiling
from ydata_profiling import ProfileReport
import sweetviz as sv

# Visualization
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="CSV Analyzer", layout="wide")

st.title("📊 CSV Data Analyzer App")

# File uploader
uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

if uploaded_file is not None:
    try:
        # Load dataset
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
        missing = df.isnull().sum()
        st.dataframe(missing)

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

            # Correlation heatmap
            st.subheader("🔥 Correlation Heatmap")
            fig2, ax2 = plt.subplots()
            sns.heatmap(df[numeric_cols].corr(), annot=True, cmap="coolwarm", ax=ax2)
            st.pyplot(fig2)
        else:
            st.warning("No numeric columns available for visualization.")

        # =========================
        # REPORT GENERATION
        # =========================
        st.subheader("📄 Generate Full Reports")

        if st.button("Generate Reports"):
            
            # -------- YData Profiling --------
            with st.spinner("Generating YData Profiling report..."):
                profile = ProfileReport(df, title="EDA Report", explorative=True)
                profile_html = profile.to_html()

            st.download_button(
                label="📥 Download YData Profiling Report",
                data=profile_html,
                file_name="ydata_profiling_report.html",
                mime="text/html"
            )

            # -------- Sweetviz Report --------
            with st.spinner("Generating Sweetviz report..."):
                temp_dir = tempfile.mkdtemp()
                sweetviz_path = os.path.join(temp_dir, "sweetviz_report.html")

                report = sv.analyze(df)
                report.show_html(sweetviz_path, open_browser=False)

                with open(sweetviz_path, "r", encoding="utf-8") as f:
                    sweetviz_html = f.read()

            st.download_button(
                label="📥 Download Sweetviz Report",
                data=sweetviz_html,
                file_name="sweetviz_report.html",
                mime="text/html"
            )

            st.success("Both reports generated successfully!")

    except Exception as e:
        st.error(f"Error processing file: {e}")

else:
    st.info("Please upload a CSV file to begin.")
