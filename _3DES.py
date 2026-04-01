import time
import os

# Hoán vị khởi tạo (Initial Permutation - IP)
IP = [
    58, 50, 42, 34, 26, 18, 10, 2, 60, 52, 44, 36, 28, 20, 12, 4,
    62, 54, 46, 38, 30, 22, 14, 6, 64, 56, 48, 40, 32, 24, 16, 8,
    57, 49, 41, 33, 25, 17, 9, 1, 59, 51, 43, 35, 27, 19, 11, 3,
    61, 53, 45, 37, 29, 21, 13, 5, 63, 55, 47, 39, 31, 23, 15, 7
]

# Hoán vị kết thúc (Final Permutation - FP / IP^-1)
FP = [
    40, 8, 48, 16, 56, 24, 64, 32, 39, 7, 47, 15, 55, 23, 63, 31,
    38, 6, 46, 14, 54, 22, 62, 30, 37, 5, 45, 13, 53, 21, 61, 29,
    36, 4, 44, 12, 52, 20, 60, 28, 35, 3, 43, 11, 51, 19, 59, 27,
    34, 2, 42, 10, 50, 18, 58, 26, 33, 1, 41, 9, 49, 17, 57, 25
]

# Bảng mở rộng (Expansion - E) từ 32-bit lên 48-bit
E_BOX = [
    32, 1, 2, 3, 4, 5, 4, 5, 6, 7, 8, 9,
    8, 9, 10, 11, 12, 13, 12, 13, 14, 15, 16, 17,
    16, 17, 18, 19, 20, 21, 20, 21, 22, 23, 24, 25,
    24, 25, 26, 27, 28, 29, 28, 29, 30, 31, 32, 1
]

# Hoán vị (Permutation - P)
P_BOX = [
    16, 7, 20, 21, 29, 12, 28, 17, 1, 15, 23, 26, 5, 18, 31, 10,
    2, 8, 24, 14, 32, 27, 3, 9, 19, 13, 30, 6, 22, 11, 4, 25
]

# Hoán vị lựa chọn khóa 1 (PC-1) - Bỏ bit chẵn lẻ
PC1 = [
    57, 49, 41, 33, 25, 17, 9, 1, 58, 50, 42, 34, 26, 18,
    10, 2, 59, 51, 43, 35, 27, 19, 11, 3, 60, 52, 44, 36,
    63, 55, 47, 39, 31, 23, 15, 7, 62, 54, 46, 38, 30, 22,
    14, 6, 61, 53, 45, 37, 29, 21, 13, 5, 28, 20, 12, 4
]

# Hoán vị lựa chọn khóa 2 (PC-2)
PC2 = [
    14, 17, 11, 24, 1, 5, 3, 28, 15, 6, 21, 10,
    23, 19, 12, 4, 26, 8, 16, 7, 27, 20, 13, 2,
    41, 52, 31, 37, 47, 55, 30, 40, 51, 45, 33, 48,
    44, 49, 39, 56, 34, 53, 46, 42, 50, 36, 29, 32
]

# Số bit dịch trái cho từng vòng tạo khóa DES
SHIFT_SCHEDULE = [1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1]

# 8 Bảng S-Box (Mỗi bảng 4 dòng x 16 cột, viết dạng mảng 1 chiều 64 phần tử)
S_BOXES = [
    [14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7, 0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8, 4, 1,
     14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0, 15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13],
    [15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10, 3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5, 0, 14,
     7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15, 13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9],
    [10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8, 13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1, 13, 6,
     4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7, 1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12],
    [7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15, 13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9, 10, 6,
     9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4, 3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14],
    [2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9, 14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6, 4, 2,
     1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14, 11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3],
    [12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11, 10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8, 9, 14,
     15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6, 4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13],
    [4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1, 13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6, 1, 4,
     11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2, 6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12],
    [13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7, 1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2, 7, 11,
     4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8, 2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11]
]


# =====================================================================
# CÁC HÀM XỬ LÝ BIT CHO DES
# =====================================================================

def permute(block, table, n_bits_in):
    """Thực hiện hoán vị bit dựa trên bảng table"""
    res = 0
    for i, pos in enumerate(table):
        # Lấy bit tại vị trí 'pos' (đếm từ 1, từ trái sang phải)
        bit = (block >> (n_bits_in - pos)) & 1
        # Gắn vào vị trí mới trong kết quả
        res |= (bit << (len(table) - 1 - i))
    return res


def s_box_substitution(block_48):
    """Quá trình thay thế qua 8 bảng S-Box"""
    res = 0
    for i in range(8):
        # Cắt lấy 6 bit từ trái sang phải
        chunk = (block_48 >> (42 - 6 * i)) & 0x3F
        # Xác định dòng (bit 1 và 6) và cột (bit 2,3,4,5)
        row = ((chunk & 0x20) >> 4) | (chunk & 0x01)
        col = (chunk & 0x1E) >> 1
        # Lấy giá trị từ S-Box
        val = S_BOXES[i][row * 16 + col]
        # Ghép vào kết quả 32-bit
        res |= (val << (28 - 4 * i))
    return res


def des_key_schedule(key_64):
    """Tạo ra 16 khóa con (48-bit) từ khóa gốc 64-bit"""
    # Ép khóa nguyên thủy từ byte sang số nguyên
    key_int = int.from_bytes(key_64, 'big')

    # 1. Hoán vị PC1 (64 -> 56 bit)
    key_56 = permute(key_int, PC1, 64)

    # Tách làm 2 nửa C và D (28 bit mỗi nửa)
    c = (key_56 >> 28) & 0xFFFFFFF
    d = key_56 & 0xFFFFFFF

    subkeys = []
    for shift in SHIFT_SCHEDULE:
        # Dịch xoay trái
        c = ((c << shift) | (c >> (28 - shift))) & 0xFFFFFFF
        d = ((d << shift) | (d >> (28 - shift))) & 0xFFFFFFF

        # Ghép C và D, sau đó hoán vị PC2 (56 -> 48 bit)
        cd_joined = (c << 28) | d
        key_48 = permute(cd_joined, PC2, 56)
        subkeys.append(key_48)

    return subkeys


# =====================================================================
# LÕI THUẬT TOÁN DES VÀ 3DES
# =====================================================================

def des_core(block_64_int, subkeys, mode="encrypt"):
    """Thực thi thuật toán DES cho 1 khối 64-bit"""
    # 1. Hoán vị khởi tạo IP
    block = permute(block_64_int, IP, 64)

    # Tách L và R (32 bit)
    left = (block >> 32) & 0xFFFFFFFF
    right = block & 0xFFFFFFFF

    # Đảo ngược khóa nếu là giải mã
    keys_to_use = subkeys if mode == "encrypt" else subkeys[::-1]

    # 16 Vòng Feistel
    for key in keys_to_use:
        # F-Function
        expanded_r = permute(right, E_BOX, 32)  # Mở rộng E
        xored = expanded_r ^ key  # XOR với subkey
        sbox_out = s_box_substitution(xored)  # Đi qua S-Box
        f_res = permute(sbox_out, P_BOX, 32)  # Hoán vị P

        # Trộn với Left
        new_right = left ^ f_res
        left = right
        right = new_right

    # Cuối vòng 16 không hoán đổi L và R, nên ta ghép Right trước Left
    pre_output = (right << 32) | left

    # Hoán vị kết thúc FP
    final_output = permute(pre_output, FP, 64)
    return final_output


def triple_des_block(block_bytes, keys_3, mode="encrypt"):
    """
    Thực thi 3DES (Triple DES).
    - encrypt: E(K1) -> D(K2) -> E(K3)
    - decrypt: D(K3) -> E(K2) -> D(K1)
    """
    block_int = int.from_bytes(block_bytes, 'big')

    if mode == "encrypt":
        b1 = des_core(block_int, keys_3[0], "encrypt")
        b2 = des_core(b1, keys_3[1], "decrypt")
        b3 = des_core(b2, keys_3[2], "encrypt")
    else:
        b1 = des_core(block_int, keys_3[2], "decrypt")
        b2 = des_core(b1, keys_3[1], "encrypt")
        b3 = des_core(b2, keys_3[0], "decrypt")

    return b3.to_bytes(8, 'big')


# =====================================================================
# XỬ LÝ ĐỌC/GHI FILE VÀ GIAO DIỆN CHÍNH
# =====================================================================
def main():
    print("======================================================")
    print(" BÀI TẬP NHÓM 18: MÃ HÓA VÀ GIẢI MÃ CHUỖI VĂN BẢN (3DES)")
    print("======================================================")

    # 1. Nhập và xử lý Khóa (Key)
    key_in = input("[?] Nhập khóa mã hóa (tối đa 24 ký tự): ")
    # Đệm null byte nếu khóa ngắn hơn 24, cắt đi nếu dài hơn 24
    key_str = key_in.encode("utf-8").ljust(24, b"\0")[:24]

    k1, k2, k3 = key_str[0:8], key_str[8:16], key_str[16:24]
    subkeys_3 = [
        des_key_schedule(k1),
        des_key_schedule(k2),
        des_key_schedule(k3)
    ]

    # 2. Nhập đoạn dữ liệu (Validate >= 15 ký tự)
    while True:
        data_in = input("\n[?] Nhập dữ liệu cần mã hóa (Tối thiểu 15 ký tự/số): ")
        if len(data_in) >= 15:
            break
        print(f"[!] Lỗi: Bạn vừa nhập {len(data_in)} ký tự. Vui lòng nhập tối thiểu 15 ký tự!")

    raw_data = data_in.encode("utf-8")

    # 3. THỰC HIỆN MÃ HÓA
    print("\n[*] Đang tiến hành MÃ HÓA...")
    block_size = 8
    pad_len = block_size - (len(raw_data) % block_size)
    data_to_encrypt = raw_data + bytes([pad_len] * pad_len)

    start_e = time.perf_counter()
    encrypted = bytearray()
    for i in range(0, len(data_to_encrypt), block_size):
        block = data_to_encrypt[i: i + block_size]
        encrypted += triple_des_block(block, subkeys_3, mode="encrypt")
    end_e = time.perf_counter()
    time_encrypt = end_e - start_e

    # In kết quả mã hóa dưới dạng Hex để dễ quan sát
    enc_hex = encrypted.hex().upper()
    print(f"[+] Bản mã (Hex): {enc_hex}")

    # 4. THỰC HIỆN GIẢI MÃ
    print("\n[*] Đang tiến hành GIẢI MÃ...")
    start_d = time.perf_counter()
    decrypted_raw = bytearray()
    for i in range(0, len(encrypted), block_size):
        block = encrypted[i: i + block_size]
        decrypted_raw += triple_des_block(block, subkeys_3, mode="decrypt")

    # Gỡ Padding
    pad_len_dec = decrypted_raw[-1]
    if 0 < pad_len_dec <= block_size:
        final_data = decrypted_raw[:-pad_len_dec]
    else:
        final_data = decrypted_raw
    end_d = time.perf_counter()
    time_decrypt = end_d - start_d

    try:
        dec_text = final_data.decode("utf-8")
    except Exception:
        dec_text = "<Lỗi giải mã UTF-8>"
    print(f"[+] Bản rõ sau giải mã: {dec_text}")

    # 5. TỔNG KẾT BÁO CÁO THỜI GIAN
    print("\n================ TỔNG KẾT KẾT QUẢ ================")
    print(f"Dữ liệu gốc ({len(data_in)} ký tự): {data_in}")
    print("-" * 50)
    print(f"[THỜI GIAN MÃ HÓA 3DES]:  {time_encrypt:.6f} giây")
    print(f"[THỜI GIAN GIẢI MÃ 3DES]: {time_decrypt:.6f} giây")
    print("======================================================")


if __name__ == "__main__":
    main()
