

# 🏥 FastAPI Patient Records API

A lightweight and efficient RESTful API built with **FastAPI** for managing patient records. Data is stored in a **JSON file**, making it ideal for small-scale healthcare applications or prototyping.

---

## 🚀 Features

- **Create Patient Record** – Add a new patient.
- **Read Patient Records** – View all or individual patients.
- **Update Patient Record** – Modify existing patient information.
- **Delete Patient Record** – Remove patient data.
- **Validation** – Ensures correct data types and constraints using Pydantic.
- **OpenAPI Docs** – Swagger UI for easy testing.

---

## 📁 Project Structure
├── main.py # FastAPI app with CRUD endpoints and Pydantic models (Patient, PatientUpdate)
├── data.json # Patient data storage
├── requirements.txt # Python dependencies
└── README.md # Project documentation

## ⚙️ Setup Instructions

### 1. Clone the repository

git clone https://github.com/yourusername/patient-api.git
cd patient-api

### 2. Create a virtual environment (recommended)

python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

### 3.Install dependencies
pip install -r requirements.txt

### 4. Runn the server

uvicorn main:app --reload


📌 API Endpoints
Method	Endpoint	Description
POST	/create	Create a new patient
GET	/patients	Get all patients
GET	/patients/{id}	Get patient by ID
PUT	/edit/{id}	Update patient info
DELETE	/delete/{id}	Delete patient by ID


### To get the API documentation Visit: http://localhost:8000/docs
