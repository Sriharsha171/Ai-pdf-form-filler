#data_filling

import fitz

def fill_pdf_form(input_pdf_path, output_pdf_path, mapped_fields):
    pdf = fitz.open(input_pdf_path)

    for (bbox, page_num), value in mapped_fields.items():
        page = pdf.load_page(page_num)
        x0, y0, x1, y1 = bbox

        # Adjust the y-coordinate to position the text in the placeholder
        adjusted_y = y1-4  # Slight adjustment to position the text lower

        # Fill the field with data
        page.insert_text((x1+5, adjusted_y), value, fontsize=14)  # Adjust position as needed

    # Save the filled PDF
    pdf.save(output_pdf_path)
    pdf.close()
