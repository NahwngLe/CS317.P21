from fastapi import FastAPI
import mlflow
import numpy as np
import time
import os
import logging
import sys

from prometheus_client import (
    CollectorRegistry,
    make_asgi_app,
    Histogram,
    Gauge,
)
from prometheus_fastapi_instrumentator import Instrumentator, metrics

# ──────────────────────────────────────────────
# Load model from MLflow
mlflow.set_tracking_uri("http://mlflow:5000/")
model_uri = "models:/XGBoost/1"
model = mlflow.sklearn.load_model(model_uri)

# ──────────────────────────────────────────────

app = FastAPI()

# ──────────────────────────────────────────────
# Logging setup
os.makedirs("logs", exist_ok=True)

logger = logging.getLogger("model_api_logger")
logger.setLevel(logging.INFO)

# Log to file
file_handler = logging.FileHandler("logs/model_api.log")
file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
logger.addHandler(file_handler)

# Log to stdout
stdout_handler = logging.StreamHandler(sys.stdout)
stdout_handler.setLevel(logging.INFO)
stdout_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
logger.addHandler(stdout_handler)

# Log errors to stderr
stderr_handler = logging.StreamHandler(sys.stderr)
stderr_handler.setLevel(logging.ERROR)
stderr_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
logger.addHandler(stderr_handler)

logger.info("✅ Model API server started.")

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
        logger.info("Received prediction request.")
        features = np.array(data["feature"]).reshape(1, -1)

        start = time.time()
        probabilities = model.predict_proba(features)
        predicted_class = int(np.argmax(probabilities))
        confidence = float(np.max(probabilities))
        end = time.time()

        # Record custom metrics
        inference_latency.observe(end - start)
        confidence_gauge.set(confidence)

        logger.info(f"Predicted: {'Benign' if predicted_class == 0 else 'Not Benign'}, Confidence: {confidence:.4f}, "
                    f"Latency: {end - start:.4f}s")

        return {
            "predicted_class": "Benign" if predicted_class == 0 else "Not Benign",
            "confidence_score": confidence
        }

    except Exception as e:
        logger.error(f"Prediction error: {str(e)}", exc_info=True)
        return {"error": str(e)}
