import optuna
import mlflow
import mlflow.sklearn
import xgboost as xgb
from functools import partial
from sklearn.metrics import accuracy_score

def objective(trial, X_train, y_train, X_val, y_val):
    # Định nghĩa không gian tìm kiếm hyperparameter
    n_estimators = trial.suggest_int("n_estimators", 50, 500)
    max_depth = trial.suggest_int("max_depth", 3, 15)
    learning_rate = trial.suggest_float("learning_rate", 0.01, 0.3)
    subsample = trial.suggest_float("subsample", 0.5, 1.0)
    colsample_bytree = trial.suggest_float("colsample_bytree", 0.5, 1.0)
    gamma = trial.suggest_float("gamma", 0, 1.0)
    min_child_weight = trial.suggest_int("min_child_weight", 1, 10)
    reg_alpha = trial.suggest_float("reg_alpha", 1e-5, 1.0, log=True)
    reg_lambda = trial.suggest_float("reg_lambda", 1e-5, 1.0, log=True)

    # Khởi tạo mô hình XGBoost
    model = xgb.XGBClassifier(
        n_estimators=n_estimators,
        max_depth=max_depth,
        learning_rate=learning_rate,
        subsample=subsample,
        colsample_bytree=colsample_bytree,
        gamma=gamma,
        min_child_weight=min_child_weight,
        reg_alpha=reg_alpha,
        reg_lambda=reg_lambda,
        random_state=42
    )

    # Huấn luyện mô hình
    model.fit(X_train, y_train)

    # Dự đoán trên tập validation
    y_pred = model.predict(X_val)

    # Tính toán metric
    accuracy = accuracy_score(y_val, y_pred)

    return accuracy

def tune_and_log(X_train, y_train, X_val, y_val, run_name, n_trials=30):
    mlflow.set_experiment("Hyperparametter Tunning")
    def objective_with_mlflow(trial, run_name):
        with mlflow.start_run(run_name=run_name, nested=True):
            accuracy = objective(trial, X_train, y_train, X_val, y_val)
            mlflow.log_params(trial.params)
            mlflow.log_metric("accuracy", accuracy)
        return accuracy

    objective_with_run_name = partial(objective_with_mlflow, run_name=run_name)

    study = optuna.create_study(direction="maximize")
    study.optimize(lambda trial: objective_with_run_name(trial), n_trials=n_trials)

    best_params = study.best_params
    best_accuracy = study.best_value

    print(f"Best params: {best_params}")
    print(f"Best accuracy: {best_accuracy}")

    return best_params