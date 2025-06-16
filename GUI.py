import tkinter as tk
from tkinter import ttk, messagebox
from RSA import generate_keys, sign_message, verify_signature, hash_message

class RSAApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Ứng dụng Chữ ký RSA")
        self.root.geometry("800x600")
        
        # Tạo style
        style = ttk.Style()
        style.configure("TLabel", padding=5, font=('Arial', 10))
        style.configure("TButton", padding=5, font=('Arial', 10))
        style.configure("TEntry", padding=5, font=('Arial', 10))
        
        # Frame chính
        main_frame = ttk.Frame(root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Phần nhập thông số
        ttk.Label(main_frame, text="=== Thông số RSA ===", font=('Arial', 12, 'bold')).grid(row=0, column=0, columnspan=2, pady=10)
        
        # Nhập p
        ttk.Label(main_frame, text="Số nguyên tố p:").grid(row=1, column=0, sticky=tk.W)
        self.p_var = tk.StringVar()
        ttk.Entry(main_frame, textvariable=self.p_var, width=30).grid(row=1, column=1, pady=5)
        
        # Nhập q
        ttk.Label(main_frame, text="Số nguyên tố q:").grid(row=2, column=0, sticky=tk.W)
        self.q_var = tk.StringVar()
        ttk.Entry(main_frame, textvariable=self.q_var, width=30).grid(row=2, column=1, pady=5)
        
        # Nhập e
        ttk.Label(main_frame, text="Số e:").grid(row=3, column=0, sticky=tk.W)
        self.e_var = tk.StringVar()
        ttk.Entry(main_frame, textvariable=self.e_var, width=30).grid(row=3, column=1, pady=5)
        
        # Nhập thông điệp
        ttk.Label(main_frame, text="Thông điệp:").grid(row=4, column=0, sticky=tk.W)
        self.message_var = tk.StringVar()
        ttk.Entry(main_frame, textvariable=self.message_var, width=30).grid(row=4, column=1, pady=5)
        
        # Nút thực hiện
        ttk.Button(main_frame, text="Tạo chữ ký", command=self.generate_signature).grid(row=5, column=0, columnspan=2, pady=20)
        
        # Kết quả
        ttk.Label(main_frame, text="=== Kết quả ===", font=('Arial', 12, 'bold')).grid(row=6, column=0, columnspan=2, pady=10)
        
        # Khóa công khai
        ttk.Label(main_frame, text="Khóa công khai (e, n):").grid(row=7, column=0, sticky=tk.W)
        self.public_key_var = tk.StringVar()
        ttk.Label(main_frame, textvariable=self.public_key_var).grid(row=7, column=1, sticky=tk.W)
        
        # Khóa bí mật
        ttk.Label(main_frame, text="Khóa bí mật (d, n):").grid(row=8, column=0, sticky=tk.W)
        self.private_key_var = tk.StringVar()
        ttk.Label(main_frame, textvariable=self.private_key_var).grid(row=8, column=1, sticky=tk.W)
        
        # Chữ ký
        ttk.Label(main_frame, text="Chữ ký:").grid(row=9, column=0, sticky=tk.W)
        self.signature_var = tk.StringVar()
        ttk.Label(main_frame, textvariable=self.signature_var).grid(row=9, column=1, sticky=tk.W)
        
        # Xác minh
        ttk.Label(main_frame, text="Xác minh chữ ký:").grid(row=10, column=0, sticky=tk.W)
        self.verify_var = tk.StringVar()
        ttk.Label(main_frame, textvariable=self.verify_var).grid(row=10, column=1, sticky=tk.W)
        
        # Giá trị băm
        ttk.Label(main_frame, text="Giá trị băm H(M):").grid(row=11, column=0, sticky=tk.W)
        self.hash_var = tk.StringVar()
        ttk.Label(main_frame, textvariable=self.hash_var).grid(row=11, column=1, sticky=tk.W)

    def generate_signature(self):
        try:
            # Lấy giá trị từ giao diện
            p = int(self.p_var.get())
            q = int(self.q_var.get())
            e = int(self.e_var.get())
            message = self.message_var.get()
            
            # Kiểm tra tính hợp lệ
            if p <= 1 or q <= 1:
                raise ValueError("p và q phải là số nguyên tố lớn hơn 1")
            
            # Tạo khóa
            public_key, private_key = generate_keys(p, q, e)
            self.public_key_var.set(str(public_key))
            self.private_key_var.set(str(private_key))
            
            # Tạo giá trị băm và chữ ký
            hash_value = hash_message(message)
            self.hash_var.set(str(hash_value))
            
            signature = sign_message(hash_value, private_key)
            self.signature_var.set(str(signature))
            
            # Xác minh chữ ký
            is_valid = verify_signature(hash_value, signature, public_key)
            self.verify_var.set("Hợp lệ" if is_valid else "Không hợp lệ")
            
        except ValueError as e:
            messagebox.showerror("Lỗi", str(e))
        except Exception as e:
            messagebox.showerror("Lỗi", f"Đã xảy ra lỗi không mong muốn: {str(e)}")

def main():
    root = tk.Tk()
    app = RSAApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
