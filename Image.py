from flask import Flask, request, send_file, render_template
from googletrans import Translator
import os
from PIL import Image
import pytesseract

app = Flask(__name__)

DOWNLOAD_FOLDER = os.path.join(os.getcwd(), 'download')
if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)


@app.route('/upload', methods=['POST'])
def upload_file():
    uploaded_file = request.files['file']
    if uploaded_file.filename != '':
        if uploaded_file.filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
            # Handle image file
            text = extract_text_from_image(uploaded_file)
        else:
            # Handle text file
            content = uploaded_file.read().decode('utf-8')  # Decode file content from bytes to string
            text = translate_to_bangla(content)

        # Save translated text to file
        file_path = os.path.join(DOWNLOAD_FOLDER, 'translated_text.txt')
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(text)

        return 'File uploaded and translated successfully.'
    return 'No file uploaded'


def extract_text_from_image(image_file):
    # Open image and perform OCR
    img = Image.open(image_file)
    text = pytesseract.image_to_string(img)
    return text


def translate_to_bangla(english_text):
    translator = Translator()
    translated = translator.translate(english_text, src='en', dest='bn')
    return translated.text


@app.route('/download', methods=['GET'])
def download_file():
    # Send the file for download
    return send_file(os.path.join(DOWNLOAD_FOLDER, 'translated_text.txt'), as_attachment=True)


# Define route for the root URL to render index.html
@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
