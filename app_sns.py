# import sqlite3
from io import BytesIO
import base64
import matplotlib, matplotlib.pyplot as plt
matplotlib.use('Agg')
import pandas as pd
import seaborn as sns
sns.set()
from flask import Flask,render_template,request,g

app = Flask(__name__)

@app.route('/')
def index():
    # indexページの表示
    return render_template('index.html')

@app.route('/graph')
def create_graph_sns():
    # 文字化け対策
    # import japanize_matplotlib  # 使えない場合はコメントアウトして下記を有効に
    plt.rcParams['font.family'] = "Hiragino Sans"  # Macの場合
    # plt.rcParams['font.family'] = "MS Gothic"  # Windowsの場合
    # plt.rcParams['font.family'] = "IPAGothic"  # その他の場合

    # pandasでcsvファイルを読み込む
    df = pd.read_csv('data.csv', encoding='utf8', header=0, index_col=0, parse_dates=True, usecols=['年月日','札幌平均気温(℃)','旭川平均気温(℃)'])

    # グラフ作成
    sns.regplot(data=df, ci=95, x="札幌平均気温(℃)", y="旭川平均気温(℃)", order=1)

    # グラフ画像をbase64にエンコード
    buf = BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    base64_img = base64.b64encode(buf.read()).decode()

    # おまけ：表を作成
    table = df.to_html()

    return render_template('graph.html', image=base64_img, table=table)

## sqliteからデータを読む場合は上記部分をコメントアウトし，かわりに下記を有効にする
# @app.route('/graph')
# def create_graph_sns():
#     # データベースを開く
#     con = sqlite3.connect('data.db')

#     # SQLでデータを読む
#     sql = "SELECT date,temperature_sapporo,temperature_asahikawa FROM items ORDER BY id"
 
#     # pandasからSQLを実行してデータフレームを作成
#     df = pd.read_sql(sql=sql, con=con, index_col='date', parse_dates='date')

#     # データベースを閉じる
#     con.close()

#     # グラフ作成
#     sns.regplot(data=df, ci=95, x="temperature_sapporo", y="temperature_asahikawa", order=1)

#     # グラフ画像をbase64にエンコード
#     buf = BytesIO()
#     plt.savefig(buf, format='png')
#     buf.seek(0)
#     base64_img = base64.b64encode(buf.read()).decode()

#     # おまけ：表を作成
#     table = df.to_html()

#     return render_template('graph.html', image=base64_img, table=table)

if __name__ == '__main__':
    app.debug = True
    app.run(host='localhost')
