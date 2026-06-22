# Lab 5 - Thực hành với Private Hosted Zone - Hướng dẫn chi tiết

  **[Xem Đề bài / Yêu cầu bài Lab](5.%20Lab%205%20-%20Private%20Hosted%20Zone.md)**

---

## Các bước thực hiện chi tiết

### Bước 1: Chuẩn bị hai mạng ảo VPC và kích hoạt tính năng DNS
Trước hết, ta cần đảm bảo các mạng VPC được phép phân giải tên miền do AWS cung cấp:
1. Mở dịch vụ **VPC** trên AWS Console.
2. Tạo (hoặc sử dụng) hai VPC ở cùng một Region:
   * **VPC-A:** Dải CIDR `10.0.0.0/16` (ví dụ: `vpc-a-tokyo`).
   * **VPC-B:** Dải CIDR `172.16.0.0/16` (ví dụ: `vpc-b-tokyo`).
3. **Kích hoạt tính năng DNS cho từng VPC:**
   * Tại danh sách VPC, tích chọn **VPC-A** > Click chọn nút **Actions** ở góc trên bên phải > Chọn **Edit VPC settings**.
   * Tại màn hình cấu hình, tích chọn cả hai ô:
     * **Enable DNS resolution** (Bật phân giải DNS).
     * **Enable DNS hostnames** (Bật cấp phát DNS hostname).
   * Click chọn **Save**.
   * Thực hiện tương tự các bước trên đối với **VPC-B**.

---

### Bước 2: Khởi tạo Private Hosted Zone và Liên kết VPC-A
1. Mở dịch vụ **Route 53** > Click chọn **Hosted zones** > Click chọn nút **Create hosted zone**.
2. Thiết lập thông số Hosted Zone:
   * **Domain name:** Nhập tên miền nội bộ bạn muốn sử dụng (ví dụ: `corp.internal`).
   * **Type:** Tích chọn **Private hosted zone** (Vùng lưu trữ bản ghi nội bộ).
   * **VPCs to associate with the hosted zone:**
     * **Region:** Chọn đúng Region chứa các VPC của bạn (ví dụ: *ap-northeast-1*).
     * **VPC ID:** Chọn **VPC-A** từ danh sách gợi ý.
3. Click chọn nút **Create hosted zone**.

---

### Bước 3: Liên kết thêm VPC-B vào Private Hosted Zone
Mặc định lúc khởi tạo, Hosted Zone chỉ mới được liên kết với VPC-A. Ta cần liên kết thêm VPC-B để các máy chủ trong VPC-B cũng có thể tra cứu được tên miền này:
1. Tại giao diện chi tiết của Hosted Zone `corp.internal` vừa tạo, tìm tab **Hosted zone details**.
2. Tại mục **VPCs**, bạn sẽ thấy danh sách các VPC đang được liên kết. Click chọn nút **Edit** hoặc **Associate VPC**.
3. Chọn Region và tiếp tục chọn **VPC-B** từ danh sách > Click chọn **Associate**.
4. Click chọn **Save changes** (hoặc **Associate**). Lúc này cả hai VPC đều đã được gắn kết với vùng DNS nội bộ.

---

### Bước 4: Tạo EC2 trong VPC-A và Cấu hình Bản ghi DNS A nội bộ
1. Vào dịch vụ **EC2** > Khởi tạo một instance trong **VPC-A** (ví dụ tên: `app-server-vpc-a`).
2. Nhấp chọn instance vừa tạo, di chuyển xuống tab **Details** và sao chép địa chỉ **Private IPv4 address** của máy chủ này (ví dụ: `10.0.1.10`).
3. Quay lại **Route 53** > Hosted Zone `corp.internal`.
4. Click chọn **Create record** và cấu hình bản ghi nội bộ:
   * **Record name:** Nhập `db` (tên miền nội bộ đầy đủ sẽ là `db.corp.internal`).
   * **Record type:** Chọn **A – Routes traffic to an IPv4 address...**
   * **Alias:** Để tắt (**No**).
   * **Value:** Dán địa chỉ Private IP của EC2 trong VPC-A vừa sao chép (`10.0.1.10`).
   * **TTL (seconds):** Giữ mặc định `300`.
   * **Routing policy:** Chọn `Simple routing`.
5. Click chọn **Create records**.

---

### Bước 5: Kiểm thử phân giải tên miền nội bộ
Để xác minh DNS hoạt động, ta sẽ đăng nhập vào một máy chủ nằm ngoài VPC-A nhưng vẫn nằm trong mạng liên kết (VPC-B):

#### 1. Kiểm thử từ bên trong mạng AWS (EC2 trong VPC-B)
1. Khởi tạo một EC2 Instance phụ trong **VPC-B** (ví dụ tên: `client-vpc-b`), cấu hình gán Public IP để có thể SSH vào kiểm thử.
2. Sử dụng Terminal/PowerShell để SSH vào máy chủ `client-vpc-b`.
3. Chạy lệnh sau để kiểm tra phân giải DNS nội bộ:
   ```bash
   nslookup db.corp.internal
   ```
4. **Kết quả trả về chính xác:**
   ```text
   Server:         172.16.0.2
   Address:        172.16.0.2#53

   Non-authoritative answer:
   Name:   db.corp.internal
   Address: 10.0.1.10
   ```
   Tên miền nội bộ `db.corp.internal` đã được dịch chuyển thành công sang IP `10.0.1.10` nhờ máy chủ DNS mặc định của VPC-B (`172.16.0.2`).
   
   > [!NOTE]
   > **Lưu ý về kết nối mạng:**
   > Việc Private Hosted Zone phân giải thành công tên miền `db.corp.internal` ra địa chỉ IP `10.0.1.10` chỉ là bước **dịch nghĩa địa chỉ (DNS Resolution)**. Để máy chủ ở VPC-B có thể thực sự ping hoặc truyền dữ liệu kết nối tới máy chủ ở VPC-A, bạn cần thiết lập thêm hạ tầng kết nối mạng thực tế giữa 2 VPC như **VPC Peering** hoặc **Transit Gateway**.

#### 2. Kiểm thử từ máy tính cá nhân ngoài Internet
1. Mở Command Prompt hoặc PowerShell trên máy tính cá nhân của bạn ở nhà (đang kết nối mạng internet thông thường).
2. Chạy lệnh:
   ```powershell
   nslookup db.corp.internal
   ```
3. **Kết quả:** Hệ thống báo lỗi không tìm thấy tên miền (`Non-existent domain` hoặc `NXDOMAIN`). Điều này xác minh tên miền `db.corp.internal` được bảo vệ hoàn toàn và chỉ có giá trị phân giải an toàn bên trong các VPC đã khai báo.
