from flask import Flask, jsonify, request
from flask_mysqldb import MySQL
from datetime import datetime, timedelta
import json
from flask.json.provider import DefaultJSONProvider
import logging

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'tubes-nabilamelsyana5-c7f0.a.aivencloud.com'
app.config['MYSQL_USER'] = 'avnadmin'
app.config['MYSQL_PASSWORD'] = 'AVNS_pr3FDArYqXJReBFPPXg'
app.config['MYSQL_DB'] = 'rumahsakit'
app.config['MYSQL_PORT'] = 26484

mysql = MySQL(app)

# Setup logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class CustomJSONProvider(DefaultJSONProvider):
    def default(self, obj):
        if isinstance(obj, (datetime, timedelta)):
            return str(obj)
        return super().default(obj)

app.json = CustomJSONProvider(app)

@app.route('/riwayat', methods=['GET'])
def get_riwayat():
    try:
        cur = mysql.connection.cursor()
        cur.execute("""
           SELECT r.riwayat_id, r.pasien_id, p.nama as nama_pasien, r.riwayat_penyakit, r.tanggal
            FROM riwayat r
            JOIN pasien p ON r.pasien_id = p.pasien_id

        """)
        data = cur.fetchall()
        cur.close()
        
        riwayat_list = []
        for row in data:
            riwayat_list.append({
                "riwayat_id": row[0],
                "pasien_id": row[1],
                "nama_pasien": row[2],
                "riwayat_penyakit": row[3],
                "tanggal": row[4]
            })
        
        return jsonify(riwayat_list)
    except Exception as e:
        logger.error(f"Error occurred while fetching riwayat: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/tambah_riwayat', methods=['POST'])
def tambah_riwayat():
    try:
        data = request.get_json()
        pasien_id = data['pasien_id']
        riwayat_penyakit = data['riwayat_penyakit']
        tanggal = data['tanggal']
        
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO riwayat (pasien_id, riwayat_penyakit, tanggal) VALUES (%s, %s, %s)", (pasien_id, riwayat_penyakit, tanggal))
        mysql.connection.commit()
        cur.close()
        return jsonify({"message": "Data riwayat berhasil ditambahkan"}), 201
    except Exception as e:
        logger.error(f"Error occurred while adding riwayat: {e}")
        return jsonify({"error": str(e)}), 500


# Endpoint untuk mendapatkan detail data riwayat berdasarkan id
@app.route('/detailriwayat/<int:riwayat_id>', methods=['GET'])
def detail_riwayat(riwayat_id):
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT riwayat_id, pasien_id, riwayat_penyakit, tanggal FROM riwayat WHERE riwayat_id = %s", (riwayat_id,))
        data = cur.fetchone()
        cur.close()
        
        if data:
            riwayat_detail = {
                "riwayat_id": data[0],
                "pasien_id": data[1],
                "riwayat_penyakit": data[2],
                "tanggal": data[3]
            }
            return jsonify(riwayat_detail)
        else:
            return jsonify({"error": "Data riwayat tidak ditemukan"}), 404
    except Exception as e:
        logger.error(f"Error occurred while fetching detail riwayat: {e}")
        return jsonify({"error": str(e)}), 500


@app.route('/editriwayat/<int:riwayat_id>', methods=['PUT'])
def edit_riwayat(riwayat_id):
    try:
        data = request.get_json()
        pasien_id = data['pasien_id']
        riwayat_penyakit = data['riwayat_penyakit']
        tanggal = data['tanggal']
        
        cur = mysql.connection.cursor()
        cur.execute("UPDATE riwayat SET pasien_id = %s, riwayat_penyakit = %s, tanggal = %s WHERE riwayat_id = %s", (pasien_id, riwayat_penyakit, tanggal, riwayat_id))
        mysql.connection.commit()
        cur.close()
        return jsonify({"message": "Data riwayat berhasil diupdate"}), 200
    except Exception as e:
        logger.error(f"Error occurred while updating riwayat: {e}")
        return jsonify({"error": str(e)}), 500


# Endpoint untuk menghapus data riwayat berdasarkan id
@app.route('/deleteriwayat/<int:riwayat_id>', methods=['DELETE'])
def delete_riwayat(riwayat_id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM riwayat WHERE riwayat_id = %s", (riwayat_id,))
    mysql.connection.commit()
    cur.close()
    return jsonify({"message": "Data riwayat berhasil dihapus"}), 200

@app.route('/pasien_riwayat', methods=['GET'])
def get_pasien_riwayat():
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT pasien_id, nama FROM pasien")
        data = cur.fetchall()
        cur.close()
        
        pasien_list = []
        for row in data:
            pasien_list.append({
                "pasien_id": row[0],
                "nama": row[1]
            })
        
        return jsonify({"data": pasien_list})
    except Exception as e:
        logger.error(f"Error occurred while fetching pasien: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5004, debug=True)
