#data_mapping

def map_ocr_fields_to_data(form_fields, data):
    mapped_fields = {}
    used_keys = set()  # Track keys that have been used to avoid overlaps

    for field in form_fields:
        field_label = field['text'].lower()
        for key in data:
            if key in field_label and key not in used_keys:  # Check for exact match and not already used
                mapped_fields[(field['bbox'], field['page'])] = data[key]  # Added page information to key
                used_keys.add(key)  # Mark this key as used
                print(f"Mapped '{data[key]}' to field '{field_label}'")  # Debug print for mapping
                break  # Break to avoid multiple mappings for the same field

    return mapped_fields