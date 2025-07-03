from flask import Flask, render_template, request
import webbrowser
from threading import Timer
import re

from berechnungen import (
    berechne_reihenschaltung,
    berechne_parallelschaltung,
    berechne_schaltung_D,
    berechne_schaltung_E,
    berechne_schaltung_F
)

app = Flask(__name__)
PORT = 5001

def open_browser():
    webbrowser.open_new(f'http://127.0.0.1:{PORT}/')

@app.route('/', methods=['GET', 'POST'])
def index():
    form_values = {
        'ug': 24.0,
        'anzahl_r': 4,
        'schaltungstyp': 'reihe',
        'misch_typ': 'd',
        'widerstaende': [10.0, 20.0, 50.0, 100.0]
    }
    result = None

    if request.method == 'POST':
        try:
            ug = float(request.form['ug'])
            schaltungstyp = request.form['schaltungstyp']
            widerstaende = request.form.getlist('r[]', type=float)

            form_values = {
                'ug': ug,
                'anzahl_r': len(widerstaende),
                'schaltungstyp': schaltungstyp,
                'misch_typ': request.form.get('misch_typ', 'd'),
                'widerstaende': widerstaende
            }

            if schaltungstyp == 'reihe':
                result = berechne_reihenschaltung(ug, widerstaende)
            elif schaltungstyp == 'parallel':
                result = berechne_parallelschaltung(ug, widerstaende)
            elif schaltungstyp == 'misch':
                misch_typ = request.form.get('misch_typ')
                if misch_typ == 'd':
                    result = berechne_schaltung_D(ug, widerstaende)
                elif misch_typ == 'e':
                    result = berechne_schaltung_E(ug, widerstaende)
                elif misch_typ == 'f':
                    result = berechne_schaltung_F(ug, widerstaende)
                else:
                    raise ValueError("Unbekannter Mischschaltungstyp ausgewählt.")

        except (ValueError, ZeroDivisionError, IndexError) as e:
            result = {'error': f"Fehler bei der Berechnung: {e}. Bitte prüfen Sie Ihre Eingaben."}

    return render_template('index.html', result=result, form_values=form_values)

if __name__ == '__main__':
    Timer(1, open_browser).start()
    app.run(host='127.0.0.1', port=PORT)