import os
import sqlite3
import hashlib
from client import run_client
conn = sqlite3.connect('user_database.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password_hash TEXT
    )
''')
conn.commit()
def hash_password(password):
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

def verify_password(password, stored_password_hash):
    return stored_password_hash == hash_password(password)

def clear_terminal():
    os.system('cls')

def register_user(username, password):
    password_hash = hash_password(password)
    cursor.execute('Select username From users Where username == ?', (username,))
    exist_name = cursor.fetchone()
    if exist_name:
        print("Kullanıcı zaten mevcut")
        return
    cursor.execute('INSERT INTO users (username, password_hash) VALUES (?, ?)', (username, password_hash))
    print("Kayıt başarı ile tamamlandı...")
    run_client()
    conn.commit()
def login_user(username, password):
    cursor.execute('SELECT password_hash FROM users WHERE username = ?', (username,))
    result = cursor.fetchone()

    if result:
        stored_password_hash = result[0]
        if verify_password(password, stored_password_hash):
            print("Oturum açma başarılı!")
            if username == 'batuhan':
                yetkili_menu()
            else:
                run_client()
        else:
            print("Kullanıcı adı veya parola hatalı.")
    else:
        print("Kullanıcı bulunamadı.")

def yetkili_menu():
    while True:
        clear_terminal()
        print("\nYETKILI MENU:")
        print("1. Veritabanını görüntüle")
        print("2. Geri")

        sub_choice = input("Seçiminizi yapın: ")

        if sub_choice == "1":
            cursor.execute('SELECT username, password_hash FROM users')
            rows = cursor.fetchall()
            for row in rows:
                print(row)
        elif sub_choice == "2":
            break
        else:
            print("Geçersiz seçim. Lütfen tekrar deneyin.")


def main():
    while True:
        clear_terminal()
        print("\nMENU:")
        print("1. Giriş Yap")
        print("2. Kaydol")
        print("3. Yetkili Giriş")
        print("4. Çıkış")

        choice = input("Seçiminizi yapın: ")

        if choice == "1":
            username = input("Kullanıcı adı: ")
            password = input("Parola: ")
            login_user(username, password)

        elif choice == "2":
            username = input("Kullanıcı adı: ")
            password = input("Parola: ")
            register_user(username, password)

        elif choice == "3":
            username = input("Yetkili adı: ")
            password = input("Parola: ")
            login_user(username, password)
        elif choice == "4":
            print("Çıkılıyor...")

            break
        else:
            print("Geçersiz seçim. Lütfen tekrar deneyin.")

    conn.close()


if __name__ == "__main__":
    main()
