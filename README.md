# Phát hiện bất thường mạng với Python và MLflow trên CICIDS2017

Dự án này sử dụng Python và MLflow để phát hiện bất thường mạng trên tập dữ liệu CICIDS2017.

## Giới thiệu

Dự án này nhằm xây dựng một hệ thống phát hiện xâm nhập mạng sử dụng mô hình học máy huấn luyện trên tập dữ liệu CICIDS2017 — một bộ dữ liệu phổ biến mô phỏng các loại tấn công mạng khác nhau trong môi trường thực tế. Mục tiêu chính là huấn luyện và triển khai các mô hình học máy để phát hiện các bất thường trong lưu lượng mạng một cách hiệu quả.

### 🎯 Công nghệ sử dụng
✅ **MLflow** – Quản lý vòng đời mô hình học máy
MLflow là một nền tảng mã nguồn mở giúp quản lý toàn bộ vòng đời của mô hình học máy, bao gồm:

- **Tracking**: Ghi lại các tham số, metric, mô hình, và artifact từ quá trình huấn luyện để dễ dàng theo dõi và so sánh giữa các lần thử nghiệm.


- **Projects**: Tổ chức mã nguồn huấn luyện thành các đơn vị dễ tái sử dụng và chia sẻ.


- **Models**: Quản lý mô hình ở định dạng chuẩn (Scikit-learn, XGBoost, PyTorch, TensorFlow,...).


- **Registry**: Cho phép đăng ký (register), theo dõi và triển khai các phiên bản mô hình khác nhau trong môi trường sản xuất.


✅ **FastAPI** – Triển khai mô hình dưới dạng API
Sau khi huấn luyện mô hình, chúng tôi sử dụng FastAPI để xây dựng một RESTful API cho phép người dùng gửi dữ liệu đầu vào và nhận lại dự đoán từ mô hình đã được đăng ký trong MLflow Model Registry.

**FastAPI** mang lại hiệu suất cao và cú pháp đơn giản, phù hợp cho việc triển khai nhanh các mô hình học máy.

✅ **Docker & Docker Compose** – Đóng gói và triển khai hệ thống
Để đảm bảo khả năng tái sử dụng và triển khai linh hoạt, toàn bộ hệ thống (bao gồm FastAPI và mô hình đã đăng ký từ MLflow) được đóng gói trong container bằng Docker.

Sử dụng **Docker Compose**, người dùng có thể dễ dàng khởi chạy và sử dụng Model Api bằng một lệnh duy nhất:
```bash
docker compose up --build
```

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
    cd training_pipeline
    pip install -r requirement.txt
    ```
    
## Dữ liệu
Tập dữ liệu CICIDS2017 có thể được tải xuống từ [đây](https://www.kaggle.com/datasets/dhoogla/cicids2017). Đặt tập dữ liệu vào thư mục `training_pipeline/data/` trong dự án. Bạn sẽ thấy các tệp `parquet` tương ứng với từng ngày và loại tấn công:

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
    cd training_pipeline
    mlflow ui
    ```
    Truy cập vào đường link hiện ra trong terminal hoặc [tại đây](http://127.0.0.1:5000/)
    

2.  **Chạy pipeline tiền xử lý và huấn luyện mô hình (Đã có sẵn model để dùng nếu không muốn chạy pipeline):**

    ```bash
    python main.py
    ```

    Điều này sẽ chạy pipeline tiền xử lý dữ liệu, huấn luyện mô hình và ghi lại các kết quả vào MLflow.

3.  **Xem kết quả trong MLflow UI:**
    [Tại đây](http://127.0.0.1:5000/)


4. **Sau khi chạy xong experiment trong MLflow UI, ta register model XGBoost và chuyển qua bước tạo api cho model:**
    
    - **Đầu tiên ta hủy Mlflow đang chạy ở port 5000 để giải phóng port 5000:**
    
      - *Qua terminal đã chạy Mlflow UI trước đó và nhấn Ctrl + C.*
   - Sau đó chạy:
    ```bash
    cd ..
    docker compose up --build
    ```
   Sẽ mất khoảng 5 phút để build và sau khi build xong ta sẽ có được một model api


5. **Mở MLFlow với đường dẫn [MLflow](http://localhost:5000/)** và Uvicorn để test api tại [đây](http://localhost:8000/docs)


6. **Giờ chúng ta đã có api model để dùng cho việc dự đoán, dùng lệnh sau đây để test api model với 77 feature để dự đoán:**
    
   *Label "Benign":*
   ```bash
    curl -X POST "http://localhost:8000/predict" \
      -H "Content-Type: application/json" \
      -d '{
        "feature": [
          123456, 10, 8, 500, 400, 60, 40, 50.0, 7.07, 55, 35, 45.0, 7.07,
          9000.0, 5.0, 1000.0, 100.0, 2000, 500, 5000, 1000.0, 200.0, 1500, 500,
          4000, 800.0, 150.0, 1200, 400, 0, 0, 0, 0, 120, 100, 2.0, 1.5, 35, 65,
          50.0, 10.0, 100.0, 0, 1, 0, 0, 1, 0, 0, 0, 1.2, 52.0, 50.0, 45.0, 120,
          0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 10, 500, 8, 400, 256, 256, 1, 20,
          3000.0, 400.0, 4000, 2000, 10000.0, 500.0, 11000, 9000
        ]
      }'
    ```
   *Label "Not Benign":*
   ```bash
    curl -X POST "http://localhost:8000/predict" \
      -H "Content-Type: application/json" \
      -d '{
        "feature": [
          6.0, 1293792.0, 3.0, 7.0, 26.0, 11607.0, 20.0, 0.0,
          8.66666698, 10.2632027, 5840.0, 0.0, 1658.14282, 2137.29712,
          8991.39893, 7.72921768, 143754.672, 430865.812, 1292730.0, 2.0,
          747.0, 373.5, 523.966125, 744.0, 3.0, 1293746.0, 215624.328,
          527671.938, 1292730.0, 2.0, 0.0, 0.0, 0.0, 0.0, 72.0, 152.0,
          2.3187654, 5.41045237, 0.0, 5840.0, 1057.54541, 1853.4375,
          3435230.75, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 2.0,
          1163.30005, 8.66666698, 1658.14282, 0.0, 0.0, 0.0, 0.0, 0.0,
          0.0, 3.0, 26.0, 7.0, 11607.0, 8192.0, 229.0, 2.0, 20.0,
          0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0
        ]
      }'
   ```
## Cấu trúc thư mục
```
MLFlows/
├── mlops_model_api/                # Thư mục chứa mã nguồn của API phục vụ mô hình
│   ├── .dockerignore               # Danh sách file/thư mục bị Docker bỏ qua
│   ├── api.py                      # Hàm tạo api cho model predict
│   ├── Dockerfile                  # Dockerfile để build image cho Model api sử dụng Fastapi
│   ├── requirements.txt            # Các thư viện cần thiết
├── training_pipeline/              # Pipeline tiền xử lý dữ liệu và huấn luyện mô hình
│   ├── asset/                      # Các asset phụ trợ (nếu có)
│   ├── data/                       # Thư mục chứa các file dữ liệu đầu vào (.parquet)
│   │   ├── Benign-Monday-no-metadata.parquet
│   │   ├── Botnet-Friday-no-metadata.parquet
│   │   ├── Bruteforce-Tuesday-no-metadata.parquet
│   │   ├── DDoS-Friday-no-metadata.parquet
│   │   ├── DoS-Wednesday-no-metadata.parquet
│   │   ├── Infiltration-Thursday-no-metadata.parquet
│   │   ├── Portscan-Friday-no-metadata.parquet
│   │   └── WebAttacks-Thursday-no-metadata.parquet
│   ├── mlruns/                     # Thư mục do MLflow tạo để lưu các lần thực nghiệm (experiments)
│   ├── mlartifact/                 # Lưu các artifact như scaler, encoder, mô hình...
│   ├── models/                     # Thư mục chứa các checkpoints mô hình đã train
│   ├── utils/                      # Thư viện tiện ích dùng trong pipeline
│   │   ├── __init__.py
│   │   ├── tunning.py              # Hàm dùng để tune mô hình
│   │   └── utils.py                # Hàm xử lý dữ liệu, feature engineering,...
│   ├── Dockerfile                  # Dockerfile để build image cho Mlflow server
│   ├── input.json                  # File chứa dữ liệu mẫu để test API
│   ├── load_model.py               # Mã để load và phục vụ mô hình từ MLflow
│   ├── main.py                     # File chính để chạy pipeline tiền xử lý & huấn luyện
│   ├── requirement.txt             # Các thư viện cần thiết
│   ├── test.py                     # File để test model để chạy api
├── venv/                           # Môi trường ảo (không nên commit vào git)
├── .gitignore                      # Danh sách file/thư mục bị git bỏ qua
├── docker-compose.yml              # Docker Compose để chạy toàn bộ hệ thống
└── README.md                       # Tài liệu hướng dẫn sử dụng dự án

```


## 🧠 Mô hình
Dự án sử dụng hai thuật toán học máy phổ biến để phát hiện bất thường trong lưu lượng mạng từ tập dữ liệu CICIDS2017:

- MLP (Multi-Layer Perceptron): Một mạng nơ-ron sâu dùng cho bài toán phân loại phi tuyến.

- XGBoost: Một thuật toán boosting mạnh mẽ, hiệu quả cao, thường được sử dụng trong các bài toán phân loại và đạt kết quả tốt trên các tập dữ liệu phức tạp.

Cả hai mô hình đều được huấn luyện, đánh giá và so sánh trực tiếp thông qua MLflow Tracking.

## 📊 Quản lý thí nghiệm với MLflow
Toàn bộ pipeline từ tiền xử lý dữ liệu, huấn luyện mô hình đến đánh giá đều được theo dõi và ghi nhận bằng MLflow Tracking, bao gồm:

- Tham số (Parameters): như số tầng của MLP, learning rate, v.v.

- Metric đánh giá: như độ chính xác (Accuracy), AUC, F1-score,...

- Artifact: bao gồm mô hình đã huấn luyện, scaler, encoder và các file hỗ trợ khác.

- Sau khi huấn luyện, bạn có thể sử dụng MLflow UI để xem lại tất cả các lần chạy, so sánh hiệu suất giữa các mô hình và dễ dàng chọn ra mô hình tốt nhất để triển khai.

## 📈 Kết quả
Tất cả kết quả huấn luyện và đánh giá mô hình được lưu trữ trong MLflow, bao gồm:

- Bảng so sánh các mô hình theo metric

- Đường biểu diễn hiệu suất (ROC, Precision-Recall,...)

- Phiên bản mô hình đã được đăng ký để phục vụ API
## 📷 Hình ảnh Demo

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
