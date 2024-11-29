# import sqlite3
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
def create_graph_csv():
    # pandasでcsvファイルを読み込む
    df = pd.read_csv('data.csv', encoding='utf8', header=0, index_col=0, parse_dates=True, usecols=['年月日','札幌平均気温(℃)','旭川平均気温(℃)'])

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
