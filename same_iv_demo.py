from trivium import keystream

key = bytes.fromhex("00112233445566778899")   # Đề cho sẵn dùng luôn
iv  = bytes.fromhex("aabbccddeeff00112233")   # IV cố định

p1 = b"Chuyen khoan 1000 USD cho Binh"
p2 = b"Mat khau la: binhdz123 nhe!!!"
n = min(len(p1), len(p2))          # cắt về cùng độ dài
p1, p2 = p1[:n], p2[:n]

ks = keystream(key, iv, n)         # cùng keystream cho cả hai
c1 = bytes(a ^ b for a, b in zip(p1, ks))
c2 = bytes(a ^ b for a, b in zip(p2, ks))

c1c2 = bytes(a ^ b for a, b in zip(c1, c2))   # c1 ⊕ c2
p1p2  = bytes(a ^ b for a, b in zip(p1, p2))   # p1 ⊕ p2
print("c1 xor c2 == p1 xor p2 ?", c1c2 == p1p2)   # phải là True

# biết p1 thì suy ra p2 mà ko cần key:
recovered_p2 = bytes(a ^ b for a, b in zip(c1c2, p1))
print("p2 khôi phục được:", recovered_p2)