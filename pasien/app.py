from flask import Flask, jsonify, request , render_template
from flask_mysqldb import MySQL

app= Flask(__name__)

app.config['MYSQL_HOST'] = 'tubes-nabilamelsyana5-c7f0.a.aivencloud.com'
app.config['MYSQL_USER'] = 'avnadmin'
app.config['MYSQL_PASSWORD'] = 'AVNS_pr3FDArYqXJReBFPPXg'
app.config['MYSQL_DB'] = 'rumahsakit'
app.config['MYSQL_PORT'] = 26484

mysql = MySQL(app)

@app.route('/pasien', methods=['GET', 'POST'])
def pasien():
    if request.method == 'GET':
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM pasien")
        kolom = [i[0] for i in cursor.description]
        data = []
        for row in cursor.fetchall():
            data.append(dict(zip(kolom, row)))
        for item in data:
            tanggal_lahir_date = item['tanggal_lahir']
            item['tanggal_lahir'] = tanggal_lahir_date.strftime("%Y-%m-%d")
        cursor.close()
        return jsonify(data)
    
    elif request.method =='POST':
        nama = request.json['nama']
        tanggal_lahir = request.json['tanggal_lahir']
        alamat = request.json['alamat']
        tipe_darah = request.json['tipe_darah']
        

        cursor = mysql.connection.cursor()
        sql = "INSERT INTO pasien (nama, tanggal_lahir, alamat, tipe_darah) VALUES (%s,%s,%s,%s)"

        val = (nama, tanggal_lahir, alamat, tipe_darah)
        cursor.execute(sql,val)

        mysql.connection.commit()

        return jsonify({'message':'data berhasil masuk'})
        cursor.close()
    

@app.route('/detailpasien',methods =['GET'])
def detailpasien():
    if 'pasien_id' in request.args:
        cursor = mysql.connection.cursor()
        sql = "SELECT * FROM pasien WHERE pasien_id = %s"
        val = (request.args['pasien_id'])
        cursor.execute(sql,val)
        kolom = [i[0] for i in cursor.description]
        data = []
        for row in cursor.fetchall():
            data.append(dict(zip(kolom,row)))

        
        return jsonify(data)
        cursor.close()


@app.route('/editpasien', methods = ['PUT'])
def editpasien():
    if 'pasien_id' in request.args:
        data = request.get_json()

        cursor = mysql.connection.cursor()
        sql = "UPDATE pasien SET nama = %s, tanggal_lahir = %s, alamat = %s, tipe_darah = %s WHERE pasien_id = %s"
        val = (data['nama'], data['tanggal_lahir'], data['alamat'], data['tipe_darah'],request.args['pasien_id'])
        cursor.execute(sql, val)
        mysql.connection.commit()
        cursor.close()  

        return jsonify({'message': 'data berhasil diubah'})
    return jsonify({'error': 'pasien_id is required'}), 400

@app.route('/deletepasien', methods=['DELETE'])
def deletepasien():
    if 'pasien_id' in request.args:
        pasien_id = request.args['pasien_id']

        cursor = mysql.connection.cursor()
        sql = "DELETE FROM pasien WHERE pasien_id = %s"
        val = (pasien_id,)
        cursor.execute(sql, val)
        mysql.connection.commit()
        cursor.close()

        return jsonify({'message': 'Data pasien berhasil dihapus'})

    return jsonify({'error': 'pasien_id is required'}), 400

if __name__ == '__main__':
    app.run(host = '0.0.0.0', port = 5001, debug = True)