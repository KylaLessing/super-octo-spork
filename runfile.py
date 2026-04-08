import streamlit as st
import pandas as pd
import tempfile
import os

# Safe import
try:
    import sweetviz as sv
    SWEETVIZ_AVAILABLE = True
except ImportError:
    SWEETVIZ_AVAILABLE = False

st.set_page_config(page_title="Sweetviz Report Generator", layout="wide")

st.title("📊 Sweetviz Report Generator")

# Check dependency
if not SWEETVIZ_AVAILABLE:
    st.error("Sweetviz is not installed. Please add 'sweetviz' to your requirements.txt.")
    st.stop()

# Upload CSV
uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)
        st.success("File uploaded successfully!")

        st.subheader("🔍 Dataset Preview")
        st.dataframe(df.head())

        if st.button("Generate Sweetviz Report"):
            with st.spinner("Generating report..."):

                temp_dir = tempfile.mkdtemp()
                report_path = os.path.join(temp_dir, "sweetviz_report.html")

                report = sv.analyze(df)
                report.show_html(report_path, open_browser=False)

                with open(report_path, "r", encoding="utf-8") as f:
                    html = f.read()

            st.download_button(
                label="📥 Download Sweetviz Report",
                data=html,
                file_name="sweetviz_report.html",
                mime="text/html"
            )

            st.success("Report generated successfully!")

    except Exception as e:
        st.error(f"Error processing file: {e}")

else:
    st.info("Please upload a CSV file to begin.")
