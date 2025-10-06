#!/usr/bin/env python3
"""
Script para gerar diagramas visuais da arquitetura da aplicação
Execução: python generate_diagrams.py
"""

from diagrams import Diagram, Cluster, Edge
from diagrams.onprem.container import Docker
from diagrams.generic.database import SQL
from diagrams.programming.framework import Fastapi
from diagrams.programming.language import Python
from diagrams.generic.blank import Blank
from diagrams.generic.storage import Storage
from diagrams.aws.general import User
from diagrams.onprem.client import Client
import os

def create_architecture_diagram():
    """Cria diagrama da arquitetura geral do sistema"""
    
    with Diagram("🩺 Arquitetura - Sistema Predição Diabetes", 
                 filename="docs/architecture_diagram", 
                 show=False,
                 direction="TB"):
        
        # Camada de usuário
        user = User("👤 Usuário")
        
        # Camada de interface
        with Cluster("🌐 Interface Web"):
            dashboard = Client("📊 Dashboard\nStreamlit:8501")
            api_docs = Client("🚀 API Docs\nSwagger:8000")
        
        # Camada de aplicação (Containers)
        with Cluster("🐳 Containers Docker"):
            with Cluster("Container Dashboard"):
                streamlit_app = Python("Streamlit App")
            
            with Cluster("Container API"):
                fastapi_app = Fastapi("FastAPI App")
        
        # Camada de negócio
        with Cluster("🤖 Camada ML"):
            data_collector = Python("📥 Data\nCollector")
            data_processor = Python("⚙️ Data\nProcessor")
            ml_model = Python("🎯 ML Model\nRandom Forest")
        
        # Camada de dados
        with Cluster("💾 Persistência"):
            sqlite_db = SQL("🗄️ SQLite\nraw_data + processed_data")
            model_storage = Storage("💾 Model Files\n.joblib")
        
        # Fonte externa
        kaggle = Storage("🌐 Kaggle Dataset\n250k+ registros")
        
        # Conexões
        user >> dashboard
        user >> api_docs
        
        dashboard >> streamlit_app
        api_docs >> fastapi_app
        
        fastapi_app >> [data_collector, data_processor, ml_model]
        streamlit_app >> fastapi_app
        
        data_collector >> kaggle
        data_collector >> sqlite_db
        data_processor >> sqlite_db
        ml_model >> sqlite_db
        ml_model >> model_storage

def create_data_flow_diagram():
    """Cria diagrama do fluxo de dados"""
    
    with Diagram("🔄 Fluxo de Dados - Pipeline ML", 
                 filename="docs/data_flow_diagram", 
                 show=False,
                 direction="LR"):
        
        # Processo sequencial
        start = Python("🚀 Início")
        
        collect = Python("📥 Coleta\nKaggle API")
        process = Python("⚙️ Processamento\nLimpeza + Features")
        train = Python("🤖 Treinamento\nRandom Forest")
        deploy = Python("🚀 Deploy\nAPI + Dashboard")
        predict = Python("🎯 Predição\nTempo Real")
        
        end = Python("✅ Fim")
        
        # Base de dados
        raw_db = SQL("Raw Data")
        processed_db = SQL("Processed Data")
        model_files = Storage("Model Files")
        
        # Fluxo principal
        start >> collect >> raw_db
        raw_db >> process >> processed_db
        processed_db >> train >> model_files
        model_files >> deploy >> predict >> end

def create_container_diagram():
    """Cria diagrama dos containers Docker"""
    
    with Diagram("🐳 Containers - Deployment View", 
                 filename="docs/container_diagram", 
                 show=False,
                 direction="TB"):
        
        # Docker Compose
        docker_compose = Docker("🐳 Docker Compose")
        
        # Containers
        with Cluster("diabetes-api"):
            api_container = Docker("API Container\nPort 8000")
            api_app = Fastapi("FastAPI")
            api_container >> api_app
        
        with Cluster("diabetes-dashboard"):
            dash_container = Docker("Dashboard Container\nPort 8501")
            dash_app = Python("Streamlit")
            dash_container >> dash_app
        
        # Volumes compartilhados
        with Cluster("📂 Volumes Compartilhados"):
            data_volume = Storage("/data")
            models_volume = Storage("/models")
        
        # Rede interna
        network = Blank("🌐 Docker Network\ndiabetes-network")
        
        # Conexões
        docker_compose >> [api_container, dash_container]
        
        api_container >> data_volume
        api_container >> models_volume
        dash_container >> data_volume
        dash_container >> models_volume
        
        [api_container, dash_container] >> network

def create_ml_pipeline_diagram():
    """Cria diagrama específico do pipeline de ML"""
    
    with Diagram("🤖 Pipeline Machine Learning", 
                 filename="docs/ml_pipeline_diagram", 
                 show=False,
                 direction="TB"):
        
        # Entrada
        raw_data = Storage("📊 Dataset Bruto\n253,680 registros\n22 colunas")
        
        # Processamento
        with Cluster("⚙️ Data Processing"):
            cleaning = Python("🧹 Limpeza\nValores faltantes\nOutliers")
            feature_eng = Python("🔧 Feature Engineering\nSeleção + Normalização")
            validation = Python("✅ Validação\nQualidade dos dados")
        
        # Dados processados
        processed_data = Storage("📈 Dataset Processado\n11 features selecionadas")
        
        # Treinamento
        with Cluster("🤖 Model Training"):
            split = Python("📊 Train/Test Split\n80/20")
            training = Python("🎯 Random Forest\n100 árvores")
            evaluation = Python("📏 Avaliação\nAccuracy: 87.5%")
        
        # Modelo treinado
        with Cluster("💾 Model Artifacts"):
            model_file = Storage("🤖 model.joblib")
            scaler_file = Storage("📏 scaler.joblib")
            features_file = Storage("📋 feature_names.joblib")
        
        # Predição
        prediction = Python("🎯 Predição\nTempo Real")
        
        # Fluxo
        raw_data >> cleaning >> feature_eng >> validation >> processed_data
        processed_data >> split >> training >> evaluation
        evaluation >> [model_file, scaler_file, features_file]
        [model_file, scaler_file, features_file] >> prediction

def create_api_endpoints_diagram():
    """Cria diagrama dos endpoints da API"""
    
    with Diagram("🚀 API Endpoints - FastAPI", 
                 filename="docs/api_endpoints_diagram", 
                 show=False,
                 direction="LR"):
        
        # Cliente
        client = Client("👤 Cliente\nDashboard/External")
        
        # API Gateway
        api = Fastapi("🚀 FastAPI\nlocalhost:8000")
        
        # Endpoints
        with Cluster("📡 Endpoints"):
            health = Python("GET /health\nStatus da aplicação")
            data_stats = Python("GET /data-stats\nEstatísticas dos dados")
            collect = Python("POST /collect-data\nColeta do Kaggle")
            process = Python("POST /process-data\nProcessamento")
            train = Python("POST /train-model\nTreinamento ML")
            model_info = Python("GET /model-info\nInfo do modelo")
            predict = Python("POST /predict\nPredição individual")
        
        # Serviços
        with Cluster("🛠️ Services"):
            data_service = Python("DataService")
            ml_service = Python("MLService")
            db_service = SQL("DatabaseService")
        
        # Conexões
        client >> api
        api >> [health, data_stats, collect, process, train, model_info, predict]
        
        [collect, process] >> data_service
        [train, model_info, predict] >> ml_service
        data_service >> db_service
        ml_service >> db_service

def main():
    """Função principal que gera todos os diagramas"""
    
    print("🎨 Gerando diagramas da arquitetura...")
    
    # Criar diretório se não existir
    os.makedirs("docs", exist_ok=True)
    
    # Gerar diagramas
    print("  📊 Diagrama de arquitetura geral...")
    create_architecture_diagram()
    
    print("  🔄 Diagrama de fluxo de dados...")
    create_data_flow_diagram()
    
    print("  🐳 Diagrama de containers...")
    create_container_diagram()
    
    print("  🤖 Diagrama do pipeline ML...")
    create_ml_pipeline_diagram()
    
    print("  🚀 Diagrama dos endpoints API...")
    create_api_endpoints_diagram()
    
    print("✅ Diagramas gerados com sucesso em /docs/")
    print("\n📁 Arquivos criados:")
    print("  - architecture_diagram.png")
    print("  - data_flow_diagram.png") 
    print("  - container_diagram.png")
    print("  - ml_pipeline_diagram.png")
    print("  - api_endpoints_diagram.png")
    
    print("\n💡 Para visualizar:")
    print("  - Abra os arquivos .png no /docs/")
    print("  - Ou use: display docs/*.png (Linux)")
    print("  - Ou use: open docs/*.png (macOS)")

if __name__ == "__main__":
    main()