import pandas as pd
import numpy as np
import random
import os

def generate_synthetic_data(num_records=5000):
    np.random.seed(42)
    random.seed(42)
    
    customer_ids = [f"CUST-{str(i).zfill(5)}" for i in range(1, num_records + 1)]
    genders = [random.choice(["Male", "Female"]) for _ in range(num_records)]
    tenures = [random.randint(1, 72) for _ in range(num_records)]
    
    contract_types = [random.choices(["Month-to-month", "One year", "Two year"], weights=[0.55, 0.20, 0.25])[0] for _ in range(num_records)]
    
    payment_methods = [random.choices(
        ["Electronic check", "Mailed check", "Bank transfer", "Credit card"], 
        weights=[0.35, 0.25, 0.20, 0.20])[0] for _ in range(num_records)]
    
    monthly_charges = [round(random.uniform(20.0, 120.0), 2) for _ in range(num_records)]
    
    churn = []
    for i in range(num_records):
        risk_score = 0
        if contract_types[i] == "Month-to-month":
            risk_score += 0.4
        elif contract_types[i] == "Two year":
            risk_score -= 0.3
            
        if tenures[i] < 12:
            risk_score += 0.3
        elif tenures[i] > 60:
            risk_score -= 0.2
            
        if monthly_charges[i] > 90:
            risk_score += 0.2
            
        if payment_methods[i] == "Electronic check":
            risk_score += 0.1
            
        prob = 0.2 + risk_score  
        
        prob += random.uniform(-0.1, 0.1)
        prob = max(0, min(1, prob))
        
        churn.append("Yes" if random.random() < prob else "No")
        
    df = pd.DataFrame({
        "CustomerID": customer_ids,
        "Gender": genders,
        "Tenure": tenures,
        "MonthlyCharges": monthly_charges,
        "ContractType": contract_types,
        "PaymentMethod": payment_methods,
        "Churn": churn
    })
    
    from pathlib import Path
    base_dir = Path(__file__).resolve().parent.parent
    data_dir = base_dir / "data"
    data_dir.mkdir(parents=True, exist_ok=True)
    df.to_csv(data_dir / "synthetic_churn_data.csv", index=False)
    print("Synthetic data generated successfully at 'data/synthetic_churn_data.csv'")

if __name__ == "__main__":
    generate_synthetic_data()
