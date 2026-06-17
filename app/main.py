import os
import psycopg2
from psycopg2.extras import RealDictCursor
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv

# Tải cấu hình từ file .env
load_dotenv()

DB_HOST = os.getenv("DB_HOST", "127.0.0.1")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "password")
DB_NAME = os.getenv("DB_NAME", "postgres")

app = FastAPI(
    title="FastAPI VM App Connects to VM DB",
    description="Ứng dụng FastAPI đơn giản kết nối tới PostgreSQL trên máy ảo khác trong mạng LAN",
    version="1.0.0"
)

# Khai báo cấu trúc dữ liệu cho API thêm mới Item
class Item(BaseModel):
    name: str
    description: str = None

def get_db_connection():
    """Hàm tạo kết nối tới cơ sở dữ liệu PostgreSQL"""
    return psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        cursor_factory=RealDictCursor,
        connect_timeout=3 # Hạn chế treo ứng dụng nếu mất kết nối
    )

@app.on_event("startup")
def startup_db_init():
    """Tự động khởi tạo bảng dữ liệu mẫu khi ứng dụng khởi chạy (nếu kết nối DB thành công)"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        # Tạo bảng nếu chưa tồn tại
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS test_items (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                description TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        conn.commit()
        cursor.close()
        conn.close()
        print("💡 [DB INIT] Khởi tạo bảng 'test_items' thành công!")
    except Exception as e:
        print(f"⚠️ [DB INIT WARN] Không thể kết nối DB lúc khởi động để tạo bảng: {e}")

@app.get("/")
def read_root():
    """Trang thông tin chung"""
    return {
        "status": "online",
        "app": "FastAPI Demo Connection",
        "target_db_host": DB_HOST,
        "target_db_port": DB_PORT,
        "message": "Sử dụng endpoint /db-test để kiểm tra kết nối tới Database."
    }

@app.get("/db-test")
def test_db_connection():
    """Endpoint dùng để kiểm tra kết nối trực tiếp đến Database và trả về phiên bản PostgreSQL"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT version();")
        db_version = cursor.fetchone()
        cursor.close()
        conn.close()
        return {
            "status": "success",
            "message": "Kết nối tới Database thành công!",
            "database_version": db_version["version"]
        }
    except Exception as e:
        return {
            "status": "failed",
            "message": "Không thể kết nối tới Database. Vui lòng kiểm tra địa chỉ IP, cổng, tường lửa hoặc thông tin đăng nhập.",
            "error_detail": str(e)
        }

@app.get("/items")
def get_items():
    """Đọc dữ liệu từ bảng test_items trong Database"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM test_items ORDER BY id DESC;")
        items = cursor.fetchall()
        cursor.close()
        conn.close()
        return {"items": items}
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Lỗi khi đọc dữ liệu từ Database: {str(e)}"
        )

@app.post("/items")
def create_item(item: Item):
    """Thêm mới dữ liệu vào bảng test_items trong Database"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO test_items (name, description) VALUES (%s, %s) RETURNING *;",
            (item.name, item.description)
        )
        new_item = cursor.fetchone()
        conn.commit()
        cursor.close()
        conn.close()
        return {
            "status": "success",
            "message": "Thêm dữ liệu thành công!",
            "data": new_item
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Lỗi khi ghi dữ liệu vào Database: {str(e)}"
        )

if __name__ == "__main__":
    import uvicorn
    # Khởi chạy ứng dụng lắng nghe ở cổng 8000 trên tất cả các card mạng
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
