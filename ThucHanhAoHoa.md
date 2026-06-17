# BÁO CÁO THỰC HÀNH: TẠO MÁY ẢO, CẤU HÌNH MẠNG VÀ TRIỂN KHAI ỨNG DỤNG

* **Nội dung:** Thực hành tạo 02 máy ảo, cấu hình kết nối mạng (Bridge/NAT/Host-Only) để liên lạc giữa các máy ảo và triển khai thử nghiệm ứng dụng 2-tier (Web App & Database).
* **Người thực hiện:** [Họ và tên của bạn]
* **Thiết bị/Hệ điều hành sử dụng:** Máy vật lý chạy Windows, phần mềm ảo hóa [VMware Workstation / VirtualBox], hệ điều hành máy ảo [Ubuntu Server 22.04 LTS / CentOS].

---

## 1. Nhật ký thực hành chi tiết

### Bước 1: Khởi tạo 02 Máy ảo (VM1 và VM2)
1. Tải file ISO hệ điều hành từ trang chủ (Khuyên dùng Ubuntu Server 22.04 LTS để tối ưu hiệu năng chạy CLI).
2. Mở phần mềm ảo hóa và tạo mới máy ảo với các thông số cấu hình:
   * **vCPU:** 1-2 vCPU (Tương ứng 1-2 cores vật lý).
   * **vRAM:** 2 GB.
   * **vDisk:** 20 GB (Chọn chế độ *Thin Provisioning* hoặc *Dynamically allocated* để tiết kiệm dung lượng cho ổ cứng máy vật lý).
3. Tiến hành các bước cài đặt hệ điều hành ban đầu (đặt tên máy, tạo tài khoản user/password). Sau khi cài đặt hoàn tất, tiến hành nhân bản (Clone) hoặc tạo mới VM thứ hai để có 02 máy ảo độc lập: **VM1** và **VM2**.

---

### Bước 2: Cấu hình mạng cho các máy ảo
Để các máy ảo có thể kết nối được với nhau và kết nối ra Internet, tôi tiến hành cấu hình mạng trên phần mềm ảo hóa:

1. **Lựa chọn chế độ mạng:** 
   * **NAT Mode:** Giúp máy ảo có Internet qua mạng của máy vật lý và các máy ảo cùng dải NAT có thể kết nối được với nhau.
   * **Host-Only Mode (hoặc VMnet nội bộ):** Thích hợp khi muốn cô lập máy ảo với Internet nhưng vẫn cho phép máy vật lý và các máy ảo liên lạc được với nhau.
   * **Bridge Mode:** Máy ảo nhận IP trực tiếp từ Router vật lý cùng dải với máy vật lý.
   * *Trong bài thực hành này, tôi chọn chế độ mạng:* **[Chọn chế độ mạng bạn dùng, ví dụ: NAT Mode / VMnet8]**.
2. **Khởi động máy ảo và kiểm tra IP:** Sử dụng lệnh `ip a` (trên Linux) hoặc `ipconfig` (trên Windows) để xem địa chỉ IP được cấp phát tự động (DHCP) hoặc cấu hình IP tĩnh cho cả 2 máy.

---

### Bước 3: Kiểm tra kết nối mạng (Ping test)
1. Từ máy ảo **VM1**, thực hiện gửi gói tin kiểm tra tới địa chỉ IP của **VM2**.
2. Từ máy ảo **VM2**, thực hiện gửi gói tin kiểm tra tới địa chỉ IP của **VM1**.
3. Tiến hành kiểm tra kết nối internet bằng cách ping tới một địa chỉ bên ngoài (ví dụ: `8.8.8.8`).

---

### Bước 4: Xây dựng ứng dụng thử nghiệm (Web App & Database)
Để chứng minh hệ thống ảo hóa hoạt động thực tế, tôi triển khai mô hình ứng dụng 2-tier:
* **VM1 (Application Server):** Cài đặt Web Server (như Nginx/Apache) hoặc ứng dụng Backend (Node.js/Python).
* **VM2 (Database Server):** Cài đặt và cấu hình hệ quản trị cơ sở dữ liệu (MySQL/MariaDB/PostgreSQL) cho phép kết nối từ xa từ IP của VM1.
* Tiến hành kết nối từ Web App ở VM1 sang CSDL ở VM2 và hiển thị dữ liệu lên giao diện Web.

---

## 2. Minh chứng thực hành thành công (Nơi chèn ảnh chụp màn hình)

*Lưu ý: Để báo cáo có tính thuyết phục, bạn cần chụp ảnh màn hình các bước thực hành của mình, lưu vào thư mục `images/` trong thư mục báo cáo này và chèn đường dẫn vào các vị trí dưới đây.*

### 📸 Ảnh 1: Minh chứng cấu hình phần cứng của 2 máy ảo
* **Mô tả nội dung cần chụp:** Chụp giao diện phần cứng của phần mềm ảo hóa (VMware/VirtualBox) hiển thị cấu hình chi tiết (vCPU, vRAM, vDisk dạng mỏng, Network Adapter) của cả VM1 và VM2.
* **Hình ảnh minh chứng:**
  
  ```markdown
  ![Cấu hình phần cứng VM1 và VM2](images/01_hardware_config.png)
  ```
  *(Thay thế file `images/01_hardware_config.png` bằng ảnh chụp thực tế của bạn)*

---

### 📸 Ảnh 2: Minh chứng địa chỉ IP của 2 máy ảo sau khi cấu hình mạng
* **Mô tả nội dung cần chụp:** Chụp màn hình Terminal/Console của cả 2 máy ảo đã khởi động thành công, chạy lệnh kiểm tra IP (`ip a` hoặc `ifconfig`) để hiển thị rõ địa chỉ IP của từng máy.
  * Địa chỉ IP VM1: `...........................`
  * Địa chỉ IP VM2: `...........................`
* **Hình ảnh minh chứng:**

  ```markdown
  ![Địa chỉ IP của VM1 và VM2](images/02_ip_addresses.png)
  ```
  *(Thay thế file `images/02_ip_addresses.png` bằng ảnh chụp thực tế của bạn)*

---

### 📸 Ảnh 3: Minh chứng kết nối mạng thành công (Ping qua lại giữa 2 VM)
* **Mô tả nội dung cần chụp:** Chụp màn hình kết quả chạy lệnh ping giữa 2 máy ảo. 
  * Nửa màn hình bên trái: VM1 ping sang IP của VM2 thành công (không bị drop gói tin).
  * Nửa màn hình bên phải: VM2 ping sang IP của VM1 thành công.
* **Hình ảnh minh chứng:**

  ```markdown
  ![Kết quả Ping qua lại giữa 2 máy ảo](images/03_ping_test.png)
  ```
  *(Thay thế file `images/03_ping_test.png` bằng ảnh chụp thực tế của bạn)*

---

### 📸 Ảnh 4: Minh chứng trạng thái hoạt động của các dịch vụ (Services)
* **Mô tả nội dung cần chụp:** 
  * Trên **VM1**: Chụp màn hình Terminal chạy lệnh kiểm tra dịch vụ Web Server đang chạy (Ví dụ: `systemctl status nginx` hiển thị trạng thái `active (running)`).
  * Trên **VM2**: Chụp màn hình Terminal chạy lệnh kiểm tra dịch vụ Database Server đang chạy (Ví dụ: `systemctl status mysql` hiển thị trạng thái `active (running)`).
* **Hình ảnh minh chứng:**

  ```markdown
  ![Trạng thái các dịch vụ trên VM1 và VM2](images/04_services_status.png)
  ```
  *(Thay thế file `images/04_services_status.png` bằng ảnh chụp thực tế của bạn)*

---

### 📸 Ảnh 5: Minh chứng chạy ứng dụng thành công từ máy Host vật lý
* **Mô tả nội dung cần chụp:** Trên máy vật lý (Host), mở trình duyệt web (Chrome/Edge) và truy cập vào địa chỉ IP của VM1 (ví dụ: `http://<IP_VM1>:<Port>`). Giao diện trang web hiển thị thành công và có lấy dữ liệu chạy thử từ Database (VM2) để chứng minh luồng kết nối thông suốt từ Host -> VM1 -> VM2.
* **Hình ảnh minh chứng:**

  ```markdown
  ![Ứng dụng chạy thành công truy cập từ trình duyệt máy Host](images/05_app_success.png)
  ```
  *(Thay thế file `images/05_app_success.png` bằng ảnh chụp thực tế của bạn)*

---

## 3. Bài học kinh nghiệm & Khó khăn gặp phải

*(Ghi lại những trải nghiệm thực tế của bạn trong quá trình thực hành, ví dụ:)*
* **Lỗi tường lửa (Firewall):** Ban đầu hai máy ảo không ping được cho nhau do tường lửa của hệ điều hành chặn gói tin ICMP. Đã khắc phục bằng cách cấu hình firewall (`ufw allow` hoặc tạm tắt để thử nghiệm).
* **Lỗi quyền truy cập Database:** Database ở VM2 mặc định chỉ nhận kết nối từ `localhost` (127.0.0.1). Đã khắc phục bằng cách cấu hình lại file `mysqld.cnf` (sửa `bind-address = 0.0.0.0`) và cấp quyền cho User Database từ xa.
* **Lưu ý về tài nguyên:** Cần chú ý lượng RAM của máy Host vật lý để tránh bị quá tải (overcommit RAM quá mức) khi bật cùng lúc cả 2 máy ảo kèm theo trình duyệt web.
