# 🔄 ChurnPredict: Customer Retention Intelligence Dashboard

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://churn-predict.streamlit.app/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0055ff?style=flat&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Python 3.11](https://img.shields.io/badge/Python-3.11-3776AB?style=flat&logo=python&logoColor=white)](https://www.python.org/)

A production-ready full-stack SaaS analytics platform that predicts customer churn using Machine Learning, identifies key churn drivers, and provides actionable business recommendations.

## 🚀 Key Features

- **AI-Powered Predictions**: Real-time churn risk analysis using Random Forest and XGBoost models.
- **Explainable AI (XAI)**: Integrated SHAP values to explain *why* a customer is at risk.
- **Interactive Analytics**: Deep-dive dashboard for segmenting customers by tenure, charges, and contract type.
- **Automated Retention Plans**: AI-generated suggestions for targeted customer outreach and discounts.
- **FastAPI Backend**: High-performance API for serving predictions and logging data to a persistent database.

## 🏗️ Architecture

```text
User 
  --> [Streamlit Frontend] (Port: 8501)
        --> [FastAPI Backend] (Port: 8000)
              --> [ML Models (RF/XGBoost)]
              --> [SQLite Database]
```

## 🛠️ Local Setup

1. **Clone & Install:**
   ```bash
   git clone <your-repo-url>
   cd churn-predict
   pip install -r requirements.txt
   ```

2. **Initialize & Train:**
   ```bash
   python scripts/generate_data.py
   python scripts/train_model.py
   ```

3. **Launch Application:**
   - **Start Backend:** `uvicorn app.main:app --reload`
   - **Start Dashboard:** `streamlit run dashboard/app.py`

## ☁️ Deployment

### Streamlit Community Cloud
This project is optimized for one-click deployment on Streamlit Cloud:
1. Push this repository to GitHub.
2. Connect your GitHub account to [Streamlit Cloud](https://share.streamlit.io/).
3. Select this repository and set the main file path to `dashboard/app.py`.
4. The application will automatically install dependencies from `requirements.txt`.

### Environment Compatibility
- **Python Version**: 3.11+
- **Entry Point**: `dashboard/app.py`
- **Data/Models**: All required artifacts are included in the `data/` and `models/` directories.

## 📊 Sample Insights
- **Intelligence Panel**: Input customer profiles to get instant risk scores and retention strategies.
- **Analytics Dashboard**: Visualize high-level metrics like Churn Rate, Average Revenue, and Risk Segmentation.

## 📄 License
Distributed under the MIT License. See `LICENSE` for more information.
