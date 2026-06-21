# AWS Services cho DevOps / CI-CD

Thư mục này mô tả các dịch vụ AWS thường được sử dụng trong quy trình DevOps và CI/CD. Mỗi dịch vụ được trình bày với tên, mô tả ngắn, trường hợp sử dụng và hướng dẫn cơ bản để bắt đầu.

---

## Mục lục

| # | Dịch vụ | Mô tả ngắn |
|---|---------|------------|
| 01 | [EC2 (Amazon Elastic Compute Cloud)](1. EC2/1. Amazon EC2.md) | Máy chủ ảo (Virtual Server) |
| 02 | [IAM (Identity & Access Management)](2. IAM/1. Amazon IAM.md) | Quản lý định danh & quyền truy cập (IAM) |
| 03 | [S3 (Amazon Simple Storage Service)](3. S3/1. Amazon S3.md) | Lưu trữ đối tượng (Object Storage) |
| 04 | [ELB & Auto Scaling (Cân bằng tải & Co giãn)](4. ELB & Auto Scaling/1. Amazon ELB.md) | Bộ cân bằng tải và Co giãn tự động (ELB & ASG) |
| 05 | [RDS (Relational Database Service)](5. RDS/1. Amazon RDS Overview.md) | Cơ sở dữ liệu quan hệ được quản lý (Managed SQL Database) |
| 06 | [DynamoDB (Amazon DynamoDB)](6. DynamoDB/1. NoSQL Overview.md) | Cơ sở dữ liệu NoSQL được quản lý (Managed NoSQL Database) |
| 07 | [AWS Lambda (Serverless Compute)](7.%20AWS%20Lambda/1.%20AWS%20Lambda%20Overview.md) | Dịch vụ tính toán Serverless (Serverless Compute) |
| 08 | [VPC (Virtual Private Cloud)](8. VPC/1. VPC Overview.md) | Mạng ảo dùng riêng (Virtual Private Cloud) |
| 09 | [API Gateway & Cognito](9.%20API%20Gateway%20&%20Cognito/1.%20Amazon%20API%20Gateway%20Overview.md) | Quản lý API & Định danh người dùng (API Gateway & Identity) |
| 10 | [EKS (Elastic Kubernetes Service)](10.%20EKS.md) | Dịch vụ Kubernetes được quản lý (Managed Kubernetes) |
| 11 | [ECS (Elastic Container Service)](11.%20ECS.md) | Điều phối container (Container Orchestration) |
| 12 | [ECR (Elastic Container Registry)](12.%20ECR.md) | Kho lưu trữ Docker image (Docker Registry) |
| 13 | [CodePipeline / CodeBuild / CodeDeploy](13.%20CodePipeline.md) | Bộ dịch vụ CI/CD nguyên bản của AWS (Pipeline) |
| 14 | [Route 53](14.%20Route%2053.md) | Hệ thống phân giải tên miền (DNS) |
| 15 | [CloudFront](15.%20CloudFront.md) | Mạng phân phối nội dung (CDN) |
| 16 | [ACM (Certificate Manager)](16.%20ACM.md) | Quản lý chứng chỉ bảo mật TLS/SSL (ACM) |
| 17 | [EFS (Elastic File System)](17.%20EFS.md) | Hệ thống tệp lưu trữ dùng chung (Shared Storage) |

---

## Lưu ý chung

- Tất cả các dịch vụ trên nên được cấu hình bằng IaC (Terraform, CloudFormation) để đảm bảo tính tái sử dụng và đồng bộ.
- Không commit AWS Access Key, Secret Key, hoặc bất kỳ thông tin xác thực nào vào repository.
- Ưu tiên sử dụng IAM Role thay vì Access Key khi có thể.
- Tham khảo thư mục `cloud/aws/lab/` để xem các deploy template tích hợp với các dịch vụ này.
