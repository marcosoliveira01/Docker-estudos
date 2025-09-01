FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    APP_HOME=/app

RUN apt-get update \
  && apt-get install -y --no-install-recommends gcc libpq-dev curl \
  && rm -rf /var/lib/apt/lists/*

# Cria usuário não-root
RUN groupadd -r app && useradd -r -g app app

WORKDIR ${APP_HOME}

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY --chown=app:app . ${APP_HOME}

USER app

EXPOSE 8501

HEALTHCHECK --interval=30s --timeout=3s --start-period=10s --retries=3 \
  CMD curl -fsS http://localhost:8501/ || exit 1

CMD ["streamlit", "run", "app.py", "--server.address=0.0.0.0", "--server.port=8501"]
