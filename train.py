"""
Script huấn luyện model - chạy file này để train model trước khi chạy chatbot.

Cách dùng:
    python train.py
"""

import sys
import io

# Fix encoding cho Windows console (tránh lỗi emoji)
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from src.trainer import NaiveBayesTrainer


def main():
    print("=" * 60)
    print("HUAN LUYEN MO HINH NAIVE BAYES")
    print("Chatbot Tu Van Y Te")
    print("=" * 60)

    # Khởi tạo trainer
    trainer = NaiveBayesTrainer()

    # Tải dữ liệu
    trainer.load_data()

    # Huấn luyện
    results = trainer.train(test_size=0.2, random_state=42)

    # Hiển thị từ quan trọng
    trainer.get_feature_importance(top_n=5)

    # Lưu model
    trainer.save_model()

    print("\n" + "=" * 60)
    print("HOAN TAT HUAN LUYEN!")
    print(f"Accuracy: {results['accuracy']:.2%}")
    print("Model da duoc luu tai: models/naive_bayes_model.pkl")
    print("=" * 60)
    print("\nTiep theo: chay 'python app.py' de khoi dong chatbot web.")


if __name__ == "__main__":
    main()
