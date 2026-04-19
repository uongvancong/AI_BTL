# 3. KỸ THUẬT DATA AUGMENTATION (SINH DỮ LIỆU)

Để mô hình NLP áp dụng trên Naive Bayes đạt được tỷ lệ chuẩn xác `(Accuracy >97%)`, việc cung cấp 100-200 mẫu câu là không đủ. Hệ thống cần "Nhìn" thấy rất nhiều cách tổ hợp từ ngữ. Project này giải quyết bằng Python Sinh Dữ Liệu Tự Động thông qua file `generate_disease_data.py`.

## 3.1 Tổ Hợp Kéo Thả Triệu Chứng
Khai báo 20 loại bệnh, mỗi loại bệnh gồm ~10 triệu chứng đặc thù cốt lõi:
```python
diseases = {
    "Sốt xuất huyết": {
        "symptoms": ["sốt cao", "phát ban", "nhức mỏi cơ", "chảy máu chân răng", ...]
    }
}
```

Script sẽ sử dụng hàm `random.sample()` và vòng lặp `for` lồng ghép 15.000 lần để tiến hành bốc ngẫu nhiên các tổ hợp triệu chứng (kèm theo tiêm nhiễu noise/common symptoms), ghép lại thành các mẫu mô tả bệnh khác nhau.

## 3.2 Sinh Các Tiền Tố Đa Dạng
Ngôn ngữ bệnh nhân không chỉ có triệu chứng khô khan. Khi trò chuyện với AI, họ sẽ thêm các tiền tố:
```python
prefixes = ["Tôi bị", "Đang khó chịu", "Bác sĩ ơi tôi bị", "Tự nhiên bị", "Cảm thấy"]
```

-> Khi hệ thống ghép chuỗi ngẫu nhiên, ta sẽ được vô vàn tổ hợp như:
- *"Bác sĩ ơi tôi bị phát ban, chảy máu chân răng"*
- *"Tự nhiên bị sốt cao, nhức mỏi cơ"*
- *"phát ban, nhức mỏi cơ, chảy máu chân răng"*

## 3.3 Set Filter Loại Bỏ Trùng Lặp
Vì sử dụng random.choice với số lượng vòng lặp lớn, dữ liệu chắc chắn sẽ bị trùng. Hệ thống sử dụng thuật toán Hash Set để loại bỏ triệt để bộ trùng:
`patterns = list(patterns)[:1000]`

## 3.4 Kết quả
Công cụ tạo ra file `data/intents.json` lớn với đúng **20.000 mẫu dữ liệu gán nhãn** chất lượng cao mà không tốn công sức ngồi gõ tay từng chữ. Mô hình đào tạo Naive Bayes vì vậy trở nên có độ uyên bác.
