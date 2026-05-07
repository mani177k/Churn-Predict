CREATE TABLE IF NOT EXISTS predictions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    gender TEXT,
    tenure INTEGER,
    monthly_charges REAL,
    contract_type TEXT,
    payment_method TEXT,
    prediction TEXT,
    probability REAL,
    risk_level TEXT
);
