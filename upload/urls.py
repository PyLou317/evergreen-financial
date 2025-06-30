from django.urls import path

from .views import *

app_name = 'upload'

urlpatterns = [
    path('', upload_statement, name="file_upload")
]