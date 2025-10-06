import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import requests
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent))

from src.database import get_raw_data, get_processed_data
from src.ml.diabetes_model import DiabetesMLModel

st.set_page_config(
    page_title="Dashboard - Predição de Diabetes",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded",
)

API_URL = "http://api:8000"


def call_api_endpoint(endpoint, method="GET", data=None):
    """Chama um endpoint da API"""
    try:
        url = f"{API_URL}/{endpoint}"
        if method == "POST":
            response = requests.post(url, json=data)
        else:
            response = requests.get(url)

        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Erro na API: {response.status_code}")
            return None
    except requests.ConnectionError:
        st.warning("API não está disponível. Usando dados locais.")
        return None


def main():
    st.title("🩺 Dashboard - Predição de Diabetes")
    st.markdown("---")

    st.sidebar.title("Navegação")
    page = st.sidebar.selectbox(
        "Escolha uma página:",
        [
            "Visão Geral",
            "Coleta de Dados",
            "Análise Exploratória",
            "Modelo ML",
            "Predição",
        ],
    )

    if page == "Visão Geral":
        show_overview()
    elif page == "Coleta de Dados":
        show_data_collection()
    elif page == "Análise Exploratória":
        show_data_analysis()
    elif page == "Modelo ML":
        show_model_info()
    elif page == "Predição":
        show_prediction()


def show_overview():
    """Página de visão geral"""
    st.header("📊 Visão Geral do Projeto")

    col1, col2, col3 = st.columns(3)

    # Verificar status da API
    api_status = call_api_endpoint("health")

    with col1:
        if api_status:
            st.success("✅ API Online")
        else:
            st.error("❌ API Offline")

    with col2:
        stats = call_api_endpoint("data-stats")
        if stats:
            st.metric("Registros Brutos", stats.get("raw_data_count", 0))
        else:
            raw_data = get_raw_data()
            st.metric("Registros Brutos", len(raw_data))

    with col3:
        if stats:
            st.metric("Registros Processados", stats.get("processed_data_count", 0))
        else:
            processed_data = get_processed_data()
            st.metric("Registros Processados", len(processed_data))

    st.markdown("---")

    st.subheader("🎯 Sobre o Projeto")
    st.write(
        """
    Este projeto implementa uma solução completa de Machine Learning para predição de diabetes, incluindo:
    
    - **Coleta de Dados**: Integração com dataset do Kaggle
    - **Processamento**: Limpeza e preparação dos dados
    - **Modelo ML**: Random Forest para classificação
    - **API**: Interface RESTful com FastAPI
    - **Dashboard**: Visualização interativa com Streamlit
    """
    )

    st.subheader("🔄 Pipeline de Dados")
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.info("📥 Coleta\nKaggle Dataset")
    with col2:
        st.info("🔧 Processamento\nLimpeza e Features")
    with col3:
        st.info("🤖 Treinamento\nRandom Forest")
    with col4:
        st.info("🎯 Predição\nAPI + Dashboard")


def show_data_collection():
    """Página de coleta de dados"""
    st.header("📥 Coleta de Dados")

    st.write("Esta seção permite coletar e processar dados do dataset de diabetes.")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("🔄 Coletar Dados do Kaggle", type="primary"):
            with st.spinner("Coletando dados..."):
                result = call_api_endpoint("collect-data", "POST")
                if result:
                    st.success("Dados coletados com sucesso!")
                    st.json(result)
                else:
                    st.error("Erro ao coletar dados via API. Tentando localmente...")

    with col2:
        if st.button("⚙️ Processar Dados", type="secondary"):
            with st.spinner("Processando dados..."):
                result = call_api_endpoint("process-data", "POST")
                if result:
                    st.success("Dados processados com sucesso!")
                    st.json(result)
                else:
                    st.error("Erro ao processar dados via API.")

    st.subheader("📊 Status dos Dados")

    try:
        raw_data = get_raw_data()
        processed_data = get_processed_data()

        col1, col2 = st.columns(2)

        with col1:
            st.write("**Dados Brutos:**")
            if not raw_data.empty:
                st.write(f"- {len(raw_data)} registros")
                st.write(f"- {len(raw_data.columns)} colunas")
                with st.expander("Ver amostra dos dados brutos"):
                    st.dataframe(raw_data.head())
            else:
                st.write("Nenhum dado bruto encontrado.")

        with col2:
            st.write("**Dados Processados:**")
            if not processed_data.empty:
                st.write(f"- {len(processed_data)} registros")
                st.write(f"- {len(processed_data.columns)} features")
                with st.expander("Ver amostra dos dados processados"):
                    st.dataframe(processed_data.head())
            else:
                st.write("Nenhum dado processado encontrado.")

    except Exception as e:
        st.error(f"Erro ao carregar dados: {e}")


def show_data_analysis():
    """Página de análise exploratória"""
    st.header("📈 Análise Exploratória dos Dados")

    try:
        processed_data = get_processed_data()

        if processed_data.empty:
            st.warning(
                "Nenhum dado processado encontrado. Execute a coleta e processamento primeiro."
            )
            return

        st.subheader("🎯 Distribuição de Diabetes")
        diabetes_counts = processed_data["diabetes"].value_counts()

        col1, col2 = st.columns(2)

        with col1:
            fig_pie = px.pie(
                values=diabetes_counts.values,
                names=["Não Diabético", "Diabético"],
                title="Distribuição de Diabetes",
            )
            st.plotly_chart(fig_pie, use_container_width=True)

        with col2:
            fig_bar = px.bar(
                x=["Não Diabético", "Diabético"],
                y=diabetes_counts.values,
                title="Contagem de Casos",
            )
            st.plotly_chart(fig_bar, use_container_width=True)

        st.subheader("📊 Análise de Features")

        if "bmi" in processed_data.columns:
            fig_bmi = px.box(
                processed_data,
                x="diabetes",
                y="bmi",
                title="Distribuição do BMI por Status de Diabetes",
            )
            st.plotly_chart(fig_bmi, use_container_width=True)

        st.subheader("🔗 Matriz de Correlação")
        numeric_cols = processed_data.select_dtypes(
            include=["int64", "float64"]
        ).columns
        if len(numeric_cols) > 1:
            corr_matrix = processed_data[numeric_cols].corr()
            fig_corr = px.imshow(
                corr_matrix, title="Matriz de Correlação das Features", aspect="auto"
            )
            st.plotly_chart(fig_corr, use_container_width=True)

        with st.expander("📋 Estatísticas Descritivas"):
            st.dataframe(processed_data.describe())

    except Exception as e:
        st.error(f"Erro na análise exploratória: {e}")


def show_model_info():
    """Página de informações do modelo"""
    st.header("🤖 Modelo de Machine Learning")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("🚀 Treinar Modelo", type="primary"):
            with st.spinner("Treinando modelo Random Forest..."):
                result = call_api_endpoint("train-model", "POST")
                if result:
                    st.success("Modelo treinado com sucesso!")

                    metrics = result.get("metrics", {})
                    col_a, col_b, col_c, col_d = st.columns(4)

                    with col_a:
                        st.metric("Acurácia", f"{metrics.get('accuracy', 0):.4f}")
                    with col_b:
                        st.metric("Precisão", f"{metrics.get('precision', 0):.4f}")
                    with col_c:
                        st.metric("Recall", f"{metrics.get('recall', 0):.4f}")
                    with col_d:
                        st.metric("F1-Score", f"{metrics.get('f1', 0):.4f}")
                else:
                    st.error("Erro ao treinar modelo via API.")

    with col2:
        st.write("**Configurações do Modelo:**")
        st.write("- Algoritmo: Random Forest")
        st.write("- N° de árvores: 100")
        st.write("- Profundidade máxima: 10")
        st.write("- Min samples split: 5")
        st.write("- Min samples leaf: 2")

    st.subheader("📊 Informações do Modelo")
    model_info = call_api_endpoint("model-info")

    if model_info and model_info.get("features"):
        st.write("**Features utilizadas:**")
        features = model_info["features"]

        num_cols = 3
        cols = st.columns(num_cols)
        for i, feature in enumerate(features):
            with cols[i % num_cols]:
                st.write(f"• {feature}")

        if model_info.get("feature_importance"):
            st.subheader("🎯 Importância das Features")
            importance_data = model_info["feature_importance"]
            df_importance = pd.DataFrame(importance_data)

            fig_importance = px.bar(
                df_importance,
                x="importance",
                y="feature",
                orientation="h",
                title="Importância das Features no Modelo",
            )
            st.plotly_chart(fig_importance, use_container_width=True)
    else:
        st.info("Informações do modelo não disponíveis. Treine o modelo primeiro.")


def show_prediction():
    """Página de predição"""
    st.header("🎯 Predição de Diabetes")

    st.write("Insira as características do paciente para obter uma predição:")

    with st.form("prediction_form"):
        col1, col2 = st.columns(2)

        with col1:
            age = st.number_input("Idade", min_value=18, max_value=100, value=35)
            sex = st.selectbox("Sexo", ["Feminino", "Masculino"])
            bmi = st.number_input(
                "BMI", min_value=10.0, max_value=50.0, value=25.0, step=0.1
            )
            highbp = st.selectbox("Pressão Alta", ["Não", "Sim"])
            highchol = st.selectbox("Colesterol Alto", ["Não", "Sim"])
            smoker = st.selectbox("Fumante", ["Não", "Sim"])

        with col2:
            stroke = st.selectbox("Histórico de AVC", ["Não", "Sim"])
            heartdiseaseorattack = st.selectbox("Doença Cardíaca", ["Não", "Sim"])
            physactivity = st.selectbox("Atividade Física", ["Não", "Sim"])
            diffwalk = st.selectbox("Dificuldade para Caminhar", ["Não", "Sim"])
            genhlth = st.selectbox("Saúde Geral", [1, 2, 3, 4, 5])

        submitted = st.form_submit_button("🔍 Fazer Predição", type="primary")

        if submitted:
            features = {
                "age": age,
                "sex": 1 if sex == "Masculino" else 0,
                "bmi": bmi,
                "highbp": 1 if highbp == "Sim" else 0,
                "highchol": 1 if highchol == "Sim" else 0,
                "smoker": 1 if smoker == "Sim" else 0,
                "stroke": 1 if stroke == "Sim" else 0,
                "heartdiseaseorattack": 1 if heartdiseaseorattack == "Sim" else 0,
                "physactivity": 1 if physactivity == "Sim" else 0,
                "diffwalk": 1 if diffwalk == "Sim" else 0,
                "genhlth": genhlth,
            }

            with st.spinner("Fazendo predição..."):
                result = call_api_endpoint("predict", "POST", features)

                if result:
                    prediction = result["prediction"]
                    probability = result["probability"]
                    risk_level = result["risk_level"]

                    st.markdown("---")
                    st.subheader("📋 Resultado da Predição")

                    col1, col2, col3 = st.columns(3)

                    with col1:
                        if prediction == 1:
                            st.error("⚠️ Risco de Diabetes Detectado")
                        else:
                            st.success("✅ Sem Risco de Diabetes")

                    with col2:
                        st.metric(
                            "Probabilidade de Diabetes",
                            f"{probability['diabético']:.1%}",
                        )

                    with col3:
                        color = (
                            "red"
                            if risk_level == "Alto"
                            else "orange" if risk_level == "Moderado" else "green"
                        )
                        st.markdown(f"**Nível de Risco:** :{color}[{risk_level}]")

                    # Gráfico de probabilidades
                    fig = go.Figure(
                        data=[
                            go.Bar(
                                x=["Não Diabético", "Diabético"],
                                y=[
                                    probability["não_diabético"],
                                    probability["diabético"],
                                ],
                                marker_color=["green", "red"],
                            )
                        ]
                    )
                    fig.update_layout(
                        title="Probabilidades da Predição", yaxis_title="Probabilidade"
                    )
                    st.plotly_chart(fig, use_container_width=True)

                    st.subheader("💡 Recomendações")
                    if prediction == 1:
                        st.warning(
                            """
                        **Recomendações importantes:**
                        - Consulte um médico para avaliação completa
                        - Mantenha uma dieta balanceada
                        - Pratique exercícios regulares
                        - Monitore regularmente os níveis de glicose
                        - Controle o peso e a pressão arterial
                        """
                        )
                    else:
                        st.info(
                            """
                        **Mantenha hábitos saudáveis:**
                        - Continue com uma alimentação equilibrada
                        - Mantenha atividade física regular
                        - Realize check-ups médicos periódicos
                        - Evite o sedentarismo
                        """
                        )
                else:
                    st.error(
                        "Erro ao fazer predição via API. Verifique se o modelo está treinado."
                    )


if __name__ == "__main__":
    main()
