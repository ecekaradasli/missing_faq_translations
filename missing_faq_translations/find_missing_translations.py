import json

with open(r"C:\Users\Monster\Desktop\translator\filtered_2.json", "r", encoding="utf-8") as f:
    data = json.load(f)

def get_questions(qa_list):
    return set((item["question"], item["answer"]) for item in qa_list)

missing_structured = []
for entry in data:
    en_questions = get_questions(entry.get("en", []))
    tr_questions = get_questions(entry.get("tr", []))

    missing_tr = en_questions - tr_questions
    missing_en = tr_questions - en_questions

    for q, a in missing_tr:
        missing_structured.append({
            "url": entry["url"],
            "missing_language": "tr",
            "question": q,
            "answer": a,
            "source_language": "en"
        })

    for q, a in missing_en:
        missing_structured.append({
            "url": entry["url"],
            "missing_language": "en",
            "question": q,
            "answer": a,
            "source_language": "tr"
        })

with open(r"C:\Users\Monster\Desktop\translator\missing_translations_structured.json", "w", encoding="utf-8") as out_json:
    json.dump(missing_structured, out_json, ensure_ascii=False, indent=2)
print(f"Oluşturulan kayıt sayısı: {len(missing_structured)}")
print("missing_translations_structured.json dosyası oluşturuldu.")
