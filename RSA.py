def gcd(a, b):
    """Tính ước chung lớn nhất (GCD) bằng thuật toán Euclid."""
    while b:
        a, b = b, a % b
    return a

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

def generate_keys(p, q, e):
    """Tạo khóa công khai và khóa bí mật."""
    # Tính n = p * q
    n = p * q
    # Tính phi(n) = (p-1) * (q-1)
    phi = (p - 1) * (q - 1)
    # Kiểm tra e có hợp lệ (coprime với phi)
    if gcd(e, phi) != 1:
        raise ValueError("e không hợp lệ, phải là số nguyên tố cùng nhau với phi(n).")
    # Tính d (nghịch đảo modulo của e)
    d = mod_inverse(e, phi)
    return (e, n), (d, n)

def sign_message(message, private_key):
    """Tạo chữ ký cho thông điệp bằng khóa bí mật."""
    d, n = private_key
    # Chữ ký: S = message^d mod n
    signature = pow(message, d, n)
    return signature

def verify_signature(message, signature, public_key):
    """Xác minh chữ ký bằng khóa công khai."""
    e, n = public_key
    # Tính message' = signature^e mod n
    verified_message = pow(signature, e, n)
    return verified_message == message

def hash_message(message):
    """Tạo giá trị băm đơn giản cho thông điệp."""
    hash_value = 0
    for char in message:
        hash_value = (hash_value * 31 + ord(char)) % 1000  # Giới hạn giá trị băm trong khoảng 0-999
    return hash_value

def main():
    print("=== Hệ chữ ký RSA ===")
    
    # Nhập các thông số
    try:
        p = int(input("Nhập số nguyên tố p: "))
        q = int(input("Nhập số nguyên tố q: "))
        e = int(input("Nhập số e (phải là số nguyên tố cùng nhau với (p-1)*(q-1)): "))
        
        # Nhập thông điệp gốc
        original_message = input("Nhập thông điệp cần ký: ")
        message = hash_message(original_message)
        
        # Kiểm tra tính hợp lệ của p và q
        if p <= 1 or q <= 1:
            raise ValueError("p và q phải là số nguyên tố lớn hơn 1")
            
        print("\n=== Kết quả ===")
        print(f"Thông số: p = {p}, q = {q}, e = {e}")
        print(f"Thông điệp gốc: {original_message}")
        print(f"Giá trị băm H(M): {message}")

        # Tạo khóa
        public_key, private_key = generate_keys(p, q, e)
        print(f"\nKhóa công khai (e, n): {public_key}")
        print(f"Khóa bí mật (d, n): {private_key}")

        # Tạo chữ ký
        signature = sign_message(message, private_key)
        print(f"\nChữ ký (S = H(M)^d mod n): {signature}")

        # Xác minh chữ ký
        is_valid = verify_signature(message, signature, public_key)
        print(f"Xác minh chữ ký: {'Hợp lệ' if is_valid else 'Không hợp lệ'}")
        print(f"Thông điệp gốc: {original_message}")
        print(f"Giá trị băm H(M): {message}")
        
    except ValueError as e:
        print(f"\nLỗi: {str(e)}")
    except Exception as e:
        print(f"\nĐã xảy ra lỗi không mong muốn: {str(e)}")

if __name__ == "__main__":
    main()