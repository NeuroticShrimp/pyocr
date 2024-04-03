import os
from datetime import datetime
import subprocess
import platform

def search_in_files(directory, search_queries):
    search_terms = [term.strip().lower() for term in search_queries.split(',')]  # Split and lowercase search terms
    results = []
    
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith("_OCR.txt"):
                ocr_file_path = os.path.join(root, file)
                with open(ocr_file_path, 'r') as f:
                    file_content = f.read().lower()  # Lowercase file content for case-insensitive search
                    for term in search_terms:
                        if term in file_content:
                            original_pdf_path = ocr_file_path.replace('_OCR.txt', '.pdf')  # Assuming original PDF has same path without '_OCR.txt'
                            results.append((original_pdf_path, datetime.fromtimestamp(os.path.getmtime(ocr_file_path))))
                            print(f"{len(results)}. Found '{term}' in: {original_pdf_path}")
                            print(f"   Date & Time: {results[-1][1]}")
                            break  # Found a term, no need to check the rest
    
    if results:
        choice = input("Enter the number of the PDF to open or 'q' to quit: ")
        if choice.isdigit():
            choice = int(choice)
            if 1 <= choice <= len(results):
                open_pdf(results[choice - 1][0])
            else:
                print("Invalid number. Exiting.")
        elif choice.lower() != 'q':
            print("Invalid input. Exiting.")
    else:
        print("No matching files found.")

def open_pdf(pdf_path):
    if platform.system() == 'Darwin':       # macOS
        subprocess.run(['open', pdf_path])
    elif platform.system() == 'Windows':    # Windows
        subprocess.run(['start', pdf_path], shell=True)
    else:                                   # linux variants
        subprocess.run(['xdg-open', pdf_path])

search_query = input("Enter search query (use ',' to separate multiple terms): ")
directory = input("Enter the directory to search in: ")
search_in_files(directory, search_query)
