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
        return redirect(url_for("es2"))
    elif scelta == "es3":
        return redirect(url_for("es3"))
    else:
        return redirect(url_for("es4"))

@app.route('/es1', methods=['GET'])
def es1():
    global df1
    query = 'select category_name, count(*) as prodotti_per_categoria from production.categories inner join production.products on production.categories.category_id = production.products.category_id group by category_name '
    df1 = pd.read_sql(query, conn)
    return render_template('es1.html', nomiColonne = df1.columns.values, dati = list(df1.values.tolist()))

@app.route('/grafico', methods=['GET'])
def grafico():

    fig = plt.figure(figsize=(7,10))
    ax = plt.axes()
    x = df1['category_name']
    y = df1['prodotti_per_categoria']
    fig.autofmt_xdate(rotation=45)

    ax.bar(x,y,color = "#304C89")

    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')
    
@app.route('/es2', methods=['GET'])
def es2():
    global df2
    query ='select store_name, count(*)as ordini_per_store from sales.orders inner join sales.stores on sales.orders.store_id = sales.stores.store_id group by store_name'
    df2 = pd.read_sql(query, conn)
    return render_template('es2.html', nomiColonne = df2.columns.values, dati = list(df2.values.tolist()))

@app.route('/grafico2', methods=['GET'])
def grafico2():


    fig = plt.figure(figsize=(7,10))
    ax = plt.axes()
    x = df2['store_name']
    y = df2['ordini_per_store']

    ax.barh(x,y)

    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

@app.route('/es3', methods=['GET'])
def es3():
    global df3
    query ='select brand_name, count(*)as brand_per_prodotto from production.brands inner join production.products on production.products.brand_id = production.brands.brand_id group by brand_name'
    df3 = pd.read_sql(query, conn)
    return render_template('es3.html', nomiColonne = df3.columns.values, dati = list(df3.values.tolist()))

@app.route('/grafico3', methods=['GET'])
def grafico3():


    names = list(df3['brand_name'])
    values =df3['brand_per_prodotto']
    fig = plt.figure(figsize=[10,10])
    fig.suptitle('grafico a torta', color = 'r', fontsize= 40)

    ax = plt.axes()
    ax.pie(values, labels=names, autopct='%1.1f%%')

    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

@app.route('/es4', methods=['GET'])
def es4():
        return render_template('es4.html')


@app.route('/result4', methods=['GET'])
def result4():
    NomeProdotto = request.args['NomeProdotto']
    query = f"select * from production.products where product_name LIKE '{NomeProdotto}%'"
    dfprodotti = pd.read_sql(query, conn)
    # visualizzare le informazioni 
    return render_template('result4.html', nomiColonne = dfprodotti.columns.values, dati = list(dfprodotti.values.tolist()))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3245, debug=True)