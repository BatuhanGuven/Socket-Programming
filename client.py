import socket
import ssl
from metin_şifreleme import encrypte
import json
import hashlib


def run_client():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #IPV4,TCP Soketi
    server_ip = "127.0.0.1"
    server_port = 8000
    client.connect((server_ip, server_port)) # Sunucuya bağlan
    ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT) #SSL bağlantısı için bir SSL bağlamı oluşturulur.
    ssl_context.load_verify_locations("server_cert.pem") #Sunucunun sertifikasının yüklenir
    secure_client_socket = ssl_context.wrap_socket(client, server_hostname="localhost") # Güvenli soket oluşturulur.Sunucu bağlantısı kurulur

    msg = ""
    try:
        while msg.lower() != "close":
            msg = input("Mesajı girin: ")

            hash_object = hashlib.sha256(msg.encode()) #  SHA-256 algoritmasıyla kriptografik olarak hashlenmesi sağlanır.
            hash_code = hash_object.hexdigest() # Hash kodu hesaplanır ve onaltılık formatta döndürülür.

            encrypted_message = encrypte(msg)

            data_to_send = {'string': encrypted_message, 'hash_code': hash_code}
            data_json = json.dumps(data_to_send).encode()

            secure_client_socket.sendall(data_json)
            response = secure_client_socket.recv(1024)
            response = response.decode("utf-8")
            print(f"Alındı: {response}")

    except Exception as e:
        print(f"Hata: {e}")
    finally:
        secure_client_socket.close()
        print("Sunucuyla bağlantı kapatıldı")



