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
def home1():
    return render_template('home1.html')

@app.route('/result1', methods=['GET', 'POST'])
def result1():
    Nome = request.args['NomeS']
    query = f"select staffs.first_name, staffs.last_name, stores.store_name from sales.staffs inner join sales.stores on sales.staffs.store_id = sales.stores.store_id where stores.store_name = '{Nome}' "
    d = pd.read_sql(query, conn)
    if Nome not in d.store_name.tolist():
        return render_template('errore1.html')
    else:
        return render_template('result1.html', nomiColonne = d.columns.values, dati = list(d.values.tolist()))

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=3245, debug=True)