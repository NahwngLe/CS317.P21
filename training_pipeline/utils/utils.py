import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns

import time
import xgboost as xgb
from sklearn.preprocessing import LabelEncoder, Normalizer, QuantileTransformer, RobustScaler
from sklearn.model_selection import train_test_split

# for evaluation
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
# for SMOTE
from imblearn.over_sampling import SMOTE
# for I/O & automatic EDA
import os

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.callbacks import ModelCheckpoint

from keras import layers, Sequential
from keras.layers import Input, Dense
from keras.initializers import GlorotUniform, HeUniform
from keras.models import load_model

# for the customization of the model and the training process
from keras.callbacks import EarlyStopping, ReduceLROnPlateau
from keras.utils import plot_model

import mlflow
import mlflow.tensorflow
import mlflow.keras
from mlflow.models.signature import infer_signature
import warnings
warnings.filterwarnings("ignore")

from training_pipeline.utils.tunning import *

def data_preperation(data_path, seed=1802):
    seed = 1802

    np.random.seed(seed)
    tf.random.set_seed(seed)

    for dir_name, _, file_names in os.walk(data_path):
        for file_name in file_names:
            print(os.path.join(dir_name, file_name))

    df_1 = pd.read_parquet(f'{data_path}/Benign-Monday-no-metadata.parquet')
    df_2 = pd.read_parquet(f'{data_path}/Bruteforce-Tuesday-no-metadata.parquet')
    df_3 = pd.read_parquet(f'{data_path}/Portscan-Friday-no-metadata.parquet')
    df_4 = pd.read_parquet(f'{data_path}/WebAttacks-Thursday-no-metadata.parquet')
    df_5 = pd.read_parquet(f'{data_path}/DoS-Wednesday-no-metadata.parquet')
    df_6 = pd.read_parquet(f'{data_path}/DDoS-Friday-no-metadata.parquet')
    df_7 = pd.read_parquet(f'{data_path}/Infiltration-Thursday-no-metadata.parquet')
    df_8 = pd.read_parquet(f'{data_path}/Botnet-Friday-no-metadata.parquet')

    # Concatenating df
    df = pd.concat([df_1, df_2, df_3, df_4, df_5, df_6, df_7, df_8], axis=0, ignore_index=True)
    df.info()
    return df


def preprocessing_data(df, seed=1802, test_size=0.2, val_size=0.1, shuffle=True):
    # Find and drop null
    null_counts = df.isnull().sum()
    print("Nums of null values: ", null_counts.sum())
    df.dropna(inplace=True)
    print("Nums of null values after process: ", null_counts.sum())

    # Find and drop duplicated
    duplicate_count = df.duplicated().sum()
    print(f"Nums of duplicated values: {duplicate_count}")
    df.drop_duplicates(inplace=True)
    duplicate_count_after = df.duplicated().sum()
    print(f"Nums of duplicated values after process: {duplicate_count_after}")

    # Reset index after preprocessing data
    df.reset_index(drop=True, inplace=True)
    print("Index reset successfull")

    print("Categorical columns:", df.select_dtypes(include=['object']).columns.tolist(), '\n')

    # Inspection of Target Feature
    print('Inspection of Target Feature - y:\n')
    # Target feature count
    print(df['Label'].value_counts())

    # Split to train and test data
    X = df.copy()
    X = X.drop('Label', axis=1)
    y = df['Label'].copy()
    # Binarize labels
    y = y.map({'Benign': 0}).fillna(1)
    print(f"X shape: {X.shape} \ny shape: {y.shape} ")

    # Split data into train, val, test
    X_train_temp, X_test, y_train_temp, y_test = train_test_split(X, y,
                                                                  stratify=y,
                                                                  test_size=test_size,
                                                                  random_state=seed,
                                                                  shuffle=shuffle)
    X_train, X_val, y_train, y_val = train_test_split(X_train_temp, y_train_temp,
                                                      stratify=y_train_temp,
                                                      test_size=val_size,
                                                      random_state=seed,
                                                      shuffle=shuffle)
    print(X_train.shape, X_val.shape, X_test.shape, y_train.shape, y_val.shape, y_test.shape)

    # SMOTE for training data
    smote = SMOTE(sampling_strategy=0.5, random_state=seed)
    X_train, y_train = smote.fit_resample(X_train, y_train)
    print(f"Smote for Label 1 done!")
    print(X_train.shape, X_val.shape, X_test.shape, y_train.shape, y_val.shape, y_test.shape)

    # Scaler
    scaler = RobustScaler()
    X_train = scaler.fit_transform(X_train)
    X_val = scaler.transform(X_val)
    X_test = scaler.transform(X_test)
    print(f"RobustScaler done.")

    return X_train, X_val, X_test, y_train, y_val, y_test

def training_model_nn(X_train, X_val, y_train, y_val, model, model_name, run_name, optimizer="adam", loss="binary_crossentropy", metrics=["accuracy"], experiment_name="Default", dataset_link=""):
    mlflow.set_tracking_uri('http://127.0.0.1:5000/')
    mlflow.set_experiment(experiment_name=experiment_name)

    # Define Early Stopping
    early_stopping = EarlyStopping(
        monitor="val_accuracy",
        patience=10,
        verbose=1,
        restore_best_weights=True
    )

    # Define ReduceLROnPlateau
    reduce_lr = ReduceLROnPlateau(
        monitor='val_accuracy',
        patience=5,
        min_lr=1e-07,
        verbose=5,
        factor=0.1
    )

    # Define checkpoint callback
    checkpoint_filepath = f'models/{model_name}_checkpoint.keras'
    checkpoint_callback = ModelCheckpoint(
        filepath=checkpoint_filepath,
        monitor='val_loss',
        save_best_only=True,
        verbose=1
    )

    with mlflow.start_run(run_name=run_name, nested=True) as run:
        run_id = run.info.run_id  # Get the run_id
        model.compile(optimizer=optimizer, loss=loss, metrics=metrics)
        print(f"This training session corresponds to '{model_name}'. \n")

        # Log model parameters
        mlflow.log_param("model_name", model_name)
        mlflow.log_param("dataset_url", dataset_link)
        mlflow.log_param("num_layers", len(model.layers))
        mlflow.log_param("optimizer", optimizer)
        mlflow.log_param("loss", loss)

        # Training session
        history = model.fit(X_train, y_train, validation_data=(X_val, y_val), epochs=100, verbose=1,
                            batch_size=1024, callbacks=[early_stopping, reduce_lr, checkpoint_callback])

        # Log checkpoint as artifact
        mlflow.log_artifact(checkpoint_filepath)

        # Log metrics
        for epoch, (loss, accuracy, val_loss, val_accuracy) in enumerate(zip(
                history.history['loss'], history.history['accuracy'],
                history.history['val_loss'], history.history['val_accuracy'])):
            mlflow.log_metric("loss", loss, step=epoch)
            mlflow.log_metric("accuracy", accuracy, step=epoch)
            mlflow.log_metric("val_loss", val_loss, step=epoch)
            mlflow.log_metric("val_accuracy", val_accuracy, step=epoch)

        # Log model
        try:
            signature = infer_signature(X_train, model.predict(X_train[:5]))
            mlflow.keras.log_model(model, "model", signature=signature)
        except Exception as e:
            print(f"Error inferring signature: {e}")
            mlflow.keras.log_model(model, "model")

        # Log plots
        plt.figure()
        plt.plot(history.history['loss'], label='loss')
        plt.plot(history.history['val_loss'], label='val_loss')
        plt.legend()
        plt.savefig("loss_plot.png")
        mlflow.log_artifact("loss_plot.png")
        plt.close()

        plt.figure()
        plt.plot(history.history['accuracy'], label='accuracy')
        plt.plot(history.history['val_accuracy'], label='val_accuracy')
        plt.legend()
        plt.savefig("accuracy_plot.png")
        mlflow.log_artifact("accuracy_plot.png")
        plt.close()

    return history, model, run_id

def training_model_traditional(X_train, X_val, y_train, y_val, model_name, run_name, experiment_name="Default", dataset_link=""):
    mlflow.set_tracking_uri('http://127.0.0.1:5000/')
    mlflow.set_experiment(experiment_name=experiment_name)

    with mlflow.start_run(run_name=run_name, nested=True) as run:
        run_id = run.info.run_id
        checkpoint_dir = "models"
        iterations  = 20
        checkpoint_prefix = f"{model_name}_checkpoint"

        os.makedirs("models", exist_ok=True)

        if model_name == "xgboost":
            best_param = tune_and_log(X_train, y_train, X_val, y_val,
                                      "XgboostOptunaTunning",
                                      n_trials=20)
            model = xgb.XGBClassifier(**best_param)
            mlflow.log_params(best_param)

        model.fit(X_train, y_train, eval_set=[(X_val, y_val)], early_stopping_rounds=10,
                  verbose=False, callbacks=[xgb.callback.TrainingCheckPoint(directory ="models",
                                                                            name=f"{model_name}_checkpoint",
                                                                            iterations =100 )])

        mlflow.log_params(model.get_params())
        mlflow.sklearn.log_model(model, "model")

        # Find latest check point and log to artifact
        checkpoint_files = [f for f in os.listdir(checkpoint_dir) if f.startswith(checkpoint_prefix)]
        if checkpoint_files:
            latest_checkpoint = max(checkpoint_files)
            latest_checkpoint_path = os.path.join(checkpoint_dir, latest_checkpoint)

            mlflow.log_artifact(latest_checkpoint_path)
        else:
            print("Không tìm thấy tệp checkpoint.")

        y_pred_val = model.predict(X_val)

        # Calculate and log metrics
        accuracy = accuracy_score(y_val, y_pred_val)

        mlflow.log_metric("val_accuracy", accuracy)

        # Log val_loss (if available)
        if hasattr(model, 'evals_result') and model.evals_result():
            val_loss = model.evals_result()['validation_0']['logloss'][-1]
            mlflow.log_metric("val_loss", val_loss)
        elif hasattr(model, 'evals_result_') and model.evals_result_():
            val_loss = model.evals_result_['validation']['Logloss'][-1]
            mlflow.log_metric("val_loss", val_loss)

    return model, run_id
def evaluate_model(X_test, y_test, model, run_id, experiment_name="Default"):
    mlflow.set_tracking_uri('http://127.0.0.1:5000/')
    mlflow.set_experiment(experiment_name=experiment_name)

    with mlflow.start_run(run_id=run_id, nested=True):
        loss, accuracy = model.evaluate(X_test, y_test)
        # Make prediction
        y_pred = model.predict(X_test)
        # Convert predicted probabilities to class labels
        y_pred_labels = (y_pred > 0.5).astype(int)
        # Caculation Precision, Recall, F1_score
        precision = precision_score(y_test, y_pred_labels)
        recall = recall_score(y_test, y_pred_labels)
        f1 = f1_score(y_test, y_pred_labels)
        mlflow.log_metric("test_loss", loss)
        mlflow.log_metric("test_accuracy", accuracy)
        mlflow.log_metric("precision", precision)
        mlflow.log_metric("recall", recall)
        mlflow.log_metric("f1_score", f1)

def evaluate_xgboost_model(X_test, y_test, model, run_id, experiment_name="Default"):
    mlflow.set_tracking_uri('http://127.0.0.1:5000/')
    mlflow.set_experiment(experiment_name=experiment_name)

    with mlflow.start_run(run_id=run_id, nested=True):
        # Dự đoán nhãn
        y_pred = model.predict(X_test)

        # Tính các chỉ số đánh giá
        accuracy = accuracy_score(y_test, y_pred)
        precision = precision_score(y_test, y_pred)
        recall = recall_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred)

        # Ghi log vào MLflow
        mlflow.log_metric("accuracy", accuracy)
        mlflow.log_metric("precision", precision)
        mlflow.log_metric("recall", recall)
        mlflow.log_metric("f1_score", f1)

def create_nn_model(input_dim, type):
    if type == "MLP_7layer":
        model = keras.Sequential([
            Input(shape=(input_dim,)),
            Dense(32, activation='sigmoid', kernel_initializer=GlorotUniform()),
            Dense(16, activation='relu', kernel_initializer=HeUniform()),
            Dense(8, activation='relu', kernel_initializer=HeUniform()),
            Dense(4, activation='relu', kernel_initializer=HeUniform()),
            Dense(2, activation='relu', kernel_initializer=HeUniform()),
            Dense(1, activation='sigmoid', kernel_initializer=GlorotUniform()),
        ])
        return model
    elif type == "MLP_10layer":
        model = keras.Sequential([
            Input(shape=(input_dim,)),
            Dense(256, activation='tanh', kernel_initializer=GlorotUniform()),
            Dense(128, activation='selu', kernel_initializer=HeUniform()),
            Dense(64,  activation='selu', kernel_initializer=HeUniform()),
            Dense(32,  activation='selu', kernel_initializer=HeUniform()),
            Dense(16,  activation='selu', kernel_initializer=HeUniform()),
            Dense(8,   activation='selu', kernel_initializer=HeUniform()),
            Dense(4,   activation='selu', kernel_initializer=HeUniform()),
            Dense(2,   activation='selu', kernel_initializer=HeUniform()),
            Dense(1,   activation='sigmoid', kernel_initializer=GlorotUniform())
        ])
        return model

def train_and_evaluate_nn(X_train, X_val, X_test, y_train, y_val, y_test, model, model_name, run_name, optimizer, loss, metrics, experiment_name, dataset_link):
    history, trained_model, run_id = training_model_nn(X_train, X_val, y_train, y_val, model, model_name, run_name, optimizer, loss, metrics, experiment_name, dataset_link)
    evaluate_model(X_test, y_test, trained_model, run_id, experiment_name)

def train_and_evaluate_xgboost(X_train, X_val, X_test, y_train, y_val, y_test, model_name, run_name, experiment_name, dataset_link):
    trained_model, run_id = training_model_traditional(X_train, X_val, y_train, y_val, model_name, run_name, experiment_name, dataset_link)
    evaluate_xgboost_model(X_test, y_test, trained_model, run_id, experiment_name)

def pipeline(data_path, dataset_link, model_type, model_params, experiment_name):
    """
        Hàm pipeline thực hiện toàn bộ quy trình huấn luyện mô hình học máy bao gồm:
        - Đọc và xử lý dữ liệu
        - Tiền xử lý (chuẩn hóa, chia tập train/val/test)
        - Tạo mô hình theo loại được chọn (NN hoặc XGBoost)
        - Huấn luyện và đánh giá mô hình, log kết quả với MLflow

        Tham số:
            data_path (str): Đường dẫn đến file dữ liệu gốc
            model_type (str): Loại mô hình sử dụng ("nn" cho neural network hoặc "xgboost")
            model_params (dict): Dictionary chứa các tham số cấu hình cho mô hình
            experiment_name (str): Tên experiment trên MLflow để lưu kết quả
    """
    df = data_preperation(data_path)

    X_train, X_val, X_test, y_train, y_val, y_test = preprocessing_data(df)
    input_dim = X_train.shape[1]

    if model_type == "nn":
        model = create_nn_model(input_dim, model_params["model_name"])
        train_and_evaluate_nn(X_train, X_val, X_test, y_train, y_val, y_test, model,
                              model_params["model_name"], model_params["run_name"],
                              model_params["optimizer"], model_params["loss"], model_params
                              ["metrics"], experiment_name, dataset_link)
    elif model_type == "xgboost":
        train_and_evaluate_xgboost(X_train, X_val, X_test, y_train, y_val, y_test,
                                   model_params["model_name"], model_params["run_name"],
                                   experiment_name, dataset_link)
    else:
        raise ValueError("Invalid model type")