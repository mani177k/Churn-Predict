import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
import joblib
import os

class ChurnDataProcessor:
    def __init__(self):
        self.num_imputer = SimpleImputer(strategy='median')
        self.cat_imputer = SimpleImputer(strategy='most_frequent')
        self.scaler = StandardScaler()
        self.encoder = OneHotEncoder(handle_unknown='ignore', sparse_output=False)
        self.numerical_cols = []
        self.categorical_cols = []
        self.feature_names = []
        self.is_fitted = False

    def fit(self, X):
        X = X.copy()
        self.numerical_cols = X.select_dtypes(include=['number']).columns.tolist()
        self.categorical_cols = X.select_dtypes(include=['object']).columns.tolist()

        if self.numerical_cols:
            self.num_imputer.fit(X[self.numerical_cols])
            X_num = self.num_imputer.transform(X[self.numerical_cols])
            self.scaler.fit(X_num)

        if self.categorical_cols:
            self.cat_imputer.fit(X[self.categorical_cols])
            X_cat = self.cat_imputer.transform(X[self.categorical_cols])
            self.encoder.fit(X_cat)

        self.is_fitted = True
        self._set_feature_names()
        return self

    def transform(self, X):
        if not self.is_fitted:
            raise ValueError("Processor must be fitted before transformation.")

        X = X.copy()
        
        X_num_processed = np.array([]).reshape(len(X), 0)
        if self.numerical_cols:
            X_num = self.num_imputer.transform(X[self.numerical_cols])
            X_num_processed = self.scaler.transform(X_num)

        X_cat_processed = np.array([]).reshape(len(X), 0)
        if self.categorical_cols:
            X_cat = self.cat_imputer.transform(X[self.categorical_cols])
            X_cat_processed = self.encoder.transform(X_cat)

        if X_num_processed.size > 0 and X_cat_processed.size > 0:
            X_combined = np.hstack([X_num_processed, X_cat_processed])
        elif X_num_processed.size > 0:
            X_combined = X_num_processed
        else:
            X_combined = X_cat_processed

        return pd.DataFrame(X_combined, columns=self.feature_names)

    def _set_feature_names(self):
        encoded_names = []
        if self.categorical_cols:
            encoded_names = self.encoder.get_feature_names_out(self.categorical_cols).tolist()
        self.feature_names = self.numerical_cols + encoded_names

    def save(self, path):
        joblib.dump(self, path)

    @staticmethod
    def load(path):
        return joblib.load(path)

def get_models_dir():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_dir, "models")

def load_data(filepath=None):
    if filepath is None:
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        filepath = os.path.join(base_dir, "data", "synthetic_churn_data.csv")
    return pd.read_csv(filepath)
