# csv_to_json_converter
- PUTメソッドのHTTPリクエストで送信されたCSVファイルを解析し、JSON形式に-変換して返却するWeb APIです。
- Web画面からアップロードされたCSVファイルの内容をlocalStorage に保存したい時に使用します。
- [この画面](https://github.com/orphanizee/sakusaku)から呼び出すことを想定しています。
- 開発環境で使用することを想定しています。

# Supported Versions
- Python 3.10.5
- Django 4.1.1

# Installation
1. プロジェクトをダウンロード
    ```bash
    git clone https://github.com/orphanizee/csv_to_json_converter.git
    ```
1. CORS設定を追加
    リクエストを許可したいドメインを追加します
    csv_to_json_converter/settings.py
    ```python
    # CORS設定
    CORS_ORIGIN_WHITELIST = [
        'http://localhost:3000/'
    ]
    ```

1. 起動
    ```bash
    cd csv_to_json_converter
    python manage.py runserver
    ```

1. テスト
    ```bash
    python manage.py test
    ```

# Usage
以下の形式でリクエストを送信して下さい。
|項目|値|
|:--|:--|
|エンドポイント|http://127.0.0.1:8000/csv-to-json/|
|HTTPメソッド|PUT|
|HTTPヘッダ|Content-type: multipart/form-data|
|リクエストボディ|file: <CSVデータ>|

# Note
- 200行を超えるCSVファイル、または50MBを超えるCSVファイル受信時には、エラーレスポンスを返却します
- CORS設定で、localhost:3000 からのリクエストを許可しています

# License
This project is licensed under the MIT License.

# CHANGELOG
## 1.0.0 - 2023/04/16
新規作成
