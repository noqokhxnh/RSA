# Ứng dụng Chữ ký RSA

Đây là một ứng dụng minh họa việc tạo và xác minh chữ ký số sử dụng thuật toán RSA. Ứng dụng bao gồm cả phiên bản giao diện dòng lệnh và giao diện đồ họa.

## Tính năng

- Tạo khóa RSA (công khai và bí mật)
- Tạo chữ ký số cho thông điệp
- Xác minh tính hợp lệ của chữ ký
- Hỗ trợ nhập thông điệp dạng văn bản
- Tự động tạo giá trị băm cho thông điệp
- Giao diện đồ họa thân thiện với người dùng

## Yêu cầu hệ thống

- Python 3.x
- Thư viện tkinter (thường được cài đặt sẵn với Python)

## Cài đặt

1. Clone repository hoặc tải xuống các file nguồn   
      ```bash
      git clone https://github.com/noqokhxnh/RSA.git
      ```
2. Đảm bảo Python 3.x đã được cài đặt trên máy tính
3. Không cần cài đặt thêm thư viện bổ sung

## Cách sử dụng

### Phiên bản giao diện dòng lệnh (RSA.py)

```bash
python RSA.py
```

Chương trình sẽ yêu cầu nhập:
- Số nguyên tố p
- Số nguyên tố q
- Số e
- Thông điệp cần ký

### Phiên bản giao diện đồ họa (GUI.py)

```bash
python GUI.py
```

1. Nhập các thông số RSA:
   - Số nguyên tố p
   - Số nguyên tố q
   - Số e
   - Thông điệp cần ký
2. Nhấn nút "Tạo chữ ký"
3. Xem kết quả hiển thị ở phần dưới

## Ví dụ sử dụng

### Ví dụ 1:
```
p = 17
q = 23
e = 7
Thông điệp: "Hello RSA"
```

### Ví dụ 2:
```
p = 11
q = 13
e = 7
Thông điệp: "Test RSA"
```

## Lưu ý quan trọng

1. Các số p và q phải là số nguyên tố
2. Số e phải là số nguyên tố cùng nhau với (p-1)*(q-1)
3. Thông điệp có thể là bất kỳ văn bản nào
4. Chương trình tự động tạo giá trị băm cho thông điệp

## Cấu trúc project

- `RSA.py`: Chứa các hàm xử lý RSA và phiên bản giao diện dòng lệnh
- `GUI.py`: Chứa giao diện đồ họa sử dụng tkinter
- `README.md`: Tài liệu hướng dẫn sử dụng

## Giải thích thuật toán

1. Tạo khóa:
   - Tính n = p * q
   - Tính phi(n) = (p-1) * (q-1)
   - Chọn e sao cho gcd(e, phi(n)) = 1
   - Tính d = e^(-1) mod phi(n)

2. Tạo chữ ký:
   - Tạo giá trị băm H(M) của thông điệp
   - Tính S = H(M)^d mod n

3. Xác minh chữ ký:
   - Tính H(M)' = S^e mod n
   - So sánh H(M)' với H(M)

## Đóng góp

Mọi đóng góp đều được hoan nghênh. Vui lòng tạo issue hoặc pull request để đóng góp.

## Giấy phép

Project này được phân phối dưới giấy phép MIT. Xem file `LICENSE` để biết thêm chi tiết. 
