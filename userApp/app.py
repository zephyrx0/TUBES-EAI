from flask import Flask, jsonify, request, session
from flask_mysqldb import MySQL
from datetime import datetime
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

app.secret_key = 'cobain'

# MySQL config
app.config['MYSQL_HOST'] = 'tubes-nabilamelsyana5-c7f0.a.aivencloud.com'
app.config['MYSQL_PORT'] = 26484
app.config['MYSQL_USER'] = 'avnadmin'
app.config['MYSQL_PASSWORD'] = 'AVNS_pr3FDArYqXJReBFPPXg'
app.config['MYSQL_DB'] = 'rumahsakit'
mysql = MySQL(app)

def create_response(data, status_code, message):
    response = {
        'timestamp': datetime.now().isoformat(),
        'status': status_code,
        'message': message,
        'data': data
    }
    return jsonify(response)

# Login route
@app.route('/', methods=['POST'])
def login():
    try:
        email = request.form['email']
        password = request.form['password']
        
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM user WHERE email = %s AND password = %s", (email, password))
        user = cur.fetchone()
        cur.close()
        
        if user:
            session['email'] = email
            return jsonify({"message": "Login successful"}), 200
        else:
            return jsonify({"message": "Invalid email or password"}), 401
    except Exception as e:
        return jsonify({"message": str(e)}), 500

# Logout route
@app.route('/logout', methods=['POST'])
def logout():
    try:
        session.pop('email', None)
        return jsonify({"message": "Logout successful"}), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500

# User route for testing
@app.route('/user', methods=['GET'])
def user():
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM user")
        column_names = [i[0] for i in cursor.description]
        data = [dict(zip(column_names, row)) for row in cursor.fetchall()]
        cursor.close()
        return create_response(data, 200, 'Success')
    except Exception as e:
        return create_response(None, 500, str(e))

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=4999)
