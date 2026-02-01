import sqlite3
from flask import Flask, jsonify, request, render_template, g

app = Flask(__name__)
DATABASE = 'students.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def init_db():
    with app.app_context():
        db = get_db()
        db.execute('''
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL
            )
        ''')
        db.commit()

@app.before_request
def setup():
    init_db()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/students', methods=['GET'])
def get_students():
    db = get_db()
    cur = db.execute('SELECT * FROM students')
    students = [dict(row) for row in cur.fetchall()]
    return jsonify(students)

@app.route('/add')
def add_student_page():
    return render_template('add.html')

@app.route('/students/<int:id>', methods=['GET'])
def get_student_by_id(id: int):
    db = get_db()
    cur = db.execute('SELECT * FROM students WHERE id = ?', (id,))
    student = cur.fetchone()
    if student is None:
        return jsonify({ 'error': 'Student does not exist'}), 404
    return jsonify(dict(student))

@app.route('/students/random', methods=['GET'])
def get_random_student():
    db = get_db()
    cur = db.execute('SELECT * FROM students ORDER BY RANDOM() LIMIT 1')
    student = cur.fetchone()
    if student is None:
        return jsonify({ 'error': 'No students available' }), 404
    return jsonify(dict(student))

def student_is_valid(student):
    return set(student.keys()) == {'name'}

@app.route('/students', methods=['POST'])
def create_student():
    student = request.get_json()
    if not student_is_valid(student):
        return jsonify({ 'error': 'Invalid student properties.' }), 400
    db = get_db()
    cur = db.execute('INSERT INTO students (name) VALUES (?)', (student['name'],))
    db.commit()
    student_id = cur.lastrowid
    return '', 201, { 'location': f'/students/{student_id}' }

@app.route('/students/<int:id>', methods=['PUT'])
def update_student(id: int):
    db = get_db()
    cur = db.execute('SELECT * FROM students WHERE id = ?', (id,))
    student = cur.fetchone()
    if student is None:
        return jsonify({ 'error': 'Student does not exist.' }), 404
    updated_student = request.get_json()
    if not student_is_valid(updated_student):
        return jsonify({ 'error': 'Invalid student properties.' }), 400
    db.execute('UPDATE students SET name = ? WHERE id = ?', (updated_student['name'], id))
    db.commit()
    return jsonify({ 'id': id, 'name': updated_student['name'] })

@app.route('/students/<int:id>', methods=['DELETE'])
def delete_student(id: int):
    db = get_db()
    cur = db.execute('SELECT * FROM students WHERE id = ?', (id,))
    student = cur.fetchone()
    if student is None:
        return jsonify({ 'error': 'Student does not exist.' }), 404
    db.execute('DELETE FROM students WHERE id = ?', (id,))
    db.commit()
    return jsonify(dict(student)), 200

def init_db():
    with app.app_context():
        db = get_db()
        db.execute('''
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL
            )
        ''')
        db.commit()
        cur = db.execute('SELECT COUNT(*) FROM students')
        if cur.fetchone()[0] == 0:
            initial_students = [
                ('Owen',), ('Mats',), ('Oliver',), ('Atsushi',), ('Shubham',),
                ('Nicolas',), ('Louie the Dog',), ('Sandy the Cat',),
                ('Buster the Cat',), ('Adam',), ('Alex C',)
            ]
            db.executemany('INSERT INTO students (name) VALUES (?)', initial_students)
            db.commit()



if __name__ == '__main__':
    init_db()
    app.run()