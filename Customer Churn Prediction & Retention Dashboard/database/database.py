import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "churn_app.db")
SCHEMA_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "schema.sql")

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    if not os.path.exists(DB_PATH):
        conn = get_db_connection()
        with open(SCHEMA_PATH, 'r') as f:
            conn.executescript(f.read())
        conn.commit()
        conn.close()
        print("Database initialized.")

def log_prediction(data, prediction_result):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO predictions 
        (gender, tenure, monthly_charges, contract_type, payment_method, prediction, probability, risk_level)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        data['Gender'],
        data['Tenure'],
        data['MonthlyCharges'],
        data['ContractType'],
        data['PaymentMethod'],
        prediction_result['prediction'],
        prediction_result['probability'],
        prediction_result['risk_level']
    ))
    conn.commit()
    conn.close()

def get_recent_predictions(limit=100):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM predictions ORDER BY timestamp DESC LIMIT ?", (limit,))
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

if __name__ == "__main__":
    init_db()
