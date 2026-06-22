# Lab 1 - Thực hành với CloudWatch Alarm

## I. Yêu cầu bài Lab
Thiết lập cảnh báo tự động khi tài nguyên máy chủ EC2 bị quá tải CPU (> 70% liên tục) và gửi email thông báo qua dịch vụ **Amazon SNS**.

---

## II. Các bước thực hiện chi tiết

### Bước 1: Khởi tạo Amazon SNS Topic để nhận thông báo
1. Truy cập dịch vụ **Simple Notification Service (SNS)** trên AWS Console.
2. Tại menu bên trái, chọn **Topics** > Click **Create topic**.
3. Chọn loại **Standard**:
   * **Name**: Nhập `cpu-alert-topic`.
   * Click **Create topic**.
4. Chọn topic vừa tạo, click **Create subscription**:
   * **Protocol**: Chọn **Email**.
   * **Endpoint**: Nhập địa chỉ email cá nhân của bạn để nhận cảnh báo.
   * Click **Create subscription**.
5. **Kích hoạt Subscription**:
   * Mở hộp thư email của bạn. Bạn sẽ nhận được một email từ AWS có tiêu đề *AWS Notification - Subscription Confirmation*.
   * Click chọn liên kết **Confirm subscription** trong email để xác nhận. Trạng thái subscription trên console sẽ chuyển từ *PendingConfirmation* sang *Confirmed*.

---

### Bước 2: Thiết lập CloudWatch Alarm giám sát CPU
1. Truy cập dịch vụ **CloudWatch** > Chọn **Alarms** > Chọn **In alarm** hoặc **All alarms** > Click **Create alarm**.
2. Click **Select metric** > Chọn **EC2** > Chọn **Per-Instance Metrics**.
3. Tìm kiếm máy chủ EC2 của bạn theo Instance ID hoặc Name, tích chọn chỉ số **`CPUUtilization`** > Click **Select metric**.
4. Cấu hình các thông số đo lường (Metric & Conditions):
   * **Statistic**: Chọn **Average**.
   * **Period**: Chọn **5 minutes** (hoặc **1 minute** nếu bạn đang bật Detailed Monitoring).
   * **Threshold type**: Chọn **Static**.
   * **Whenever CPUUtilization is...**: Chọn **Greater/Threshold** và điền **`70`** (nghĩa là cảnh báo khi CPU > 70%).
   * Click **Next**.
5. Cấu hình hành động cảnh báo (Configure actions):
   * **Alarm state trigger**: Chọn **In alarm** (trạng thái báo động).
   * **Send a notification to the following SNS topic**: Chọn **Select an existing SNS topic** và chọn `cpu-alert-topic` đã tạo ở Bước 1.
   * Click **Next**.
6. Đặt tên Alarm:
   * **Alarm name**: Nhập `EC2-High-CPU-Warning`.
   * Click **Next** > Xem lại cấu hình > Click **Create alarm**.

---

### Bước 3: Giả lập stress test tải CPU trên EC2
1. Sử dụng Terminal/PowerShell để SSH vào instance EC2 của bạn.
2. Chạy lệnh sau để cài đặt công cụ stress test (đối với Amazon Linux 2 / 2023):
   ```bash
   sudo amazon-linux-extras install epel -y  # (Chỉ dành cho Amazon Linux 2)
   sudo yum install stress -y
   ```
3. Chạy stress test tải CPU lên 100% trong vòng 15 phút:
   ```bash
   stress --cpu 1 --timeout 900
   ```
   *(Hoặc sử dụng lệnh dd thô nếu không cài được stress: `dd if=/dev/urandom of=/dev/null`)*

4. Giữ nguyên terminal chạy stress và quay lại trang CloudWatch Alarm Console để theo dõi.
5. Sau vài phút, bạn sẽ thấy cột đồ thị CPU tăng vọt, trạng thái Alarm chuyển sang màu đỏ **`In alarm`** và bạn sẽ nhận được một email cảnh báo chi tiết từ AWS gửi về hộp thư.
6. Để tắt stress test, quay lại terminal và bấm tổ hợp phím `Ctrl + C`. CPU sẽ hạ nhiệt và Alarm sẽ tự động chuyển về trạng thái màu xanh **`OK`**.

---

## III. Các lưu ý quan trọng cho CloudWatch Alarm

1. **Threshold (Ngưỡng cảnh báo):** Phải được thiết lập dựa trên thực tế vận hành để tránh báo động giả. Thông thường, ngưỡng cảnh báo CPU quá tải an toàn là từ **75% - 85%**.
2. **Evaluation Periods (Chu kỳ đánh giá):** 
   * Ví dụ cấu hình: *CPU > 80% for 3 datapoints within 3 periods*. Nghĩa là CPU phải vượt 80% liên tục trong 3 chu kỳ liên tiếp (ví dụ 15 phút) thì mới kích hoạt Alarm. Điều này giúp lọc bỏ các hiện tượng CPU spike nhất thời (đột biến ngắn hạn khi restart service hoặc chạy cron job).
3. **Missing Data Treatment (Xử lý khi thiếu dữ liệu):** Bạn cần chọn cách Alarm phản xử khi không nhận được dữ liệu (ví dụ EC2 bị tắt):
   * *`notBreaching`*: Coi như bình thường (mặc định - khuyên dùng để tránh spam cảnh báo khi tắt máy chủ chủ động).
   * *`breaching`*: Coi như lỗi và kích hoạt ALARM ngay lập tức.
   * *`ignore`*: Giữ nguyên trạng thái Alarm hiện tại.
   * *`missing`*: Chuyển trạng thái Alarm sang `INSUFFICIENT_DATA`.
4. **Detailed Monitoring vs Basic Monitoring:**
   * Mặc định (Basic), metrics của EC2 được gửi lên mỗi **5 phút** (miễn phí). Nếu bạn cần độ nhạy cao, hãy bật Detailed Monitoring để gửi metrics mỗi **1 phút** (có tính phí).
