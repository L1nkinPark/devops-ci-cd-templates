# Lab 2 - Cài đặt CloudWatch Agent để thu thập Logs & Custom Metrics

## I. Yêu cầu bài Lab
Mặc định, AWS không thể tự thu thập dung lượng Memory (RAM) sử dụng và dung lượng Disk còn trống của máy chủ EC2 do ranh giới bảo mật của hệ điều hành. Chúng ta cần cài đặt **CloudWatch Agent** bên trong máy chủ để thu thập các chỉ số này kèm theo tệp tin nhật ký truy cập (Access Log) của Apache Web Server.

---

## II. Các bước thực hiện chi tiết

### Bước 1: Tạo và gắn IAM Role cho phép ghi logs/metrics
1. Truy cập dịch vụ **IAM** > Chọn **Roles** > Click **Create role**.
2. Chọn Trusted entity type là **AWS service** và Common use case là **EC2** > Click **Next**.
3. Tại trang phân quyền, tìm kiếm và tích chọn chính sách:
   * **`CloudWatchAgentServerPolicy`**
   * Click **Next**.
4. Đặt tên Role:
   * **Role name**: Nhập `EC2-CloudWatch-Agent-Role`.
   * Click **Create role**.
5. Gán Role vào EC2:
   * Vào **EC2 Console** > Nhấp chọn instance của bạn > **Actions** > **Security** > **Modify IAM role**.
   * Chọn `EC2-CloudWatch-Agent-Role` vừa tạo > Click **Update IAM role**.

---

### Bước 2: Tải và cài đặt CloudWatch Agent trên EC2
1. SSH vào terminal của EC2.
2. Chạy lệnh tải gói cài đặt RPM của CloudWatch Agent (dành cho Amazon Linux 2 / 2023):
   ```bash
   sudo yum install amazon-cloudwatch-agent -y
   ```

---

### Bước 3: Tạo tệp cấu hình thu thập Log & Metrics
Chúng ta sẽ tạo file cấu hình thủ công tại đường dẫn mặc định của agent `/opt/aws/amazon-cloudwatch-agent/etc/amazon-cloudwatch-agent.json`:
1. Mở trình biên dịch bằng quyền root:
   ```bash
   sudo vi /opt/aws/amazon-cloudwatch-agent/etc/amazon-cloudwatch-agent.json
   ```
2. Dán nội dung cấu hình JSON mẫu dưới đây vào file:
   ```json
   {
     "agent": {
       "metrics_collection_interval": 60,
       "run_as_user": "cwagent"
     },
     "metrics": {
       "metrics_collected": {
         "disk": {
           "measurement": [
             "disk_used_percent"
           ],
           "metrics_collection_interval": 60,
           "resources": [
             "/"
           ]
         },
         "mem": {
           "measurement": [
             "mem_used_percent"
           ],
           "metrics_collection_interval": 60
         }
       }
     },
     "logs": {
       "logs_collected": {
         "files": {
           "collect_list": [
             {
               "file_path": "/var/log/httpd/access_log",
               "log_group_name": "/var/log/httpd/access_log",
               "log_stream_name": "{instance_id}",
               "retention_in_days": 7
             }
           ]
         }
       }
     }
   }
   ```
   *(Cấu hình trên yêu cầu thu thập % Disk sử dụng của thư mục gốc `/`, % RAM sử dụng và file log truy cập của Apache tại `/var/log/httpd/access_log` rồi đẩy về Log Group cùng tên, lưu trữ tự động trong 7 ngày).*
3. Nhấn `Esc`, gõ `:wq` và `Enter` để lưu tệp tin.

---

### Bước 4: Khởi chạy CloudWatch Agent Service
1. Khởi chạy agent và áp dụng file cấu hình vừa tạo bằng công cụ control utility:
   ```bash
   sudo /opt/aws/amazon-cloudwatch-agent/bin/amazon-cloudwatch-agent-ctl -a fetch-config -m ec2 -s -c file:/opt/aws/amazon-cloudwatch-agent/etc/amazon-cloudwatch-agent.json
   ```
2. Kiểm tra trạng thái hoạt động của agent để đảm bảo dịch vụ đang chạy bình thường:
   ```bash
   sudo systemctl status amazon-cloudwatch-agent
   ```

---

### Bước 5: Xác thực kết quả trên CloudWatch Console
1. **Kiểm tra Logs**:
   * Truy cập **CloudWatch Console** > Chọn **Logs groups** trong menu bên trái.
   * Bạn sẽ thấy một Log Group mới tên là `/var/log/httpd/access_log` đã được tự động tạo. Nhấp chọn stream (tương ứng với Instance ID của bạn) để xem các dòng access log của Apache đã được đồng bộ trực tiếp lên đám mây.
2. **Kiểm tra Custom Metrics**:
   * Chọn **Metrics** > **All metrics** trên CloudWatch Console.
   * Tại tab *Browse*, bạn sẽ thấy xuất hiện một Namespace mới tên là **`CWAgent`**. Nhấp chọn Namespace này để xem biểu đồ đo lường thời gian thực của RAM (`mem_used_percent`) và dung lượng đĩa cứng (`disk_used_percent`).
