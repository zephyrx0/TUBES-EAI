from flask import Flask, jsonify, request , render_template
from flask_mysqldb import MySQL

app= Flask(__name__)

app.config['MYSQL_HOST'] = 'tubes-nabilamelsyana5-c7f0.a.aivencloud.com'
app.config['MYSQL_USER'] = 'avnadmin'
app.config['MYSQL_PASSWORD'] = 'AVNS_pr3FDArYqXJReBFPPXg'
app.config['MYSQL_DB'] = 'rumahsakit'
app.config['MYSQL_PORT'] = 26484

mysql = MySQL(app)

@app.route('/dokter', methods=['GET', 'POST'])
def dokter():
    if request.method == 'GET':
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM dokter")
        kolom = [i[0] for i in cursor.description]
        data = []
        for row in cursor.fetchall():
            data.append(dict(zip(kolom, row)))
        cursor.close()
        return jsonify(data)
    
    elif request.method =='POST':
        nama = request.json['nama']
        poli = request.json['poli']
        

        cursor = mysql.connection.cursor()
        sql = "INSERT INTO dokter (nama, poli) VALUES (%s,%s)"

        val = (nama, poli)
        cursor.execute(sql,val)

        mysql.connection.commit()

        return jsonify({'message':'data berhasil masuk'})
        cursor.close()
    

@app.route('/detaildokter',methods =['GET'])
def detaildokter():
    if 'dokter_id' in request.args:
        cursor = mysql.connection.cursor()
        sql = "SELECT * FROM dokter WHERE dokter_id = %s"
        val = (request.args['dokter_id'])
        cursor.execute(sql,val)
        kolom = [i[0] for i in cursor.description]
        data = []
        for row in cursor.fetchall():
            data.append(dict(zip(kolom,row)))

        
        return jsonify(data)
        cursor.close()


@app.route('/editdokter', methods = ['PUT'])
def editdokter():
    if 'dokter_id' in request.args:
        data = request.get_json()

        cursor = mysql.connection.cursor()
        sql = "UPDATE dokter SET nama = %s, poli = %s WHERE dokter_id = %s"
        val = (data['nama'], data['poli'],request.args['dokter_id'])
        cursor.execute(sql, val)
        mysql.connection.commit()
        cursor.close()  

        return jsonify({'message': 'data berhasil diubah'})
    return jsonify({'error': 'dokter_id is required'}), 400

@app.route('/deletedokter', methods=['DELETE'])
def deletedokter():
    if 'dokter_id' in request.args:
        dokter_id = request.args['dokter_id']

        cursor = mysql.connection.cursor()
        sql = "DELETE FROM dokter WHERE dokter_id = %s"
        val = (dokter_id,)
        cursor.execute(sql, val)
        mysql.connection.commit()
        cursor.close()

        return jsonify({'message': 'Data dokter berhasil dihapus'})

    return jsonify({'error': 'dokter_id is required'}), 400

if __name__ == '__main__':
    app.run(host = '0.0.0.0', port = 5002, debug = True)