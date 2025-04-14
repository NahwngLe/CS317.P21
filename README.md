# Phát hiện bất thường mạng với Python và MLflow trên CICIDS2017

Dự án này sử dụng Python và MLflow để phát hiện bất thường mạng trên tập dữ liệu CICIDS2017.

## Giới thiệu

CICIDS2017 là một tập dữ liệu phổ biến được sử dụng để đánh giá các hệ thống phát hiện xâm nhập mạng. Dự án này nhằm mục đích xây dựng và đánh giá các mô hình học máy để phát hiện các bất thường trong lưu lượng mạng.

## Thành viên nhóm:
- Lê Quý Nhân - 22520999
- Bùi Minh Quân - 22521173
- Nguyễn Phạm Tiến Đạt - 22520217

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

Dự án này sử dụng mô hình MLP, XGBoost để phát hiện bất thường mạng thông qua bộ dữ liệu CICIDS2017.

## MLflow

MLflow được sử dụng để theo dõi các thí nghiệm, ghi lại các tham số, metrics và artifacts. Bạn có thể xem kết quả trong MLflow UI.

## Kết quả

Kết quả của dự án này được ghi lại trong MLflow. Bạn có thể xem các kết quả trong MLflow UI.

## Hình ảnh Demo

![Screenshot 2025-04-14 115447](https://github.com/user-attachments/assets/c309db2f-7b70-410e-9b50-62056b257849)

![Screenshot 2025-04-14 115422](https://github.com/user-attachments/assets/a8de4305-4342-4be1-9405-b9c957a969e7)

![491010114_688199713574516_5695982584423680773_n](https://github.com/user-attachments/assets/491bcb8e-ef7c-4fa5-a5e9-93d78dc78a90)

![483682444_641587248748952_913109542874550237_n](https://github.com/user-attachments/assets/77a07f15-0ee2-4fe4-afab-73bdc5b8f0c5)

![482842237_1989233068153219_7961432184739762084_n](https://github.com/user-attachments/assets/cfab2cac-5a07-46f6-a3b4-d379975cd20d)

![491026607_1460727028670256_1670560323149226156_n](https://github.com/user-attachments/assets/bc981d9f-ce40-4a40-b483-5294e2b38299)

![Screenshot 2025-04-14 115806](https://github.com/user-attachments/assets/e0db0845-bf81-4b06-8fd6-45e8b180560d)

## Demo
https://drive.google.com/file/d/1qsrdkCoRoceD5wUY-S3fakloE2FlWxGL/view?usp=drive_link

## Đóng góp

Đóng góp cho dự án này được hoan nghênh. Vui lòng tạo pull request nếu bạn có bất kỳ cải tiến nào.

## Liên hệ

Nếu bạn có bất kỳ câu hỏi hoặc nhận xét nào, vui lòng liên hệ với nhan.lequy12@gmail.com.

## Notebook tham khảo
[MLflow : End-to-end ML models](https://www.kaggle.com/code/sharanharsoor/mlflow-end-to-end-ml-models#Loading-and-visualising-a-model)
