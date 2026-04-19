"""
Module dự đoán intent (Predictor)

Chức năng:
- Tải model đã train từ file
- Dự đoán intent cho câu hỏi mới
- Trả về intent và confidence score
"""

import os
import joblib
import numpy as np

from src.preprocessor import TextPreprocessor


class IntentPredictor:
    """
    Lớp dự đoán intent từ câu hỏi của người dùng.
    
    Sử dụng model Naive Bayes đã train để phân loại câu hỏi
    vào các intent (chủ đề) đã định nghĩa.
    """

    def __init__(self, model_path=None, preprocessor=None):
        """
        Khởi tạo IntentPredictor.

        Args:
            model_path (str): Đường dẫn đến file model (.pkl).
            preprocessor (TextPreprocessor): Đối tượng tiền xử lý.
        """
        self.preprocessor = preprocessor or TextPreprocessor()

        if model_path is None:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            model_path = os.path.join(base_dir, "models", "naive_bayes_model.pkl")

        if not os.path.exists(model_path):
            raise FileNotFoundError(
                f"Không tìm thấy model tại: {model_path}\n"
                f"Hãy chạy trainer.py để huấn luyện model trước!"
            )

        self.model = joblib.load(model_path)
        pass

    def predict(self, text):
        """
        Dự đoán intent cho một câu hỏi.

        Args:
            text (str): Câu hỏi của người dùng.

        Returns:
            tuple: (intent, confidence)
                - intent (str): Tên intent được dự đoán.
                - confidence (float): Độ tin cậy (0.0 - 1.0).

        Ví dụ:
            >>> predictor = IntentPredictor()
            >>> intent, conf = predictor.predict("Điểm chuẩn bao nhiêu?")
            >>> print(f"{intent} ({conf:.2%})")
            hoi_tuyen_sinh (87.50%)
        """
        # Tiền xử lý câu hỏi
        processed_text = self.preprocessor.preprocess(text)

        if not processed_text:
            return "hoi_khac", 0.0

        # Dự đoán intent
        intent = self.model.predict([processed_text])[0]

        # Tính confidence (xác suất cao nhất)
        probabilities = self.model.predict_proba([processed_text])[0]
        confidence = float(np.max(probabilities))

        return intent, confidence

    def predict_top_k(self, text, k=3):
        """
        Dự đoán top K intents có xác suất cao nhất.

        Args:
            text (str): Câu hỏi của người dùng.
            k (int): Số lượng intents trả về.

        Returns:
            list[tuple]: Danh sách (intent, probability) sắp xếp giảm dần.
        """
        processed_text = self.preprocessor.preprocess(text)

        if not processed_text:
            return [("hoi_khac", 0.0)]

        probabilities = self.model.predict_proba([processed_text])[0]
        classes = self.model.classes_

        # Sắp xếp theo xác suất giảm dần
        sorted_indices = np.argsort(probabilities)[::-1][:k]

        results = []
        for idx in sorted_indices:
            results.append((classes[idx], float(probabilities[idx])))

        return results

    def get_all_intents(self):
        """Trả về danh sách tất cả các intents mà model biết."""
        return list(self.model.classes_)


# === Test nhanh ===
if __name__ == "__main__":
    predictor = IntentPredictor()

    test_questions = [
        "Xin chào",
        "Điểm chuẩn năm nay bao nhiêu",
        "Học phí ngành CNTT bao nhiêu",
        "Trường có những ngành nào",
        "Có ký túc xá không",
        "Làm sao để nhận học bổng",
        "Ra trường dễ xin việc không",
        "Tạm biệt nhé",
        "Bạn là ai",
    ]

    print("=" * 70)
    print("TEST DỰ ĐOÁN INTENT")
    print("=" * 70)

    for q in test_questions:
        intent, conf = predictor.predict(q)
        print(f"\n  Q: {q}")
        print(f"  → Intent: {intent} | Confidence: {conf:.2%}")

        # Hiển thị top 3
        top3 = predictor.predict_top_k(q, k=3)
        for rank, (tag, prob) in enumerate(top3, 1):
            print(f"    #{rank}: {tag} ({prob:.2%})")
