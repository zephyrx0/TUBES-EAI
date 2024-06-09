from flask import Flask, jsonify, request
from flask_mysqldb import MySQL
from datetime import datetime, timedelta
import json
from flask.json.provider import DefaultJSONProvider

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'tubes-nabilamelsyana5-c7f0.a.aivencloud.com'
app.config['MYSQL_USER'] = 'avnadmin'
app.config['MYSQL_PASSWORD'] = 'AVNS_pr3FDArYqXJReBFPPXg'
app.config['MYSQL_DB'] = 'rumahsakit'
app.config['MYSQL_PORT'] = 26484

mysql = MySQL(app)

class CustomJSONProvider(DefaultJSONProvider):
    def default(self, obj):
        if isinstance(obj, timedelta):
            return str(obj)
        return super().default(obj)

app.json = CustomJSONProvider(app)

@app.route('/rawat_inap', methods=['GET', 'POST'])
def rawat_inap():
    if request.method == 'GET':
        cursor = mysql.connection.cursor()
        query = """
        SELECT r.rawat_inap_id, r.pasien_id, p.nama AS nama_pasien, r.dokter_id, d.nama AS nama_dokter, r.tanggal_masuk, r.tanggal_keluar, r.ruangan
        FROM rawat_inap r
        JOIN pasien p ON r.pasien_id = p.pasien_id
        JOIN dokter d ON r.dokter_id = d.dokter_id
        """
        cursor.execute(query)
        kolom = [i[0] for i in cursor.description]
        data = [dict(zip(kolom, row)) for row in cursor.fetchall()]
        for item in data:
            tanggal_masuk_date = item['tanggal_masuk']
            item['tanggal_masuk'] = tanggal_masuk_date.strftime("%Y-%m-%d")

            tanggal_keluar_date = item['tanggal_keluar']
            item['tanggal_keluar'] = tanggal_keluar_date.strftime("%Y-%m-%d")
        cursor.close()
        return jsonify(data)
    
    elif request.method == 'POST':
        data = request.json
        pasien_id = data['pasien_id']
        dokter_id = data['dokter_id']
        tanggal_masuk = data['tanggal_masuk']
        tanggal_keluar = data['tanggal_keluar']
        ruangan = data['ruangan']
        
        cursor = mysql.connection.cursor()
        sql = "INSERT INTO rawat_inap (pasien_id, dokter_id, tanggal_masuk, tanggal_keluar, ruangan) VALUES (%s, %s, %s, %s, %s)"
        val = (pasien_id, dokter_id, tanggal_masuk, tanggal_keluar, ruangan)
        cursor.execute(sql, val)
        mysql.connection.commit()
        cursor.close()
        return jsonify({'message': 'Rawat inap berhasil dibuat'})

@app.route('/detailrawat_inap/<int:rawat_inap_id>', methods=['GET'])
def detailrawat_inap(rawat_inap_id):
    try:
        cursor = mysql.connection.cursor()
        sql = "SELECT * FROM rawat_inap WHERE rawat_inap_id = %s"
        cursor.execute(sql, (rawat_inap_id,))
        result = cursor.fetchone()
        if result:
            rawat_inap = {
                'rawat_inap_id': result[0],
                'pasien_id': result[1],
                'dokter_id': result[2],
                'tanggal_masuk': result[3].strftime("%Y-%m-%d") if isinstance(result[3], datetime) else str(result[3]),
                'tanggal_keluar': result[4].strftime("%Y-%m-%d") if isinstance(result[4], datetime) else str(result[4]),
                'ruangan': result[5]
            }
            cursor.close()
            return jsonify(rawat_inap)
        else:
            cursor.close()
            return jsonify({'error': 'rawat_inap not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/editrawat_inap/<int:rawat_inap_id>', methods=['PUT'])
def editrawat_inap(rawat_inap_id):
    data = request.get_json()
    if data:
        pasien_id = data.get('pasien_id')
        dokter_id = data.get('dokter_id')
        tanggal_masuk = data.get('tanggal_masuk')
        tanggal_keluar = data.get('tanggal_keluar')
        ruangan = data.get('ruangan')
        
        cursor = mysql.connection.cursor()
        sql = "UPDATE rawat_inap SET pasien_id = %s, dokter_id = %s, tanggal_masuk = %s, tanggal_keluar = %s, ruangan = %s WHERE rawat_inap_id = %s"
        val = (pasien_id, dokter_id, tanggal_masuk, tanggal_keluar, ruangan, rawat_inap_id)
        cursor.execute(sql, val)
        mysql.connection.commit()
        cursor.close()  

        return jsonify({'message': 'Data rawat_inap berhasil diperbarui'})
    else:
        return jsonify({'error': 'Data tidak ditemukan atau tidak lengkap'}), 400

@app.route('/deleterawat_inap/<int:rawat_inap_id>', methods=['DELETE'])
def deleterawat_inap(rawat_inap_id):
    cursor = mysql.connection.cursor()
    sql = "DELETE FROM rawat_inap WHERE rawat_inap_id = %s"
    val = (rawat_inap_id,)
    cursor.execute(sql, val)
    mysql.connection.commit()
    cursor.close()

    return jsonify({'message': 'Data rawat_inap berhasil dihapus'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5005, debug=True)
