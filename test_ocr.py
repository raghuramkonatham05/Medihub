from ocr.ocr_engine import extract_text
from ocr.lab_parser import extract_lab_values
from ml.report_classifier import detect_diseases

# 🔽 CHANGE THIS PATH to one real uploaded file
FILE_PATH = "uploads/WhatsApp Image 2025-12-30 at 13.18.02.jpeg"

print("\n========== OCR TEXT ==========\n")
text = extract_text(FILE_PATH)
print(text)

print("\n========== LAB VALUES ==========\n")
labs, flags = extract_lab_values(text)
print(labs)
print("Flags:", flags)

print("\n========== DISEASE DETECTION ==========\n")
diseases = detect_diseases(labs)
print(diseases)
