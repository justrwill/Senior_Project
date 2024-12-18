from django.urls import path
from .views import ocr_process

urlpatterns = [
    path('process/', ocr_process, name='ocr_process'),
]
