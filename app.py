from flask import Flask, render_template, request, jsonify
import numpy_financial as npf

app = Flask(__name__)

def calcul_amortizare(dobanda_anuala, numar_rate, suma_imprumutata):
    rata_anuala = dobanda_anuala / 100
    rata_lunara = -npf.pmt(rata_anuala / 12, numar_rate, suma_imprumutata)
    
    sold_ramas = suma_imprumutata
    amortizare = []

    for luna in range(1, numar_rate + 1):
        dobanda_lunara = sold_ramas * (rata_anuala / 12)
        principal_lunar = rata_lunara - dobanda_lunara
        sold_ramas -= principal_lunar

        amortizare.append([luna, round(rata_lunara, 2), round(dobanda_lunara, 2), round(principal_lunar, 2), round(sold_ramas, 2)])

    return amortizare

@app.route('/', methods=['GET', 'POST'])
def index():
    rezultat = None

    if request.method == 'POST':
        suma_imprumutata = float(request.form['suma_imprumutata'])
        dobanda_anuala = float(request.form['dobanda_anuala'])
        numar_rate = int(request.form['numar_rate'])

        amortizare = calcul_amortizare(dobanda_anuala, numar_rate, suma_imprumutata)
        rezultat = {'amortizare': amortizare}

    return render_template('index.html', rezultat=rezultat)

if __name__ == '__main__':
    app.run(debug=True)
