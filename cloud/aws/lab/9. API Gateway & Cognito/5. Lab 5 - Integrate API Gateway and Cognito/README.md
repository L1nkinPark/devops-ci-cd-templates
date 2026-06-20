# 5. Kết hợp API Gateway & Cognito - Hướng dẫn chi tiết

 **[Xem Đề bài / Yêu cầu bài Lab](5.%20Lab%205%20-%20Integrate%20API%20Gateway%20and%20Cognito.md)**

---

## Các bước thực hiện chi tiết

### Bước 1: Khởi tạo Cognito Authorizer trên API Gateway

Trước tiên, bạn cần cấu hình để API Gateway biết cách kết nối với Cognito User Pool để xác thực token gửi lên từ client.

1. Truy cập vào AWS Management Console, mở dịch vụ **API Gateway**.
2. Chọn API **`test-api`** của bạn từ danh sách.
3. Ở menu bên trái dưới mục **API: test-api**, click chọn **Authorizers**.
4. Hiện tại danh sách Authorizers đang trống. Click chọn **Create authorizer** (hoặc **Create an authorizer** ở giữa màn hình).

![Giao diện danh sách Authorizers trống](../../../../../images/aws/apigw_cognito_authorizers_list.png)

5. Cấu hình chi tiết Authorizer mới:
   * **Authorizer name**: Nhập `cognito-auth`.
   * **Authorizer type**: Tích chọn **Cognito**.
   * **Cognito user pool**:
     * Chọn Region tương ứng (ví dụ: `us-east-1`).
     * Nhấp chọn ô tìm kiếm và chọn User Pool **`test-user-pool-01`** đã tạo trước đó.
   * **Token source**: Nhập `method.request.header.authorization`.
     * *Lưu ý: Cấu hình này chỉ định API Gateway sẽ tìm kiếm JWT token từ Header mang tên `authorization` (hoặc `Authorization`) trong request của Client gửi lên.*
   * **Token validation**: Để trống (không bắt buộc).
6. Click chọn nút **Create authorizer** ở góc dưới bên phải để lưu.

![Khởi tạo Cognito Authorizer trên API Gateway](../../../../../images/aws/apigw_cognito_authorizer_create.png)

---

### Bước 2: Liên kết Authorizer vào Resource Method

Sau khi đã tạo Authorizer, bạn cần áp dụng nó vào phương thức API cụ thể để bảo vệ endpoint đó.

1. Ở menu bên trái, chọn **Resources**.
2. Tìm đến resource `/calculate` và click chọn phương thức **POST**.
3. Tại giao diện **Method request** (phần cấu hình yêu cầu từ Client), bạn sẽ thấy phần **Authorization** mặc định là `NONE`.

![Trạng thái Authorization mặc định là NONE](../../../../../images/aws/apigw_cognito_method_before.png)

4. Click vào nút **Edit** ở góc phải của khu vực *Method request settings*.
5. Tại mục **Authorization**, nhấp chọn menu thả xuống và chọn **`cognito-auth`** vừa tạo ở Bước 1.
6. Mục **API key required**: Đảm bảo vẫn giữ là `True` nếu bạn muốn giữ lớp bảo vệ API Key song song với Cognito.
7. Click chọn **Save** để cập nhật thay đổi.

![Cập nhật Authorization thành công sang cognito-auth](../../../../../images/aws/apigw_cognito_method_edit.png)

---

### Bước 3: Deploy API Gateway để áp dụng cấu hình mới

Mọi cấu hình trên API Gateway chỉ thực sự có hiệu lực sau khi bạn tiến hành deploy API lên một stage cụ thể.

1. Nhấp chọn nút **Deploy API** ở góc trên bên phải giao diện quản lý Resources.
2. Trong hộp thoại **Deploy API**:
   * **Stage**: Chọn stage **`dev`** đang sử dụng.
   * **Deployment description**: Nhập mô tả phiên bản cập nhật (ví dụ: `v0.4` hoặc `Integrate Cognito authorizer`).
3. Click chọn nút **Deploy**.

![Hộp thoại Deploy API lên stage dev](../../../../../images/aws/apigw_cognito_deploy_dialog.png)

---

### Bước 4: Kiểm thử và xác minh tích hợp bằng Postman

Bây giờ API của bạn đã được bảo vệ kép bởi **API Key** và **Cognito Authorizer (JWT Token)**. Chúng ta sẽ dùng Postman để kiểm chứng:

#### 1. Kiểm thử khi không truyền Token (hoặc Token không hợp lệ)
1. Mở Postman, cấu hình request POST gửi tới API Gateway Invoke URL (ví dụ: `https://da0brxb62b.execute-api.us-east-1.amazonaws.com/dev/calculate`).
2. Đính kèm API Key vào Header `x-api-key`.
3. Nhấn **Send** khi **không** đính kèm Header `authorization`.
4. **Kết quả**: API Gateway lập tức từ chối request và trả về mã lỗi **`401 Unauthorized`** kèm body:
   ```json
   {
       "message": "Unauthorized"
   }
   ```
   *(Lambda backend hoàn toàn không bị kích hoạt trong trường hợp này, giúp bạn tiết kiệm chi phí tính toán).*

#### 2. Kiểm thử khi truyền ID Token hợp lệ
1. Mở file [id_token.txt](../4.%20Lab%204%20-%20Cognito%20Hosted%20UI%20Login%20and%20Token/id_token.txt) được tạo từ Lab 4 và sao chép toàn bộ chuỗi token dài bên trong.
2. Quay lại Postman, trong phần **Headers** của request, thêm một header mới:
   * **Key**: `authorization`
   * **Value**: Dán toàn bộ chuỗi ID Token vừa copy ở trên.
3. Gửi kèm Request Body (ví dụ: phép tính cộng):
   ```json
   {
       "a": 15,
       "b": 25,
       "op": "+"
   }
   ```
4. Nhấn **Send**.
5. **Kết quả**: API Gateway xác thực thành công ID Token từ Cognito, chuyển tiếp request xuống Lambda backend xử lý. Bạn sẽ nhận được mã phản hồi **`200 OK`** cùng kết quả trả về chính xác:
   ```json
   {
       "result": 40"
   }
   ```

> [!NOTE]
> Trong AWS API Gateway, khi cấu hình `Token source` là `method.request.header.authorization`, mặc định hệ thống sẽ kiểm tra chuỗi token thô (Raw JWT). Do đó trong Postman bạn chỉ cần truyền trực tiếp chuỗi token vào ô Value của header `authorization` (không cần tiền tố `Bearer ` trừ khi bạn cấu hình kiểm tra Regex cho trường Token validation).

---

* **Bài trước**: [4. Lab 4 – Sử dụng Cognito Hosted UI để login và lấy token](../4.%20Lab%204%20-%20Cognito%20Hosted%20UI%20Login%20and%20Token/4.%20Lab%204%20-%20Cognito%20Hosted%20UI%20Login%20and%20Token.md)
* **Bài tiếp theo**: Sắp ra mắt (Coming soon...)

---

 **[Quay lại Đề bài](5.%20Lab%205%20-%20Integrate%20API%20Gateway%20and%20Cognito.md)**
