# Lab 4 - Thực hành với Route 53 Health check & Failover Routing - Hướng dẫn chi tiết

  **[Xem Đề bài / Yêu cầu bài Lab](4.%20Lab%204%20-%20Route%2053%20Health%20Check.md)**

---

## Các bước thực hiện chi tiết

### Bước 1: Chuẩn bị Tài nguyên Chính & Dự phòng
1. **Máy chủ chính (EC2):** Sử dụng máy chủ web EC2 đã khởi tạo từ Lab 2 (hoặc tạo mới). Đảm bảo dịch vụ Apache đang chạy và bạn có địa chỉ Public IP của nó (ví dụ: `54.198.88.99`).
2. **Trang dự phòng (S3):** 
   * Truy cập S3 Console > Chọn bucket chứa website tĩnh của bạn (hoặc tạo một bucket mới, ví dụ: `maintenance-h1eudayne`).
   * Upload tệp `index.html` đơn giản với nội dung thông báo bảo trì:
     ```html
     <h1>System Under Maintenance</h1>
     <p>Chúng tôi đang bảo trì hệ thống định kỳ. Xin vui lòng quay lại sau ít phút.</p>
     ```
   * Đảm bảo bucket đã được bật tính năng **Static website hosting** và có địa chỉ endpoint hoạt động bình thường (ví dụ: `maintenance-h1eudayne.s3-website-us-east-1.amazonaws.com`).

---

### Bước 2: Khởi tạo Route 53 Health Check
1. Mở dịch vụ **Route 53** trên AWS Console.
2. Tại menu bên trái, nhấp chọn mục **Health checks** (Kiểm tra sức khỏe).
3. Click chọn nút **Create health check**.
4. Cấu hình các thông số kiểm tra:
   * **Name:** Nhập `main-server-health-check`.
   * **What to monitor:** Chọn **Endpoint**.
   * **Specify endpoint by:** Chọn **IP address**.
   * **Protocol:** Chọn **HTTP** (do lab của chúng ta đang chạy Apache thường không có SSL ở cổng 80).
   * **IP address:** Nhập địa chỉ Public IP của máy chủ EC2 chính (ví dụ: `54.198.88.99`).
   * **Port:** Nhập `80`.
   * **Path:** Nhập `/` (để kiểm tra trang chủ).
5. Click chọn **Next**.
6. Tại màn hình cấu hình Cảnh báo (Create alarm):
   * Chọn **No** ở mục *Create alarm* (để tránh phát sinh thêm chi phí dịch vụ CloudWatch Alarm/SNS trong môi trường học tập).
7. Click chọn **Create health check**.
8. Trạng thái ban đầu của Health Check sẽ hiển thị là *Unknown*. Sau khoảng **1 - 2 phút**, hệ thống gửi request probe thành công sẽ chuyển sang màu xanh **Healthy**.

---

### Bước 3: Cấu hình bản ghi Failover Routing trong Hosted Zone
Chúng ta sẽ tạo hai bản ghi trùng tên nhưng khác kiểu định tuyến Failover:

#### 1. Tạo bản ghi chính (Primary Record)
1. Vào Route 53 > **Hosted zones** > Chọn tên miền của bạn (`h1eudayne.click`).
2. Nhấp chọn **Create record** và cấu hình:
   * **Record name:** Nhập `service` (tên miền truy cập sẽ là `service.h1eudayne.click`).
   * **Record type:** Chọn **A – Routes traffic to an IPv4 address...**
   * **Alias:** Để tắt (**No**).
   * **Value:** Nhập Public IP của máy chủ EC2 chính (ví dụ: `54.198.88.99`).
   * **Routing policy:** Chọn **Failover**.
   * **Failover record type:** Chọn **Primary** (Bản ghi chính).
   * **Associate with health check:** Chọn **Yes**.
   * **Health check to associate:** Chọn đúng tên Health check bạn vừa tạo ở Bước 2 (`main-server-health-check`).
   * **Record ID:** Nhập `main-web-server`.
3. Click chọn **Create records**.

#### 2. Tạo bản ghi dự phòng (Secondary Record)
1. Tiếp tục nhấp chọn **Create record** để cấu hình bản ghi dự phòng:
   * **Record name:** Nhập trùng tên `service`.
   * **Record type:** Chọn **A – Routes traffic to an IPv4 address...**
   * **Alias:** Gạt sang bật (**Yes**) (vì chúng ta sẽ trỏ tới S3 Static Website Endpoint bằng ALIAS).
   * **Route traffic to:**
     * Chọn *Alias to S3 website endpoint*.
     * Chọn Region tương ứng của bucket S3 (ví dụ: *us-east-1*).
     * Chọn đúng tên bucket dự phòng của bạn (`maintenance-h1eudayne`).
   * **Routing policy:** Chọn **Failover**.
   * **Failover record type:** Chọn **Secondary** (Bản ghi dự phòng).
   * **Associate with health check:** Chọn **No** (Bản ghi phụ không cần tự kiểm tra).
   * **Record ID:** Nhập `maintenance-web-page`.
2. Click chọn **Create records**.

---

### Bước 4: Kiểm thử kịch bản tự động phục hồi sự cố
1. **Kiểm tra trạng thái bình thường:**
   * Mở trình duyệt và truy cập `http://service.h1eudayne.click`.
   * **Kết quả:** Giao diện hiển thị trang web hoạt động bình thường của EC2.
2. **Giả lập sự cố máy chủ chính:**
   * SSH vào máy chủ EC2 chính qua terminal.
   * Chạy lệnh sau để tắt hoàn toàn dịch vụ máy chủ web Apache:
     ```bash
     sudo systemctl stop httpd
     ```
3. **Theo dõi sự thay đổi trên Route 53:**
   * Quay lại Route 53 Console > mục **Health checks**.
   * Chờ khoảng **1 - 2 phút** (tùy thuộc vào tần suất kiểm tra), bạn sẽ thấy trạng thái chuyển từ xanh sang đỏ **Unhealthy**.
4. **Kiểm tra kết quả phân giải DNS của Client:**
   * Mở trình duyệt ẩn danh mới (hoặc xóa cache DNS bằng lệnh `ipconfig /flushdns` trên Windows).
   * Truy cập lại địa chỉ: `http://service.h1eudayne.click`.
   * **Kết quả:** Trình duyệt tự động hiển thị trang thông báo bảo trì từ S3:
     *"System Under Maintenance - Chúng tôi đang bảo trì hệ thống định kỳ. Xin vui lòng quay lại sau ít phút."*
5. **Khôi phục hệ thống:**
   * Quay lại terminal EC2 và khởi chạy lại dịch vụ web:
     ```bash
     sudo systemctl start httpd
     ```
   * Theo dõi Health Check chuyển sang xanh trở lại. Truy cập lại tên miền phụ, giao diện web EC2 sẽ tự động hiển thị lại bình thường.
