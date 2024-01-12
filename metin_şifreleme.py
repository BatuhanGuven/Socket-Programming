
import sympy as sp
import random
import sympy

def string_to_int(message):
    # Her karakterin ASCII değerini alarak bir sayı dizisine dönüştürme
    return [ord(char) for char in message]

def int_to_string(numbers):
    # Her sayıyı ASCII karakterine dönüştürme
    return ''.join([chr(num) for num in numbers])
def add_points(p, q, curve):
    # Toplama işlemi: P + Q
    if p == (float('inf'), float('inf')):
        return q
    if q == (float('inf'), float('inf')):
        return p

    x_p, y_p = p
    x_q, y_q = q

    if p != q:
        # P ve Q farklı noktalarsa
        slope = (y_q - y_p) / (x_q - x_p)
        x_r = slope**2 - x_p - x_q
        y_r = slope * (x_p - x_r) - y_p
    else:
        # P ve Q aynı noktadaysa
        slope = (3 * x_p**2) / (2 * y_p)
        x_r = slope**2 - 2 * x_p
        y_r = slope * (x_p - x_r) - y_p

    return (x_r, y_r)
        
def multiply_point(scalar, point, curve):
    # Skalar ile noktanın çarpımı: k * P
    result = (float('inf'), float('inf'))
    for _ in range(scalar.bit_length()):
        if (scalar >> _) & 1:
            result = add_points(result, point, curve)
        point = add_points(point, point, curve)
    return result
def ellipticCurve_points(p, a, b):
    points = []
    for x in range(p):
        w = (x**3 + a*x + b) % p
        sqrt_w = square_root_mod(w, p)
        if sqrt_w is not None:
            points.append((x, sqrt_w))
            points.append((x, p - sqrt_w))
    return points

def square_root_mod(n, p):
    # Karekök mod p hesaplama
    for i in range(1, p):
        if (i * i) % p == n:
            return i
    return None

# Örnek kullanım
p = 17
message = "selam"
plaintext = string_to_int(message)

# Şifreleme için kullanılan özel anahtar
private_key = 271
a = -3
b = 5
x, y = sp.symbols('x y')
curve = sp.Eq(y**2, x**3 + a*x + b)
generator = (1481, 3248363203) # Sabit başlangıç noktası
public_key = multiply_point(private_key, generator, curve)
# Rastgele bir sayı
# Şifreleme

def encrypte(mesaj):
    plaintext = string_to_int(mesaj)
    ciphertext = []
    for char_code in plaintext:
        k = 5
        C1 = multiply_point(k, generator, curve)  # C1=k×generator. (x1,y1)
        C2 = add_points((char_code, 0), multiply_point(k, public_key, curve), curve) # Mesajı göndermek istediği kullanıcının açık anahtarını kullanır.
        ciphertext.append((C1, C2))
    return ciphertext
def decrypte(ciphertext):
    decrypted_text = ""
    for C1, C2 in ciphertext:
        shared_secret = multiply_point(private_key, C1, curve)## x2,y2 noktası bulunur
        decrypted_char = int(add_points(C2, (shared_secret[0], -shared_secret[1]), curve)[0])
        decrypted_text += chr(decrypted_char)
    return decrypted_text


result = ellipticCurve_points(p, a, b)

