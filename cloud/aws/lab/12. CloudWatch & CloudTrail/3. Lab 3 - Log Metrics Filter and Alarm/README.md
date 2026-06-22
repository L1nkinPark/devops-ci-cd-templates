# Lab 3 - Sử dụng Log Metrics Filter & cài đặt Alarm cho Log message

## I. Yêu cầu bài Lab
Thiết lập bộ lọc từ khóa (**Metric Filter**) tự động quét qua các dòng nhật ký của Apache Web Server nhằm tìm kiếm mã trạng thái lỗi truy cập `404` (truy cập đường dẫn không tồn tại), và tự động gửi email cảnh báo khi số lượng lỗi vượt quá ngưỡng thiết lập.

---

## II. Các bước thực hiện chi tiết

### Bước 1: Tạo Metric Filter trên Log Group
1. Truy cập **CloudWatch Console** > Chọn **Log groups** > Nhấp chọn Log Group `/var/log/httpd/access_log` đã được tạo từ Lab 2.
2. Chuyển sang tab **Metric filters** > Click chọn nút **Create metric filter**.
3. Cấu hình bộ lọc (Define pattern):
   * **Filter pattern**: Nhập **`" 404 "`** (có dấu khoảng trắng 2 bên để lọc chính xác mã HTTP status 404, tránh bị trùng với các chuỗi số 404 khác trong log).
   * Click **Next**.
4. Thiết lập Metric:
   * **Filter name**: Nhập `Apache-404-Filter`.
   * **Metric namespace**: Nhập `WebServerMetrics` (Custom namespace mới).
   * **Metric name**: Nhập `Apache404Count`.
   * **Metric value**: Nhập **`1`** (tự động cộng thêm 1 đơn vị vào metric mỗi khi tìm thấy một dòng log khớp pattern).
   * **Default value**: Để trống.
   * Click **Next** > Click **Create metric filter**.

---

### Bước 2: Tạo Alarm dựa trên Custom Metric vừa filter
1. Tại tab **Metric filters** của Log Group, bạn sẽ thấy filter `Apache-404-Filter` vừa tạo. Tích chọn nó và click nút **Create alarm**.
2. Cấu hình Metric & Conditions cho Alarm:
   * **Statistic**: Chọn **Sum** (Tổng số lỗi cộng dồn).
   * **Period**: Chọn **1 minute** (hoặc **5 minutes**).
   * **Threshold type**: Chọn **Static**.
   * **Whenever Apache404Count is...**: Chọn **Greater/Threshold** và điền **`5`** (cảnh báo khi xuất hiện quá 5 lỗi 404 trong vòng 1 phút).
   * Click **Next**.
3. Cấu hình Actions gửi thông báo:
   * **Alarm state trigger**: Chọn **In alarm**.
   * **Send a notification to the following SNS topic**: Chọn **Select an existing SNS topic** và chọn `cpu-alert-topic` (SNS topic đã tạo từ Lab 1).
   * Click **Next**.
4. Đặt tên Alarm:
   * **Alarm name**: Nhập `Apache-Too-Many-404-Errors`.
   * Click **Next** > Click **Create alarm**.

---

### Bước 3: Giả lập sinh lỗi 404 và kiểm chứng
1. Mở trình duyệt web của bạn và truy cập liên tục vào các đường dẫn không tồn tại trên IP công cộng của EC2 instance của bạn (ví dụ: `http://<ec2-public-ip>/fake-page-1`, `http://<ec2-public-ip>/fake-page-2`, `http://<ec2-public-ip>/test-error`,...).
2. Truy cập lỗi liên tục hơn 6 lần trong vòng 1 phút.
3. Kiểm tra Logs để chắc chắn Apache đã ghi nhận các mã lỗi:
   * Vào **CloudWatch Log Group** `/var/log/httpd/access_log` để xem nhật ký ghi nhận các dòng dạng:
     `"GET /fake-page-1 HTTP/1.1" 404 196`
4. Chờ từ 1 đến 2 phút. Bạn sẽ thấy trạng thái Alarm chuyển sang màu đỏ **`In alarm`** trên giao diện điều khiển và nhận được một email từ AWS thông báo hệ thống đang phát sinh nhiều lỗi truy cập trang không tồn tại (lỗi 404).
5. Sau khi ngừng truy cập lỗi và hết thời gian chu kỳ đánh giá (Period), Alarm sẽ tự động chuyển đổi trạng thái về lại màu xanh **`OK`**.
