from flask import Flask, request, jsonify
from flask_mysqldb import MySQL

app = Flask(__name__)

# MySQL Configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'new_schema1'

mysql = MySQL(app)

# Create tables based on the provided data model
with app.app_context():
    cur = mysql.connection.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS dogs (
            id INT PRIMARY KEY AUTO_INCREMENT,
            name VARCHAR(255),
            gender VARCHAR(255),
            date_of_birth DATE,
            place_of_birth VARCHAR(255)
        )
    ''')
    cur.execute('''
        CREATE TABLE IF NOT EXISTS health_records (
            id INT PRIMARY KEY AUTO_INCREMENT,
            summary VARCHAR(255),
            details VARCHAR(255),
            dogs_id INT,
            vets_id INT,
            FOREIGN KEY (dogs_id) REFERENCES dogs(id)
            FOREIGN KEY (vets_id) REFERENCES vets(id)
        )
    ''')
    cur.execute('''
        CREATE TABLE IF NOT EXISTS vets (
            id INT PRIMARY KEY AUTO_INCREMENT,
            name VARCHAR(255),
        )
    ''')
    mysql.connection.commit()
    cur.close()

# CRUD Routes for dogs
@app.route('/dogs', methods=['GET'])
def get_dogs():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM dogs')
    dogs = cur.fetchall()
    cur.close()
    return jsonify({'dogs': dogs})


# CRUD Routes for health_records
@app.route('/health_records', methods=['GET'])
def get_health_records():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM health_records')
    records = cur.fetchall()
    cur.close()
    return jsonify({'health_records': records})


# CRUD Routes for vets
@app.route('/vets', methods=['GET'])
def get_vets():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM vets')
    vets = cur.fetchall()
    cur.close()
    return jsonify({'vets': vets})


if __name__ == '__main__':
    app.run(debug=True)
