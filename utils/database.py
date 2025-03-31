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
        conn.commit()  # Commit the transaction
    except sqlite3.IntegrityError:
        print(f"User {username} already exists.")
    finally:
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
        print(f"User {username} not found in the database.")
        conn.close()
        return
    
    current_highscore = result[0]

    # If the highscore is NULL or the new score is higher, update it
    if current_highscore is None or score > current_highscore:
        cursor.execute('''
            UPDATE users
            SET highscore = ?
            WHERE username = ?
        ''', (score, username))
        print(f"Highscore updated for user {username}: {score}")

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
    if result and result[0] is not None:
        return result[0]  # Return the high score
    return 0  # Return 0 if no high score is found

def getTopScores(limit = 5):
    """Returns the top scores from the database"""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    cursor.execute('''
        SELECT username, highscore
        FROM users
        WHERE highscore IS NOT NULL
        ORDER BY highscore DESC
        LIMIT ?''', (limit,))
    top_scores = cursor.fetchall()
    conn.close()
    return top_scores


initialazeDatabase()



    
