# Lab 3 - Thực hành CNAME Record (Tích hợp CloudFront & ACM) - Hướng dẫn chi tiết

  **[Xem Đề bài / Yêu cầu bài Lab](3.%20Lab%203%20-%20CNAME%20Record.md)**

---

## Các bước thực hiện chi tiết

### Bước 1: Yêu cầu cấp chứng chỉ SSL/TLS từ AWS Certificate Manager (ACM)
1. Đăng nhập AWS Console và mở dịch vụ **Certificate Manager** (ACM).
2. **Cực kỳ quan trọng:** Nhìn lên thanh điều hướng góc trên bên phải, kiểm tra Region hiện tại. Bạn **bắt buộc** phải chuyển sang **`us-east-1` (US East - N. Virginia)** để tạo chứng chỉ cho CloudFront.
3. Click chọn nút **Request a certificate** > Chọn loại **Request a public certificate** > Click **Next**.
4. Cấu hình thông tin chứng chỉ:
   * **Domain names:** Nhập tên miền phụ bạn muốn sử dụng (ví dụ: `web.h1eudayne.click`).
     > [!TIP]
     > Bạn cũng có thể yêu cầu chứng chỉ bao phủ wildcard bằng cách thêm `*.h1eudayne.click` để sử dụng cho nhiều subdomain khác nhau.
   * **Validation method:** Chọn **DNS validation - recommended** (Xác thực qua DNS).
   * **Key algorithm:** Chọn **RSA 2048** (Mặc định).
5. Click chọn **Request**.

---

### Bước 2: Tạo bản ghi xác thực DNS sở hữu tên miền trên Route 53
1. Sau khi gửi yêu cầu, click vào **Certificate ID** của chứng chỉ vừa yêu cầu từ bảng danh sách.
2. Tại phần cấu hình chi tiết, cuộn xuống mục **Domains**. Bạn sẽ thấy trạng thái của domain hiển thị là *Pending validation*.
3. Nhấp chọn nút **Create records in Route 53**.
4. AWS ACM sẽ tự động hiển thị bản ghi CNAME xác thực tương ứng trong Hosted Zone được quản lý bởi Route 53 của bạn. Click chọn **Create records**.
5. Chờ khoảng **1 - 3 phút** để DNS đồng bộ và trạng thái của chứng chỉ chuyển sang màu xanh lá **Issued** (Đã phát hành).

---

### Bước 3: Tạo bản ghi CNAME trỏ subdomain về CloudFront
Chúng ta cần cấu hình bản ghi để điều hướng lưu lượng truy cập từ tên miền phụ tới CloudFront Distribution:
1. Mở dịch vụ **Route 53** > **Hosted zones** > Click chọn Hosted Zone tên miền của bạn (`h1eudayne.click`).
2. Click chọn **Create record**.
3. Cấu hình bản ghi CNAME:
   * **Record name:** Nhập `web` (Tên miền phụ sẽ có dạng `web.h1eudayne.click`).
   * **Record type:** Chọn **CNAME – Routes traffic to another domain name and to some AWS resources**.
   * **Alias:** Để tắt (**No**).
   * **Value:** Dán địa chỉ **Distribution domain name** mặc định của CloudFront (ví dụ: `dyef164pbgy7w.cloudfront.net`).
   * **TTL (seconds):** Giữ mặc định `300`.
   * **Routing policy:** Chọn `Simple routing`.
4. Click chọn **Create records**.

---

### Bước 4: Khai báo Custom Domain (Alternate Domain) và SSL trên CloudFront
Sau khi hoàn tất cấu hình DNS, ta cần khai báo để CloudFront chấp nhận các request đi từ tên miền phụ:
1. Mở dịch vụ **CloudFront** > Click chọn Distribution của bạn.
2. Tại tab **General**, cuộn xuống tìm phần **Settings** > Click chọn **Edit**.
3. Tại phần cấu hình:
   * **Alternate domain name (CNAME):** Click chọn **Add item** và nhập đúng tên miền phụ: `web.h1eudayne.click`.
   * **Custom SSL certificate:** Click vào ô chọn và tìm đúng tên chứng chỉ SSL bảo mật cho domain `web.h1eudayne.click` (hoặc wildcard `*.h1eudayne.click`) bạn đã tạo thành công ở Bước 1.
4. Cuộn xuống dưới cùng và click chọn **Save changes**.
5. Đợi trạng thái của CloudFront chuyển từ *In progress* sang thời gian cập nhật cụ thể (Đã Deployed xong).

---

### Bước 5: Kiểm thử và Xác minh qua HTTPS
1. Mở một trình duyệt ẩn danh (Incognito).
2. Truy cập địa chỉ tên miền riêng qua giao thức an toàn HTTPS:
   `https://web.h1eudayne.click`
3. **Kết quả:** Website tĩnh hiển thị thành công. Click biểu tượng **ổ khóa** ở góc trái thanh địa chỉ trình duyệt để kiểm tra chi tiết thông tin chứng chỉ SSL được cấp bởi Amazon Web Services an toàn.

> [!WARNING]
> Nếu bạn truy cập ngay lập tức sau khi cấu hình và gặp lỗi trình duyệt cảnh báo kết nối không an toàn ("Not secure"), hãy kiên nhẫn chờ 3-5 phút để mạng lưới Edge Location của CloudFront đồng bộ xong cấu hình SSL mới. Sau đó tải lại trang để lỗi bảo mật biến mất.
