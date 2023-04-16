from django.test import TestCase
from django.urls import reverse, resolve
from .views import csv_to_json
from rest_framework import status
from rest_framework.test import APIClient
from io import BytesIO
from .consts import MESSAGES
from django.utils.translation import gettext as _


# ルーティングを確認するテストケース
class TestUrls(TestCase):
    def test_put_csv_to_json(self):
        url = reverse('csv_to_json')
        view = resolve(url)
        self.assertEqual(view.func, csv_to_json)

# 各リクエストパターンを確認するテストケース
class CsvToJsonTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_csv_to_json_with_valid_file(self):
        # テストに必要なデータを準備する
        csv_file_data = b'name,age,gender\nAlice,25,F\nBob,30,M\n'
        csv_file = BytesIO(csv_file_data)
        csv_file.name = 'test.csv'

        # テストを実行する
        url = reverse('csv_to_json')
        response = self.client.put(url, {'file': csv_file}, format='multipart')

        # テスト結果を検証する
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected_response = [{'name': 'Alice', 'age': '25', 'gender': 'F'}, {
            'name': 'Bob', 'age': '30', 'gender': 'M'}]
        self.assertEqual(response.data, expected_response)

    def test_csv_to_json_with_missing_file(self):
        # テストを実行する
        url = reverse('csv_to_json')
        response = self.client.put(url, {}, format='multipart')

        # テスト結果を検証する
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {'error': _(MESSAGES['CSV_FILE_NOT_SUBMITTED'])})

    def test_csv_to_json_with_large_file(self):
        # テストに必要なデータを準備する
        csv_file_data = b'x\n' * 201
        csv_file = BytesIO(csv_file_data)
        csv_file.name = 'test.csv'

        # テストを実行する
        url = reverse('csv_to_json')
        response = self.client.put(url, {'file': csv_file}, format='multipart')

        # テスト結果を検証する
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data, {'error': _(MESSAGES['CSV_FILE_TOO_LARGE_LINES'])})

    def test_csv_to_json_with_invalid_file(self):
        # テストに必要なデータを準備する
        csv_file_data = b'name,age,gender\nAlice,25Bob,30,M\n'
        csv_file = BytesIO(csv_file_data)
        csv_file.name = 'test.csv'

        # テストを実行する
        url = reverse('csv_to_json')
        response = self.client.put(url, {'file': csv_file}, format='multipart')

        # テスト結果を検証する
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {'error': _(MESSAGES['INVALID_CSV_FORMAT'])})
