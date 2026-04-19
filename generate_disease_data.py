import json
import random
import csv

def generate_disease_data():
    dataset = {"intents": []}
    
    diseases = {
        "Viêm phổi": {
            "symptoms": ["sốt cao", "ho có đờm", "khó thở", "đau ngực", "lạnh run", "thở dốc", "tức ngực", "ho ra máu", "cơ thể mệt lả", "ho dai dẳng"]
        },
        "Cảm cúm (Flu)": {
            "symptoms": ["ho", "sốt nhẹ", "đau đầu", "sổ mũi", "nghẹt mũi", "hắt hơi", "đau họng", "mỏi cơ", "sốt", "đau mỏi vai gáy"]
        },
        "Sốt xuất huyết": {
            "symptoms": ["sốt cao liên tục", "phát ban", "nhức mỏi cơ", "đau hốc mắt", "xuất huyết dưới da", "chảy máu chân răng", "nôn mửa", "buồn nôn", "đau quặn bụng", "chóng mặt"]
        },
        "Viêm loét dạ dày": {
            "symptoms": ["đau bụng thượng vị", "ợ chua", "đầy hơi", "buồn nôn", "khó tiêu", "ợ nóng", "chán ăn", "đau nhói bụng lúc đói", "tức vùng ngực dưới"]
        },
        "Ngộ độc thực phẩm": {
            "symptoms": ["nôn mửa", "tiêu chảy", "đau quặn bụng", "sốt", "đi ngoài nhiều lần", "mất nước", "ớn lạnh", "khô miệng"]
        },
        "Sỏi thận": {
            "symptoms": ["đau quặn thắt lưng", "đi tiểu ra máu", "tiểu buốt", "đau bụng dưới", "tiểu rắt", "ớn lạnh", "buồn nôn khi đau", "nước tiểu đục"]
        },
        "Viêm gan": {
            "symptoms": ["da vàng", "mắt vàng", "nước tiểu sẫm màu", "phân nhạt màu", "mệt mỏi kéo dài", "chán ăn", "đau hạ sườn phải", "sốt nhẹ", "ngứa da"]
        },
        "Thoái hóa khớp": {
            "symptoms": ["đau nhức xương khớp", "cứng khớp buổi sáng", "lạo xạo khi cử động", "sưng khớp", "đau gối", "mỏi lưng", "khó vận động", "đau khi bước đi"]
        },
        "Rối loạn tiền đình": {
            "symptoms": ["chóng mặt", "hoa mắt", "quay cuồng", "mất thăng bằng", "buồn nôn", "ù tai", "sợ tiếng ồn", "đau nửa đầu", "choáng váng"]
        },
        "Dị ứng da": {
            "symptoms": ["nổi mề đay", "ngứa ngáy", "phát ban đỏ", "sưng phù", "bong tróc da", "nổi mẩn đỏ", "rát da", "nổi sẩn"]
        },
        "Viêm xoang": {
            "symptoms": ["đau nhức vùng mặt", "nghẹt mũi", "chảy dịch mũi", "đau đầu vùng trán", "giảm khứu giác", "ho về đêm", "hơi thở hôi"]
        },
        "Đái tháo đường": {
            "symptoms": ["khát nước liên tục", "tiểu nhiều lần", "nhanh đói", "sụt cân không nguyên nhân", "mệt mỏi", "mờ mắt", "vết thương lâu lành"]
        },
        "Cao huyết áp": {
            "symptoms": ["đau đầu", "chóng mặt", "chảy máu cam", "khó thở", "đau tức ngực", "mờ mắt", "tê bì chân tay", "nhịp tim không đều"]
        },
        "Bệnh gút (Gout)": {
            "symptoms": ["đau nhức khớp dữ dội", "sưng đỏ ngón chân cái", "nóng rát khớp", "khớp sưng to", "đau tăng về đêm", "sốt lười ăn"]
        },
        "Suy tim": {
            "symptoms": ["khó thở khi nằm", "ho khan kéo dài", "phù nề chân", "mệt mỏi kiệt sức", "nhịp tim nhanh", "tăng cân bất thường", "chóng mặt"]
        },
        "Bệnh trĩ": {
            "symptoms": ["đau rát hậu môn", "đi ngoài ra máu", "ngứa ngáy hậu môn", "sa búi trĩ", "táo bón kéo dài", "sưng phồng vùng hậu môn"]
        },
        "Đau mắt đỏ": {
            "symptoms": ["mắt đỏ", "đau cộm mắt", "chảy nước mắt", "đổ ghèn nhiều", "nhạy cảm ánh sáng", "sưng mi mắt", "ngứa mắt"]
        },
        "Thủy đậu": {
            "symptoms": ["nổi mụn nước", "phát ban toàn thân", "sốt cao", "chán ăn", "đau đầu", "đau cơ", "ngứa ngáy", "mệt mỏi"]
        },
        "Viêm ruột thừa": {
            "symptoms": ["đau hố chậu phải", "đau quanh rốn", "sốt nhẹ", "buồn nôn", "chán ăn", "chướng bụng", "tiêu chảy"]
        },
        "Hen suyễn": {
            "symptoms": ["khó thở", "thở khò khè", "nặng ngực", "ho nhiều về đêm", "hụt hơi", "đau nhức ngực", "thở rít"]
        }
    }

    prefixes = ["Tôi bị", "Cháu bị", "Bác sĩ ơi tôi bị", "Mình đang", "Có triệu chứng", "Hay bị", "Mấy hôm nay tôi bị", "Dấu hiệu", "Cảm thấy", "Tự nhiên bị"]
    common_symptoms = ["mệt mỏi", "sốt", "đau đầu", "chán ăn", "lừ đừ", "khó chịu trong người", "buồn nôn", "mất ngủ", "suy nhược", "ớn lạnh"]

    for disease, data in diseases.items():
        patterns = set()
        symps = data["symptoms"]
        
        # Tạo số lượng lớn mẫu kết hợp ngẫu nhiên các triệu chứng để có thể lọc ra 1000 mẫu unique
        for _ in range(15000):
            # Chọn 1 đến 2 triệu chứng đặc thù (giảm đi để khó đoán hơn)
            chosen = random.sample(symps, min(len(symps), random.randint(1, 2)))
            
            # Tiêm nhiễu ngẫu nhiên rất mạnh (noise) bằng các triệu chứng chung (overlap) với tỷ lệ 95%
            if random.random() < 0.95:
                noise = random.sample(common_symptoms, random.randint(2, 4))
                chosen.extend(noise)
                random.shuffle(chosen)
                
            combo = ", ".join(chosen)
            pref = random.choice(prefixes)
            
            p = f"{pref} {combo}".strip().lower()
            patterns.add(p)
                
            # Tạo các cụm chỉ có triệu chứng không cần đại từ
            p2 = f"{combo}".strip().lower()
            patterns.add(p2)
                
        patterns = list(patterns)[:1000]
        
        dataset["intents"].append({
            "tag": disease,
            "patterns": patterns,
            "responses": [disease]
        })

    total = sum([len(i["patterns"]) for i in dataset["intents"]])
    print(f"Total disease diagnosis samples generated: {total}")

    with open('data/intents.json', 'w', encoding='utf-8') as f:
        json.dump(dataset, f, ensure_ascii=False, indent=2)

    csv_filename = "data/dataset_20k.csv"
    with open(csv_filename, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["Disease_Label", "Symptom_Text"])
        for intent in dataset["intents"]:
            disease = intent["tag"]
            for pattern in intent["patterns"]:
                writer.writerow([disease, pattern])
                
    print(f"Dataset CSV exported to: {csv_filename}")

if __name__ == "__main__":
    generate_disease_data()

