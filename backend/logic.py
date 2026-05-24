

def evaluar_paciente(temperatura: float, presion_arterial: float,
                     frecuencia_cardiaca: int, frecuencia_respiratoria: int,
                     nivel_oxigeno: float) -> str:
    """ Función de evaluación del paciente con 5 categorías """
    riesgo = 0

    if 37 < temperatura <= 38: riesgo += 1
    elif temperatura > 38: riesgo += 2

    if 120 < presion_arterial <= 140: riesgo += 1
    elif presion_arterial > 140: riesgo += 2

    if 90 < frecuencia_cardiaca <= 100: riesgo += 1
    elif frecuencia_cardiaca > 100: riesgo += 2

    if 16 < frecuencia_respiratoria <= 20: riesgo += 1
    elif frecuencia_respiratoria > 20: riesgo += 2

    if 90 <= nivel_oxigeno < 95: riesgo += 1
    elif nivel_oxigeno < 90: riesgo += 2

    # Las 5 categorías requeridas por la entrega
    if riesgo == 0:
        return "PACIENTE SANO"
    elif riesgo <= 2:
        return "ENFERMEDAD LEVE"
    elif riesgo <= 5:
        return "ENFERMEDAD MODERADA"
    elif riesgo <= 8:
        return "ENFERMEDAD GRAVE"
    else:
        return "ENFERMEDAD TERMINAL"


def validar_rango_medico(temp, pres, fc, fr, oxigeno):
    """Retorna un mensaje de error si los valores son físicamente improbables"""
    if not (30 <= temp <= 45): return "Revisar valores: Temperatura fuera de rango lógico (30-45°C)"
    if not (50 <= pres <= 250): return "Revisar valores: Presión arterial fuera de rango (50-250 mmHg)"
    if not (20 <= fc <= 250): return "Revisar valores: Frecuencia cardíaca fuera de rango (20-250 bpm)"
    if not (5 <= fr <= 60): return "Revisar valores: Frecuencia respiratoria fuera de rango (5-60 rpm)"
    if not (40 <= oxigeno <= 100): return "Revisar valores: Nivel de oxígeno fuera de rango (40-100%)"
    return None  # Todo es válido
