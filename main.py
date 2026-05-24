from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import uvicorn 

# Importaciones de tus módulos separados
from database.database import init_db, insert_patient_data, get_all_patient_data
from backend.logic import evaluar_paciente, validar_rango_medico

app = FastAPI(title="MLops Taller 1 Evaluacion Medica")

# Ruta directa a templates ya que main.py está en la raíz
templates = Jinja2Templates(directory="templates")

# Inicializar DB al arrancar la app
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
    
    # Si hay error, devolvemos el HTML con el aviso y NO guardamos en base de datos
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

@app.post("/api/predict")
async def predecir_api(datos: PatientData):
    resultado = evaluar_paciente(
        datos.temperatura, datos.presion_arterial,
        datos.frecuencia_cardiaca, datos.frecuencia_respiratoria,
        datos.nivel_oxigeno
    )
    
    # Persistir en DB desde consumo vía API
    get_all_patient_data(datos.temperatura, datos.presion_arterial, 
                       datos.frecuencia_cardiaca, datos.frecuencia_respiratoria, 
                       datos.nivel_oxigeno, resultado)
                       
    return {"resultado": resultado}

# Endpoint requerido para las métricas de los médicos
@app.get("/stats", response_class=HTMLResponse)
async def ver_estadisticas_html(request: Request):
    datos_estadisticas = get_all_patient_data()
    return templates.TemplateResponse(request=request, name="stats.html", context={
        "stats": datos_estadisticas
    })

if __name__ == '__main__':
    # Al estar en la raíz, lo ejecutas de forma normal
    uvicorn.run("main:app", host='0.0.0.0', port=8000, reload=True)