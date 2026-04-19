# 4. HƯỚNG DẪN CÀI ĐẶT VÀ VẬN HÀNH DỰ ÁN

Tài liệu này hướng dẫn chi tiết cách để deploy hệ thống AI Chẩn Đoán Bệnh trên Local từ Source Code.

## 4.1 Cấu Hình Yêu Cầu
- Python >= 3.10
- Trình duyệt Web (Chrome, Edge)
- Hệ điều hành: Chạy được đa nền tảng (Windows, macOS, Linux)

## 4.2 Tiến hành cài đặt thư viện
Thư mục dự án đã có sẵn `requirements.txt`. Mở Terminal tại thư mục `/AI_BTL` và cài đặt:

```bash
pip install -r requirements.txt
```

Các thư viện trọng tâm bao gồm:
- `flask`: Cung cấp Web Server và API REST.
- `scikit-learn`: Lõi thuật toán Naive Bayes.
- `underthesea`: NLP xử lý từ ngữ Tiếng Việt theo chuẩn từ điển quốc gia.

## 4.3 Khởi tạo Dữ liệu (Building Data)

Để Model hoạt động, bạn cần sinh data và huấn luyện.
**Bước 1:** Khởi động máy sinh 20.000 mẫu triệu chứng:
```bash
python generate_disease_data.py
# Console: Total disease diagnosis samples generated: 20000
```
**Bước 2:** Biên dịch nội dung vào mô hình Machine Learning:
```bash
python train.py
# Console hiển thị bảng Confusion Matrix và xếp hạng F1-Score của các chứng bệnh.
```

## 4.4 Khởi động Chẩn Đoán Cục Bộ
Chạy máy chủ Flask Backend để tiếp nhận lệnh từ Server Render ra giao diện Web người dùng:
```bash
python app.py
```
Máy chủ sẽ thông báo Web Server đang lắng nghe trên cổng 5000. Bạn mở trình duyệt và truy cập vào:
-> `http://localhost:5000/`

**Tip Debug:** Trong màn hình cửa sổ Terminal, khi người dùng nhập thông tin trên Web, hệ thống sẽ log chi tiết Tên bệnh xuất ra kèm thông số Vector để theo dõi khả năng phán đoán mô hình của thuật toán.
