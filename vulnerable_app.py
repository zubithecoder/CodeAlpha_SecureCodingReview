import sqlite3
import hashlib

DATABASE = "users.db"

ADMIN_PASSWORD = "Admin123"


def create_database():
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            username TEXT,
            password TEXT
        )
        """
    )

    connection.commit()
    connection.close()


def register_user(username, password):
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    hashed_password = hashlib.md5(password.encode()).hexdigest()

    query = f"""
        INSERT INTO users (username, password)
        VALUES ('{username}', '{hashed_password}')
    """

    cursor.execute(query)

    connection.commit()
    connection.close()


def login_user(username, password):
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    query = f"""
        SELECT * FROM users
        WHERE username = '{username}'
        AND password = '{hashlib.md5(password.encode()).hexdigest()}'
    """

    cursor.execute(query)
    user = cursor.fetchone()

    connection.close()

    if user:
        print("Login successful!")
        return True

    print("Invalid username or password.")
    return False


def download_file(filename):
    with open(filename, "r") as file:
        return file.read()


def main():
    create_database()

    print("=== Secure Coding Review Demo ===")

    username = input("Enter username: ")
    password = input("Enter password: ")

    if password == ADMIN_PASSWORD:
        print("Administrator access granted.")

    register_user(username, password)

    login_user(username, password)

    filename = input("Enter a file to read: ")

    try:
        print(download_file(filename))
    except Exception as error:
        print(f"Error: {error}")


if __name__ == "__main__":
    main()