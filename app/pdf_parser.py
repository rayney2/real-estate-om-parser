import pdfplumber
import fitz  # PyMuPDF
import pytesseract
from pdf2image import convert_from_path
import tempfile
import os


def extract_text_with_pdfplumber(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        return "\n".join(page.extract_text() or "" for page in pdf.pages)


def extract_text_with_fitz(pdf_path):
    doc = fitz.open(pdf_path)
    return "\n".join([page.get_text("text") for page in doc])


def extract_text_with_ocr(pdf_path, dpi=300):
    images = convert_from_path(pdf_path, dpi=dpi)
    text = ""
    for img in images:
        text += pytesseract.image_to_string(img) + "\n"
    return text


def is_scanned_pdf(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        for i, page in enumerate(pdf.pages[:3]):
            if page.extract_text():
                return False
    return True


def extract_text_smart(pdf_path):
    if is_scanned_pdf(pdf_path):
        print("[pdf_parser] Detected scanned PDF — using OCR")
        return extract_text_with_ocr(pdf_path)
    else:
        print("[pdf_parser] Detected digital PDF — extracting text")
        return extract_text_with_pdfplumber(pdf_path)


if __name__ == "__main__":
    # Quick test
    import sys
    pdf_path = sys.argv[1]
    text = extract_text_smart(pdf_path)
    print(text[:3000])  # Preview first 3k chars