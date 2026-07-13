"""
Phreddy Web App
------------------
This is a website version of Phreddy, built using Streamlit.
It reuses the SAME analysis code as the command-line version —
we are not rewriting any of the logic, just adding a new "front door" to it.
"""
import streamlit as st 
#Streamlit is a python library used to build web applications  instead of writing HTML, CSS JAVASCRIPT we can build website using only python  
import tempfile #tempfile module is used to create a temporary file so the uploaded FASTQ file can be analyzed
import os #os module is used to remove temporary files after analysis 
from quality_calculator import analyze_fastq
from export_csv import export_csv

# ---------- Page setup ----------
st.set_page_config(page_title="Phreddy - FASTQ Quality Checker", page_icon="🧬")
st.title("🧬 Phreddy — FASTQ Quality Checker")
#this configure the webpage title and icon shown in the browser and sets up the large heading
st.write("Upload a FASTQ file (.fastq or .fastq.gz) to see its quality report.")
#created a file upload button 

# ---------- File upload ----------
uploaded_file = st.file_uploader("Choose a FASTQ file", type=["fastq", "gz"])
#The file uploder allows user to upload either a FASTQ or compressed FASTQ files 

if uploaded_file is not None: 
    #Initially no file is uploaded after uploading this brcomes a file object , then analysis begin"""
    suffix = ".gz" if uploaded_file.name.endswith(".gz") else ".fastq"
          # this is called a ternary operator similar to if else 

    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp_file: #creates a temp file 
        tmp_file.write(uploaded_file.getvalue()) #copies the uploaded file into the temp file
        temp_path = tmp_file.name #stores the temporary fiel name 

    try:
        reads, max_len, min_len, gc, n, per_base, all_scores = analyze_fastq(temp_path)
    except ValueError as e: #hanfles the broken FASTQ files 
        st.error(f"Problem with the file: {e}")
        st.stop()
    finally:
        os.remove(temp_path)

    overall = (sum(all_scores) / len(all_scores)) if all_scores else 0.0

    # ---------- Overall verdict ----------
    if overall >= 28:
        st.success("Overall quality: GOOD ✅")
    elif overall >= 20:
        st.warning("Overall quality: ACCEPTABLE ⚠️")
    else:
        st.error("Overall quality: POOR ❌")

    # ---------- Summary section (with hover tooltips) ----------
    st.subheader("Summary") #creates summary section 
    col1, col2, col3 = st.columns(3) #creates column 
    col1.metric("Total Reads", reads, #displays metric cards 
                help="How many sequencing reads were found in the file.") #parameters create a tooltip when mouse hover and explanantion appears 
    col2.metric("Read Length (Min-Max)", f"{min_len}-{max_len} bp",
                help="The shortest and longest reads found in the file.")
    col3.metric("Overall Avg Quality", f"{overall:.2f}",
                help="Average Phred quality score across all bases in all reads. 28+ is good, 20-27 is acceptable, below 20 is poor.")

    col4, col5 = st.columns(2)
    col4.metric("GC Content", f"{gc:.2f}%",
                help="Percentage of bases that are G or C. Normal range depends on the organism, but very high or very low values can signal contamination.")
    col5.metric("N Content", f"{n:.2f}%",
                help="Percentage of bases the sequencer could not confidently call (shown as 'N'). Should normally be very low.")

    # ---------- Per-base quality chart ----------
    if per_base: #only shows charts if data exists 
        st.subheader("Per-base Average Quality")
        positions = sorted(per_base.keys())
        averages = [per_base[pos][0] for pos in positions]
        st.line_chart(data={"Average Quality": averages})

        # ---------- Pass/Warn/Fail counts ----------
        pass_count = sum(1 for pos in per_base if per_base[pos][0] >= 28)
        warn_count = sum(1 for pos in per_base if 20 <= per_base[pos][0] < 28)
        fail_count = sum(1 for pos in per_base if per_base[pos][0] < 20)

        st.subheader("Position Verdict Counts")
        col6, col7, col8 = st.columns(3)
        col6.metric("✅ Passing Positions", pass_count)
        col7.metric("⚠️ Warning Positions", warn_count)
        col8.metric("❌ Failing Positions", fail_count)

        # ---------- Per-base table ----------
        st.subheader("Per-base Table")
        table_data = []
        for pos in positions:
            avg, min_q, max_q = per_base[pos]
            if avg >= 28:
                status = "✅ PASS"
            elif avg >= 20:
                status = "⚠️ WARN"
            else:
                status = "❌ FAIL"
            table_data.append({ #appends dictioanry 
                "Position": pos,
                "Avg": round(avg, 2),
                "Min": min_q,
                "Max": max_q,
                "Status": status
            })
        st.table(table_data)

        # ---------- Download report as CSV ----------
        st.subheader("Download Report")
        temp_csv_path = "temp_phreddy_report.csv"
        export_csv(temp_csv_path, reads, max_len, gc, n, overall, per_base)

        with open(temp_csv_path, "rb") as f:
            st.download_button("Download CSV Report", f, file_name="phreddy_report.csv")

        os.remove(temp_csv_path)  # clean up after offering the download

    else:
        st.warning("No reads were found in this file.")

        """
        This module provides a web interface for Phreddy using the Streamlit framework. 
        The user uploads a FASTQ or compressed FASTQ file through the browser,
        which is temporarily saved so it can be processed by the existing analyze_fastq() function.
        After analysis, the application calculates the overall average quality and displays an overall quality verdict. 
        It then presents summary metrics, a per-base quality line chart, counts of PASS, WARN, and FAIL positions, and a detailed per-base quality table.
        Finally, it allows the user to download the results as a CSV report by reusing the same export function from the command-line version.
        This demonstrates modular programming because the analysis logic is reused while only the user interface changes.
        """