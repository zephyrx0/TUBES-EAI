from flask import Flask , render_template, redirect, url_for, request
import requests


app = Flask(__name__)

#layanan pasien

def get_pasien():
    response = requests.get('http://127.0.0.1:5001/pasien')
    return response.json()

#layanan dokter

def get_dokter():
    response = requests.get('http://127.0.0.1:5002/dokter')
    return response.json()

#layanan janji

def get_janji():
    response = requests.get('http://127.0.0.1:5003/janji')
    return response.json()

#layanan riwayat

def get_riwayat():
    response = requests.get('http://127.0.0.1:5004/riwayat')
    return response.json()

#layanan rawat_inap

def get_rawat_inap():
    response = requests.get('http://127.0.0.1:5005/rawat_inap')
    return response.json()

#layanan klinik

def get_klinik():
    response = requests.get('http://127.0.0.1:5006/klinik')
    return response.json()

#layanan obat

def get_obat():
    response = requests.get('http://127.0.0.1:5007/obat')
    return response.json()

#layanan alat medis

def get_alat_medis():
    response = requests.get('http://127.0.0.1:5008/alat_medis')
    return response.json()


@app.route('/')
def home():
    return render_template('base.html')

@app.route('/pasien')
def pasien_page():
    return render_template('pasien.html')

@app.route('/dokter')
def dokter_page():
    dokters = get_dokter()
    return render_template('dokter.html', dokters=dokters)

@app.route('/delete_dokter/<int:dokter_id>')
def delete_dokter(dokter_id):
    response = requests.delete(f'http://localhost:5002/delete_dokter/{dokter_id}')
    return redirect(url_for('dokter_page'))

@app.route('/janji')
def janji_page():
    return render_template('janji.html')

@app.route('/riwayat')
def riwayat_page():
    return render_template('riwayat.html')

@app.route('/rawat_inap')
def rawat_inap_page():
    return render_template('rawat_inap.html')

def get_klinik():
    response = requests.get('http://127.0.0.1:5006/klinik')
    return response.json()

def get_klinik_id(klinik_id):
    response = requests.get('http://127.0.0.1:5006/api/klinik/{klinik_id}')
    return response.json()

@app.route('/klinik')
def klinik_page():
    klinik = get_klinik()
    return render_template('klinik.html', klinik=klinik)

@app.route('/addklinik')
def tambah_klinik():
    return render_template('tambah_klinik.html')

@app.route('/add_klinik', methods=['POST'])
def add_klinik():
    data = request.form
    response = requests.post('http://127.0.0.1:5006/klinik', json=data)
    return redirect(url_for('klinik_page'))

#form edit
@app.route('/editklinik/<int:klinik_id>')
def edit_klinik(klinik_id):
    klinikk = get_klinik_id(klinik_id)
    return render_template('edit_klinik.html', klinik_id=klinik_id, klinikk=klinikk)

@app.route('/update_klinik/<int:klinik_id>', methods=['GET', 'POST'])
def update_klinik(klinik_id):
    if request.method == 'GET':
        response = requests.get(f'http://127.0.0.1:5006/klinik/{klinik_id}')
        klinik = response.json()
        return render_template('edit_klinik.html', klinik=klinik)
    elif request.method == 'POST':
        data = request.form
        response = requests.put(f'http://127.0.0.1:5006/klinik/{klinik_id}', json=data)
        return redirect(url_for('klinik_page'))

@app.route('/delete_klinik/<int:klinik_id>')
def delete_klinik(klinik_id):
    response = requests.delete(f'http://localhost:5006/delete_klinik/{klinik_id}')
    return redirect(url_for('klinik_page'))

@app.route('/obat')
def obat_page():
    return render_template('obat.html')

@app.route('/alat_medis')
def alat_medis_page():
    medis = get_alat_medis()
    return render_template('alat_medis.html',medis=medis)
    
    

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=5000) 