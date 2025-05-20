FROM python:3.12-slim

COPY ../requirement.txt .

RUN pip install --no-cache-dir -r requirement.txt

EXPOSE 5000

CMD mlflow models serve -m "models:/XGBoost/1" -h 0.0.0.0 -p 5000