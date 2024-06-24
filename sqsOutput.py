import json
import pymysql

db_host = 'database-host'
db_user = 'username'
db_password = 'password'
db_name = 'database-name'

def get_db_connection():
    connection = pymysql.connect(
        host=db_host,
        user=db_user,
        password=db_password,
        db=db_name
    )
    return connection

def lambda_handler(event, context):
    for record in event['Records']:
        data = json.loads(record['body'])
        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
                sql = "INSERT INTO progress (student_id, course_id, progress) VALUES (%s, %s, %s)"
                cursor.execute(sql, (data['student_id'], data['course_id'], data['progress']))
                connection.commit()
        finally:
            connection.close()
    return {
        'statusCode': 200,
        'body': json.dumps('Data processed and stored in database successfully')
    }
