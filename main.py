import streamlit as st
from datetime import datetime
import os

st.title("Cinepax Attendance Manager")

# Input fields
name = st.text_input("Employee Name")
status = st.selectbox("Status", ["Present", "Absent", "Late"])

if st.button("Save Attendance"):
    if name.strip() == "":
        st.error("Please enter employee name!")
    else:
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        record = f"Name: {name} | Status: {status} | Time: {current_time}\n"
        
        # Save to file
        with open("attendance_log.txt", "a") as f:
            f.write(record)
        st.success("Attendance saved successfully!")

st.subheader("Saved Attendance Records:")
file_path = "attendance_log.txt"
if os.path.exists(file_path):
    with open(file_path, "r") as f:
        content = f.read()
        if content.strip():
            st.text(content)
        else:
            st.text("No records found yet.")
else:
    st.text("No records found yet.")

