# Week4-Day1: Giới thiệu FastAPI

Fast API là 1 framework Python hiện đại dùng để xây dựng API (RESTful hoặc GraphQL). Được thiết kế với mục tiêu:
•	Dễ dùng cho lập trình viên
•	Hiệu suất cao 
•	Tự động sinh tài liệu API 
•	Tối ưu hóa trải nghiệm code với type hints của Python.
FastAPI được xây dựng trên Starlette (cho web server) và Pydantic (cho validation dữ liệu), hai thư viện mạnh mẽ.
Ưu điểm chính:
Tính năng	Mô tả
Hiệu suất nhanh	Ngang Go, NodeJS nhờ hỗ trợ async/await
Docs tự động	Swagger UI & ReDoc tự sinh từ code
Kiểm tra kiểu dữ liệu tự động	Dựa vào Pydantic & type hints
Async natively	Viết API bất đồng bộ dễ dàng
Autocomplete & editor friendly	Hỗ trợ tốt trong VSCode, PyCharm
Tích hợp bảo mật dễ dàng	OAuth2, JWT, Basic Auth đều có
Hỗ trợ dependency injection	Cho việc tái sử dụng code, kiểm soát logic dễ dàng
Testing đơn giản	Tích hợp tốt với pytest, httpx

Tạo Server cơ bản: 
B1 : pip install fastapi uvicorn 
	(FastAPI là framework, còn Uvicorn là server chạy FastAPI (giống như Node chạy Express)).
B2 : tạo file main.py rồi viết code
B3 : Chạy server 
	Truy cập trình duyệt 
Truy cập: http://127.0.0.1:8000/ → để xem kết quả JSON
Truy cập: http://127.0.0.1:8000/docs → để test API bằng Swagger UI

Cấu trúc project cơ bán thực tế:
fastapi_project/
├── app/
│   ├── __init__.py
│   ├── main.py              ← Điểm khởi đầu app FastAPI
│   ├── api/                 ← Các route/API chia theo chức năng
│   │   ├── __init__.py
│   │   └── v1/
│   │       ├── __init__.py
│   │       ├── endpoints/
│   │       │   ├── __init__.py
│   │       │   └── example.py  	← Route GET/POST
│   │       └── router.py        ← Gom tất cả route v1
│   ├── core/
│   │   ├── __init__.py
│   │   └── config.py           ← Cấu hình app (CORS, env, API keys...)
│   ├── models/
│   │   ├── __init__.py
│   │   └── item.py             ← Khai báo schema (BaseModel)
│   ├── services/
│   │   ├── __init__.py
│   │   └── openai_service.py   ← Gọi OpenAI API ở đây
│   └── utils/
│       └── helper.py           ← Hàm phụ trợ, xử lý chung
├── .env                        ← Biến môi trường (API keys, port...)
├── requirements.txt            ← Các thư viện cần cài
└── run.py                      ← File chạy chính (gọi app từ main.py)
Khai báo route: Route (tuyến đường) là URL mà client (trình duyệt, frontend, postman, v.v.) gọi đến để lấy dữ liệu hoặc gửi dữ liệu lên server.
FastAPI cho phép bạn khai báo route bằng các decorator như:
Decorator	Mô tả
@app.get()	Nhận yêu cầu GET
@app.post()	Nhận yêu cầu POST
@app.put()	Nhận yêu cầu PUT
@app.delete()	Nhận yêu cầu DELETE

Decorator là cách Python "gắn" một hành vi đặc biệt vào hàm - ở đây là gắn URL vào hàm xử lý.
Ví dụ :
@app.get("/hello")
def hello():
   	 return {"msg": "Xin chào"}
Khi có ai gọi GET /hello, hàm hello() sẽ được thực thi.
Route có Path và Query parameter:
Ví dụ: 
Path param:
@app.get("/items/{item_id}")
def get_item(item_id: int):
    return {"item_id": item_id}	
Query param:
@app.get("/search")
def search(q: str = ""):
    return {"query": q}
Request body: Request Body là phần dữ liệu mà client gửi kèm theo POST/PUT request dưới dạng JSON.
Dữ liệu này sẽ được FastAPI tự động ánh xạ vào một đối tượng Python nếu bạn dùng BaseModel từ Pydantic.
	Ví dụ :
from pydantic import BaseModel

class Item(BaseModel):
 name: str
 price: float
			
	@app.post("/items/")
def create_item(item: Item):
 		return {"name": item.name, "price": item.price}

 Khi client gửi JSON:
{
  "name": "Laptop",
  "price": 1200.5
}
FastAPI sẽ tự parse vào biến item và bạn có thể dùng như đối tượng Python.

Response: Response là dữ liệu mà server trả về cho client. FastAPI tự động:
•	Chuyển Python dict → JSON
•	Trả đúng mã HTTP (status code)
•	Tạo tài liệu Swagger để test
Ví dụ: 
@app.get("/user")
def get_user():
   		 return {"username": "nam", "role": "admin"}
Khi gọi API này, client sẽ nhận về JSON:
{
  "username": "nam",
  "role": "admin"
}
