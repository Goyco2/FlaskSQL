from flask import Flask, render_template, request
app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return render_template('search.html')

@app.route('/result', methods=['GET'])
def result():
    # collegamento al database 
    import pandas as pd
    import pymssql
    import matplotlib.pyplot as plt
    conn = pymssql.connect(server='213.140.22.237\SQLEXPRESS', user='goycochea.gabriel', password='xxx123##', database='goycochea.gabriel')
    # Invio quesry al database e ricezione informazione
    NomeProdotto = request.args['NomeProdotto']
    query = f"select * from production.products where product_name LIKE '{NomeProdotto}%'"
    dfprodotti = pd.read_sql(query, conn)
    # visualizzare le informazioni 
    return render_template('result.html', nomiColonne = dfprodotti.columns.values, dati = list(dfprodotti.values.tolist()))
    
if __name__ == '__main__':
  app.run(host='0.0.0.0', port=3245, debug=True)