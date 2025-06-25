import hashlib
from flask import Flask, request, jsonify
from flask_cors import CORS
import sympy

app = Flask(__name__)
CORS(app)

def is_prime(n):
    return sympy.isprime(n)

# Hàm tính ước chung lớn nhất (GCD) của hai số a và b
def gcd(a, b):
    if b == 0:
        return a
    return gcd(b, a % b)

# Hàm tính nghịch đảo modulo của e theo modulo phi
def mod_inverse(e, phi):
    m0, x0, x1 = phi, 0, 1
    if phi == 0:
        return None
    while e > 1:
        if phi == 0:
            return None  # Tránh chia cho 0
        q = e // phi
        e, phi = phi, e % phi
        x0, x1 = x1 - q * x0, x0
    return x1 + m0 if x1 < 0 else x1


# Kiểm tra p, q là số nguyên tố, e hợp lệ, tính n, phi(n), d
# Nếu hợp lệ trả về bộ khóa, nếu không trả về lỗi
def generate_keys(p, q, e):
    if not (is_prime(p) and is_prime(q)):
        return None, None, 'p hoặc q không phải là số nguyên tố!'
    n = p * q
    phi = (p - 1) * (q - 1)
    if gcd(e, phi) != 1:
        return None, None, 'e không hợp lệ! Phải nguyên tố cùng nhau với phi(n).'
    d = mod_inverse(e, phi)
    if d is None:
        return None, None, 'Không tìm được nghịch đảo modular cho e theo phi(n)!'
    # Ẩn thông tin nhạy cảm, chỉ log khi ở chế độ debug
    import os
    if os.environ.get('FLASK_ENV') == 'development' or app.debug:
        print(f"Generated keys: e={e}, n={n}, d={d}, phi={phi}")
    return (e, n), (d, n), None

# Hàm ký nội dung tệp
# Quy trình:
#    Băm nội dung bằng SHA-256
#    Lấy giá trị băm mod n để đảm bảo nhỏ hơn n
#    Tính chữ ký: signature = (hash_mod_n ^ d) mod n
# Trả về chữ ký
def sign_file_content(content, private_key):
    d, n = private_key
    hash_value = int(hashlib.sha256(content.encode('utf-8')).hexdigest(), 16)
    hash_mod_n = hash_value % n
    print(f"Hash value: {hash_value}, Hash mod n: {hash_mod_n}")
    signature = pow(hash_mod_n, d, n)
    return signature, None

# Hàm xác minh chữ ký số của tệp (hoặc thông điệp)
# Quy trình:
#   - Băm lại nội dung bằng SHA-256, lấy mod n
#   - Giải mã chữ ký: decrypted_hash = (signature ^ e) mod n
#   - So sánh decrypted_hash với hash_mod_n
#   - Nếu trùng khớp, chữ ký hợp lệ
def verify_file_signature(content, signature, public_key):
    e, n = public_key
    hash_value = int(hashlib.sha256(content.encode('utf-8')).hexdigest(), 16)
    hash_mod_n = hash_value % n
    decrypted_hash = pow(signature, e, n)
    print(f"Hash mod n: {hash_mod_n}, Decrypted hash: {decrypted_hash}")
    return decrypted_hash == hash_mod_n, None

# API endpoint: Sinh khóa RSA
# Nhận POST với p, q, e (dưới dạng JSON)
# Trả về public_key, private_key hoặc lỗi
@app.route('/generate_keys', methods=['POST'])
def api_generate_keys():
    data = request.json
    try:
        p = int(data['p'])
        q = int(data['q'])
        e = int(data['e'])
    except Exception:
        return jsonify({'error': 'Dữ liệu đầu vào không hợp lệ!'}), 400
    public_key, private_key, err = generate_keys(p, q, e)
    if err:
        return jsonify({'error': err}), 400
    return jsonify({'public_key': public_key, 'private_key': private_key})

# API endpoint: Ký thông điệp hoặc file
# Nhận POST với message (nội dung), private_key (d, n)
# Trả về signature hoặc lỗi
@app.route('/sign_message', methods=['POST'])
def api_sign_message():
    data = request.json
    try:
        message = data['message']
        private_key = tuple(map(int, data['private_key']))
    except Exception:
        return jsonify({'error': 'Dữ liệu đầu vào không hợp lệ!'}), 400
    signature, err = sign_file_content(message, private_key)
    if err:
        return jsonify({'error': err}), 400
    return jsonify({'signature': signature})

# API endpoint: Xác minh chữ ký số
# Nhận POST với message (nội dung), signature (chữ ký), public_key (e, n)
# Trả về is_valid (True/False) hoặc lỗi
@app.route('/verify_signature', methods=['POST'])
def api_verify_signature():
    data = request.json
    try:
        message = data['message']
        signature = int(data['signature'])
        public_key = tuple(map(int, data['public_key']))
    except Exception:
        return jsonify({'error': 'Dữ liệu đầu vào không hợp lệ!'}), 400
    is_valid, err = verify_file_signature(message, signature, public_key)
    if err:
        return jsonify({'error': err}), 400
    return jsonify({'is_valid': is_valid})

# Chạy server Flask ở chế độ debug
if __name__ == '__main__':
    app.run(debug=True)
    
    