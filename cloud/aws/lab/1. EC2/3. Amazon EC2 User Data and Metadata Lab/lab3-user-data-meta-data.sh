#!/bin/bash
# 1. Cài đặt Apache Web Server và khởi động dịch vụ
yum install httpd -y
service httpd start
chkconfig httpd on

# 2. Di chuyển vào thư mục gốc của trang web
cd /var/www/html
echo "<html>" > index.html

# 3. Tạo cấu trúc trang web cơ bản
echo "<h1>Welcome to AWS</h1>" >> index.html
echo "<h4>You are running instance from this IP (For debug only!!!!Do not public this to user):</h4>" >> index.html

# 4. Sử dụng IMDSv2 để lấy Session Token bảo mật (thời gian sống 6 tiếng)
export TOKEN=`curl -X PUT "http://169.254.169.254/latest/api/token" -H "X-aws-ec2-metadata-token-ttl-seconds: 21600"`

# 5. Truy xuất Private IP từ Metadata và ghi vào trang web
echo "<br>Private IP: " >> index.html
curl -H "X-aws-ec2-metadata-token: $TOKEN" -v http://169.254.169.254/latest/meta-data/local-ipv4 >> index.html

# 6. Truy xuất Public IP từ Metadata và ghi vào trang web
echo "<br>Public IP: " >> index.html
curl -H "X-aws-ec2-metadata-token: $TOKEN" -v http://169.254.169.254/latest/meta-data/public-ipv4 >> index.html 

echo "</html>" >> index.html
