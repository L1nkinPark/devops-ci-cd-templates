# Hướng dẫn Triển khai Uptime Kuma bằng Helm trên Kubernetes

Tài liệu này hướng dẫn chi tiết các bước cấu hình và triển khai **Uptime Kuma** (công cụ giám sát trạng thái dịch vụ self-hosted) sử dụng Helm Chart kết hợp với hệ thống lưu trữ **NFS Storage (PV & PVC)** đã cấu hình trước đó trong namespace `monitoring`.

---

## 1. Sơ đồ Kiến trúc Hoạt động

Dưới đây là luồng hoạt động của hệ thống lưu trữ Uptime Kuma:

```text
       [ Người dùng / Quản trị viên ]
                    │
                    ▼ (Kết nối Web UI)
         [ Uptime Kuma Service / Ingress ]
                    │
                    ▼ (Lưu cơ sở dữ liệu SQLite)
      [ PVC: uptime-kuma-pvc (5Gi) ]
                    │
        [ PV: uptime-kuma-pv (NFS) ]
                    │
  [ NFS Server Share: /data/monitoring ]
```

---

## 2. Quy trình Triển khai Chi tiết

Quá trình này có thể được thực hiện trực tiếp trên máy chủ **k8s-master-1** hoặc thông qua **kubectl shell trên giao diện Rancher**.

### BƯỚC 1: Khởi tạo môi trường & Cấp phát ổ đĩa (PV & PVC)

1. **Khởi tạo Namespace `monitoring`** (nếu chưa có):
   ```bash
   kubectl create namespace monitoring
   ```

2. **Cấu hình lưu trữ vật lý trên NFS Server** (Thực hiện trên máy chủ NFS):
   Tạo thư mục chia sẻ cho giám sát và phân quyền ghi đọc đầy đủ để tránh lỗi Permission Denied từ Pod:
   ```bash
   sudo mkdir -p /data/monitoring
   sudo chown -R nobody:nogroup /data/
   sudo chmod -R 777 /data
   ```

3. **Áp dụng cấu hình PV & PVC cho Uptime Kuma**:
   Đảm bảo tệp `uptime-kuma-pv-pvc.yml` đã được cập nhật đúng địa chỉ IP của NFS Server, sau đó triển khai:
   ```bash
   kubectl apply -f on-premise/kubernetes/storage/uptime-kuma-pv-pvc.yml -n monitoring
   ```

4. **Kiểm tra trạng thái liên kết đĩa (PVC)**:
   Bạn có thể đăng nhập giao diện **Rancher** để xem PVC `uptime-kuma-pvc` đã chuyển sang trạng thái **`Bound`** hay chưa, hoặc kiểm tra bằng CLI:
   ```bash
   kubectl get pvc uptime-kuma-pvc -n monitoring
   ```

---

### BƯỚC 2: Tạo thư mục làm việc & Chuẩn bị cấu hình

1. **Tạo thư mục làm việc trên K8S Master**:
   ```bash
   mkdir -p uptime-kuma
   cd uptime-kuma
   ```

2. **Khởi tạo file cấu hình `values.yaml`**:
   Sao chép tệp mẫu `values.yml.example` sang `values.yaml` trong thư mục làm việc của bạn:
   ```bash
   cp on-premise/kubernetes/uptime-kuma/values.yml.example values.yaml
   ```

3. **Thêm kho lưu trữ Uptime Kuma Helm & Cập nhật**:
   ```bash
   helm repo add uptime-kuma https://dirsigler.github.io/uptime-kuma-helm
   helm repo update
   ```

---

### BƯỚC 3: Cài đặt Uptime Kuma bằng Helm

Thực hiện lệnh cài đặt với tệp cấu hình `values.yaml` trong namespace `monitoring`:

```bash
helm install uptime-kuma uptime-kuma/uptime-kuma --values values.yaml --namespace monitoring
```

> [!NOTE]
> Nếu bạn muốn nâng cấp hoặc cập nhật cấu hình trong tương lai, chỉ cần chỉnh sửa `values.yaml` và chạy lệnh:
> `helm upgrade uptime-kuma uptime-kuma/uptime-kuma --values values.yaml --namespace monitoring`

---

## 3. Các lệnh kiểm tra vận hành và giám sát

Sau khi triển khai thành công, hãy thực hiện các bước sau để đảm bảo Uptime Kuma hoạt động ổn định:

### 1. Kiểm tra trạng thái các Pods và Services
```bash
# Kiểm tra danh sách các Pod (Đợi cho tới khi pod ở trạng thái Running)
kubectl get pods -n monitoring -l app.kubernetes.io/name=uptime-kuma -w

# Kiểm tra danh sách Services
kubectl get svc -n monitoring -l app.kubernetes.io/name=uptime-kuma
```

### 2. Xem log của Uptime Kuma để xác nhận hoạt động
```bash
kubectl logs deployment/uptime-kuma -n monitoring --tail=100
```
