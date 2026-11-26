FROM python:3.13-slim

WORKDIR /app
COPY pyproject.toml ./
COPY omnicore_ai_api ./omnicore_ai_api
RUN pip install --no-cache-dir .
EXPOSE 8001
CMD ["uvicorn", "omnicore_ai_api.main:app", "--host", "0.0.0.0", "--port", "8001"]
