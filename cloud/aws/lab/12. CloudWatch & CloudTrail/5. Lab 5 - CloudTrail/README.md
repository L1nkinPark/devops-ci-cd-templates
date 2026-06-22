# Lab 5 - Thực hành với CloudTrail

## I. Yêu cầu bài Lab
Tạo một **Trail** mới trong AWS CloudTrail để lưu trữ vĩnh viễn và kiểm toán lịch sử cuộc gọi API trên tài khoản AWS của bạn về một S3 Bucket bảo mật, đồng thời thực hiện tra cứu truy vết hành động xóa tài nguyên thực tế để xác định danh tính người dùng thực thi.

---

## II. Các bước thực hiện chi tiết

### Bước 1: Tạo một S3 Bucket lưu trữ logs của CloudTrail
1. Truy cập dịch vụ **S3** > Click **Create bucket**.
2. Thiết lập thông số:
   * **Bucket name**: Đặt tên duy nhất, ví dụ: `cloudtrail-audit-logs-yourname`.
   * **Region**: Chọn Region chạy tài nguyên chính của bạn.
   * Để tất cả cài đặt khác mặc định > Click **Create bucket**.

---

### Bước 2: Khởi tạo một Trail mới trong CloudTrail
1. Truy cập dịch vụ **CloudTrail** trên AWS Console.
2. Tại menu bên trái, chọn **Trails** > Click chọn nút **Create trail**.
3. Cấu hình thông tin Trail:
   * **Trail name**: Nhập `account-audit-trail`.
   * **Storage location**: Chọn **Use an existing S3 bucket** > Click **Browse** và chọn bucket `cloudtrail-audit-logs-yourname` vừa tạo ở Bước 1.
   * **Log file SSE-KMS encryption**: Tắt (**Uncheck** - để đơn giản hóa bài lab và tránh phát sinh chi phí KMS).
   * **Log file validation**: Tích chọn **Enabled** (đảm bảo tính toàn vẹn của file log, chống giả mạo logs).
   * Click **Next**.
4. Chọn loại sự kiện cần ghi nhận (Choose log events):
   * **Event type**: Tích chọn **Management events** (để ghi lại các hoạt động quản trị hạ tầng).
   * **API activity**: Tích chọn cả **Read** và **Write**.
   * Click **Next** > Xem lại cấu hình > Click **Create trail**.
   Trạng thái của Trail sẽ hiển thị là **`Logging`** (Đang ghi nhận).

---

### Bước 3: Thực hiện một thay đổi hạ tầng thực tế để tạo sự kiện
Chúng ta sẽ giả lập một hành động thay đổi cấu hình hạ tầng để kiểm toán:
1. Vào dịch vụ **EC2** > Chọn **Security Groups** ở menu bên trái.
2. Click **Create security group**:
   * **Security group name**: Nhập `temp-test-group`.
   * **Description**: Nhập `Testing CloudTrail audit`.
   * Click **Create security group**.
3. Nhấp chọn Security Group `temp-test-group` vừa tạo > Chọn **Actions** > Click **Delete security group** để xóa bỏ nó.

---

### Bước 4: Truy vết hành động xóa tài nguyên trên CloudTrail Console
Lưu ý: Mặc dù CloudTrail ghi lại API rất nhanh, các sự kiện có thể mất từ **5 đến 15 phút** để xuất hiện đầy đủ trên giao diện Console Event History.
1. Quay lại dịch vụ **CloudTrail** > Chọn **Event history** trong menu bên trái.
2. Tại bộ lọc tìm kiếm (Lookup attributes):
   * Chọn **Event name** và nhập tên API xóa Security Group: **`DeleteSecurityGroup`**.
   * Hoặc chọn **User name** và điền tên người dùng IAM của bạn.
3. Bạn sẽ thấy một dòng sự kiện hiển thị trong danh sách. Nhấp chọn dòng sự kiện đó để xem chi tiết thông tin truy vết:
   * **Event time**: Thời gian chính xác diễn ra hành động xóa.
   * **User name**: Tài khoản/IAM User thực hiện hành động.
   * **Source IP address**: Địa chỉ IP mạng thực tế của người thực hiện.
4. Click chọn **View event** để xem tệp JSON đầy đủ. File JSON này chứa thông tin cấu hình chi tiết về tham số yêu cầu và kết quả trả về của API.

---

### Bước 5: Kiểm tra logs thô trong S3 Bucket
1. Quay lại dịch vụ **S3** > Mở bucket `cloudtrail-audit-logs-yourname`.
2. Bạn sẽ thấy một cấu trúc cây thư mục được tự động sinh ra dạng:
   `AWSLogs/ <account-id>/ CloudTrail/ <region>/ <year>/ <month>/ <day>/`
3. Điều hướng vào thư mục ngày hiện tại. Bạn sẽ thấy các tệp tin log thô định dạng nén JSON (`.json.gz`).
4. Bạn có thể tải tệp tin này về máy tính, giải nén và mở bằng text editor để đọc toàn bộ nhật ký kiểm toán.
