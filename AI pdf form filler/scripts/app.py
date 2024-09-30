#app

from flask import Flask, request, render_template_string, send_file
import os

from data_extarct import extract
from data_loader import load_data_from_file
from data_mapping import map_ocr_fields_to_data
from data_filling import fill_pdf_form

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'samples'  # Change this to your samples folder
app.config['OUTPUT_FOLDER'] = r'C:\Users\bksh1\Desktop\final\scripts\outputs'  # Set to your desired outputs folder

# Ensure the output folder exists
os.makedirs(app.config['OUTPUT_FOLDER'], exist_ok=True)

# HTML Template as a string
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI PDF Form Filler</title>
    <style>
        body {
            background-color: #0D0D0D;
            color: #E0E0E0;
            font-family: 'Roboto', sans-serif;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
        }
        h1, h2 {
            text-align: center;
            color: #00FFB3;
        }
        form {
            background: rgba(255, 255, 255, 0.05);
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0px 0px 20px rgba(0, 255, 179, 0.5);
            display: flex;
            flex-direction: column;
            align-items: center;
        }
        input[type="file"] {
            margin: 20px 0;
            color: #00FFB3;
            border: 1px solid #00FFB3;
            padding: 10px;
            background-color: transparent;
            border-radius: 5px;
            width: 250px;
        }
        button {
            background-color: #00FFB3;
            color: #0D0D0D;
            padding: 10px 20px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-size: 16px;
            transition: background-color 0.3s ease;
        }
        button:hover {
            background-color: #00CC8C;
        }
        a {
            color: #00FFB3;
            text-decoration: none;
            padding: 10px;
            background: rgba(255, 255, 255, 0.05);
            border-radius: 5px;
            margin-top: 20px;
            display: inline-block;
            transition: background-color 0.3s ease;
        }
        a:hover {
            background-color: #00CC8C;
        }
    </style>
</head>
<body>
    <div>
        <h1>AI PDF Form Filler</h1>
        <form action="/upload" method="post" enctype="multipart/form-data">
            <input type="file" name="file" required>
            <button type="submit">Fill the Form Using AI</button>
        </form>
        {% if filled_pdf %}
            <h2>Your filled PDF is ready!</h2>
            <a href="{{ url_for('view_filled_form', filename=filled_pdf.split('/')[-1]) }}" download>Download Filled PDF</a>
        {% endif %}
    </div>
</body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "No file uploaded", 400

    file = request.files['file']
    if file.filename == '':
        return "No selected file", 400

    # Save the uploaded file to the samples folder
    pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(pdf_path)

    # Load data from the data.txt file
    data_path = r"C:\Users\bksh1\Desktop\final\scripts\data\data.txt"
    data = load_data_from_file(data_path)

    # Extract form fields
    form_fields = extract(pdf_path)

    # Map the form fields to the data
    mapped_fields = map_ocr_fields_to_data(form_fields, data)

    # Prepare output PDF path in the outputs folder
    output_pdf_path = os.path.join(app.config['OUTPUT_FOLDER'], f'filled_{file.filename}')

    # Fill the PDF with mapped data
    fill_pdf_form(pdf_path, output_pdf_path, mapped_fields)

    # Extract just the filename from the output path
    filled_filename = os.path.basename(output_pdf_path)

    # Provide a link to view or download the filled form
    return render_template_string(HTML_TEMPLATE, filled_pdf=filled_filename)

@app.route('/view/<filename>')
def view_filled_form(filename):
    filled_pdf_path = os.path.join(app.config['OUTPUT_FOLDER'], filename)
    return send_file(filled_pdf_path)


if __name__ == '__main__':
    app.run(debug=True)
