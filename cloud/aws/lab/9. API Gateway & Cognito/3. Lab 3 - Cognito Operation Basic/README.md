# 3. Cognito Operation Basic - Hướng dẫn chi tiết

 **[Xem Đề bài / Yêu cầu bài Lab](3.%20Lab%203%20-%20Cognito%20Operation%20Basic.md)**

---

## Các bước thực hiện chi tiết

### Bước 1: Khởi tạo Cognito User Pool

Amazon Cognito User Pool là một thư mục người dùng hỗ trợ các chức năng đăng ký, đăng nhập và xác thực cho ứng dụng của bạn.

1. Đăng nhập vào AWS Management Console, tìm kiếm và truy cập dịch vụ **Cognito**.
2. Tại màn hình dashboard của Amazon Cognito, click chọn nút **Create user pool**.

![Màn hình danh sách User pools của Cognito](../../../../../images/aws/cognito_user_pools_list.png)

3. Tiến hành cấu hình thông tin cho ứng dụng tại trang **Set up resources for your application**:
   * **Define your application:**
     * **Application type**: Chọn **Traditional web application**.
     * **Name your application**: Nhập `test-user-pool-01`.
   * **Configure options:**
     * **Options for sign-in identifiers**: Tích chọn cả **Email** và **Username**.
     * **Self-registration**: Tích chọn **Enable self-registration** (Cho phép người dùng tự đăng ký).
     * **Required attributes for sign-up**: Chọn **email** và **name** từ danh sách các thuộc tính bắt buộc.
   * **Add a return URL - optional:**
     * **Return URL**: Nhập `https://h1eudayne.dev` (Đây là URL mà Cognito sẽ chuyển hướng người dùng quay trở lại sau khi họ đăng nhập thành công).
4. Click chọn nút **Create user directory** ở góc dưới cùng bên phải để hoàn tất việc tạo User Pool.

![Cấu hình thuộc tính đăng nhập, đăng ký và App Client](../../../../../images/aws/cognito_set_up_resources.png)

---

### Bước 2: Tạo User bằng quyền quản trị (Admin)

Để tạo sẵn các tài khoản nội bộ mà không cần thông qua form đăng ký công khai, quản trị viên có thể khởi tạo trực tiếp người dùng từ bảng điều khiển Cognito:

1. Click chọn User Pool **`test-user-pool-01`** vừa tạo.
2. Tại menu danh mục bên trái, chọn **Users** dưới phần *User management*.
3. Click chọn nút **Create user**.

![Giao diện quản lý người dùng](../../../../../images/aws/cognito_users_list.png)

4. Cấu hình chi tiết thông tin người dùng mới:
   * **Invitation message**: Chọn **Don't send an invitation** (Không gửi thư mời qua email).
   * **User name**: Nhập `h1eudayne`.
   * **Email address**: Nhập `voduchieu42@gmail.com`.
   * Tích chọn **Mark email address as verified** (Đánh dấu email đã được xác minh để bỏ qua bước xác thực mã OTP khi đăng nhập).
   * **Temporary password**: Chọn **Set a password** và nhập mật khẩu tạm thời cho người dùng.
5. Click chọn **Create user** để lưu.

![Biểu mẫu tạo người dùng mới](../../../../../images/aws/cognito_create_user.png)

---

### Bước 3: Tạo Group và Thêm User vào Group

Group (Nhóm) trong Cognito giúp gom cụm người dùng để phân quyền truy cập thông qua IAM Role hoặc token claims.

1. Quay lại trang quản trị User Pool **`test-user-pool-01`** trên AWS Console.
2. Chọn mục **Groups** ở thanh danh mục bên trái (trong mục *User management*).
3. Click chọn nút **Create group**.

![Giao diện quản lý Groups trống](../../../../../images/aws/cognito_groups_list.png)

4. Cấu hình chi tiết cho Group mới:
   * **Group name**: Nhập `normal_group`.
   * **Description**: Nhập `normal user`.
   * **Precedence**: Nhập `1` (Mức độ ưu tiên để Cognito xác định group chính khi người dùng thuộc nhiều group).
   * **IAM role**: Để trống hoặc chọn mặc định (ở đây ta chưa cần gán IAM role).
5. Click chọn nút **Create group** ở góc dưới cùng bên phải.

![Biểu mẫu tạo group mới](../../../../../images/aws/cognito_create_group.png)

6. Sau khi tạo thành công, click vào group **`normal_group`** vừa tạo.
7. Click chọn nút **Add user to group** (Thêm người dùng vào nhóm).

![Trang chi tiết Group normal_group](../../../../../images/aws/cognito_group_details.png)

8. Trong bảng danh sách người dùng hiển thị:
   * Tích chọn người dùng **`h1eudayne`** (trạng thái `Confirmed`).
   * Click chọn nút **Add** ở góc dưới cùng bên phải.

![Chọn user và add vào group](../../../../../images/aws/cognito_add_user_to_group.png)

> [!NOTE]
> **Một số lưu ý quan trọng về Cognito Group:**
> - **Không hỗ trợ nhóm lồng nhau (No nested groups):** Amazon Cognito không hỗ trợ cấu trúc nhóm con bên trong nhóm cha. Tất cả các nhóm đều nằm ở mức độ ngang hàng nhau trong cùng một User Pool.
> - AWS cho phép tích hợp Group với **Amazon Verified Permissions** để thực hiện phân quyền chi tiết (fine-grained authorization) cho các API trên API Gateway.

---

* **Bài trước**: [2. Lab 2 – API Key và Usage Plan trong API Gateway](../2.%20Lab%202%20-%20API%20Key%20and%20Usage%20Plan/2.%20Lab%202%20-%20API%20Key%20and%20Usage%20Plan.md)
* **Bài tiếp theo**: [4. Lab 4 – Sử dụng Cognito Hosted UI để login và lấy token](../4.%20Lab%204%20-%20Cognito%20Hosted%20UI%20Login%20and%20Token/4.%20Lab%204%20-%20Cognito%20Hosted%20UI%20Login%20and%20Token.md)

---

 **[Quay lại Đề bài](3.%20Lab%203%20-%20Cognito%20Operation%20Basic.md)**
