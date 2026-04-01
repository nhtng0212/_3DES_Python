import tkinter as tk
from tkinter import ttk, messagebox
import time
import os

# Import file chứa thuật toán của bạn
import _3DES


class CipherShiftTextApp:
    def __init__(self, root):
        self.root = root
        self.root.title("3DES Text Crypto - Nhóm 18")
        self.root.geometry("950x600")

        # Bảng màu tối (Dark Mode) cho 3DES
        self.BG_MAIN = "#1e1e2f"
        self.BG_CARD = "#2a2a40"
        self.FG_TEXT = "#ffffff"
        self.FG_DIM = "#a0a0b8"

        self.root.configure(bg=self.BG_MAIN)
        self.raw_encrypted_bytes = b""  # Lưu bản mã dạng byte trong biến chương trình

        # --- LOGIC CACHE KHÓA ---
        self.cache_file = "key_cache.txt"
        self.key_var = tk.StringVar(value=self.load_key_cache())
        self.show_pwd_var = tk.BooleanVar(value=False)

        self._build_ui()
        self.write_log("Hệ thống 3DES Text Crypto đã khởi động.")
        self.write_log("Yêu cầu: Nhập ít nhất 15 ký tự để mã hóa.")

    # --- HÀM XỬ LÝ CACHE ---
    def load_key_cache(self):
        """Đọc khóa từ file cache nếu có"""
        if os.path.exists(self.cache_file):
            try:
                with open(self.cache_file, "r", encoding="utf-8") as f:
                    return f.read().strip()
            except Exception:
                pass
        return ""

    def save_key_cache(self, key_str):
        """Lưu khóa vào file cache"""
        try:
            with open(self.cache_file, "w", encoding="utf-8") as f:
                f.write(key_str)
        except Exception:
            pass

    def _build_ui(self):
        style = ttk.Style()
        style.theme_use('clam')

        # ============ KHU VỰC NHẬP KHÓA ============
        top_frame = tk.Frame(self.root, bg=self.BG_CARD, pady=15, padx=20)
        top_frame.pack(fill="x", padx=15, pady=(15, 5))

        tk.Label(top_frame, text="🔑 Khóa 3DES (Max 24 ký tự):", font=("Segoe UI", 11, "bold"), bg=self.BG_CARD,
                 fg=self.FG_TEXT).pack(side="left")

        # Ô nhập liệu liên kết với biến key_var (chứa cache)
        self.entry_key = tk.Entry(top_frame, textvariable=self.key_var, show="*", font=("Consolas", 12), bg="#1e1e2f",
                                  fg="#00ffcc", insertbackground="white", width=30)
        self.entry_key.pack(side="left", padx=10)

        # Nút Icon con mắt (Hiển thị / Ẩn khóa)
        self.btn_eye = tk.Button(top_frame, text="👁", font=("Segoe UI", 10), bg="#444466", fg="white", relief="flat",
                                 cursor="hand2", command=self.toggle_password)
        self.btn_eye.pack(side="left", ipadx=5)

        # ============ KHU VỰC VĂN BẢN (CHIA ĐÔI) ============
        content_frame = tk.Frame(self.root, bg=self.BG_MAIN)
        content_frame.pack(fill="both", expand=True, padx=15, pady=5)

        # NỬA TRÁI (Nhập liệu)
        left_panel = tk.Frame(content_frame, bg=self.BG_CARD)
        left_panel.pack(side="left", fill="both", expand=True, padx=(0, 5))

        tk.Label(left_panel, text="📝 DỮ LIỆU ĐẦU VÀO (>= 15 ký tự)", font=("Segoe UI", 10, "bold"), bg=self.BG_CARD,
                 fg="#ff6666").pack(anchor="w", padx=10, pady=5)
        self.txt_input = tk.Text(left_panel, font=("Consolas", 11), bg="#1e1e2f", fg="white", insertbackground="white",
                                 wrap="word", padx=10, pady=10)
        self.txt_input.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        # NỬA PHẢI (Kết quả)
        right_panel = tk.Frame(content_frame, bg=self.BG_CARD)
        right_panel.pack(side="right", fill="both", expand=True, padx=(5, 0))

        tk.Label(right_panel, text="📤 KẾT QUẢ ĐẦU RA (Raw Characters)", font=("Segoe UI", 10, "bold"), bg=self.BG_CARD,
                 fg="#66ff99").pack(anchor="w", padx=10, pady=5)
        self.txt_output = tk.Text(right_panel, font=("Consolas", 11), bg="#1e1e2f", fg="#f0f0f0", wrap="word", padx=10,
                                  pady=10, state="disabled")
        self.txt_output.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        # ============ ACTION BAR ============
        action_frame = tk.Frame(self.root, bg=self.BG_MAIN)
        action_frame.pack(fill="x", padx=15, pady=10)

        self.btn_enc = tk.Button(action_frame, text="🔒 MÃ HÓA", bg="#ff4d4d", fg="white", font=("Segoe UI", 11, "bold"),
                                 width=15, cursor="hand2", command=self.run_encrypt)
        self.btn_enc.pack(side="left", padx=5)

        self.btn_dec = tk.Button(action_frame, text="🔓 GIẢI MÃ", bg="#00cc99", fg="white",
                                 font=("Segoe UI", 11, "bold"), width=15, cursor="hand2", command=self.run_decrypt)
        self.btn_dec.pack(side="left", padx=5)

        # ============ TERMINAL LOG ============
        log_frame = tk.Frame(self.root, bg=self.BG_MAIN)
        log_frame.pack(side="bottom", fill="x", padx=15, pady=(0, 15))

        tk.Label(log_frame, text="THỐNG KÊ THỜI GIAN & NHẬT KÝ", font=("Segoe UI", 9, "bold"), bg=self.BG_MAIN,
                 fg=self.FG_DIM, anchor="w").pack(fill="x")
        self.txt_log = tk.Text(log_frame, height=4, bg="#000000", fg="#33ccff", font=("Consolas", 10), padx=8, pady=8)
        self.txt_log.pack(fill="both")

    # --- HÀM TIỆN ÍCH UI ---
    def toggle_password(self):
        """Bật / Tắt hiển thị mật khẩu"""
        self.show_pwd_var.set(not self.show_pwd_var.get())
        if self.show_pwd_var.get():
            self.entry_key.config(show="")
            self.btn_eye.config(text="🙈", bg="#ff4d4d")  # Mở mắt thì đổi màu cảnh báo
        else:
            self.entry_key.config(show="*")
            self.btn_eye.config(text="👁", bg="#444466")

    def write_log(self, msg):
        time_str = time.strftime("%H:%M:%S")
        self.txt_log.insert(tk.END, f"[{time_str}] {msg}\n")
        self.txt_log.see(tk.END)

    def set_output(self, text):
        self.txt_output.config(state="normal")
        self.txt_output.delete(1.0, tk.END)
        self.txt_output.insert(tk.END, text)
        self.txt_output.config(state="disabled")

    def _prepare_3des_subkeys(self, key_24):
        k1, k2, k3 = key_24[0:8], key_24[8:16], key_24[16:24]
        return [
            _3DES.des_key_schedule(k1),
            _3DES.des_key_schedule(k2),
            _3DES.des_key_schedule(k3)
        ]

    # --- HÀM XỬ LÝ LÕI ---
    def run_encrypt(self):
        input_text = self.txt_input.get(1.0, tk.END).strip()

        if len(input_text) < 15:
            messagebox.showwarning("Cảnh báo",
                                   f"Đoạn văn bản hiện tại chỉ có {len(input_text)} ký tự.\nYêu cầu tối thiểu là 15 ký tự (chữ/số)!")
            return

        key_str = self.key_var.get()
        if not key_str:
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập khóa bí mật!")
            return

        # Lưu cache khóa lại
        self.save_key_cache(key_str)

        try:
            key_24 = key_str.encode("utf-8").ljust(24, b"\0")[:24]
            subkeys_3 = self._prepare_3des_subkeys(key_24)

            raw_data = input_text.encode("utf-8")

            # Padding PKCS#7 (Block 8)
            block_size = 8
            pad_val = block_size - (len(raw_data) % block_size)
            padded_data = raw_data + bytes([pad_val] * pad_val)

            t_start = time.perf_counter()
            encrypted_blocks = []
            for i in range(0, len(padded_data), block_size):
                block = padded_data[i: i + block_size]
                encrypted_blocks.append(_3DES.triple_des_block(block, subkeys_3, "encrypt"))

            self.raw_encrypted_bytes = b"".join(encrypted_blocks)
            t_end = time.perf_counter()
            exec_time = t_end - t_start

            # ĐIỂM SỬA ĐỔI: Dùng chuẩn latin-1 để ép hiển thị các byte thô thành ký tự (Gibberish Text)
            # Latin-1 an toàn 100% vì nó map toàn bộ 256 giá trị byte sang 256 ký tự Unicode
            raw_chars_output = self.raw_encrypted_bytes.decode("latin-1")

            self.set_output(raw_chars_output)
            self.write_log(f"MÃ HÓA THÀNH CÔNG! Thời gian xử lý: {exec_time:.6f} giây.")

        except Exception as e:
            messagebox.showerror("Ngoại lệ", f"Lỗi trong quá trình mã hóa:\n{e}")

    def run_decrypt(self):
        if not self.raw_encrypted_bytes:
            messagebox.showinfo("Thông báo",
                                "Chưa có dữ liệu mã hóa trong bộ nhớ. Vui lòng mã hóa một đoạn văn bản trước!")
            return

        key_str = self.key_var.get()
        if not key_str:
            return

        # Lưu cache khóa lại (phòng hờ trường hợp người dùng đổi khóa lúc giải mã)
        self.save_key_cache(key_str)

        try:
            key_24 = key_str.encode("utf-8").ljust(24, b"\0")[:24]
            subkeys_3 = self._prepare_3des_subkeys(key_24)

            t_start = time.perf_counter()
            decrypted_blocks = []
            block_size = 8
            for i in range(0, len(self.raw_encrypted_bytes), block_size):
                block = self.raw_encrypted_bytes[i: i + block_size]
                decrypted_blocks.append(_3DES.triple_des_block(block, subkeys_3, "decrypt"))

            raw_decrypted = b"".join(decrypted_blocks)

            # Unpadding
            pad_val = raw_decrypted[-1]
            if 0 < pad_val <= block_size:
                final_data = raw_decrypted[:-pad_val]
            else:
                final_data = raw_decrypted

            t_end = time.perf_counter()
            exec_time = t_end - t_start

            dec_text = final_data.decode("utf-8")
            self.set_output(dec_text)
            self.write_log(f"GIẢI MÃ THÀNH CÔNG! Thời gian xử lý: {exec_time:.6f} giây.")

        except Exception as e:
            messagebox.showerror("Lỗi Giải Mã", f"Sai khóa hoặc dữ liệu hỏng.\nChi tiết: {e}")


if __name__ == "__main__":
    app_root = tk.Tk()
    app = CipherShiftTextApp(app_root)
    app_root.mainloop()