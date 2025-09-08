def delete_data(conn):
    '''Удаляет все записи из таблиц students и rooms.'''
    cursor = conn.cursor()
    cursor.execute("DELETE FROM students")
    cursor.execute("DELETE FROM rooms")
    conn.commit()

def create_indexes(conn):
    '''Эта функция создает четыре индекса для таблиц student и room.
    Цель создания этих индексов - ускорить выполнение SQL-запросов, которые фильтруют или соединяют данные по этим столбцам.'''
    cursor = conn.cursor()
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_student_room_id ON students(room_id);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_student_birthday ON students(birthday);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_student_sex ON students(sex);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_room_name ON rooms(name);")
    conn.commit()

def count_students_into_rooms(conn):
    '''Выполяет запрос по подсчету количества студентов в каждой из комнат и возвращает результат.'''
    cursor = conn.cursor()
    cursor.execute("""
        select rooms.name, count(students.id) as student_count
            from rooms
            left join students on rooms.id = students.room_id
            group by rooms.id, rooms.name
            order by rooms.name;
    """)
    result = cursor.fetchall()
    return result

def rooms_min_avg_age(conn):
    '''Выполяет запрос по поиску 5 минимальных средних возрастов в комнате и возвращает результат.'''
    cursor = conn.cursor()
    cursor.execute("""
    select rooms.name, avg(extract(year from age(now(), students.birthday))) as avg_age
        from rooms
        join students on rooms.id = students.room_id
        group by rooms.id,rooms.name
        order by avg_age
        limit 5;
    """)
    result = cursor.fetchall()
    return result

def max_age_diff(conn):
    '''Выполяет запрос по поиску 5 максимальных разниц в возрасте в комнате и возвращает результат.'''
    cursor = conn.cursor()
    cursor.execute("""
        select rooms.name, max(extract(year from age(now(), students.birthday))) -
            min(extract(year from age(now(), students.birthday))) as age_diff
            from rooms
            join students on rooms.id = students.room_id
            group by rooms.id,rooms.name
            order by age_diff desc
            limit 5;
    """)
    result = cursor.fetchall()
    return result

def mixed_sex_rooms(conn):
    '''Выполяет запрос по поиску комнат, в которых живут представители обоих полов и возвращает результат.'''
    cursor = conn.cursor()
    cursor.execute("""
    SELECT rooms.name
        from students
        inner JOIN rooms on students.room_id = rooms.id
        Group by rooms.id
        HAVING COUNT(DISTINCT students.sex) > 1
        ORDER BY rooms.id;
    """)
    result = cursor.fetchall()
    return result