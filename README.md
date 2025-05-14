# Phát hiện bất thường mạng với Python và MLflow trên CICIDS2017

Dự án này sử dụng Python và MLflow để phát hiện bất thường mạng trên tập dữ liệu CICIDS2017.

## Giới thiệu

CICIDS2017 là một tập dữ liệu phổ biến được sử dụng để đánh giá các hệ thống phát hiện xâm nhập mạng. Dự án này nhằm mục đích xây dựng và đánh giá các mô hình học máy để phát hiện các bất thường trong lưu lượng mạng.

MLflow là một nền tảng mã nguồn mở dùng để quản lý vòng đời của mô hình học máy, từ việc thử nghiệm, huấn luyện, đến triển khai. Nó giúp dễ dàng theo dõi, quản lý và chia sẻ các mô hình học máy trong môi trường sản xuất. Các tính năng chính của MLflow bao gồm:

* Tracking: Ghi lại các tham số, metrics, mô hình, và artifacts từ các thử nghiệm huấn luyện để dễ dàng theo dõi và so sánh.

* Projects: Tổ chức mã nguồn, giúp tái sử dụng và chia sẻ mã nguồn huấn luyện mô hình.

* Models: Quản lý và triển khai các mô hình học máy dưới dạng chuẩn (standard formats) như TensorFlow, PyTorch, Scikit-learn, v.v.

* Registry: Quản lý các phiên bản mô hình, cho phép lưu trữ, theo dõi và triển khai các mô hình từ các môi trường khác nhau.

MLflow hỗ trợ mọi giai đoạn trong quá trình phát triển mô hình, từ việc thử nghiệm các hyperparameters đến triển khai mô hình sản xuất một cách có tổ chức và hiệu quả.

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

### Màn hình MLflow Ui với experiment Anomaly Detection với các model trainning là các run name riêng biệt:

![Screenshot 2025-04-14 115447](https://github.com/user-attachments/assets/c309db2f-7b70-410e-9b50-62056b257849)

***
**Hình ảnh chi tiết từng run name**

- *Details*
  
![491010114_688199713574516_5695982584423680773_n](https://github.com/user-attachments/assets/491bcb8e-ef7c-4fa5-a5e9-93d78dc78a90)

- *Parametters* và *Metrics* của từng model.

![483682444_641587248748952_913109542874550237_n](https://github.com/user-attachments/assets/77a07f15-0ee2-4fe4-afab-73bdc5b8f0c5)

- *Artifact* nơi lưu trữ các file đầu ra của 1 run, model checkpoint.

![491026607_1460727028670256_1670560323149226156_n](https://github.com/user-attachments/assets/bc981d9f-ce40-4a40-b483-5294e2b38299)

 Màn hình MLflow Ui với experiment Hyperparameter Tuning với các trials là các run name riêng biệt để dễ dàng so sánh các trials với nhau để lựa chọn hyperparameter tốt nhất:

![Screenshot 2025-04-14 115422](https://github.com/user-attachments/assets/a8de4305-4342-4be1-9405-b9c957a969e7)

- So sánh các trials:

![482842237_1989233068153219_7961432184739762084_n](https://github.com/user-attachments/assets/cfab2cac-5a07-46f6-a3b4-d379975cd20d)


## Demo
[Demo quá trình training va flog vào MLflow](https://drive.google.com/file/d/1qsrdkCoRoceD5wUY-S3fakloE2FlWxGL/view?usp=drive_link)

## Đóng góp

Đóng góp cho dự án này được hoan nghênh. Vui lòng tạo pull request nếu bạn có bất kỳ cải tiến nào.

## Liên hệ

Nếu bạn có bất kỳ câu hỏi hoặc nhận xét nào, vui lòng liên hệ với nhan.lequy12@gmail.com.

## Notebook tham khảo
[MLflow : End-to-end ML models](https://www.kaggle.com/code/sharanharsoor/mlflow-end-to-end-ml-models#Loading-and-visualising-a-model)
