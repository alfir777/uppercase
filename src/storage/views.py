from typing import Union

from django.http import FileResponse, Http404, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from storage.repositories import FileDBRepository, FileRepository
from storage.services import FileService
from storage.tools import log_action

MAX_FILE_SIZE = 16 * 1024 * 1024


def api_documentation(request) -> JsonResponse:
    doc = {
        'endpoints': {
            'api/v1/files/upload/': 'POST - Upload file with form-data (file, user_id)',
            'api/v1/files/<uuid:file_id>/download/': 'GET - Download file with query parameter (user_id)'
        }
    }
    return JsonResponse(doc)


@csrf_exempt
def upload_file(request) -> JsonResponse:
    repository: FileRepository = FileDBRepository()
    service = FileService(repository)
    if request.method == 'POST':
        user_id = request.user.id if request.user.id else int(request.POST.get('user_id', None))
        if not user_id:
            return JsonResponse({'error': 'Invalid user'}, status=401)

        data_file = request.FILES.get('file')

        if not data_file:
            return JsonResponse({'error': 'Invalid file'}, status=400)
        if data_file.size > MAX_FILE_SIZE:
            return JsonResponse({'error': 'File too large (max size 16Mb)'}, status=400)

        file_id = service.save_file(data_file, user_id)
        log_action(user_id, f'Uploaded file {data_file.name}')

        return JsonResponse({'file_id': file_id}, status=201)
    return JsonResponse({'error': 'Invalid request'}, status=400)


def download_file(request, file_id: str) -> Union[FileResponse, JsonResponse]:
    repository: FileRepository = FileDBRepository()
    service = FileService(repository)
    user_id = request.user.id if request.user.id else int(request.GET.get('user_id', None))
    if not user_id:
        return JsonResponse({'error': 'Invalid user'}, status=401)
    try:
        file_entry = service.get_file(file_id)
    except Http404:
        log_action(user_id, f'File not found')
        return JsonResponse({'error': 'File not found'}, status=404)
    restored_file_path = service.unzip_file(file_id)
    log_action(user_id, f'Downloaded file {file_entry.original_name}')
    return FileResponse(open(restored_file_path, 'rb'), as_attachment=True, filename=file_entry.original_name)
