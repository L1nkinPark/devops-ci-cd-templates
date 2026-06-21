# 1. API Gateway sử dụng Lambda làm backend (Calculator API) - Hướng dẫn chi tiết

 **[Xem Đề bài / Yêu cầu bài Lab](1.%20Lab%201%20-%20API%20Gateway%20with%20Lambda%20Backend.md)**

---

## Các bước thực hiện chi tiết

### Bước 1: Tạo Lambda Function

1. Truy cập **AWS Lambda Console** $\rightarrow$ **Functions** $\rightarrow$ Chọn **Create function**.
2. Cấu hình các thông số cơ bản:
   * Chọn **Author from scratch** (Tự viết từ đầu).
   * **Function name**: `test-calculator-function`.
   * **Runtime**: Chọn **Python 3.12** (hoặc phiên bản Python mới nhất).
   * **Architecture**: Chọn **x86_64**.
3. Nhấp chọn **Create function** ở góc dưới bên phải.

<p align="center">
  <img src="../../../../images/aws/apigw_lambda_create_function.png" alt="Khởi tạo Lambda Function" width="750"/>
</p>

---

### Bước 2: Đưa code đã chuẩn bị vào Lambda

1. Tại giao diện Lambda Function vừa tạo, di chuyển đến tab **Code**.
2. Mở file `calculator-lambda.py` (hoặc `lambda_function.py` tùy theo thiết lập của bạn) trong trình soạn thảo trực tuyến.
3. Thay thế mã nguồn mặc định bằng đoạn mã Calculator hỗ trợ cả gọi trực tiếp hoặc gọi qua API Gateway Proxy dưới đây:

```python
import json

def lambda_handler(event, context):
    # for debug
    print("DEBUG INPUT FROM CLIENT:")
    print(event)
    
    # Hỗ trợ cả hai trường hợp: Test trực tiếp trên Lambda (Direct Event) hoặc gọi qua API Gateway Proxy (bật Lambda Proxy Integration)
    if isinstance(event, dict) and 'body' in event:
        # Nếu event nhận từ API Gateway Proxy, event['body'] là chuỗi JSON string
        body = json.loads(event['body']) if isinstance(event['body'], str) else event['body']
    else:
        body = event
        
    firstNum = body['firstNum']
    secondNum = body['secondNum']
    operator = body['operator'] # ADD, MULTIPLE, DEVIDE, SUBSTRACT
    # Process the request
    result = calculate(firstNum, secondNum, operator)
    
    # Create the response body
    response_body = {
        'message': 'Request processed successfully',
        'result': result
    }
    
    # Create the HTTP response (Bắt buộc trả về đúng định dạng này khi dùng Proxy Integration)
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

4. Nhấn nút **Deploy** phía trên code editor để lưu và áp dụng mã nguồn mới lên AWS.

<p align="center">
  <img src="../../../../images/aws/apigw_lambda_code_editor.png" alt="Cập nhật code Lambda và Deploy" width="750"/>
</p>

---

### Bước 3: Tạo REST API trên API Gateway

1. Truy cập **Amazon API Gateway Console**.
2. Cuộn xuống và tìm mục **REST API** (không chọn *REST API Private*), nhấn **Build**.

<p align="center">
  <img src="../../../../images/aws/apigw_create_rest_api.png" alt="Chọn REST API Build" width="750"/>
</p>

3. Điền các thông số khởi tạo:
   * **Choose the protocol**: Chọn **REST**.
   * **Create new API**: Chọn **New API**.
   * **API name**: Nhập `test-api` (hoặc tên tùy chọn của bạn).
   * **Description**: Nhập mô tả (ví dụ: `test-api`).
   * **API endpoint type**: Chọn **Regional** (hoặc Edge-optimized).
4. Nhấn nút **Create API** ở góc dưới cùng bên phải.

<p align="center">
  <img src="../../../../images/aws/apigw_api_details.png" alt="Cấu hình API details" width="750"/>
</p>

---

### Bước 4: Tạo Resource `/calculate` và Method `POST`

Ta cần tạo một Endpoint dạng `POST /calculate` nhận các thông số từ client.

1. Tại giao diện quản lý API `test-api`, chọn **Resources** ở menu bên trái.
2. Click **Create resource** ở phía trên:
   * **Resource name**: Nhập `calculate`.
   * **Resource path**: Sẽ tự động điền `/calculate`.
   * Nhấp chọn **Create resource**.

<p align="center">
  <img src="../../../../images/aws/apigw_create_resource.png" alt="Tạo resource thành công" width="750"/>
</p>

3. Click chọn resource `/calculate` vừa tạo trong cây thư mục $\rightarrow$ Click chọn **Create method**:
   * **Method type**: Chọn **POST**.
   * **Integration type**: Chọn **Lambda function**.
    * **Lambda proxy integration**: **BẬT** tùy chọn này (đảm bảo gạt nút sang phải/màu xanh dương như hình dưới).
    * **Lambda function**: Nhập ARN hoặc tên hàm Lambda đã tạo ở Bước 1: `test-calculator-function` (đảm bảo chọn đúng Region, ví dụ: `us-east-1`).
   * Nhấn **Create method** ở góc dưới cùng bên phải.

<p align="center">
  <img src="../../../../images/aws/apigw_integration_request_settings.png" alt="Xem chi tiết Integration Request" width="750"/>
</p>

<p align="center">
  <img src="../../../../images/aws/apigw_lambda_proxy_toggle.png" alt="Bật Lambda proxy integration" width="700"/>
</p>

4. Sau khi click tạo, API Gateway sẽ tự động gán quyền gọi (invoke permission) cho Lambda function. Giao diện sau khi tạo thành công sẽ như hình bên dưới:

<p align="center">
  <img src="../../../../images/aws/apigw_method_execution.png" alt="Giao diện Method Execution chi tiết" width="750"/>
</p>

---

### Bước 5: Tạo Stages và Triển khai (Deploy) API

Sau khi cấu hình xong tài nguyên, ta cần tạo Stage triển khai và deploy API:

#### 1. Tạo Stage mới (`dev`)
1. Click chọn **Stages** ở danh mục menu bên trái.
2. Click chọn nút **Create stage** ở góc phải:
   * **Stage name**: Nhập `dev`.
   * **Stage description**: Nhập mô tả (ví dụ: `dev stage`).
   * **Deployment**: Giữ nguyên mặc định (hoặc chọn *New deployment*).
3. Click nút **Create stage**.

<p align="center">
  <img src="../../../../images/aws/apigw_stages_list.png" alt="Chọn tạo Stage mới" width="750"/>
</p>

<p align="center">
  <img src="../../../../images/aws/apigw_create_stage.png" alt="Điền thông số Stage dev" width="750"/>
</p>

#### 2. Triển khai Resource lên Stage vừa tạo
1. Chọn lại **Resources** ở menu bên trái.
2. Click chọn resource `/` hoặc `/calculate`.
3. Nhấp chọn nút **Deploy API** ở góc trên cùng bên phải:
   * **Stage**: Chọn Stage vừa tạo ở trên (`dev`).
   * **Deployment description**: Nhập mô tả phiên bản (ví dụ: `v0.1`).
4. Nhấn nút **Deploy**.

<p align="center">
  <img src="../../../../images/aws/apigw_deploy_api_dialog.png" alt="Deploy API lên Stage dev" width="550"/>
</p>

5. Sau khi Deploy thành công, hệ thống sẽ chuyển bạn đến màn hình quản trị Stage. Tại đây, hãy sao chép **Invoke URL** của API. 

<p align="center">
  <img src="../../../../images/aws/apigw_stage_invoke_url.png" alt="Sao chép Invoke URL từ Stage dev" width="750"/>
</p>

Endpoint URL POST đầy đủ để gọi tới Lambda của bạn (thêm `/calculate`) sẽ là:
`https://{api-id}.execute-api.{region}.amazonaws.com/dev/calculate`

---

### Bước 6: Kiểm thử API bằng Client (Postman / cURL)

Sử dụng bất kỳ công cụ test API nào để thực hiện gửi HTTP POST request:

#### 1. Kiểm thử bằng lệnh cURL (Terminal / Git Bash)
Thay thế `{api-id}` và `{region}` bằng thông tin Endpoint của bạn và chạy lệnh sau:

```bash
curl -X POST https://{api-id}.execute-api.{region}.amazonaws.com/dev/calculate \
  -H "Content-Type: application/json" \
  -d '{"firstNum": 15, "secondNum": 5, "operator": "ADD"}'
```

#### 2. Kiểm thử bằng Postman và File Collection có sẵn

Để thuận tiện cho việc kiểm thử, một tệp tin Postman Collection đã được chuẩn bị sẵn trong thư mục lab này: [calculator.postman_collection.json](calculator.postman_collection.json).

1. Mở Postman $\rightarrow$ Chọn **Import** và chọn file [calculator.postman_collection.json](calculator.postman_collection.json) để tải collection tên là `cloud-basic` vào workspace của bạn.
2. Thư mục `cloud-basic` chứa 4 request tương ứng với 4 phép toán (`ADD`, `SUBSTRACT`, `MULTIPLE`, `DEVIDE`).

<p align="center">
  <img src="../../../../images/aws/apigw_postman_collection.png" alt="Import thành công Postman Collection" width="300"/>
</p>

3. Chọn request **Calculator API Gateway-ADD** $\rightarrow$ Thay thế đường dẫn URL bằng **Invoke URL** đầy đủ bạn lấy được ở Bước 5 (ví dụ: `https://da0brxb62b.execute-api.us-east-1.amazonaws.com/dev/calculate`).
4. Nhấn **Send** để gửi request.

<p align="center">
  <img src="../../../../images/aws/apigw_postman_test_response.png" alt="Gọi thành công API trên Postman" width="750"/>
</p>

#### Kết quả phản hồi (Response)

Nếu cấu hình đúng, bạn sẽ nhận được kết quả HTTP `200 OK` kèm theo dữ liệu phản hồi từ Lambda backend:

```json
{
  "statusCode": 200,
  "body": "{\"message\": \"Request processed successfully\", \"result\": 30}",
  "headers": {
      "Content-Type": "application/json"
  }
}
```



> [!TIP]
> Hãy thử thay đổi toán tử `operator` thành `SUBSTRACT` (Trừ), `MULTIPLE` (Nhân), hoặc `DEVIDE` (Chia) để kiểm nghiệm kết quả xử lý của Lambda backend!

---

### Bước 7: Kiểm tra CloudWatch Logs để debug

Để kiểm tra quá trình nhận request và debug:

1. Truy cập dịch vụ **CloudWatch Console** $\rightarrow$ Chọn mục **Log groups** từ menu bên trái.
2. Tìm kiếm và click chọn vào nhóm log tương ứng với hàm Lambda: `/aws/lambda/test-calculator-function`.
3. Nhấp chọn vào **Log stream** mới nhất được sinh ra từ request bạn vừa gửi.
4. Bạn sẽ thấy dòng nhật ký in ra định dạng `event` mà Lambda nhận được:

```text
DEBUG INPUT FROM CLIENT:
{'firstNum': 15, 'secondNum': 5, 'operator': 'ADD'}
```

---

* **Bài trước**: [4. Lab 4 - VPC Peering (Thực hành kết nối 2 VPC)](../../8.%20VPC/4.%20Lab%204%20-%20VPC%20Peering.md)
* **Bài tiếp theo**: Sắp ra mắt (Coming soon...)

---

 **[Quay lại Đề bài](1.%20Lab%201%20-%20API%20Gateway%20with%20Lambda%20Backend.md)**
