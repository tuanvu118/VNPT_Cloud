# BÁO CÁO LÝ THUYẾT - PHẦN 4: CƠ BẢN VỀ LINUX VÀ STORAGE

* **Nội dung:** Tìm hiểu tổng quan về hệ điều hành Linux, phân biệt các Distro phổ biến, giấy phép mã nguồn mở; quy trình cài đặt hệ điều hành Ubuntu và CentOS/Rocky Linux; nắm vững các khái niệm cốt lõi bao gồm Kernel, Directory (FHS), quản lý User/Group, phân quyền tập tin, Filesystem, Service (systemd), câu lệnh terminal cơ bản, giao thức SSH và cấu hình mạng cơ bản trên Linux.
---

## 1. Tổng quan về Hệ điều hành Linux

### a. Khái niệm Linux: Kernel và Operating System (Hệ điều hành)
*   **Linux Kernel (Nhân Linux):**
    *   Do Linus Torvalds khởi xướng vào năm 1991.
    *   Là thành phần cốt lõi trung tâm của hệ thống, đóng vai trò giao tiếp trực tiếp giữa phần cứng (CPU, RAM, ổ đĩa, thiết bị ngoại vi) và phần mềm.
    *   Nhiệm vụ chính: Quản lý bộ nhớ (Memory Management), quản lý tiến trình (Process Management), trình điều khiển thiết bị (Device Drivers), và quản lý hệ thống tệp tin (Filesystem).
    *   Bản thân Kernel không phải là một hệ điều hành hoàn chỉnh, nó cần các công cụ và ứng dụng đi kèm để tạo nên môi trường người dùng hoạt động được.
*   **GNU/Linux Operating System (Hệ điều hành Linux hoàn chỉnh):**
    *   Là sự kết hợp giữa nhân Linux và bộ công cụ hệ thống GNU (compiler, shell, các tiện ích dòng lệnh cơ bản). Vì vậy, tên gọi đầy đủ chính xác của hệ điều hành là **GNU/Linux**.

### b. Phân loại và Phân biệt các Distro Linux phổ biến
Một **Distribution (Distro)** là một hệ điều hành hoàn chỉnh được đóng gói bao gồm Linux Kernel, các thư viện hệ thống GNU, trình quản lý gói (Package Manager), môi trường giao diện (Desktop Environment) và các ứng dụng đi kèm.

Các distro chính được chia thành các nhánh dòng họ (Family Tree) lớn:

| Tiêu chí | Nhánh Debian (Ubuntu/Debian) | Nhánh RedHat (CentOS/Rocky Linux/RHEL) |
| :--- | :--- | :--- |
| **Nhà phát triển chính** | Cộng đồng (Debian) / Canonical (Ubuntu). | Red Hat / IBM (RHEL) / Cộng đồng (Rocky, Alma). |
| **Môi trường mục tiêu** | Phổ biến ở cả Desktop cá nhân và Web Server doanh nghiệp. | Chuyên dụng cho doanh nghiệp, hệ thống Enterprise lớn, Data Center. |
| **Định dạng gói cài đặt** | `.deb` | `.rpm` |
| **Trình quản lý gói cơ bản** | `dpkg` (bậc thấp), `apt-get` / `apt` (bậc cao). | `rpm` (bậc thấp), `yum` / `dnf` (bậc cao). |
| **Tính cập nhật ổn định** | Ubuntu LTS cập nhật mỗi 2 năm, hỗ trợ 5 năm. Debian cực kỳ bảo thủ và ổn định. | RHEL/Rocky có chu kỳ hỗ trợ rất dài (10 năm), tập trung tối đa vào độ ổn định doanh nghiệp. |
| **Công cụ cấu hình mạng** | Netplan (đối với Ubuntu Server phiên bản mới). | NetworkManager / `nmcli` / `nmtui`. |

### c. Các loại giấy phép sử dụng mã nguồn mở phổ biến (Open Source Licenses)
Giấy phép mã nguồn mở quy định quyền hạn và trách nhiệm của người sử dụng, sửa đổi và phân phối mã nguồn.

*   **GNU GPL (General Public License - GPLv2/GPLv3):**
    *   *Tính chất:* Mang tính ràng buộc mạnh (Copyleft).
    *   *Quy định:* Cho phép người dùng chạy, nghiên cứu, chia sẻ và sửa đổi phần mềm tự do. Tuy nhiên, bất kỳ phần mềm nào sử dụng hoặc chỉnh sửa mã nguồn có giấy phép GPL khi phân phối ra ngoài **bắt buộc** cũng phải mở mã nguồn dưới giấy phép GPL (tính kế thừa). Nhân Linux sử dụng giấy phép GPLv2.
*   **MIT License:**
    *   *Tính chất:* Rất cởi mở và tự do (Permissive).
    *   *Quy định:* Cho phép làm bất kỳ điều gì với mã nguồn (sử dụng, sửa đổi, phân phối, thương mại hóa, đóng gói thành mã nguồn đóng) miễn là đính kèm thông báo bản quyền và giấy phép MIT gốc trong sản phẩm phân phối.
*   **Apache License (Apache 2.0):**
    *   *Tính chất:* Tự do, tương tự MIT nhưng chặt chẽ hơn về mặt pháp lý quyền sở hữu trí tuệ.
    *   *Quy định:* Cho phép sửa đổi và thương mại hóa mã nguồn đóng. Ngoài việc yêu cầu giữ thông báo bản quyền, Apache 2.0 còn bổ sung các điều khoản rõ ràng về việc cấp quyền sử dụng bằng sáng chế (patent rights) và yêu cầu ghi rõ các file nào đã bị thay đổi so với bản gốc.

---

## 2. Quy trình cài đặt các Hệ điều hành Linux phổ biến

Cài đặt Linux trên môi trường ảo hóa (như VMware, VirtualBox, KVM) tuân theo các quy trình tiêu chuẩn dưới đây:

### a. Quy trình cài đặt Ubuntu Server (ví dụ phiên bản 22.04 / 24.04 LTS)
1.  **Chuẩn bị:** Tải file hình ảnh đĩa `.iso` của Ubuntu Server từ trang chủ. Khởi tạo VM với cấu hình phần cứng phù hợp (CPU, RAM, Disk).
2.  **Khởi động:** Gắn file ISO vào ổ đĩa ảo của VM và bật nguồn để khởi động vào bộ cài đặt GRUB.
3.  **Lựa chọn ngôn ngữ và bàn phím:** Chọn ngôn ngữ cài đặt (thường là English) và kiểu bố cục bàn phím (US).
4.  **Cấu hình mạng (Network Connections):** Trình cài đặt tự động nhận IP qua DHCP. Ta có thể chỉnh sửa thủ công để cấu hình IP tĩnh (Static IP), Subnet, Gateway và DNS Server.
5.  **Cấu hình Proxy và Mirror:** Thiết lập Proxy nếu cần kết nối ra ngoài qua proxy, chọn máy chủ lưu trữ gói phần mềm (Archive Mirror) mặc định hoặc máy chủ gần nhất để tăng tốc độ tải.
6.  **Cấu hình lưu trữ (Guided Storage Configuration):**
    *   Chọn đĩa cài đặt hệ điều hành.
    *   Có thể chọn tự động phân vùng hoặc tùy chỉnh phân vùng thủ công (Custom Storage Layout).
    *   Hệ điều hành khuyến nghị tích hợp LVM (Logical Volume Manager) để dễ dàng mở rộng dung lượng đĩa sau này.
7.  **Thiết lập Profile thông tin:** Đặt tên máy chủ (Hostname), tên người dùng quản trị (Username) và mật khẩu (Password).
8.  **Cài đặt SSH (SSH Setup):** Chọn tích hợp cài đặt **OpenSSH Server** để cho phép quản trị và điều khiển máy ảo từ xa ngay sau khi hoàn tất.
9.  **Cài đặt các dịch vụ bổ sung:** Lựa chọn cài thêm các gói phần mềm đóng gói sẵn (Snap packages) nếu cần (Docker, microk8s,...), hoặc bỏ qua để cài đặt thủ công sau.
10. **Tiến trình cài đặt và Khởi động lại:** Trình cài đặt tải và ghi dữ liệu lên ổ đĩa. Khi hoàn tất, hệ thống yêu cầu ngắt file ISO cài đặt và nhấn **Reboot** để khởi động vào hệ điều hành chính thức.

### b. Quy trình cài đặt CentOS / Rocky Linux
1.  **Chuẩn bị:** Tải file `.iso` cài đặt (ví dụ Rocky Linux Minimal hoặc DVD). Gắn ISO vào máy ảo và khởi động.
2.  **Khởi động bộ cài Anaconda:** Chọn "Install Rocky Linux". Trình cài đặt đồ họa Anaconda GUI/TUI sẽ được tải lên.
3.  **Lựa chọn ngôn ngữ:** Chọn ngôn ngữ hiển thị trong suốt quá trình cài đặt.
4.  **Bảng điều khiển chính (Installation Summary):** Cần cấu hình các mục đánh dấu cảnh báo màu vàng trước khi bắt đầu cài đặt:
    *   **Time & Date (Múi giờ):** Chọn múi giờ địa phương (ví dụ Asia/Ho_Chi_Minh).
    *   **Software Selection (Lựa chọn phần mềm):** Đối với máy chủ, chọn chế độ **Minimal Install** (cài đặt tối giản, không giao diện GUI) để tiết kiệm tài nguyên hệ thống và tăng tính bảo mật.
    *   **Installation Destination (Phân vùng ổ đĩa):** Chọn ổ đĩa cài đặt. Có thể chọn tự động phân chia phân vùng (Automatic) hoặc cấu hình phân vùng thủ công (Custom) với các phân vùng cơ bản `/boot`, `/`, `/boot/efi` (nếu dùng UEFI) và vùng nhớ ảo `swap`.
    *   **Network & Host Name:** Bật card mạng lên (Ethernet ON), cấu hình IP tĩnh và thiết lập Hostname cho máy chủ.
5.  **Thiết lập tài khoản người dùng:** 
    *   Thiết lập mật khẩu cho tài khoản quản trị tối cao **Root**.
    *   Tạo thêm một tài khoản người dùng thường và phân quyền quản trị (Make this user administrator) thông qua nhóm `wheel` (sử dụng lệnh `sudo`).
6.  **Thực hiện cài đặt:** Nhấp chọn **Begin Installation** để tiến hành cài đặt.
7.  **Hoàn thành:** Sau khi hệ thống sao chép xong các file, nhấn **Reboot System** và ngắt đĩa ISO để hoàn tất.

---

## 3. Các khái niệm cốt lõi trong Linux

### a. Kernel (Nhân)
*   Là lõi của hệ điều hành, chạy ở chế độ đặc quyền nhất (Kernel Space).
*   Chịu trách nhiệm trực tiếp trong việc quản lý tài nguyên vật lý và chia sẻ chúng cho các chương trình người dùng (chạy ở User Space).
*   Các chức năng chính bao gồm:
    *   *Quản lý thiết bị:* Giao tiếp với phần cứng thông qua các Device Driver tích hợp hoặc nạp dưới dạng Module (`.ko`).
    *   *Quản lý bộ nhớ:* Cấp phát RAM cho tiến trình, quản lý bộ nhớ ảo (Virtual Memory) và dọn dẹp giải phóng RAM.
    *   *Quản lý tiến trình:* Lập lịch điều phối (Scheduler) để CPU xử lý luân phiên các luồng công việc của hệ thống.
    *   *Lời gọi hệ thống (System Calls):* Cung cấp giao diện lập trình ứng dụng (API) cho phép ứng dụng từ User Space yêu cầu dịch vụ từ Kernel Space (ví dụ đọc/ghi file, kết nối mạng).

### b. Directory (Thư mục) & Cấu trúc cây thư mục tiêu chuẩn FHS
Hệ thống tập tin của Linux được tổ chức theo cấu trúc hình cây phân cấp, bắt đầu từ gốc cao nhất là thư mục root `/`. Tiêu chuẩn FHS (Filesystem Hierarchy Standard) quy định chức năng của từng thư mục:

| Thư mục | Chức năng chi tiết |
| :--- | :--- |
| `/` | Thư mục gốc (Root directory), điểm bắt đầu của toàn bộ cây thư mục. |
| `/bin` | Chứa các câu lệnh thực thi cơ bản cần thiết cho tất cả người dùng (ls, cp, mv, ping, ...). |
| `/sbin` | Chứa các lệnh hệ thống thiết yếu dành cho quản trị viên Root (iptables, fdisk, reboot, ...). |
| `/etc` | Chứa toàn bộ các file cấu hình của hệ thống và các ứng dụng dịch vụ (ví dụ: `/etc/ssh/sshd_config`, `/etc/fstab`). |
| `/var` | Chứa dữ liệu biến đổi liên tục trong quá trình vận hành hệ thống (các file log hệ thống `/var/log`, dữ liệu hàng đợi mail, database). |
| `/home` | Thư mục cá nhân của người dùng thường (ví dụ: `/home/tuanvu`). |
| `/root` | Thư mục cá nhân riêng của tài khoản quản trị tối cao Root. |
| `/usr` | Chứa các chương trình, tài liệu hướng dẫn và mã nguồn của người dùng. Trong đó `/usr/bin` chứa các lệnh cài thêm sau này. |
| `/opt` | Thư mục cài đặt các phần mềm của bên thứ ba (Add-on application software packages). |
| `/tmp` | Thư mục chứa các tệp tin tạm thời, thường bị xóa sạch khi hệ thống khởi động lại. |
| `/boot` | Chứa các tệp tin cần thiết cho quá trình khởi động hệ thống như nhân Linux (vmlinuz), cấu hình GRUB bootloader. |
| `/dev` | Chứa các tệp tin đại diện cho các thiết bị phần cứng vật lý (ổ đĩa `/dev/sda`, chuột, bàn phím). |
| `/proc` | Thư mục ảo (Virtual filesystem) chứa thông tin về trạng thái nhân Kernel và các tiến trình đang chạy dưới dạng file văn bản. |
| `/sys` | Thư mục ảo tương tự `/proc`, dùng để xuất thông tin và cấu hình các thiết bị phần cứng nối với nhân Kernel. |

### c. User & Group (Người dùng và Nhóm người dùng)
Linux là hệ điều hành đa nhiệm, đa người dùng. Hệ thống nhận dạng và quản lý phân quyền dựa trên định danh số: **UID** (User ID) và **GID** (Group ID).

*   **Tài khoản người dùng (User):**
    *   *Root User (UID = 0):* Quản trị tối cao, có toàn quyền can thiệp hệ thống mà không bị giới hạn.
    *   *System User (UID = 1 - 999):* Tài khoản không có thư mục home và shell đăng nhập, dùng để chạy các dịch vụ ngầm (ví dụ user `nginx`, `postgres`, `ssh`).
    *   *Normal User (UID >= 1000):* Người dùng thông thường do quản trị tạo ra để làm việc hàng ngày.
*   **Nhóm người dùng (Group):**
    *   Tập hợp nhiều tài khoản người dùng để dễ dàng quản lý phân quyền truy cập tài nguyên chung.
*   **Các file cấu hình hệ thống cốt lõi:**
    *   `/etc/passwd`: Lưu trữ thông tin tài khoản người dùng (Username, UID, GID, thư mục Home, Shell đăng nhập).
    *   `/etc/shadow`: Lưu trữ mật khẩu người dùng đã được mã hóa kèm chính sách thời hạn mật khẩu (chỉ có quyền root mới đọc được).
    *   `/etc/group`: Lưu trữ danh sách nhóm người dùng và các thành viên thuộc nhóm.
*   **Các lệnh quản trị cơ bản:**
    *   `useradd -m <username>`: Tạo người dùng mới và thư mục home.
    *   `groupadd <groupname>`: Tạo nhóm mới.
    *   `passwd <username>`: Đổi mật khẩu cho người dùng.
    *   `usermod -aG <group> <user>`: Thêm người dùng vào một nhóm bổ sung (ví dụ nhóm `sudo` hoặc `wheel` để cấp quyền chạy sudo).
    *   `userdel -r <username>`: Xóa người dùng và xóa sạch thư mục home đi kèm.

### d. Phân quyền trong Linux (File & Directory Permissions)
Khi chạy lệnh `ls -l`, mỗi file hoặc thư mục đều hiển thị chuỗi ký tự phân quyền dạng: `drwxr-xr--`.

#### Cấu trúc chuỗi phân quyền:
*   Kí tự đầu tiên: loại file (`-` là file thường, `d` là thư mục, `l` là liên kết mềm link).
*   9 kí tự tiếp theo chia làm 3 nhóm (mỗi nhóm 3 kí tự tương ứng `rwx`):
    1.  **Owner/User (u):** Quyền của chủ sở hữu file.
    2.  **Group (g):** Quyền của các thành viên trong nhóm sở hữu file.
    3.  **Others (o):** Quyền của mọi người dùng khác trên hệ thống.

#### Quyền truy cập:
*   **Read (r):** Đọc nội dung file (giá trị số = 4). Với thư mục, cho phép liệt kê danh sách file bên trong (`ls`).
*   **Write (w):** Chỉnh sửa nội dung file (giá trị số = 2). Với thư mục, cho phép tạo, xóa hoặc đổi tên file bên trong.
*   **Execute (x):** Thực thi file như một chương trình/script (giá trị số = 1). Với thư mục, cho phép truy cập đi vào trong thư mục đó (`cd`).

#### Bảng quy đổi giá trị phân quyền dạng Octal (Số bát phân):
Cộng các giá trị quyền lại với nhau:
*   `rwx` = 4 + 2 + 1 = 7 (Toàn quyền)
*   `rw-` = 4 + 2 + 0 = 6 (Đọc và viết)
*   `r-x` = 4 + 0 + 1 = 5 (Đọc và thực thi)
*   `r--` = 4 + 0 + 0 = 4 (Chỉ đọc)

#### Lệnh thay đổi phân quyền:
*   `chmod`: Thay đổi quyền truy cập của file/thư mục.
    *   Ví dụ dạng ký tự: `chmod u+x,g-w file.txt` (Thêm quyền thực thi cho Owner, bớt quyền ghi của Group).
    *   Ví dụ dạng số: `chmod 755 script.sh` (Owner có quyền rwx, Group và Others có quyền r-x).
*   `chown`: Thay đổi chủ sở hữu (Owner) và nhóm sở hữu (Group) của file/thư mục.
    *   Ví dụ: `chown tuanvu:developers file.txt` (Đổi chủ sở hữu thành user `tuanvu`, nhóm sở hữu thành `developers`).

### e. Filesystem (Hệ thống tập tin)
Hệ thống tập tin xác định cách thức dữ liệu được tổ chức, lưu trữ và đọc ghi trên phân vùng đĩa.

*   **So sánh ext4 và xfs:**
    *   **ext4 (Fourth Extended Filesystem):** 
        *   Hệ thống tệp mặc định lâu đời của Debian/Ubuntu.
        *   Hỗ trợ kích thước file đơn lẻ lên đến 16 TB và phân vùng lên tới 1 EB.
        *   Rất tin cậy, tối ưu tốt cho các ổ đĩa dung lượng nhỏ đến trung bình và có khả năng thu nhỏ kích thước phân vùng (shrink) khi cần thiết.
    *   **xfs:**
        *   Hệ thống tệp mặc định của RedHat/CentOS/Rocky Linux.
        *   Tối ưu hóa cực mạnh cho việc xử lý song song các tác vụ I/O (đọc/ghi) trên hệ thống lưu trữ quy mô lớn, phân vùng cực lớn (lên tới 8 EB).
        *   Có hiệu năng rất cao đối với các tệp tin dung lượng lớn, tuy nhiên **không hỗ trợ thu nhỏ phân vùng** sau khi đã định dạng (chỉ cho phép mở rộng tăng dung lượng).
*   **Khái niệm Mount Point (Điểm gắn kết):**
    *   Khác với Windows dùng các ổ đĩa độc lập (C:, D:, E:), Linux quản lý tất cả dưới một cây thư mục duy nhất `/`.
    *   **Mounting** là quá trình liên kết một phân vùng ổ đĩa vật lý (ví dụ `/dev/sdb1`) vào một thư mục rỗng cụ thể trên cây thư mục (ví dụ `/mnt/data`). Thư mục này gọi là **Mount Point**. Khi ghi dữ liệu vào `/mnt/data`, thực chất dữ liệu đang được lưu trên phân vùng `/dev/sdb1`.
*   **Tệp tin `/etc/fstab`:**
    *   Là file cấu hình tĩnh chứa thông tin các ổ đĩa và phân vùng được hệ thống tự động mount mỗi khi khởi động máy. Nếu cấu hình sai file này, hệ điều hành có thể bị lỗi boot treo hệ thống.

### f. Service (systemd)
`systemd` là hệ thống khởi tạo (Init System) và quản lý dịch vụ hệ thống mặc định trên hầu hết các distro Linux hiện đại.

*   Các tiến trình con, dịch vụ được định nghĩa dưới dạng các **Unit** (thường có phần mở rộng `.service`).
*   **systemctl** là công cụ dòng lệnh chính để kiểm soát trạng thái và quản lý dịch vụ:
    *   `systemctl start <service>`: Khởi chạy dịch vụ ngay lập tức.
    *   `systemctl stop <service>`: Dừng dịch vụ đang chạy.
    *   `systemctl restart <service>`: Khởi động lại dịch vụ.
    *   `systemctl status <service>`: Kiểm tra trạng thái hoạt động chi tiết cùng các dòng log mới nhất của dịch vụ.
    *   `systemctl enable <service>`: Thiết lập dịch vụ tự động khởi động cùng hệ thống.
    *   `systemctl disable <service>`: Hủy tự động khởi động dịch vụ cùng hệ thống.

### g. Terminal & Command Line cơ bản
Bảng tổng hợp các câu lệnh thiết yếu để làm việc với hệ thống qua dòng lệnh:

| Nhóm lệnh | Lệnh | Chức năng chi tiết |
| :--- | :--- | :--- |
| **Thao tác thư mục** | `pwd` | Hiển thị đường dẫn thư mục hiện tại đang làm việc (Print Working Directory). |
| | `ls -la` | Liệt kê tất cả file/thư mục (bao gồm cả file ẩn bắt đầu bằng dấu `.`) kèm thông tin phân quyền chi tiết. |
| | `cd <path>` | Di chuyển chuyển đổi thư mục làm việc hiện hành. |
| | `mkdir -p <dir>` | Tạo thư mục mới (tham số `-p` cho phép tạo tự động thư mục cha nếu chưa có). |
| | `rmdir <dir>` | Xóa thư mục rỗng. |
| **Thao tác file** | `touch <file>` | Tạo một file trống mới hoặc cập nhật lại mốc thời gian của file hiện tại. |
| | `cp -r <src> <dest>` | Sao chép file hoặc thư mục (tham số `-r` để sao chép đệ quy thư mục). |
| | `mv <src> <dest>` | Di chuyển file/thư mục hoặc dùng để đổi tên file/thư mục. |
| | `rm -rf <path>` | Xóa file hoặc thư mục vĩnh viễn (tham số `-r` xóa đệ quy, `-f` ép buộc xóa không hỏi lại - **Rất nguy hiểm**). |
| **Xem nội dung file** | `cat <file>` | Đọc và hiển thị toàn bộ nội dung file ra màn hình Terminal. |
| | `less <file>` | Đọc nội dung file theo từng trang, cho phép cuộn lên xuống dễ dàng. |
| | `head -n <N> <file>`| Đọc `<N>` dòng đầu tiên của file. |
| | `tail -f <file>` | Xem nội dung các dòng cuối cùng của file và giữ kết nối để cập nhật trực tiếp thời gian thực khi file có dòng mới (thường dùng để xem log). |
| **Soạn thảo văn bản** | `vim` | Trình soạn thảo văn bản mạnh mẽ chạy trên Terminal. Có 2 chế độ chính: **Command mode** (dùng để gõ phím tắt điều hướng/thao tác) và **Insert mode** (nhấn phím `i` để bắt đầu gõ văn bản). Nhấn `Esc` rồi gõ `:wq` để lưu và thoát, `:q!` để thoát không lưu. |

### h. SSH (Secure Shell)
SSH là một giao thức mạng mật mã được sử dụng để thiết lập kết nối điều khiển máy chủ từ xa một cách an toàn qua mạng không bảo mật.

*   Hoạt động mặc định ở cổng **22 / TCP**.
*   **Cơ chế xác thực đăng nhập:**
    1.  *Xác thực bằng Password:* Người dùng nhập tài khoản và mật khẩu hệ thống. Mật khẩu được mã hóa trên đường truyền. Dễ bị tấn công vét cạn (Brute-force) nếu đặt mật khẩu yếu.
    2.  *Xác thực bằng SSH Key (Khuyến nghị bảo mật):* Sử dụng cặp khóa mã hóa bất đối xứng:
        *   **Khóa riêng tư (Private Key):** Lưu trữ bí mật ở máy Client của người dùng. Cấm chia sẻ cho bất kỳ ai.
        *   **Khóa công khai (Public Key):** Được sao chép và lưu trên máy chủ cần kết nối (thường ghi vào tệp `/home/user/.ssh/authorized_keys`).
        *   Khi kết nối, máy chủ gửi một thử thách được mã hóa bằng Public Key, Client sử dụng Private Key tương ứng để giải mã và chứng minh danh tính mà không cần gửi mật khẩu qua mạng.
*   **Cấu hình dịch vụ SSH Daemon (`/etc/ssh/sshd_config`):**
    *   Cho phép thay đổi cổng kết nối (ví dụ đổi cổng từ 22 sang cổng khác để tránh bị quét).
    *   Cấu hình `PermitRootLogin no` để cấm tài khoản Root đăng nhập trực tiếp từ xa qua SSH (bắt buộc đăng nhập bằng user thường rồi mới dùng sudo).
    *   Cấu hình `PasswordAuthentication no` để bắt buộc đăng nhập bằng SSH Key, nâng cao bảo mật tối đa.

### i. Network (Mạng cơ bản trên Linux)
Các công cụ và lệnh thiết lập/kiểm tra cấu hình mạng.

*   **Cách thức cấu hình mạng trên các Distro:**
    *   **Ubuntu Server (Netplan):** Sử dụng các file cấu hình định dạng YAML nằm trong thư mục `/etc/netplan/` (ví dụ `01-netcfg.yaml`). Sau khi chỉnh sửa, áp dụng cấu hình bằng lệnh `sudo netplan apply`.
    *   **CentOS / Rocky Linux (NetworkManager):** Quản lý qua dịch vụ NetworkManager. Sử dụng tiện ích dòng lệnh giao diện xanh `nmtui` hoặc dòng lệnh `nmcli`.
*   **Các câu lệnh kiểm tra và khắc phục sự cố mạng:**
    *   `ip addr` hoặc `ip a`: Hiển thị chi tiết địa chỉ IP và trạng thái của các card mạng đang có trên hệ thống (thay thế cho lệnh cũ `ifconfig`).
    *   `ip route` hoặc `ip r`: Xem bảng định tuyến hiện tại của hệ thống để biết Gateway mặc định (Default Gateway).
    *   `ping <IP/Domain>`: Gửi các gói tin ICMP Echo Request để kiểm tra độ trễ và khả năng kết nối thông suốt giữa hai thiết bị mạng.
    *   `nslookup <domain>` hoặc `dig <domain>`: Tra cứu phân giải tên miền thành địa chỉ IP thông qua các máy chủ DNS Server.
    *   `ss -tunlp` hoặc `netstat -tunlp`: Liệt kê tất cả các cổng mạng (Port) đang ở trạng thái lắng nghe (LISTEN) kèm thông tin tiến trình dịch vụ đang chiếm giữ cổng đó.
