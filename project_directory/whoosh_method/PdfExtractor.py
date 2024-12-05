import PyPDF2
import pytesseract
from PIL import Image
import io
import fitz  # PyMuPDF for extracting images
from PyPDF2 import PdfReader
from pdf2image import convert_from_path

file_path = r"C:\coding\projects\Pathology finder\Cardiology Textbook.pdf"

chapter1 = 12
chapter2 = 37
chapter3 = 44
chapter4 = 85
chapter5 = 123
chapter6 = 145
chapter7 = 173
chapter8 = 203
chapter9 = 231
chapter10 = 260
chapter11 = 279
chapter12 = 298
chapter13 = 321
chapter14 = 345
chapter15 = 361
chapter16 = 384
chapter17 = 411 

chapterindex = [chapter1, chapter2, chapter3, chapter4, chapter5, chapter6, chapter7, chapter8, chapter9, chapter10, chapter11, chapter12, chapter13, chapter14, chapter15, chapter16, chapter17]


def extract_text_from_pdf_with_ocr(pdf_path, start_page, end_page):
    # Convert PDF pages to images
    pages = convert_from_path(pdf_path, first_page=start_page, last_page=end_page)

    extracted_text = ""

    # Loop through the pages
    for page_num, page_image in enumerate(pages, start=start_page):
        print(f"Extracting text from page {page_num}...")
        
        # Perform OCR on the image (page)
        text = pytesseract.image_to_string(page_image, config='--psm 6')

        # Append the extracted text
        extracted_text += text

    return extracted_text


def save_text_to_file(text, output_file_path):
    with open(output_file_path, "w", encoding="utf-8") as file:
        file.write(text)  # Write the extracted text to the file


start_page = 12  # Starting from page 3
end_page = 12   # Ending at page 10
text_content = extract_text_from_pdf_with_ocr(file_path, start_page, end_page)

# Save the extracted text to a file
output_file_path = "extracted_text.txt"
save_text_to_file(text_content, output_file_path)

print(f"Text content from pages {start_page} to {end_page} saved to {output_file_path}")


# reader = PdfReader(file_path)

# # Attempt to extract text from the first page
# page = reader.pages[11]
# text = page.extract_text()
# print(text)

for i in range(len(chapterindex)-1):
    text_content = extract_text_from_pdf_with_ocr(file_path, chapterindex[i], chapterindex[i+1])
    output_file_path = f"chapter{i + 1}.txt"
    save_text_to_file(text_content, output_file_path)
