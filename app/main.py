from pdf_parser import extract_text_smart
from gpt_extractor import init_api_key, extract_underwriting_json
import json
import os

def main():
    init_api_key()

    pdf_path = input("📄 Enter path to OM PDF: ").strip()

    if not os.path.exists(pdf_path):
        print(f"❌ File not found: {pdf_path}")
        return

    print("🔍 Extracting text from PDF...")
    text = extract_text_smart(pdf_path)

    print("🤖 Sending to GPT-4o...")
    raw_response = extract_underwriting_json(text)

    try:
        data = json.loads(raw_response)
        print("✅ Underwriting fields extracted:\n")
        print(json.dumps(data, indent=2))

        os.makedirs("output", exist_ok=True)
        filename = os.path.basename(pdf_path).replace(".pdf", "_fields.json")
        out_path = os.path.join("output", filename)
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        print(f"\n[📁] Saved to {out_path}")

    except json.JSONDecodeError:
        print("⚠️ GPT response was not valid JSON:\n")
        print(raw_response)

if __name__ == "__main__":
    main()