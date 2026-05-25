from fastapi.testclient import TestClient
from backend.logic import evaluar_paciente
from main import app

client = TestClient(app)


def test_paciente_sano():
    """Caso 0: todos los signos vitales normales → SANO"""
    assert evaluar_paciente(36.5, 110, 80, 15, 98) == "PACIENTE SANO"


def test_enfermedad_leve():
    """Caso 1-2: ligera elevación → LEVE"""
    assert evaluar_paciente(37.5, 110, 80, 15, 98) == "ENFERMEDAD LEVE"


def test_enfermedad_moderada():
    """Caso 3-5: varios signos alterados → MODERADA"""
    assert evaluar_paciente(37.5, 130, 95, 18, 92) == "ENFERMEDAD MODERADA"


def test_enfermedad_grave():
    """Caso 6-8: signos muy alterados → GRAVE"""
    assert evaluar_paciente(38.5, 130, 95, 18, 92) == "ENFERMEDAD GRAVE"


def test_enfermedad_terminal():
    """Caso 9+: todos los signos críticos → TERMINAL"""
    assert evaluar_paciente(39.0, 160, 110, 25, 85) == "ENFERMEDAD TERMINAL"


def test_endpoint_stats_responde():
    """El endpoint /stats debe responder con código 200"""
    response = client.get("/stats")
    assert response.status_code == 200


def test_prediccion_se_refleja_en_estadisticas():
    """Tras una predicción vía formulario, /stats debe reflejarla"""
    response = client.post("/Prediction", data={
        "temperatura": 39.0,
        "presion_arterial": 160,
        "frecuencia_cardiaca": 110,
        "frecuencia_respiratoria": 25,
        "nivel_oxigeno": 85.0
    })
    assert response.status_code == 200
    assert "ENFERMEDAD TERMINAL" in response.text

    stats_response = client.get("/stats")
    assert stats_response.status_code == 200
    assert "ENFERMEDAD TERMINAL" in stats_response.text