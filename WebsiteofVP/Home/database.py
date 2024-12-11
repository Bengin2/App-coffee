import sqlite3
import os


curent_pth = os.path.abspath(os.path.dirname(__file__))
dbb_path = os.path.join(curent_pth,"user.db")
connection = sqlite3.connect(dbb_path,check_same_thread=False)
cursor = connection.cursor()
print(dbb_path)


def _create_user():
    try:
        
        user = '''
            CREATE TABLE users(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username VARCHAR(100),
                password VARCHAR(100)
            )
        '''
        cursor.execute(user)
        return "database set up"
       
    except Exception as error:
        return error
    
def _create_login():
    try:
    
        user_login = [1,"adminadmin","admin123"]
        user = '''
            INSERT INTO users (id,username,password)
            VALUEs (?,?,?)
        '''
        
        cursor.execute(user,user_login)
        connection.commit()
        return "user set up"
      
    except Exception as error:
        return error
    
def _query_user():
    try:
    
        query = '''SELECT * FROM users'''
        cursor.execute(query)    
        for obj in cursor.fetchall():
            id = obj[0]
            username = obj[1]
            password = obj[2]
        return f"{id} {username} {password}"
        
    except Exception as error:
        return error
    
    

print(_create_user())
print(_create_login())
print(_query_user())
