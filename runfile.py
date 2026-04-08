import streamlit as st
import pandas as pd
import sweetviz as sv
import tempfile
import os

st.set_page_config(page_title="Random Questions Dataset", layout="wide")

st.title("📊 Random Questions Dataset")

uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)
        st.success("File uploaded successfully!")

        st.subheader("🔍 Dataset Preview")
        st.dataframe(df.head())

        if st.button("Generate Sweetviz Report"):
            with st.spinner("Generating report... Please wait."):

                # Create temp file
                temp_dir = tempfile.mkdtemp()
                report_path = os.path.join(temp_dir, "sweetviz_report.html")

                # Generate report
                report = sv.analyze(df)
                report.show_html(report_path, open_browser=False)

                # Read HTML
                with open(report_path, "r", encoding="utf-8") as f:
                    html_data = f.read()

            st.success("Report generated successfully!")

            # =========================
            # DISPLAY REPORT IN APP
            # =========================
            st.subheader("📄 Sweetviz Report")

            st.components.v1.html(html_data, height=1000, scrolling=True)

            # =========================
            # DOWNLOAD OPTION
            # =========================
            st.download_button(
                label="📥 Download Report",
                data=html_data,
                file_name="sweetviz_report.html",
                mime="text/html"
            )

    except Exception as e:
        st.error(f"Error: {e}")

else:
    st.info("Please upload a CSV file to begin.")
