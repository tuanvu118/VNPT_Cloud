# BÁO CÁO LÝ THUYẾT - PHẦN 5: CƠ BẢN VỀ KUBERNETES

* **Nội dung:** Tìm hiểu tổng quan về công nghệ Containerization và kiến trúc Microservices; phân biệt vị trí, vai trò của Docker và Kubernetes; so sánh sự khác nhau giữa các Container Engine/Runtime (Docker Engine, Containerd, CRI-O); nắm vững các cơ chế quản lý Pod (Deployment, StatefulSet, DaemonSet), các giao thức truyền tải dịch vụ (ClusterIP, NodePort, LoadBalancer, Ingress) và cơ chế quản lý lưu trữ Persistent Storage trong Kubernetes.
---

## 1. Khái niệm về Container và Kiến trúc Microservices

### a. Công nghệ Container và so sánh với Máy ảo (Virtualization)
*   **Virtualization (Ảo hóa truyền thống - Máy ảo VM):**
    *   *Cơ chế:* Sử dụng phần mềm Hypervisor (như VMware ESXi, KVM, Hyper-V) chạy trực tiếp trên phần cứng để phân chia tài nguyên vật lý thành nhiều máy ảo độc lập. Mỗi máy ảo (VM) đều bắt buộc phải cài đặt và vận hành một hệ điều hành khách riêng biệt (**Guest OS**) cùng với toàn bộ driver hệ thống, thư viện và ứng dụng đi kèm.
    *   *Đặc điểm:* Cô lập hoàn toàn ở mức phần cứng, cực kỳ an toàn. Tuy nhiên, hiệu năng bị suy hao do gánh nặng chạy nhiều Guest OS cùng lúc, dung lượng file máy ảo rất lớn (vài GB đến hàng chục GB) và thời gian khởi động lâu (từ vài chục giây đến vài phút).
*   **Containerization (Công nghệ đóng gói Container):**
    *   *Cơ chế:* Không ảo hóa phần cứng để cài hệ điều hành khách. Thay vào đó, toàn bộ các Container chạy trực tiếp trên cùng một hệ điều hành máy chủ vật lý (**Host OS**), chia sẻ chung nhân hệ điều hành (**Shared Kernel**) của máy Host. Các container được cô lập độc lập với nhau ở mức tiến trình nhờ các tính năng cốt lõi của nhân Linux là **Namespaces** (cô lập tài nguyên mạng, tiến trình, mount point...) và **Cgroups** (giới hạn tài nguyên CPU, RAM).
    *   *Đặc điểm:* Dung lượng siêu nhẹ (chỉ từ vài MB đến vài trăm MB), tốc độ khởi động nhanh tức thì (chỉ mất vài mili giây đến vài giây), hiệu năng đọc ghi đạt tốc độ gần như tiệm cận máy vật lý và mật độ triển khai trên một máy chủ cao gấp nhiều lần so với máy ảo.

| Tiêu chí so sánh | Máy ảo (Virtual Machine - VM) | Container |
| :--- | :--- | :--- |
| **Hệ điều hành** | Mỗi VM chạy một Guest OS riêng biệt hoàn chỉnh. | Chia sẻ chung nhân (Kernel) của Host OS. |
| **Hypervisor** | Bắt buộc phải có (VMware, VirtualBox, KVM). | Không cần. Sử dụng Container Engine (Docker, Containerd). |
| **Dung lượng tệp** | Rất nặng (từ vài GB trở lên). | Siêu nhẹ (từ vài MB đến vài trăm MB). |
| **Thời gian khởi động** | Chậm (Vài chục giây đến vài phút). | Gần như ngay lập tức (Miligiây đến vài giây). |
| **Tài nguyên tiêu hao** | Cao (Do phải cấp phát RAM/CPU cố định cho Guest OS). | Thấp (Chỉ tiêu tốn tài nguyên thực tế tiến trình sử dụng). |
| **Độ cô lập an toàn** | Cực kỳ cao (Cô lập ở mức phần cứng). | Trung bình cao (Cô lập ở mức tiến trình và nhân OS). |

### b. Kiến trúc Microservices (Dịch vụ nhỏ) và so sánh với Monolithic (Đơn khối)
*   **Monolithic Architecture (Kiến trúc đơn khối):**
    *   *Định nghĩa:* Toàn bộ các chức năng của ứng dụng (quản lý người dùng, thanh toán, hiển thị sản phẩm, gửi email...) đều được viết chung trong một dự án mã nguồn duy nhất và đóng gói chạy thành một tiến trình duy nhất.
    *   *Ưu điểm:* Dễ dàng xây dựng, chạy thử nghiệm trực tiếp và triển khai nhanh ở giai đoạn đầu.
    *   *Nhược điểm:* Khi ứng dụng phình to, mã nguồn sẽ trở nên cực kỳ phức tạp và khó bảo trì. Một lỗi nhỏ ở một chức năng phụ (ví dụ lỗi gửi email) có thể làm sập toàn bộ hệ thống. Rất khó scale (mở rộng) cục bộ (ví dụ chỉ muốn tăng tài nguyên cho chức năng xử lý thanh toán nhưng bắt buộc phải nhân bản toàn bộ ứng dụng lớn).
*   **Microservices Architecture (Kiến trúc dịch vụ nhỏ):**
    *   *Định nghĩa:* Ứng dụng được chia nhỏ thành các dịch vụ độc lập, mỗi dịch vụ đảm nhận một nghiệp vụ nghiệp vụ chuyên biệt (Ví dụ: Service Thanh toán, Service Giỏ hàng). Các dịch vụ này giao tiếp với nhau qua mạng bằng API (RESTful API, gRPC) hoặc Message Queue (RabbitMQ, Kafka).
    *   *Ưu điểm:* Dễ dàng nâng cấp, bảo trì độc lập từng dịch vụ. Nếu một dịch vụ bị lỗi (ví dụ dịch vụ bình luận bị sập), các dịch vụ khác như xem sản phẩm và mua hàng vẫn hoạt động bình thường. Cho phép scale cục bộ dịch vụ chịu tải cao một cách linh hoạt, tiết kiệm tài nguyên.
    *   *Nhược điểm:* Thiết kế hệ thống phức tạp hơn, khó khăn trong việc quản trị hạ tầng, đảm bảo tính đồng bộ dữ liệu giữa các dịch vụ và giám sát lưu lượng mạng.

---

## 2. Phân biệt Docker và Kubernetes (K8s)

Rất nhiều người thường nhầm lẫn Docker và Kubernetes là đối thủ cạnh tranh của nhau, nhưng thực tế chúng được thiết kế cho các nhiệm vụ hoàn toàn khác nhau và hỗ trợ lẫn nhau:

*   **Docker (Công cụ đóng gói và vận hành Container đơn lẻ):**
    *   *Nhiệm vụ:* Tập trung vào việc **xây dựng (Build), đóng gói (Package) và chạy (Run)** các container trên một máy chủ đơn lẻ.
    *   *Cách thức hoạt động:* Docker định nghĩa cấu trúc container thông qua tệp `Dockerfile` để đóng gói mã nguồn và môi trường thành một `Image` cố định. Sau đó, nó chạy image đó thành các Container độc lập trên máy chủ.
    *   *Hạn chế:* Docker không được thiết kế để quản lý hàng trăm container chạy trên nhiều máy chủ vật lý khác nhau. Nó không tự động xử lý khi một máy chủ vật lý bị sập (làm chết các container trên đó), không tự động mở rộng (auto-scale) khi tải tăng đột biến, và quản lý mạng/cân bằng tải thủ công rất phức tạp.
*   **Kubernetes - K8s (Hệ thống điều phối Container quy mô lớn):**
    *   *Nhiệm vụ:* Tập trung vào việc **điều phối, quản lý và tự động hóa** hàng ngàn container chạy trên một cụm máy chủ (**Cluster**) gồm nhiều Node vật lý hoặc máy ảo khác nhau.
    *   *Cách thức hoạt động:* K8s không tự đóng gói container. Nó nhận các Docker Image (hoặc image từ các công cụ khác), sau đó tự động lập lịch phân bổ chúng chạy trên các Node máy chủ trống tài nguyên, quản lý vòng đời, tự động sửa lỗi (Self-healing), tự động nhân bản (Scaling) và cấu hình mạng kết nối giữa chúng.
    *   *Ví dụ minh họa:* Docker đóng vai trò là các **nhạc công** chơi các nhạc cụ riêng lẻ, còn Kubernetes đóng vai trò là **nhạc trưởng** điều phối toàn bộ ban nhạc để cùng hòa tấu nhịp nhàng.

---

## 3. Phân biệt các Container Runtime (Docker Engine, Containerd, CRI-O)

Để chạy được container, Kubernetes cần một thành phần phần mềm bậc thấp chịu trách nhiệm tải image và trực tiếp khởi tạo container. Thành phần này gọi là **Container Runtime**. 
Ban đầu K8s sử dụng Docker làm runtime mặc định. Tuy nhiên, sau này K8s đã chuẩn hóa giao diện tương tác thông qua tiêu chuẩn **CRI (Container Runtime Interface)** để tách biệt với Docker:

*   **Docker Engine:**
    *   Là một bộ công cụ hoàn chỉnh, bao gồm giao diện CLI, daemon xử lý API, trình build image, trình quản lý volume, mạng... 
    *   Vì quá đồ sộ và chứa nhiều tính năng không cần thiết cho việc vận hành trong cụm máy chủ, đồng thời không tuân thủ trực tiếp chuẩn CRI, Docker Engine đã bị Kubernetes **loại bỏ hoàn toàn sự hỗ trợ (deprecated)** kể từ phiên bản K8s 1.24.
*   **Containerd:**
    *   Thực chất là một thành phần cốt lõi được tách ra từ chính dự án Docker Engine nhằm thực hiện nhiệm vụ quản lý vòng đời container tối giản nhất (tải image, chạy, dừng, giám sát container).
    *   Được phát triển tuân thủ chuẩn CRI của CNCF. Nó hoạt động siêu nhẹ, tiêu tốn cực ít RAM/CPU và hiện đang là **Container Runtime phổ biến nhất** trong các cụm K8s ngày nay.
*   **CRI-O:**
    *   Là một Container Runtime được phát triển độc lập bởi Red Hat và cộng đồng, được viết ra **chỉ để dành riêng cho Kubernetes** tuân thủ 100% chuẩn CRI.
    *   CRI-O lược bỏ hoàn toàn tất cả các tính năng phụ thừa thãi, chỉ giữ lại đúng những mã nguồn tối thiểu nhất để khởi chạy container. Nhờ đó, nó có độ bảo mật cao nhất, thời gian phản hồi siêu tốc và hoạt động vô cùng ổn định.

---

## 4. Tìm hiểu các K8s Controller phổ biến (Deployment, StatefulSet, DaemonSet)

Trong Kubernetes, các tài nguyên không được quản lý thủ công mà được giám sát thông qua các **Controller** để duy trì trạng thái mong muốn (Desired State) của hệ thống:

### a. Deployment
*   **Đặc điểm:** Là Controller phổ biến nhất, chuyên dùng để quản lý các ứng dụng **Stateless** (ứng dụng không lưu trạng thái nội bộ, ví dụ: Web frontend, API Gateway, Nginx).
*   **Cơ chế hoạt động:** 
    *   Quản lý việc nhân bản số lượng Pod mong muốn (Replicaset).
    *   Hỗ trợ cơ chế cập nhật không gián đoạn **Rolling Update** (tạo Pod phiên bản mới trước, kiểm tra sức khỏe ổn định rồi mới xóa Pod phiên bản cũ) và **Rollback** (quay xe về phiên bản cũ ngay lập tức nếu phiên bản mới bị lỗi).
    *   Các Pod do Deployment tạo ra có tên ngẫu nhiên (ví dụ: `myweb-5f7bc9-abcde`), nếu một Pod bị sập, K8s sẽ tạo một Pod mới thay thế với một định danh số ngẫu nhiên khác hoàn toàn.

### b. StatefulSet
*   **Đặc điểm:** Chuyên dụng để quản lý các ứng dụng **Stateful** (ứng dụng bắt buộc phải lưu trữ và đồng bộ trạng thái dữ liệu, ví dụ: Database PostgreSQL, MySQL, Redis, MongoDB).
*   **Cơ chế hoạt động:**
    *   Các Pod do StatefulSet tạo ra được gắn định danh cố định không đổi tăng dần từ 0 (Ví dụ: `db-0`, `db-1`, `db-2`).
    *   Khi nâng cấp hoặc khởi động, các Pod sẽ được khởi tạo lần lượt theo thứ tự (từ `db-0` đến `db-2`) và khi tắt thì tắt theo chiều ngược lại để tránh xung đột dữ liệu.
    *   Mỗi Pod trong StatefulSet sẽ được gắn kết chặt chẽ với một phân vùng lưu trữ riêng biệt (Persistent Volume) cố định. Nếu Pod `db-0` bị sập và khởi động lại trên Node khác, nó vẫn kết nối đúng với ổ đĩa dữ liệu cũ của nó.

### c. DaemonSet
*   **Đặc điểm:** Đảm bảo chạy **duy nhất một bản sao Pod** trên tất cả các Node (hoặc một số Node chỉ định cụ thể) trong cụm Cluster.
*   **Cơ chế hoạt động:**
    *   Khi có một Node mới được thêm vào cụm Cluster, DaemonSet sẽ tự động tạo một Pod trên Node đó. Khi Node bị xóa khỏi cụm, Pod tương ứng cũng sẽ bị hủy đi.
    *   *Ứng dụng tiêu biểu:* Thu thập log hệ thống (Fluentd, Logstash), giám sát tài nguyên Node (Prometheus Node Exporter, Datadog Agent) hoặc chạy các dịch vụ mạng (Flannel, Calico).

---

## 5. Tìm hiểu cơ chế mạng và Services trong K8s

Mặc định, mỗi Pod khi tạo ra đều được cấp một địa chỉ IP nội bộ riêng. Tuy nhiên, IP này sẽ bị thay đổi mỗi khi Pod bị khởi động lại hoặc thay thế. Để giải quyết vấn đề này, K8s cung cấp đối tượng **Service** đóng vai trò là một đầu mối kết nối cố định có cân bằng tải đi đến các Pod phía sau:

### a. ClusterIP (Mặc định)
*   **Nguyên lý:** K8s cấp cho Service một địa chỉ IP ảo cố định chỉ có giá trị truy cập **nội bộ bên trong cụm Cluster**.
*   **Ứng dụng:** Dùng cho các dịch vụ chạy ngầm không cần phơi bày ra thế giới bên ngoài như database, cache, hoặc các dịch vụ nội bộ kết nối với nhau.

### b. NodePort
*   **Nguyên lý:** K8s sẽ mở một cổng tĩnh (trong dải mặc định `30000 - 32767`) trên **tất cả các Node** (cả Master và Worker). Bất kỳ lưu lượng truy cập nào gửi tới địa chỉ `IP_Node:NodePort` sẽ được tự động chuyển tiếp tới các Pod tương ứng của Service.
*   **Ứng dụng:** Dùng để kiểm thử ứng dụng nhanh hoặc khi hệ thống chưa tích hợp Load Balancer ngoài.

### c. LoadBalancer
*   **Nguyên lý:** Tích hợp trực tiếp với các nhà cung cấp Cloud (AWS, Azure, GCP...). Khi tạo Service kiểu này, Cloud Provider sẽ tự động cấp một bộ cân bằng tải vật lý (External Load Balancer) với địa chỉ IP công cộng (Public IP) chuyển tiếp traffic vào cụm.
*   **Ứng dụng:** Dành cho các dịch vụ Web chính thức cần mở rộng cho khách hàng truy cập từ Internet. Trong môi trường On-Premises tự dựng (như máy ảo ở nhà), ta cần cài thêm công cụ như **MetalLB** để giả lập tính năng này.

### d. Ingress
*   **Nguyên lý:** Là một đối tượng quản lý định tuyến ở tầng ứng dụng (Layer 7 Routing). Ingress hoạt động như một Reverse Proxy (sử dụng Nginx Ingress Controller hoặc HAProxy Ingress) để tiếp nhận toàn bộ traffic HTTP/HTTPS đi vào và định tuyến tới các Service khác nhau dựa trên đường dẫn dẫn (URL Path) hoặc tên miền (Host Name).
*   **Ứng dụng:** Tiết kiệm IP Public (chỉ cần duy nhất 1 LoadBalancer trỏ tới Ingress, Ingress sẽ phân phối traffic cho hàng trăm dịch vụ bên trong), đồng thời hỗ trợ quản lý SSL/TLS tập trung.

---

## 6. Tìm hiểu về lưu trữ dữ liệu (Persistent Storage) trong K8s

Vì các Pod trong K8s có tính chất tạm thời (Ephemeral) - dữ liệu ghi bên trong Pod sẽ bị xóa sạch hoàn toàn nếu Pod bị lỗi hoặc bị thay thế. Để lưu trữ dữ liệu bền vững, K8s sử dụng cơ chế quản lý lưu trữ Persistent Storage:

### a. Khái niệm PV, PVC và mối quan hệ
*   **PersistentVolume (PV - Phân vùng lưu trữ vật lý):**
    *   Là một tài nguyên lưu trữ thực tế trong cụm Cluster do Quản trị viên hệ thống (Admin) cấu hình sẵn trước. PV đại diện cho một không gian lưu trữ vật lý cụ thể. Các loại PV phổ biến bao gồm:
        *   **hostPath:** Gắn kết một thư mục hoặc tệp tin từ hệ thống tệp của Node máy chủ trực tiếp vào Pod. Thích hợp cho môi trường phát triển hoặc chạy cụm đơn node.
        *   **Local Persistent Volume / LVM:** Gắn kết các phân vùng ổ cứng cục bộ (như ổ đĩa LVM đã chia tách) trên các Node để có tốc độ đọc ghi tối đa.
        *   **Network Storage (NFS, Ceph, GlusterFS...):** Hệ thống lưu trữ phân tán qua mạng, cho phép Pod di chuyển linh hoạt giữa các Node khác nhau mà không sợ mất kết nối dữ liệu.
    *   PV tồn tại độc lập hoàn toàn với vòng đời của các Pod.
*   **PersistentVolumeClaim (PVC - Yêu cầu cấp phát lưu trữ):**
    *   Là yêu cầu xin cấp phát tài nguyên lưu trữ do Lập trình viên (User) tạo ra. PVC mô tả các yêu cầu cụ thể như: *"Tôi cần một ổ đĩa dung lượng 5GB, có quyền đọc ghi đồng thời (ReadWriteMany)"*.
*   **Mối quan hệ:**
    *   PVC đóng vai trò là "phiếu yêu cầu mua hàng", còn PV đóng vai trò là "mặt hàng có sẵn trong kho".
    *   Kubernetes sẽ tự động tìm kiếm trong cụm có PV nào phù hợp với yêu cầu của PVC hay không. Nếu tìm thấy, K8s sẽ thực hiện liên kết (**Bind**) chúng lại với nhau để cấp cho Pod sử dụng.

### b. StorageClass và cơ chế Dynamic Provisioning (Cấp phát động)
*   **Static Provisioning (Cấp phát tĩnh thủ công):** Admin phải tự đi tạo từng ổ cứng vật lý (PV) trước, sau đó người dùng mới viết PVC để bind. Cách này rất mất thời gian và khó mở rộng khi có hàng trăm ứng dụng cần đĩa cứng.
*   **Dynamic Provisioning (Cấp phát động tự động):** 
    *   Admin chỉ cần định nghĩa một đối tượng **StorageClass** đóng vai trò là bản thiết kế của loại ổ cứng (ví dụ: ổ cứng SSD tốc độ cao, ổ cứng HDD lưu trữ log...).
    *   Khi người dùng tạo một PVC yêu cầu gắn StorageClass này, StorageClass sẽ tự động gọi API của hệ thống lưu trữ bên dưới (ví dụ API của AWS, Ceph, LVM...) để tự động tạo ra một ổ cứng vật lý tương ứng và tự động tạo PV để bind cho PVC đó. Quy trình diễn ra hoàn toàn tự động trong vài giây mà không cần sự can thiệp thủ công của Admin.
