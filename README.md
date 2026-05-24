# Servicio de Evaluación Clínica — MLOps Taller 1

## punto 1
1. Diseño: Restricciones, Limitaciones y Datos

Restricciones y Limitaciones:

Desbalanceo de Clases Extremo: La principal limitación es la escasez de registros para enfermedades huérfanas frente a la abundancia de datos para enfermedades comunes. Entrenar un modelo único generaría un sesgo (bias) fuerte hacia la clase mayoritaria, produciendo falsos negativos críticos en diagnósticos de enfermedades raras.

Privacidad y Seguridad (Cumplimiento Normativo): Al tratar con información médica de pacientes, existen restricciones legales estrictas sobre la anonimización y el manejo de datos sensibles.

Frecuencia de Actualización: Las enfermedades huérfanas presentan nuevos casos con muy baja frecuencia, lo que dificulta establecer ventanas de re-entrenamiento periódicas estándar.

Tipos de Datos:

Se trabajará principalmente con datos tabulares extraídos de Historias Clínicas Electrónicas (EHR). Esto incluye variables continuas (temperatura, presión arterial), variables categóricas (síntomas presentados) y resultados numéricos de exámenes de laboratorio (ej. cuadros hemáticos, perfiles bioquímicos).

2. Desarrollo: Fuentes, Manejo de Datos y Modelado

Fuentes y Manejo de Datos (Pipeline ETL):

Fuentes: Integración de múltiples orígenes, como bases de datos gubernamentales de salud pública, registros internos de clínicas asociadas y datasets médicos anonimizados de consorcios de investigación.

Procesamiento: Es fundamental un pipeline robusto que realice la ingesta, limpieza e igualación de columnas. Esto implica normalizar la nomenclatura clínica, estandarizar las unidades y manejar valores nulos. Se sugiere el uso de herramientas como Great Expectations para validar la calidad de los datos médicos antes de consolidarlos en un Feature Store centralizado.

Estrategia de Modelado (Arquitectura de Ensamble por Stacking):
Dado el desafío del desbalanceo, se propone un enfoque de ejecución paralela con fusión tardía (Late Fusion o Stacking):

Modelo de Enfermedades Comunes: Un modelo de clasificación tradicional (ej. XGBoost) robusto y optimizado para la clase mayoritaria.

Modelo de Enfermedades Huérfanas: Un modelo especializado en detectar patrones atípicos o entrenado con técnicas de Few-Shot Learning para las clases minoritarias.

Modelo Juez (Meta-Learner): Ambos modelos base ejecutan sus predicciones en paralelo. Estos resultados alimentan a un modelo "juez" final (desarrollado en frameworks como PyTorch) que evalúa las salidas de ambos modelos para tomar la decisión definitiva. Este juez aprende a ponderar en qué modelo confiar según el contexto de la predicción.

Validación y Pruebas:

Se realizará una división de datos utilizando muestreo estratificado (stratified split) para garantizar que las enfermedades huérfanas estén representadas tanto en train como en test.

Tras la validación offline con métricas como F1-Score (priorizando el Recall), el modelo empaquetado se almacenará en un Model Registry (ej. MLflow). Posteriormente, se implementará un despliegue en modo Shadow en entornos clínicos reales: el modelo hará predicciones silenciosas para comparar su rendimiento con el criterio de los médicos antes de tomar decisiones activas.

3. Producción: Despliegue, Monitoreo y Retraining

Despliegue de la Solución:

La solución debe ser empaquetada en contenedores (Docker) para garantizar la consistencia.

Se expondrá mediante una API rápida y segura (ej. FastAPI). La arquitectura debe contemplar Control de Acceso Basado en Roles (RBAC), ya que la interfaz y los permisos variarán si el usuario es un paciente desde su casa o un profesional de la salud con acceso a datos sensibles.

Monitoreo (Observabilidad):

Métricas Operacionales: Uso de dashboards interactivos (Prometheus + Grafana) para monitorear la latencia, el uptime y la tasa de requests de la API.

Métricas de ML: Monitoreo continuo del Data Drift y Concept Drift utilizando librerías especializadas en datos tabulares (ej. Evidently AI o NannyML). Se compararán las distribuciones de los datos de entrada en tiempo real frente a los datos de entrenamiento.

Re-entrenamiento Continuo (CT):

El pipeline incluirá un flujo orquestado mediante DAGs en Airflow. Este orquestador disparará una alerta y ejecutará un nuevo ciclo de entrenamiento (leyendo los datos actualizados del Feature Store) cuando se detecte un drift significativo en el monitoreo o cuando se acumule un volumen predefinido de nuevos casos de enfermedades huérfanas.

### Diagrama del Pipeline

![Diagrama del Pipeline MLOps](Diagram.png)

## Punto 2

Servicio contenerizado con **FastAPI** que permite evaluar el estado de salud de un paciente a partir de 5 signos vitales. Retorna una clasificación de riesgo: **Bajo riesgo**, **Riesgo moderado** o **Alto riesgo**.

## Parámetros del modelo

| Parámetro               | Tipo  | Descripción                        |
|--------------------------|-------|------------------------------------|
| `temperatura`            | float | Temperatura corporal en °C         |
| `presion_arterial`       | float | Presión arterial sistólica (mmHg)  |
| `frecuencia_cardiaca`    | int   | Frecuencia cardíaca (bpm)          |
| `frecuencia_respiratoria`| int   | Frecuencia respiratoria (rpm)      |
| `nivel_oxigeno`          | float | Saturación de oxígeno (% SpO2)     |

## Lógica de predicción

Cada parámetro se evalúa individualmente y suma puntos de riesgo (0, 1 o 2). La suma total determina la clasificación:

- **0–2 puntos** → Bajo riesgo
- **3–5 puntos** → Riesgo moderado
- **6+ puntos** → Alto riesgo

## 1. Construir la imagen de Docker

```bash
docker build -t mlopstaller1 .
```

## 2. Correr el contenedor

```bash
docker run -p 8000:8000 mlopstaller1
```

El servicio estará disponible en `http://localhost:8000`.

## 3. Obtener predicciones

### Opción A: Interfaz web

Abre `http://localhost:8000` en tu navegador. Ingresa los 5 signos vitales y presiona **Evaluar Paciente**.

### Opción B: API REST con `curl`

```bash
curl -X POST http://localhost:8000/api/predict \
  -H "Content-Type: application/json" \
  -d '{
    "temperatura": 39.0,
    "presion_arterial": 150,
    "frecuencia_cardiaca": 110,
    "frecuencia_respiratoria": 22,
    "nivel_oxigeno": 88.0
  }'
```

Respuesta esperada:

```json
{"resultado": "Alto riesgo"}
```

## Tecnologías

- Python 3.12
- FastAPI + Uvicorn
- Jinja2 (templates HTML)
- Docker


## Punto 2: Mejoras y nuevas funcionalidades

1. **Nuevo requerimiento funcional:**
  - Se añadió la funcionalidad para calcular y mostrar estadísticas de los pacientes evaluados, accesible desde la interfaz web.

2. **Integración de base de datos:**
  - Se integró una base de datos SQLite para almacenar los registros de las evaluaciones médicas.
  - El backend permite guardar y consultar los resultados históricos de los pacientes, facilitando el análisis y la trazabilidad.

3. **Página de estadísticas:**
  - Se creó una nueva vista (`/stats`) que muestra estadísticas agregadas de las evaluaciones realizadas, como el conteo por nivel de riesgo.

4. **Automatización con GitHub Actions:**
  - Se añadieron dos flujos de trabajo para CI/CD:
    - **Evento 1 - PR:** Ejecuta pruebas automáticas en cada Pull Request y en cada push a `main`.
    - **Evento 2 - Merge a Main:** Tras completar el workflow anterior en `main`, ejecuta pruebas y despliega la imagen Docker en GitHub Packages.

Puedes ver la imagen generada automáticamente en:
https://github.com/sam2800ml/santiagoAristizabalM-mlops-U2/pkgs/container/santiagoaristizabalm-mlops-u2%2Fevaluacion-medica