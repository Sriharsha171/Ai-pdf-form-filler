#data_extarctor

import fitz
import pdfplumber
import pytesseract


def extract(pdf_path):
    pdf = fitz.open(pdf_path)
    form_fields = []

    # Layout extraction
    for page_num in range(len(pdf)):
        page = pdf.load_page(page_num)
        blocks = page.get_text("dict")["blocks"]  # Extract blocks of text
        for block in blocks:
            if "lines" in block:
                for line in block["lines"]:
                    for span in line["spans"]:
                        text = span["text"].strip()
                        if not text:  # Detect empty spaces (potential form fields)
                            bbox = span["bbox"]
                            form_fields.append({"text": "[BLANK]", "bbox": bbox, "page": page_num})
                        else:
                            # If there is text, we could capture labeled fields too
                            form_fields.append({"text": text, "bbox": span["bbox"], "page": page_num})

    # OCR-based extraction
    with pdfplumber.open(pdf_path) as pdf:
        for i, page in enumerate(pdf.pages):
            img = page.to_image().original
            data = pytesseract.image_to_data(img, output_type=pytesseract.Output.DICT)
            n_boxes = len(data['level'])
            for j in range(n_boxes):
                (x, y, w, h) = (data['left'][j], data['top'][j], data['width'][j], data['height'][j])
                text = data['text'][j].strip()
                if text:  # Only append if there's recognized text
                    form_fields.append({"bbox": (x, y, w + x, h + y), "page": i, "text": text})

    print("Extracted Form Fields:")
    for field in form_fields:
        print(field)

    return form_fields
