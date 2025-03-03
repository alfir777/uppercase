import uuid

import pytest
from django.contrib.auth.models import User
from django.test import Client


@pytest.mark.django_db
def test_file_upload():
    client = Client()
    user = User.objects.create_user(
        username='test_user',
    )
    with open('test_file.txt', 'wb') as f:
        f.write(b'Test file content')
    with open('test_file.txt', 'rb') as f:
        response = client.post('/api/v1/files/upload/', {'file': f, 'user_id': user.pk})
    assert response.status_code == 200
    assert 'file_id' in response.json()


@pytest.mark.django_db
def test_file_download():
    client = Client()
    user = User.objects.create_user(
        username='test_user',
    )
    with open('test_file.txt', 'wb') as f:
        f.write(b'Test file content')
    with open('test_file.txt', 'rb') as f:
        response_upload = client.post('/api/v1/files/upload/', {'file': f, 'user_id': user.pk})
    response_data = response_upload.json()
    response = client.get(f'/api/v1/files/{response_data['file_id']}/download/', {'user_id': user.pk})
    assert response.status_code == 200
    assert response.get('Content-Disposition') is not None
