# ocr/ocr_engine.py

import cv2
import numpy as np
import time
import pdfplumber
from paddleocr import PaddleOCR
from pdf2image import convert_from_path

# ==================================================
# Lazy OCR init (PaddleOCR v5 SAFE)
# ==================================================
_ocr = None


def get_ocr():
    global _ocr
    if _ocr is None:
        print("🟡 Initializing PaddleOCR (LAB REPORT MODE)...", flush=True)
        _ocr = PaddleOCR(
            lang="en",
            use_angle_cls=True
        )
    return _ocr


# ==================================================
# Image preprocessing (for lab reports)
# ==================================================
def preprocess_image(img):
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    gray = cv2.bilateralFilter(gray, 11, 75, 75)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    gray = clahe.apply(gray)
    return cv2.cvtColor(gray, cv2.COLOR_GRAY2RGB)


# ==================================================
# ✅ PaddleOCR v5 RESULT PARSER (CORRECT)
# ==================================================
def parse_ocr_result(result):
    """
    PaddleOCR v5 returns:
    [
      {
        'rec_texts': [...],
        'rec_scores': [...],
        ...
      }
    ]
    """
    lines = []

    if not result:
        return lines

    for page in result:
        if isinstance(page, dict) and "rec_texts" in page:
            for text in page["rec_texts"]:
                if isinstance(text, str) and text.strip():
                    lines.append(text.strip())

    return lines


# ==================================================
# MAIN OCR FUNCTION
# ==================================================
def extract_text(file_path):
    start_time = time.time()

    # ==================================================
    # 1️⃣ DIGITAL PDF FIRST
    # ==================================================
    if file_path.lower().endswith(".pdf"):
        try:
            texts = []
            with pdfplumber.open(file_path) as pdf:
                for page in pdf.pages:
                    t = page.extract_text()
                    if t:
                        texts.append(t)

            digital_text = "\n".join(texts)
            if len(digital_text.strip()) > 100:
                print("✅ Digital PDF detected – skipping OCR", flush=True)
                return digital_text

        except Exception as e:
            print("⚠️ Digital PDF failed, using OCR:", e, flush=True)

    # ==================================================
    # 2️⃣ OCR FOR IMAGES / SCANNED PDF
    # ==================================================
    ocr = get_ocr()
    extracted_lines = []

    try:
        # ---------- PDF OCR ----------
        if file_path.lower().endswith(".pdf"):
            pages = convert_from_path(file_path, dpi=300)
            for page in pages:
                img = preprocess_image(np.array(page))
                result = ocr.ocr(img)
                extracted_lines.extend(parse_ocr_result(result))

        # ---------- IMAGE OCR ----------
        else:
            img = cv2.imread(file_path)
            if img is None:
                print("❌ Image read failed", flush=True)
                return ""

            img = preprocess_image(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
            result = ocr.ocr(img)
            extracted_lines.extend(parse_ocr_result(result))

    except Exception as e:
        print("❌ OCR ERROR:", e, flush=True)
        return ""

    # ==================================================
    # 🔍 OCR VERIFICATION OUTPUT (CRITICAL)
    # ==================================================
    print(f"🟢 OCR completed in {time.time() - start_time:.2f}s", flush=True)
    print(f"🔎 OCR lines extracted: {len(extracted_lines)}", flush=True)

    print("\n========== OCR RAW OUTPUT (FIRST 40 LINES) ==========\n")
    for i, line in enumerate(extracted_lines[:40], start=1):
        print(f"{i:02d}: {line}")
    print("\n====================================================\n")

    return "\n".join(extracted_lines)
