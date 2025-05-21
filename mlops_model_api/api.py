from fastapi import FastAPI
import mlflow
import numpy as np

mlflow.set_tracking_uri("http://mlflow:5000/")

model_uri = "models:/XGBoost/1"
model = mlflow.sklearn.load_model(model_uri)

app = FastAPI()

@app.get("/")
def get_root():
    return {"Message": "Welcome to ModelCICIDS2017 API, please use post and reach the Api endpoint /predict({data}) to use model"}


@app.post("/predict")
async def predict(data: dict):
    """
    Predict the class of a given set of features

    Args:
        data (dict): {"feature": [f1, f2, ..., f78]}

    Returns:
        dict: {"predicted_class": 0 or 1}
    """
    try:
        features = np.array(data["feature"]).reshape(1, -1)
        prediction = model.predict(features)
        return {"predicted_class": "Benign" if int(prediction[0]) == 0 else "Not Benign"}
    except Exception as e:
        return {"error": str(e)}