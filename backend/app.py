from flask import Flask, jsonify, request, send_from_directory
import psycopg2
import os

app = Flask(__name__)
DATABASE_URL = os.getenv('DATABASE_URL')

def get_db_connection():
    return psycopg2.connect(DATABASE_URL)

@app.route('/')
def index():
    # Указываем путь к папке frontend, которая находится на уровень выше
    return send_from_directory('../frontend', 'index.html')

@app.route('/api/data', methods=['GET'])
def get_data():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT * FROM items;')
        items = cur.fetchall()
        cur.close()
        conn.close()
        return jsonify([{"id": i[0], "name": i[1]} for i in items])
    except:
        return jsonify([])

@app.route('/api/data', methods=['POST'])
def add_data():
    new_item = request.json.get('name')
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('INSERT INTO items (name) VALUES (%s)', (new_item,))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"status": "added"}), 201

if __name__ == '__main__':
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('CREATE TABLE IF NOT EXISTS items (id serial PRIMARY KEY, name varchar(100));')
        conn.commit()
        cur.close()
        conn.close()
    except:
        print("Waiting for DB...")
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 5000)))
