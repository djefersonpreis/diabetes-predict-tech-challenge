# 🩺 Projeto de Predição de Diabetes - Tech Challenge

## 📋 Descrição do Projeto

Este projeto implementa uma solução completa de Machine Learning para predição de diabetes, atendendo aos requisitos do Tech Challenge. A solução inclui coleta automatizada de dados, processamento, treinamento de modelo ML e interfaces para visualização e predição.

### 🎯 Objetivos Atendidos

- ✅ **API para coleta de dados**: FastAPI que baixa dataset do Kaggle automaticamente
- ✅ **Banco de dados**: SQLite para armazenamento de dados brutos e processados  
- ✅ **Modelo ML**: Random Forest para classificação de diabetes
- ✅ **Código versionado**: Projeto completo disponível no GitHub
- ✅ **Documentação completa**: README detalhado e comentários no código
- ✅ **Aplicação produtiva**: Dashboard interativo e API RESTful

## 🏗️ Arquitetura do Projeto

```
mlet3/
├── src/
│   ├── api/
│   │   └── main.py              # API FastAPI
│   ├── dashboard/
│   │   └── app.py               # Dashboard Streamlit
│   ├── ml/
│   │   └── diabetes_model.py    # Modelo Random Forest
│   ├── database.py              # Gerenciamento do banco SQLite
│   ├── data_collector.py        # Coleta de dados do Kaggle
│   └── data_processor.py        # Processamento de dados
├── data/                        # Dados coletados e banco SQLite
├── models/                      # Modelos treinados salvos
├── requirements.txt             # Dependências Python
└── README.md                    # Esta documentação
```

## 🚀 Como Executar o Projeto

### Pré-requisitos

- **Docker** e **Docker Compose** (Recomendado)
- Ou Python 3.8+ e pip (para execução local)

### 🐳 Execução com Docker (Recomendado)

#### Opção 1: Docker Compose (Mais Simples)

```bash
# Clone o repositório
git clone https://github.com/djefersonpreis/diabetes-predict-tech-challenge.git
cd mlet3

# Inicie tudo com um comando
docker-compose up -d

# Acesse as aplicações:
# API: http://localhost:8000/docs
# Dashboard: http://localhost:8501
```

### 💻 Execução Local (Desenvolvimento)

#### 1. Instalação

```bash
# Clone o repositório
git clone https://github.com/djefersonpreis/diabetes-predict-tech-challenge.git
cd mlet3

# Crie e ative um ambiente virtual (recomendado)
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate

# Instale as dependências
pip install -r requirements.txt
```

### 🌐 Acessando as Interfaces

- **API Documentation**: http://localhost:8000/docs
- **API Swagger UI**: http://localhost:8000/redoc  
- **Dashboard Streamlit**: http://localhost:8501

## 📐 Diagramas da Aplicação

### 🏗️ Arquitetura Geral

Veja o diagrama completo da arquitetura em: [`docs/ARCHITECTURE_DIAGRAM.txt`](docs/ARCHITECTURE_DIAGRAM.txt)

```
🌐 INTERFACES        📊 Dashboard (8501)  |  🚀 API (8000)
                           │                    │
🤖 ML LAYER          📥 Collector  →  ⚙️ Processor  →  🎯 Model
                           │                    │
🗄️ DATA LAYER        📊 Raw Data  →  🔧 Processed  →  💾 Models
                           │                    │
🐳 CONTAINERS        🔧 API Container  |  📊 Dashboard Container
```

### 🔄 Fluxo de Execução

Fluxo detalhado disponível em: [`docs/EXECUTION_FLOW.txt`](docs/EXECUTION_FLOW.txt)

```
1. 🐳 docker-compose up    →  Iniciar containers
2. 📥 Coleta Kaggle        →  Download dataset  
3. 🔧 Processamento        →  Limpeza + features
4. 🤖 Treinamento ML       →  Random Forest
5. 🚀 API + 📊 Dashboard   →  Sistema produtivo
6. 🎯 Predições            →  Tempo real
```

## 📊 Dataset e Features

### Fonte de Dados
- **Dataset**: Diabetes Health Indicators (Kaggle)
- **URL**: https://www.kaggle.com/datasets/mohankrishnathalla/diabetes-health-indicators-dataset
- **Registros**: ~250k+ registros
- **Features**: 22 indicadores de saúde

### Features Principais Utilizadas

| Feature | Descrição | Tipo |
|---------|-----------|------|
| `diabetes` | Status de diabetes (0: não, 1: sim) | Target |
| `highbp` | Pressão alta | Binary |
| `highchol` | Colesterol alto | Binary |
| `bmi` | Índice de massa corporal | Numeric |
| `smoker` | Fumante | Binary |
| `stroke` | Histórico de AVC | Binary |
| `heartdiseaseorattack` | Doença cardíaca | Binary |
| `physactivity` | Atividade física | Binary |
| `genhlth` | Saúde geral (1-5) | Ordinal |
| `age` | Idade (categorizada) | Ordinal |
| `sex` | Sexo (0: F, 1: M) | Binary |
| `diffwalk` | Dificuldade para caminhar | Binary |

## 🤖 Modelo de Machine Learning

### Algoritmo: Random Forest Classifier

**Parâmetros utilizados:**
- `n_estimators=100`: Número de árvores
- `max_depth=10`: Profundidade máxima
- `min_samples_split=5`: Mínimo de amostras para divisão
- `min_samples_leaf=2`: Mínimo de amostras por folha
- `random_state=42`: Seed para reprodutibilidade

### Performance Esperada
- **Acurácia**: ~85-90%
- **Precisão**: ~80-85%
- **Recall**: ~75-85%
- **F1-Score**: ~80-85%

## 🔌 API Endpoints

### Principais Endpoints

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| GET | `/` | Informações da API |
| POST | `/collect-data` | Coleta dados do Kaggle |
| POST | `/process-data` | Processa dados brutos |
| POST | `/train-model` | Treina modelo ML |
| POST | `/predict` | Faz predição de diabetes |
| GET | `/model-info` | Informações do modelo |
| GET | `/data-stats` | Estatísticas dos dados |
| GET | `/health` | Health check da API |

### Exemplo de Uso da API

```python
import requests

# Fazer predição
prediction_data = {
    "highbp": 1,
    "highchol": 1,
    "bmi": 30.0,
    "smoker": 0,
    "stroke": 0,
    "heartdiseaseorattack": 0,
    "physactivity": 1,
    "genhlth": 3,
    "age": 45,
    "sex": 1,
    "diffwalk": 0
}

response = requests.post("http://localhost:8000/predict", json=prediction_data)
result = response.json()

print(f"Predição: {result['prediction']}")
print(f"Probabilidade: {result['probability']}")
print(f"Nível de risco: {result['risk_level']}")
```

## 📱 Dashboard Interativo

### Funcionalidades

1. **Visão Geral**
   - Status da API e estatísticas gerais
   - Overview do pipeline de dados

2. **Coleta de Dados**
   - Interface para coletar dados do Kaggle
   - Processamento e validação de dados
   - Visualização de amostras dos datasets

3. **Análise Exploratória**
   - Distribuição da variável target
   - Análise de features importantes
   - Matriz de correlação
   - Estatísticas descritivas

4. **Modelo ML**
   - Treinamento do modelo
   - Métricas de performance
   - Importância das features

5. **Predição Interativa**
   - Formulário para entrada de dados do paciente
   - Predição em tempo real
   - Visualização de probabilidades
   - Recomendações personalizadas

## 🗄️ Estrutura do Banco de Dados

### Tabelas

1. **raw_data**: Dados brutos do Kaggle
2. **processed_data**: Dados limpos e preparados
3. **model_metrics**: Métricas de performance dos modelos

### Exemplo de Consulta

```sql
-- Ver distribuição de diabetes nos dados processados
SELECT diabetes, COUNT(*) as count 
FROM processed_data 
GROUP BY diabetes;

-- Ver métricas do último modelo treinado
SELECT * FROM model_metrics 
ORDER BY training_date DESC 
LIMIT 1;
```

## 🔄 Pipeline de Dados

### Fluxo Completo

1. **Coleta** (`DataCollector`)
   - Download automático do dataset do Kaggle
   - Extração de arquivos ZIP
   - Armazenamento em `raw_data`

2. **Processamento** (`DataProcessor`)
   - Limpeza de dados nulos
   - Seleção de features importantes
   - Tratamento de outliers
   - Normalização de variáveis
   - Armazenamento em `processed_data`

3. **Treinamento** (`DiabetesMLModel`)
   - Divisão treino/teste (80/20)
   - Treinamento do Random Forest
   - Validação cruzada
   - Cálculo de métricas
   - Salvamento do modelo

4. **Predição**
   - Carregamento do modelo treinado
   - Preprocessing dos dados de entrada
   - Predição e cálculo de probabilidades
   - Retorno de resultados formatados

## 🧪 Testes e Validação

### Como Testar

```bash
# Teste da API (com a API rodando)
curl -X POST "http://localhost:8000/predict" \
     -H "Content-Type: application/json" \
     -d '{
       "highbp": 1,
       "highchol": 1,
       "bmi": 30.0,
       "smoker": 0,
       "stroke": 0,
       "heartdiseaseorattack": 0,
       "physactivity": 1,
       "genhlth": 3,
       "age": 45,
       "sex": 1,
       "diffwalk": 0
     }'
```

## 📈 Métricas e Monitoramento

### Métricas Coletadas
- Acurácia do modelo
- Precisão, Recall e F1-Score
- Tempo de treinamento
- Número de registros processados
- Distribuição das classes

### Logs e Monitoramento
- Logs detalhados em cada etapa
- Validação de dados de entrada
- Tratamento de erros robusto
- Health checks da API

## � Containerização Docker

### Arquitetura dos Containers

O projeto utiliza **Docker Compose** para orquestrar dois serviços principais:

```yaml
services:
  api:           # FastAPI (porta 8000)
  dashboard:     # Streamlit (porta 8501)
```

### Arquivos Docker

| Arquivo | Descrição |
|---------|-----------|
| `Dockerfile.api` | Imagem específica da API |
| `Dockerfile.dashboard` | Imagem específica do Dashboard |
| `docker-compose.yml` | Orquestração dos serviços |
| `docker-entrypoint.sh` | Script de entrada flexível |
| `.dockerignore` | Arquivos ignorados no build |

### Volumes Compartilhados

- **./data:/app/data** - Dados e banco SQLite
- **./models:/app/models** - Modelos ML treinados

### Comandos Docker Essenciais

```bash
# Build e start completo
docker-compose up -d

# Rebuild forçado
docker-compose up -d --build

# Ver logs em tempo real
docker-compose logs -f

# Parar e remover tudo
docker-compose down -v
```

---

## 📊 Tech Challenge - Requisitos Atendidos

### ✅ Checklist de Entrega

- [x] **API para coleta de dados**: FastAPI com integração Kaggle
- [x] **Banco de dados**: SQLite com estrutura normalizada
- [x] **Modelo ML**: Random Forest com alta performance
- [x] **Código no GitHub**: Repositório completo e documentado
- [x] **Documentação**: README detalhado com instruções
- [x] **Aplicação produtiva**: Dashboard interativo funcional
- [x] **Pipeline automatizado**: Script de execução completa
- [x] **Métricas de performance**: Coleta e armazenamento de métricas
- [x] **Interface de usuário**: Dashboard Streamlit responsivo
- [x] **API RESTful**: Endpoints bem estruturados com validação

### 🎯 Diferenciais Implementados

- **Coleta automatizada** de dados do Kaggle
- **Interface dupla**: API + Dashboard
- **Pipeline completo** end-to-end
- **Validação robusta** de dados
- **Documentação abrangente**
- **Scripts de automação**
- **Tratamento de erros**
- **Métricas detalhadas**
- **Predições em tempo real**
- **Visualizações interativas**

---

**Projeto desenvolvido para o Tech Challenge - Predição de Diabetes com Machine Learning** 🚀