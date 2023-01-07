## このリポジトリの目的
研究室で発生する事務処理を簡略化するためのコードを作っています。
基本的にはひとつの研究室で起こることや、自分がより情報をまとめやすくするために作ったコードあります。

## 開発言語・環境
- python 3.10.7
- vue3

### 作成物
1. create_summary
  - 班員の資料<sup>[1](#note1)</sup>から議事録を生成するためのコード
2. create_index
  - 過去の自分の資料<sup>[1](#note1)</sup>からインデックスを生成するコード


<small id="note1">1:対象としている資料はパワーポイントで作成後にpdfにエクスポートしたものである．</small>

### 使用方法

**create_summary**
```
usual_zemi > cd material/frontend
frontend > npm run build
frontend > cd ../create_summary/api
api > py app.py
```
