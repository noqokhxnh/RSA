import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from PIL import Image, ImageTk
import io
import base64
import threading
from RSA import generate_keys, sign_message, verify_signature, hash_message, is_prime

class RSAApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Ứng dụng Chữ ký RSA")
        self.public_key = None
        self.private_key = None
        self.signature = None
        self.selected_image = None
        
        # Thêm biến để theo dõi trạng thái tạo khóa
        self.is_generating_keys = False
        
        # Lấy kích thước màn hình
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        # Tính toán vị trí để căn giữa cửa sổ
        window_width = 1000
        window_height = 800
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        
        # Đặt kích thước và vị trí cửa sổ
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")
        self.root.configure(bg='#f0f0f0')
        
        # Tạo style
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("TFrame", background='#f0f0f0')
        style.configure("TLabel", padding=5, font=('Arial', 10), background='#f0f0f0')
        style.configure("TButton", padding=5, font=('Arial', 10))
        style.configure("TEntry", padding=5, font=('Arial', 10))
        
        # Cấu hình style cho các thành phần
        style.configure("Title.TLabel", 
                       font=('Arial', 14, 'bold'),
                       foreground='#2c3e50',
                       padding=10)
        
        style.configure("Header.TLabel",
                       font=('Arial', 11, 'bold'),
                       foreground='#34495e',
                       padding=5)
        
        style.configure("Result.TLabel",
                       font=('Arial', 10),
                       foreground='#2c3e50',
                       padding=5)
        
        style.configure("Input.TEntry",
                       font=('Arial', 10),
                       padding=5)
        
        style.configure("Message.TEntry",
                       font=('Arial', 10),
                       padding=5)
        
        style.configure('Accent.TButton',
                       font=('Arial', 11, 'bold'),
                       background='#3498db',
                       foreground='white',
                       padding=10)
        
        # Frame chính
        main_frame = ttk.Frame(root, padding="20")
        main_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        # Frame bên trái cho nhập liệu
        left_frame = ttk.Frame(main_frame, padding="10")
        left_frame.grid(row=0, column=0, padx=20, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Tiêu đề
        title_label = ttk.Label(left_frame, text="=== Thông số RSA ===", style="Title.TLabel")
        title_label.grid(row=0, column=0, columnspan=2, pady=10)
        
        # Nhập p
        ttk.Label(left_frame, text="Số nguyên tố p:", style="Header.TLabel").grid(row=1, column=0, sticky=tk.W)
        self.p_var = tk.StringVar()
        p_entry = ttk.Entry(left_frame, textvariable=self.p_var, width=30, style="Input.TEntry")
        p_entry.grid(row=1, column=1, pady=5, padx=5)
        
        # Nhập q
        ttk.Label(left_frame, text="Số nguyên tố q:", style="Header.TLabel").grid(row=2, column=0, sticky=tk.W)
        self.q_var = tk.StringVar()
        q_entry = ttk.Entry(left_frame, textvariable=self.q_var, width=30, style="Input.TEntry")
        q_entry.grid(row=2, column=1, pady=5, padx=5)
        
        # Nhập e
        ttk.Label(left_frame, text="Số e:", style="Header.TLabel").grid(row=3, column=0, sticky=tk.W)
        self.e_var = tk.StringVar()
        e_entry = ttk.Entry(left_frame, textvariable=self.e_var, width=30, style="Input.TEntry")
        e_entry.grid(row=3, column=1, pady=5, padx=5)
        
        # Frame cho thông điệp
        message_frame = ttk.LabelFrame(left_frame, text="Thông điệp", padding="10")
        message_frame.grid(row=4, column=0, columnspan=2, pady=10, sticky=(tk.W, tk.E))
        
        # Nhập thông điệp văn bản
        ttk.Label(message_frame, text="Văn bản:", style="Header.TLabel").grid(row=0, column=0, sticky=tk.W)
        self.message_var = tk.StringVar()
        message_entry = ttk.Entry(message_frame, textvariable=self.message_var, width=30, style="Message.TEntry")
        message_entry.grid(row=0, column=1, pady=5, padx=5)
        
        # Nút chọn hình ảnh
        ttk.Button(message_frame, text="Chọn hình ảnh", 
                  command=self.select_image,
                  style='Accent.TButton').grid(row=1, column=0, columnspan=2, pady=5)
        
        # Hiển thị hình ảnh đã chọn
        self.image_label = ttk.Label(message_frame)
        self.image_label.grid(row=2, column=0, columnspan=2, pady=5)
        
        # Nút tạo khóa
        ttk.Button(left_frame, text="Tạo khóa", 
                  command=self.create_keys,
                  style='Accent.TButton').grid(row=6, column=0, columnspan=2, pady=10)
        # Nút tạo chữ ký
        ttk.Button(left_frame, text="Tạo chữ ký", 
                  command=self.generate_signature,
                  style='Accent.TButton').grid(row=7, column=0, columnspan=2, pady=10)
        # Nút xác minh chữ ký
        ttk.Button(left_frame, text="Xác minh chữ ký", 
                  command=self.verify_signature_gui,
                  style='Accent.TButton').grid(row=8, column=0, columnspan=2, pady=10)
        
        # Frame bên phải cho kết quả
        right_frame = ttk.Frame(main_frame, padding="10")
        right_frame.grid(row=0, column=1, padx=20, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Tiêu đề kết quả
        result_title = ttk.Label(right_frame, text="=== Kết quả ===", style="Title.TLabel")
        result_title.grid(row=0, column=0, columnspan=2, pady=10)
        
        # Khóa công khai
        ttk.Label(right_frame, text="Khóa công khai (e, n):", style="Header.TLabel").grid(row=1, column=0, sticky=tk.W)
        self.public_key_var = tk.StringVar()
        ttk.Label(right_frame, textvariable=self.public_key_var, style="Result.TLabel", wraplength=600, justify='left').grid(row=1, column=1, sticky=tk.W, padx=5)
        
        # Khóa bí mật
        ttk.Label(right_frame, text="Khóa bí mật (d, n):", style="Header.TLabel").grid(row=2, column=0, sticky=tk.W)
        self.private_key_var = tk.StringVar()
        ttk.Label(right_frame, textvariable=self.private_key_var, style="Result.TLabel", wraplength=600, justify='left').grid(row=2, column=1, sticky=tk.W, padx=5)
        
        # Chữ ký
        ttk.Label(right_frame, text="Chữ ký:", style="Header.TLabel").grid(row=3, column=0, sticky=tk.W)
        self.signature_var = tk.StringVar()
        ttk.Label(right_frame, textvariable=self.signature_var, style="Result.TLabel", wraplength=600, justify='left').grid(row=3, column=1, sticky=tk.W, padx=5)
        
        # Xác minh
        ttk.Label(right_frame, text="Xác minh chữ ký:", style="Header.TLabel").grid(row=4, column=0, sticky=tk.W)
        self.verify_var = tk.StringVar()
        ttk.Label(right_frame, textvariable=self.verify_var, style="Result.TLabel").grid(row=4, column=1, sticky=tk.W, padx=5)
        
        # Giá trị băm
        ttk.Label(right_frame, text="Giá trị băm SHA-256:", style="Header.TLabel").grid(row=5, column=0, sticky=tk.W)
        self.hash_var = tk.StringVar()
        ttk.Label(right_frame, textvariable=self.hash_var, style="Result.TLabel", wraplength=600, justify='left').grid(row=5, column=1, sticky=tk.W, padx=5)
        
        # Căn giữa tất cả các thành phần
        for child in main_frame.winfo_children():
            child.grid_configure(padx=10, pady=5)
            
        # Căn giữa các label trong message_frame
        for child in message_frame.winfo_children():
            child.grid_configure(padx=5, pady=5)
            
        # Căn giữa văn bản trong các entry
        for entry in [p_entry, q_entry, e_entry, message_entry]:
            entry.configure(justify='center')

    def update_status(self, message):
        """Cập nhật trạng thái trên giao diện."""
        self.status_label.configure(text=message)
        self.root.update()

    def generate_keys_thread(self):
        """Hàm tạo khóa trong luồng riêng."""
        try:
            self.update_status("Đang tạo khóa...")
            public_key, private_key = generate_keys()
            
            # Lưu khóa dưới dạng tuple
            self.public_key = public_key
            self.private_key = private_key
            
            # Hiển thị khóa trong giao diện
            self.public_key_var.set(f"({public_key[0]}, {public_key[1]})")
            self.private_key_var.set(f"({private_key[0]}, {private_key[1]})")
            
            self.update_status("Đã tạo khóa thành công!")
            messagebox.showinfo("Thành công", "Đã tạo khóa tự động!")
        except Exception as e:
            self.update_status("Lỗi khi tạo khóa!")
            messagebox.showerror("Lỗi", f"Không thể tạo khóa: {str(e)}")
        finally:
            self.is_generating_keys = False
            self.generate_keys_button.configure(state='normal')

    def generate_auto_keys(self):
        """Tạo khóa tự động trong luồng riêng."""
        if self.is_generating_keys:
            return
            
        self.is_generating_keys = True
        self.generate_keys_button.configure(state='disabled')
        threading.Thread(target=self.generate_keys_thread, daemon=True).start()

    def select_image(self):
        """Chọn và hiển thị hình ảnh."""
        file_path = filedialog.askopenfilename(
            filetypes=[("Image files", "*.png *.jpg *.jpeg *.gif *.bmp")]
        )
        if file_path:
            try:
                # Đọc và resize hình ảnh
                image = Image.open(file_path)
                image = image.resize((200, 200), Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(image)
                
                # Hiển thị hình ảnh
                self.image_label.configure(image=photo)
                self.image_label.image = photo
                
                # Lưu hình ảnh đã chọn
                self.selected_image = image
                
            except Exception as e:
                messagebox.showerror("Lỗi", f"Không thể mở hình ảnh: {str(e)}")

    def image_to_hash(self, image):
        """Chuyển đổi hình ảnh thành giá trị băm."""
        try:
            # Chuyển đổi hình ảnh thành bytes
            img_byte_arr = io.BytesIO()
            image.save(img_byte_arr, format='PNG')
            img_byte_arr = img_byte_arr.getvalue()
            
            # Tạo giá trị băm từ bytes của hình ảnh
            return hash_message(img_byte_arr)
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể xử lý hình ảnh: {str(e)}")
            return None

    def create_keys(self):
        try:
            p = int(self.p_var.get())
            q = int(self.q_var.get())
            e = int(self.e_var.get())
            if not is_prime(p) or not is_prime(q):
                messagebox.showerror("Lỗi", "p và q phải là số nguyên tố!")
                return
            if p == q:
                messagebox.showerror("Lỗi", "p và q phải khác nhau!")
                return
            public_key, private_key = generate_keys(p, q, e)
            self.public_key = public_key
            self.private_key = private_key
            self.public_key_var.set(f"({public_key[0]}, {public_key[1]})")
            self.private_key_var.set(f"({private_key[0]}, {private_key[1]})")
            self.signature_var.set("")
            self.verify_var.set("")
            self.hash_var.set("")
            messagebox.showinfo("Thành công", "Đã tạo khóa thành công!")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể tạo khóa: {str(e)}")

    def generate_signature(self):
        try:
            if not self.public_key or not self.private_key:
                messagebox.showwarning("Cảnh báo", "Vui lòng tạo khóa trước!")
                return
            if self.selected_image:
                img_byte_arr = io.BytesIO()
                self.selected_image.save(img_byte_arr, format='PNG')
                original_message = img_byte_arr.getvalue()
                hash_value = hash_message(original_message)
            else:
                original_message = self.message_var.get()
                if not original_message:
                    messagebox.showwarning("Cảnh báo", "Vui lòng nhập thông điệp hoặc chọn hình ảnh")
                    return
                hash_value = hash_message(original_message)
            self.hash_var.set(str(hash_value))
            self.signature = sign_message(original_message, self.private_key)
            self.signature_var.set(str(self.signature))
            self.verify_var.set("")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể tạo chữ ký: {str(e)}")

    def verify_signature_gui(self):
        try:
            if not self.public_key or not self.signature:
                messagebox.showwarning("Cảnh báo", "Vui lòng tạo khóa và chữ ký trước!")
                return
            if self.selected_image:
                img_byte_arr = io.BytesIO()
                self.selected_image.save(img_byte_arr, format='PNG')
                original_message = img_byte_arr.getvalue()
            else:
                original_message = self.message_var.get()
                if not original_message:
                    messagebox.showwarning("Cảnh báo", "Vui lòng nhập thông điệp hoặc chọn hình ảnh")
                    return
            is_valid = verify_signature(original_message, self.signature, self.public_key)
            self.verify_var.set("Hợp lệ" if is_valid else "Không hợp lệ")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể xác minh chữ ký: {str(e)}")

def main():
    root = tk.Tk()
    app = RSAApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
