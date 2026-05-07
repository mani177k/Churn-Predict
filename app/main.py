import sys
import os
from pathlib import Path
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

# Robust path handling for local and cloud deployment
BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

try:
    from scripts.predict import predict_churn
    from database.database import init_db, log_prediction, get_recent_predictions
except ImportError as e:
    print(f"Import Error: {e}")

app = FastAPI(title="ChurnPredict Intelligence API", version="2.0")

class CustomerData(BaseModel):
    Gender: str = Field(..., description="Gender (Male/Female)")
    Tenure: int = Field(..., ge=0, description="Tenure in months")
    MonthlyCharges: float = Field(..., gt=0, description="Monthly charges")
    ContractType: str = Field(..., description="Contract Type")
    PaymentMethod: str = Field(..., description="Payment Method")

@app.on_event("startup")
def startup_event():
    try:
        init_db()
    except:
        pass

@app.get("/")
def read_root():
    return {"status": "online", "message": "Welcome to ChurnPredict Intelligence API"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.post("/predict")
def get_prediction(customer: CustomerData):
    try:
        data_dict = customer.dict()
        result = predict_churn(data_dict)
        
        try:
            log_prediction(data_dict, result)
        except:
            pass
            
        return result
    except FileNotFoundError as e:
        raise HTTPException(status_code=503, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/logs")
def get_logs(limit: int = 100):
    try:
        logs = get_recent_predictions(limit)
        return {"logs": logs}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
