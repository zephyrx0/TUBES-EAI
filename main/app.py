from flask import Flask , request, render_template, jsonify, redirect, url_for
import requests

app = Flask(__name__)

#layanan pasien

def get_pasien():
    response = requests.get('http://127.0.0.1:5001/pasien')
    return response.json()

def get_pasien_by_id(pasien_id):
    response = requests.get(f'http://127.0.0.1:5001/detailpasien?pasien_id={pasien_id}')
    return response.json()

@app.route('/pasien')
def pasien_page():
    pasien = get_pasien()
    return render_template('pasien.html', pasien=pasien)

@app.route('/detailpasien/<int:pasien_id>', methods=['GET'])
def detail_pasien_page(pasien_id):
    pasien = get_pasien_by_id(pasien_id)
    if pasien:
        return render_template('detail_pasien.html', pasien=pasien)
    else:
        return "Data pasien tidak ditemukan", 404

@app.route('/pasien/add', methods=['GET', 'POST'])
def add_pasien_form():
    if request.method == 'POST':
        new_pasien = request.form.to_dict()
        response = requests.post('http://127.0.0.1:5001/pasien', json=new_pasien)
        return redirect(url_for('pasien_page'))
    return render_template('add_pasien.html')

@app.route('/pasien/edit/<int:pasien_id>', methods=['GET','POST'])
def update_pasien(pasien_id):
    pasien = get_pasien_by_id(pasien_id)
    if request.method == 'POST':
        updated_pasien = request.form.to_dict()
        response = requests.put(f'http://127.0.0.1:5001/editpasien/{pasien_id}', json=updated_pasien)
        return redirect(url_for('pasien_page'))
    return render_template('edit_pasien.html', pasien=pasien)

@app.route('/pasien/<int:pasien_id>', methods=['DELETE'])
def delete_pasien(pasien_id):
    if request.method == 'DELETE':
        response = requests.delete(f'http://127.0.0.1:5001/pasien/{pasien_id}')
        return jsonify(response.json())

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


@app.route('/')
def home():
    return render_template('base.html')



@app.route('/dokter')
def dokter_page():
    dokter = get_dokter()
    return render_template('dokter.html', dokter=dokter)

@app.route('/janji')
def janji_page():
    pasien = {p['pasien_id']: p['nama'] for p in get_pasien()}
    dokter = {d['dokter_id']: d['nama'] for d in get_dokter()}
    janji = get_janji()

    # Enrich janji data with patient and doctor names
    for j in janji:
        j['nama_pasien'] = pasien.get(j['pasien_id'], 'Unknown')
        j['nama_dokter'] = dokter.get(j['dokter_id'], 'Unknown')
    return render_template('janji.html', janji=janji, pasien=pasien, dokter=dokter)

@app.route('/riwayat')
def riwayat_page():
    pasien = {p['pasien_id']: p['nama'] for p in get_pasien()}
    riwayat = get_riwayat()

    for r in riwayat:
        r['nama_pasien'] = pasien.get(r['pasien_id'], 'Unknown')
    return render_template('riwayat.html', riwayat=riwayat)

@app.route('/rawat_inap')
def rawat_inap_page():
    pasien = {p['pasien_id']: p['nama'] for p in get_pasien()}
    dokter = {d['dokter_id']: d['nama'] for d in get_dokter()}
    rawat_inap = get_rawat_inap()

    # Enrich janji data with patient and doctor names
    for r in rawat_inap:
        r['nama_pasien'] = pasien.get(r['pasien_id'], 'Unknown')
        r['nama_dokter'] = dokter.get(r['dokter_id'], 'Unknown')
    return render_template('rawat_inap.html', rawat_inap=rawat_inap)

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=5000) 