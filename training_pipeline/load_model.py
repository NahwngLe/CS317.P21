import mlflow
import numpy as np

mlflow.set_tracking_uri('http://localhost:5000')

test_sample = np.array([
    6, 609, 7, 4, 484, 414, 233, 0, 69.14286, 111.967896, 207, 0, 103.5, 119.511505,
    1474548.44, 18062.39737, 60.9, 115.194954, 381, 2, 609, 101.5, 177.08952, 460, 2,
    467, 155.66667, 263.56088, 460, 3, 0, 0, 0, 0, 164, 104, 11494.253, 6568.1445, 0,
    233, 74.833336, 107.52744, 11562.151, 0, 0, 0, 1, 0, 0, 0, 0, 0, 81.63636, 69.14286,
    103.5, 0, 0, 0, 0, 0, 0, 7, 484, 4, 414, 8192, 2053, 5, 20, 0, 0, 0, 0, 0, 0, 0, 0
])
test_sample = test_sample.reshape(1, -1)

test_label = "Attack"

model_name = "XGBoost"
model_version = 1
model_uri = f"models:/{model_name}/{model_version}"

load_model = mlflow.sklearn.load_model(model_uri)
y_pred = load_model.predict(test_sample)

print("Predict:", "Benign" if y_pred[0] < 0.5 else "Attack")
print("True label: Attack")
