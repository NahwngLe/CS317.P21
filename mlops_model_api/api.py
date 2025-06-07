from fastapi import FastAPI
import mlflow
import numpy as np
import time

from prometheus_client import (
    CollectorRegistry,
    make_asgi_app,
    Histogram,
    Gauge,
)
from prometheus_fastapi_instrumentator import Instrumentator, metrics

# Load model from MLflow
mlflow.set_tracking_uri("http://mlflow:5000/")
model_uri = "models:/XGBoost/1"
model = mlflow.sklearn.load_model(model_uri)

app = FastAPI()

# ──────────────────────────────────────────────
# Custom Prometheus registry for /sysmetrics
custom_registry = CollectorRegistry()

# Custom metrics registered to the custom registry
inference_latency = Histogram(
    'model_inference_latency_seconds',
    'Model inference latency in seconds',
    registry=custom_registry
)
confidence_gauge = Gauge(
    'model_confidence_score',
    'Confidence score of model predictions',
    registry=custom_registry
)

# Expose custom registry on /sysmetrics
sysmetrics_app = make_asgi_app(registry=custom_registry)
app.mount("/sysmetrics", sysmetrics_app)

# ──────────────────────────────────────────────
# Instrumentator for default registry exposed at /metrics
instrumentator = Instrumentator(
    should_group_status_codes=False,
    should_ignore_untemplated=True,
    should_respect_env_var=True,
    should_instrument_requests_inprogress=True,
    excluded_handlers=[".*admin.*", "/metrics", "/sysmetrics"],
    env_var_name="ENABLE_METRICS",
    inprogress_name="inprogress",
    inprogress_labels=True,
)

instrumentator.add(
    metrics.latency(
        buckets=(0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1, 2.5, 5, 10)
    )
)

instrumentator.instrument(app).expose(app)


# ──────────────────────────────────────────────
@app.get("/")
def get_root():
    return {
        "Message": "Welcome to ModelCICIDS2017 API. Please POST to /predict with {'feature': [...]} to use the model."
    }


@app.post("/predict")
async def predict(data: dict):
    """
    Predict the class of a given set of features

    Args:
        data (dict): {"feature": [f1, f2, ..., f78]}

    Returns:
        dict: {"predicted_class": "Benign" or "Not Benign", "confidence_score": float}
    """
    try:
        features = np.array(data["feature"]).reshape(1, -1)

        start = time.time()
        probabilities = model.predict_proba(features)
        predicted_class = int(np.argmax(probabilities))
        confidence = float(np.max(probabilities))
        end = time.time()

        # Record custom metrics
        inference_latency.observe(end - start)
        confidence_gauge.set(confidence)

        return {
            "predicted_class": "Benign" if predicted_class == 0 else "Not Benign",
            "confidence_score": confidence
        }

    except Exception as e:
        return {"error": str(e)}
