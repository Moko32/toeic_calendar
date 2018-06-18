# toeic_calendar
TOEIC Testの日程を公式サイトから抽出してGoogle Calendarに登録する

## Usage
### 1. GoogleからAPI情報を取得する
https://console.developers.google.com/ からGoogle Calendar API のOAuth認証情報が格納されたJSONファイルをダウンロードし，'json'ディレクトリに格納する
### 2. プログラムにJSONファイルの名前を記述する
toeic_calendar.pyにて
```python
# 以下の変数にクライアントのクレデンシャル情報が入ったJSONファイルの名前を書いておく
CLIENT_SECRET_FILE = 'json/hogehoge.json'
```
### 3. プログラム実行
`python toeic_calendar.py`
