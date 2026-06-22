# Lab 1 - Sử dụng CloudFront kết hợp với S3 - Hướng dẫn chi tiết

 **[Xem Đề bài / Yêu cầu bài Lab](1.%20Lab%201%20-%20Integrate%20CloudFront%20with%20S3.md)**

---

## So sánh hai phương thức tích hợp CloudFront với S3

Trước khi bắt đầu thực hành, hãy nắm rõ sự khác biệt giữa hai phương thức tích hợp chính dưới đây để áp dụng chính xác cho từng dự án:

| Tiêu chí | Phương pháp 1: S3 Website Endpoint (Custom HTTP Origin) | Phương pháp 2: S3 REST API Endpoint + OAC (Khuyên dùng) |
| :--- | :--- | :--- |
| **Sự phù hợp** | Dành cho các website tĩnh tận dụng tính năng định hướng (routing/redirect rules) của S3 Website Hosting. | Dành cho các website cần bảo mật tối đa, không để lộ dữ liệu nguồn trên S3. |
| **Chế độ S3 Bucket** | Bắt buộc phải bật **Public Access** và cấu hình public bucket policy. | Bucket ở chế độ **Private hoàn toàn** (Block all public access). |
| **Bảo mật mạng** | Người dùng vẫn có thể bypass CloudFront truy cập trực tiếp qua S3 HTTP URL. | Chặn hoàn toàn truy cập trực tiếp S3. Chỉ có thể đi qua cổng CloudFront. |
| **Cơ chế xác thực** | Không sử dụng OAC. CloudFront coi S3 như một máy chủ web ngoài (HTTP). | Sử dụng **Origin Access Control (OAC)** ký số cho mọi request từ CloudFront. |

> [!NOTE]
> **Lưu ý bổ sung (Cập nhật từ tháng 10/2025):**
> Kể từ tháng 10/2025, nếu S3 bucket được cấu hình ở chế độ **Private** và **Block all public access** nhưng vẫn bật tính năng **Static Website Hosting**, thì CloudFront vẫn có thể truy cập và phân phối dữ liệu từ S3 Website Endpoint bình thường mà không bị lỗi 403 Forbidden.

---

## PHƯƠNG PHÁP 1: Tích hợp với S3 Static Website Hosting Endpoint (Theo thực tế cấu hình)

*Phương pháp này tương ứng trực tiếp với cấu hình thực tế trong các ảnh chụp màn hình console của bạn.*

### Bước 1: Chuẩn bị website tĩnh trên S3 (S3 Lab đã hoàn tất)
1. Đảm bảo bạn đã hoàn thành bài thực hành S3 Static Website Hosting trước đó cho bucket `h1eudayne`.
2. Kiểm tra trạng thái hoạt động của website tĩnh tại đường link endpoint S3:
   `http://h1eudayne.s3-website-us-east-1.amazonaws.com`
   *(Trang web Dimension hoặc trang chủ đơn giản hiển thị thành công).*

### Bước 2: Khởi tạo CloudFront Distribution
1. Đăng nhập vào AWS Console, tìm kiếm dịch vụ **CloudFront**.
2. Tại màn hình quản lý Distributions, click chọn **Create distribution**.

   ![Giao diện CloudFront Distributions Dashboard](../../../../images/aws/cloudfront_logo.png) *(Hoặc nhấn nút Create distribution tại màn hình chính)*

3. **Cấu hình Step 2 - Get started (Bắt đầu):**
   * **Distribution name:** Nhập `demo-cloudfront`.
   * **Description - optional:** Nhập `demo-cloudfront`.
   * **Distribution type:** Tích chọn **Single website or app** (Lưu trữ đơn website hoặc ứng dụng).
   * **Domain (Route 53 managed domain - optional):** Để trống nếu chưa cấu hình DNS Route 53.
   * Click **Next**.

4. **Cấu hình Step 3 - Specify origin (Xác định nguồn phát):**
   * **Origin type:** Chọn **Amazon S3**.
   * **S3 origin:** Nhập hoặc dán địa chỉ S3 Website Endpoint của bạn:
     `h1eudayne.s3-website-us-east-1.amazonaws.com`
   * **Origin settings:** Tích chọn **Use recommended origin settings** (Sử dụng cấu hình đề xuất).
   * **Cache settings:** Tích chọn **Use recommended cache settings tailored to serving S3 content** (Sử dụng chính sách bộ đệm tối ưu cho S3).
   * Click **Next**.

5. **Cấu hình Step 4 - Enable security (Kích hoạt bảo mật):**
   * AWS mặc định đề xuất bật WAF bảo vệ. Trong lab này, hệ thống cấu hình **Security protections: Enabled** (WAF được bật ở chế độ cơ bản).
   * Click **Next**.

6. **Cấu hình Step 5 - Review and create (Kiểm tra và khởi tạo):**
   * Xem lại toàn bộ thông tin cấu hình:
     * **General configuration:** Name: `demo-cloudfront`, Billing: Free ($0/month).
     * **Origin:** S3 origin: `h1eudayne.s3-website-us-east-1.amazonaws.com`, Origin path: `-`, Connection attempts: `3`.
     * **Cache settings:** Áp dụng mặc định cho S3.
     * **Security:** Security protections: `Enabled`.
   * Nhấp chọn **Create distribution** ở góc dưới cùng bên phải và chờ trạng thái phân phối chuyển sang hoạt động (Deployed/Active).

---

## PHƯƠNG PHÁP 2: Tích hợp bảo mật sử dụng S3 REST API & OAC (Khuyên dùng trong môi trường Product)

*Nếu bạn muốn chuyển sang giải pháp bảo mật cao hơn, hãy làm theo các bước sau đây để khóa S3 Bucket về Private và cấu hình OAC:*

### Bước 1: Khóa Public Access của S3 Bucket
1. Truy cập dịch vụ **Amazon S3** > Click chọn bucket `h1eudayne`.
2. Di chuyển sang tab **Permissions** (Quyền truy cập).
3. Tại phần **Block public access (bucket settings)**, click chọn **Edit** > Tích chọn **Block *all* public access** > Nhấn **Save changes** và nhập `confirm`.

### Bước 2: Tạo CloudFront Distribution trỏ tới S3 REST và tạo OAC
1. Truy cập dịch vụ **CloudFront** > Chọn **Create distribution**.
2. Cấu hình phần **Origin**:
   * **Origin domain:** Chọn đúng tên S3 bucket từ danh sách gợi ý (dạng `h1eudayne.s3.amazonaws.com` - đây là REST API endpoint, không chứa chữ `-website`).
   * **Origin access:** Tích chọn **Origin access control settings (recommended)**.
   * **Origin access control (OAC):** Nhấn **Create control setting** > Giữ nguyên tên mặc định và click **Create**.
3. Cấu hình phần **Default cache behavior**:
   * **Viewer protocol policy:** Chọn **Redirect HTTP to HTTPS** (Tự động chuyển hướng sang HTTPS bảo mật).
   * **Allowed HTTP methods:** Chọn `GET, HEAD`.
4. Cấu hình phần **Cache key and origin requests**:
   * **Cache policy:** Chọn chính sách tối ưu sẵn **`CachingOptimized`**.
5. Cấu hình **Web Application Firewall (WAF)**:
   * Chọn *Do not enable security protections* (nếu muốn tối ưu chi phí trong môi trường thử nghiệm).
6. Cuộn xuống dưới cùng và click chọn **Create distribution**.

### Bước 3: Cập nhật S3 Bucket Policy cho phép OAC truy cập
1. Sau khi tạo xong distribution, sao chép cấu hình policy JSON được sinh ra tự động (nhấp nút **Copy policy** từ thanh thông báo màu xanh lá).
2. Quay lại tab **Permissions** của S3 bucket `h1eudayne` > Phần **Bucket policy** > Chọn **Edit**.
3. Dán đoạn JSON vừa copy vào. Đoạn policy sẽ tương tự như sau:
   ```json
   {
       "Version": "2008-10-17",
       "Id": "PolicyForCloudFrontPrivateContent",
       "Statement": [
           {
               "Sid": "AllowCloudFrontServicePrincipal",
               "Effect": "Allow",
               "Principal": {
                   "Service": "cloudfront.amazonaws.com"
               },
               "Action": "s3:GetObject",
               "Resource": "arn:aws:s3:::h1eudayne/*",
               "Condition": {
                   "StringEquals": {
                       "AWS:SourceArn": "arn:aws:cloudfront::<Account_ID>:distribution/<CF_Distribution_ID>"
                   }
               }
           }
       ]
   }
   ```
4. Chọn **Save changes**.

---

## Hướng dẫn Kiểm thử & So sánh Tốc độ (S3 vs CloudFront)

### 1. Lấy thông tin Tên miền CloudFront (Distribution Domain Name)
1. Truy cập dịch vụ **CloudFront** > click chọn distribution của bạn (`demo-cloudfront`).
2. Tại tab **Details**, sao chép địa chỉ **Distribution domain name** (Ví dụ thực tế trong lab: `dyef164pbgy7w.cloudfront.net`).

---

### 2. So sánh tốc độ tải tài nguyên (Ví dụ với tệp hình ảnh dung lượng 4.7 MB)

Để thấy rõ sự khác biệt của CDN CloudFront trong việc tối ưu hóa hiệu năng, chúng ta thực hiện tải một hình ảnh `/images/20230408_010527653_iOS.jpg` (dung lượng 4.7 MB) và quan sát tab **Network** trong Chrome DevTools:

#### Kịch bản 1: Truy cập trực tiếp qua S3 Web Endpoint
* **Địa chỉ truy cập:** `http://h1eudayne.s3-website-us-east-1.amazonaws.com/images/20230408_010527653_iOS.jpg`
* **Kết quả đo lường thực tế:** Thời gian tải tệp tin mất khoảng **3.72 giây (≈ 4s)**.
* **Nguyên nhân:** Dữ liệu phải được truyền tải trực tiếp từ S3 bucket (nằm tại Region `us-east-1` - Bắc Virginia, Mỹ) vượt khoảng cách địa lý xa xôi về máy người dùng.

#### Kịch bản 2: Truy cập qua CloudFront Distribution
* **Địa chỉ truy cập:** `http://dyef164pbgy7w.cloudfront.net/images/20230408_010527653_iOS.jpg`
* **Kết quả đo lường thực tế:**
  * **Lần đầu tiên (Cache Miss):** Tốc độ tải tương đương với S3 (~4 giây) do CloudFront phải gửi request về S3 để lấy dữ liệu lần đầu và ghi vào Cache.
  * **Từ lần thứ hai trở đi (Cache Hit):** Thời gian tải giảm đột biến chỉ còn **312 miligiây (≈ 300ms)**!
* **Nguyên nhân:** CloudFront đã lưu tệp hình ảnh vào bộ nhớ đệm tại máy chủ Edge Location gần người dùng nhất. Ở các lượt truy cập sau, tài nguyên được phân phối tức thì từ Edge Location mà không cần quay lại S3 Origin nữa.

> [!TIP]
> Tốc độ cải thiện **gấp hơn 10 lần** (~3.7s giảm xuống còn ~300ms) chính là minh chứng rõ ràng nhất cho hiệu quả của CloudFront Caching khi triển khai các website tĩnh có nhiều tài nguyên hình ảnh, media.

---

### 3. Xoá Cache khi cập nhật giao diện web (Invalidations)
Khi thay đổi mã nguồn trên S3, để khách hàng nhận được giao diện mới ngay lập tức mà không phải chờ hết thời gian TTL (Cache expiry):
1. Chỉnh sửa nội dung tệp `index.html` trên máy tính và upload đè lên S3.
2. Truy cập trang quản trị **CloudFront Distribution** vừa tạo.
3. Chọn tab **Invalidations** > Click chọn **Create invalidation**.
4. Tại ô nhập **Object paths**, gõ `/index.html` (hoặc `/*` để xóa sạch toàn bộ cache của website) > Nhấn **Create invalidation**.
5. Đợi trạng thái chuyển từ *In progress* sang *Completed* (khoảng 1 phút), tải lại trình duyệt để xem kết quả cập nhật.

---

* **Bài trước**: Không có
* **Bài tiếp theo**: [2. Lab 2 – Sử dụng CloudFront kết hợp với API Gateway and S3](../2.%20Lab%202%20-%20Integrate%20CloudFront%20with%20API%20Gateway%20and%20S3/2.%20Lab%202%20-%20Integrate%20CloudFront%20with%20API%20Gateway%20and%20S3.md)
