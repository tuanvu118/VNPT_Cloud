# Sử dụng base image Python gọn nhẹ
FROM python:3.10-slim

# Thiết lập thư mục làm việc trong container
WORKDIR /app

# Sao chép file requirements.txt vào container
COPY requirements.txt .

# Cài đặt các thư viện cần thiết
RUN pip install --no-cache-dir -r requirements.txt

# Sao chép toàn bộ mã nguồn và file cấu hình (.env, main.py) vào container
COPY . .

# Mở cổng 8000 để truy cập ứng dụng từ bên ngoài container
EXPOSE 8000

# Lệnh chạy ứng dụng FastAPI khi container khởi động
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
