import socket
import ssl
def run_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) ##Burada, socket.socket metodu kullanılarak yeni bir TCP soketi oluşturulur. AF_INET, IPv4'ü ve SOCK_STREAM, bir TCP soketini gösterir.
    server_ip = "127.0.0.1"
    port = 8000
    server.bind((server_ip, port)) ##Sunucu IP adresi "127.0.0.1" (localhost) olarak ayarlanır ve port 8000 olarak belirlenir. bind metodu, soketi belirtilen IP adresi ve port ile ilişkilendirir.
    server.listen(0)##listen metodu, sunucunun gelen bağlantıları dinlemeye başlamasını sağlar. Bu argüman (bu durumda 0), kuyruğa alınabilecek maksimum bağlantı sayısını belirtir. Burada 0 olarak ayarlandığından, istenilen sayıda bağlantı kuyruğa alınabilir.
    print(f"Listening on {server_ip}:{port}")
    client_socket, client_address = server.accept() ##İstemciden bir bağlantı kabul eder. Bu, istemcinin bağlanmasını bekleyen, bloklanan bir çağrıdır. client_socket, bağlantıyı temsil eden yeni bir soket nesnesidir ve client_address, istemcinin adresidir.
    print(f"Accepted connection from {client_address[0]}:{client_address[1]}")
    ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    ssl_context.load_cert_chain("server_cert.pem", "server_key.pem") ## Bu kısımda, SSL/TLS ile güvenli iletişimi sağlamak için SSLContext oluşturulur ve sunucu sertifikası ile özel anahtar yüklenir. server_cert.pem ve server_key.pem dosyaları, sunucu sertifikası ve özel anahtar dosyalarını içermelidir.

    secure_client_socket = ssl_context.wrap_socket(client_socket, True) ## Bağlantıyı güvenli hale getirmek için wrap_socket metodu kullanılır. True parametresi, sunucu tarafında bu güvenli bağlantının oluşturulmasını temsil eder.

    while True:
        request = secure_client_socket.recv(1024) ## Sonsuz bir döngü içinde, güvenli bağlantıdan gelen veriyi alır. Burada recv metodu kullanılarak en fazla 1024 byte alınır ve bu veri UTF-8 formatında çözümlenir.
        request = request.decode("utf-8")

        if request.lower() == "close": ## Gelen veri "close" ise, bağlantıyı kapatma isteği olduğunu belirtir. "closed" mesajını istemciye gönderir ve döngüyü kırar.
            secure_client_socket.send("closed".encode("utf-8"))
            break

        print(f"Received: {request}") ## Eğer "close" değilse, gelen veriyi ekrana yazdırır, "accepted" mesajını oluşturur ve istemciye gönderir.
        response = "accepted".encode("utf-8")
        secure_client_socket.send(response)

    secure_client_socket.close() ## Döngüden çıkıldığında, güvenli bağlantıyı kapatır, istemciye kapatıldığına dair bir mesaj gönderir ve ardından sunucu soketini kapatır.
    print("Connection to client closed")
    server.close()

run_server()