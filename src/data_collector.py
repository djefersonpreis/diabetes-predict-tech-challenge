import requests
import zipfile
import pandas as pd
import os
from pathlib import Path
from src.database import insert_raw_data, init_database


class DataCollector:
    def __init__(self):
        self.dataset_url = "https://www.kaggle.com/api/v1/datasets/download/mohankrishnathalla/diabetes-health-indicators-dataset"
        self.data_dir = Path("data")
        self.data_dir.mkdir(exist_ok=True)

    def download_dataset(self):
        """Baixa o dataset do Kaggle"""
        try:
            print("Baixando dataset do Kaggle...")
            response = requests.get(self.dataset_url, stream=True)
            response.raise_for_status()

            zip_path = self.data_dir / "diabetes_dataset.zip"
            with open(zip_path, "wb") as file:
                for chunk in response.iter_content(chunk_size=8192):
                    file.write(chunk)

            print("Dataset baixado com sucesso!")
            return zip_path
        except Exception as e:
            print(f"Erro ao baixar dataset: {e}")
            raise e
            # return self.create_sample_data()

    def extract_csv(self, zip_path):
        """Extrai o arquivo CSV do ZIP"""
        try:
            with zipfile.ZipFile(zip_path, "r") as zip_ref:
                zip_ref.extractall(self.data_dir)

            csv_files = list(self.data_dir.glob("*.csv"))
            if csv_files:
                return csv_files[0]
            else:
                raise FileNotFoundError("Nenhum arquivo CSV encontrado no ZIP")
        except Exception as e:
            print(f"Erro ao extrair CSV: {e}")
            raise e
            # return self.create_sample_data()

    def create_sample_data(self):
        """Cria dados de exemplo para demonstração"""
        print("Criando dados de exemplo...")
        import numpy as np

        n_samples = 1000
        np.random.seed(42)

        data = {
            "Diabetes_012": np.random.choice([0, 1, 2], n_samples, p=[0.7, 0.2, 0.1]),
            "HighBP": np.random.choice([0, 1], n_samples, p=[0.6, 0.4]),
            "HighChol": np.random.choice([0, 1], n_samples, p=[0.6, 0.4]),
            "CholCheck": np.random.choice([0, 1], n_samples, p=[0.2, 0.8]),
            "BMI": np.random.normal(25, 5, n_samples).clip(15, 50),
            "Smoker": np.random.choice([0, 1], n_samples, p=[0.7, 0.3]),
            "Stroke": np.random.choice([0, 1], n_samples, p=[0.9, 0.1]),
            "HeartDiseaseorAttack": np.random.choice([0, 1], n_samples, p=[0.8, 0.2]),
            "PhysActivity": np.random.choice([0, 1], n_samples, p=[0.4, 0.6]),
            "Fruits": np.random.choice([0, 1], n_samples, p=[0.5, 0.5]),
            "Veggies": np.random.choice([0, 1], n_samples, p=[0.3, 0.7]),
            "HvyAlcoholConsump": np.random.choice([0, 1], n_samples, p=[0.9, 0.1]),
            "AnyHealthcare": np.random.choice([0, 1], n_samples, p=[0.1, 0.9]),
            "NoDocbcCost": np.random.choice([0, 1], n_samples, p=[0.8, 0.2]),
            "GenHlth": np.random.choice([1, 2, 3, 4, 5], n_samples),
            "MentHlth": np.random.randint(0, 31, n_samples),
            "PhysHlth": np.random.randint(0, 31, n_samples),
            "DiffWalk": np.random.choice([0, 1], n_samples, p=[0.8, 0.2]),
            "Sex": np.random.choice([0, 1], n_samples, p=[0.5, 0.5]),
            "Age": np.random.choice(range(1, 14), n_samples),
            "Education": np.random.choice(range(1, 7), n_samples),
            "Income": np.random.choice(range(1, 9), n_samples),
        }

        df = pd.DataFrame(data)
        csv_path = self.data_dir / "diabetes_health_indicators.csv"
        df.to_csv(csv_path, index=False)
        print(f"Dados de exemplo salvos em: {csv_path}")
        return csv_path

    def load_and_store_data(self):
        """Processo completo: baixar, extrair e armazenar dados"""
        init_database()

        zip_path = self.download_dataset()
        if str(zip_path).endswith(".zip"):
            csv_path = self.extract_csv(zip_path)
        else:
            csv_path = zip_path

        df = pd.read_csv(csv_path)
        print(f"Dataset carregado com {len(df)} registros e {len(df.columns)} colunas")
        print(f"🔍 Colunas disponíveis: {list(df.columns)}")

        if "diagnosed_diabetes" in df.columns:
            column_mapping = {
                "diagnosed_diabetes": "diabetes",
                "hypertension_history": "highbp",
                "cholesterol_total": "highchol",
                "bmi": "bmi",
                "smoking_status": "smoker",
                "cardiovascular_history": "stroke",
                "cardiovascular_history": "heartdiseaseorattack",
                "physical_activity_minutes_per_week": "physactivity",
                "diet_score": "genhlth",
                "age": "age",
                "gender": "sex",
            }

            for old_col, new_col in column_mapping.items():
                if old_col in df.columns:
                    df[new_col] = df[old_col]

            if "diabetes" in df.columns:
                df["diabetes"] = df["diabetes"].astype(int)
            if "smoker" in df.columns:
                df["smoker"] = (df["smoker"] == "current_smoker").astype(int)
            if "physactivity" in df.columns:
                df["physactivity"] = (df["physactivity"] > 150).astype(int)
            if "genhlth" in df.columns:
                # Normalizar diet_score (0-10) para genhlth (1-5)
                df["genhlth"] = ((df["genhlth"] / 2) + 1).clip(1, 5).round().astype(int)
            if "sex" in df.columns:
                df["sex"] = (df["sex"] == "male").astype(int)

            # Criar colunas ausentes com valores derivados ou padrão
            if "cholcheck" not in df.columns:
                df["cholcheck"] = 1
            if "diffwalk" not in df.columns:
                df["diffwalk"] = 0

        else:
            original_mapping = {
                "Diabetes_012": "diabetes",
                "HighBP": "highbp",
                "HighChol": "highchol",
                "CholCheck": "cholcheck",
                "BMI": "bmi",
                "Smoker": "smoker",
                "Stroke": "stroke",
                "HeartDiseaseorAttack": "heartdiseaseorattack",
                "PhysActivity": "physactivity",
                "GenHlth": "genhlth",
                "Sex": "sex",
                "Age": "age",
                "DiffWalk": "diffwalk",
            }

            for old_col, new_col in original_mapping.items():
                if old_col in df.columns:
                    df[new_col] = df[old_col]

        required_columns = [
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

        for col in required_columns:
            # Se a coluna não existir, cria com valor zerado
            if col not in df.columns:
                df[col] = 0

        df_final = df[required_columns + ["cholcheck"]].copy()

        print(
            f"✅ Dataset final: {len(df_final)} registros com {len(df_final.columns)} colunas"
        )

        insert_raw_data(df_final)
        print("Dados brutos inseridos no banco de dados!")

        return df_final
