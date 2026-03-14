# syntax=docker/dockerfile:1

# REGLA: Los comentarios proporcionan instrucciones paso a paso para configurar este archivo.
# INSTRUCCIÓN: Si necesitas más ayuda, consulta la guía de referencia de Dockerfile en
# https://docs.docker.com/go/dockerfile-reference/

ARG PYTHON_VERSION=3.12
FROM python:${PYTHON_VERSION}-slim as base

# REGLA: Previene que Python escriba archivos pyc en el disco.
ENV PYTHONDONTWRITEBYTECODE=1

# REGLA: Evita que Python almacene en búfer stdout y stderr.
ENV PYTHONUNBUFFERED=1

# INSTRUCCIÓN: Instala paquetes base del sistema necesarios para que funcione Ansible correctamente
RUN apt-get update && apt-get install -y --no-install-recommends \
    sshpass \
    openssh-client \
    iputils-ping \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# INSTRUCCIÓN: Crea un usuario sin privilegios bajo el cual se ejecutará la aplicación.
ARG UID=10001
RUN adduser \
    --disabled-password \
    --gecos "" \
    --shell "/sbin/nologin" \
    --uid "${UID}" \
    appuser

# REGLA: Utiliza un montaje de caché y descarga las dependencias como un paso separado.
RUN --mount=type=cache,target=/root/.cache/pip \
    --mount=type=bind,source=requirements.txt,target=requirements.txt \
    python -m pip install -r requirements.txt

# INSTRUCCIÓN: Cambia al usuario sin privilegios para ejecutar la aplicación.
USER appuser

# INSTRUCCIÓN: Copia el código fuente dentro del contenedor.
COPY . .

# INSTRUCCIÓN: Ejecuta la aplicación principal por defecto. 
CMD ["python", "app/main.py"]
