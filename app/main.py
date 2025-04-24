from pdf_parser import extract_text_smart
from gpt_extractor import init_api_key, extract_underwriting_json
from output_writer import write_json_to_excel
import json
import re
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
        cleaned_response = re.search(r"\{.*\}", raw_response, re.DOTALL)
        if cleaned_response:
            data = json.loads(cleaned_response.group(0))
        else:
            raise json.JSONDecodeError("No JSON found", raw_response, 0)
        print("✅ Underwriting fields extracted:\n")
        print(json.dumps(data, indent=2))

        filename = os.path.basename(pdf_path).replace(".pdf", "_fields")

        
        output_folder = os.path.join(os.path.dirname(__file__), "output")
        os.makedirs(output_folder, exist_ok=True)

        
        json_path = os.path.join(output_folder, f"{filename}.json")
        excel_path = os.path.join(output_folder, f"{filename}.xlsx")

        
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        print(f"\n[📁] JSON saved to: {json_path}")

        
        write_json_to_excel(data, excel_path)

    except json.JSONDecodeError:
        print("⚠️ GPT response was not valid JSON:\n")
        print(raw_response)

if __name__ == "__main__":
    main()