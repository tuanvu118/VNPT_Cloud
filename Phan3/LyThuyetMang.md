# BÁO CÁO LÝ THUYẾT - PHẦN 3: KIẾN THỨC MẠNG MÁY TÍNH CƠ BẢN VÀ NÂNG CAO

* **Nội dung:** Tìm hiểu chi tiết về các mô hình mạng (OSI, TCP/IP), các khái niệm cơ bản (MAC, IP, Port, Protocol, Packet, TCP/UDP), các loại kết nối vật lý (Quang, Đồng, SFP, NIC), các kỹ thuật Switching/VLAN, Routing/NAT và cân bằng tải (Load Balancer).
---

## 1. Mô hình Mạng, Định danh và Giao thức truyền dẫn

### a. Mô hình OSI và Mô hình TCP/IP
Đây là hai mô hình tham chiếu tiêu chuẩn giúp định hình cách thức các thiết bị truyền thông tin qua mạng.

#### Mô hình OSI (Open Systems Interconnection - 7 Tầng)
Do tổ chức ISO phát triển, chia quá trình truyền thông mạng thành 7 tầng logic:
1.  **Tầng 7 - Application (Ứng dụng):** Giao diện tương tác trực tiếp với người dùng và các phần mềm (HTTP, HTTPS, FTP, DNS, SMTP).
2.  **Tầng 6 - Presentation (Trình diễn):** Mã hóa, giải mã dữ liệu, định dạng file (ASCII, JPEG, MP3, nén/mã hóa dữ liệu).
3.  **Tầng 5 - Session (Phiên):** Thiết lập, quản lý và kết thúc các phiên hội thoại giữa các ứng dụng trên hai thiết bị.
4.  **Tầng 4 - Transport (Vận chuyển):** Đảm bảo truyền dẫn dữ liệu tin cậy hoặc nhanh chóng giữa hai tiến trình (TCP, UDP). Thực hiện phân đoạn dữ liệu (Segmentation).
5.  **Tầng 3 - Network (Mạng):** Định tuyến gói tin từ nguồn đến đích qua nhiều mạng khác nhau dựa trên IP (IP, ICMP, OSPF, Router).
6.  **Tầng 2 - Data Link (Liên kết dữ liệu):** Truyền tải dữ liệu không lỗi giữa hai node kết nối vật lý trực tiếp với nhau dựa trên địa chỉ MAC (Ethernet, Switch, ARP).
7.  **Tầng 1 - Physical (Vật lý):** Chuyển đổi dữ liệu thành các tín hiệu vật lý (điện, quang, sóng) để truyền qua dây cáp/không khí (Cáp đồng, cáp quang, Hub, Repeater).

#### Mô hình TCP/IP (4 Tầng)
Là mô hình thực tế cấu thành nên Internet ngày nay, gộp một số tầng của OSI lại:
1.  **Tầng Application (Ứng dụng):** Tương đương tầng 5, 6, 7 của OSI.
2.  **Tầng Transport (Vận chuyển):** Tương đương tầng 4 của OSI.
3.  **Tầng Internet (Mạng):** Tương đương tầng 3 của OSI.
4.  **Tầng Network Access / Link (Truy cập mạng):** Tương đương tầng 1, 2 của OSI.

---

### b. Các khái niệm định danh & đơn vị truyền dẫn

#### MAC Address (Địa chỉ MAC)
*   **Định nghĩa:** Là địa chỉ vật lý độc nhất được nhà sản xuất ghi trực tiếp lên mỗi card mạng (NIC).
*   **Độ dài:** 48-bit (6 bytes), hiển thị ở dạng Hexadecimal (Ví dụ: `00:1A:2B:3C:4D:5E`).
*   **Phạm vi hoạt động:** Hoạt động tại tầng Data Link (Layer 2) để giao tiếp nội bộ trong cùng một phân đoạn mạng LAN.

#### IP Address (Địa chỉ IP)
*   **Định nghĩa:** Là địa chỉ logic được gán cho mỗi thiết bị khi tham gia vào mạng nhằm định vị thiết bị trên quy mô toàn cầu. Hoạt động tại tầng Network (Layer 3).
*   **Phân loại:**
    *   **IPv4:** 32-bit, chia thành 4 octet viết dưới dạng thập phân cách nhau bằng dấu chấm (Ví dụ: `192.168.1.1`). Cung cấp khoảng 4.3 tỷ địa chỉ.
    *   **IPv6:** 128-bit, viết dưới dạng Hexadecimal cách nhau bởi dấu hai chấm (Ví dụ: `2001:0db8:85a3:0000:0000:8a2e:0370:7334`). Ra đời để giải quyết tình trạng cạn kiệt địa chỉ IPv4.

#### Port (Cổng)
*   **Định nghĩa:** Là một số nguyên 16-bit logic (từ 0 đến 65535) giúp hệ điều hành phân biệt luồng dữ liệu của các ứng dụng/dịch vụ khác nhau cùng chạy trên một thiết bị. Hoạt động tại tầng Transport (Layer 4).
*   **Phân vùng:**
    *   *Well-known Ports (0 - 1023):* Dành cho các dịch vụ cốt lõi (HTTP: 80, HTTPS: 443, SSH: 22, DNS: 53, MySQL: 3306).
    *   *Registered Ports (1024 - 49151):* Dành cho ứng dụng của người dùng hoặc hãng thứ ba.
    *   *Dynamic/Private Ports (49152 - 65535):* Do hệ điều hành tự động cấp phát ngẫu nhiên cho tiến trình Client khi tạo kết nối ra ngoài.

#### Protocol (Giao thức)
*   **Định nghĩa:** Là một bộ các quy tắc, quy chuẩn được chuẩn hóa để định dạng, truyền tải dữ liệu sao cho các thiết bị từ các nhà sản xuất khác nhau có thể hiểu và giao tiếp được với nhau (Ví dụ: HTTP, FTP, TCP, IP).

#### Packet (Gói tin) và Quá trình Đóng gói dữ liệu (Encapsulation)
Quá trình truyền dữ liệu từ tầng trên xuống tầng dưới sẽ được đóng gói bằng cách thêm các Header chứa thông tin điều khiển tương ứng. Đơn vị dữ liệu tại mỗi tầng có tên gọi khác nhau:
1.  **Data (Tầng Application):** Dữ liệu thô của ứng dụng.
2.  **Segment (Tầng Transport):** Data + Port Header (TCP/UDP).
3.  **Packet (Tầng Network):** Segment + IP Header (IP nguồn/đích).
4.  **Frame (Tầng Data Link):** Packet + MAC Header & Trailer (MAC nguồn/đích, mã kiểm tra lỗi CRC).
5.  **Bits (Tầng Physical):** Frame được chuyển đổi thành chuỗi nhị phân 0 và 1 truyền qua dây cáp.

---

### c. So sánh chi tiết TCP và UDP

| Tiêu chí so sánh | TCP (Transmission Control Protocol) | UDP (User Datagram Protocol) |
| :--- | :--- | :--- |
| **Cách thức kết nối** | **Connection-oriented:** Phải thiết lập kết nối trước khi truyền dữ liệu thông qua cơ chế **Bắt tay 3 bước (3-way handshake)**. | **Connectionless:** Không cần thiết lập kết nối, dữ liệu được gửi đi trực tiếp mà không cần báo trước. |
| **Độ tin cậy** | **Rất cao:** Đảm bảo dữ liệu gửi đi không bị mất mát, trùng lặp và được sắp xếp đúng thứ tự (sử dụng ACK và Seq number). | **Không đảm bảo:** Không kiểm tra dữ liệu có đến đích hay không, không gửi lại gói tin bị mất. |
| **Kiểm soát luồng & tắc nghẽn** | Có cơ chế điều chỉnh tốc độ gửi dữ liệu để tránh làm quá tải thiết bị nhận hoặc đường truyền. | Không có. Gửi dữ liệu liên tục với tốc độ tối đa có thể. |
| **Tốc độ truyền** | Chậm hơn (do phải mất thời gian xác thực gói tin và kiểm soát lỗi). | Rất nhanh (do không tốn tài nguyên quản lý kết nối). |
| **Ứng dụng tiêu biểu** | Web (HTTP/HTTPS), Email (SMTP/IMAP), Truyền file (FTP), Quản trị từ xa (SSH). | Truyền phát video trực tuyến (Streaming), Gọi điện VoIP, DNS tra cứu tên miền, Game online. |

---

## 2. Kết nối vật lý và Thiết bị ngoại vi mạng

### a. Kết nối Đồng và Kết nối Quang

#### Kết nối Đồng (Copper Cable)
*   **Cấu tạo:** Sử dụng dây cáp làm bằng đồng (thường là cáp đôi xoắn - Twisted Pair như Cat5e, Cat6). Truyền tín hiệu bằng dòng điện.
*   **Đặc điểm:**
    *   *Khoảng cách truyền:* Bị giới hạn nghiêm trọng (Tối đa khoảng 100m cho một phân đoạn mạng, xa hơn tín hiệu sẽ bị suy hao).
    *   *Nhiễu điện từ:* Dễ bị ảnh hưởng bởi từ trường từ các thiết bị điện xung quanh.
    *   *Chi phí:* Rất rẻ, dễ lắp đặt, phổ biến trong mạng LAN văn phòng.

#### Kết nối Quang (Fiber Optic Cable)
*   **Cấu tạo:** Sử dụng sợi quang làm từ thủy tinh hoặc nhựa siêu tinh khiết. Truyền dữ liệu dưới dạng xung ánh sáng.
*   **Phân loại:**
    *   *Single-Mode (Đơn mốt):* Đường kính lõi rất nhỏ, chỉ cho phép một tia sáng truyền qua. Sử dụng nguồn phát Laser, khoảng cách truyền rất xa (hàng chục đến hàng trăm kilomet), băng thông cực lớn.
    *   *Multi-Mode (Đa mốt):* Đường kính lõi lớn hơn, cho phép nhiều tia sáng truyền đi cùng lúc với các góc phản xạ khác nhau. Sử dụng nguồn phát LED, truyền cự ly ngắn (thường dưới 2km), thích hợp làm cáp backbone kết nối giữa các tủ Rack trong cùng một Data Center.
*   **Đặc điểm:** Không bị ảnh hưởng bởi nhiễu điện từ, tính bảo mật cao, tốc độ truyền siêu tốc.

---

### b. Module SFP và Card mạng NIC

#### SFP (Small Form-factor Pluggable - Module quang)
*   **Định nghĩa:** Là thiết bị thu phát nhỏ gọn, có khả năng tháo lắp nóng (Hot-swappable), dùng để cắm vào các cổng SFP của thiết bị mạng (Switch, Router).
*   **Vai trò:** Đóng vai trò là cầu nối chuyển đổi tín hiệu điện (từ bảng mạch của Switch) thành tín hiệu quang (để truyền qua cáp quang) và ngược lại.
*   **Phân loại:** SFP (1 Gbps), SFP+ (10 Gbps), QSFP (40 Gbps, QSFP28 (100 Gbps).

#### NIC (Network Interface Card - Card mạng)
*   **Định nghĩa:** Là bo mạch phần cứng cắm trên máy tính hoặc máy chủ nhằm cung cấp cổng kết nối vật lý với mạng (Cổng RJ45 cho cáp đồng hoặc cổng quang).
*   **Trong môi trường ảo hóa:** 
    *   **pNIC (Physical NIC):** Card mạng vật lý cắm trên máy chủ host (ví dụ card Dell/HP 10Gbps).
    *   **vNIC (Virtual NIC):** Card mạng ảo được Hypervisor giả lập bằng phần mềm để gán cho các máy ảo kết nối với switch ảo.

---

## 3. Khái niệm cơ bản về Switching và VLAN

### a. Switching (Chuyển mạch lớp 2)
*   **Nguyên lý hoạt động:** Thiết bị Switch hoạt động tại tầng Data Link (Layer 2). Nó đọc địa chỉ MAC đích của các Frame đi vào cổng của nó và tra cứu trong **Bảng địa chỉ MAC (MAC Address Table)** để đưa ra quyết định chuyển tiếp (Forward) Frame đó ra duy nhất cổng có thiết bị đích kết nối, thay vì gửi quảng bá ra toàn bộ các cổng như thiết bị Hub cũ.
*   **Quá trình học địa chỉ MAC (MAC Learning):** Khi một Frame đi vào một cổng, Switch ghi lại địa chỉ MAC nguồn của thiết bị gửi và gán với số hiệu cổng đó vào bảng MAC.

---

### b. VLAN (Virtual Local Area Network - Mạng LAN ảo)
*   **Khái niệm:** VLAN là công nghệ cho phép phân chia logic một Switch vật lý duy nhất thành nhiều phân đoạn mạng LAN ảo độc lập. Các thiết bị thuộc các VLAN khác nhau sẽ không thể liên lạc trực tiếp được với nhau ở Layer 2 (giống như đang nằm trên các Switch vật lý khác nhau).
*   **Mục đích:**
    *   *Giảm miền quảng bá (Broadcast Domain):* Hạn chế lưu lượng gói tin quảng bá đi khắp mạng gây nghẽn băng thông.
    *   *Tăng tính bảo mật:* Cách ly lưu lượng dữ liệu giữa các phòng ban (Ví dụ: Phòng Kế toán không thể sniff gói tin của phòng Nhân sự).
    *   *Quản lý linh hoạt:* Chuyển đổi phòng ban cho nhân sự dễ dàng qua cấu hình phần mềm mà không cần đi lại dây mạng vật lý.
*   **Các loại cổng cổng kết nối VLAN:**
    *   **Access Port (Cổng truy cập):** Chỉ thuộc về một VLAN duy nhất. Thường kết nối tới thiết bị đầu cuối như PC, máy in. Lưu lượng đi ra khỏi cổng Access sẽ bị gỡ bỏ nhãn VLAN (Untagged).
    *   **Trunk Port (Cổng trung kế):** Cho phép truyền tải dữ liệu của nhiều VLAN khác nhau đi qua trên một liên kết vật lý duy nhất (thường là đường kết nối giữa Switch - Switch hoặc Switch - Router). Switch sẽ thêm nhãn định danh VLAN ID (theo chuẩn **IEEE 802.1Q**) vào Frame khi gửi đi qua đường Trunk để Switch phía bên kia biết Frame đó thuộc VLAN nào.

---

## 4. Khái niệm cơ bản về Routing, Static Route và NAT

### a. Routing (Định tuyến lớp 3)
*   **Định nghĩa:** Hoạt động tại tầng Network (Layer 3). Là quá trình Router (hoặc Switch Layer 3) tìm kiếm và lựa chọn đường đi tối ưu nhất cho các gói tin (Packet) đi từ mạng nguồn sang mạng đích khác subnet dựa trên **Bảng định tuyến (Routing Table)**.

### b. Static Route (Định tuyến tĩnh)
*   **Định nghĩa:** Là phương pháp định tuyến mà người quản trị hệ thống phải tự tay cấu hình các tuyến đường đi cố định vào bảng định tuyến của Router.
*   **Ưu điểm:**
    *   Ít tốn tài nguyên xử lý (CPU/RAM) của Router do không phải chạy thuật toán tìm đường.
    *   Độ bảo mật cao và dễ kiểm soát luồng đi của dữ liệu trong mạng quy mô nhỏ.
*   **Nhược điểm:**
    *   Không có tính linh hoạt: Nếu một liên kết trên tuyến đường tĩnh bị đứt, Router không thể tự động tìm đường đi thay thế mà người quản trị phải vào sửa đổi cấu hình thủ công.
    *   Khó quản lý và cấu hình khi mạng mở rộng lên quy mô lớn (hàng trăm Router).

---

### c. NAT (Network Address Translation - Biên dịch địa chỉ mạng)
*   **Đặt vấn đề:** Dải địa chỉ IP công cộng (Public IP) rất hạn chế và đắt đỏ. Trong khi đó, hầu hết các thiết bị trong mạng nội bộ sử dụng dải IP tư nhân (Private IP - ví dụ `192.168.x.x`, `10.x.x.x`) không được phép định tuyến trực tiếp ra Internet.
*   **Giải pháp NAT:** NAT là kỹ thuật thay đổi thông tin địa chỉ IP nguồn/đích trong IP Header của gói tin khi nó đi qua Router biên dịch.
*   **Phân loại NAT phổ biến:**
    1.  **Static NAT (NAT tĩnh 1-1):** Ánh xạ cố định một địa chỉ Private IP sang một địa chỉ Public IP duy nhất. Thường dùng cho các máy chủ nội bộ cần public dịch vụ ra ngoài Internet (ví dụ Web Server).
    2.  **Dynamic NAT (NAT động):** Ánh xạ một nhóm địa chỉ Private IP sang một nhóm địa chỉ Public IP khả dụng (Pool) theo nguyên tắc ai đến trước dùng trước.
    3.  **PAT (Port Address Translation / NAT Overload):** Đây là loại NAT phổ biến nhất dùng trong hộ gia đình và doanh nghiệp. Cho phép hàng ngàn thiết bị dùng IP Private cùng truy cập Internet thông qua một IP Public duy nhất bằng cách thay đổi và theo dõi số hiệu **Port nguồn** của từng phiên kết nối.

---

## 5. Khái niệm cơ bản về Cân bằng tải (Load Balancer)

### a. Load Balancer là gì?
**Cân bằng tải (Load Balancer - LB)** là một thiết bị vật lý hoặc dịch vụ phần mềm đóng vai trò là điểm đầu mối nhận toàn bộ yêu cầu truy cập từ người dùng, sau đó phân phối lưu lượng đó một cách thông minh tới một nhóm các máy chủ xử lý (gọi là Server Pool / Backend Pool).

### b. Mục tiêu của Load Balancer
*   **Tăng tính sẵn sàng (High Availability):** Tự động phát hiện máy chủ bị lỗi thông qua các bài kiểm tra sức khỏe dịch vụ (Health Check) để ngừng gửi traffic tới đó, chuyển hướng sang máy chủ còn sống.
*   **Tối ưu hóa hiệu năng & Chống quá tải:** Chia đều tải cho các server, tránh tình trạng server này chạy 100% CPU trong khi server khác nhàn rỗi.
*   **Khả năng mở rộng (Scalability):** Dễ dàng thêm hoặc bớt máy chủ trong Server Pool mà không làm gián đoạn dịch vụ của người dùng cuối.

### c. Cân bằng tải Layer 4 vs Layer 7

#### Layer 4 Load Balancing (Cân bằng tải lớp Vận chuyển)
*   **Cơ chế:** Đưa ra quyết định định hướng traffic dựa trên thông tin ở tầng mạng và vận chuyển (IP nguồn/đích, Cổng nguồn/đích và Giao thức TCP/UDP).
*   **Đặc điểm:** Không can thiệp vào nội dung thực tế (Payload/Data) của gói tin. Do đó tốc độ xử lý cực nhanh, tốn rất ít tài nguyên hệ thống, nhưng không thể cấu hình các luật định tuyến phức tạp dựa trên nội dung ứng dụng.

#### Layer 7 Load Balancing (Cân bằng tải lớp Ứng dụng)
*   **Cơ chế:** Đọc và hiểu được nội dung của gói tin ở tầng Ứng dụng (như HTTP/HTTPS). Quyết định điều phối traffic dựa trên các thông tin như: URL Path (Ví dụ: `/images` gửi sang cụm server ảnh, `/api` gửi sang cụm server logic), HTTP Headers, Cookies, hoặc kiểu trình duyệt của client.
*   **Đặc điểm:** Cực kỳ thông minh và linh hoạt. Hỗ trợ các tính năng nâng cao như: **SSL Termination** (giải mã HTTPS ngay tại Load Balancer để giảm tải cho server backend), Sticky Sessions (giữ phiên làm việc của Client luôn kết nối với một server cố định nhờ Cookie). Nhược điểm là tốn tài nguyên xử lý hơn Layer 4.

---

## 6. Tổng kết
Việc nắm chắc các kiến thức lý thuyết mạng này là tiền đề quan trọng giúp:
1. Thiết kế và triển khai hạ tầng mạng ảo hóa chính xác trong các bài thực hành tiếp theo.
2. Hiểu rõ nguyên lý kết nối và bảo mật giữa các ứng dụng dạng Microservices hoặc Multi-tier.
3. Cấu hình định tuyến và phân phối tải cho hệ thống lớn hoạt động ổn định trên môi trường Cloud.
