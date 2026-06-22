# Lưu ý cho bài Lab 3: CloudFront và Certificate Manager

> [!WARNING]
> **Lưu ý đặc biệt quan trọng trước khi thực hành Lab 3**
> Trong bài Lab 3, bạn sẽ thực hiện trỏ tên miền sang CloudFront và đồng thời kích hoạt giao thức bảo mật SSL/HTTPS. Để làm được điều đó, bạn bắt buộc phải phát hành một chứng chỉ bảo mật (Certificate) sử dụng dịch vụ **AWS Certificate Manager (ACM)**.

---

## 1. Ràng buộc về Region của Certificate đối với CloudFront

Theo quy ước kỹ thuật của AWS, CloudFront là một dịch vụ phân phối toàn cầu (Global Service). Tuy nhiên, có một nguyên tắc cực kỳ quan trọng:
* **Chứng chỉ SSL/TLS (Certificate) muốn gán được cho CloudFront bắt buộc phải được tạo tại Region `us-east-1` (US East - N. Virginia).**
* Nếu bạn tạo Certificate ở các Region khác (như `ap-southeast-1` - Singapore, `ap-northeast-1` - Tokyo, v.v.), dịch vụ ACM vẫn cấp chứng chỉ bình thường nhưng CloudFront sẽ **không thể nhìn thấy** để gán cho Distribution của bạn.

> [!IMPORTANT]
> **Hành động cần làm:** Khi bắt đầu thực hiện bài Lab 3, hãy nhớ **switch (chuyển đổi) sang Region Virginia (`us-east-1`)** trên thanh menu của AWS Console trước khi thực hiện các bước tạo Certificate trong dịch vụ ACM.

---

## 2. Kiến trúc chứng chỉ trong dự án thực tế

Trong môi trường dự án thực tế chạy trên AWS, thông thường bạn sẽ phải tạo **2 Certificate** riêng biệt cho cùng một tên miền:

1. **Certificate thứ nhất (tại Region chứa tài nguyên - ví dụ: Singapore):**
   * Được dùng để gán cho các dịch vụ nội bộ chạy trong Region đó như Application Load Balancer (ALB) hoặc API Gateway để định tuyến an toàn.
2. **Certificate thứ hai (tại Region Virginia - `us-east-1`):**
   * Được dùng để gán cho CloudFront CDN ở lớp ngoài cùng của hệ thống.

*Cả hai chứng chỉ này đều có thể đại diện cho cùng một tên miền hoặc tên miền phụ (ví dụ: `*.h1eudayne.click`), giúp mã hóa lưu lượng HTTPS từ Client đến CloudFront và từ CloudFront đến ALB một cách an toàn và tối ưu.*
