FROM python:3.12-slim

WORKDIR /app

# Copiamos todo tu código tal cual está
COPY . /app

# Instalamos las dependencias explícitamente a la antigua, sin usar el pyproject.toml para evitar el error de carpetas
RUN pip install --no-cache-dir fastapi uvicorn pydantic jinja2 python-multipart pytest

EXPOSE 8000

# Arrancamos la aplicación
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]