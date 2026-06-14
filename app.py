import streamlit as st
import sqlite3
import joblib
import pandas as pd
from datetime import datetime, date

# Load ML Model
model = joblib.load("model.pkl")

# Database Connection
conn = sqlite3.connect("patients.db", check_same_thread=False)
cursor = conn.cursor()

# Title
st.set_page_config(
page_title="Health Prediction System",
page_icon="🏥",
layout="wide"
)

# Sidebar
st.sidebar.image(
    "https://img.icons8.com/color/96/hospital-3.png",
    width=100
)

st.sidebar.title("Health Prediction System")

st.sidebar.write(
    "AI-Powered Patient Health Risk Prediction"
)

st.sidebar.success(
    "Patient Management Dashboard"
)
st.sidebar.divider()

st.sidebar.header("Project Features")

st.sidebar.write("✅ Add Patient")
st.sidebar.write("✅ Update Patient")
st.sidebar.write("✅ Delete Patient")
st.sidebar.write("✅ Search Records")
st.sidebar.write("✅ Health Risk Prediction")

st.sidebar.divider()

st.title("🏥 Health Prediction System")
st.caption("AI-Powered Patient Health Risk Prediction")
st.divider()


# Input Fields
st.subheader("➕ Add New Patient")

col1, col2 = st.columns(2)

with col1:


 fullname = st.text_input("Full Name")

dob = st.date_input(
"Date of Birth",
min_value=date(1900, 1, 1),
max_value=date.today(),
value=None
)


email = st.text_input("Email Address")


with col2:


 glucose = st.number_input(
    "Glucose",
    min_value=0.0,
    format="%.2f"
)

haemoglobin = st.number_input(
    "Haemoglobin",
    min_value=0.0,
    format="%.2f"
)

cholesterol = st.number_input(
    "Cholesterol",
    min_value=0.0,
    format="%.2f"
)




# Predict and Save
if st.button("Predict & Save"):

    # Validation
    if fullname.strip() == "":
        st.error("Please enter Full Name")

    elif email.strip() == "" or "@" not in email:
        st.error("Please enter a valid Email Address")

    

    else:

        try:
            dob_date = dob

            if dob_date > date.today():
                st.error(
                    "Date of Birth cannot be a future date"
                )

            else:

                # ML Prediction
                prediction = model.predict(
                    [[18000,
                      cholesterol,
                      glucose,
                      120,
                      80]]
                )[0]

                if prediction == 1:
                    remarks = "High Cardiovascular Risk"
                else:
                    remarks = "Low Cardiovascular Risk"

                # Save Record
                cursor.execute("""SELECT *FROM patients WHERE fullname=? AND email=? AND dob=?""",(fullname,email,str(dob)))

                existing_patient = cursor.fetchone()

                if existing_patient:st.warning("⚠️ Patient record already exists")

                else:
                    cursor.execute("""
                INSERT INTO patients
                (
                    fullname,
                    dob,
                    email,
                    glucose,
                    haemoglobin,
                    cholesterol,
                    remarks
                )
                VALUES
                (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    fullname,
                    str(dob),
                    email,
                    glucose,
                    haemoglobin,
                    cholesterol,
                    remarks
                ))

                conn.commit()

                st.success(
                    "Patient Saved Successfully"
                )

                if remarks == "High Cardiovascular Risk":st.error(f"⚠️ {remarks}")
                else:st.success(f"✅ {remarks}")

        except ValueError:
            st.error(
                "Date must be in YYYY-MM-DD format"
            )

st.subheader("📊 Dashboard")

df = pd.read_sql_query(
"SELECT * FROM patients",
conn
)

col1, col2 = st.columns(2)

with col1:st.metric(
"Total Patients",
len(df)
)

with col2:st.metric(
"High Risk Patients",
len(
df[
df["remarks"] ==
"High Cardiovascular Risk"
]
)
)



# -------------------------

# UPDATE HEALTH DATA

# -------------------------

st.subheader("🩺 Update Health Data")

update_id = st.number_input(
"Patient ID",
min_value=0,
step=1,
format="%d",
key="update_id"
)

new_glucose = st.number_input(
"Glucose",
min_value=0.0,
format="%.2f",
key="upd_glucose"
)

new_haemoglobin = st.number_input(
"Haemoglobin",
min_value=0.0,
format="%.2f",
key="upd_haemoglobin"
)

new_cholesterol = st.number_input(
"Cholesterol",
min_value=0.0,
format="%.2f",
key="upd_cholesterol"
)

if st.button("Update Health Data"):


 if update_id == 0:
    st.error("Please enter Patient ID")

 else:

    cursor.execute(
        """
        SELECT glucose, haemoglobin, cholesterol
        FROM patients
        WHERE id=?
        """,
        (update_id,)
    )

    record = cursor.fetchone()

    if record is None:
        st.error("Invalid Patient ID")

    else:

        current_glucose = record[0]
        current_haemoglobin = record[1]
        current_cholesterol = record[2]

        # Keep old values if user enters 0

        if new_glucose == 0:
            new_glucose = current_glucose

        if new_haemoglobin == 0:
            new_haemoglobin = current_haemoglobin

        if new_cholesterol == 0:
            new_cholesterol = current_cholesterol

        prediction = model.predict(
            [[18000,
              new_cholesterol,
              new_glucose,
              120,
              80]]
        )[0]

        if prediction == 1:
            remarks = "High Cardiovascular Risk"
        else:
            remarks = "Low Cardiovascular Risk"

        cursor.execute(
            """
            UPDATE patients
            SET glucose=?,
                haemoglobin=?,
                cholesterol=?,
                remarks=?
            WHERE id=?
            """,
            (
                new_glucose,
                new_haemoglobin,
                new_cholesterol,
                remarks,
                update_id
            )
        )

        conn.commit()

        st.success("✅ Health Data Updated Successfully")










# -------------------------
# DELETE PATIENT
# -------------------------

st.subheader("🗑️ Delete Patient")

delete_id = st.number_input(
    "Enter Patient ID to Delete",
    step=1,
    format="%d",
    key="delete_id"
)

if st.button("🗑️ Delete Patient"):

    if delete_id == 0:
        st.error("Please enter Patient ID")

    else:

        cursor.execute(
            "SELECT * FROM patients WHERE id=?",
            (int(delete_id),)
        )

        patient = cursor.fetchone()

        if patient is None:
            st.error("Patient ID not found")

        else:

            cursor.execute(
                "DELETE FROM patients WHERE id=?",
                (int(delete_id),)
            )

            conn.commit()

            st.success("✅ Patient Deleted Successfully")

st.divider()

st.subheader("📋 Patient Records")

df = pd.read_sql_query(
"SELECT * FROM patients",
conn
)

df.columns = [
"ID",
"Full Name",
"DOB",
"Email",
"Glucose",
"Haemoglobin",
"Cholesterol",
"Remarks"
]

search_name = st.text_input(
"🔍 Search Patient by Name "
)

if search_name:df = df[
df["Full Name"]
.str.contains(
search_name,
case=False
)
]

st.dataframe(
df,
use_container_width=True,
hide_index=True
)
