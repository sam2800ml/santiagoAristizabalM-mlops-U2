from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import uvicorn 

from database.database import init_db, insert_patient_data, get_all_patient_data
from backend.logic import evaluar_paciente, validar_rango_medico

app = FastAPI(title="MLops Taller 1 Evaluacion Medica")

templates = Jinja2Templates(directory="templates")

init_db()

class PatientData(BaseModel):
    temperatura: float
    presion_arterial: float
    frecuencia_cardiaca: int
    frecuencia_respiratoria: int
    nivel_oxigeno: float

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
    error_validacion = validar_rango_medico(temperatura, presion_arterial, frecuencia_cardiaca, frecuencia_respiratoria, nivel_oxigeno)
    
    if error_validacion:
        return templates.TemplateResponse(request=request, name="index.html", context={
            "error": error_validacion,
            "temp": temperatura, "presion": presion_arterial, "fc": frecuencia_cardiaca, "fr": frecuencia_respiratoria, "oxigeno": nivel_oxigeno
        })
    
    resultado = evaluar_paciente(temperatura, presion_arterial,
                frecuencia_cardiaca, frecuencia_respiratoria, nivel_oxigeno)

    # Persistir en la base de datos
    insert_patient_data(temperatura, presion_arterial, frecuencia_cardiaca, 
                       frecuencia_respiratoria, nivel_oxigeno, resultado)

    return templates.TemplateResponse(request=request, name="index.html", context={
        "resultado": resultado,
        "temp": temperatura,
        "presion": presion_arterial,
        "fc": frecuencia_cardiaca,
        "fr": frecuencia_respiratoria,
        "oxigeno": nivel_oxigeno
    })


@app.get("/stats", response_class=HTMLResponse)
async def ver_estadisticas_html(request: Request):
    datos_estadisticas = get_all_patient_data()
    return templates.TemplateResponse(request=request, name="stats.html", context={
        "stats": datos_estadisticas
    })

if __name__ == '__main__':
    uvicorn.run("main:app", host='0.0.0.0', port=8000, reload=True)