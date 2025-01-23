from flask import Flask, jsonify, request, render_template
import json
import random

app = Flask(__name__)

students = [
    { 'id': 1, 'name': 'Owen' },
    { 'id': 2, 'name': 'Mats' },
    { 'id': 3, 'name': 'Oliver' },
    { 'id': 4, 'name': 'Atsushi' },
    { 'id': 5, 'name': 'Shubham' },
    { 'id': 6, 'name': 'Nicolas' },
    { 'id': 7, 'name': 'Damien' },
    { 'id': 8, 'name': 'Dain' },
    { 'id': 9, 'name': 'Alex' },
    { 'id': 10, 'name': 'Adam' },
    { 'id': 11, 'name': 'Alex C' }
]

nextStudentId = 12

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/students', methods=['GET'])
def get_students():
    return jsonify(students)

@app.route('/add')
def add_student_page():
    return render_template('add.html')

@app.route('/students/<int:id>', methods=['GET'])
def get_student_by_id(id: int):
    student = get_student(id)
    if student is None:
        return jsonify({ 'error': 'Student does not exist'}), 404
    return jsonify(student)

@app.route('/students/random', methods=['GET'])
def get_random_student():
    if not students:
        return jsonify({ 'error': 'No students available' }), 404
    student = random.choice(students)
    return jsonify(student)

def get_student(id):
    return next((s for s in students if s['id'] == id), None)

def student_is_valid(studenta):
    for key in student.keys():
        if key != 'name':
            return False
    return True

@app.route('/students', methods=['POST'])
def create_student():
    global nextStudentId
    student = json.loads(request.data)
    if not student_is_valid(student):
        return jsonify({ 'error': 'Invalid student properties.' }), 400

    student['id'] = nextStudentId
    nextStudentId += 1
    students.append(student)

    return '', 201, { 'location': f'/students/{student["id"]}' }

@app.route('/students/<int:id>', methods=['PUT'])
def update_student(id: int):
    student = get_student(id)
    if student is None:
        return jsonify({ 'error': 'Student does not exist.' }), 404

    updated_student = json.loads(request.data)
    if not student_is_valid(updated_student):
        return jsonify({ 'error': 'Invalid student properties.' }), 400

    student.update(updated_student)

    return jsonify(student)

@app.route('/students/<int:id>', methods=['DELETE'])
def delete_student(id: int):
    global students
    student = get_student(id)
    if student is None:
        return jsonify({ 'error': 'Student does not exist.' }), 404

    students = [s for s in students if s['id'] != id]
    return jsonify(student), 200

if __name__ == '__main__':
    app.run()