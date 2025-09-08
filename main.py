import connection
import importData
import queries
import exportData
from queries import delete_data
import sys


def main():
    if len(sys.argv) > 3:
        students_path = sys.argv[1]
        rooms_path = sys.argv[2]
        output_format = sys.argv[3]
    else:
        students_path = 'students.json'
        rooms_path = 'rooms.json'
        output_format = 'json'

    conn = connection.connection()
    delete_data(conn)
    importData.load_data(conn,
             students_path,
             rooms_path,
    )
    queries.create_indexes(conn)

    result = queries.count_students_into_rooms(conn)
    exportData.dump_data(result, output_format, "output1")
    result = queries.rooms_min_avg_age(conn)
    exportData.dump_data(result, output_format, "output2")
    result = queries.max_age_diff(conn)
    exportData.dump_data(result, output_format, "output3")
    result = queries.mixed_sex_rooms(conn)
    exportData.dump_data(result, output_format, "output4")

if __name__ == "__main__":
    main()