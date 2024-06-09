from flask import Flask, render_template, request, jsonify, redirect, url_for, session, render_template, flash
import requests


app = Flask(__name__)
app.secret_key = 'cobain'  # Pastikan untuk mengatur kunci rahasia sesi

# Fungsi bantuan untuk membuat respons JSON
def create_response(data, status_code, message):
    response = {
        'data': data,
        'status': status_code,
        'message': message
    }
    return jsonify(response)

# Login route
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        data = {
            'email': email,
            'password': password
        }
        try:
            response = requests.post('http://127.0.0.1:4999/', data=data)
            if response.status_code == 200:
                session['email'] = email
                return redirect(url_for('home'))  # Mengarahkan ke halaman home setelah login
            else:
                flash("Invalid email or password")  # Menampilkan pesan flash jika login gagal
                return render_template('login.html')
        except requests.exceptions.ConnectionError:
            return "Could not connect to login service", 500
    else:
        return render_template('login.html')

# Dashboard route
@app.route('/home')
def home():
    if 'email' not in session:
        return redirect(url_for('login'))  # Mengarahkan pengguna yang belum masuk ke halaman login
    return render_template('home.html')

# Logout route
@app.route('/logout')
def logout():
    try:
        response = requests.post('http://127.0.0.1:4999/logout', data={})
        if response.status_code == 200:
            session.pop('email', None)
            return redirect(url_for('login'))  # Mengarahkan pengguna ke halaman login setelah logout
        else:
            return "Logout failed", 400
    except requests.exceptions.ConnectionError:
        return "Could not connect to logout service", 500



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
@app.route('/pasien')
def pasien_page():
    try:
        response = requests.get('http://127.0.0.1:5001/pasien')
        pasien = response.json()
        return render_template('pasien.html', pasien=pasien, active_page='pasien_page')
    except requests.exceptions.ConnectionError:
        return "Could not connect to pasien service", 500

@app.route('/tambah_pasien', methods=['POST'])
def tambah_pasien():
    try:
        response = requests.post('http://127.0.0.1:5001/tambah_pasien', json=request.json)
        pasien = response.json()
        return render_template('pasien.html', pasien=pasien, active_page='pasien_page')
    except requests.exceptions.ConnectionError:
        return "Could not connect to pasien service", 500
    
@app.route('/editpasien/<int:pasien_id>', methods=['PUT'])
def edit_pasien(pasien_id):
    try:
        data = request.json
        response = requests.put(f'http://127.0.0.1:5001/editpasien/{pasien_id}', json=data)
        pasien = response.json()
        return render_template('pasien.html', pasien=pasien, active_page='pasien_page')
    except requests.exceptions.ConnectionError:
        return "Could not connect to pasien service", 500

@app.route('/detailpasien/<int:pasien_id>', methods=['GET'])
def detailpasien_middleware(pasien_id):
    try:
        response = requests.get(f'http://127.0.0.1:5001/detailpasien/{pasien_id}')
        pasien = response.json()
        return jsonify(pasien)
    except requests.exceptions.ConnectionError:
        return "Could not connect to pasien service", 500


@app.route('/deletepasien/<int:pasien_id>', methods=['DELETE'])
def delete_pasien(pasien_id):
    try:
        response = requests.delete(f'http://127.0.0.1:5001/deletepasien/{pasien_id}')
        if response.status_code == 200:
            return jsonify({'message': 'Data pasien berhasil dihapus'})
        else:
            return jsonify({'error': 'Gagal menghapus data'}), 500
    except requests.exceptions.RequestException as e:
        return jsonify({'error': str(e)}), 500

# layanan janji
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
@app.route('/obat')
def obat_page():
    try:
        response = requests.get('http://127.0.0.1:5007/obat')
        obat = response.json()
        return render_template('obat.html', obat=obat, active_page='obat_page')
    except requests.exceptions.ConnectionError:
        return "Could not connect to obat service", 500

@app.route('/tambahobat', methods=['POST'])
def tambah_obat():
    try:
        response = requests.post('http://127.0.0.1:5007/tambahobat', json=request.json)
        obat = response.json()
        return render_template('obat.html', obat=obat, active_page='obat_page')
    except requests.exceptions.ConnectionError:
        return "Could not connect to obat service", 500
    
@app.route('/editobat/<int:obat_id>', methods=['PUT'])
def edit_obat(obat_id):
    try:
        data = request.json
        response = requests.put(f'http://127.0.0.1:5007/editobat/{obat_id}', json=data)
        obat = response.json()
        return render_template('obat.html', obat=obat, active_page='obat_page')
    except requests.exceptions.ConnectionError:
        return "Could not connect to obat service", 500

@app.route('/detailobat/<int:obat_id>', methods=['GET'])
def detailobat_middleware(obat_id):
    try:
        response = requests.get(f'http://127.0.0.1:5007/detailobat/{obat_id}')
        obat = response.json()
        return jsonify(obat)
    except requests.exceptions.ConnectionError:
        return "Could not connect to obat service", 500


@app.route('/deleteobat/<int:obat_id>', methods=['DELETE'])
def delete_obat(obat_id):
    try:
        response = requests.delete(f'http://127.0.0.1:5007/deleteobat/{obat_id}')
        if response.status_code == 200:
            return jsonify({'message': 'Data obat berhasil dihapus'})
        else:
            return jsonify({'error': 'Gagal menghapus data'}), 500
    except requests.exceptions.RequestException as e:
        return jsonify({'error': str(e)}), 500

# layanan alat medis
def get_alat_medis():
    response = requests.get('http://127.0.0.1:5008/alat_medis')
    return response.json()




@app.route('/janji')
def janji_page():
    return render_template('janji.html', active_page='janji_page')

@app.route('/riwayat')
def riwayat_page():
    return render_template('riwayat.html', active_page='riwayat_page')

@app.route('/rawat_inap')
def rawat_inap_page():
    return render_template('rawat_inap.html', active_page='rawat_inap_page')

@app.route('/klinik')
def klinik_page():
    return render_template('klinik.html', active_page='klinik_page')

@app.route('/alat_medis')
def alat_medis_page():
    return render_template('alat_medis.html', active_page='alat_medis_page')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)