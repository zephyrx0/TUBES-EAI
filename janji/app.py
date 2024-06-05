from flask import Flask, jsonify, request , render_template
from flask_mysqldb import MySQL
from datetime import datetime, timedelta
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

@app.route('/janji', methods=['GET', 'POST'])
def janji():
    if request.method == 'GET':
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM janji")
        kolom = [i[0] for i in cursor.description]
        data = [dict(zip(kolom, row)) for row in cursor.fetchall()]
        for item in data:
            tanggal_janji_date = item['tanggal_janji']
            item['tanggal_janji'] = tanggal_janji_date.strftime("%Y-%m-%d")
        cursor.close()
        return jsonify(data)
    
    elif request.method == 'POST':
        data = request.json
        pasien_id = data['pasien_id']
        dokter_id = data['dokter_id']
        tanggal_janji = data['tanggal_janji']
        waktu_janji = data['waktu_janji']
        keterangan = data['keterangan']
        
        cursor = mysql.connection.cursor()
        sql = "INSERT INTO janji (pasien_id, dokter_id, tanggal_janji, waktu_janji, keterangan) VALUES (%s, %s, %s, %s, %s)"
        val = (pasien_id, dokter_id, tanggal_janji, waktu_janji, keterangan)
        cursor.execute(sql, val)
        mysql.connection.commit()
        cursor.close()
        return jsonify({'message': 'Janji berhasil dibuat'})

@app.route('/editjanji', methods=['PUT'])
def editjanji():
    if 'janji_id' in request.args:
        janji_id = request.args['janji_id']
        data = request.get_json()
        cursor = mysql.connection.cursor()
        sql = "UPDATE janji SET pasien_id = %s, dokter_id = %s, tanggal_janji = %s, waktu_janji = %s, keterangan = %s WHERE janji_id = %s"
        val = (data['pasien_id'], data['dokter_id'], data['tanggal_janji'], data['waktu_janji'], data['keterangan'], janji_id)
        cursor.execute(sql, val)
        mysql.connection.commit()
        cursor.close()
        return jsonify({'message': 'Janji berhasil diubah'})
    return jsonify({'error': 'janji_id is required'}), 400

@app.route('/deletejanji', methods=['DELETE'])
def deletejanji():
    if 'janji_id' in request.args:
        janji_id = request.args['janji_id']
        cursor = mysql.connection.cursor()
        sql = "DELETE FROM janji WHERE janji_id = %s"
        cursor.execute(sql, (janji_id,))
        mysql.connection.commit()
        cursor.close()
        return jsonify({'message': 'Janji berhasil dihapus'})
    return jsonify({'error': 'janji_id is required'}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003, debug=True)
