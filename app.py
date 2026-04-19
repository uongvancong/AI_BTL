"""
Flask Web Server cho Chatbot

Cung cấp:
- Giao diện web chat (HTML/CSS/JS)
- API endpoint /api/chat để giao tiếp với chatbot
- API endpoint /api/stats để xem thống kê
"""

from flask import Flask, request, jsonify, render_template
from src.chatbot import Chatbot

app = Flask(__name__)

# Khởi tạo chatbot (global instance)
chatbot = None


def get_chatbot():
    """Lazy initialization cho chatbot."""
    global chatbot
    if chatbot is None:
        chatbot = Chatbot()
    return chatbot


# === ROUTES ===

@app.route("/")
def index():
    """Trang chủ - Giao diện chat."""
    return render_template("index.html")


@app.route("/api/chat", methods=["POST"])
def chat():
    """
    API endpoint xử lý tin nhắn từ người dùng.

    Request JSON:
        { "message": "Điểm chuẩn bao nhiêu?" }

    Response JSON:
        {
            "response": "Điểm chuẩn các ngành...",
            "intent": "hoi_tuyen_sinh",
            "confidence": 0.87,
            "timestamp": "2026-04-18T10:30:00"
        }
    """
    data = request.get_json()

    if not data or "message" not in data:
        return jsonify({"error": "Thiếu trường 'message' trong request."}), 400

    message = data["message"]
    bot = get_chatbot()
    result = bot.get_response(message)

    return jsonify(result)


@app.route("/api/stats", methods=["GET"])
def stats():
    """API endpoint trả về thống kê chatbot."""
    bot = get_chatbot()
    return jsonify(bot.get_stats())


@app.route("/api/history", methods=["GET"])
def history():
    """API endpoint trả về lịch sử hội thoại."""
    bot = get_chatbot()
    return jsonify({"history": bot.get_history()})


@app.route("/api/clear", methods=["POST"])
def clear():
    """API endpoint xóa lịch sử hội thoại."""
    bot = get_chatbot()
    bot.clear_history()
    return jsonify({"message": "Đã xóa lịch sử hội thoại."})


# === MAIN ===
if __name__ == "__main__":
    import sys, io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')
    print("=" * 60)
    print("Khoi dong Chatbot Web Server...")
    print("http://localhost:5000")
    print("=" * 60)
    app.run(debug=True, host="0.0.0.0", port=5000)
