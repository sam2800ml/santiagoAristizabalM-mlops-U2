from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import uvicorn 

app = FastAPI(title= "MLops Taller 1 Evaluacion Medica")
templates = Jinja2Templates(directory="templates")

class PatientData(BaseModel):
    temperatura: float
    presion_arterial: float
    frecuencia_cardiaca: int
    frecuencia_respiratoria: int
    nivel_oxigeno: float


def evaluar_paciente(temperatura: float, presion_arterial: float,
                     frecuencia_cardiaca: int, frecuencia_respiratoria: int,
                     nivel_oxigeno: float) -> str:
    """ Patient evaluation function based on the provided parameters. """

    riesgo = 0

    # Temperatura
    if 37 < temperatura <= 38:
        riesgo += 1
    elif temperatura > 38:
        riesgo += 2

    # Presión arterial
    if 120 < presion_arterial <= 140:
        riesgo += 1
    elif presion_arterial > 140:
        riesgo += 2

    # Frecuencia cardíaca
    if 90 < frecuencia_cardiaca <= 100:
        riesgo += 1
    elif frecuencia_cardiaca > 100:
        riesgo += 2

    # Frecuencia respiratoria
    if 16 < frecuencia_respiratoria <= 20:
        riesgo += 1
    elif frecuencia_respiratoria > 20:
        riesgo += 2

    # Oxígeno
    if 90 <= nivel_oxigeno < 95:
        riesgo += 1
    elif nivel_oxigeno < 90:
        riesgo += 2

    # Clasificación
    if riesgo <= 2:
        return "Bajo riesgo"
    elif riesgo <= 5:
        return "Riesgo moderado"
    else:
        return "Alto riesgo"

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(request=request, name="index.html", context={})

@app.post("/Prediction", response_class=HTMLResponse)
async def predict(
    request: Request, temperatura: float = Form(...),
    presion_arterial: float = Form(...),
    frecuencia_cardiaca: int = Form(...),
    frecuencia_respiratoria: int = Form(...),
    nivel_oxigeno: float = Form(...)
):

    resultado = evaluar_paciente(temperatura, presion_arterial,
                frecuencia_cardiaca, frecuencia_respiratoria, nivel_oxigeno)

    return templates.TemplateResponse(request=request, name="index.html", context={
        "resultado": resultado,
        "temp": temperatura,
        "presion": presion_arterial,
        "fc": frecuencia_cardiaca,
        "fr": frecuencia_respiratoria,
        "oxigeno": nivel_oxigeno
    })

@app.post("/api/predict")
async def predecir_api(datos: PatientData):
    resultado = evaluar_paciente(
        datos.temperatura, datos.presion_arterial,
        datos.frecuencia_cardiaca, datos.frecuencia_respiratoria,
        datos.nivel_oxigeno
    )
    return {"resultado": resultado}

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)