import pandas as pd
import numpy as np
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    classification_report,
    confusion_matrix,
)
from sklearn.preprocessing import StandardScaler
from pathlib import Path
from src.database import get_processed_data, save_model_metrics


class DiabetesMLModel:
    def __init__(self):
        self.model = RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            min_samples_split=5,
            min_samples_leaf=2,
            random_state=42,
        )
        self.scaler = StandardScaler()
        self.feature_names = None
        self.model_path = Path("models")
        self.model_path.mkdir(exist_ok=True)

    def prepare_data(self):
        """Prepara os dados para treinamento"""
        df = get_processed_data()

        if df.empty:
            raise ValueError(
                "Nenhum dado processado encontrado. Execute o processamento primeiro."
            )

        if "id" in df.columns:
            df = df.drop("id", axis=1)
        if "processed_at" in df.columns:
            df = df.drop("processed_at", axis=1)

        X = df.drop("diabetes", axis=1)
        y = df["diabetes"]

        self.feature_names = X.columns.tolist()

        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )

        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)

        return X_train_scaled, X_test_scaled, y_train, y_test, X_train, X_test

    def train_model(self):
        """Treina o modelo Random Forest"""
        print("Iniciando treinamento do modelo...")

        X_train_scaled, X_test_scaled, y_train, y_test, X_train, X_test = (
            self.prepare_data()
        )

        self.model.fit(X_train, y_train)

        y_pred = self.model.predict(X_test)

        metrics = {
            "accuracy": accuracy_score(y_test, y_pred),
            "precision": precision_score(y_test, y_pred, average="weighted"),
            "recall": recall_score(y_test, y_pred, average="weighted"),
            "f1": f1_score(y_test, y_pred, average="weighted"),
        }

        print(f"Modelo treinado com sucesso!")
        print(f"Acurácia: {metrics['accuracy']:.4f}")
        print(f"Precisão: {metrics['precision']:.4f}")
        print(f"Recall: {metrics['recall']:.4f}")
        print(f"F1-Score: {metrics['f1']:.4f}")

        save_model_metrics(metrics)
        self.save_model()

        return metrics, y_test, y_pred

    def save_model(self):
        """Salva o modelo treinado"""
        model_file = self.model_path / "diabetes_model.joblib"
        scaler_file = self.model_path / "scaler.joblib"

        joblib.dump(self.model, model_file)
        joblib.dump(self.scaler, scaler_file)

        if self.feature_names:
            features_file = self.model_path / "feature_names.joblib"
            joblib.dump(self.feature_names, features_file)

        print(f"Modelo salvo em: {model_file}")

    def load_model(self):
        """Carrega o modelo treinado"""
        model_file = self.model_path / "diabetes_model.joblib"
        scaler_file = self.model_path / "scaler.joblib"
        features_file = self.model_path / "feature_names.joblib"

        if model_file.exists():
            self.model = joblib.load(model_file)
            self.scaler = joblib.load(scaler_file)

            if features_file.exists():
                self.feature_names = joblib.load(features_file)

            print("Modelo carregado com sucesso!")
            return True
        else:
            print("Nenhum modelo encontrado. Treine o modelo primeiro.")
            return False

    def predict(self, features):
        """Faz predição para um conjunto de features"""
        if not hasattr(self.model, "predict"):
            if not self.load_model():
                raise ValueError("Modelo não encontrado. Treine o modelo primeiro.")

        if isinstance(features, dict):
            features = pd.DataFrame([features])
        elif isinstance(features, list):
            features = pd.DataFrame([features], columns=self.feature_names)

        prediction = self.model.predict(features)
        probability = self.model.predict_proba(features)

        return prediction[0], probability[0]

    def get_feature_importance(self):
        """Retorna a importância das features"""
        if not hasattr(self.model, "feature_importances_"):
            if not self.load_model():
                return None

        importance_df = pd.DataFrame(
            {
                "feature": self.feature_names,
                "importance": self.model.feature_importances_,
            }
        ).sort_values("importance", ascending=False)

        return importance_df
