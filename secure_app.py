import hashlib
import hmac
import os
import sqlite3
from pathlib import Path

DATABASE = "users.db"
FILES_DIRECTORY = Path("files").resolve()


def hash_password(password: str) -> str:
    salt = os.urandom(16)

    password_hash = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt,
        600_000,
    )

    return f"{salt.hex()}:{password_hash.hex()}"


def verify_password(password: str, stored_password: str) -> bool:
    try:
        salt_hex, stored_hash_hex = stored_password.split(":", 1)

        salt = bytes.fromhex(salt_hex)
        stored_hash = bytes.fromhex(stored_hash_hex)

        password_hash = hashlib.pbkdf2_hmac(
            "sha256",
            password.encode("utf-8"),
            salt,
            600_000,
        )

        return hmac.compare_digest(password_hash, stored_hash)

    except (ValueError, TypeError):
        return False


def create_database():
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT NOT NULL
        )
        """
    )

    connection.commit()
    connection.close()


def register_user(username: str, password: str):
    if not username or not password:
        print("Username and password are required.")
        return

    password_hash = hash_password(password)

    connection = sqlite3.connect(DATABASE)

    try:
        connection.execute(
            """
            INSERT INTO users (username, password)
            VALUES (?, ?)
            """,
            (username, password_hash),
        )

        connection.commit()
        print("User registered successfully.")

    except sqlite3.IntegrityError:
        print("Username already exists.")

    finally:
        connection.close()


def login_user(username: str, password: str) -> bool:
    connection = sqlite3.connect(DATABASE)

    try:
        cursor = connection.execute(
            """
            SELECT password
            FROM users
            WHERE username = ?
            """,
            (username,),
        )

        user = cursor.fetchone()

    finally:
        connection.close()

    if user and verify_password(password, user[0]):
        print("Login successful!")
        return True

    print("Invalid username or password.")
    return False


def read_file(filename: str):
    requested_path = (FILES_DIRECTORY / filename).resolve()

    try:
        requested_path.relative_to(FILES_DIRECTORY)
    except ValueError:
        print("Access denied: invalid file path.")
        return

    if not requested_path.is_file():
        print("File not found.")
        return

    try:
        return requested_path.read_text(encoding="utf-8")
    except OSError:
        print("Unable to read the requested file.")
        return


def main():
    create_database()

    print("=== Secure Coding Review Demo ===")

    username = input("Enter username: ").strip()
    password = input("Enter password: ")

    register_user(username, password)

    login_user(username, password)

    filename = input("Enter a file to read: ").strip()

    content = read_file(filename)

    if content is not None:
        print(content)


if __name__ == "__main__":
    main()