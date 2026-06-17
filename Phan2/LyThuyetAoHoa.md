# BÁO CÁO LÝ THUYẾT: CƠ BẢN VỀ ẢO HÓA VÀ CLOUD

* **Nội dung:** Tìm hiểu các khái niệm cơ bản về ảo hóa, tài nguyên ảo (vCPU, vRAM, vDisk, vNIC), các cơ chế cấp phát tài nguyên (Overcommit, Thin Provisioning) và cấu trúc phần cứng CPU (Socket, Core).

---

## 1. Khái niệm về Ảo hóa (Virtualization)

### Ảo hóa là gì?
**Ảo hóa (Virtualization)** là công nghệ cho phép tạo ra các phiên bản ảo (phần mềm đại diện) của các tài nguyên phần cứng vật lý như CPU, RAM, ổ cứng, thiết bị mạng. 

Công nghệ này sử dụng một lớp phần mềm trung gian gọi là **Hypervisor** (Bộ giám sát máy ảo) để tách biệt phần cứng vật lý khỏi hệ điều hành của máy ảo. Nhờ đó, trên một máy chủ vật lý (Host) có thể chạy đồng thời nhiều hệ điều hành độc lập (Guest OS) với các tài nguyên được phân chia riêng biệt.

### Phân loại Hypervisor:
* **Type-1 Hypervisor (Bare-metal):** Cài đặt trực tiếp lên phần cứng vật lý của máy chủ (không cần hệ điều hành nền). Hiệu năng rất cao, thường dùng trong môi trường doanh nghiệp và trung tâm dữ liệu. 
  * *Ví dụ:* VMware ESXi, Microsoft Hyper-V, KVM.
* **Type-2 Hypervisor (Hosted):** Chạy như một ứng dụng trên một hệ điều hành máy chủ có sẵn (Windows, macOS, Linux). Thích hợp cho việc thử nghiệm, học tập cá nhân.
  * *Ví dụ:* VMware Workstation, Oracle VM VirtualBox, Parallels Desktop.

---

## 2. Các thành phần tài nguyên ảo (vCPU, vRAM, vDisk, vNIC)

Khi tạo một máy ảo (Virtual Machine - VM), Hypervisor sẽ cấp phát cho nó các tài nguyên phần cứng ảo tương ứng với phần cứng vật lý:

### a. vCPU (Virtual CPU)
* **Khái niệm:** vCPU là bộ vi xử lý ảo được gán cho máy ảo. 
* **Bản chất:** vCPU không phải là một chip vật lý riêng biệt, mà thực chất là một khoảng thời gian xử lý (time slice) được Hypervisor phân phối từ các CPU vật lý (lõi vật lý hoặc luồng logic) cho máy ảo thông qua bộ lập lịch CPU (CPU Scheduler).
* **Quy chuẩn:** 1 vCPU thường tương đương với 1 luồng logic (Logical Processor/Thread) của CPU vật lý trên máy Host.

### b. vRAM (Virtual RAM)
* **Khái niệm:** vRAM là bộ nhớ RAM ảo được cấp phát cho máy ảo.
* **Bản chất:** Khi máy ảo khởi động, Hypervisor ánh xạ không gian địa chỉ bộ nhớ ảo của máy ảo vào bộ nhớ RAM vật lý thực tế của máy Host. 
* **Quản lý:** RAM ảo hoạt động độc lập giữa các máy ảo. Khi một máy ảo truy xuất RAM, Hypervisor sẽ đảm bảo nó không can thiệp vào vùng nhớ của máy ảo khác hoặc của hệ điều hành Host.

### c. vDisk (Virtual Disk)
* **Khái niệm:** vDisk là ổ đĩa cứng ảo được gán cho máy ảo để lưu trữ hệ điều hành và dữ liệu.
* **Bản chất:** Trên hệ thống lưu trữ vật lý của máy Host, vDisk thực chất chỉ là một tệp tin duy nhất (ví dụ: `.vmdk` của VMware, `.vdi` của VirtualBox, `.qcow2` của KVM). Hệ điều hành bên trong máy ảo sẽ nhận diện tệp tin này như một ổ đĩa cứng vật lý thông thường và tiến hành phân vùng, định dạng hệ thống tệp (NTFS, ext4...) trên đó.

### d. vNIC (Virtual Network Interface Card)
* **Khái niệm:** vNIC là card mạng ảo được gán cho máy ảo để kết nối mạng.
* **Bản chất:** vNIC được giả lập bằng phần mềm bởi Hypervisor. Mỗi vNIC sẽ có một địa chỉ MAC ảo riêng độc nhất. 
* **Kết nối:** vNIC kết nối với các **vSwitch** (Virtual Switch - Switch ảo) do Hypervisor tạo ra, từ đó định tuyến lưu lượng mạng đi ra ngoài card mạng vật lý của máy Host hoặc kết nối nội bộ giữa các máy ảo với nhau.

---

## 3. Khái niệm Overcommit và Thin Provisioning

Đây là hai cơ chế tối ưu hóa tài nguyên cực kỳ quan trọng trong công nghệ ảo hóa nhằm tăng mật độ máy ảo trên một máy chủ vật lý.

### a. Overcommit (Cấp phát vượt mức)
* **Định nghĩa:** Overcommit là hành động cấu hình cấp phát tổng tài nguyên ảo (CPU, RAM) cho toàn bộ các máy ảo vượt quá khả năng đáp ứng vật lý thực tế của máy chủ Host.
* **Nguyên lý hoạt động:** Trong thực tế, các máy ảo hiếm khi sử dụng 100% tài nguyên CPU và RAM cùng một lúc. Do đó, Hypervisor tận dụng lượng tài nguyên nhàn rỗi của máy ảo này để cấp phát cho máy ảo khác đang cần xử lý.
* **Phân loại:**
  * **CPU Overcommit:** Rất phổ biến và an toàn. Tỷ lệ vCPU:pCPU (physcial CPU) có thể đạt 2:1, 4:1 hoặc cao hơn tùy thuộc vào tải của ứng dụng.
  * **RAM Overcommit:** Nguy hiểm hơn vì nếu các máy ảo đồng loạt dùng hết RAM, Host sẽ bị cạn kiệt tài nguyên vật lý, dẫn đến hiện tượng tráo đổi bộ nhớ ra ổ cứng (swapping) làm giảm hiệu năng nghiêm trọng hoặc treo hệ thống. Hypervisor sử dụng các kỹ thuật như *Memory Ballooning*, *Transparent Page Sharing (TPS)* để giảm thiểu rủi ro này.

### b. Thin Provisioning (Cấp phát mỏng / Cấp phát động)
Đây là công nghệ quản lý cấp phát dung lượng ổ cứng ảo (vDisk).
* **Thin Provisioning (Cấp phát mỏng):** 
  * *Cách hoạt động:* Ổ cứng ảo chỉ chiếm dụng không gian lưu trữ vật lý trên máy Host tương đương với dung lượng dữ liệu thực tế đang có trong máy ảo. Dung lượng tệp đĩa ảo sẽ tự động phình to dần theo thời gian sử dụng cho đến khi đạt giới hạn cấu hình tối đa.
  * *Ưu điểm:* Tiết kiệm dung lượng lưu trữ ban đầu, tránh lãng phí tài nguyên trống.
  * *Nhược điểm:* Nếu không giám sát chặt chẽ, tổng dung lượng cấu hình ảo vượt quá ổ đĩa vật lý thực tế (Storage Overcommit), khi các máy ảo đồng loạt ghi đầy dữ liệu sẽ làm tràn ổ đĩa vật lý của Host, gây lỗi toàn bộ hệ thống.
* **Thành phần đối đối chiếu - Thick Provisioning (Cấp phát dày):**
  * *Cách hoạt động:* Chiếm dụng toàn bộ không gian đĩa vật lý ngay khi khởi tạo máy ảo (ví dụ: tạo VM 100GB thì ổ cứng Host mất ngay 100GB trống, dù chưa có dữ liệu bên trong VM).
  * *Ưu điểm:* Hiệu năng ghi dữ liệu ban đầu tốt hơn, đảm bảo chắc chắn không bị thiếu hụt dung lượng đĩa vật lý bất ngờ.
  * *Nhược điểm:* Lãng phí dung lượng lưu trữ khi máy ảo chưa dùng hết dung lượng được cấp.

---

## 4. Khái niệm về Socket, CPU Core và mối liên hệ với vCPU

Để cấu hình và phân bổ vCPU tối ưu cho máy ảo, người quản trị cần nắm rõ cấu trúc phần cứng CPU vật lý:

### a. Socket (Đế cắm CPU)
* **Định nghĩa:** Socket là khe cắm vật lý trên bo mạch chủ (Mainboard) dùng để gắn bộ vi xử lý (chip CPU vật lý) vào.
* **Vai trò:** Số lượng Socket trên một máy chủ quyết định số lượng chip CPU vật lý tối đa có thể lắp đặt. Máy chủ doanh nghiệp thường có 1 Socket (Single-Socket), 2 Sockets (Dual-Socket) hoặc 4 Sockets.

### b. CPU Core (Nhân / Lõi CPU)
* **Định nghĩa:** Core là một đơn vị xử lý độc lập về mặt vật lý nằm bên trong một chip CPU. 
* **Vai trò:** Mỗi lõi (Core) có đầy đủ các thành phần như khối tính toán ALU, các thanh ghi và bộ nhớ đệm Cache riêng để tự xử lý một chuỗi lệnh độc lập. CPU hiện đại là CPU đa nhân (Multi-core), tích hợp từ 4, 8, 16 cho đến 64 cores hoặc nhiều hơn trên một chip đơn.

### c. Mối quan hệ giữa Socket, Core, Thread và vCPU
* **Siêu phân luồng (Hyper-Threading):** Công nghệ của Intel (hoặc SMT của AMD) cho phép một lõi vật lý (Core) xử lý đồng thời 2 luồng công việc (Threads). Mỗi luồng này được hệ điều hành nhận diện là một bộ vi xử lý logic (Logical Processor).
* **Công thức tính số Logical Processors trên máy Host:**
  $$\text{Tổng số Logical Processors} = \text{Số Sockets} \times \text{Số Cores trên mỗi Socket} \times \text{Số Luồng (Threads) trên mỗi Core}$$
  * *Ví dụ:* Một máy chủ có 2 Sockets, mỗi chip CPU có 16 Cores, hỗ trợ Hyper-Threading (2 Threads/Core) sẽ có tổng cộng:  
    $$2 \times 16 \times 2 = 64 \text{ Logical Processors}$$
    Đồng nghĩa với việc máy chủ này có tối đa 64 luồng xử lý độc lập có thể cung cấp làm vCPU cho các máy ảo.
