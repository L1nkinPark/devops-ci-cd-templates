# Lab 5 - Thực hành với CloudTrail

## I. Yêu cầu bài Lab
Tạo một **Trail** mới trong AWS CloudTrail để lưu trữ log cuộc gọi API ra S3 bucket và CloudWatch Logs.

---

## II. Các bước thực hiện chi tiết

### Bước 1: Khởi tạo một Trail mới xuất log ra S3 và CloudWatch
1. Truy cập dịch vụ **CloudTrail** trên AWS Console.
2. Tại menu bên trái, chọn **Trails** > Click chọn nút **Create trail**.
3. Tại bước **Choose trail attributes**:
   * **Trail name**: Nhập `test-trail`.
   * **Storage location**: Chọn **Create new S3 bucket**.
   * **Trail log bucket and folder**: Nhập tên bucket (ví dụ: `cloudtrail-log-hieu` - lưu ý tên bucket phải là duy nhất).
   * **Log file SSE-KMS encryption**: Bỏ chọn (**Disabled**) (Lưu ý: Thực tế nên bật Encrypt, nhưng làm lab nên tắt để tránh phát sinh cấu hình/chi phí).
   * **CloudWatch Logs**: Tích chọn **Enabled**.
     * **Log group**: Chọn **New**.
     * **Log group name**: Nhập `test-cloudtrail`.
     * **IAM Role**: Chọn **New**.
     * **Role name**: Nhập `test-cloudtrail-role`.
   * Click **Next**.
4. Tại bước **Choose log events**:
   * **Event type**: Tích chọn **Management events**.
   * **API activity**: Tích chọn **Write**.
   * Click **Next** > Xem lại cấu hình > Click **Create trail**.

---

### Bước 2: Kiểm tra Log group được tạo bên CloudWatch
1. Truy cập dịch vụ **CloudWatch**.
2. Ở menu bên trái, phần **Logs** > chọn **Log groups**.
3. Tìm và kiểm tra xem Log group **`test-cloudtrail`** đã được hệ thống tự động tạo thành công chưa.

---

### Bước 3: Kiểm tra S3 Bucket được tạo bên S3
1. Truy cập dịch vụ **S3**.
2. Ở menu bên trái, chọn **Buckets**.
3. Tìm bucket bạn đã thiết lập ở Bước 1 (ví dụ: `cloudtrail-log-hieu`).
4. Click vào bucket, kiểm tra xem thư mục **`AWSLogs/`** đã được tự động tạo bên trong chưa. Logs của CloudTrail sẽ bắt đầu được gửi về đây.

---

### Bước 4: Tạo một sự kiện thực tế (Tạo EC2 Instance)
Để kiểm tra xem CloudTrail có đang ghi log hoạt động hay không, ta sẽ tạo một sự kiện làm thay đổi hạ tầng.
1. Truy cập dịch vụ **EC2** > Click **Launch instance**.
2. **Name**: Nhập `test-cloudtrail`.
3. Giữ nguyên các cài đặt mặc định khác (Amazon Linux, t3.micro, v.v.) và click **Launch instance**.
   *(Sự kiện `RunInstances` này sẽ được CloudTrail ghi lại)*.

---

### Bước 5: Kiểm tra Log sự kiện trên CloudWatch
1. Quay lại dịch vụ **CloudWatch** > **Logs** > **Log groups**.
2. Click vào Log group `test-cloudtrail` đã tạo ở Bước 1.
3. Trong tab **Log events**, chọn log stream tương ứng. (Lưu ý: Các sự kiện có thể mất vài phút để xuất hiện).
4. Tìm kiếm sự kiện với `eventName: "RunInstances"` hoặc `eventSource: "ec2.amazonaws.com"`.
5. Mở rộng log event này, bạn sẽ thấy thông tin chi tiết về việc tạo EC2 instance vừa thực hiện.

---

### Bước 6: Kiểm tra Log sự kiện lưu trữ trên S3
1. Truy cập dịch vụ **S3** > Mở bucket `cloudtrail-log-hieu` (hoặc tên bucket bạn đã thiết lập).
2. Điều hướng theo đường dẫn: `AWSLogs/ <account-id>/ CloudTrail/ <region>/ <year>/ <month>/ <day>/`.
3. Bạn sẽ thấy các tệp tin log được lưu trữ dưới định dạng nén `.json.gz`.
4. Chọn một tệp log có chứa khoảng thời gian bạn vừa tạo EC2 > Click **Download**.
5. Giải nén tệp `.gz` tải về, và mở tệp `.json` bên trong bằng text editor (như VSCode).
6. Tìm kiếm từ khóa `RunInstances` trong file JSON, bạn sẽ thấy thông tin chi tiết (như `accessKeyId`, `sourceIPAddress`, `userAgent`, v.v.) chứng minh thao tác đã được lưu vết đầy đủ.

---

### Bước 7: Tra cứu lịch sử bằng Instance ID trên CloudTrail
Bên cạnh việc kiểm tra log trên S3 và CloudWatch, bạn có thể dễ dàng tìm kiếm sự kiện thông qua giao diện CloudTrail:
1. Quay lại dịch vụ **CloudTrail** > Chọn **Event history** ở menu bên trái.
2. Tại thanh tìm kiếm (Lookup attributes), chọn bộ lọc **Resource name**.
3. Nhập **Instance ID** của EC2 instance bạn vừa tạo (ví dụ: `i-0abcdef1234567890`).
4. Bạn sẽ thấy ngay sự kiện `RunInstances` và các sự kiện liên quan đến instance này hiển thị chi tiết. Mở sự kiện ra để xem toàn bộ thông tin API.
