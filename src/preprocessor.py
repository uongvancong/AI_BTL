"""
Module tiền xử lý văn bản tiếng Việt (Vietnamese Text Preprocessor)

Chức năng:
- Chuyển chữ thường (lowercase)
- Loại bỏ ký tự đặc biệt, dấu câu
- Tách từ tiếng Việt bằng thư viện underthesea
- Loại bỏ stopwords tiếng Việt
"""

import re
import os
from underthesea import word_tokenize


class TextPreprocessor:
    """
    Lớp tiền xử lý văn bản tiếng Việt.
    
    Pipeline xử lý:
    1. Chuyển thường (lowercase)
    2. Loại bỏ ký tự đặc biệt
    3. Tách từ (word segmentation) bằng underthesea
    4. Loại bỏ stopwords
    """

    def __init__(self, stopwords_path=None):
        """
        Khởi tạo TextPreprocessor.

        Args:
            stopwords_path (str): Đường dẫn đến file stopwords tiếng Việt.
                                  Nếu None, sẽ tìm file mặc định trong thư mục data/.
        """
        self.stopwords = set()

        if stopwords_path is None:
            # Tìm file stopwords mặc định
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            stopwords_path = os.path.join(base_dir, "data", "vietnamese_stopwords.txt")

        if os.path.exists(stopwords_path):
            self._load_stopwords(stopwords_path)
            pass
        else:
            pass

    def _load_stopwords(self, path):
        """Đọc file stopwords, mỗi dòng là một từ."""
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                word = line.strip()
                if word:
                    self.stopwords.add(word)

    def preprocess(self, text):
        """
        Tiền xử lý một câu văn bản tiếng Việt.

        Args:
            text (str): Văn bản đầu vào.

        Returns:
            str: Văn bản đã được tiền xử lý.

        Ví dụ:
            >>> preprocessor = TextPreprocessor()
            >>> preprocessor.preprocess("Điểm chuẩn năm nay bao nhiêu???")
            "điểm_chuẩn năm_nay"
        """
        if not text or not isinstance(text, str):
            return ""

        # Bước 1: Chuyển thường
        text = text.lower().strip()

        # Bước 2: Loại bỏ URL
        text = re.sub(r"http\S+|www\.\S+", "", text)

        # Bước 3: Loại bỏ email
        text = re.sub(r"\S+@\S+", "", text)

        # Bước 4: Loại bỏ số (giữ lại chữ và khoảng trắng)
        text = re.sub(r"\d+", "", text)

        # Bước 5: Loại bỏ ký tự đặc biệt, giữ lại chữ cái tiếng Việt và khoảng trắng
        text = re.sub(r"[^\w\sàáảãạăắằẳẵặâấầẩẫậèéẻẽẹêếềểễệìíỉĩịòóỏõọôốồổỗộơớờởỡợùúủũụưứừửữựỳýỷỹỵđ]", "", text)

        # Bước 6: Loại bỏ khoảng trắng thừa
        text = re.sub(r"\s+", " ", text).strip()

        if not text:
            return ""

        # Bước 7: Tách từ tiếng Việt bằng underthesea
        # format="text" sẽ nối các từ ghép bằng dấu gạch dưới
        # Ví dụ: "trường đại học" → "trường_đại_học"
        text = word_tokenize(text, format="text")

        # Bước 8: Loại bỏ stopwords
        words = text.split()
        words = [w for w in words if w not in self.stopwords]

        return " ".join(words)

    def preprocess_batch(self, texts):
        """
        Tiền xử lý một danh sách văn bản.

        Args:
            texts (list[str]): Danh sách các văn bản.

        Returns:
            list[str]: Danh sách các văn bản đã tiền xử lý.
        """
        return [self.preprocess(text) for text in texts]


# === Test nhanh khi chạy trực tiếp ===
if __name__ == "__main__":
    preprocessor = TextPreprocessor()

    test_cases = [
        "Xin chào bạn!!!",
        "Điểm chuẩn năm nay bao nhiêu???",
        "Trường đại học có ký túc xá không ạ?",
        "Học phí ngành CNTT khoảng bao nhiêu tiền vậy?",
        "Hello, tôi muốn hỏi về tuyển sinh",
    ]

    print("=" * 60)
    print("TEST TIỀN XỬ LÝ VĂN BẢN TIẾNG VIỆT")
    print("=" * 60)
    for text in test_cases:
        result = preprocessor.preprocess(text)
        print(f"\n  Input:  {text}")
        print(f"  Output: {result}")
    print("\n" + "=" * 60)
