import streamlit as st
import pandas as pd
import sweetviz as sv
import tempfile
import os

st.set_page_config(page_title="Sweetviz Report Generator", layout="wide")

st.title("📊 Sweetviz Report Generator")

# Upload CSV
uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

if uploaded_file is not None:
    try:
        # Read CSV
        df = pd.read_csv(uploaded_file)
        st.success("File uploaded successfully!")

        # Show preview
        st.subheader("🔍 Dataset Preview")
        st.dataframe(df.head())

        # Generate report
        if st.button("Generate Sweetviz Report"):
            with st.spinner("Generating report... Please wait."):
                
                # Create temporary file
                temp_dir = tempfile.mkdtemp()
                report_path = os.path.join(temp_dir, "sweetviz_report.html")

                # Generate Sweetviz report
                report = sv.analyze(df)
                report.show_html(report_path, open_browser=False)

                # Read report file
                with open(report_path, "r", encoding="utf-8") as f:
                    report_html = f.read()

            # Download button
            st.download_button(
                label="📥 Download Sweetviz Report",
                data=report_html,
                file_name="sweetviz_report.html",
                mime="text/html"
            )

            st.success("Report generated successfully!")

    except Exception as e:
        st.error(f"Error: {e}")

else:
    st.info("Please upload a CSV file to begin.")
