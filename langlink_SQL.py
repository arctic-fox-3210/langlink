import pymysql
import subprocess

def MySQL_status():
    try:
        result = subprocess.run(['sc', 'query', 'mysql'], capture_output=True, text=True)
        if "RUNNING" in result.stdout:
            return True
        else:
            return False
    except Exception as e:
        print(f"檢查 MySQL 狀態時發生錯誤: {e}")
        return False

def start_MySQL():
    if not MySQL_status():
        try:
            subprocess.run(['net', 'start', 'mysql'], check=True)
        except subprocess.CalledProcessError as e:
            print(f"啟動 MySQL 伺服器時發生錯誤: {e}")

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

start_MySQL()
create_table()

def delete_all_file():
    try:
        cursor = connection.cursor()
        
        SQL_delete_qurey = "DELETE FROM vector"
        cursor.execute(SQL_delete_qurey)

        connection.commit()
        print("所有檔案已成功刪除。")

    except pymysql.MySQLError as e:
        print(f"刪除檔案時發生錯誤: {e}")

    finally:
        if 'cursor' in locals() and cursor:
            cursor.close()

def delete_file(file_path: str):
    try:
        cursor = connection.cursor()

        SQL_delete_qurey = "DELETE FROM vector WHERE path = %s"
        cursor.execute(SQL_delete_qurey, (file_path, ))
        connection.commit()
    
    except pymysql.MySQLError as e:
        print(f"刪除檔案時發生錯誤: {e}")
    
    finally:
        if 'cursor' in locals() and cursor:
            cursor.close()

        
def upload_SQL(names, embeddings, paths):
    try:
        with connection.cursor() as cursor:
            for embedding, path, name in zip(embeddings, paths, names):
                SQL = "INSERT INTO vector (name, embedding, path) VALUES (%s, %s, %s)"
                cursor.execute(SQL, (name, path, str(embedding.tolist())))  # 將 embedding 轉為字符串
        connection.commit()
        
    except pymysql.MySQLError as e:
        print(f"上傳資料時發生錯誤: {e}")

if connection.open:
    connection.close()
