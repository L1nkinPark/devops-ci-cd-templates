# 4. Sử dụng Cognito Hosted UI để login và lấy token - Hướng dẫn chi tiết

 **[Xem Đề bài / Yêu cầu bài Lab](4.%20Lab%204%20-%20Cognito%20Hosted%20UI%20Login%20and%20Token.md)**

---

## Các bước thực hiện chi tiết

### Bước 1: Thử nghiệm Đăng nhập bằng Hosted UI của Cognito

AWS Cognito cung cấp sẵn một trang web giao diện đăng nhập (Hosted UI) giúp bạn dễ dàng tích hợp và thử nghiệm mà không cần tự code frontend:

1. Đăng nhập vào AWS Management Console, tìm kiếm và truy cập dịch vụ **Cognito**.
2. Click chọn User Pool **`test-user-pool-01`** đã tạo từ Lab 3.
3. Tại menu danh mục bên trái, chọn **App clients** dưới phần *Applications*.
4. Click chọn App client tương ứng của bạn.
5. Chuyển sang tab **Login pages** trong phần thông tin App client.
6. Tại khu vực *Managed login pages configuration*, click chọn nút **View login page** để mở trang đăng nhập được Cognito hosted tự động.

![Vị trí nút View login page trong cấu hình App client](../../../../../images/aws/cognito_app_client_login.png)

7. Tại trang web đăng nhập vừa mở ra:
   * Nhập **Username** (`h1eudayne`) và **Mật khẩu tạm thời** bạn đã đặt từ Lab trước.
   * Nhấp chọn **Sign In**.
   * Hệ thống sẽ yêu cầu bạn đổi mật khẩu mới trong lần đầu tiên đăng nhập. Nhập mật khẩu mới và xác nhận.
   * Sau khi đổi mật khẩu thành công, trình duyệt sẽ tự động chuyển hướng (redirect) về địa chỉ URL bạn đã cấu hình (`https://h1eudayne.dev`) kèm theo chuỗi query parameter chứa mã xác thực/token trên thanh URL (ví dụ: `?code=xxxx-xxxx-xxxx-xxxx`).

---

### Bước 2: Đăng ký tài khoản thông thường (Self Sign-up)

Bên cạnh việc admin tạo user thủ công, Cognito cũng hỗ trợ giao diện đăng ký tự động (Self Sign-up) cho người dùng bên ngoài:

1. Từ trang đăng nhập Hosted UI của Cognito (được mở ở Bước 1), click chọn liên kết **Sign up** ở dưới cùng.
2. Nhập các thông tin đăng ký cho tài khoản mới:
   * **Username**: `h1eudayne2`
   * **Email address**: `voduchieu43@gmail.com`
   * **Name**: `Vo Duc Hieu`
   * **Password / Confirm password**: Thiết lập mật khẩu thỏa mãn các quy tắc bảo mật của Cognito (được tích xanh toàn bộ).
3. Click chọn **Sign up** để đăng ký.

![Giao diện Sign Up của Cognito Hosted UI](../../../../../images/aws/cognito_signup_ui.png)

*Lưu ý:* Sau khi nhấn Sign up, tài khoản tự đăng ký này sẽ mặc định ở trạng thái `UNCONFIRMED` (chưa được xác thực) cho tới khi nhập mã OTP xác thực được gửi đến email đăng ký.

---

* **Bài trước**: [3. Lab 3 – Cognito Operation Basic](../3.%20Lab%203%20-%20Cognito%20Operation%20Basic/3.%20Lab%203%20-%20Cognito%20Operation%20Basic.md)
* **Bài tiếp theo**: [5. Lab 5 – Kết hợp API Gateway & Cognito](../5.%20Lab%205%20-%20Integrate%20API%20Gateway%20and%20Cognito/5.%20Lab%205%20-%20Integrate%20API%20Gateway%20and%20Cognito.md)

---

 **[Quay lại Đề bài](4.%20Lab%204%20-%20Cognito%20Hosted%20UI%20Login%20and%20Token.md)**
