FROM python:3.12-slim AS builder

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

FROM python:3.12-slim AS runtime
RUN groupadd --gid 1001 appgroup && \
    useradd --uid 1001 --gid appgroup --no-create-home appuser

WORKDIR /app
 
COPY --from=builder /install /usr/local
 
COPY --chown=appuser:appgroup app/ ./app/
COPY --chown=appuser:appgroup templates/ ./templates/
COPY --chown=appuser:appgroup run.py .
 

USER appuser

EXPOSE 5000

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:5000/health')"

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "--threads", "2", "--timeout", "60", "run:app"]