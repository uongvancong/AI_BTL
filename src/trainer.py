"""
Module huấn luyện mô hình Naive Bayes (Trainer)

Chức năng:
- Đọc dữ liệu từ file intents.json
- Tiền xử lý dữ liệu huấn luyện
- Xây dựng pipeline: TF-IDF + MultinomialNB
- Huấn luyện và đánh giá mô hình
- Lưu model đã train ra file
"""

import json
import os
from collections import Counter
import numpy as np
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score

from src.preprocessor import TextPreprocessor


class NaiveBayesTrainer:
    """
    Lớp huấn luyện mô hình phân loại câu hỏi bằng Naive Bayes.

    Workflow:
    1. load_data() - Đọc dữ liệu từ intents.json
    2. train() - Huấn luyện mô hình
    3. evaluate() - Đánh giá mô hình
    4. save_model() - Lưu model ra file
    """

    def __init__(self, preprocessor=None):
        """
        Khởi tạo NaiveBayesTrainer.

        Args:
            preprocessor (TextPreprocessor): Đối tượng tiền xử lý. 
                                              Nếu None, tạo mới với config mặc định.
        """
        self.preprocessor = preprocessor or TextPreprocessor()

        # Pipeline: TF-IDF Vectorizer → Multinomial Naive Bayes
        self.pipeline = Pipeline([
            ("tfidf", TfidfVectorizer(
                max_features=5000,        # Giới hạn số lượng features
                ngram_range=(1, 2),       # Sử dụng cả unigram và bigram
                sublinear_tf=True,        # Áp dụng log scaling cho TF
            )),
            ("clf", MultinomialNB(
                alpha=1.0,               # Laplace smoothing (tránh zero probability)
            )),
        ])

        self.X_raw = []       # Câu hỏi gốc
        self.X_processed = [] # Câu hỏi đã tiền xử lý
        self.y = []           # Nhãn (intent tags)
        self.intents_data = None  # Dữ liệu intents gốc (bao gồm responses)

    def load_data(self, intents_path=None):
        """
        Đọc dữ liệu từ file intents.json.

        Args:
            intents_path (str): Đường dẫn đến file intents.json.

        Returns:
            tuple: (X_processed, y) - Dữ liệu đã tiền xử lý và nhãn.
        """
        if intents_path is None:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            intents_path = os.path.join(base_dir, "data", "intents.json")

        print(f"[Trainer] Đọc dữ liệu từ: {intents_path}")

        with open(intents_path, "r", encoding="utf-8") as f:
            self.intents_data = json.load(f)

        self.X_raw = []
        self.X_processed = []
        self.y = []

        for intent in self.intents_data["intents"]:
            tag = intent["tag"]
            for pattern in intent["patterns"]:
                self.X_raw.append(pattern)
                self.X_processed.append(self.preprocessor.preprocess(pattern))
                self.y.append(tag)

        print(f"[Trainer] Đã tải {len(self.X_processed)} mẫu, {len(set(self.y))} intents.")
        print(f"[Trainer] Các intents: {sorted(set(self.y))}")

        # Thống kê số lượng mẫu mỗi intent
        from collections import Counter
        counter = Counter(self.y)
        print(f"\n[Trainer] Phân bố dữ liệu:")
        for tag, count in sorted(counter.items()):
            print(f"  - {tag}: {count} mẫu")

        return self.X_processed, self.y

    def train(self, test_size=0.2, random_state=42):
        """
        Huấn luyện mô hình Naive Bayes.

        Args:
            test_size (float): Tỷ lệ dữ liệu test (0.0 - 1.0).
            random_state (int): Seed cho việc chia dữ liệu.

        Returns:
            dict: Kết quả huấn luyện bao gồm accuracy, classification report.
        """
        if not self.X_processed:
            raise ValueError("Chưa tải dữ liệu! Gọi load_data() trước.")

        print(f"\n[Trainer] Bắt đầu huấn luyện...")
        print(f"[Trainer] Test size: {test_size}, Random state: {random_state}")

        # Chia dữ liệu train/test
        X_train, X_test, y_train, y_test = train_test_split(
            self.X_processed, self.y,
            test_size=test_size,
            random_state=random_state,
            stratify=self.y  # Đảm bảo phân bố đều các class
        )

        print(f"[Trainer] Train: {len(X_train)} mẫu, Test: {len(X_test)} mẫu")

        # Huấn luyện pipeline
        self.pipeline.fit(X_train, y_train)

        # Dự đoán trên tập test
        y_pred = self.pipeline.predict(X_test)

        # Tính metrics
        accuracy = accuracy_score(y_test, y_pred)
        report = classification_report(y_test, y_pred, zero_division=0)
        cm = confusion_matrix(y_test, y_pred)

        print(f"\n{'='*60}")
        print(f"KẾT QUẢ HUẤN LUYỆN")
        print(f"{'='*60}")
        print(f"\n[*] Accuracy: {accuracy:.2%}")
        print(f"\n[*] Classification Report:\n{report}")
        print(f"\n[*] Confusion Matrix:\n{cm}")

        # Cross-validation (nếu đủ dữ liệu)
        cv_scores = None
        if len(self.X_processed) >= 10:
            n_splits = min(5, min(Counter(self.y).values()))
            if n_splits >= 2:
                cv_scores = cross_val_score(
                    self.pipeline, self.X_processed, self.y,
                    cv=n_splits, scoring="accuracy"
                )
                print(f"\n[*] Cross-validation ({n_splits}-fold):")
                print(f"    Scores: {cv_scores}")
                print(f"    Mean: {cv_scores.mean():.2%} +/- {cv_scores.std():.2%}")

                # Re-train on full dataset sau khi đánh giá
                self.pipeline.fit(self.X_processed, self.y)
                print(f"\n[Trainer] Đã re-train trên toàn bộ dữ liệu ({len(self.X_processed)} mẫu).")

        results = {
            "accuracy": accuracy,
            "report": report,
            "confusion_matrix": cm,
            "cv_scores": cv_scores,
            "train_size": len(X_train),
            "test_size": len(X_test),
        }

        return results

    def save_model(self, model_path=None):
        """
        Lưu model đã train ra file.

        Args:
            model_path (str): Đường dẫn lưu file model.
        """
        if model_path is None:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            model_dir = os.path.join(base_dir, "models")
            os.makedirs(model_dir, exist_ok=True)
            model_path = os.path.join(model_dir, "naive_bayes_model.pkl")

        joblib.dump(self.pipeline, model_path)
        print(f"\n[Trainer] Đã lưu model tại: {model_path}")

        # Lưu thêm intents data (để lookup responses)
        intents_path = model_path.replace(".pkl", "_intents.json")
        with open(intents_path, "w", encoding="utf-8") as f:
            json.dump(self.intents_data, f, ensure_ascii=False, indent=2)
        print(f"[Trainer] Đã lưu intents data tại: {intents_path}")

        return model_path

    def get_feature_importance(self, top_n=10):
        """
        Hiển thị các từ quan trọng nhất cho mỗi intent.

        Args:
            top_n (int): Số lượng từ hiển thị cho mỗi intent.
        """
        tfidf = self.pipeline.named_steps["tfidf"]
        clf = self.pipeline.named_steps["clf"]

        feature_names = tfidf.get_feature_names_out()
        classes = clf.classes_

        print(f"\n{'='*60}")
        print(f"TOP {top_n} TỪ QUAN TRỌNG NHẤT CHO MỖI INTENT")
        print(f"{'='*60}")

        for i, class_name in enumerate(classes):
            # Log probabilities cho class này
            log_probs = clf.feature_log_prob_[i]
            top_indices = np.argsort(log_probs)[-top_n:][::-1]

            print(f"\n  [{class_name}]:")
            for idx in top_indices:
                print(f"    - {feature_names[idx]} (log_prob: {log_probs[idx]:.4f})")


# === Chạy training khi gọi trực tiếp ===
if __name__ == "__main__":
    from collections import Counter

    print("=" * 60)
    print("HUẤN LUYỆN MÔ HÌNH NAIVE BAYES")
    print("=" * 60)

    trainer = NaiveBayesTrainer()
    trainer.load_data()
    results = trainer.train()
    trainer.get_feature_importance(top_n=5)
    trainer.save_model()

    print("\n[OK] Hoan tat huan luyen!")
