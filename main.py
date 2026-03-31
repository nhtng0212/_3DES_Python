import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import time
import os

import _3DES


class CipherShiftApp:
    def __init__(self, root):
        self.root = root
        self.root.title("CipherShift: 3DES Crypto Tool - Nhóm 18")
        self.root.geometry("1050x650")

        # Biến toàn cục
        self.filepath = ""
        self.file_name_only = ""
        self.input_data = b""
        self.output_data = b""
        self.current_action = ""
        self.show_key_var = tk.BooleanVar(value=False)

        # Cấu hình Style
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("Sidebar.TFrame", background="#2c3e50")
        style.configure("Title.TLabel", background="#2c3e50", foreground="#ecf0f1", font=("Segoe UI", 14, "bold"))
        style.configure("WhiteText.TLabel", background="#2c3e50", foreground="white", font=("Segoe UI", 10))
        style.configure("Action.TButton", font=("Segoe UI", 10, "bold"), padding=5)

        # --- BỐ CỤC CHÍNH ---
        # Sidebar bên trái
        self.sidebar = ttk.Frame(root, width=250, style="Sidebar.TFrame")
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        # Main Content bên phải
        self.main_area = ttk.Frame(root, padding=10)
        self.main_area.pack(side="right", fill="both", expand=True)

        self._build_sidebar()
        self._build_main_area()

        self.log_message("Khởi động hệ thống CipherShift (Phiên bản 3DES) thành công.")
        self.log_message("Sẵn sàng xử lý file...")

    def _build_sidebar(self):
        # Tiêu đề
        ttk.Label(self.sidebar, text="⚙️ BẢNG ĐIỀU KHIỂN", style="Title.TLabel").pack(pady=(20, 10))
        ttk.Separator(self.sidebar, orient="horizontal").pack(fill="x", padx=10, pady=10)

        # Chọn File
        ttk.Button(self.sidebar, text="📁 Mở File Cần Xử Lý", command=self.load_file, style="Action.TButton").pack(
            fill="x", padx=15, pady=5)
        self.lbl_filename = ttk.Label(self.sidebar, text="<Chưa chọn file>", foreground="#bdc3c7", background="#2c3e50",
                                      wraplength=220)
        self.lbl_filename.pack(pady=(0, 15))

        # Nhập Khóa (Đã sửa đổi cho 3DES: Max 24 ký tự)
        ttk.Label(self.sidebar, text="🔑 Khóa Bí Mật (Max 24):", style="WhiteText.TLabel").pack(anchor="w", padx=15)
        self.entry_key = ttk.Entry(self.sidebar, show="*", font=("Consolas", 11))
        self.entry_key.pack(fill="x", padx=15, pady=5)

        ttk.Checkbutton(self.sidebar, text="Hiển thị khóa", variable=self.show_key_var, command=self.toggle_key_view,
                        style="WhiteText.TCheckbutton").pack(anchor="w", padx=15, pady=5)

        ttk.Separator(self.sidebar, orient="horizontal").pack(fill="x", padx=10, pady=15)

        # Các Nút Chức Năng Chính
        self.btn_enc = tk.Button(self.sidebar, text="🔒 MÃ HÓA (ENCRYPT)", bg="#e74c3c", fg="white",
                                 font=("Segoe UI", 10, "bold"), relief="flat", command=self.process_encryption)
        self.btn_enc.pack(fill="x", padx=15, pady=5, ipady=5)

        self.btn_dec = tk.Button(self.sidebar, text="🔓 GIẢI MÃ (DECRYPT)", bg="#2980b9", fg="white",
                                 font=("Segoe UI", 10, "bold"), relief="flat", command=self.process_decryption)
        self.btn_dec.pack(fill="x", padx=15, pady=5, ipady=5)

        ttk.Separator(self.sidebar, orient="horizontal").pack(fill="x", padx=10, pady=15)

        self.btn_save = tk.Button(self.sidebar, text="💾 LƯU KẾT QUẢ", bg="#27ae60", fg="white",
                                  font=("Segoe UI", 10, "bold"), relief="flat", state="disabled",
                                  command=self.save_output)
        self.btn_save.pack(fill="x", padx=15, pady=5, ipady=5)

    def _build_main_area(self):
        # Tabs system
        self.notebook = ttk.Notebook(self.main_area)
        self.notebook.pack(fill="both", expand=True)

        # TAB 1: Giao diện dữ liệu
        self.tab_data = ttk.Frame(self.notebook, padding=5)
        self.notebook.add(self.tab_data, text="📝 Trình xem Dữ liệu")

        # Khung Input
        frame_in = ttk.LabelFrame(self.tab_data, text=" Nội dung Input ", padding=5)
        frame_in.pack(fill="both", expand=True, pady=(0, 5))

        toolbar_in = ttk.Frame(frame_in)
        toolbar_in.pack(fill="x", pady=2)
        ttk.Label(toolbar_in, text="Định dạng hiển thị:").pack(side="left")
        self.cbo_in_mode = ttk.Combobox(toolbar_in, values=["Text", "Hex", "Binary"], state="readonly", width=10)
        self.cbo_in_mode.current(0)
        self.cbo_in_mode.pack(side="left", padx=5)
        self.cbo_in_mode.bind("<<ComboboxSelected>>", lambda e: self.update_view("in"))

        self.txt_input = tk.Text(frame_in, wrap="word", font=("Consolas", 10), bg="#fdfdfd")
        self.txt_input.pack(fill="both", expand=True)

        # Khung Output
        frame_out = ttk.LabelFrame(self.tab_data, text=" Nội dung Output ", padding=5)
        frame_out.pack(fill="both", expand=True, pady=(5, 0))

        toolbar_out = ttk.Frame(frame_out)
        toolbar_out.pack(fill="x", pady=2)
        ttk.Label(toolbar_out, text="Định dạng hiển thị:").pack(side="left")
        self.cbo_out_mode = ttk.Combobox(toolbar_out, values=["Text", "Hex", "Binary"], state="readonly", width=10)
        self.cbo_out_mode.current(1)
        self.cbo_out_mode.pack(side="left", padx=5)
        self.cbo_out_mode.bind("<<ComboboxSelected>>", lambda e: self.update_view("out"))

        self.txt_output = tk.Text(frame_out, wrap="word", font=("Consolas", 10), bg="#eaeff1")
        self.txt_output.pack(fill="both", expand=True)

        # TAB 2: Log Terminal
        self.tab_log = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_log, text="🖥️ Terminal Log")

        self.sys_log = tk.Text(self.tab_log, bg="#1e1e1e", fg="#00ff00", font=("Consolas", 11), padx=10, pady=10)
        self.sys_log.pack(fill="both", expand=True)

    # --- CÁC HÀM TIỆN ÍCH ---
    def log_message(self, msg):
        self.sys_log.insert(tk.END, f"[>>] {msg}\n")
        self.sys_log.see(tk.END)

    def toggle_key_view(self):
        if self.show_key_var.get():
            self.entry_key.config(show="")
        else:
            self.entry_key.config(show="*")

    def _convert_bytes_to_string(self, raw_bytes, mode):
        if not raw_bytes:
            return ""

        display_limit = 2000
        preview_data = raw_bytes[:display_limit]

        if mode == "Text":
            try:
                result = raw_bytes.decode("utf-8")
                return result if len(result) < 5000 else result[:5000] + "\n...[Dữ liệu quá dài đã bị cắt bớt]..."
            except UnicodeDecodeError:
                return "[CẢNH BÁO] Không thể hiển thị nội dung này dưới dạng văn bản (Vui lòng chuyển sang Hex/Binary)."

        elif mode == "Hex":
            hex_data = preview_data.hex().upper()
            result = " ".join(hex_data[i:i + 2] for i in range(0, len(hex_data), 2))
            if len(raw_bytes) > display_limit:
                result += "\n...[Dữ liệu quá dài đã bị cắt bớt]..."
            return result

        elif mode == "Binary":
            result = " ".join(f"{b:08b}" for b in preview_data[:500])
            if len(raw_bytes) > 500:
                result += "\n...[Dữ liệu quá dài đã bị cắt bớt]..."
            return result

    def update_view(self, target):
        if target == "in":
            self.txt_input.delete(1.0, tk.END)
            self.txt_input.insert(tk.END, self._convert_bytes_to_string(self.input_data, self.cbo_in_mode.get()))
        else:
            self.txt_output.config(state="normal")
            self.txt_output.delete(1.0, tk.END)
            self.txt_output.insert(tk.END, self._convert_bytes_to_string(self.output_data, self.cbo_out_mode.get()))

    def get_valid_key(self):
        user_key = self.entry_key.get()
        if not user_key:
            messagebox.showwarning("Thiếu thông tin", "Khóa bí mật không được để trống!")
            return None
        # 3DES yêu cầu khóa 24 byte
        return user_key.encode("utf-8").ljust(24, b"\0")[:24]

    def _prepare_3des_subkeys(self, key_24):
        """Hàm phụ trợ chia khóa 24 byte thành 3 khóa con và sinh subkeys"""
        k1, k2, k3 = key_24[0:8], key_24[8:16], key_24[16:24]
        return [
            _3DES.des_key_schedule(k1),
            _3DES.des_key_schedule(k2),
            _3DES.des_key_schedule(k3)
        ]

    def load_file(self):
        file_path = filedialog.askopenfilename(title="Chọn file dữ liệu")
        if file_path:
            self.filepath = file_path
            self.file_name_only = os.path.splitext(os.path.basename(file_path))[0]

            self.lbl_filename.config(text=os.path.basename(file_path), foreground="#f1c40f")

            with open(file_path, "rb") as f:
                self.input_data = f.read()

            self.output_data = b""
            self.btn_save.config(state="disabled")

            self.cbo_in_mode.set("Text")
            self.update_view("in")
            self.update_view("out")

            self.log_message(
                f"Tải lên thành công: '{os.path.basename(file_path)}'. Kích thước: {len(self.input_data)} bytes.")

    def process_encryption(self):
        if not self.input_data:
            messagebox.showwarning("Lỗi", "Chưa có dữ liệu đầu vào!")
            return

        key_24 = self.get_valid_key()
        if not key_24: return

        try:
            self.log_message("Khởi động tiến trình MÃ HÓA 3DES...")
            self.root.update()

            # Sinh danh sách khóa cho 3 vòng DES
            subkeys_3 = self._prepare_3des_subkeys(key_24)

            # Padding PKCS#7 với Block Size là 8 (Của 3DES) thay vì 16
            block_size = 8
            pad_val = block_size - (len(self.input_data) % block_size)
            padded_data = self.input_data + bytes([pad_val] * pad_val)

            t_start = time.perf_counter()
            encrypted_blocks = []

            # Duyệt từng khối 8 byte
            for i in range(0, len(padded_data), block_size):
                block = padded_data[i: i + block_size]
                encrypted_blocks.append(_3DES.triple_des_block(block, subkeys_3, "encrypt"))

            self.output_data = b"".join(encrypted_blocks)
            t_end = time.perf_counter()

            self.current_action = "encrypt"
            self.cbo_out_mode.set("Hex")
            self.update_view("out")
            self.btn_save.config(state="normal")

            self.log_message(f"Hoàn tất MÃ HÓA 3DES trong {t_end - t_start:.5f} giây.")
            self.notebook.select(self.tab_data)

        except Exception as e:
            messagebox.showerror("Ngoại lệ", f"Quá trình mã hóa thất bại:\n{e}")

    def process_decryption(self):
        if not self.input_data:
            messagebox.showwarning("Lỗi", "Chưa có file mã hóa để giải mã!")
            return

        # 3DES yêu cầu file mã hóa chia hết cho 8
        block_size = 8
        if len(self.input_data) % block_size != 0:
            messagebox.showerror("Lỗi Cấu Trúc",
                                 "Kích thước file không hợp lệ (không chia hết cho 8). File có thể bị hỏng hoặc không phải chuẩn 3DES.")
            return

        key_24 = self.get_valid_key()
        if not key_24: return

        try:
            self.log_message("Khởi động tiến trình GIẢI MÃ 3DES...")
            self.root.update()

            subkeys_3 = self._prepare_3des_subkeys(key_24)

            t_start = time.perf_counter()
            decrypted_blocks = []

            # Duyệt từng khối 8 byte
            for i in range(0, len(self.input_data), block_size):
                block = self.input_data[i: i + block_size]
                decrypted_blocks.append(_3DES.triple_des_block(block, subkeys_3, "decrypt"))

            raw_decrypted = b"".join(decrypted_blocks)

            # Unpadding cho Block Size 8
            pad_val = raw_decrypted[-1]
            if 0 < pad_val <= block_size:
                self.output_data = raw_decrypted[:-pad_val]
            else:
                self.output_data = raw_decrypted

            t_end = time.perf_counter()

            self.current_action = "decrypt"
            self.cbo_in_mode.set("Hex")
            self.update_view("in")
            self.cbo_out_mode.set("Text")
            self.update_view("out")
            self.btn_save.config(state="normal")

            self.log_message(f"Hoàn tất GIẢI MÃ 3DES trong {t_end - t_start:.5f} giây.")
            self.notebook.select(self.tab_data)

        except Exception as e:
            messagebox.showerror("Lỗi Giải Mã", f"Sai khóa bí mật hoặc cấu trúc file hỏng.\nChi tiết: {e}")

    def save_output(self):
        if not self.output_data: return

        if self.current_action == "encrypt":
            default_name = f"{self.file_name_only}_encrypted_3des.bin"
            save_path = filedialog.asksaveasfilename(
                title="Lưu file Encrypted",
                initialfile=default_name,
                defaultextension=".bin",
                filetypes=[("Binary File", "*.bin")]
            )
        else:
            default_name = f"{self.file_name_only}_decrypted.txt"
            save_path = filedialog.asksaveasfilename(
                title="Lưu file Decrypted",
                initialfile=default_name,
                defaultextension=".txt",
                filetypes=[("Text Document", "*.txt"), ("All Files", "*.*")]
            )

        if save_path:
            try:
                with open(save_path, "wb") as f:
                    f.write(self.output_data)
                self.log_message(f"Lưu file thành công tại: {save_path}")
                messagebox.showinfo("Thành công", "Đã lưu kết quả thành công!")
            except Exception as e:
                messagebox.showerror("Lỗi Ghi File", f"Không thể lưu file vào thư mục đích:\n{e}")


if __name__ == "__main__":
    app_root = tk.Tk()
    app_root.resizable(False, False)
    app = CipherShiftApp(app_root)
    app_root.mainloop()