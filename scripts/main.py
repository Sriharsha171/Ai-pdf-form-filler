#main

from data_extarct import extract
from data_loader import load_data_from_file
from data_mapping import map_ocr_fields_to_data
from data_filling import fill_pdf_form

if __name__ == "__main__":
    pdf_path = r"C:\Users\bksh1\Desktop\final\scripts\samples\sample1.pdf"
    data_path = r"C:\Users\bksh1\Desktop\final\scripts\data\data.txt"
    output_pdf_path = r"C:\Users\bksh1\Desktop\final\scripts\outputs\filled_sample1.pdf"

    # Load data from the data.txt file
    data = load_data_from_file(data_path)

    # Extract form fields
    form_fields = extract(pdf_path)

    # Map the form fields to the data
    mapped_fields = map_ocr_fields_to_data(form_fields, data)

    # Fill the PDF with mapped data
    fill_pdf_form(pdf_path, output_pdf_path, mapped_fields)

    print(f"Filled PDF saved as: {output_pdf_path}")