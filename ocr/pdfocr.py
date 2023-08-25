import fitz  # PyMuPDF
import pytesseract
from PIL import Image
import sys
import os
if len(sys.argv) != 2:
    print("Usage: python script_name.py pdf_file_path")
    sys.exit(1)
pdf_file_path = sys.argv[1]
if not os.path.exists(pdf_file_path):
    print("PDF file does not exist.")
    sys.exit(1)
output_text_file = os.path.join(os.path.dirname(pdf_file_path), os.path.splitext(os.path.basename(pdf_file_path))[0] + '.txt')
pdf_document = fitz.open(pdf_file_path)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
with open(output_text_file, 'a') as output_file:
    for page_num in range(pdf_document.page_count):
        page = pdf_document[page_num]
        image = page.get_pixmap()     
        img = Image.frombytes("RGB", [image.width, image.height], image.samples) # Convert the Pixmap to a PIL Image
        extracted_text = pytesseract.image_to_string(img, lang='eng')  # Perform OCR on the image
        #output_file.write(f"Page {page_num + 1}:\n{extracted_text}\n\n")
        output_file.write(f"{extracted_text}\n\n")
pdf_document.close()