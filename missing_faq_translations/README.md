# 🌍 Çok Dilli İçerik Çeviri ve Tamamlama Aracı

Bu proje, çoklu dil destekli bir platformda eksik kalan çevirileri otomatik olarak tespit edip tamamlamak amacıyla geliştirilmiştir. TR ⇄ EN dilleri arasında eksik içerikler Hugging Face üzerindeki Light LLM modelleri (Helsinki-NLP, mBART) ile çevrilerek yapılandırılmış JSON formatına entegre edilir.

## 📋 İçindekiler
- [Özellikler](#-özellikler)
- [Kurulum](#-kurulum)
- [Kullanım](#-kullanım)
- [Dosya Formatları](#-dosya-formatları)
- [Kullanılan Modeller](#-kullanılan-modeller)
- [Sorun Giderme](#-sorun-giderme)
- [Güvenlik](#️-güvenlik)

## 🔧 Özellikler
- 🔁 **Çift Yönlü Çeviri**: TR → EN ve EN → TR yönlerinde tam destek
- 🤖 **AI Destekli**: Hugging Face üzerindeki Light LLM modelleri (Helsinki-NLP, mBART)
- 🧠 **Akıllı Tespit**: Eksik çevirileri otomatik olarak tespit ve eşleştirme
- 🛠️ **Güvenilirlik**: Yedek model desteği ve hata yönetimi
- 📂 **Yapılandırılmış Çıktı**: `translation_results.json` formatında sonuç

## 🚀 Kurulum

### Gereksinimler
```bash
pip install requests
```

**Platform Desteği:**
- ✅ Yerel Python ortamı (3.7+)
- ✅ Google Colab / Jupyter (isteğe bağlı)

### Hugging Face Token (Opsiyonel)
- [Hugging Face](https://huggingface.co/join) hesabı açın
- [Token oluşturun](https://huggingface.co/settings/tokens) ve "Read" yetkili bir token alın
- Token'ı ortam değişkeni olarak ekleyin:
  ```bash
  export HF_TOKEN=hf_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
  ```
  veya kodda doğrudan değişkene yazın.

## 🚀 Kullanım

### 1. Eksik Çevirileri Tespit Etme
```bash
python find_missing_translations.py
```
- Girdi: `filtered_2.json`
- Çıktı: `missing_translations_structured.json`

### 2. Eksik Çevirileri Otomatik Tamamlama
```bash
python multi_model_translate.py
```
- Girdi: `missing_translations_structured.json`
- Çıktı: `translation_results.json`

### 3. Sonuçları İnceleme
- Otomatik çeviri sonuçları `translation_results.json` dosyasında yer alır.

## 📁 Dosya Formatları

### Giriş Dosyası: `filtered_2.json`
```json
[
  {
    "url": "https://ornek.com/soru-1",
    "source_language": "tr",
    "missing_language": "en",
    "question": "Havalimanında check-in işlemi nasıl yapılır?",
    "answer": "Check-in işlemi havalimanındaki kiosklardan yapılabilir."
  }
]
```

### Ara Dosya: `missing_translations_structured.json`
Eksik çeviriler yapılandırılmış şekilde tutulur.

### Çıktı Dosyası: `translation_results.json`
```json
[
  {
    "url": "https://ornek.com/soru-1",
    "source_language": "tr",
    "missing_language": "en",
    "question": "Havalimanında check-in işlemi nasıl yapılır?",
    "answer": "Check-in işlemi havalimanındaki kiosklardan yapılabilir.",
    "question_translation": "How do I check in at the airport?",
    "answer_translation": "You can check in using kiosks at the airport."
  }
]
```

## 🤖 Kullanılan Modeller

### Ana Modeller
| Yön | Model | Açıklama |
|-----|-------|----------|
| 🇹🇷→🇬🇧 | `Helsinki-NLP/opus-mt-tr-en` | Türkçe'den İngilizce'ye |
| 🇬🇧→🇹🇷 | `Helsinki-NLP/opus-mt-tc-big-en-tr` | İngilizce'den Türkçe'ye |

### Yedek Modeller
- `facebook/mbart-large-50-many-to-many-mmt` (Çok dilli, yüksek kalite)
- `Helsinki-NLP/opus-mt-mul-tr` (Çok dilli→Türkçe)

### Model Seçim Algoritması
1. Ana model denenir
2. Hata durumunda yedek modeller sırayla test edilir
3. Rate limit veya model hatasında otomatik bekleme ve tekrar deneme

## 🔍 Sorun Giderme

### Yaygın Hatalar
**❌ Dosya bulunamadı**
- Dosya yollarının doğru olduğundan emin olun
- Girdi dosyalarını doğru sırayla üretin

**❌ JSON formatı hatalı**
- Dosyanızın geçerli JSON formatında olduğundan emin olun
- UTF-8 kodlaması kullanın

**❌ API Hataları (429/503/404)**
- Rate limit veya model erişim hatalarında script otomatik olarak bekler ve tekrar dener

## 🛡️ Güvenlik
- Token'ınızı kimseyle paylaşmayın, mümkünse ortam değişkeni kullanın
- Script sadece çeviri yapar, veri toplamaz

## 👤 Geliştirici Notu

Bu araç, çoklu dil destekli içerik sistemlerinde çeviri eksiklerini yapay zeka destekli çözümlerle tamamlamak amacıyla hazırlanmıştır. Her türlü katkı ve geri bildirime açıktır. 