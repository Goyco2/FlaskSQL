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


@app.route('/infoUser', methods=['GET'])
def home():
    return render_template('home.html')

@app.route('/result', methods=['GET', 'POST'])
def result():

    Nome = request.args['Nome']
    Cognome = request.args['Cognome']
    query = f"select * from sales.customers where first_name = '{Nome}' and last_name = '{Cognome}' "
    d = pd.read_sql(query, conn)
    if Nome not in d['first_name'] and Cognome not in d['last_name']:
        return render_template('result.html', nomiColonne = d.columns.values, dati = list(d.values.tolist()))
    else:
        return render_template('error.html')
        


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3245, debug=True)