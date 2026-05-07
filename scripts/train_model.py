import json
import os
import sys
import joblib
import datetime
import numpy as np
from sklearn.model_selection import train_test_split, RandomizedSearchCV
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.metrics import classification_report, accuracy_score, precision_score, recall_score, f1_score
from imblearn.over_sampling import SMOTE

from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
SCRIPTS_DIR = ROOT_DIR / "scripts"

if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from scripts.data_preprocessing import ChurnDataProcessor, load_data, get_models_dir

def evaluate_model(model, X_test, y_test, model_name):
    y_pred = model.predict(X_test)
    print(f"--- {model_name} ---")
    print(classification_report(y_test, y_pred))
    
    return {
        "Accuracy": float(accuracy_score(y_test, y_pred)),
        "Precision": float(precision_score(y_test, y_pred)),
        "Recall": float(recall_score(y_test, y_pred)),
        "F1_Score": float(f1_score(y_test, y_pred))
    }

def train_and_save_models():
    print("Loading raw data...")
    df = load_data()
    
    if "CustomerID" in df.columns:
        df = df.drop("CustomerID", axis=1)
        
    y = (df["Churn"] == "Yes").astype(int)
    X = df.drop("Churn", axis=1)
    
    print("Splitting data (Train/Test)...")
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    
    print("Fitting preprocessing pipeline on training data...")
    processor = ChurnDataProcessor()
    processor.fit(X_train)
    
    print("Transforming training and test data...")
    X_train_processed = processor.transform(X_train)
    X_test_processed = processor.transform(X_test)
    
    print("Applying SMOTE to handle class imbalance on training data...")
    smote = SMOTE(random_state=42)
    X_train_smote, y_train_smote = smote.fit_resample(X_train_processed, y_train)
    
    models_dir = get_models_dir()
    os.makedirs(models_dir, exist_ok=True)
    
    print("Training Logistic Regression...")
    lr_model = LogisticRegression(max_iter=1000, random_state=42)
    lr_model.fit(X_train_smote, y_train_smote)
    lr_metrics = evaluate_model(lr_model, X_test_processed, y_test, "Logistic Regression")
    
    print("Tuning Random Forest...")
    rf_param_dist = {
        'n_estimators': [100, 200, 300],
        'max_depth': [None, 10, 20, 30],
        'min_samples_split': [2, 5, 10],
        'min_samples_leaf': [1, 2, 4]
    }
    rf_search = RandomizedSearchCV(RandomForestClassifier(random_state=42), 
                                   param_distributions=rf_param_dist, 
                                   n_iter=10, cv=3, scoring='f1', n_jobs=-1, random_state=42)
    rf_search.fit(X_train_smote, y_train_smote)
    rf_model = rf_search.best_estimator_
    rf_metrics = evaluate_model(rf_model, X_test_processed, y_test, "Random Forest")
    
    print("Tuning XGBoost...")
    xgb_param_dist = {
        'n_estimators': [100, 200, 300],
        'learning_rate': [0.01, 0.1, 0.2],
        'max_depth': [3, 5, 7],
        'subsample': [0.8, 1.0],
        'colsample_bytree': [0.8, 1.0]
    }
    xgb_search = RandomizedSearchCV(XGBClassifier(random_state=42), 
                                    param_distributions=xgb_param_dist, 
                                    n_iter=10, cv=3, scoring='f1', n_jobs=-1, random_state=42)
    xgb_search.fit(X_train_smote, y_train_smote)
    xgb_model = xgb_search.best_estimator_
    xgb_metrics = evaluate_model(xgb_model, X_test_processed, y_test, "XGBoost")
    
    results = {
        "Logistic Regression": lr_metrics,
        "Random Forest": rf_metrics,
        "XGBoost": xgb_metrics
    }
    
    best_model_name = max(results, key=lambda k: results[k]["F1_Score"])
    print(f"Selecting {best_model_name} as the best model.")
    
    if best_model_name == "Logistic Regression":
        best_model = lr_model
    elif best_model_name == "Random Forest":
        best_model = rf_model
    else:
        best_model = xgb_model
        
    feature_names = X_train_processed.columns.tolist()
    if hasattr(best_model, "feature_importances_"):
        importances = best_model.feature_importances_
    else:
        importances = abs(best_model.coef_[0])
        importances = importances / importances.sum()
        
    feat_imp = sorted(zip(feature_names, importances), key=lambda x: x[1], reverse=True)
    with open(os.path.join(models_dir, "feature_importance.json"), "w") as f:
        json.dump([{"feature": name, "importance": float(imp)} for name, imp in feat_imp], f, indent=4)
    
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    model_version = f"model_v_{timestamp}.pkl"
    processor_version = f"processor_v_{timestamp}.pkl"
    
    joblib.dump(best_model, os.path.join(models_dir, model_version))
    processor.save(os.path.join(models_dir, processor_version))
    
    metadata = {
        "version": model_version,
        "processor": processor_version,
        "best_model_type": best_model_name,
        "trained_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
        "metrics": results,
        "best_metrics": results[best_model_name]
    }
    with open(os.path.join(models_dir, "metadata.json"), "w") as f:
        json.dump(metadata, f, indent=4)
        
    print(f"Model and processor saved successfully to 'models/' directory.")

if __name__ == "__main__":
    train_and_save_models()
