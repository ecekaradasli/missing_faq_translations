import json
import requests
import time
import os

# Ana modeller 
MODELS = {
    "tr_to_en": "https://api-inference.huggingface.co/models/Helsinki-NLP/opus-mt-tr-en",
    "en_to_tr": "https://api-inference.huggingface.co/models/Helsinki-NLP/opus-mt-tc-big-en-tr"  
}

# Yedek modeller
BACKUP_MODELS = {
    "en_to_tr_1": "https://api-inference.huggingface.co/models/facebook/mbart-large-50-many-to-many-mmt",
    "en_to_tr_2": "https://api-inference.huggingface.co/models/Helsinki-NLP/opus-mt-mul-tr",
    "tr_to_en_1": "https://api-inference.huggingface.co/models/facebook/mbart-large-50-many-to-many-mmt"
}

# Token'ı environment variable'dan al
HF_TOKEN = os.getenv("HF_TOKEN", "your_token")

def translate_with_models(text, direction):
    """Metni belirtilen yöne çevir"""
    if not text or not text.strip():
        return ""
    
    headers = {"Authorization": f"Bearer {HF_TOKEN}"}
    payload = {"inputs": text}
    
    # Önce ana modeli dene
    api_url = MODELS.get(direction)
    if api_url:
        try:
            response = requests.post(api_url, headers=headers, json=payload, timeout=30)
            if response.status_code == 200:
                result = response.json()
                if isinstance(result, list) and result and 'translation_text' in result[0]:
                    return result[0]['translation_text']
        except Exception as e:
            print(f"Ana model hatası: {e}")
    
    # Ana model başarısızsa yedekleri sırayla dene
    for key, backup_url in BACKUP_MODELS.items():
        try:
            response = requests.post(backup_url, headers=headers, json=payload, timeout=30)
            if response.status_code == 200:
                result = response.json()
                if isinstance(result, list) and result and 'translation_text' in result[0]:
                    print(f"Yedek model {key} kullanıldı")
                    return result[0]['translation_text']
        except Exception as e:
            print(f"Yedek model {key} hatası: {e}")
            continue
        
        # Rate limiting için kısa bekleme
        time.sleep(0.5)
    
    return "Çeviri başarısız"

def process_translations(input_file, output_file):
    """Çeviri dosyasını işle"""
    try:
        with open(input_file, "r", encoding="utf-8") as f:
            data = json.load(f)
            
        # DÜZELTME: Eğer data bir dict ise ve missing_translations anahtarı varsa
        if isinstance(data, dict) and "missing_translations" in data:
            data = data["missing_translations"]
            
    except FileNotFoundError:
        print(f"Dosya bulunamadı: {input_file}")
        return
    except json.JSONDecodeError:
        print(f"JSON formatı hatalı: {input_file}")
        return
    
    results = []
    total_items = len(data)
    
    for i, item in enumerate(data, 1):
        print(f"İşleniyor {i}/{total_items}: {item.get('question', '')[:50]}...")
        
        # DÜZELTME: completed_translation alanı kontrolü kaldırıldı
        direction = "en_to_tr" if item["missing_language"] == "tr" else "tr_to_en"
        
        question_trans = translate_with_models(item["question"], direction)
        answer_trans = translate_with_models(item["answer"], direction)
        
        results.append({
            "url": item.get("url"),
            "source_language": item.get("source_language"),
            "missing_language": item.get("missing_language"),
            "question": item.get("question"),
            "answer": item.get("answer"),
            "question_translation": question_trans,
            "answer_translation": answer_trans
        })
        
        # Rate limiting için bekleme
        time.sleep(1)
    
    # Sonuçları kaydet
    try:
        with open(output_file, "w", encoding="utf-8") as out:
            json.dump(results, out, ensure_ascii=False, indent=2)
        print(f"Çeviri sonuçları {output_file} dosyasına kaydedildi.")
        print(f"Toplam {len(results)} öğe çevrildi.")
    except Exception as e:
        print(f"Dosya kaydetme hatası: {e}")

# Ana çalıştırma
if __name__ == "__main__":
    # Test çevirileri
    print("Test çevirileri:")
    print("TR->EN:", translate_with_models("Merhaba, nasılsın?", "tr_to_en"))
    print("EN->TR:", translate_with_models("Hello, how are you?", "en_to_tr"))
    
    # Dosya işleme 
    input_file = r"C:\Users\Monster\Desktop\translator\missing_translations_structured.json"  # Doğru dosya adı
    output_file = r"C:\Users\Monster\Desktop\translator\translation_results.json"  # Daha açık isim
    
    process_translations(input_file, output_file)
