## 1. Cách chạy

#### 1.1. Chuẩn bị file thử

Tạo một file văn bản nhỏ. Bản Python thuần chạy chậm (mỗi byte cần 8 nhịp, cộng 1152 nhịp khởi tạo), nên hãy bắt đầu với file nhỏ (vài trăm byte đến vài KB).

Linux/macOS:

bash

```bash
echo "Day la file thu nghiem cho bai lab Trivium." > plain.txt
```

Windows (PowerShell):

powershell

```powershell
"Day la file thu nghiem cho bai lab Trivium." | Out-File -Encoding utf8 plain.txt
```

#### 1.2. Chọn key

Key phải là **20 ký tự hex** (80 bit), không có tiền tố `0x`. Ví dụ dùng key mẫu của đề: `00112233445566778899`.

#### 1.3. Mã hóa và giải mã

bash

```bash
python3 encrypt_file.py enc 00112233445566778899 plain.txt cipher.bin
python3 encrypt_file.py dec 00112233445566778899 cipher.bin recovered.txt
```

Mỗi lệnh sẽ in `enc: wrote cipher.bin` hoặc `dec: wrote recovered.txt`. (Trên Windows, dùng `python` hoặc `py` thay cho `python3` nếu cần.)

#### 1.4. Kiểm tra giải mã đúng

Linux/macOS:

bash

```bash
cmp plain.txt recovered.txt && echo "GIONG NHAU"
sha256sum plain.txt recovered.txt        # hai hash phải bằng nhau
```

Windows:

powershell

```powershell
fc /b plain.txt recovered.txt
Get-FileHash plain.txt, recovered.txt    # hai hash phải bằng nhau
```

`cmp` không in gì nghĩa là hai file giống hệt nhau byte-by-byte.

#### 1.5. Kiểm tra kích thước

bash

```bash
ls -l plain.txt cipher.bin               # cipher.bin = plain.txt + 10 byte
```

### 2. Test: mã hóa cùng file hai lần phải ra hai kết quả khác nhau

bash

```bash
python3 encrypt_file.py enc 00112233445566778899 plain.txt c1.bin
python3 encrypt_file.py enc 00112233445566778899 plain.txt c2.bin
cmp c1.bin c2.bin        # phải báo "differ"
```

Để thấy rõ nguyên nhân, xem 10 byte đầu (chính là IV):

bash

```bash
xxd -l 10 c1.bin
xxd -l 10 c2.bin         # hai IV phải khác nhau
```

Hoặc dùng Python (chạy được trên mọi hệ điều hành):

python

```python
a = open('c1.bin','rb').read(); b = open('c2.bin','rb').read()
print("IV1:", a[:10].hex()); print("IV2:", b[:10].hex())
print("phan cipher khac nhau:", a[10:] != b[10:])
```

Cuối cùng, kiểm tra cả hai file đều giải mã về đúng bản gốc:

bash

```bash
python3 encrypt_file.py dec 00112233445566778899 c1.bin r1.txt
python3 encrypt_file.py dec 00112233445566778899 c2.bin r2.txt
cmp plain.txt r1.txt && cmp plain.txt r2.txt && echo "CA HAI DEU DUNG"
```

Kết luận cho báo cáo: cùng key, cùng plaintext nhưng IV khác nên keystream khác, do đó ciphertext khác. Dù vậy cả hai đều giải mã được vì IV nằm sẵn ở đầu file.
