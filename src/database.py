import sqlite3
import pandas as pd
from pathlib import Path

DATABASE_PATH = Path("data/diabetes_db.sqlite")


def init_database():
    """Inicializa o banco de dados com as tabelas necessárias"""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    # Tabela para raw_data
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS raw_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            diabetes INTEGER,
            highbp INTEGER,
            highchol INTEGER,
            cholcheck INTEGER,
            bmi REAL,
            smoker INTEGER,
            stroke INTEGER,
            heartdiseaseorattack INTEGER,
            physactivity INTEGER,
            fruits INTEGER,
            veggies INTEGER,
            hvyalcoholconsump INTEGER,
            anyhealthcare INTEGER,
            nodocbccost INTEGER,
            genhlth INTEGER,
            menthlth INTEGER,
            physhlth INTEGER,
            diffwalk INTEGER,
            sex INTEGER,
            age INTEGER,
            education INTEGER,
            income INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """
    )

    # Tabela para processed_data
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS processed_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            diabetes INTEGER,
            highbp INTEGER,
            highchol INTEGER,
            bmi REAL,
            smoker INTEGER,
            stroke INTEGER,
            heartdiseaseorattack INTEGER,
            physactivity INTEGER,
            genhlth INTEGER,
            age INTEGER,
            sex INTEGER,
            diffwalk INTEGER,
            processed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """
    )

    # Tabela para model_metrics
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS model_metrics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            accuracy REAL,
            precision_score REAL,
            recall REAL,
            f1_score REAL,
            training_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """
    )

    conn.commit()
    conn.close()


def get_connection():
    """Retorna uma conexão com o banco de dados"""
    return sqlite3.connect(DATABASE_PATH)


def insert_raw_data(df):
    """Insere dados brutos no banco"""
    conn = get_connection()
    df.to_sql("raw_data", conn, if_exists="append", index=False)
    conn.close()


def insert_processed_data(df):
    """Insere dados processados no banco"""
    conn = get_connection()
    df.to_sql("processed_data", conn, if_exists="append", index=False)
    conn.close()


def get_raw_data():
    """Recupera dados brutos do banco"""
    conn = get_connection()
    df = pd.read_sql_query("SELECT * FROM raw_data", conn)
    conn.close()
    return df


def get_processed_data():
    """Recupera dados processados do banco"""
    conn = get_connection()
    df = pd.read_sql_query("SELECT * FROM processed_data", conn)
    conn.close()
    return df


def save_model_metrics(metrics):
    """Salva métricas do modelo no banco"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO model_metrics (accuracy, precision_score, recall, f1_score)
        VALUES (?, ?, ?, ?)
    """,
        (metrics["accuracy"], metrics["precision"], metrics["recall"], metrics["f1"]),
    )
    conn.commit()
    conn.close()
