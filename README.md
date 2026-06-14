# Health-Prediction-System




****📋 Overview****

The Health Prediction System is a web-based application developed using Python, Streamlit, SQLite, and Machine Learning.

The application allows users to manage patient health records and predict cardiovascular risk based on health parameters such as glucose, haemoglobin, and cholesterol levels.

The system provides complete CRUD (Create, Read, Update, Delete) functionality along with health risk prediction using a trained Machine Learning model.

✨ Features

✅ Add New Patient Records

✅ View Patient Records

✅ Update Patient Health Data

✅ Delete Patient Records

✅ Search Patient Records

✅ Cardiovascular Risk Prediction

✅ Dashboard Statistics

✅ Input Validation

✅ Duplicate Record Detection

✅ SQLite Database Integration

🛠 Technologies Used
Python
Streamlit
SQLite
Pandas
NumPy
Scikit-Learn
Joblib
OpenPyXL

md

🤖 Machine Learning Model

A Machine Learning classification model is used to predict the cardiovascular risk of patients based on health-related parameters.

Input Features:

Glucose
Cholesterol
Blood Pressure
Other Health Attributes

Output:

High Cardiovascular Risk
Low Cardiovascular Risk

Risk
🔒 Validation Features
Email Validation
Duplicate Patient Detection
Future Date Restriction for Date of Birth
Patient ID Validation
Numeric Input Validation
Error Handling for Invalid Records

📊 CRUD Operations

Create
Add a new patient and generate a health risk prediction.

Read
View all patient records and search patients by name.

Update
Update patient health information and recalculate health risk prediction.

Delete
Delete patient records using Patient ID.

🚀 How to Run
Install Dependencies
pip install -r requirements.txt
Run Application
streamlit run app.py
