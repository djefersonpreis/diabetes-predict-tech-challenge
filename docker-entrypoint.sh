#!/bin/bash
set -e

# Função para inicializar o pipeline
init_pipeline() {
    echo "Inicializando pipeline de dados..."
    python run_pipeline.py
}

# Função para iniciar API
start_api() {
    echo "Iniciando API FastAPI..."
    exec uvicorn src.api.main:app --host 0.0.0.0 --port 8000
}

# Função para iniciar Dashboard
start_dashboard() {
    echo "Iniciando Dashboard Streamlit..."
    exec streamlit run src/dashboard/app.py --server.port=8501 --server.address=0.0.0.0
}

# Função para executar pipeline completo
run_full_pipeline() {
    echo "Executando pipeline completo..."
    python run_pipeline.py
    echo "Pipeline executado com sucesso!"
}

# Função de ajuda
show_help() {
    echo "Uso: docker run [opções] diabetes-ml [COMANDO]"
    echo ""
    echo "Comandos disponíveis:"
    echo "  api         Inicia apenas a API FastAPI"
    echo "  dashboard   Inicia apenas o Dashboard Streamlit"
    echo "  pipeline    Executa o pipeline completo de dados"
    echo "  init        Inicializa e executa o pipeline"
    echo "  help        Mostra esta ajuda"
    echo ""
    echo "Exemplos:"
    echo "  docker run -p 8000:8000 diabetes-ml api"
    echo "  docker run -p 8501:8501 diabetes-ml dashboard"
    echo "  docker run diabetes-ml pipeline"
}

# Processar comando
case "$1" in
    api)
        start_api
        ;;
    dashboard)
        start_dashboard
        ;;
    pipeline)
        run_full_pipeline
        ;;
    init)
        init_pipeline
        start_api
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo "⚠️  Comando não reconhecido: $1"
        show_help
        exit 1
        ;;
esac