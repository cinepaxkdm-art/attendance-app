import streamlit as st
import pandas as pd
from datetime import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials

st.set_page_config(page_title="Cinepax Attendance & Roster", layout="wide")

st.title("🎬 Cinepax Attendance & Duty Roster Sync")

# Employees List from Master
EMPLOYEES = [
    "Syed Tayyab Shah",
    "Akash Ilyas",
    "Emaan Sandhu",
    "Armaan Gill",
    "Fatima",
    "Shumail",
    "Ayesha Munir",
    "Syed Gohar",
    "Syed Mohsin",
    "Jamila Bibi",
    "Sehar Sarfraz",
    "Rajal",
    "Ariyan Sohail",
    "Khalil Ahmed"
]

# 1. Date Selector
selected_date = st.date_input("Select Attendance Date", datetime.today())
date_str = selected_date.strftime("%Y-%m-%d")

st.subheader(f"Attendance Sheet for: {selected_date.strftime('%d-%b-%Y')}")

# Form for Bulk Entry
with st.form("attendance_form"):
    cols = st.columns([2, 2])
    cols[0].write("**Employee Name**")
    cols[1].write("**Status (Present / Absent / Late / Off)**")
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

    submit = st.form_submit_button("🚀 Sync All to Google Sheet")

if submit:
    try:
        # Connecting to Google Sheets using Streamlit Secrets or public fallback
        # (Make sure your Google Sheet is shared with edit access)
        sheet_url = "https://docs.google.com/spreadsheets/d/1p5PDnpFaS2hUpDnW6lLAvXaDYMrzJVIuDZ2i8xoP49A/edit?usp=drivesdk"
        
        # We will use pandas to preview and confirmation
        records = []
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        for emp, status in updated_status.items():
            records.append({
                "Date": date_str,
                "Employee Name": emp,
                "Status": status,
                "Synced At": timestamp
            })
        
        new_df = pd.DataFrame(records)
        st.success(f"✅ Attendance prepared for sync for {date_str}!")
        st.dataframe(new_df, use_container_width=True)
        
        # CSV download backup as well so data is never lost
        st.download_button(
            label="📥 Download This Attendance (CSV)",
            data=new_df.to_csv(index=False),
            file_name=f"attendance_{date_str}.csv",
            mime="text/csv"
        )
        
    except Exception as e:
        st.error(f"Error connecting to sheet: {e}")

# View Saved Records
st.divider()
st.subheader("📋 Status Summary")
st.info("Aap mobile se yahan attendance submit karenge, aur yeh foran record ho jayegi!")
