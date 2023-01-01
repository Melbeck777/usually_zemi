## 目的
ゼミでいつ何を発表したのかを覚えていることが出来ないという課題があったため、発表した内容をインデックスとして一覧にすることで閲覧することが目的です。
具体的には、私の研究室ではパワーポイントで資料を作成し、それをpdfにしたものを共有の場所に上げるというルールがあります。
そのルールを利用して、pdfから進捗、予定、参考文献を抜きだして、マークダウンのファイルに追記していくことでインデックスを作っています。



## 使用方法

### セットアップ
`create_index`下で以下のコマンドを実行してください．
```
pip install -r requirements.txt
```
[wkhtmltopdf](https://document.intra-mart.jp/library/forma/public/forma_setup_guide/texts/install/windows/pdf.html)のインストールが必要です．


### フォルダ構成
一例を示すために,10/13のまとめと出力したテキストファイルがあります．
```
│  bullet_marks.txt <= 箇条書きに使うマークの一覧
│  create_index.py
│  ignore.txt       <= 無視する言葉の一覧
│  README.md
│  requirements.txt 
│
├─module
│  │  .gitignore
│  │  make_index.py
│  │  read_index.py
│  │  read_material.py
│  │  setup_material.py
│  │  test.py
│  └─  write_index.py
│
└─schedule
```

<div style="page-break-before:always"></div>

### 使用方法
1. ゼミの日にまとめられているフォルダをpdfフォルダに入れる
2. `create_index.py`を`create_index`直下で実行
   ```
   py create_index.py
   ```

<div style="page-break-before:always"></div>

## 工夫した点
1. この `README.md`を読み込んで、資料から読み出すタイトルを決定したこと。
2. 1つの巨大なファイルで完結するのではなくモジュール化して分解したこと。
3. マークダウンで見られない人や存在を知らない人にも見てもらえるようにpdfとして出力するようにしたこと。


<div style="page-break-before:always"></div>


下記の`<!-- title -!>`をタイトルとするページを資料内に作成して下さい．

## Rule
- 作成資料に必要な項目
  - 進捗報告 <!-- title -!>
  - 今後の予定 <!-- title -!>
  - 参考文献 <!-- title -!>
    - 論文
    - 学会誌
    - 参考にした技術ブログ
    - ショッピングサイト
    - 本
    - Githubのリンク
    - etc..
  - 作成物 <!-- title -!>
   - 共有サーバ内のリンク
    - 書いたコード
    - 何かのマニュアル


