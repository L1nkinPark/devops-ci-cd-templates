# Lab 2 - Sử dụng CloudFront kết hợp với API Gateway and S3 - Hướng dẫn chi tiết

 **[Xem Đề bài / Yêu cầu bài Lab](2.%20Lab%202%20-%20Integrate%20CloudFront%20with%20API%20Gateway%20and%20S3.md)**

---

## Các bước thực hiện chi tiết

### Bước 1: Thêm API Gateway Origin vào CloudFront Distribution

Chúng ta sẽ cấu hình thêm một Origin mới để CloudFront biết cách kết nối tới API Gateway:

1. Truy cập dịch vụ **CloudFront** trên AWS Console.
2. Click chọn bản phân phối (Distribution) đã tạo ở Lab 1.
3. Chuyển sang tab **Origins** -> Click chọn nút **Create origin**.
4. Thiết lập cấu hình Origin mới:
   * **Origin domain**: Nhập hoặc chọn tên miền của API Gateway Stage (ví dụ: `da0brxb62b.execute-api.us-east-1.amazonaws.com`).
   * **Protocol**: Tích chọn **HTTPS only** (API Gateway bắt buộc kết nối bảo mật).
   * **Origin path - optional**: Nhập `/dev` (đây là Stage Name đã tạo trên API Gateway. Việc điền này giúp CloudFront tự động ánh xạ phần tiền tố stage khi gửi request về Origin).
   * Các mục khác giữ nguyên mặc định.
5. Click chọn nút **Create origin**.

---

### Bước 2: Khởi tạo Cache Behavior cho API động

Sau khi đã có 2 Origins (S3 cho tĩnh, API Gateway cho động), ta cần tạo Behavior để phân luồng request dựa trên đường dẫn:

1. Di chuyển sang tab **Behaviors** -> Click chọn nút **Create behavior**.
2. Thiết lập thông số Behavior:
   * **Path pattern**: Nhập `/calculate`.
     * *Lưu ý: Mọi request gửi tới địa chỉ `https://<CF_domain>/calculate` sẽ được xử lý bởi Behavior này và chuyển hướng về API Gateway Origin.*
   * **Origin**: Chọn Origin API Gateway vừa tạo ở Bước 1.
   * **Viewer protocol policy**: Chọn **Redirect HTTP to HTTPS**.
   * **Allowed HTTP methods**: Chọn **`GET, HEAD, OPTIONS, PUT, POST, PATCH, DELETE`** (Bắt buộc phải bật đầy đủ các phương thức để hỗ trợ request POST/PUT động của API).
3. Tại mục **Cache key and origin requests**:
   * **Cache policy**: Chọn **`CachingDisabled`**.
     * *Cực kỳ quan trọng: Chúng ta tuyệt đối không cache kết quả tính toán động của API, mỗi request gửi lên bắt buộc phải đẩy về Lambda xử lý trực tiếp.*
   * **Origin request policy**: Chọn **`AllViewer`** (hoặc `AllViewerAndCloudFrontHeaders-2022-06`).
     * *Cực kỳ quan trọng: Chính sách này đảm bảo CloudFront sẽ chuyển tiếp toàn bộ Headers (như `x-api-key`, `authorization`) và Request Body của Client xuống API Gateway để phục vụ việc xác thực và tính toán).*
4. Click chọn nút **Create behavior**.
5. Đảm bảo thứ tự ưu tiên (Precedence) tại bảng danh sách Behaviors:
   * **Thứ tự 0**: Path `/calculate` trỏ tới API Gateway.
   * **Thứ tự 1 (Default `*`)**: Path mặc định trỏ tới S3 bucket.

---

### Bước 3: Đợi CloudFront Deploy và tiến hành kiểm thử

Chờ trạng thái của Distribution chuyển từ *Deploying* sang hoàn tất (nút chuyển sang màu xám/không xoay vòng).

#### 1. Kiểm thử định tuyến trang tĩnh S3
1. Truy cập `https://<CF_domain>/index.html` trên trình duyệt.
2. Trang web tĩnh hiển thị bình thường. (Đường dẫn khớp với Default Behavior `*` nên định hướng tới S3).

#### 2. Kiểm thử định tuyến API động (Postman)
1. Mở Postman, cấu hình request POST.
2. Địa chỉ URL: Thay đổi domain API Gateway gốc thành **Tên miền CloudFront Distribution** của bạn.
   * Cú pháp: `https://<CF_domain>/calculate`
   * Ví dụ: `https://d111111abcdef8.cloudfront.net/calculate`
3. Tại tab **Headers**, đính kèm:
   * `x-api-key`: API Key của bạn (nếu API Gateway vẫn yêu cầu).
4. Tại tab **Authorization** (nếu API Gateway đang cấu hình Cognito Authorizer từ Lab 5):
   * Chọn **Bearer Token** và dán JWT ID Token của bạn vào.
5. Tại tab **Body**, gửi phép tính cộng:
   ```json
   {
       "firstName": 10,
       "secondNum": 20,
       "operator": "ADD"
   }
   ```
6. Click chọn nút **Send**.
7. **Kết quả**: Bạn sẽ nhận được mã phản hồi **`200 OK`** cùng kết quả tính toán chính xác (`30`) được xử lý bởi Lambda. Điều này chứng minh CloudFront đã nhận diện đường dẫn `/calculate`, bỏ qua cache, chuyển tiếp đầy đủ token/API key và body xuống API Gateway xử lý thành công.

---

* **Bài trước**: [1. Lab 1 – Sử dụng CloudFront kết hợp với S3](../1.%20Lab%201%20-%20Integrate%20CloudFront%20with%20S3/1.%20Lab%201%20-%20Integrate%20CloudFront%20with%20S3.md)
* **Bài tiếp theo**: Sắp ra mắt (Coming soon...)
