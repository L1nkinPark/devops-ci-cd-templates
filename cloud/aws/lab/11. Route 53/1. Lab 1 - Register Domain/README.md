# Lab 1 - Đăng ký tên miền (Register Domain) bằng Route 53 - Hướng dẫn chi tiết

 **[Xem Đề bài / Yêu cầu bài Lab](1.%20Lab%201%20-%20Register%20Domain.md)**

---

## Các bước thực hiện chi tiết

### Bước 1: Tìm kiếm và Lựa chọn Tên miền
1. Đăng nhập vào **AWS Management Console**.
2. Tìm kiếm và mở dịch vụ **Route 53**.
3. Tại trang Dashboard chính của Route 53, ở menu bên trái, di chuyển đến mục **Registered domains** (Tên miền đã đăng ký).
4. Click chọn nút **Register domains** để mở trình duyệt mua tên miền.
5. Tại thanh tìm kiếm, nhập tên miền bạn mong muốn sở hữu (ví dụ: `h1eudayne`).
6. Chọn đuôi mở rộng phù hợp từ danh sách gợi ý.
   > [!TIP]
   > Để tiết kiệm chi phí học tập, hãy lọc danh sách các tên miền có đuôi mở rộng giá rẻ (ví dụ: đuôi `.click` hoặc `.link` có giá khoảng $3.00 USD/năm).
7. Nhấp chọn **Select** cho tên miền mong muốn để thêm vào giỏ hàng, sau đó click chọn **Proceed to checkout** (Tiến hành thanh toán).

---

### Bước 2: Khai báo Thông tin Đăng ký (Contact Info)
1. Tại màn hình điền thông tin liên hệ:
   * **Contact type:** Chọn **Person** (Cá nhân) hoặc **Company** (Doanh nghiệp).
   * Điền đầy đủ thông tin cá nhân của bạn theo mẫu, bao gồm: Họ tên, Địa chỉ, Số điện thoại (chú ý điền đúng mã vùng quốc gia, ví dụ Việt Nam là `+84`), và địa chỉ Email chính xác.
   * **Privacy protection:** Tích chọn **Enable** để bảo mật thông tin liên hệ của bạn khỏi các công cụ tra cứu công khai (Whois), tránh việc bị spam điện thoại/email.
2. Click chọn **Next**.
3. Xác nhận lại các điều khoản dịch vụ (Terms and Conditions) của AWS và Registrar partner.
4. Click chọn **Submit** để hoàn tất gửi yêu cầu đăng ký.

---

### Bước 3: Xác minh Email & Kiểm tra Tiến độ Đăng ký
1. **Kiểm tra Email của bạn:** Hệ thống DNS Registry sẽ gửi một email xác minh đến địa chỉ email bạn đã khai báo ở Bước 2. Bạn bắt buộc phải nhấp chọn liên kết xác minh (Verification Link) trong email này để hoàn tất thủ tục đăng ký tên miền.
2. **Kiểm tra trên AWS Console:**
   * Di chuyển tới mục **Requests** ở menu bên trái trong Route 53.
   * Tại đây bạn sẽ thấy yêu cầu đăng ký `Register domain` đang ở trạng thái *In progress*.
   * Chờ khoảng **5 - 15 phút**, tải lại trang và xác nhận trạng thái (Status) hiển thị là **Successful** (Thành công).
3. **Hosted Zone được tạo tự động:** 
   * Sau khi đăng ký thành công, hãy di chuyển tới mục **Hosted zones** ở menu bên trái.
   * Bạn sẽ thấy một Hosted Zone mới tương ứng với tên miền vừa mua (ví dụ: `h1eudayne.click`) đã được Route 53 tự động khởi tạo.
   * Hosted Zone này đã được điền sẵn 2 bản ghi mặc định cực kỳ quan trọng là **NS (Name Servers)** và **SOA (Start of Authority)**.

---

> [!CAUTION]
> **LƯU Ý TỐI ƯU CHI PHÍ:**
> Mặc định khi mua tên miền, AWS sẽ bật tính năng tự động gia hạn (Auto-renew) hàng năm. Nếu bạn chỉ mua tên miền cho mục đích học tập và làm Lab, hãy thực hiện tắt tính năng này để tránh phát sinh chi phí ngoài ý muốn vào năm sau:
> 1. Vào Route 53 > **Registered domains** > Click chọn tên miền vừa mua.
> 2. Tại phần cấu hình chi tiết, tìm mục **Auto-renew** và chuyển từ **Enabled** sang **Disabled**.
