import socket
import ssl

def run_client():
    # TCP soketi oluştur
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bağlanılacak sunucu IP adresi ve port numarası
    server_ip = "127.0.0.1"
    server_port = 8000

    # Sunucuya bağlan
    client.connect((server_ip, server_port))

    # SSL/TLS için SSLContext oluştur ve sunucu sertifikasının konumunu belirle
    ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    ssl_context.load_verify_locations("server_cert.pem")

    # Bağlantıyı güvenli hale getirerek SSL/TLS wrap işlemi gerçekleştir
    secure_client_socket = ssl_context.wrap_socket(client, server_hostname="localhost")

    try:
        while True:
            # Kullanıcıdan bir mesaj al
            msg = input("Mesajı girin: ")

            # Mesajı UTF-8 formatında kodla ve en fazla 1024 byte olarak gönder
            secure_client_socket.send(msg.encode("utf-8")[:1024])

            # Sunucudan gelen yanıtı al
            response = secure_client_socket.recv(1024)

            # Gelen yanıtı UTF-8 formatına çevir
            response = response.decode("utf-8")

            # Eğer sunucu "closed" mesajını gönderdiyse döngüyü sonlandır
            if response.lower() == "closed":
                break

            # Gelen yanıtı ekrana yazdır
            print(f"Alındı: {response}")
    except Exception as e:
        # Hata durumunda hata mesajını yazdır
        print(f"Hata: {e}")
    finally:
        # İstemci soketini kapat (sunucuyla olan bağlantıyı sonlandır)
        secure_client_socket.close()
        print("Sunucuyla bağlantı kapatıldı")


# İstemci kodunu çalıştır
run_client()
