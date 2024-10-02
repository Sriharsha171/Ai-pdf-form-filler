#data_mapping

def map_ocr_fields_to_data(form_fields, data):
    mapped_fields = {}
    used_keys = set()  # Track keys

    for field in form_fields:
        field_label = field['text'].lower()
        for key in data:
            if key in field_label and key not in used_keys:  # Check for exact match
                mapped_fields[(field['bbox'], field['page'])] = data[key]
                used_keys.add(key)
                print(f"Mapped '{data[key]}' to field '{field_label}'")
                break

    return mapped_fields