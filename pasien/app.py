from flask import Flask, jsonify, request, render_template
from flask_mysqldb import MySQL

app= Flask(__name__)

app.config['MYSQL_HOST'] = 'tubes-nabilamelsyana5-c7f0.a.aivencloud.com'
app.config['MYSQL_USER'] = 'avnadmin'
app.config['MYSQL_PASSWORD'] = 'AVNS_pr3FDArYqXJReBFPPXg'
app.config['MYSQL_DB'] = 'rumahsakit'
app.config['MYSQL_PORT'] = 26484

mysql = MySQL(app)

@app.route('/pasien', methods=['GET'])
def get_pasien():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM pasien")
    kolom = [i[0] for i in cursor.description]
    data = []
    for row in cursor.fetchall():
        data.append(dict(zip(kolom, row)))
    cursor.close()
    return jsonify(data)

@app.route('/tambah_pasien', methods=['POST'])
def tambah_pasien():
    nama = request.json['nama']
    tanggal_lahir = request.json['tanggal_lahir']
    alamat = request.json['alamat']
    tipe_darah = request.json['tipe_darah']

    cursor = mysql.connection.cursor()
    sql = "INSERT INTO pasien (nama, tanggal_lahir, alamat, tipe_darah) VALUES (%s,%s,%s,%s)"
    val = (nama, tanggal_lahir, alamat, tipe_darah)
    cursor.execute(sql, val)
    mysql.connection.commit()

    cursor.close()
    return jsonify({'message': 'data berhasil masuk'})

@app.route('/detailpasien/<int:pasien_id>', methods=['GET'])
def detailpasien(pasien_id):
    try:
        cursor = mysql.connection.cursor()
        sql = "SELECT * FROM pasien WHERE pasien_id = %s"
        cursor.execute(sql, (pasien_id,))
        result = cursor.fetchone()
        if result:
            pasien = {
                'pasien_id': result[0],
                'nama': result[1],
                'tanggal_lahir': result[2],
                'alamat': result[3],
                'tipe_darah': result[4]
            }
            cursor.close()
            return jsonify(pasien)
        else:
            cursor.close()
            return jsonify({'error': 'Pasien not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500



@app.route('/editpasien/<int:pasien_id>', methods=['PUT'])
def editpasien(pasien_id):
    data = request.get_json()
    if data:
        nama = data.get('nama')
        tanggal_lahir = data.get('tanggal_lahir')
        alamat = data.get('alamat')
        tipe_darah = data.get('tipe_darah')
        
        cursor = mysql.connection.cursor()
        sql = "UPDATE pasien SET nama = %s, tanggal_lahir = %s,  alamat = %s, tipe_darah = %s WHERE pasien_id = %s"
        val = (nama, tanggal_lahir, alamat, tipe_darah, pasien_id)
        cursor.execute(sql, val)
        mysql.connection.commit()
        cursor.close()  

        return jsonify({'message': 'Data pasien berhasil diperbarui'})
    else:
        return jsonify({'error': 'Data tidak ditemukan atau tidak lengkap'}), 400

@app.route('/deletepasien/<int:pasien_id>', methods=['DELETE'])
def deletepasien(pasien_id):
    cursor = mysql.connection.cursor()
    sql = "DELETE FROM pasien WHERE pasien_id = %s"
    val = (pasien_id,)
    cursor.execute(sql, val)
    mysql.connection.commit()
    cursor.close()

    return jsonify({'message': 'Data pasien berhasil dihapus'})

if __name__ == '__main__':
    app.run(host = '0.0.0.0', port = 5001, debug = True)