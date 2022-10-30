## How to create summary

### Set up
`create_summary`を自分のPCにコピーしてください．\
`create_summary`下で以下のコマンドを実行してください．
```
pip install -r requirements.txt
```

### Folder structure
一例を示すために,10/13のまとめと出力したテキストファイルがあります．
```
│  year_month_day.txt <= 最低限のテンプレート
│  2022_schedule.csv  <= 今年度のスケジュール(全班分)
│  bullet_marks.txt   <= 箇条書きのマーク
│  ignore.txt         <= pdfの中の無視する文字列
│  create_summary.py         <= 特定の研究班の議事録を自動生成する
│  create_summary_general.py <= 汎用性の高いコード
│ 
├─pdf
│  └─test_pdf.py <= pdfを取得して確認するための補助コード
│          
├─member <= 研究室のメンバー
│      
│      
└─out <= 議事録出力用フォルダ
```

<div style="page-break-before:always"></div>

### Use
1. ゼミの日にまとめられているフォルダをpdfフォルダに入れる
2. `create_summary.py`を`create_summary`直下で実行
   ```
   py create_summary.py
   ```


## Caution
* 10/13のフォルダのまとめを作る場合は10/20までに実行する必要があります．
* 10/20以降outにある過去のファイルはpdfのその日のところにまとめられます．
  * 複数の議事録が乱立して，ichiにコピーするときに編集後のファイルを上書きしないため
* 編集後はファイル名の中にある自分の名前を消してからアップロードしてください
  * 編集後のなのか編集前なのか分からなくなります．
* ローカルで編集してからアップロードするとき
  1. 編集する
  2. 自分の名前をファイル名から消す
  3. ichiにあるその日の自分の名前が書いてあるファイルを消す
     * 該当する日以外の自分の名前の書いてあるファイルを消さないでください． 
  4. ichiにアップロードする

## Member database
`year_member.xlsx`の構造

|学年|氏|名|セイ|メイ|氏名|セイメイ|学籍番号|メアド|研究室|大臣|研究班|
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|


<div style="page-break-before:always"></div>

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

上記の項目をタイトルとするページを作成して下さい．