from flask import Flask , request, render_template, jsonify, redirect, url_for
import requests

app = Flask(__name__)


@app.route('/dokter', methods=['GET'])
def dokter_page():
    try:
        response = requests.get('http://127.0.0.1:5002/dokter')
        dokter = response.json()
        return render_template('dokter.html', dokter=dokter, active_page='dokter_page')
    except requests.exceptions.ConnectionError:
        return "Could not connect to dokter service", 500

@app.route('/tambah_dokter', methods=['POST'])
def tambah_dokter():
    try:
        response = requests.post('http://127.0.0.1:5002/tambah_dokter', json=request.json)
        dokter = response.json()
        return render_template('dokter.html', dokter=dokter, active_page='dokter_page')
    except requests.exceptions.ConnectionError:
        return "Could not connect to dokter service", 500
    
@app.route('/editdokter/<int:dokter_id>', methods=['PUT'])
def edit_dokter(dokter_id):
    try:
        data = request.json
        response = requests.put(f'http://127.0.0.1:5002/editdokter/{dokter_id}', json=data)
        dokter = response.json()
        return render_template('dokter.html', dokter=dokter, active_page='dokter_page')
    except requests.exceptions.ConnectionError:
        return "Could not connect to dokter service", 500

@app.route('/detaildokter/<int:dokter_id>', methods=['GET'])
def detaildokter_middleware(dokter_id):
    try:
        response = requests.get(f'http://127.0.0.1:5002/detaildokter/{dokter_id}')
        dokter = response.json()
        return jsonify(dokter)
    except requests.exceptions.ConnectionError:
        return "Could not connect to dokter service", 500


@app.route('/deletedokter/<int:dokter_id>', methods=['DELETE'])
def delete_dokter(dokter_id):
    try:
        response = requests.delete(f'http://127.0.0.1:5002/deletedokter/{dokter_id}')
        if response.status_code == 200:
            return jsonify({'message': 'Data dokter berhasil dihapus'})
        else:
            return jsonify({'error': 'Gagal menghapus data'}), 500
    except requests.exceptions.RequestException as e:
        return jsonify({'error': str(e)}), 500




# layanan pasien
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

# layanan riwayat
def get_riwayat():
    response = requests.get('http://127.0.0.1:5004/riwayat')
    return response.json()

# layanan rawat_inap
def get_rawat_inap():
    response = requests.get('http://127.0.0.1:5005/rawat_inap')
    return response.json()

# layanan klinik
def get_klinik():
    response = requests.get('http://127.0.0.1:5006/klinik')
    return response.json()

# layanan obat
def get_obat():
    response = requests.get('http://127.0.0.1:5007/obat')
    return response.json()

# layanan alat medis
def get_alat_medis():
    response = requests.get('http://127.0.0.1:5008/alat_medis')
    return response.json()

@app.route('/')
def home():
    return render_template('home.html', active_page='home')



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

@app.route('/klinik')
def klinik_page():
    return render_template('klinik.html', active_page='klinik_page')

@app.route('/obat')
def obat_page():
    return render_template('obat.html', active_page='obat_page')

@app.route('/alat_medis')
def alat_medis_page():
    return render_template('alat_medis.html', active_page='alat_medis_page')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
