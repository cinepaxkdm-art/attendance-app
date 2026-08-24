import streamlit as st
import pandas as pd
from datetime import datetime
import os

st.set_page_config(page_title="Cinepax Attendance", layout="wide")

st.title("🎬 Cinepax Bulk Attendance System")

# 1. Date Selector
selected_date = st.date_input("Select Date", datetime.today())

# 2. Employees List (Yahan aap apne tamam employees ke naam daal sakte hain)
EMPLOYEES = [
    "Sarfraz Mushtaq",
    "Ali Raza",
    "Usman Ahmed",
    "Hamza Khan",
    "Zaid Mahmood"
]

st.subheader(f"Attendance for {selected_date.strftime('%d-%b-%Y')}")

# Data storage setup
FILE_NAME = "bulk_attendance.csv"

# Pre-fill data or current form state
if "attendance_data" not in st.session_state:
    st.session_state.attendance_data = {emp: "Present" for emp in EMPLOYEES}

# Form for Bulk Entry
with st.form("bulk_attendance_form"):
    cols = st.columns([2, 2])
    cols[0].write("**Employee Name**")
    cols[1].write("**Status**")
    st.divider()

    updated_status = {}
    for emp in EMPLOYEES:
        c1, c2 = st.columns([2, 2])
        c1.write(f"**{emp}**")
        status = c2.selectbox(
            f"Status for {emp}",
            ["Present", "Absent", "Late", "Off"],
            key=f"status_{emp}",
            label_visibility="collapsed"
        )
        updated_status[emp] = status

    submit = st.form_submit_button("🚀 Sync All Attendance")

if submit:
    # Prepare records to save
    records = []
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    for emp, status in updated_status.items():
        records.append({
            "Date": selected_date.strftime("%Y-%m-%d"),
            "Employee Name": emp,
            "Status": status,
            "Synced At": timestamp
        })

    new_df = pd.DataFrame(records)

    # Append to CSV file
    if os.path.exists(FILE_NAME):
        existing_df = pd.read_csv(FILE_NAME)
        # Avoid duplicate entry for same date & employee
        combined_df = pd.concat([existing_df, new_df]).drop_duplicates(
            subset=["Date", "Employee Name"], keep="last"
        )
        combined_df.to_csv(FILE_NAME, index=False)
    else:
        new_df.to_csv(FILE_NAME, index=False)

    st.success(f"✅ Attendance for all employees synced successfully for {selected_date}!")

# 3. View & Filter Saved Data
st.divider()
st.subheader("📋 Saved Records & History")

if os.path.exists(FILE_NAME):
    df = pd.read_csv(FILE_NAME)
    
    # Filter by date if needed
    filter_date = st.date_input("Filter View by Date", selected_date)
    filtered_df = df[df["Date"] == filter_date.strftime("%Y-%m-%d")]
    
    if not filtered_df.empty:
        st.dataframe(filtered_df, use_container_width=True)
    else:
        st.info("No records found for the selected date.")
        
    # Download option for Excel/CSV report
    st.download_button(
        label="📥 Download Full Attendance Sheet (CSV)",
        data=df.to_csv(index=False),
        file_name="cinepax_attendance_report.csv",
        mime="text/csv"
    )
else:
    st.info("No attendance records created yet.")
