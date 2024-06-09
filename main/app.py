from flask import Flask, render_template, request, jsonify, redirect, url_for, session, render_template, flash
import requests
import logging


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
    

@app.route('/pasien_riwayat', methods=['GET'])
def get_pasien_riwayat():
    try:
        response = requests.get('http://127.0.0.1:5004/pasien_riwayat')
        response.raise_for_status()  # Raise an error for bad status codes
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching pasien data: {e}")
        return []


# Setup logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Fetch riwayat data and render the page
@app.route('/riwayat', methods=['GET'])
def riwayat_page():
    try:
        # Mendapatkan data riwayat dari backend (port 5004)
        response = requests.get('http://127.0.0.1:5004/riwayat', timeout=10)
        response.raise_for_status()  # Raise an error for bad status codes

        # Mengembalikan respons JSON dari backend ke middleware
        data = response.json()
        return render_template('riwayat.html', riwayat=data, active_page='riwayat_page')
    except requests.exceptions.ConnectionError:
        logger.error("Could not connect to riwayat service")
        return "Could not connect to riwayat service", 500
    except requests.exceptions.Timeout:
        logger.error("The request to riwayat service timed out")
        return "The request to riwayat service timed out", 500
    except requests.exceptions.HTTPError as e:
        # Menampilkan pesan kesalahan yang lebih spesifik
        logger.error(f"HTTP error occurred: {e}")
        return f"HTTP error occurred: {e}", 500
    except requests.exceptions.RequestException as e:
        # Menangani semua jenis kesalahan lainnya
        logger.error(f"An error occurred: {e}")
        return f"An error occurred: {e}", 500

# Add a new riwayat entry
@app.route('/tambah_riwayat', methods=['POST'])
def tambah_riwayat():
    try:
        response = requests.post('http://127.0.0.1:5004/tambah_riwayat', json=request.json, timeout=10)
        response.raise_for_status()  # Raise an error for bad status codes
        return jsonify({'message': 'Data riwayat berhasil ditambahkan'})
    except requests.exceptions.ConnectionError:
        logger.error("Could not connect to riwayat service")
        return "Could not connect to riwayat service", 500
    except requests.exceptions.Timeout:
        logger.error("The request to riwayat service timed out")
        return "The request to riwayat service timed out", 500
    except requests.exceptions.HTTPError as e:
        logger.error(f"HTTP error occurred: {e}")
        return f"HTTP error occurred: {e}", 500
    except requests.exceptions.RequestException as e:
        logger.error(f"An error occurred: {e}")
        return f"An error occurred: {e}", 500

# Edit an existing riwayat entry
@app.route('/editriwayat/<int:riwayat_id>', methods=['PUT'])
def edit_riwayat(riwayat_id):
    try:
        response = requests.put(f'http://127.0.0.1:5004/editriwayat/{riwayat_id}', json=request.json, timeout=10)
        response.raise_for_status()  # Raise an error for bad status codes
        return jsonify({'message': 'Data riwayat berhasil diperbarui'})
    except requests.exceptions.ConnectionError:
        logger.error("Could not connect to riwayat service")
        return "Could not connect to riwayat service", 500
    except requests.exceptions.Timeout:
        logger.error("The request to riwayat service timed out")
        return "The request to riwayat service timed out", 500
    except requests.exceptions.HTTPError as e:
        logger.error(f"HTTP error occurred: {e}")
        return f"HTTP error occurred: {e}", 500
    except requests.exceptions.RequestException as e:
        logger.error(f"An error occurred: {e}")
        return f"An error occurred: {e}", 500

# Fetch details of a specific riwayat entry
@app.route('/detailriwayat/<int:riwayat_id>', methods=['GET'])
def detailriwayat_middleware(riwayat_id):
    try:
        response = requests.get(f'http://127.0.0.1:5004/detailriwayat/{riwayat_id}', timeout=10)
        response.raise_for_status()  # Raise an error for bad status codes
        return jsonify(response.json())
    except requests.exceptions.ConnectionError:
        logger.error("Could not connect to riwayat service")
        return "Could not connect to riwayat service", 500
    except requests.exceptions.Timeout:
        logger.error("The request to riwayat service timed out")
        return "The request to riwayat service timed out", 500
    except requests.exceptions.HTTPError as e:
        logger.error(f"HTTP error occurred: {e}")
        return f"HTTP error occurred: {e}", 500
    except requests.exceptions.RequestException as e:
        logger.error(f"An error occurred: {e}")
        return f"An error occurred: {e}", 500

# Delete a riwayat entry
@app.route('/deleteriwayat/<int:riwayat_id>', methods=['DELETE'])
def delete_riwayat(riwayat_id):
    try:
        response = requests.delete(f'http://127.0.0.1:5004/deleteriwayat/{riwayat_id}', timeout=10)
        response.raise_for_status()  # Raise an error for bad status codes
        return jsonify({'message': 'Data riwayat berhasil dihapus'})
    except requests.exceptions.ConnectionError:
        logger.error("Could not connect to riwayat service")
        return "Could not connect to riwayat service", 500
    except requests.exceptions.Timeout:
        logger.error("The request to riwayat service timed out")
        return "The request to riwayat service timed out", 500
    except requests.exceptions.HTTPError as e:
        logger.error(f"HTTP error occurred: {e}")
        return f"HTTP error occurred: {e}", 500
    except requests.exceptions.RequestException as e:
        logger.error(f"An error occurred: {e}")
        return jsonify({'error': str(e)}), 500

# layanan janji
def get_janji():
    response = requests.get('http://127.0.0.1:5003/janji')
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

@app.route('/pasien')
def pasien_page():
    return render_template('pasien.html', active_page='pasien_page')


@app.route('/janji')
def janji_page():
    return render_template('janji.html', active_page='janji_page')


@app.route('/rawat_inap')
def rawat_inap_page():
    return render_template('rawat_inap.html', active_page='rawat_inap_page')

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
