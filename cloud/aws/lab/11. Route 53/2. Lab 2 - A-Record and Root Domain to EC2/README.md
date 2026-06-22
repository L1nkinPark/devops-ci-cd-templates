# Lab 2 - Thực hành A-Record & Sử dụng root domain để trỏ tới một EC2 Instance - Hướng dẫn chi tiết

 **[Xem Đề bài / Yêu cầu bài Lab](2.%20Lab%202%20-%20A-Record%20and%20Root%20Domain%20to%20EC2.md)**

---

## Các bước thực hiện chi tiết

### Bước 1: Khởi tạo máy chủ Web EC2 và lấy Public IP
1. Truy cập dịch vụ **Amazon EC2** trên AWS Console > Click chọn **Launch instance**.
2. Thiết lập thông số cơ bản cho instance:
   * **Name:** Nhập `web-server-lab2`.
   * **OS:** Chọn **Amazon Linux 2023** (hoặc Amazon Linux 2).
   * **Instance type:** Chọn **t2.micro** (Free Tier).
   * **Key pair:** Chọn key pair có sẵn của bạn để SSH (nếu cần).
   * **Network settings:** Tích chọn **Allow HTTP traffic from the internet** (cho phép truy cập cổng 80).
3. Cuộn xuống phần **Advanced details**, tại mục **User data**, dán đoạn script sau để tự động cài đặt Apache Web Server:
   ```bash
   #!/bin/bash
   # Cập nhật hệ thống
   yum update -y
   # Cài đặt máy chủ web Apache
   yum install -y httpd
   # Khởi chạy dịch vụ httpd
   systemctl start httpd
   # Kích hoạt tự chạy cùng hệ thống
   systemctl enable httpd
   # Tạo trang web mặc định hiển thị thông tin chào mừng và IP của máy chủ
   PUBLIC_IP=$(curl -s http://169.254.169.254/latest/meta-data/public-ipv4)
   echo "<h1>Welcome to AWS Route 53 Lab 2!</h1><p>Served by EC2 instance. Public IP: $PUBLIC_IP</p>" > /var/www/html/index.html
   ```
4. Click chọn **Launch instance** và đợi trạng thái của instance chuyển sang *Running*.
5. Click chọn instance mới tạo, ghi lại địa chỉ **Public IPv4 address** (ví dụ: `54.198.88.99`).

---

### Bước 2: Cấu hình bản ghi A cho Subdomain trên Route 53
1. Quay lại dịch vụ **Route 53** > Click chọn **Hosted zones** > Chọn tên miền của bạn (ví dụ: `h1eudayne.click`).
2. Nhấp chọn nút **Create record** ở góc trên bên phải.
3. Điền cấu hình bản ghi như sau:
   * **Record name:** Nhập `app` (để tạo tên miền phụ `app.h1eudayne.click`).
   * **Record type:** Chọn **A – Routes traffic to an IPv4 address and some AWS resources**.
   * **Alias:** Để tắt (**No**).
   * **Value:** Dán địa chỉ Public IP của EC2 bạn đã sao chép ở Bước 1 (ví dụ: `54.198.88.99`).
   * **TTL (seconds):** Giữ mặc định `300` (5 phút).
   * **Routing policy:** Chọn **Simple routing**.
4. Click chọn **Create records**.

---

### Bước 3: Cấu hình trỏ Root Domain về EC2 Instance
Để trỏ tên miền gốc (Root Domain / Apex Domain - ví dụ: `h1eudayne.click` không chứa tiền tố) về máy chủ EC2, ta thực hiện như sau:

#### Phương án 1: Trỏ trực tiếp về IP tĩnh của EC2 (Thực hành trong Lab này)
1. Trong Hosted Zone, tiếp tục click chọn **Create record**.
2. Điền cấu hình bản ghi:
   * **Record name:** **Để trống** (để cấu hình trực tiếp cho tên miền gốc `h1eudayne.click`).
   * **Record type:** Chọn **A – Routes traffic to an IPv4 address...**
   * **Alias:** Để tắt (**No**).
   * **Value:** Dán địa chỉ Public IP của EC2 (ví dụ: `54.198.88.99`).
   * Click chọn **Create records**.

#### Phương án 2: Trỏ về Elastic Load Balancer (ELB) bằng bản ghi ALIAS (Môi trường Product)
Trong thực tế sản xuất, các máy chủ EC2 thường đứng sau một bộ cân bằng tải (ELB). ELB không sử dụng IP cố định mà sử dụng một DNS mặc định (dạng `my-load-balancer-123.amazonaws.com`).
Vì chuẩn DNS quốc tế không cho phép tạo bản ghi CNAME tại Root Domain, ta bắt buộc phải sử dụng bản ghi **ALIAS** (bí danh) của Route 53:
1. Nhấp chọn **Create record**.
2. **Record name:** **Để trống**.
3. **Record type:** Chọn **A – Routes traffic to an IPv4 address...**
4. **Alias:** Gạt nút sang bật (**Yes**).
5. **Route traffic to:**
   * Chọn *Alias to Application and Classic Load Balancer*.
   * Chọn *Region* tương ứng (ví dụ: *us-east-1*).
   * Chọn bộ cân bằng tải *Load Balancer* của bạn từ danh sách gợi ý.
6. Click chọn **Create records**. (Route 53 sẽ tự động phân giải DNS của ELB sang các địa chỉ IP tương ứng cho Client hoàn toàn miễn phí).

---

### Bước 4: Kiểm thử và Xác minh DNS
Sau khi tạo xong bản ghi, chúng ta sẽ kiểm tra xem DNS đã hoạt động chưa:

#### 1. Sử dụng công cụ dòng lệnh (nslookup/dig)
Mở PowerShell hoặc Command Prompt trên máy tính cá nhân của bạn và chạy lệnh sau:
```powershell
nslookup app.h1eudayne.click
```
**Kết quả hiển thị chính xác:**
```text
Server:  UnKnown
Address:  192.168.1.1

Non-authoritative answer:
Name:    app.h1eudayne.click
Address:  54.198.88.99
```
Địa chỉ IP trả về trùng khớp với Public IP của EC2 chứng tỏ bản ghi A-Record đã hoạt động chính xác. Chạy tương tự cho tên miền gốc `nslookup h1eudayne.click`.

#### 2. Kiểm thử trên Trình duyệt
1. Mở trình duyệt web của bạn.
2. Truy cập địa chỉ: `http://app.h1eudayne.click` (hoặc `http://h1eudayne.click`).
3. **Kết quả:** Trình duyệt hiển thị trang HTML chào mừng:
   *"Welcome to AWS Route 53 Lab 2! Served by EC2 instance. Public IP: 54.198.88.99"*
