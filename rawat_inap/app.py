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
        cursor.execute("SELECT * FROM rawat_inap")
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

@app.route('/editrawat_inap', methods=['PUT'])
def editrawat_inap():
    if 'rawat_inap_id' in request.args:
        rawat_inap_id = request.args['rawat_inap_id']
        data = request.get_json()
        cursor = mysql.connection.cursor()
        sql = "UPDATE rawat_inap SET pasien_id = %s, dokter_id = %s, tanggal_masuk = %s, tanggal_keluar = %s, ruangan = %s WHERE rawat_inap_id = %s"
        val = (data['pasien_id'], data['dokter_id'], data['tanggal_masuk'], data['tanggal_keluar'], data['ruangan'], rawat_inap_id)
        cursor.execute(sql, val)
        mysql.connection.commit()
        cursor.close()
        return jsonify({'message': 'Rawat inap berhasil diubah'})
    return jsonify({'error': 'rawat_inap_id is required'}), 400

@app.route('/deleterawat_inap', methods=['DELETE'])
def deleterawat_inap():
    if 'rawat_inap_id' in request.args:
        rawat_inap_id = request.args['rawat_inap_id']
        cursor = mysql.connection.cursor()
        sql = "DELETE FROM rawat_inap WHERE rawat_inap_id = %s"
        cursor.execute(sql, (rawat_inap_id,))
        mysql.connection.commit()
        cursor.close()
        return jsonify({'message': 'Rawat inap berhasil dihapus'})
    return jsonify({'error': 'rawat_inap_id is required'}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5005, debug=True)
