import hashlib
import socket
import ssl
import json
from metin_şifreleme import decrypte


def run_server():
    global calculated_hash_code
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_ip = "127.0.0.1"
    port = 8000
    server.bind((server_ip, port))
    server.listen(0)
    print(f"Listening on {server_ip}:{port}")
    client_socket, client_address = server.accept()
    print(f"Accepted connection from {client_address[0]}:{client_address[1]}")

    ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    ssl_context.load_cert_chain("server_cert.pem", "server_key.pem")

    secure_client_socket = ssl_context.wrap_socket(client_socket, True)

    while True:
        request = secure_client_socket.recv(4096)
        request = json.loads(request.decode())
        mesaj = decrypte(request['string'])
        hash_code = request['hash_code']
        print('Gelen mesaj: ', mesaj)
        print('Gelen Hash Kodu: ', hash_code)

        if mesaj.lower() == "close":
            secure_client_socket.send("close".encode("utf-8"))
            break

        response = "Veri server tarafından kabul edildi."
        secure_client_socket.send(response.encode("utf-8"))

        hash_object = hashlib.sha256(mesaj.encode())
        calculated_hash_code = hash_object.hexdigest()
        print('Hesaplanan Hash Kodu: ', calculated_hash_code)
        if calculated_hash_code == hash_code:
            print("Bütünlük kontrolü yapıldı veri güvenli")

    secure_client_socket.close()
    print("Connection to client closed")
    server.close()


run_server()
