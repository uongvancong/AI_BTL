# 1. TỔNG QUAN DỰ ÁN AI CHẨN ĐOÁN BỆNH LÝ

## 1.1 Mục Tiêu Dự Án
Dự án nhằm xây dựng một **Hệ Thống Chương trình Chẩn Đoán Bệnh Lý (Medical Diagnosis System)** dựa trên việc thu thập các triệu chứng lâm sàng từ ngôn ngữ tự nhiên của người dùng. Hệ thống có khả năng nhận diện các từ khóa chỉ báo và tính toán xác suất phần trăm người bệnh mắc phải 20 chứng bệnh phổ biến nhất định.

## 1.2 Đặc Điểm Nổi Bật
- **Phân Loại Văn Bản Học Máy (Machine Learning Text Classification):** Sử dụng `Thuật toán Naive Bayes` với `Word Vectorizer (TF-IDF)` để quét các Triệu chứng dưới dạng Đặc trưng (Features).
- **Data Augmentation:** Khắc phục nhược điểm thiếu hụt dữ liệu lâm sàng Tiếng Việt bằng cách sử dụng Tổ hợp Ngôn ngữ (Combinatorial Generation) tạo ra **20.000 cấu trúc câu** khác nhau.
- **Micro-Services Architecture:** Hệ thống chạy trên Backend Python Flask kết nối với Frontend HTML/CSS/JS thuần, tuân thủ đúng chuẩn Mobile-First (Responsive).

## 1.3 Công nghệ & Framework
| Component | Công nghệ |
| --------- | --------- |
| **Backend** | Python 3 |
| **Web Server**| Flask |
| **Machine Learning**| scikit-learn (MultinomialNB, TfidfVectorizer) |
| **Xử lý Tiếng Việt** | underthesea |
| **Mô hình Dữ liệu** | Dạng JSON lưu tĩnh tập `20.000` biểu thức từ tự nhiên |
| **Frontend** | HTML5 / CSS3 / ES6 (Mobile First UI) |

## 1.4 Danh sách bệnh lý theo dõi
Hệ thống hiện tại có khả năng nhận diện và phân biệt chính xác 20 căn bệnh bao gồm:
1. Viêm phổi (Pneumonia)
2. Cảm cúm (Flu)
3. Sốt xuất huyết
4. Viêm loét dạ dày
5. Ngộ độc thực phẩm
6. Sỏi thận
7. Viêm gan
8. Thoái hóa khớp
9. Rối loạn tiền đình
10. Dị ứng da
11. Viêm xoang
12. Đái tháo đường
13. Cao huyết áp
14. Bệnh gút (Gout)
15. Suy tim
16. Bệnh trĩ
17. Đau mắt đỏ
18. Thủy đậu
19. Viêm ruột thừa
20. Hen suyễn

## 1.5 Sơ đồ Hoạt Động (Flowchart)
1. **Người dùng** nhập chuỗi văn bản mô tả: *"Tôi bị sốt cao, ho dai dẳng"*
2. **Preprocessor** làm sạch chuỗi (Chuẩn hoá thấp, xóa số, nối từ vựng Tiếng Việt).
3. **TF-IDF Model** chuyển chuỗi câu thành Ma trận số hóa đặc trưng.
4. **Naive Bayes Classifier** tính xác suất trùng khớp dựa theo tri thức từ 20.000 mẫu siêu dữ liệu (Metadata).
5. **Chatbot Engine** xuất chuỗi chẩn đoán bệnh theo cấu trúc quy định đính kèm cùng `[Tỷ lệ %]`.
