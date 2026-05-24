import sqlite3
from datetime import datetime
import os

DB_PATH = os.path.join("database", "patient_data.db")


def init_db():
    """ Initialize the SQLite database and create the patient_data table if it doesn't exist. """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS patient_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            temperatura REAL,
            presion_arterial REAL,
            frecuencia_cardiaca INTEGER,
            frecuencia_respiratoria INTEGER,
            nivel_oxigeno REAL,
            riesgo TEXT,
            timestamp TEXT
        )
    ''')
    conn.commit()
    conn.close()


def insert_patient_data(temp, presion, fc, fr, oxigeno, riesgo):
    """ Insert patient data into the database. """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    timestamp = datetime.now().isoformat()
    cursor.execute('''
        INSERT INTO patient_data (temperatura, presion_arterial, frecuencia_cardiaca, frecuencia_respiratoria, nivel_oxigeno, riesgo, timestamp)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (temp, presion, fc, fr, oxigeno, riesgo, timestamp))
    conn.commit()
    conn.close()


def get_all_patient_data():
    """ Retrieve all patient data from the database. """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # 1. Total por categoría
    cursor.execute('SELECT riesgo, COUNT(*) FROM patient_data GROUP BY riesgo')
    conteo_categorias = dict(cursor.fetchall())

    # 2. Últimas 5 predicciones
    cursor.execute('SELECT riesgo FROM patient_data ORDER BY id DESC LIMIT 5')
    ultimas_5 = [row[0] for row in cursor.fetchall()]
    # 3. Fecha de la última predicción
    cursor.execute('SELECT MAX(timestamp) FROM patient_data')
    ultima_fecha = cursor.fetchone()[0]   
    conn.close()
    return {
        "total_por_categoria": conteo_categorias,
        "ultimas_5_predicciones": ultimas_5,
        "fecha_ultima_prediccion": ultima_fecha
    }
