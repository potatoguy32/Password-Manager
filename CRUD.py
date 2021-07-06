import sqlite3


def create_db():
    # Create (connect) database
    conn = sqlite3.connect("PasswordManager.db")
    cur = conn.cursor()

    # Create users and passwords tables
    cur.execute("""
    CREATE TABLE IF NOT EXISTS Users (
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        master_password TEXT NOT NULL
    );
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS Passwords(
        pass_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        site TEXT,
        url TEXT,
        email TEXT,
        site_username TEXT,
        password TEXT NOT NULL
    );
    """)

    # Commit changes
    conn.commit()
    # Close database
    conn.close()


# Query to check if the user already is registered in the DB
def can_login(username, password):
    with sqlite3.connect("PasswordManager.db") as conn:
        cur = conn.cursor()
        cur.execute("""
                SELECT * FROM Users
                WHERE username = :username AND master_password = :master_password;""",
                    {
                        "username": username,
                        "master_password": password
                    })
        if cur.fetchone() is None:
            return False

        return True

def get_id(username):
    with sqlite3.connect("PasswordManager.db") as conn:
        cur = conn.cursor()
        cur.execute("""SELECT user_id FROM Users WHERE username = :username""",
                    {
                        "username": username,
                    })
        return cur.fetchone()


# Check if user already exist
def is_registered(username):
    with sqlite3.Connection("PasswordManager.db") as conn:
        cur = conn.cursor()
        cur.execute("""SELECT * FROM Users WHERE username = :username;""",
                    {
                        "username": username,
                    })
        if len(cur.fetchall()) != 1:
            return True

        return False


# Create a new user
def register_user(username, password):
    conn = sqlite3.connect("PasswordManager.db")
    cur = conn.cursor()
    cur.execute("""INSERT INTO Users (username, master_password) VALUES (:username, :master_password);""",
                {
                    "username": username,
                    "master_password": password
                })
    conn.commit()
    conn.close()


def query_site(user_id, site=None):
    with sqlite3.connect("PasswordManager.db") as conn:
        cur = conn.cursor()
        if site == "" or site is None:
            cur.execute("""SELECT site, url, email, site_username, password
                           FROM Passwords
                           WHERE user_id = :user_id;""",
                        {
                            "user_id": user_id
                        })

        else:
            cur.execute("""SELECT site, url, email, site_username, password
                           FROM Passwords
                           WHERE ((site LIKE  ':text') OR (url = :text)) AND (user_id = :user_id);""",
                        {
                            "text": site,
                            "user_id": user_id
                        })

        return cur.fetchall()


def submit_site(user_id, site_name, site_url, site_email, site_username, site_password):
    with sqlite3.connect("PasswordManager.db") as conn:
        cur = conn.cursor()
        cur.execute("""INSERT INTO Passwords (user_id, site, url, email, site_username, password)
                        VALUES  (:user_id, :site, :url, :email, :site_username, :password);""",
                    {
                        "user_id": user_id,
                        "site": site_name,
                        "url": site_url,
                        "email": site_email,
                        "site_username": site_username,
                        "password": site_password
                    })
        conn.commit()

def get_data_to_config(user_id):
    with sqlite3.connect("PasswordManager.db") as conn:
        cur = conn.cursor()
        cur.execute("""SELECT site, email, site_username FROM Passwords
                        WHERE user_id = :user_id""", {"user_id": user_id})
        return cur.fetchall()
