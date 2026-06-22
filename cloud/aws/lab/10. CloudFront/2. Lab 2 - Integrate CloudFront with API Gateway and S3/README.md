# Lab 2 - Sử dụng CloudFront kết hợp với API Gateway and S3 - Hướng dẫn chi tiết

 **[Xem Đề bài / Yêu cầu bài Lab](2.%20Lab%202%20-%20Integrate%20CloudFront%20with%20API%20Gateway%20and%20S3.md)**

---

## Các bước thực hiện chi tiết

### Bước 1: Chuẩn bị cấu hình (Setup) trên API Gateway

Trước khi tích hợp qua CloudFront, ta cần loại bỏ các lớp xác thực tạm thời trên API Gateway để kiểm thử định tuyến dễ dàng hơn:

1. Đăng nhập vào AWS Console, mở dịch vụ **API Gateway** và chọn API của bạn (ví dụ: `test-api` - `da0brxb62b`).
2. Di chuyển tới mục **Resources** ở menu bên trái > Chọn tài nguyên `/calculate` > phương thức **POST**.
3. Tại tab **Method request**, kiểm tra cấu hình hiện tại (ở các lab trước đang yêu cầu Cognito Authorizer và API Key). Nhấp chọn nút **Edit** ở góc phải phần *Method request settings*.

   ![Cấu hình Method Request lúc đầu](../../../../../images/aws/cloudfront_apigw_method_settings.png)
   *Hình 1: Trạng thái thiết lập Method Request ban đầu với Authorizer và API Key.*

4. Trong màn hình chỉnh sửa:
   * **Authorization**: Chọn **None** (Chuyển tất cả bộ xác thực về None).
   * **API key required**: Bỏ tích chọn (Thiết lập thành False/Không yêu cầu).
5. Click chọn **Save**.

   ![Chuyển Authorization về None và tắt API Key](../../../../../images/aws/cloudfront_apigw_edit_method.png)
   *Hình 2: Chuyển cấu hình Method request về None và tắt yêu cầu API key.*

6. **Lưu ý cực kỳ quan trọng:** Sau khi lưu, bạn phải nhấn chọn nút **Deploy API** ở góc trên bên phải > Chọn Stage tương ứng (ví dụ: `dev`) > Click **Deploy** để các thay đổi này chính thức có hiệu lực trên Internet.

---

### Bước 2: Thêm API Gateway làm Origin cho CloudFront

Chúng ta sẽ khai báo thêm API Gateway làm nguồn gốc (Origin) thứ hai cho bản phân phối CloudFront:

1. Truy cập dịch vụ **CloudFront** trên AWS Console.
2. Click chọn Distribution của bạn (ví dụ: `demo-cloudfront` - ID: `E26CV1JX0F3ALC`).
3. Chuyển sang tab **Origins** > Click chọn nút **Create origin**.

   ![Xem tab Origins hiện tại](../../../../../images/aws/cloudfront_apigw_cf_origins.png)
   *Hình 3: Giao diện tab Origins hiển thị danh sách các nguồn hiện tại - Chọn Create origin.*

4. Thiết lập cấu hình Origin mới:
   * **Origin domain**: Dán địa chỉ Endpoint API Gateway của bạn (ví dụ: `da0brxb62b.execute-api.us-east-1.amazonaws.com`).
   * **Protocol**: Tích chọn **HTTPS only** (API Gateway bắt buộc kết nối bảo mật).
   * **Origin path - optional**: **Để trống** (không điền Stage name `/dev` ở đây như thực tế cấu hình trong ảnh chụp màn hình).
   * **Name**: Nhập `my-custom-api-gateway` (hoặc tên bất kỳ bạn tự chọn).
   * Các mục khác giữ nguyên mặc định.
5. Click chọn nút **Create origin**.

   ![Cấu hình Create Origin trỏ tới API Gateway](../../../../../images/aws/cloudfront_apigw_cf_create_origin.png)
   *Hình 4: Thiết lập thông số và domain API Gateway làm HTTP Origin mới.*

---

### Bước 3: Tạo Cache Behavior định tuyến cho API động

Sau khi đã có 2 Origins (S3 chứa web tĩnh và API Gateway xử lý logic động), chúng ta cần tạo quy luật định tuyến (Behavior) trên CloudFront:

1. Di chuyển sang tab **Behaviors** > Click chọn nút **Create behavior**.
2. Thiết lập thông số Behavior:
   * **Path pattern**: Nhập `/dev/calculate`.
     * *Giải thích quan trọng:* Do ở Bước 2 chúng ta để trống **Origin path**, nên Path pattern bắt buộc phải bao gồm cả Stage name `/dev` của API Gateway. Khi người dùng gọi tới `https://<CF_domain>/dev/calculate`, CloudFront sẽ chuyển tiếp nguyên vẹn đường dẫn này tới API Gateway Origin, khớp chính xác cấu trúc Stage và tài nguyên của API.
   * **Origin**: Chọn Origin API Gateway vừa tạo ở Bước 2 (`my-custom-api-gateway`).
   * **Viewer protocol policy**: Chọn **Redirect HTTP to HTTPS** (Tự động nâng cấp kết nối bảo mật).
   * **Allowed HTTP methods**: Chọn **`GET, HEAD, OPTIONS, PUT, POST, PATCH, DELETE`** (Bắt buộc phải bật đầy đủ phương thức để hỗ trợ request POST gửi dữ liệu tính toán).
3. Tại mục **Cache key and origin requests**:
   * **Cache policy**: Chọn **`CachingDisabled`**.
     * *Lưu ý quan trọng:* Chúng ta tuyệt đối không lưu cache kết quả tính toán động của API, mỗi request gửi lên bắt buộc phải chuyển trực tiếp về Lambda xử lý.
   * **Origin request policy**: Chọn **`AllViewer`**.
     * *Lưu ý quan trọng:* Đảm bảo chuyển tiếp đầy đủ Headers, Query Strings và Request Body từ người dùng xuống API Gateway.
4. Click chọn nút **Create behavior**.
5. Đảm bảo thứ tự ưu tiên (Precedence) tại bảng danh sách Behaviors:
   * **Thứ tự 0**: Path `/dev/calculate` trỏ tới API Gateway.
   * **Thứ tự 1 (Default `*`)**: Path mặc định trỏ tới S3 bucket.

---

### Bước 4: Kiểm thử và Xác minh

Chờ trạng thái của CloudFront Distribution chuyển từ *Deploying* sang hoàn tất (Last modified hiển thị mốc thời gian cụ thể).

#### 1. Kiểm thử định tuyến API động qua tên miền CloudFront
1. Mở Postman hoặc một công cụ test API, cấu hình request **POST**.
2. **Địa chỉ URL:** Sử dụng tên miền mặc định của CloudFront hoặc Custom Domain bạn đã cấu hình ở Lab 1 kèm đường dẫn `/dev/calculate`:
   * Cú pháp: `https://<CF_domain>/dev/calculate` hoặc `https://web.h1eudayne.click/dev/calculate`
3. Tại tab **Body**, cấu hình định dạng JSON gửi phép tính cộng:
   ```json
   {
       "firstName": 10,
       "secondNum": 20,
       "operator": "ADD"
   }
   ```
4. Click chọn **Send**.
5. **Kết quả:** Trả về mã phản hồi **`200 OK`** cùng kết quả tính toán chính xác (`30`) từ Lambda Backend. Điều này xác nhận CloudFront đã phân tuyến chính xác request động `/dev/*` tới API Gateway mà không bị cache.

#### 2. Kiểm thử định tuyến trang tĩnh S3
1. Truy cập `https://<CF_domain>/index.html` hoặc `https://web.h1eudayne.click/index.html` trên trình duyệt.
2. **Kết quả:** Trang web tĩnh DIMENSION hiển thị bình thường. (Do đường dẫn không khớp với `/dev/calculate` nên được định tuyến về S3 thông qua Default Behavior `*`).

---

* **Bài trước**: [1. Lab 1 – Sử dụng CloudFront kết hợp với S3](../1.%20Lab%201%20-%20Integrate%20CloudFront%20with%20S3/1.%20Lab%201%20-%20Integrate%20CloudFront%20with%20S3.md)
* **Bài tiếp theo**: Sắp ra mắt (Coming soon...)
