import streamlit as st
import pandas as pd
from datetime import datetime
import gspread
from google.oauth2.service_account import Credentials

st.set_page_config(page_title="Cinepax Attendance & Roster Sync", layout="wide")

st.title("🎬 Cinepax Attendance & Duty Roster Sync")

# Employees List
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

# Google Sheets Scope Setup
SCOPE = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]

@st.cache_resource
def init_connection():
    # Direct aapki upload ki hui file ka naam yahan likh diya hai
    creds_file = "mos-attendance-e4eb455f193c.json"
    creds = Credentials.from_service_account_file(creds_file, scopes=SCOPE)
    client = gspread.authorize(creds)
    return client

client = init_connection()

# Date Selector
selected_date = st.date_input("Select Attendance Date", datetime.today())
date_str = selected_date.strftime("%Y-%m-%d")

st.subheader(f"Attendance Sheet for: {selected_date.strftime('%d-%b-%Y')}")

# Attendance Form
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
    if client:
        try:
            sheet_url = "https://docs.google.com/spreadsheets/d/1p5PDnpFaS2hUpDnW6lLAvXaDYMrzJVIuDZ2i8xoP49A/edit?usp=drivesdk"
            sheet = client.open_by_url(sheet_url).sheet1
            
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            rows_added = 0
            for emp, status in updated_status.items():
                sheet.append_row([date_str, emp, status, timestamp])
                rows_added += 1
                
            st.success(f"✅ Kamyaabi se {rows_added} employees ki attendance Google Sheet par sync ho gayi hai!")
            
        except Exception as e:
            st.error(f"Error syncing with Google Sheet: {e}")
    else:
        st.error("Google Sheets connection initialize nahi ho saka.")
