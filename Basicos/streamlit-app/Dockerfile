FROM python:3.11-slim AS base


# 2) Variáveis de ambiente para produção
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    APP_HOME=/app \
    APP_ENV=production \
    APP_NAME="Streamlit Docker App"

RUN groupadd -r app && useradd -r -g app app
WORKDIR ${APP_HOME}
RUN chown -R app:app ${APP_HOME}
COPY --chown=app:app requirements.txt ${APP_HOME}/
RUN pip install --no-cache-dir -r requirements.txt
COPY --chown=app:app . ${APP_HOME}
EXPOSE 8501
HEALTHCHECK --interval=30s --timeout=3s --start-period=10s --retries=3 CMD curl -fsS http://localhost:8501/ || exit 1
USER app
CMD ["streamlit", "run", "app.py", "--server.address=0.0.0.0"]