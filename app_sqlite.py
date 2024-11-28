import sqlite3
from io import BytesIO
import base64
import matplotlib, matplotlib.pyplot as plt
matplotlib.use('Agg')
# import japanize_matplotlib  # 使えない場合はコメントアウトして下記を有効に
plt.rcParams['font.family'] = "Hiragino Sans"  # Macの場合
# plt.rcParams['font.family'] = "MS Gothic"  # Windowsの場合
# plt.rcParams['font.family'] = "IPAGothic"  # その他の場合
import pandas as pd
from flask import Flask,render_template,request,g

app = Flask(__name__)

@app.route('/')
def index():
    # indexページの表示
    return render_template('index.html')

@app.route('/graph')
def create_graph_sqlite():
    # データベースを開く
    con = sqlite3.connect('data.db')
    cur = con.cursor()

    # SQLでデータを読む
    sql = "SELECT date,temperature_sapporo,temperature_asahikawa FROM items ORDER BY id"

    # SQL実行
    rows = cur.execute(sql)
    data = rows.fetchall()

    # データベースを閉じる
    con.close()

    # SQL実行結果からデータフレームを作成
    df = pd.DataFrame(data, columns=['日付','札幌','旭川'])
    df['日付'] = pd.to_datetime(df['日付'])
    df = df.set_index('日付')

    # pandasのplotメソッドによるグラフ作成
    df.plot(title="日平均気温比較", kind="line", rot=0, grid=True, alpha=0.5)

    # グラフ画像をbase64にエンコード
    buf = BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    base64_img = base64.b64encode(buf.read()).decode()

    # おまけ：pandasのto_htmlメソッドによる表の作成
    table = df.to_html()

    return render_template('graph.html', image=base64_img, table=table)

if __name__ == '__main__':
    app.debug = True
    app.run(host='localhost')
