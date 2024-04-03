import os
import fitz  # PyMuPDF
from PIL import Image
import pytesseract
import shutil

def convert_pdf_to_text(pdf_path, ocr_output_dir):
    doc = fitz.open(pdf_path)
    text = ""
    
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        pix = page.get_pixmap()
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        
        text += pytesseract.image_to_string(img)
    
    output_file_path = os.path.join(ocr_output_dir, os.path.basename(pdf_path).replace('.pdf', '_OCR.txt'))
    with open(output_file_path, 'w') as f:
        f.write(text)

def process_directory(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".pdf"):
                pdf_path = os.path.join(root, file)
                ocr_output_dir = root + "_OCR"
                if not os.path.exists(ocr_output_dir):
                    os.makedirs(ocr_output_dir)
                convert_pdf_to_text(pdf_path, ocr_output_dir)

directory = input("Enter the directory to process: ")
process_directory(directory)


