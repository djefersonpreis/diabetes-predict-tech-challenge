import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from src.database import get_raw_data, insert_processed_data


class DataProcessor:
    def __init__(self):
        self.scaler = StandardScaler()

    def process_data(self):
        """Processa os dados brutos e salva os dados processados"""
        df = get_raw_data()

        if df.empty:
            raise ValueError("Nenhum dado bruto encontrado no banco de dados")

        print(f"Processando {len(df)} registros...")

        if "id" in df.columns:
            df = df.drop("id", axis=1)
        if "created_at" in df.columns:
            df = df.drop("created_at", axis=1)

        # Converter diabetes para binário (0: não diabético, 1: diabético/pré-diabético)
        df["diabetes"] = (df["diabetes"] > 0).astype(int)

        important_features = [
            "diabetes",
            "highbp",
            "highchol",
            "bmi",
            "smoker",
            "stroke",
            "heartdiseaseorattack",
            "physactivity",
            "genhlth",
            "age",
            "sex",
            "diffwalk",
        ]

        # Verificar se todas as colunas existem
        available_features = [col for col in important_features if col in df.columns]
        df_processed = df[available_features].copy()

        # Remover valores nulos
        df_processed = df_processed.dropna()

        # Tratar outliers no BMI
        Q1 = df_processed["bmi"].quantile(0.25)
        Q3 = df_processed["bmi"].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        df_processed["bmi"] = df_processed["bmi"].clip(lower_bound, upper_bound)

        # Normalizar a idade (convertendo de categoria para numérico aproximado)
        age_mapping = {
            1: 22,
            2: 27,
            3: 32,
            4: 37,
            5: 42,
            6: 47,
            7: 52,
            8: 57,
            9: 62,
            10: 67,
            11: 72,
            12: 77,
            13: 82,
        }
        if "age" in df_processed.columns:
            df_processed["age"] = (
                df_processed["age"].map(age_mapping).fillna(df_processed["age"])
            )

        print(
            f"Dados processados: {len(df_processed)} registros com {len(df_processed.columns)} features"
        )

        insert_processed_data(df_processed)
        return df_processed

    def get_feature_importance_data(self):
        """Retorna dados formatados para análise de importância das features"""
        df = get_raw_data()
        if df.empty:
            return None

        stats = {}
        for diabetes_class in [0, 1, 2]:
            class_data = df[df["diabetes"] == diabetes_class]
            if not class_data.empty:
                stats[f"diabetes_{diabetes_class}"] = {
                    "count": len(class_data),
                    "avg_bmi": class_data["bmi"].mean(),
                    "avg_age": class_data["age"].mean(),
                    "highbp_rate": class_data["highbp"].mean(),
                    "highchol_rate": class_data["highchol"].mean(),
                    "smoker_rate": class_data["smoker"].mean(),
                }

        return stats
