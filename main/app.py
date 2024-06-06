from flask import Flask , render_template
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
    return render_template('dokter.html')

@app.route('/janji')
def janji_page():
    return render_template('janji.html')

@app.route('/riwayat')
def riwayat_page():
    return render_template('riwayat.html')

@app.route('/rawat_inap')
def rawat_inap_page():
    return render_template('rawat_inap.html')

@app.route('/klinik')
def klinik_page():
    return render_template('klinik.html')

@app.route('/obat')
def obat_page():
    return render_template('obat.html')

@app.route('/alat_medis')
def alat_medis_page():
    return render_template('alat_medis.html')

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=5000) 