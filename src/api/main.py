from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict
import sys
from pathlib import Path

# Adicionar o diretório raiz ao path
sys.path.append(str(Path(__file__).parent.parent))

from src.data_collector import DataCollector
from src.data_processor import DataProcessor
from src.ml.diabetes_model import DiabetesMLModel
from src.database import get_raw_data, get_processed_data

app = FastAPI(
    title="Diabetes Prediction API",
    description="API para coleta, processamento e predição de diabetes usando Machine Learning",
    version="1.0.0",
)


# Modelos Pydantic para validação
class DiabetesFeatures(BaseModel):
    highbp: int  # 0 ou 1
    highchol: int  # 0 ou 1
    bmi: float
    smoker: int  # 0 ou 1
    stroke: int  # 0 ou 1
    heartdiseaseorattack: int  # 0 ou 1
    physactivity: int  # 0 ou 1
    genhlth: int  # 1-5
    age: int  # Idade real (será convertida)
    sex: int  # 0: feminino, 1: masculino
    diffwalk: int  # 0 ou 1


class PredictionResponse(BaseModel):
    prediction: int
    probability: Dict[str, float]
    risk_level: str


# Instâncias dos serviços
data_collector = DataCollector()
data_processor = DataProcessor()
ml_model = DiabetesMLModel()


@app.get("/")
async def root():
    """Endpoint raiz com informações da API"""
    return {
        "message": "API de Predição de Diabetes",
        "version": "1.0.0",
        "endpoints": {
            "/collect-data": "Coleta dados do Kaggle",
            "/process-data": "Processa dados brutos",
            "/train-model": "Treina modelo ML",
            "/predict": "Faz predição de diabetes",
            "/model-info": "Informações do modelo",
            "/data-stats": "Estatísticas dos dados",
        },
    }


@app.post("/collect-data")
async def collect_data():
    """Coleta dados do dataset de diabetes do Kaggle"""
    try:
        df = data_collector.load_and_store_data()
        return {
            "message": "Dados coletados com sucesso",
            "records_count": len(df),
            "columns": list(df.columns),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao coletar dados: {str(e)}")


@app.post("/process-data")
async def process_data():
    """Processa os dados brutos"""
    try:
        df = data_processor.process_data()
        return {
            "message": "Dados processados com sucesso",
            "processed_records": len(df),
            "features": list(df.columns),
        }
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Erro ao processar dados: {str(e)}"
        )


@app.post("/train-model")
async def train_model():
    """Treina o modelo de machine learning"""
    try:
        metrics, _, _ = ml_model.train_model()
        return {"message": "Modelo treinado com sucesso", "metrics": metrics}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao treinar modelo: {str(e)}")


@app.post("/predict", response_model=PredictionResponse)
async def predict_diabetes(features: DiabetesFeatures):
    """Faz predição de diabetes baseada nas características fornecidas"""
    try:
        # Converter idade real para categoria (aproximação)
        age_category = min(13, max(1, (features.age - 18) // 5 + 1))

        # Preparar dados para predição
        feature_dict = {
            "highbp": features.highbp,
            "highchol": features.highchol,
            "bmi": features.bmi,
            "smoker": features.smoker,
            "stroke": features.stroke,
            "heartdiseaseorattack": features.heartdiseaseorattack,
            "physactivity": features.physactivity,
            "genhlth": features.genhlth,
            "age": age_category,
            "sex": features.sex,
            "diffwalk": features.diffwalk,
        }

        prediction, probability = ml_model.predict(feature_dict)

        # Determinar nível de risco
        prob_diabetes = probability[1] if len(probability) > 1 else 0
        if prob_diabetes < 0.3:
            risk_level = "Baixo"
        elif prob_diabetes < 0.7:
            risk_level = "Moderado"
        else:
            risk_level = "Alto"

        return PredictionResponse(
            prediction=int(prediction),
            probability={
                "não_diabético": float(probability[0]),
                "diabético": float(probability[1]) if len(probability) > 1 else 0.0,
            },
            risk_level=risk_level,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro na predição: {str(e)}")


@app.get("/model-info")
async def get_model_info():
    """Retorna informações sobre o modelo"""
    try:
        if ml_model.load_model():
            feature_importance = ml_model.get_feature_importance()
            return {
                "model_type": "Random Forest Classifier",
                "features": ml_model.feature_names,
                "feature_importance": (
                    feature_importance.to_dict("records")
                    if feature_importance is not None
                    else None
                ),
            }
        else:
            return {"message": "Modelo não encontrado. Treine o modelo primeiro."}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Erro ao obter informações do modelo: {str(e)}"
        )


@app.get("/data-stats")
async def get_data_stats():
    """Retorna estatísticas dos dados"""
    try:
        # Dados brutos
        raw_data = get_raw_data()
        processed_data = get_processed_data()

        stats = {
            "raw_data_count": len(raw_data),
            "processed_data_count": len(processed_data),
        }

        if not processed_data.empty:
            diabetes_distribution = processed_data["diabetes"].value_counts().to_dict()
            stats["diabetes_distribution"] = diabetes_distribution

        return stats
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Erro ao obter estatísticas: {str(e)}"
        )


@app.get("/health")
async def health_check():
    """Endpoint para verificação de saúde da API"""
    return {"status": "healthy", "message": "API funcionando normalmente"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
