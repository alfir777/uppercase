from django.urls import path

from storage.views import api_documentation, download_file, upload_file

urlpatterns = [
    path('', api_documentation, name='api_documentation'),
    path('api/v1/files/upload/', upload_file, name='upload_file'),
    path('api/v1/files/<uuid:file_id>/download/', download_file, name='download_file'),
]
