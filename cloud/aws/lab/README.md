# AWS Pipeline Templates

Thư mục này chứa các CI/CD pipeline template để deploy ứng dụng lên các dịch vụ AWS như EKS, ECS, và push image lên ECR. Các template được thiết kế để có thể tái sử dụng cho nhiều dự án, chỉ cần thay đổi các biến (variable) theo từng môi trường.

---

## Nội dung chính

### 1. Pipeline cho GitHub Actions deploy lên EKS/ECS

Các workflow `.yml` để tích hợp với GitHub Actions, thực hiện:

- Build Docker image và push lên ECR.
- Deploy lên EKS bằng `kubectl apply` hoặc Helm chart.
- Deploy lên ECS bằng `aws ecs update-service` hoặc tạo task definition mới.
- Hỗ trợ đa môi trường (dev, staging, production) qua GitHub Environments.

**File mẫu:**

| File | Mô tả |
|------|-------|
| `github-actions-eks-deploy.yml` | Build, push ECR, deploy lên EKS bằng kubectl/Helm |
| `github-actions-ecs-deploy.yml` | Build, push ECR, cập nhật ECS service |
| `github-actions-ecr-push.yml` | Chỉ build và push image lên ECR |

### 2. Pipeline cho GitLab CI push image lên ECR

Các file `.gitlab-ci.yml` template để:

- Build Docker image trong GitLab Runner.
- Đăng nhập và push image lên AWS ECR.
- Kích hoạt (trigger) deploy lên EKS/ECS từ GitLab CI.

**File mẫu:**

| File | Mô tả |
|------|-------|
| `gitlab-ci-ecr-push.yml` | Build và push image lên ECR |
| `gitlab-ci-eks-deploy.yml` | Push image + deploy lên EKS |
| `gitlab-ci-ecs-deploy.yml` | Push image + cập nhật ECS service |

### 3. CodePipeline / CodeBuild Templates

Template cho bộ CI/CD native của AWS:

- **`buildspec.yml`**: File cấu hình cho CodeBuild, định nghĩa các phase (install, pre_build, build, post_build).
- **CodePipeline definition**: Cấu hình pipeline với các stage Source → Build → Deploy.
- **CodeDeploy `appspec.yml`**: Định nghĩa cách deploy lên EC2 hoặc ECS (blue/green).

**File mẫu:**

| File | Mô tả |
|------|-------|
| `buildspec-docker.yml` | CodeBuild: build Docker image và push lên ECR |
| `buildspec-maven.yml` | CodeBuild: build ứng dụng Java bằng Maven, chạy test |
| `appspec-ecs-blue-green.yml` | CodeDeploy: blue/green deployment cho ECS |
| `codepipeline-eks.json` | CodePipeline definition: GitHub → CodeBuild → EKS |

### 4. Hướng dẫn thực hành triển khai cơ bản (EC2 Hands-on Labs)

Các hướng dẫn thực hành deploy ứng dụng và cấu hình hạ tầng EC2 từng bước (step-by-step):

| File | Mô tả | Giao thức / Công nghệ |
|------|-------|-----------------------|
| [1. Amazon EC2 Hands-on Lab(Linux)](1.%20EC2/1.%20Amazon%20EC2%20Hands-on%20Lab%28Linux%29.md) | Khởi tạo EC2 Linux, SSH từ Windows, cài đặt httpd, Snapshot/AMI | SSH, HTTP, Apache |
| [2. Amazon EC2 Hands-on Lab(Windows)](1.%20EC2/2.%20Amazon%20EC2%20Hands-on%20Lab%28Windows%29.md) | Khởi tạo EC2 Windows Server, giải mã mật khẩu Administrator, đăng nhập RDP | RDP, Windows Server |
| [3. Amazon EC2 User Data and Metadata Lab](1.%20EC2/3.%20Amazon%20EC2%20User%20Data%20and%20Metadata%20Lab/3.%20Amazon%20EC2%20User%20Data%20and%20Metadata%20Lab.md) | Tự động hóa cài đặt Web Server và lấy IP động qua IMDSv2 | User Data, IMDSv2, Bash |
| [4. Amazon EC2 Hands-on Lab(Windows Volume)](1.%20EC2/4.%20Amazon%20EC2%20Hands-on%20Lab%28Windows%20Volume%29.md) | Tạo EBS Volume, gắn vào instance, online và định dạng NTFS | EBS, Windows Disk Mgmt |
| [5. Amazon EC2 Hands-on Lab(Linux Volume)](1.%20EC2/5.%20Amazon%20EC2%20Hands-on%20Lab%28Linux%20Volume%29.md) | EBS volume, fdisk phân vùng, định dạng XFS, cấu hình auto-mount trong /etc/fstab, mở rộng dung lượng trực tuyến | EBS, fdisk, XFS, growpart |
| [6. Amazon EC2 Hands-on Lab(Add Member SSH)](1.%20EC2/6.%20Amazon%20EC2%20Hands-on%20Lab%28Add%20Member%20SSH%29.md) | Tạo user dev01, cấu hình phân quyền thư mục .ssh (700) và authorized_keys (600) | SSH, Linux Security |

### 5. Hướng dẫn thực hành IAM (IAM Hands-on Labs)

Các hướng dẫn thực hành quản lý người dùng, nhóm và phân quyền trên AWS IAM:

| File | Mô tả | Công nghệ |
|------|-------|-----------|
| [1. Amazon IAM Hands-on Lab(User, Group and Policy)](2.%20IAM/1.%20Amazon%20IAM%20Hands-on%20Lab%28User%2C%20Group%20and%20Policy%29.md) | Tạo nhóm AdministratorAccess, tạo người dùng, thêm vào nhóm, tải thông tin đăng nhập (csv credentials) và đăng nhập giao diện console | AWS IAM, AWS Console |
| [2. Amazon IAM Hands-on Lab(AWS CLI and MFA)](2.%20IAM/2.%20Amazon%20IAM%20Hands-on%20Lab%28AWS%20CLI%20and%20MFA%29.md) | Cài đặt AWS CLI, cấu hình truy cập qua Access Key/Secret Key, các lệnh S3 cơ bản, chính sách ép buộc xác thực MFA, xử lý lỗi AccessDenied và cấu hình profile MFA | AWS IAM, AWS CLI |
| [3. Amazon IAM Hands-on Lab(IAM Role for EC2)](2.%20IAM/3.%20Amazon%20IAM%20Hands-on%20Lab%28IAM%20Role%20for%20EC2%29.md) | Tạo IAM Role cho phép EC2 truy cập dịch vụ S3, gán role vào máy chủ ảo và kiểm tra kết nối không cần key | AWS IAM, S3, EC2 |
| [4. Amazon IAM Hands-on Lab(Assume Role with AWS CLI)](2.%20IAM/4.%20Amazon%20IAM%20Hands-on%20Lab%28Assume%20Role%20with%20AWS%20CLI%29.md) | Gỡ quyền trực tiếp của User, tạo Role PowerUserAccess với Custom Trust Policy, và dùng AWS CLI assume-role với profile credentials tạm thời | AWS IAM, AWS CLI, STS |

### 6. Hướng dẫn thực hành S3 (S3 Hands-on Labs)

Các hướng dẫn thực hành quản lý thùng chứa và đối tượng trên AWS S3:

| File | Mô tả | Công nghệ |
|------|-------|-----------|
| [1. Amazon S3 Hands-on Lab(Basic)](3.%20S3/1.%20Amazon%20S3%20Hands-on%20Lab%28Basic%29.md) | Các thao tác cơ bản bao gồm truy cập S3 Console, khởi tạo bucket, tạo thư mục, tải lên tệp tin và thực hiện di chuyển (move) đối tượng giữa các thư mục | AWS S3, AWS Console |
| [2. Amazon S3 Versioning Lab](3.%20S3/2.%20Amazon%20S3%20Versioning%20Lab.md) | Các bước thực hành bật tính năng quản lý phiên bản (Versioning) cho bucket S3, tải lên, chỉnh sửa và ghi đè tệp tin để xem phiên bản, thực hiện xóa để kiểm nghiệm Delete Marker và hiển thị phiên bản | AWS S3, AWS Console |
| [3. Amazon S3 Pre-signed URL Lab](3.%20S3/3.%20Amazon%20S3%20Pre-signed%20URL%20Lab.md) | Các bước thực hành kiểm tra cấu hình kết nối AWS CLI, cấu hình chặn truy cập công khai và tạo đường dẫn ký trước (Pre-signed URL) để cấp quyền truy cập tạm thời | AWS S3, AWS Console, AWS CLI |
| [4. Amazon S3 Lifecycle Lab](3.%20S3/4.%20Amazon%20S3%20Lifecycle%20Lab.md) | Thực hành cấu hình tự động chuyển đổi lớp lưu trữ sau 90 ngày sang Glacier và xóa hoàn toàn sau 270 ngày | AWS S3, AWS Console |
| [5. Amazon S3 Static Website Hosting Lab](3.%20S3/5.%20Amazon%20S3%20Static%20Website%20Hosting%20Lab.md) | Thực hành upload mã nguồn qua AWS CLI, bật Static Website Hosting và cấu hình Public Access / Bucket Policy | AWS S3, AWS Console, AWS CLI |
| [6. Amazon S3 Event Notifications Lab](3.%20S3/6.%20Amazon%20S3%20Event%20Notifications%20Lab.md) | Thực hành cấu hình S3 Event Notification kết hợp với Lambda Function, kiểm tra log tự động qua CloudWatch khi tải lên đối tượng | AWS S3, AWS Lambda, AWS Console |

### 7. Hướng dẫn thực hành ELB & Auto Scaling (ELB & ASG Hands-on Labs)

Các hướng dẫn thực hành quản lý bộ cân bằng tải và tự động co giãn trên AWS ELB và Auto Scaling:

| File | Mô tả | Công nghệ |
|------|-------|-----------|
| [1. Amazon ELB Hands-on Lab](4.%20ELB%20%26%20Auto%20Scaling/1.%20Amazon%20ELB%20Hands-on%20Lab.md) | Cấu hình cân bằng tải bằng Application Load Balancer (ALB) kết hợp với 2 EC2 instances ở các zone khác nhau chạy script User Data phân biệt | AWS ELB, ALB, EC2, User Data |
| [2. Amazon Auto Scaling Group Hands-on Lab](4.%20ELB%20%26%20Auto%20Scaling/2.%20Amazon%20Auto%20Scaling%20Group%20Hands-on%20Lab.md) | Các bước thực hành chuẩn bị Base Image (Golden Image) từ EC2 gốc bằng cách kích hoạt dịch vụ httpd tự chạy cùng hệ thống và đóng gói thành AMI | AWS ASG, EC2, SSH, AMI, Systemd |

### 8. Hướng dẫn thực hành RDS (RDS Hands-on Labs)

Các hướng dẫn thực hành quản lý và triển khai cơ sở dữ liệu trên Amazon RDS:

| File | Mô tả | Công nghệ |
|------|-------|-----------|
| [1. Amazon RDS Hands-on Lab(Basic)](5.%20RDS/1.%20Amazon%20RDS%20Hands-on%20Lab%28Basic%29.md) | Thực hành tạo một RDS Instance sử dụng tùy chọn Full Configuration với cơ sở dữ liệu MySQL và cấu hình phần cứng db.t3.medium | AWS RDS, MySQL, db.t3.medium |
| [2. Amazon RDS Hands-on Lab(Cluster)](5.%20RDS/2.%20Amazon%20RDS%20Hands-on%20Lab%28Cluster%29.md) | Thực hành tạo một RDS Cluster gồm 1 Writer và 2 Readers, giải thích vai trò của các node, các loại Endpoint và kết nối qua Cluster Write Endpoint | AWS RDS, DB Cluster, Writer/Reader Endpoints |
| [3. Amazon Aurora Hands-on Lab(Backtrack)](5.%20RDS/3.%20Amazon%20Aurora%20Hands-on%20Lab%28Backtrack%29.md) | Thực hành tạo Aurora DB Cluster với tính năng Backtrack, thực hiện xóa dữ liệu và quay ngược thời gian (Backtracking) để khôi phục dữ liệu | AWS Aurora, Backtrack, DB Cluster |

### 9. Hướng dẫn thực hành DynamoDB (DynamoDB Hands-on Labs)

Các hướng dẫn thực hành quản lý và thao tác với cơ sở dữ liệu NoSQL trên Amazon DynamoDB:

| File | Mô tả | Công nghệ |
|------|-------|-----------|
| [1. Amazon DynamoDB Hands-on Lab(Basic)](6.%20DynamoDB/1.%20Amazon%20DynamoDB%20Hands-on%20Lab%28Basic%29.md) | Thực hành tạo bảng student với Partition Key (id) và Sort Key (name), nhập các dữ liệu học sinh với cấu trúc động và trường tùy biến | AWS DynamoDB, AWS Console, NoSQL |
| [2. Amazon DynamoDB Hands-on Lab(Index)](6.%20DynamoDB/2.%20Amazon%20DynamoDB%20Hands-on%20Lab%28Index%29.md) | Thực hành tạo Global Secondary Index (GSI) với partition key (name) và sort key (birthday), truy vấn kiểm nghiệm dữ liệu qua GSI | AWS DynamoDB, AWS Console, Index |

### 10. Hướng dẫn thực hành AWS Lambda (AWS Lambda Hands-on Labs)

Các hướng dẫn thực hành viết code và cấu hình vận hành tự động trên AWS Lambda:

| File | Mô tả | Công nghệ |
|------|-------|-----------|
| [1. Hello Lambda (Làm quen với AWS Lambda Console)](7.%20AWS%20Lambda/1.%20Hello%20Lambda.md) | Thực hành tạo hàm Lambda đơn giản trả về Hello World, cấu hình sự kiện kiểm thử (Test Event) và thực thi kiểm nghiệm | AWS Lambda, Python, AWS Console |
| [2. AWS Lambda Hands-on Lab(Resize Image on S3)](7.%20AWS%20Lambda/2.%20AWS%20Lambda%20Hands-on%20Lab%28Resize%20Image%20on%20S3%29/2.%20AWS%20Lambda%20Hands-on%20Lab%28Resize%20Image%20on%20S3%29.md) | Tự động co nhỏ kích thước ảnh (Thumbnail 300x300) khi có ảnh tải lên S3 bucket nguồn và upload ảnh kết quả lên S3 bucket đích | AWS Lambda, S3, IAM, Python (Pillow) |
| [3. AWS Lambda Hands-on Lab(EC2 Auto Start-Stop)](7.%20AWS%20Lambda/3.%20AWS%20Lambda%20Hands-on%20Lab%28EC2%20Auto%20Start-Stop%29/3.%20AWS%20Lambda%20Hands-on%20Lab%28EC2%20Auto%20Start-Stop%29.md) | Lập lịch tự động bật/tắt các máy chủ EC2 có gắn thẻ tag chỉ định (ví dụ: Env: Dev) qua EventBridge Rules để tiết kiệm chi phí | AWS Lambda, EC2, EventBridge, Python (boto3) |
| [4. AWS Lambda Hands-on Lab(Read CSV and Save to DynamoDB)](7.%20AWS%20Lambda/4.%20AWS%20Lambda%20Hands-on%20Lab%28Read%20CSV%20and%20Save%20to%20DynamoDB%29/4.%20AWS%20Lambda%20Hands-on%20Lab%28Read%20CSV%20and%20Save%20to%20DynamoDB%29.md) | Tự động hóa quy trình ETL đọc tệp tin dữ liệu CSV từ S3, phân tích cú pháp và ghi trực tiếp các bản ghi vào bảng DynamoDB | AWS Lambda, S3, DynamoDB, Python (csv) |

### 11. Hướng dẫn thực hành VPC (VPC Hands-on Labs)

Các hướng dẫn thực hành thiết kế, phân hoạch mạng và cấu hình bảo mật trên AWS VPC:

| [1. Lab 1 – Thiết kế VPC Đơn giản](8.%20VPC/1.%20Lab%201%20-%20Thi%E1%BA%BFt%20k%E1%BA%BF%20VPC%20%C4%90%C6%A1n%20gi%E1%BA%A3n.md) | Thực hành thiết kế sơ đồ phân hoạch mạng và liên kết Security Groups (Draw.io/PowerPoint) đáp ứng Multi-AZ | AWS VPC, Subnetting, Security Group, Draw.io |
| [2. Lab 2 – Tạo VPC đã thiết kế](8.%20VPC/2.%20Lab%202%20-%20T%E1%BA%A1o%20VPC%20%C4%91%C3%A3%20thi%E1%BA%BFt%20k%E1%BA%BF.md) | Triển khai thực tế trên AWS Console cấu hình tạo VPC, 4 Subnets và gắn Internet Gateway | AWS VPC, Subnetting, Internet Gateway, AWS Console |
| [3. Lab 3 – Test kết nối trên VPC đã tạo](8.%20VPC/3.%20Lab%203%20-%20Test%20k%E1%BA%BFt%20n%E1%BB%91i%20tr%C3%AAn%20VPC%20%C4%91%C3%A3%20t%E1%BA%A1o.md) | Khởi tạo máy chủ EC2, kiểm tra kết nối mạng Internet qua IGW và gán Elastic IP | AWS VPC, EC2, Elastic IP, Internet Gateway |
| [4. Lab 4 – VPC Peering](8.%20VPC/4.%20Lab%204%20-%20VPC%20Peering.md) | Thực hành VPC Peering kết nối 2 VPC độc lập và cấu hình Route Table, Security Group | AWS VPC, VPC Peering, Route Table, Security Group |

### 12. Hướng dẫn thực hành API Gateway & Cognito (API Gateway & Cognito Hands-on Labs)

Các hướng dẫn thực hành xây dựng cổng API và quản lý danh tính người dùng:

| File | Mô tả | Công nghệ |
|------|-------|-----------|
| [1. Lab 1 – API Gateway sử dụng Lambda làm backend](9.%20API%20Gateway%20%26%20Cognito/1.%20Lab%201%20-%20API%20Gateway%20with%20Lambda%20Backend/1.%20Lab%201%20-%20API%20Gateway%20with%20Lambda%20Backend.md) | Xây dựng REST API trên API Gateway định tuyến và chuyển tiếp các yêu cầu tính toán sang Lambda backend xử lý (phương thức Non-Proxy Integration) | AWS API Gateway, AWS Lambda, Python 3.12 |
| [2. Lab 2 – API Key và Usage Plan trong API Gateway](9.%20API%20Gateway%20%26%20Cognito/2.%20Lab%202%20-%20API%20Key%20and%20Usage%20Plan/2.%20Lab%202%20-%20API%20Key%20and%20Usage%20Plan.md) | Thiết lập bảo mật, giới hạn tần suất (Rate Limiting/Throttling) và hạn mức cuộc gọi (Quota) bằng API Key và Usage Plan | AWS API Gateway, Postman |
| [3. Lab 3 – Cognito Operation Basic](9.%20API%20Gateway%20%26%20Cognito/3.%20Lab%203%20-%20Cognito%20Operation%20Basic/3.%20Lab%203%20-%20Cognito%20Operation%20Basic.md) | Khởi tạo Cognito User Pool, cấu hình thuộc tính bắt buộc, tạo tài khoản người dùng bằng quyền Admin và quản lý nhóm người dùng | AWS Cognito, Admin Panel |
| [4. Lab 4 – Sử dụng Cognito Hosted UI để login và lấy token](9.%20API%20Gateway%20%26%20Cognito/4.%20Lab%204%20-%20Cognito%20Hosted%20UI%20Login%20and%20Token/4.%20Lab%204%20-%20Cognito%20Hosted%20UI%20Login%20and%20Token.md) | Đăng nhập kiểm thử qua Hosted UI với tài khoản có sẵn và đăng ký tài khoản tự do (Self Sign-up) | AWS Cognito, Hosted UI |
| [5. Lab 5 – Kết hợp API Gateway & Cognito](9.%20API%20Gateway%20%26%20Cognito/5.%20Lab%205%20-%20Integrate%20API%20Gateway%20and%20Cognito/5.%20Lab%205%20-%20Integrate%20API%20Gateway%20and%20Cognito.md) | Liên kết API Gateway REST API với Cognito Authorizer để xác thực token người dùng | AWS API Gateway, AWS Cognito |

### 13. Hướng dẫn thực hành CloudFront (CloudFront Hands-on Labs)

Các hướng dẫn thực hành phân phối nội dung tĩnh và động toàn cầu bằng Amazon CloudFront CDN:

| File | Mô tả | Công nghệ |
|------|-------|-----------|
| [1. Lab 1 – Sử dụng CloudFront kết hợp với S3](10.%20CloudFront/1.%20Lab%201%20-%20Integrate%20CloudFront%20with%20S3/1.%20Lab%201%20-%20Integrate%20CloudFront%20with%20S3.md) | Cấu hình CloudFront phân phối static website từ S3 bucket private sử dụng Origin Access Control (OAC) và cập nhật Bucket Policy | AWS CloudFront, AWS S3, OAC, Bucket Policy |
| [2. Lab 2 – Sử dụng CloudFront kết hợp với API Gateway and S3](10.%20CloudFront/2.%20Lab%202%20-%20Integrate%20CloudFront%20with%20API%20Gateway%20and%20S3/2.%20Lab%202%20-%20Integrate%20CloudFront%20with%20API%20Gateway%20and%20S3.md) | Cấu hình CloudFront Multi-Origin phân luồng định tuyến tĩnh (S3) và động (API Gateway) qua Cache Behaviors, Cache Policy và Origin Request Policy | AWS CloudFront, AWS API Gateway, Multi-Origin, CachingDisabled, AllViewer |

### 14. Hướng dẫn thực hành Route 53 (Route 53 Hands-on Labs)

Các hướng dẫn thực hành cấu hình hệ thống tên miền (DNS), quản lý định tuyến lưu lượng và giám sát sức khỏe bằng Amazon Route 53:

| File | Mô tả | Công nghệ |
|------|-------|-----------|
| [1. Lab 1 – Đăng ký tên miền (Register Domain)](11.%20Route%2053/1.%20Lab%201%20-%20Register%20Domain/1.%20Lab%201%20-%20Register%20Domain.md) | Đăng ký mua và sở hữu tên miền riêng trực tiếp trên Route 53 và tắt Auto-renew | AWS Route 53, Domain Registration |
| [2. Lab 2 – Thực hành A-Record & Root Domain](11.%20Route%2053/2.%20Lab%202%20-%20A-Record%20and%20Root%20Domain%20to%20EC2/2.%20Lab%202%20-%20A-Record%20and%20Root%20Domain%20to%20EC2.md) | Cấu hình bản ghi A trỏ subdomain và root domain (hoặc sử dụng ALIAS trỏ ELB) về máy chủ web EC2 | AWS Route 53, A-Record, ALIAS, EC2 |
| [3. Lab 3 – Thực hành CNAME Record](11.%20Route%2053/3.%20Lab%203%20-%20CNAME%20Record/3.%20Lab%203%20-%20CNAME%20Record.md) | Liên kết subdomain qua CNAME tới CloudFront, tích hợp xác thực DNS để cấp SSL từ ACM | AWS Route 53, CNAME, AWS ACM, CloudFront |
| [4. Lab 4 – Route 53 Health Check & Failover](11.%20Route%2053/4.%20Lab%204%20-%20Route%2053%20Health%20Check/4.%20Lab%204%20-%20Route%2053%20Health%20Check.md) | Thiết lập Health Check giám sát EC2 chính và cấu hình Failover routing chuyển hướng sang S3 dự phòng | AWS Route 53, Health Check, Failover Routing |
| [5. Lab 5 – Thực hành Private Hosted Zone](11.%20Route%2053/5.%20Lab%205%20-%20Private%20Hosted%20Zone/5.%20Lab%205%20-%20Private%20Hosted%20Zone.md) | Cấu hình phân giải tên miền nội bộ giữa các VPC bảo mật, kiểm tra tra cứu thành công từ mạng AWS và bị chặn bên ngoài | AWS Route 53, Private Hosted Zone, VPC |

---

## Cấu trúc khuyến nghị

```text
cloud/aws/lab/
  github-actions/
    github-actions-eks-deploy.yml
    github-actions-ecs-deploy.yml
    github-actions-ecr-push.yml
  gitlab-ci/
    gitlab-ci-ecr-push.yml
    gitlab-ci-eks-deploy.yml
    gitlab-ci-ecs-deploy.yml
  codepipeline/
    buildspec-docker.yml
    buildspec-maven.yml
    appspec-ecs-blue-green.yml
    codepipeline-eks.json
  1. EC2/
    1. Amazon EC2 Hands-on Lab(Linux).md
    2. Amazon EC2 Hands-on Lab(Windows).md
    3. Amazon EC2 User Data and Metadata Lab/
      3. Amazon EC2 User Data and Metadata Lab.md
      README.md
      user_data.sh
    4. Amazon EC2 Hands-on Lab(Windows Volume).md
    5. Amazon EC2 Hands-on Lab(Linux Volume).md
    6. Amazon EC2 Hands-on Lab(Add Member SSH).md
  2. IAM/
    1. Amazon IAM Hands-on Lab(User, Group and Policy).md
    2. Amazon IAM Hands-on Lab(AWS CLI and MFA).md
    3. Amazon IAM Hands-on Lab(IAM Role for EC2).md
  3. S3/
    1. Amazon S3 Hands-on Lab(Basic).md
    2. Amazon S3 Versioning Lab.md
    3. Amazon S3 Pre-signed URL Lab.md
    4. Amazon S3 Lifecycle Lab.md
    5. Amazon S3 Static Website Hosting Lab.md
    6. Amazon S3 Event Notifications Lab.md
  4. ELB & Auto Scaling/
    1. Amazon ELB Hands-on Lab.md
    2. Amazon Auto Scaling Group Hands-on Lab.md
  5. RDS/
    1. Amazon RDS Hands-on Lab(Basic).md
    2. Amazon RDS Hands-on Lab(Cluster).md
    3. Amazon Aurora Hands-on Lab(Backtrack).md
  6. DynamoDB/
    1. Amazon DynamoDB Hands-on Lab(Basic).md
    2. Amazon DynamoDB Hands-on Lab(Index).md
  7. AWS Lambda/
    1. Hello Lambda.md
    2. AWS Lambda Hands-on Lab(Resize Image on S3)/
      2. AWS Lambda Hands-on Lab(Resize Image on S3).md
      README.md
      lambda_function.py
    3. AWS Lambda Hands-on Lab(EC2 Auto Start-Stop)/
      3. AWS Lambda Hands-on Lab(EC2 Auto Start-Stop).md
      README.md
      lambda_function.py
    4. AWS Lambda Hands-on Lab(Read CSV and Save to DynamoDB)/
      4. AWS Lambda Hands-on Lab(Read CSV and Save to DynamoDB).md
      README.md
      lambda_function.py
  8. VPC/
    1. Lab 1 - Thiết kế VPC Đơn giản.md
    2. Lab 2 - Tạo VPC đã thiết kế.md
    3. Lab 3 - Test kết nối trên VPC đã tạo.md
    4. Lab 4 - VPC Peering.md
  9. API Gateway & Cognito/
    1. Lab 1 - API Gateway with Lambda Backend/
      1. Lab 1 - API Gateway with Lambda Backend.md
      README.md
      calculator-lambda.py
    2. Lab 2 - API Key and Usage Plan/
      2. Lab 2 - API Key and Usage Plan.md
      README.md
    3. Lab 3 - Cognito Operation Basic/
      3. Lab 3 - Cognito Operation Basic.md
      README.md
    4. Lab 4 - Cognito Hosted UI Login and Token/
      4. Lab 4 - Cognito Hosted UI Login and Token.md
      README.md
    5. Lab 5 - Integrate API Gateway and Cognito/
      5. Lab 5 - Integrate API Gateway and Cognito.md
      README.md
  10. CloudFront/
    1. Lab 1 - Integrate CloudFront with S3/
      1. Lab 1 - Integrate CloudFront with S3.md
      README.md
    2. Lab 2 - Integrate CloudFront with API Gateway and S3/
      2. Lab 2 - Integrate CloudFront with API Gateway and S3.md
      README.md
  11. Route 53/
    11. Route 53.md
    1. Lab 1 - Register Domain/
      1. Lab 1 - Register Domain.md
      README.md
    2. Lab 2 - A-Record and Root Domain to EC2/
      2. Lab 2 - A-Record and Root Domain to EC2.md
      README.md
    3. Lab 3 - CNAME Record/
      3. Lab 3 - CNAME Record.md
      README.md
    4. Lab 4 - Route 53 Health Check/
      4. Lab 4 - Route 53 Health Check.md
      README.md
    5. Lab 5 - Private Hosted Zone/
      5. Lab 5 - Private Hosted Zone.md
      README.md
  README.md
```

---

## Quy tắc đặt tên file

Mỗi file pipeline nên được đặt tên theo định dạng (format):

```
<ci-tool>-<cloud-service>-<action>.yml
```

**Giải thích:**

| Thành phần | Giải thích | Ví dụ |
|-----------|------------|-------|
| `ci-tool` | Công cụ CI/CD đang sử dụng | `github-actions`, `gitlab-ci`, `codepipeline`, `buildspec` |
| `cloud-service` | Dịch vụ AWS đích | `eks`, `ecs`, `ecr`, `s3` |
| `action` | Hành động chính của pipeline | `deploy`, `push`, `build`, `blue-green` |

**Ví dụ tên file:**

- `github-actions-eks-deploy.yml` — GitHub Actions deploy lên EKS
- `gitlab-ci-ecr-push.yml` — GitLab CI push image lên ECR
- `buildspec-docker.yml` — CodeBuild buildspec cho Docker build
- `appspec-ecs-blue-green.yml` — CodeDeploy appspec cho ECS blue/green

---

## Biến cần thay đổi

Khi sử dụng các template, thay đổi các biến sau cho phù hợp với dự án:

| Biến | Mô tả | Ví dụ |
|------|-------|-------|
| `AWS_REGION` | Vùng (Region) của AWS | `ap-southeast-1` |
| `AWS_ACCOUNT_ID` | Account ID của tài khoản AWS | `123456789012` |
| `ECR_REPOSITORY` | Tên repository trên ECR | `my-app` |
| `EKS_CLUSTER_NAME` | Tên cụm (cluster) EKS | `my-cluster` |
| `ECS_SERVICE_NAME` | Tên service ECS | `my-service` |
| `ECS_CLUSTER_NAME` | Tên cluster ECS | `my-ecs-cluster` |
| `ENVIRONMENT` | Môi trường deploy | `dev`, `staging`, `prod` |

---

## Lưu ý quan trọng

- Tất cả secret (AWS Access Key, Secret Key) phải được lưu trong CI/CD secret management (GitHub Secrets, GitLab CI Variables), **không** hardcode trong file.
- Ưu tiên sử dụng OIDC / IAM Role thay vì Access Key khi có thể (GitHub Actions hỗ trợ kết nối OIDC trực tiếp với AWS).
- Kiểm tra kỹ quyền IAM của role/user dùng trong pipeline để đảm bảo nguyên tắc phân quyền tối thiểu (least privilege).
- Tham khảo thư mục `cloud/aws/services/` để hiểu rõ từng dịch vụ AWS được sử dụng trong pipeline.
