import json

def load_data(conn, student_path, room_path):
    '''Принимает пути хранения двух json файлов, считывает их и заносит в БД'''
    cursor = conn.cursor()
    with open(room_path, 'r', encoding= 'utf-8') as f:
        for room in json.load(f):
            cursor.execute('INSERT INTO rooms (id, name) VALUES (%s, %s)', (room["id"], room["name"]))

    with open(student_path, 'r', encoding='utf-8') as f:
        for student in json.load(f):
            cursor.execute(
                'INSERT INTO students values (%s, %s, %s, %s, %s)', (
                    student["birthday"],
                    student["id"],
                    student["name"],
                    student["room"],
                    student["sex"],
                )
            )
    conn.commit()