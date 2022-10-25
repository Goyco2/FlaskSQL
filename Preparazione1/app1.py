from flask import Flask,render_template,request,send_file,make_response, url_for, Response,redirect
app = Flask(__name__)
import io
import geopandas
import contextily
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd
import pandas as pd
import pymssql
import matplotlib.pyplot as plt
conn = pymssql.connect(server='213.140.22.237\SQLEXPRESS', user='goycochea.gabriel', password='xxx123##', database='goycochea.gabriel')


@app.route('/', methods=['GET'])
def home():
    return render_template('home.html')

@app.route('/selezione', methods=['GET'])
def selezione():
    scelta = request.args["scelta"]
    if scelta == "es1":
        return redirect(url_for("es1"))
    elif scelta == "es2":
        return redirect(url_for(""))
    elif scelta == "es3":
        return redirect(url_for(""))
    else:
        return redirect(url_for(""))

@app.route('/es1', methods=['GET'])
def es1():
    global df1
    query = 'select category_name, count(*) as prodotti_per_categoria from production.categories inner join production.products on production.categories.category_id = production.products.category_id group by category_name '
    df1 = pd.read_sql(query, conn)
    return render_template('es1.html', nomiColonne = df1.columns.values, dati = list(df1.values.tolist()))

@app.route('/grafico', methods=['GET'])
def grafico():

    fig = plt.figure(figsize=(10,10))
    ax = plt.axes()
    x = df1['category_name']
    y = df1['prodotti_per_categoria']
    fig.autofmt_xdate(rotation=45)

    ax.bar(x,y,color = "#304C89")

    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')
    


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3245, debug=True)