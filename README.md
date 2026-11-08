# 🌱 AgriMind AI
### Smart Agriculture Powered by Artificial Intelligence

AgriMind AI is an AI-powered smart agriculture platform designed to support data-driven farming decisions. It combines Machine Learning models with an interactive Streamlit interface to help users make better decisions about crop selection, irrigation, and crop yield estimation.

The project aims to contribute to more efficient agricultural practices through predictive analytics and intelligent recommendations.

---
<p align="center">
  <a href="https://agrimind-ai.streamlit.app/">
    <img src="https://img.shields.io/badge/Live%20Demo-Try%20AgriMind%20AI-brightgreen?style=for-the-badge&logo=streamlit" alt="Live Demo">
  </a>
</p>
## 🚀 Key Features

### 🌾 1. Crop Recommendation
- Recommends the most suitable crop based on soil and environmental conditions.
- Uses soil nutrients (N, P, K), temperature, humidity, pH, and rainfall.
- Helps farmers make informed crop-selection decisions.

### 💧 2. Irrigation Prediction
- Predicts the required irrigation level based on agricultural conditions.
- Analyzes soil moisture, temperature, rainfall, wind speed, and other relevant features.
- Classifies irrigation requirements into:
  - Low
  - Medium
  - High

### 🌱 3. Crop Yield Prediction
- Estimates expected crop yield based on agricultural and environmental inputs.
- Considers soil properties, weather conditions, fertilizers, pesticides, sunlight, and crop-related information.
- Uses a trained Machine Learning regression model to generate predictions.

---

## 🧠 Machine Learning

AgriMind AI integrates multiple Machine Learning approaches to solve different agricultural problems.

| Feature | ML Approach | Task |
|---|---|---|
| Crop Recommendation | Random Forest Classifier | Multi-class Classification |
| Irrigation Prediction | Random Forest Classifier | Multi-class Classification |
| Crop Yield Prediction | Linear Regression | Regression |

### Model Evaluation

The models were evaluated using appropriate performance metrics, including:

- Accuracy
- Precision
- Recall
- F1-Score
- Confusion Matrix
- Cross-Validation

Model evaluation was performed during the development phase to assess predictive performance and reliability.

---

## 🛠️ Tech Stack

**Programming Language**
- Python

**Machine Learning & Data Processing**
- Scikit-learn
- Pandas
- NumPy
- Joblib

**Data Visualization**
- Matplotlib
- Seaborn

**Application Development**
- Streamlit

**Development Tools**
- Jupyter Notebook
- Visual Studio Code
- Git & GitHub

---

## 📂 Project Structure

```text
AgriMind-AI/
│
├── app/
│   ├── app.py
│   ├── Components/
│   │   ├── agrimind_ui.py
│   │   ├── components.py
│   │   └── styles.py
│   │
│   └── pages/
│       ├── crop_recommendation.py
│       ├── irrigation_prediction.py
│       └── 3_Crop_Yield_Prediction.py
│
├── Data/
│
├── models/
│   ├── Trained ML Models
│   └── Saved Preprocessing Objects
│
├── Notebooks/
│   └── Model Development & Evaluation
│
├── reports/
│
├── src/
│
├── requirements.txt
└── README.md
```

---

## ⚙️ Installation & Setup

Follow these steps to run AgriMind AI locally.

### 1. Clone the Repository

```bash
git clone https://github.com/mo7amedwa7ed/AgriMind-AI-Depi-Final-Project.git
```

### 2. Navigate to the Project Directory

```bash
cd AgriMind-AI-Depi-Final-Project
```

### 3. Create a Virtual Environment (Recommended)

```bash
python -m venv venv
```

Activate it:

**Windows:**
```bash
venv\Scripts\activate
```

**Linux / macOS:**
```bash
source venv/bin/activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Run the Application

```bash
streamlit run app/app.py
```

The application will open in your browser.

---

## 🌐 Deployment

AgriMind AI is built with Streamlit and can be deployed using **Streamlit Community Cloud**.

Deployment steps:

1. Push the project to a GitHub repository.
2. Open [Streamlit Community Cloud](https://share.streamlit.io/).
3. Connect your GitHub account.
4. Select the AgriMind AI repository.
5. Set the main application file to:

```text
app/app.py
```

6. Deploy the application.

---

## 🎯 Project Objectives

- Apply Machine Learning to real-world agricultural challenges.
- Support data-driven crop selection and irrigation decisions.
- Estimate crop productivity using predictive analytics.
- Build an interactive and user-friendly AI application.
- Demonstrate the integration of Machine Learning models into a practical software solution.

---

## 👨‍💻 Contributors

Developed as part of the **Digital Egypt Pioneers Initiative (DEPI)** – AI & Data Science Track.

---

## 📌 Future Improvements

- Integrate real-time weather data.
- Add more crop types and agricultural datasets.
- Improve model generalization using additional real-world data.
- Introduce explainable AI to provide insights into model predictions.
- Develop a farmer-focused recommendation and monitoring system.

---

**AgriMind AI — Smarter Decisions, Better Farming.** 🌱
