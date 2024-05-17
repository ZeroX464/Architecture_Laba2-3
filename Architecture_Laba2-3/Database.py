import sqlite3
def checkUsernameIsExistInDB(username): # Проверка, что логина нет в БД
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM users WHERE username=?', (username,))
    answer = cursor.fetchone()[0] # 0 - записи нету, 1 - запись есть
    conn.close()
    return answer

def initialize_db():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    
    # Создание таблицы пользователей
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    
    users = [
    ('user1', 'password1'),
    ('user2', 'password2'),
    ('user3', 'password3')
]

    # Добавление тестовых пользователей, если их уже нет в БД
    for i in range(len(users)):
        user = users[i]
        if not checkUsernameIsExistInDB(user[0]):
            cursor.executemany('INSERT INTO users (username, password) VALUES (?, ?)', [(user[0], user[1])])
    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    initialize_db()
