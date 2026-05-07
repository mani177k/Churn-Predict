import joblib
import pandas as pd
import os
import sys
import json
import shap

from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
SCRIPTS_DIR = ROOT_DIR / "scripts"

if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from scripts.data_preprocessing import ChurnDataProcessor

def get_metadata():
    metadata_path = os.path.join(ROOT_DIR, "models", "metadata.json")
    try:
        with open(metadata_path, "r") as f:
            return json.load(f)
    except:
        return {}

def load_artifacts():
    metadata = get_metadata()
    models_dir = os.path.join(ROOT_DIR, "models")
    
    model_name = metadata.get("version", "best_model.pkl")
    processor_name = metadata.get("processor", "scaler.pkl")
    
    model_path = os.path.join(models_dir, model_name)
    processor_path = os.path.join(models_dir, processor_name)
    
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model not found at {model_path}")
        
    model = joblib.load(model_path)
    
    try:
        processor = ChurnDataProcessor.load(processor_path)
    except:
        processor = None
        
    return model, processor

def predict_churn(customer_data: dict):
    model, processor = load_artifacts()
    df = pd.DataFrame([customer_data])
    
    if processor:
        X_processed = processor.transform(df)
    else:
        from data_preprocessing import transform_data as legacy_transform
        X_processed = legacy_transform(df)
    
    prediction = model.predict(X_processed)[0]
    probability = model.predict_proba(X_processed)[0]
    prob_churn = float(probability[1])
    
    risk_level = "Low"
    if prob_churn > 0.7:
        risk_level = "High"
    elif prob_churn > 0.4:
        risk_level = "Medium"
        
    reasons = []
    try:
        if "XGB" in str(type(model)) or "Forest" in str(type(model)):
            explainer = shap.TreeExplainer(model)
            shap_values = explainer.shap_values(X_processed)
            if isinstance(shap_values, list):
                shap_values = shap_values[1]
        else:
            explainer = shap.LinearExplainer(model, X_processed)
            shap_values = explainer.shap_values(X_processed)

        feature_names = X_processed.columns
        vals = shap_values[0] if len(shap_values.shape) > 1 else shap_values
        
        feature_contributions = sorted(zip(feature_names, vals), key=lambda x: x[1], reverse=True)
        
        for feature, contribution in feature_contributions[:3]:
            if contribution > 0.01:
                orig_feature = feature.split('_')[0]
                reasons.append(f"High impact from '{orig_feature}' contributes to churn risk.")
    except Exception as e:
        print(f"SHAP Error: {e}")
        if customer_data.get("ContractType") == "Month-to-month":
            reasons.append("Month-to-month contract is a strong churn indicator.")
        if float(customer_data.get("MonthlyCharges", 0)) > 80:
            reasons.append("High monthly charges increase financial pressure.")

    if not reasons:
        reasons.append("Customer shows stable account patterns.")
        
    recommendations = []
    if risk_level in ["High", "Medium"]:
        if customer_data.get("ContractType") == "Month-to-month":
            recommendations.append("Offer 20% discount on switching to an Annual Plan.")
        if float(customer_data.get("MonthlyCharges", 0)) > 70:
            recommendations.append("Suggest a tiered bundle to reduce monthly costs.")
        recommendations.append("Priority outreach: Schedule a customer success call.")
    else:
        recommendations.append("Maintain engagement with regular feature updates.")

    return {
        "prediction": "Yes" if prediction == 1 else "No",
        "probability": prob_churn,
        "risk_level": risk_level,
        "reasons": list(set(reasons)),
        "recommendations": recommendations
    }

if __name__ == "__main__":
    test_data = {
        "Gender": "Female",
        "Tenure": 5,
        "MonthlyCharges": 85.0,
        "ContractType": "Month-to-month",
        "PaymentMethod": "Electronic check"
    }
    print(json.dumps(predict_churn(test_data), indent=4))
