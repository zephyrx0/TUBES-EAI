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

@app.route('/riwayat', methods=['GET', 'POST'])
def riwayat():
    if request.method == 'GET':
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM riwayat")
        kolom = [i[0] for i in cursor.description]
        data = [dict(zip(kolom, row)) for row in cursor.fetchall()]
        cursor.close()
        return jsonify(data)
    
    elif request.method == 'POST':
        data = request.json
        pasien_id = data['pasien_id']
        riwayat_penyakit = data['riwayat_penyakit']
        
        cursor = mysql.connection.cursor()
        sql = "INSERT INTO riwayat (pasien_id, riwayat_penyakit) VALUES (%s, %s, %s)"
        val = (pasien_id, riwayat_penyakit)
        cursor.execute(sql, val)
        mysql.connection.commit()
        cursor.close()
        return jsonify({'message': 'Riwayat berhasil dibuat'})

@app.route('/editriwayat', methods=['PUT'])
def editriwayat():
    if 'riwayat_id' in request.args:
        riwayat_id = request.args['riwayat_id']
        data = request.get_json()
        cursor = mysql.connection.cursor()
        sql = "UPDATE riwayat SET pasien_id = %s, riwayat_penyakit = %s WHERE riwayat_id = %s"
        val = (data['pasien_id'], data['riwayat_penyakit'], riwayat_id)
        cursor.execute(sql, val)
        mysql.connection.commit()
        cursor.close()
        return jsonify({'message': 'Riwayat berhasil diubah'})
    return jsonify({'error': 'riwayat_id is required'}), 400

@app.route('/deleteriwayat', methods=['DELETE'])
def deleteriwayat():
    if 'riwayat_id' in request.args:
        riwayat_id = request.args['riwayat_id']
        cursor = mysql.connection.cursor()
        sql = "DELETE FROM riwayat WHERE riwayat_id = %s"
        cursor.execute(sql, (riwayat_id,))
        mysql.connection.commit()
        cursor.close()
        return jsonify({'message': 'Riwayat berhasil dihapus'})
    return jsonify({'error': 'riwayat_id is required'}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5004, debug=True)
