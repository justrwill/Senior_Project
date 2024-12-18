from flask import Flask, request, jsonify, render_template
from werkzeug.utils import secure_filename
from PIL import Image
import pytesseract
import os
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import wordnet

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = './uploads'

# Ensure Tesseract path is set (Windows users)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def get_definitions(word):
    """
    Retrieve definitions for a given word using NLTK's WordNet.
    """
    synsets = wordnet.synsets(word)
    definitions = [syn.definition() for syn in synsets]
    return definitions[:3]  # Return up to 3 definitions for brevity

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/process', methods=['POST'])
def process_image():
    if 'image' not in request.files:
        return jsonify({"success": False, "error": "No file uploaded"}), 400

    file = request.files['image']
    if file.filename == '':
        return jsonify({"success": False, "error": "No file selected"}), 400

    filename = secure_filename(file.filename)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)

    try:
        # Perform OCR
        img = Image.open(file_path)
        extracted_text = pytesseract.image_to_string(img)
        os.remove(file_path)  # Cleanup uploaded file

        # Tokenize text and get definitions
        words = word_tokenize(extracted_text)
        word_definitions = {}
        for word in words:
            if word.isalpha():  # Ignore non-alphabetical tokens
                definitions = get_definitions(word.lower())
                if definitions:  # Only include words with definitions
                    word_definitions[word] = definitions

        return jsonify({
            "success": True,
            "text": extracted_text,
            "word_definitions": word_definitions,
        })

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

if __name__ == '__main__':
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    app.run(debug=True)
