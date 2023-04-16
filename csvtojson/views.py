import csv
import io
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .consts import MESSAGES
from django.utils.translation import gettext as _


@api_view(['PUT'])
def csv_to_json(request):
    # リクエストからファイルを取得
    file = request.FILES.get('file')
    if not file:
        return Response({'error': _(MESSAGES['CSV_FILE_NOT_SUBMITTED'])}, status=status.HTTP_400_BAD_REQUEST)

    # CSVファイルが200行以上の場合、エラーを返す
    num_lines = sum(1 for line in file)
    file.seek(0)  # ファイルを先頭に戻す
    if num_lines > 200:
        return Response({'error': _(MESSAGES['CSV_FILE_TOO_LARGE_LINES'])}, status=status.HTTP_400_BAD_REQUEST)

    # CSVファイルが50MB以上の場合、エラーを返す
    if file.size > 50 * 1024 * 1024:
        return Response({'error': _(MESSAGES['CSV_FILE_TOO_LARGE_SIZE'])}, status=status.HTTP_400_BAD_REQUEST)

    # CSVファイルをパースして、JSON形式に変換する
    try:
        csv_data = io.StringIO(file.read().decode('utf-8'))

        # ヘッダー行があるかどうかを検出する
        sniffer = csv.Sniffer()
        has_header = sniffer.has_header(csv_data.read(1024))
        csv_data.seek(0)

        # ヘッダー行がない場合、不正なCSVファイルとして扱う
        if not has_header:
            return Response({'error': _(MESSAGES['INVALID_CSV_FORMAT'])}, status=status.HTTP_400_BAD_REQUEST)

        reader = csv.DictReader(csv_data)
        json_data = [row for row in reader]
        return Response(json_data)
    except csv.Error:
        return Response({'error': _(MESSAGES['INVALID_CSV_FORMAT'])}, status=status.HTTP_400_BAD_REQUEST)
