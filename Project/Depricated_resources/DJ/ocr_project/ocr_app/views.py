from django.shortcuts import render

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import pytesseract
from PIL import Image
import os

# Ensure Tesseract path is configured
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

@csrf_exempt
def ocr_process(request):
    if request.method == "POST" and request.FILES.get("image"):
        # Save uploaded file to media directory
        uploaded_file = request.FILES["image"]
        file_path = os.path.join(settings.MEDIA_ROOT, uploaded_file.name)
        with open(file_path, 'wb') as f:
            for chunk in uploaded_file.chunks():
                f.write(chunk)

        # Perform OCR
        try:
            img = Image.open(file_path)
            extracted_text = pytesseract.image_to_string(img)
            os.remove(file_path)  # Cleanup uploaded file
            return JsonResponse({"success": True, "text": extracted_text})
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)})

    return JsonResponse({"success": False, "error": "Invalid request"})

