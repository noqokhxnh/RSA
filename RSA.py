import hashlib
import random
import math

def is_prime(n, k=5):
    """Kiểm tra tính nguyên tố của số n sử dụng thuật toán Miller-Rabin."""
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0:
        return False

    # Tìm r và d sao cho n-1 = 2^r * d
    r, d = 0, n - 1
    while d % 2 == 0:
        r += 1
        d //= 2

    # Thực hiện k lần kiểm tra
    for _ in range(k):
        a = random.randint(2, n - 2)
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True

def generate_prime(bits):
    """Tạo số nguyên tố ngẫu nhiên với số bit cho trước."""
    while True:
        # Tạo số ngẫu nhiên với số bit cho trước
        n = random.getrandbits(bits)
        # Đảm bảo số là lẻ
        n |= 1
        # Kiểm tra tính nguyên tố
        if is_prime(n):
            return n

def gcd(a, b):
    """Tính ước chung lớn nhất (GCD) bằng thuật toán Euclid."""
    if (b==0):
        return a
    else:
        return gcd(b,a%b)

def mod_inverse(e, phi):
    """Tìm nghịch đảo modulo của e theo phi bằng thuật toán Euclid mở rộng."""
    def extended_gcd(a, b):
        if a == 0:
            return b, 0, 1
        gcd, x1, y1 = extended_gcd(b % a, a)
        x = y1 - (b // a) * x1
        y = x1
        return gcd, x, y

    _, d, _ = extended_gcd(e, phi)
    # Đảm bảo d là số dương
    d = (d % phi + phi) % phi
    return d

def generate_keys(p=None, q=None, e=None, bits=512):
    """Tạo khóa công khai và khóa bí mật."""
    # Nếu không cung cấp p và q, tự động tạo
    if p is None or q is None:
        p = generate_prime(bits)
        q = generate_prime(bits)
    
    # Tính n = p * q
    n = p * q
    # Tính phi(n) = (p-1) * (q-1)
    phi = (p - 1) * (q - 1)
    
    # Nếu không cung cấp e, tìm e phù hợp
    if e is None:
        while True:
            e = random.randint(3, phi - 1)
            if gcd(e, phi) == 1:
                break
    
    # Kiểm tra e có hợp lệ
    if gcd(e, phi) != 1:
        raise ValueError("e không hợp lệ, phải là số nguyên tố cùng nhau với phi(n).")
    
    # Tính d (nghịch đảo modulo của e)
    d = mod_inverse(e, phi)
    return (e, n), (d, n)

def hash_message(message):
    """Tạo giá trị băm mật mã cho thông điệp sử dụng SHA-256."""
    if isinstance(message, str):
        # Xử lý chuỗi
        message = message.encode('utf-8')
    elif isinstance(message, bytes):
        # Đã là bytes
        pass
    else:
        # Chuyển đổi số thành bytes
        message = str(message).encode('utf-8')
    
    # Tạo băm SHA-256
    hash_obj = hashlib.sha256(message)
    # Chuyển đổi thành số nguyên
    return int.from_bytes(hash_obj.digest(), byteorder='big')

def sign_message(message, private_key):
    """Tạo chữ ký cho thông điệp bằng khóa bí mật."""
    d, n = private_key
    # Tạo giá trị băm
    hash_value = hash_message(message)
    # Đảm bảo giá trị băm nằm trong khoảng [0, n-1]
    hash_value = hash_value % n
    # Tạo chữ ký
    signature = pow(hash_value, d, n)
    return signature

def verify_signature(message, signature, public_key):
    """Xác minh chữ ký bằng khóa công khai."""
    e, n = public_key
    # Tạo giá trị băm
    hash_value = hash_message(message)
    # Đảm bảo giá trị băm nằm trong khoảng [0, n-1]
    hash_value = hash_value % n
    # Xác minh chữ ký
    verified_hash = pow(signature, e, n)
    return verified_hash == hash_value

def main():
    print("=== Hệ chữ ký RSA ===")
    
    try:
        # Tự động tạo p và q
        print("Đang tạo các số nguyên tố...")
        public_key, private_key = generate_keys()
        p, q = None, None  # Không hiển thị p và q vì lý do bảo mật
        
        # Nhập thông điệp
        original_message = input("Nhập thông điệp cần ký: ")
        hash_val = hash_message(original_message)
        
        print("\n=== Kết quả ===")
        print(f"Thông điệp gốc: {original_message}")
        print(f"Giá trị băm SHA-256: {hash_val}")

        print(f"\nKhóa công khai (e, n): {public_key}")
        print(f"Khóa bí mật (d, n): {private_key}")

        # Tạo chữ ký
        signature = sign_message(original_message, private_key)
        print(f"\nChữ ký: {signature}")

        # Xác minh chữ ký
        is_valid = verify_signature(original_message, signature, public_key)
        print(f"Xác minh chữ ký: {'Hợp lệ' if is_valid else 'Không hợp lệ'}")
        
    except ValueError as e:
        print(f"\nLỗi: {str(e)}")
    except Exception as e:
        print(f"\nĐã xảy ra lỗi không mong muốn: {str(e)}")

if __name__ == "__main__":
    main()