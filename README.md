# HỆ THỐNG HỖ TRỢ CHẨN ĐOÁN Y TẾ (Chẩn Đoán Bệnh Lý Qua Triệu Chứng)

Hệ thống AI ứng dụng thuật toán máy học **Multinomial Naive Bayes** kết hợp với **TF-IDF Vectorizer** nhằm phân tích ngôn ngữ tự nhiên (Triệu chứng tiếng Việt) và tính toán xác suất mắc bệnh. 

Dự án này là minh chứng cụ thể cho khả năng của thuật toán Naive Bayes trong bài toán Classification (Phân loại dữ liệu y khoa). Hệ thống đi kèm với một giao diện Website tinh gọn (Mobile-first Light Theme).

---

## Tính Năng Chính
- **Symptom Tracker**: Quét văn bản người dùng để lọc ra Keyword y tế bằng Underthesea NLP.
- **Disease Probability Matrix**: Đưa ra kết luận có bao nhiêu `%` khả năng người dùng gặp phải từng chứng bệnh.
- **Data Augmentation**: Mô hình sở hữu tập dữ liệu tự sinh bằng ngôn ngữ tự nhiên lớn (Lên tới 20.000 records).
- **Trải Nghiệm Responsive**: Tương thích tốt giao diện trên Desktop và có độ mượt mà trên chuẩn Web-Mobile.

![UI Screenshot](docs/images/test_diagnosis_ui.png)
*(Giao diện UI Trợ lý Phân loại Y tế)*

## Kết quả Huấn Luyện AI
- **Dataset:** 20.000 mẫu, 20 Bệnh lý cơ bản
- **Algorithm:** Naive Bayes `alpha=1.0`
- **Accuracy trên tập test:** Đạt đúng **89.0%** trên tập test hoàn chỉnh.
- **Cross-validation (5-fold):** Cực kỳ ổn định (Biên độ dao động `±0.00%`).

## Hướng dẫn 3 Bước Cài Đặt
```bash
# B1: Cài đặt Python Dependencies
pip install -r requirements.txt

# B2: Cấp tập sinh dữ liệu 20.000 mẫu & Huấn luyện Model thuật toán
python generate_disease_data.py
python train.py

# B3: Cấp cổng phục vụ Web HTML UI
python app.py
```
-> `Truy cập trên trình duyệt: http://localhost:5000`

---
> * **Tuyên bố bảo lưu y khoa**: *Softwares và kết quả thuật toán chỉ mang tính ước lượng trên số liệu thống kê máy học ML. Hệ thống không thay thế được bác sĩ lâm sàng và thiết bị chẩn đoán y tế thực tế.*
