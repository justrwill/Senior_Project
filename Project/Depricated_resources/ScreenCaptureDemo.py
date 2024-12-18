import tkinter as tk
from PIL import ImageGrab
import pytesseract
import requests
import time
import os
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

class ScreenCaptureApp:
    def __init__(self, root):
        self.root = root
        self.root.attributes('-fullscreen', True)
        self.root.attributes('-alpha', 0.3)
        self.root.attributes('-topmost', True)
        self.root.bind('<ButtonPress-1>', self.on_mouse_down)
        self.root.bind('<B1-Motion>', self.on_mouse_drag)
        self.root.bind('<ButtonRelease-1>', self.on_mouse_up)
        self.canvas = tk.Canvas(root, cursor='cross', bg='white')
        self.canvas.pack(fill='both', expand=True)
        self.rect = None
        self.start_x = None
        self.start_y = None

    def on_mouse_down(self, event):
        self.start_x = event.x
        self.start_y = event.y
        if not self.rect:
            self.rect = self.canvas.create_rectangle(
                self.start_x, self.start_y, self.start_x, self.start_y, outline='blue', width=2
            )

    def on_mouse_drag(self, event):
        self.canvas.coords(self.rect, self.start_x, self.start_y, event.x, event.y)

    def on_mouse_up(self, event):
        end_x = event.x
        end_y = event.y
        self.capture_screen(self.start_x, self.start_y, end_x, end_y)
        self.root.destroy()

    def capture_screen(self, start_x, start_y, end_x, end_y):
        self.root.withdraw()
        time.sleep(0.1)
        x1, y1 = min(start_x, end_x), min(start_y, end_y)
        x2, y2 = max(start_x, end_x), max(start_y, end_y)
        bbox = (x1, y1, x2, y2)

        screenshot = ImageGrab.grab(bbox)
        screenshot.save('screen-shot.png')
        print("Screenshot saved as 'screen-shot.png'.")
        self.perform_ocr('screen-shot.png')

    def perform_ocr(self, image_path):
        try:
            text = pytesseract.image_to_string(image_path)
            print("Extracted Text:")
            print(text)
            with open("extracted_text.txt", "w") as file:
                file.write(text)
            print("Extracted text saved as 'extracted_text.txt'.")
            self.get_definitions(text)
        except Exception as e:
            print(f"Error during OCR: {e}")

    def get_definitions(self, text):
        # Tokenize and filter words using NLTK
        nltk.download('punkt')
        nltk.download('stopwords')
        words = word_tokenize(text.lower())  # Tokenize text
        filtered_words = [
            word for word in words if word.isalpha() and word not in stopwords.words('english')
        ]

        # Fetch definitions for unique words
        definitions = {}
        for word in set(filtered_words):
            definition = self.fetch_definition(word)
            if definition:
                definitions[word] = definition

        # Print and save definitions
        with open("word_definitions.txt", "w") as file:
            for word, definition in definitions.items():
                output = f"{word}: {definition}\n"
                print(output)
                file.write(output)
        print("Word definitions saved as 'word_definitions.txt'.")

    def fetch_definition(self, word):
        api_key = "YOUR_API_KEY" #Placeholder for when API changes
        url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}" 
        try:
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                if data and isinstance(data, list):
                    return data[0].get("meanings", [{}])[0].get("definitions", [{}])[0].get("definition", "Definition not found.")
            else:
                print(f"Definition not found for '{word}'.")
        except Exception as e:
            print(f"Error fetching definition for '{word}': {e}")
        return "Definition not found."


if __name__ == '__main__':
    # Ensure Tesseract-OCR is installed and accessible
    if not os.getenv('TESSDATA_PREFIX'):
        pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

    root = tk.Tk()
    app = ScreenCaptureApp(root)
    root.mainloop()
