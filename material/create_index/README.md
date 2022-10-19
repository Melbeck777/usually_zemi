## How to create date

### Set up
`create_date`を自分のPCにコピーしてください．\
`create_date`下で以下のコマンドを実行してください．
```
pip install -r requirements.txt
```
[wkhtmltopdf](https://document.intra-mart.jp/library/forma/public/forma_setup_guide/texts/install/windows/pdf.html)のいインストールが必要


### Folder structure
一例を示すために,10/13のまとめと出力したテキストファイルがあります．
```
bullet_marks.txt   <= 箇条書きに使うマークの一覧
ignore.txt         <= 無視する言葉の一覧
requirements.txt   <= コードを使うために必要なライブラリの記述
READMe.md
READMe.pdf         <= 説明用の資料
2022_schedule.csv　<= 今年度のスケジュール
create_date.py     <= index.pdfを作成する
```

<div style="page-break-before:always"></div>

### Use
1. ゼミの日にまとめられているフォルダをpdfフォルダに入れる
2. `create_date.py`を`create_date`直下で実行
   ```
   py create_date.py
   ```

## Rule
- 作成資料に必要な項目
  - 進捗報告 <!-- title -!>
  - 今後の予定 <!-- title -!>
  - 外部調査 <!-- title -!>
    - 論文
    - 学会誌
  - 参考文献 <!-- title -!>
    - 参考にした技術ブログ
    - ショッピングサイト
    - 本
    - Githubのリンク
    - etc..
  - 作成物 <!-- title -!>
    - ichiのリンク
      - 書いたコード
      - 何かのマニュアル

上記の項目をタイトルとするページを作成して下さい．