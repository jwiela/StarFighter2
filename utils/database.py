import sqlite3
import os 
import bcrypt

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_PATH = os.path.join(BASE_DIR, '..', 'game_data.db')

# Check if the database file exists, if not, create it

def initialazeDatabase():
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            highscore INTEGER DEFAULT 0
        )
    ''')

    conn.commit()
    conn.close()

# Returns hashed password
def hashPassword(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

# Checks if the password is correct
def verifyPassword(password, hashed_password):
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))


# Adds a new user to the database
def addUser(username, password):
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    hashed_password = hashPassword(password)

    try:
        cursor.execute('''
            INSERT INTO users (username, password)
            VALUES (?, ?)
        ''', (username, hashed_password))
    except sqlite3.IntegrityError:
        pass

    conn.close()


# Cheks if the user exists in the database and if the password is correct
def authenticateUser(username, password):
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    cursor.execute('''SELECT password
                   FROM users
                   WHERE username = ?''', (username,)
                   )
    result = cursor.fetchone()

    conn.close()

    if result:
        return verifyPassword(password, result[0])
    return False


# Updates the highscore of the user if the new score is higher than the current highscore
def updateHighscore(username, score):
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    cursor.execute('''SELECT highscore
                   FROM users
                   WHERE username = ?''', (username,)
                   )
    
    result = cursor.fetchone()

    if result is None:
        return
    
    if score > result[0]:
        cursor.execute('''
            UPDATE users
            SET highscore = ?
            WHERE username = ?
        ''', (score, username))

    conn.commit()
    conn.close()

# Returns the highscore of the user
def getHighscore(username):
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    cursor.execute('''SELECT highscore
                   FROM users
                   WHERE username = ?''', (username,)
                   )
    result = cursor.fetchone()

    conn.close()
    if result:
        return result[0]
    return 0

initialazeDatabase()



    
