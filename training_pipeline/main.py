import xgboost as xgb

from utils.utils import *

import warnings
warnings.filterwarnings("ignore")

# Example usage
model_nn_10layer_params = {
    "model_name": "MLP_10layer",
    "run_name": "MLP_10layer_run",
    "optimizer": "adam",
    "loss": "binary_crossentropy",
    "metrics": ["accuracy"]
}

model_nn_7layer_params = {
    "model_name": "MLP_7layer",
    "run_name": "MLP_7layer_run",
    "optimizer": "adam",
    "loss": "binary_crossentropy",
    "metrics": ["accuracy"]
}


model_xgboost_params = {
    "model_name": "xgboost",
    "run_name": "xgboost_run",
}
dataset_link = "https://www.kaggle.com/datasets/dhoogla/cicids2017"

pipeline("training_pipeline/data", dataset_link, "nn", model_nn_7layer_params, "Anomaly Detection")
pipeline("training_pipeline/data", dataset_link, "nn", model_nn_10layer_params, "Anomaly Detection")
pipeline("training_pipeline/data", dataset_link, "xgboost", model_xgboost_params, "Anomaly Detection")
