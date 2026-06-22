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

   ![Xem tab Behaviors hiện tại](../../../../../images/aws/cloudfront_apigw_cf_behaviors.png)
   *Hình 5: Danh sách Behaviors hiện tại của Distribution - Chọn Create behavior.*

2. Thiết lập thông số Behavior:
   * **Path pattern**: Nhập `/dev*` (dùng dấu wildcard để khớp với tất cả các API requests đi qua stage `/dev`).
   * **Origin**: Chọn Origin API Gateway vừa tạo ở Bước 2 (`my-custom-api-gateway`).
   * **Viewer protocol policy**: Chọn **Redirect HTTP to HTTPS** (Tự động nâng cấp kết nối bảo mật).
   * **Allowed HTTP methods**: Chọn **`GET, HEAD, OPTIONS, PUT, POST, PATCH, DELETE`** (Cho phép đầy đủ các phương thức để API hoạt động bình thường).
3. Tại mục **Cache key and origin requests**:
   * **Cache policy**: Chọn **`CachingDisabled`** (Tắt cache hoàn toàn đối với request API động).
   * **Origin request policy**: Chọn chính sách **`AllViewerExceptHostHeader`** (Đây là cấu hình khuyên dùng cho API Gateway không có custom domain để tránh lỗi không khớp Host header khi forward request).
4. Click chọn nút **Create behavior**.

   ![Cấu hình Create Behavior](../../../../../images/aws/cloudfront_apigw_cf_create_behavior.png)
   *Hình 6: Thiết lập chi tiết Path pattern /dev* và chính sách Caching/Origin Request.*

5. Đảm bảo thứ tự ưu tiên (Precedence) tại bảng danh sách Behaviors:
   * **Thứ tự 0**: Path `/dev*` trỏ tới API Gateway.
   * **Thứ tự 1 (Default `*`)**: Path mặc định trỏ tới S3 bucket.

---

### Bước 4: Kiểm thử và Xác minh

Sau khi cấu hình hoàn tất và CloudFront đã deploy xong (trạng thái Last modified hiển thị thời gian cụ thể), CloudFront sẽ đồng thời phục vụ **2 backend song song** thông qua một tên miền duy nhất (ở đây là Custom Domain `web.h1eudayne.click`).

#### 1. Kiểm thử định tuyến API động qua Custom Domain (Postman)
1. Mở Postman, cấu hình request **POST**.
2. **Địa chỉ URL:** Sử dụng tên miền riêng của bạn thay thế cho link API Gateway trực tiếp trước đây:
   `https://web.h1eudayne.click/dev/calculate`
3. Tại tab **Body**, dán payload JSON phép tính (ví dụ thực hiện phép tính `5 + 25`):
   ```json
   {
       "firstNum": 5,
       "secondNum": 25,
       "operator": "ADD"
   }
   ```
4. Click chọn **Send**.
5. **Kết quả:** Trả về mã phản hồi **`200 OK`** cùng kết quả tính toán chính xác từ Lambda Backend (`result: 30`). Điều này xác nhận CloudFront đã nhận diện tiền tố `/dev`, bỏ qua cache và chuyển tiếp chính xác request về API Gateway.

   ![Kết quả kiểm thử qua Postman](../../../../../images/aws/cloudfront_apigw_postman_test.png)
   *Hình 7: Postman gọi thành công qua Custom Domain CloudFront, trả về kết quả tính toán 30 từ Lambda.*

#### 2. Kiểm thử định tuyến trang tĩnh S3
1. Truy cập `https://web.h1eudayne.click/index.html` hoặc trực tiếp trang chủ trên trình duyệt.
2. **Kết quả:** Trang web tĩnh DIMENSION hiển thị bình thường. 
3. **Giải thích cơ chế:** Vì request này không khớp với Path pattern `/dev*`, nên CloudFront tự động khớp với Default Behavior (`*`) và định tuyến về S3 Origin để tải tệp tĩnh lên trình duyệt. Quy trình này diễn ra hoàn toàn trong suốt với người dùng.

---

## PHẦN MỞ RỘNG: Bật Lambda Proxy Integration & Cấu hình Custom Header từ CloudFront

*(Mục tiêu: Cấu hình API Gateway chuyển tiếp đầy đủ thông tin request xuống Lambda dạng structured event để in ra và kiểm nghiệm custom header `Source: CloudFront` do CloudFront tự động đính kèm khi gửi request tới Origin).*

### Bước 1: Bật Lambda Proxy Integration trên API Gateway
Mặc định, API Gateway không truyền đầy đủ headers và metadata của request xuống Lambda trừ khi ta kích hoạt tính năng Proxy Integration:
1. Vào **API Gateway** > Chọn API `test-api` (`da0brxb62b`) > **Resources** > Chọn `/calculate` > phương thức **POST**.
2. Nhấp chọn tab **Integration request**.

   ![Xem cấu hình Integration Request](../../../../../images/aws/cloudfront_apigw_lambda_proxy_settings.png)
   *Hình 8: Giao diện Integration request hiển thị trạng thái Lambda proxy integration ban đầu đang tắt (False).*

3. Click nút **Edit** ở góc phải mục *Integration request settings*.
4. Gạt nút bật **Lambda proxy integration** (chuyển sang trạng thái True).
5. Click chọn **Save**.

   ![Bật Lambda proxy integration](../../../../../images/aws/cloudfront_apigw_edit_lambda_proxy.png)
   *Hình 9: Kích hoạt Lambda proxy integration và click Save.*

6. **Quan trọng:** Chọn **Deploy API** lên stage `dev` để cập nhật cấu hình mới lên Internet.

### Bước 2: Cấu hình Custom Header trên CloudFront Origin
Ta sẽ cấu hình CloudFront tự động đính kèm thêm một header riêng khi gửi yêu cầu tới API Gateway:
1. Vào trang dịch vụ **CloudFront** > click chọn distribution `demo-cloudfront` (`E26CV1JX0F3ALC`).
2. Chuyển tới tab **Origins** > Tích chọn Origin API Gateway (`my-custom-api-gateway`) > Click **Edit**.

   ![Chọn Edit Origin trong CloudFront](../../../../../images/aws/cloudfront_apigw_edit_origin_tab.png)
   *Hình 10: Chọn Origin my-custom-api-gateway và nhấp Edit.*

3. Cuộn xuống mục **Add custom header - optional**:
   * **Header name:** Nhập `Source`
   * **Value:** Nhập `CloudFront`
4. Click chọn **Save changes**.

   ![Thêm custom header](../../../../../images/aws/cloudfront_apigw_edit_origin_custom_header.png)
   *Hình 11: Cấu hình thêm Custom Header Source: CloudFront cho API Gateway Origin.*

### Bước 3: Cập nhật mã nguồn Lambda để đọc Header và Body
Khi bật Lambda Proxy, cấu trúc dữ liệu truyền vào hàm Lambda (`event`) thay đổi sang định dạng JSON có khóa `headers` và `body` dạng string.
1. Cập nhật mã nguồn hàm Lambda backend của bạn theo tệp mẫu [calculator-lambda-new.py](calculator-lambda-new.py):
   ```python
   import json

   def lambda_handler(event, context):
       # Log thông tin debug
       print('DEBUG INPUT FROM CLIENT:')
       print(event)
       
       headers = event['headers']
       body = json.loads(event['body'])
       
       print('DEBUG HEADER FROM CLIENT:')
       print(headers)
       
       print('DEBUG BODY FROM CLIENT:')
       print(body)
       
       firstNum = body['firstNum']
       secondNum = body['secondNum']
       operator = body['operator']
       
       result = calculate(firstNum, secondNum, operator)
       
       response_body = {
           'message': 'Request processed successfully',
           'result': result
       }
       
       response = {
           'statusCode': 200,
           'body': json.dumps(response_body),
           'headers': {
               'Content-Type': 'application/json'
           }
       }
       return response

   def calculate(num1, num2, operator):
       if operator == 'ADD':
           return num1 + num2
       elif operator == 'SUBSTRACT':
           return num1 - num2
       elif operator == 'MULTIPLE':
           return num1 * num2
       elif operator == 'DEVIDE':
           return num1 / num2
       else:
           return 0
   ```
2. Lưu và nhấn **Deploy** code trên AWS Lambda Console.
3. Khi bạn gửi request qua Postman hoặc xem log trên **Amazon CloudWatch Logs**, bạn sẽ thấy các log debug in ra thông tin headers và body, đặc biệt là sự xuất hiện của custom header `'source': 'CloudFront'` được chuyển tiếp thành công từ CloudFront CDN xuống Lambda.

   ![Xem log CloudWatch có custom header Source CloudFront](../../../../../images/aws/cloudfront_apigw_cloudwatch_logs.png)
   *Hình 12: Logs sự kiện CloudWatch xác nhận header Source: CloudFront và body JSON được Lambda ghi nhận thành công.*

---

* **Bài trước**: [1. Lab 1 – Sử dụng CloudFront kết hợp với S3](../1.%20Lab%201%20-%20Integrate%20CloudFront%20with%20S3/1.%20Lab%201%20-%20Integrate%20CloudFront%20with%20S3.md)
* **Bài tiếp theo**: Sắp ra mắt (Coming soon...)
