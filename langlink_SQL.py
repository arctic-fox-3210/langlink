import pymysql

connection = pymysql.connect(
    host='localhost',
    user='root',
    password='shk0572A',
    charset='utf8'
)

def create_database():
    try:
        with connection.cursor() as cursor:
            create_database_query = "CREATE DATABASE IF NOT EXISTS langlink_SQL"
            cursor.execute(create_database_query)
    except Exception as e:
        print(f"創建資料庫時發生錯誤: {e}")

def create_table():
    try:
        create_database()
        connection.select_db('langlink_SQL')
        
        with connection.cursor() as cursor:
            create_table_query = """
            CREATE TABLE IF NOT EXISTS vector (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                embedding VARCHAR(255) NOT NULL,
                path TEXT NOT NULL
            )
            """
            cursor.execute(create_table_query)
    except Exception as e:
        print(f"創建資料表時發生錯誤: {e}")

def delete_all_file(file_name: str):
    try:
        create_table()
        cursor = connection.cursor()
        
        SQL_delete_qurey = "DELETE FROM vector"
        cursor.execute(SQL_delete_qurey)

        connection.commit()
        print("所有檔案已成功刪除。")

    except pymysql.MySQLError as e:
        print(f"刪除檔案時發生錯誤: {e}")

    finally:
        if connection.open:
            cursor.close()
            connection.close()

def upload_SQL(names, embeddings, paths):
    try:
        create_table()
        with connection.cursor() as cursor:
            for embedding, path, name in zip(embeddings, paths, names):
                SQL = "INSERT INTO vector (name, embedding, path) VALUES (%s, %s, %s)"
                cursor.execute(SQL, (name, path, str(embedding.tolist())))  # 將 embedding 轉為字符串
        connection.commit()
        
    except pymysql.MySQLError as e:
        print(f"上傳資料時發生錯誤: {e}")

    finally:
        connection.close()
