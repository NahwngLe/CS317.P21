# Phát hiện bất thường mạng với Python và MLflow trên CICIDS2017

Dự án này sử dụng Python và MLflow để phát hiện bất thường mạng trên tập dữ liệu CICIDS2017.

## Giới thiệu

CICIDS2017 là một tập dữ liệu phổ biến được sử dụng để đánh giá các hệ thống phát hiện xâm nhập mạng. Dự án này nhằm mục đích xây dựng và đánh giá các mô hình học máy để phát hiện các bất thường trong lưu lượng mạng.

## Thành viên nhóm:
- Lê Quý Nhân - 22520999

## Cài đặt

1.  **Clone repository:**

    ```bash
    git clone https://github.com/NahwngLe/CS317.P21.git
    ```

2.  **Tạo môi trường ảo (khuyến nghị):**

    ```bash
    python3 -m venv venv
    source venv/bin/activate  # Trên Linux/macOS
    venv\Scripts\activate  # Trên Windows
    ```

3.  **Cài đặt các thư viện cần thiết:**

    ```bash
    pip install -r requirements.txt
    ```
    
## Dữ liệu
Tập dữ liệu CICIDS2017 có thể được tải xuống từ [đây](https://www.kaggle.com/datasets/dhoogla/cicids2017). Đặt tập dữ liệu vào thư mục `data/` trong dự án. Bạn sẽ thấy các tệp `parquet` tương ứng với từng ngày và loại tấn công:

* `Benign-Monday-no-metadata.parquet`
* `Botnet-Friday-no-metadata.parquet`
* `Bruteforce-Tuesday-no-metadata.parquet`
* `DDoS-Friday-no-metadata.parquet`
* `DoS-Wednesday-no-metadata.parquet`
* `Infiltration-Thursday-no-metadata.parquet`
* `Portscan-Friday-no-metadata.parquet`
* `WebAttacks-Thursday-no-metadata.parquet`

## Sử dụng
1. **Khởi động MLflow UI**
    ```bash
    mlflow ui
    ```
    Truy cập vào đường link hiện ra trong terminal hoặc [localhost](http://127.0.0.1:5000/)
    
2.  **Chạy pipeline tiền xử lý và huấn luyện mô hình:**

    ```bash
    python main.py
    ```

    Điều này sẽ chạy pipeline tiền xử lý dữ liệu, huấn luyện mô hình và ghi lại các kết quả vào MLflow.

3.  **Xem kết quả trong MLflow UI:**


## Cấu trúc thư mục
```
cicids2017-anomaly-detection/
├── assest/
├── data/
│   ├── Benign-Monday-no-metadata.parquet
│   ├── Botnet-Friday-no-metadata.parquet
│   ├── Bruteforce-Tuesday-no-metadata.parquet
│   ├── DDoS-Friday-no-metadata.parquet
│   ├── DoS-Wednesday-no-metadata.parquet
│   ├── Infiltration-Thursday-no-metadata.parquet
│   ├── Portscan-Friday-no-metadata.parquet
│   └── WebAttacks-Thursday-no-metadata.parquet
├── utils/
│   ├── __init__.py
│   ├── tunning.py
│   └── utils.py
├── venv/
├── .gitignore
├── main.py
└── README.md
```


## Mô hình

Dự án này sử dụng mô hình MLP, XGBoost để phát hiện bất thường mạng.

## MLflow

MLflow được sử dụng để theo dõi các thí nghiệm, ghi lại các tham số, metrics và artifacts. Bạn có thể xem kết quả trong MLflow UI.

## Kết quả

Kết quả của dự án này được ghi lại trong MLflow. Bạn có thể xem các kết quả trong MLflow UI.

## Đóng góp

Đóng góp cho dự án này được hoan nghênh. Vui lòng tạo pull request nếu bạn có bất kỳ cải tiến nào.

## Liên hệ

Nếu bạn có bất kỳ câu hỏi hoặc nhận xét nào, vui lòng liên hệ với nhan.lequy12@gmail.com.

## Notebook tham khảo
[MLflow : End-to-end ML models](https://www.kaggle.com/code/sharanharsoor/mlflow-end-to-end-ml-models#Loading-and-visualising-a-model)
