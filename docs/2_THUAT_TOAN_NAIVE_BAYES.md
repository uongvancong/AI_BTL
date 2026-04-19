# 2. KIẾN TRÚC THUẬT TOÁN NAIVE BAYES

## 2.1 Định Lý Bayes trong Y Khoa
Định lý Bayes mô tả xác suất xảy ra của một sự kiện dựa trên các kiến thức đã biết trước đó có liên quan đến sự kiện này.
Trong bài toán của chúng ta:

`P(Bệnh | Triệu Chứng) = [ P(Triệu Chứng | Bệnh) * P(Bệnh) ] / P(Triệu Chứng)`

- **P(Bệnh | Triệu Chứng):** Xác suất mắc căn bệnh đó khi có các triệu chứng đang xét (Hậu nghiệm).
- **P(Triệu Chứng | Bệnh):** Khả năng xuất hiện tổ hợp triệu chứng này trên những người đã từng mắc bệnh (Khả năng).
- **P(Bệnh):** Xác suất mắc bệnh đó xét trên toàn bộ dữ liệu (Tiên nghiệm).

Việc giả định các triệu chứng hoàn toàn độc lập với nhau đưa chúng ta đến giới hạn **"Naive" (Ngây thơ)** của thuật toán. Mặc dù trên thực tế, "sốt" và "sổ mũi" hay đi kèm nhau, nhưng giả định ngây thơ này giúp tính toán nhân xác suất cực nhanh và lại cho Độ chính xác thực tế vô cùng ấn tượng.

## 2.2 Xử lý Vector hóa bằng TF-IDF
Máy tính không hiểu được String `"sốt cao"`, nó cần biến đổi văn bản thành Vector số rải rác:
- **TF (Term Frequency):** Số lần từ khóa như *"chóng mặt"* xuất hiện trong câu của người bệnh.
- **IDF (Inverse Document Frequency):** Đánh giá mức độ "Đắt giá" của từ khóa. Những từ xuất hiện ở mọi chứng bệnh (ví dụ: *"đau"*) sẽ có điểm IDF thấp. Những từ đặc thù (ví dụ: *"đi tiểu ra máu"*) sẽ mang điểm IDF rất cao, giúp phân loại bệnh ngay lập tức.

## 2.3 Phân Tích Logic Hàm Predictor
File `src/predictor.py` triển khai Naive Bayes như sau:
1. Load mô hình Scikit-Learn đã được Pickled từ trước.
2. Tiền xử lý `(preprocessor.preprocess)` input văn bản từ người dùng (Tách từ Underthesea).
3. Đưa chuỗi vào mô hình để gọi lệnh `predict_proba()`. Lệnh này không chỉ xuất ra Nhãn bệnh duy nhất mà xuất danh sách % tất cả 20 loại bệnh.
4. Chọn ra xác suất cao nhất `np.max(model.predict_proba)`.

Đó là lý do tại sao hệ thống AI này có thể đẩy dữ liệu lên cho Bot xuất ra câu trả lời chứa đúng hệ số xác suất của Bác Sĩ!
