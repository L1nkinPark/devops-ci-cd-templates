# Cài Đặt và Cấu Hình Teleport (Teleport Setup)

Thư mục này chứa tài liệu và cấu hình phục vụ việc triển khai cổng quản lý truy cập máy chủ Teleport tập trung trên môi trường On-Premise.

## Danh Sách Hướng Dẫn

1. **[Bài 5: Triển khai công cụ quản lý truy cập máy chủ (Teleport)](./05-deploy-server-access-management.md)**
   * Đánh giá ưu/nhược điểm khi chạy Teleport On-Premise.
   * Tạo bản ghi DNS, thiết lập Nginx Load Balancer.
   * Cấu hình Port Forwarding bằng Cloudflare Tunnel (Zero Trust).

2. **[Bài 6: Cài đặt Teleport](./06-install-teleport.md)**
   * Tải và giải nén gói cài đặt binary của Teleport v13.2.0.
   * Di chuyển các file thực thi (`teleport`, `tctl`, `tsh`) vào `/usr/local/bin/`.
   * Khởi tạo thư mục cấu hình `/etc/teleport/`.
