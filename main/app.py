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


#layanan dokter
def get_dokter():
    response = requests.get('http://127.0.0.1:5002/dokter')
    return response.json()

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
@app.route('/janji', methods=['GET'])
def janji_page():
    try:
        pasien = get_pasien()
        dokter = get_dokter()
        response = requests.get('http://127.0.0.1:5003/janji')
        janji = response.json()
        return render_template('janji.html', janji=janji,  pasien=pasien, dokter=dokter, active_page='janji_page')
    except requests.exceptions.ConnectionError:
        return "Could not connect to janji service", 500

@app.route('/tambah_janji', methods=['POST'])
def tambah_janji():
    try:
        response = requests.post('http://127.0.0.1:5003/janji', json=request.json)
        janji = response.json()
        return render_template('janji.html', janji=janji, active_page='janji_page')
    except requests.exceptions.ConnectionError:
        return "Could not connect to janji service", 500
    
@app.route('/editjanji/<int:janji_id>', methods=['PUT'])
def edit_janji(janji_id):
    try:
        data = request.json
        response = requests.put(f'http://127.0.0.1:5003/editjanji/{janji_id}', json=data)
        
        # Check if response status code is OK
        if response.status_code == 200:
            janji = response.json()
            return render_template('janji.html', janji=janji, active_page='janji_page')
        else:
            return f"Error: {response.status_code} - {response.text}", response.status_code

    except requests.exceptions.ConnectionError:
        return "Could not connect to janji service", 500
    except Exception as e:
        return str(e), 500

@app.route('/detailjanji/<int:janji_id>', methods=['GET'])
def detailjanji_middleware(janji_id):
    try:
        response = requests.get(f'http://127.0.0.1:5003/detailjanji/{janji_id}')
        response.raise_for_status()  # Raise an error for bad status codes
        janji = response.json()
        return jsonify(janji)
    except requests.exceptions.ConnectionError:
        return "Could not connect to janji service", 500
    except requests.exceptions.JSONDecodeError:
        return "Invalid JSON format in response from janji service", 500
    except Exception as e:
        return str(e), 500



@app.route('/deletejanji/<int:janji_id>', methods=['DELETE'])
def delete_janji(janji_id):
    try:
        response = requests.delete(f'http://127.0.0.1:5003/deletejanji/{janji_id}')
        if response.status_code == 200:
            return jsonify({'message': 'Data janji berhasil dihapus'})
        else:
            return jsonify({'error': 'Gagal menghapus data'}), 500
    except requests.exceptions.RequestException as e:
        return jsonify({'error': str(e)}), 500


# layanan rawat_inap
@app.route('/rawat_inap', methods=['GET'])
def rawat_inap_page():
    try:
        pasien = get_pasien()
        dokter = get_dokter()
        response = requests.get('http://127.0.0.1:5005/rawat_inap')
        rawat_inap = response.json()
        return render_template('rawat_inap.html', rawat_inap=rawat_inap,  pasien=pasien, dokter=dokter, active_page='rawat_inap_page')
    except requests.exceptions.ConnectionError:
        return "Could not connect to rawat_inap service", 500

@app.route('/tambah_rawat_inap', methods=['POST'])
def tambah_rawat_inap():
    try:
        response = requests.post('http://127.0.0.1:5005/rawat_inap', json=request.json)
        rawat_inap = response.json()
        return render_template('rawat_inap.html', rawat_inap=rawat_inap, active_page='rawat_inap_page')
    except requests.exceptions.ConnectionError:
        return "Could not connect to rawat_inap service", 500
    
@app.route('/editrawat_inap/<int:rawat_inap_id>', methods=['PUT'])
def edit_rawat_inap(rawat_inap_id):
    try:
        data = request.json
        response = requests.put(f'http://127.0.0.1:5005/editrawat_inap/{rawat_inap_id}', json=data)
        
        # Check if response status code is OK
        if response.status_code == 200:
            rawat_inap = response.json()
            return render_template('rawat_inap.html', rawat_inap=rawat_inap, active_page='rawat_inap_page')
        else:
            return f"Error: {response.status_code} - {response.text}", response.status_code

    except requests.exceptions.ConnectionError:
        return "Could not connect to rawat_inap service", 500
    except Exception as e:
        return str(e), 500

@app.route('/detailrawat_inap/<int:rawat_inap_id>', methods=['GET'])
def detailrawat_inap_middleware(rawat_inap_id):
    try:
        response = requests.get(f'http://127.0.0.1:5005/detailrawat_inap/{rawat_inap_id}')
        response.raise_for_status()  # Raise an error for bad status codes
        rawat_inap = response.json()
        return jsonify(rawat_inap)
    except requests.exceptions.ConnectionError:
        return "Could not connect to rawat_inap service", 500
    except requests.exceptions.JSONDecodeError:
        return "Invalid JSON format in response from rawat_inap service", 500
    except Exception as e:
        return str(e), 500



@app.route('/deleterawat_inap/<int:rawat_inap_id>', methods=['DELETE'])
def delete_rawat_inap(rawat_inap_id):
    try:
        response = requests.delete(f'http://127.0.0.1:5005/deleterawat_inap/{rawat_inap_id}')
        if response.status_code == 200:
            return jsonify({'message': 'Data rawat_inap berhasil dihapus'})
        else:
            return jsonify({'error': 'Gagal menghapus data'}), 500
    except requests.exceptions.RequestException as e:
        return jsonify({'error': str(e)}), 500

# layanan klinik

@app.route('/klinik')
def klinik_page():
    try:
        response = requests.get('http://127.0.0.1:5006/klinik')
        klinik = response.json()
        return render_template('klinik.html', klinik=klinik, active_page='klinik_page')
    except requests.exceptions.ConnectionError:
        return "Could not connect to klinik service", 500

@app.route('/tambahklinik', methods=['POST'])
def tambah_klinik():
    try:
        response = requests.post('http://127.0.0.1:5006/tambahklinik', json=request.json)
        klinik = response.json()
        return render_template('klinik.html', klinik=klinik, active_page='klinik_page')
    except requests.exceptions.ConnectionError:
        return "Could not connect to klinik service", 500
    
@app.route('/editklinik/<int:klinik_id>', methods=['PUT'])
def edit_klinik(klinik_id):
    try:
        data = request.json
        response = requests.put(f'http://127.0.0.1:5006/editklinik/{klinik_id}', json=data)
        klinik = response.json()
        return render_template('klinik.html',klinik=klinik, active_page='klinik_page')
    except requests.exceptions.ConnectionError:
        return "Could not connect to obat service", 500

@app.route('/detailklinik/<int:klinik_id>', methods=['GET'])
def detailklinik_middleware(klinik_id):
    try:
        response = requests.get(f'http://127.0.0.1:5006/detailklinik/{klinik_id}')
        klinik = response.json()
        return jsonify(klinik)
    except requests.exceptions.ConnectionError:
        return "Could not connect to klinik service", 500
    
@app.route('/deleteklinik/<int:klinik_id>', methods=['DELETE'])
def delete_klinik(klinik_id):
    try:
        response = requests.delete(f'http://127.0.0.1:5006/deleteklinik/{klinik_id}')
        if response.status_code == 200:
            return jsonify({'message': 'Data klinik berhasil dihapus'})
        else:
            return jsonify({'error': 'Gagal menghapus data'}), 500
    except requests.exceptions.RequestException as e:
        return jsonify({'error': str(e)}), 500
    

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
@app.route('/alat')
def alat_page():
    try:
        response = requests.get('http://127.0.0.1:5008/alat')
        alat = response.json()
        return render_template('alat.html', alat=alat, active_page='alat_page')
    except requests.exceptions.ConnectionError:
        return "Could not connect to alat medis service", 500

@app.route('/tambahalat', methods=['POST'])
def tambah_alat():
    try:
        response = requests.post('http://127.0.0.1:5008/tambahalat', json=request.json)
        alat = response.json()
        return render_template('alat.html', alat=alat, active_page='alat_page')
    except requests.exceptions.ConnectionError:
        return "Could not connect to alat medis service", 500
    
@app.route('/editalat/<int:alat_id>', methods=['PUT'])
def edit_alat(alat_id):
    try:
        data = request.json
        response = requests.put(f'http://127.0.0.1:5008/editalat/{alat_id}', json=data)
        alat = response.json()
        return render_template('alat.html', alat=alat, active_page='alat_page')
    except requests.exceptions.ConnectionError:
        return "Could not connect to obat service", 500

@app.route('/detailalat/<int:alat_id>', methods=['GET'])
def detailalat_middleware(alat_id):
    try:
        response = requests.get(f'http://127.0.0.1:5008/detailalat/{alat_id}')
        alat = response.json()
        return jsonify(alat)
    except requests.exceptions.ConnectionError:
        return "Could not connect to alat service", 500


@app.route('/deletealat/<int:alat_id>', methods=['DELETE'])
def delete_alat(alat_id):
    try:
        response = requests.delete(f'http://127.0.0.1:5008/deletealat/{alat_id}')
        if response.status_code == 200:
            return jsonify({'message': 'Data alat medis berhasil dihapus'})
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


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)