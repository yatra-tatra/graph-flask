# FlaskでPandasを使ってグラフを描く
## 概要

- Flaskによるwebアプリ上で，matplotlib + pandas ( + seaborn ) を使ったグラフを描く実験
- 特にpandasのplotメソッドから作成したグラフを表示する方法に関する情報が見つからなかった（需要が無いのかな）ので，とりあえず実験してみた
  - `app_csv.py`：csvファイル（data.csv）からpandasを使ってグラフを描く
  - `app_sqlite.py`：sqliteデータベースファイル（data.db）からpandasを使ってグラフを描く
  - `app_sns.py`：csvファイル（またはsqliteデータベースファイル）から，seabornを使ってグラフを描く

## 使用法

1. ビルトインwebサーバの起動：`python3 app_csv.py`（Linux, Mac），`py app_csv.py`（Windows）
2. ブラウザからアクセス：`http://localhost:5000/`
3. 最初に開かれるページで「作成！」ボタンを押すとcsvファイル（data.csv）から作成されたグラフを表示するページが開かれる
4. サーバ停止で終了：`Ctrl-C`
5. `app_sqlite.py`や`app_sns.py`についても，同様にグラフ作成が実験できる
6. 以上
