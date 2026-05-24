
from backend.logic import evaluar_paciente

def test_evaluar_paciente():
    assert evaluar_paciente(36.5, 110, 80, 15, 98) == "PACIENTE SANO"
    assert evaluar_paciente(37.5, 130, 95, 18, 92) == "ENFERMEDAD MODERADA"
    assert evaluar_paciente(38.5, 150, 105, 22, 88) == "ENFERMEDAD TERMINAL"
    assert evaluar_paciente(39.0, 160, 110, 25, 85) == "ENFERMEDAD TERMINAL"

