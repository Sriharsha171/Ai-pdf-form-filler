#data_loader

def load_data_from_file(data_path):
    data_dict = {}
    with open(data_path, 'r') as file:
        for line in file:
            if ":" in line:
                key, value = line.split(":", 1)
                data_dict[key.strip().lower()] = value.strip()  # Normalize to lower case

    print("Loaded Data:")
    for key, value in data_dict.items():
        print(f"{key}: {value}")

    return data_dict


