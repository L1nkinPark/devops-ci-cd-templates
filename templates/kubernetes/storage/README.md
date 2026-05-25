# Kubernetes Storage - Hướng dẫn cấu hình StorageClass, PV và PVC

Thư mục này chứa các template và hướng dẫn cấu hình lưu trữ trong Kubernetes, đặc biệt là sử dụng StorageClass với cơ chế cấp phát thủ công (manual provisioning) cho NFS hoặc Local Storage.

---

## 1. Các câu lệnh thường dùng

### Quản lý StorageClass (SC)
```bash
# Liệt kê tất cả StorageClass
kubectl get sc

# Xem chi tiết cấu hình StorageClass
kubectl describe sc nfs-storage
```

### Quản lý PersistentVolume (PV)
```bash
# Liệt kê tất cả PV trong cluster (PV là tài nguyên toàn cluster, không thuộc namespace)
kubectl get pv

# Xem chi tiết PV cụ thể
kubectl describe pv <ten-pv>
```

### Quản lý PersistentVolumeClaim (PVC)
```bash
# Liệt kê tất cả PVC trong namespace
kubectl get pvc -n <namespace>

# Xem chi tiết PVC cụ thể
kubectl describe pvc <ten-pvc> -n <namespace>
```

---

## 2. Quy trình cấu hình và sử dụng StorageClass thủ công (no-provisioner)

Khi sử dụng `provisioner: kubernetes.io/no-provisioner`, Kubernetes sẽ không tự động tạo ổ đĩa vật lý cho bạn. Bạn cần thực hiện theo quy trình 3 bước sau:

### Bước 1: Tạo StorageClass
Sử dụng file template [storageclass.yml.example](storageclass.yml.example) (bỏ đuôi `.example`):
```bash
kubectl apply -f storageclass.yml
```

### Bước 2: Tạo PersistentVolume (PV) thủ công
Do dùng `no-provisioner`, bạn cần khai báo PV thủ công trỏ tới thư mục NFS đã export trên NFS Server.

Ví dụ file `nfs-pv.yml`:
```yaml
apiVersion: v1
kind: PersistentVolume
metadata:
  name: nfs-pv-example
spec:
  capacity:
    storage: 10Gi
  volumeMode: Filesystem
  accessModes:
    - ReadWriteMany
  persistentVolumeReclaimPolicy: Retain
  storageClassName: nfs-storage
  nfs:
    path: /volume1/k8s-share/example
    server: 192.168.1.100
```
*Lưu ý: Thay thế `path` và `server` trỏ đúng cấu hình NFS của bạn.*

Apply PV:
```bash
kubectl apply -f nfs-pv.yml
```

### Bước 3: Tạo PersistentVolumeClaim (PVC) trong ứng dụng
Ứng dụng sẽ yêu cầu dung lượng lưu trữ thông qua PVC.

Ví dụ file `app-pvc.yml`:
```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: app-nfs-pvc
  namespace: <NAMESPACE>
spec:
  accessModes:
    - ReadWriteMany
  storageClassName: nfs-storage
  resources:
    requests:
      storage: 10Gi
```

Apply PVC:
```bash
kubectl apply -f app-pvc.yml -n <NAMESPACE>
```

---

## 3. Gắn PVC vào Pod / Deployment

Trong spec của Pod hoặc Deployment, gắn PVC đã tạo vào container:

```yaml
spec:
  containers:
    - name: web-app
      image: nginx:alpine
      volumeMounts:
        - name: storage-volume
          mountPath: /usr/share/nginx/html
  volumes:
    - name: storage-volume
      persistentVolumeClaim:
        claimName: app-nfs-pvc
```
