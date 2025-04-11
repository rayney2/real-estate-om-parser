import pdfplumber
import fitz  # PyMuPDF
import pytesseract
from pdf2image import convert_from_path
import tempfile
import os


def extract_text_with_pdfplumber(pdf_path):
    """Extracts layout-aware text from a digital (non-scanned) PDF."""
    with pdfplumber.open(pdf_path) as pdf:
        return "\n".join(page.extract_text() or "" for page in pdf.pages)


def extract_text_with_fitz(pdf_path):
    """Alternative extractor using PyMuPDF (good for certain layouts)."""
    doc = fitz.open(pdf_path)
    return "\n".join([page.get_text("text") for page in doc])


def extract_text_with_ocr(pdf_path, dpi=300):
    """Uses OCR to extract text from scanned/image PDFs."""
    images = convert_from_path(pdf_path, dpi=dpi)
    text = ""
    for img in images:
        text += pytesseract.image_to_string(img) + "\n"
    return text


def is_scanned_pdf(pdf_path):
    """
    Heuristic to determine if a PDF is likely scanned (has no extractable text).
    Tries the first few pages with pdfplumber.
    """
    with pdfplumber.open(pdf_path) as pdf:
        for i, page in enumerate(pdf.pages[:3]):
            if page.extract_text():
                return False
    return True


def extract_text_smart(pdf_path):
    """
    Smart PDF text extraction:
    - Uses `pdfplumber` or `fitz` for digital PDFs
    - Falls back to OCR for image-based/scanned PDFs
    """
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