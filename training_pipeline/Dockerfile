FROM python:3.12-slim

WORKDIR /app

COPY . .

#RUN #pip install --no-cache-dir mlflow xgboost scikit-learn pandas

RUN pip install --no-cache-dir mlflow xgboost

EXPOSE 5000

CMD ["mlflow", "server", "--backend-store-uri", "file:/app/mlruns", "--default-artifact-root", "/app/mlartifacts", "--host", "0.0.0.0", "--port", "5000"]
