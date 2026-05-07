# Customer Churn Prediction & Retention Dashboard

## Project Overview

This project is a complete, production-ready full-stack application that simulates a real-world SaaS analytics product used by telecom or subscription-based businesses. 

It predicts customer churn using Machine Learning, identifies key drivers, provides actionable business insights, and displays the results in an interactive Streamlit dashboard. A FastAPI backend serves predictions and logs them to a SQLite database.

## Architecture

```text
User 
  --> [Streamlit Dashboard]
        --> /predict API Endpoint 
              --> [FastAPI Backend]
                    --> [ML Models (Logistic Regression / Random Forest)]
                    --> [SQLite Database (Logging)]
```

## Setup Instructions

### Prerequisites
- Python 3.9+
- Git

### Installation

1. **Clone the repository:**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Generate Synthetic Data:**
   Generate the realistic telecom dataset used for training.
   ```bash
   python scripts/generate_data.py
   ```

4. **Train the ML Models:**
   Train the Logistic Regression and Random Forest models, handle class imbalance, and save the artifacts.
   ```bash
   python scripts/train_model.py
   ```

5. **Initialize the Database (Optional, done automatically on API start):**
   ```bash
   python database/database.py
   ```

### Running the Application

1. **Start the FastAPI Backend:**
   In a terminal, run:
   ```bash
   uvicorn app.main:app --reload
   ```
   The API will be available at `http://localhost:8000`.

2. **Start the Streamlit Dashboard:**
   In a separate terminal, run:
   ```bash
   streamlit run dashboard/app.py
   ```
   The interactive UI will open in your browser.

## Screenshots
*(Placeholders for screenshots)*
- `[Screenshot: Prediction Panel]`
- `[Screenshot: Analytics Dashboard]`
- `[Screenshot: Power BI Dashboard]`
