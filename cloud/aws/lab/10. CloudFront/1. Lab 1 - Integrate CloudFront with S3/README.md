# Lab 1 - Sử dụng CloudFront kết hợp với S3 - Hướng dẫn chi tiết

 **[Xem Đề bài / Yêu cầu bài Lab](1.%20Lab%201%20-%20Integrate%20CloudFront%20with%20S3.md)**

---

## Các bước thực hiện chi tiết

### Bước 1: Tạo Amazon S3 Bucket và tải tệp trang chủ lên

Trước tiên, chúng ta cần một kho lưu trữ để chứa các tệp tĩnh của trang web:

1. Đăng nhập vào AWS Console, truy cập dịch vụ **Amazon S3** và chọn **Create bucket**.
2. Thiết lập cấu hình bucket:
   * **Bucket name**: Nhập một tên duy nhất toàn cầu (ví dụ: `vduc-cloudfront-s3-lab-01`).
   * **Region**: Chọn region gần bạn (ví dụ: `us-east-1` hoặc `ap-southeast-1`).
   * **Object Ownership**: Giữ mặc định (*ACLs disabled*).
   * **Block Public Access settings for this bucket**: Đảm bảo tích chọn **Block *all* public access** để chặn hoàn toàn truy cập công khai.
3. Click chọn **Create bucket** ở dưới cùng.
4. Tạo một tệp tin đơn giản tên là `index.html` trên máy tính với nội dung sau:
   ```html
   <!DOCTYPE html>
   <html>
   <head>
       <title>CloudFront S3 Lab</title>
       <meta charset="UTF-8">
       <style>
           body { font-family: Arial, sans-serif; text-align: center; padding-top: 100px; background-color: #f4f6f9; }
           h1 { color: #ff9900; }
           .container { border: 1px solid #ccc; padding: 20px; background: white; max-width: 600px; margin: 0 auto; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
       </style>
   </head>
   <body>
       <div class="container">
           <h1>Chào mừng bạn đến với Amazon CloudFront!</h1>
           <p>Tài nguyên này được lưu trữ an toàn trên Amazon S3 và phân phối qua CloudFront OAC.</p>
       </div>
   </body>
   </html>
   ```
5. Click chọn bucket vừa tạo -> Click **Upload** -> Chọn tệp `index.html` vừa tạo và tải lên.

---

### Bước 2: Khởi tạo CloudFront Distribution

Tiếp theo, ta tạo bản phân phối CloudFront để làm cổng truy cập duy nhất cho S3 bucket:

1. Truy cập dịch vụ **CloudFront** trên AWS Console.
2. Click chọn nút **Create distribution**.
3. Tại mục **Origin**:
   * **Origin domain**: Nhấp chuột vào ô tìm kiếm và chọn tên S3 bucket vừa tạo ở Bước 1.
   * **Origin access**: Tích chọn **Origin access control settings (recommended)**.
   * **Origin access control (OAC)**: Click chọn **Create control setting** ở bên cạnh. Giữ nguyên tên mặc định và nhấn **Create** để hệ thống tạo thực thể OAC liên kết.
4. Tại mục **Default cache behavior**:
   * **Viewer protocol policy**: Chọn **Redirect HTTP to HTTPS** để tự động chuyển hướng các request HTTP thường sang HTTPS bảo mật.
   * **Allowed HTTP methods**: Chọn `GET, HEAD`.
5. Tại mục **Cache key and origin requests**:
   * Chọn **Cache policy**: Chọn chính sách mặc định tối ưu **`CachingOptimized`**.
6. Tại mục **Web Application Firewall (WAF)**:
   * Chọn **Do not enable security protections** để tránh phát sinh chi phí WAF trong quá trình thực hành Lab.
7. Cuộn xuống dưới cùng và click chọn **Create distribution**.

---

### Bước 3: Cập nhật S3 Bucket Policy cho phép CloudFront OAC truy cập

Sau khi Distribution được khởi tạo, bạn sẽ thấy một biểu ngữ thông báo màu xanh lá cây ở đầu trang có nội dung: *"The S3 bucket policy needs to be updated..."*.

1. Click chọn nút **Copy policy** hiển thị trên biểu ngữ để sao chép đoạn cấu hình JSON tự động sinh ra.
2. Quay lại dịch vụ **Amazon S3**, click chọn S3 bucket `vduc-cloudfront-s3-lab-01` của bạn.
3. Di chuyển sang tab **Permissions** (Quyền truy cập).
4. Cuộn xuống phần **Bucket policy** -> Click chọn **Edit**.
5. Dán đoạn mã JSON vừa copy ở trên vào ô nhập liệu. Đoạn mã có dạng tương tự như sau:
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
               "Resource": "arn:aws:s3:::vduc-cloudfront-s3-lab-01/*",
               "Condition": {
                   "StringEquals": {
                       "AWS:SourceArn": "arn:aws:cloudfront::<Account_ID>:distribution/<CF_Distribution_ID>"
                   }
               }
           }
       ]
   }
   ```
6. Click chọn nút **Save changes** để lưu chính sách bảo mật mới.

---

### Bước 4: Kiểm thử và Xác minh

Bây giờ cấu hình đã hoàn tất, chúng ta tiến hành kiểm chứng:

#### 1. Kiểm thử truy cập trực tiếp qua S3 (Bị chặn)
1. Trong giao diện S3 bucket, click chọn đối tượng `index.html`.
2. Sao chép địa chỉ **Object URL** ở phần Object Overview.
3. Mở một tab ẩn danh trên trình duyệt và dán link này vào.
4. **Kết quả**: Bạn sẽ nhận được trang thông báo lỗi **`403 Forbidden` / Access Denied** từ S3. Điều này xác nhận rằng tệp tin S3 được bảo vệ hoàn toàn và không ai có thể truy cập trực tiếp.

#### 2. Kiểm thử truy cập qua CloudFront (Thành công)
1. Quay lại dịch vụ **CloudFront**, click chọn distribution của bạn.
2. Tại phần *Details*, sao chép địa chỉ **Distribution domain name** (có dạng `d111111abcdef8.cloudfront.net`).
3. Mở trình duyệt và truy cập tên miền này kèm theo tên file: `https://d111111abcdef8.cloudfront.net/index.html`.
4. **Kết quả**: Trang web HTML hiển thị đầy đủ giao diện thiết kế chào mừng. Đường truyền được tự động bảo mật qua HTTPS.

---

### Bước 5: Tìm hiểu cơ chế invalidate cache khi cập nhật mã nguồn

Khi tệp tĩnh được cache ở Edge Location, nếu bạn thay đổi nội dung tệp trên S3, CloudFront vẫn sẽ phân phối tệp cũ cho đến khi TTL hết hạn. Để làm mới ngay lập tức:

1. Chỉnh sửa tệp `index.html` trên máy tính (ví dụ sửa chữ "Amazon CloudFront" thành "Amazon CloudFront v2").
2. Upload đè tệp `index.html` mới này lên S3 bucket của bạn.
3. Truy cập lại link CloudFront: Hệ thống vẫn sẽ hiển thị trang cũ do chưa hết thời gian cache.
4. Vào lại trang quản lý **CloudFront Distribution** -> Chọn tab **Invalidations**.
5. Click chọn **Create invalidation**.
6. Tại ô *Object paths*, nhập `/index.html` (hoặc `/*` để xóa cache toàn bộ distribution).
7. Nhấn **Create invalidation** và chờ trạng thái chuyển từ *In progress* sang *Completed* (mất khoảng 1-2 phút).
8. F5 lại trình duyệt, bạn sẽ thấy nội dung mới đã được cập nhật thành công.

---

* **Bài trước**: Không có
* **Bài tiếp theo**: [2. Lab 2 – Sử dụng CloudFront kết hợp với API Gateway and S3](../2.%20Lab%202%20-%20Integrate%20CloudFront%20with%20API%20Gateway%20and%20S3/2.%20Lab%202%20-%20Integrate%20CloudFront%20with%20API%20Gateway%20and%20S3.md)
