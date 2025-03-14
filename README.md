# Thi giữa kỳ phát triển ứng dụng
# 22684181 - 55 - Phan Tấn Tài

# Task Management System

Xây dựng một ứng dụng quản lý công việc (task), tình trạng hoàn thành (status) và thời gian tạo (created), thời gian hoàn thành (finished) với hai tác nhân (admin, user) với các chức năng sau:

1) Cho phép user có thể upload avatar (hình đại diện)

2) Frontend có layout là Card-Based (Dạng Thẻ)

3) chức năng quản lý phân loại công việc (category) để người dùng có thể dễ theo dõi.
 

## Features

### User Features
- Đăng ký và xác thực người dùng
- Tạo và quản lý nhiệm vụ
- Phân loại nhiệm vụ
- Theo dõi trạng thái nhiệm vụ (đang chờ xử lý, đang tiến hành, đã hoàn thành)
- Quản lý hồ sơ với tải lên Avatar
- Lọc tác vụ theo danh mục

### Admin Features
- Quản lý người dùng
- Đặt lại mật khẩu cho người dùng
- Chức năng cấm người dùng/Unban
- Xem tất cả người dùng và trạng thái của họ

## Technologies Used
- Python 3.10+
- Flask
- SQLAlchemy
- Flask-Login
- SQLite
- Bootstrap 5

## Installation

1. Clone dự án:
```bash
git clone https://github.com/tontide1/ptud-gk-de-2.git
cd ptud-gk-de-2
```
2. Tạo virtual environment:

- Bạn nên tạo môi trường ảo với ***python 3.10.11*** để phù hợp với phiên bản mà tôi đã sử dụng khi xây dựng dự án này
```bash
python -m venv venv
venv\Scripts\activate.ps1
```
3. Cài đặt thư viện:
```bash
pip install -r requirements.txt
```
4. Chạy ứng dụng:
```bash
python app.py
```
5. Tạo tài khoản admin:
   - Lưu ý: nên chạy ứng dụng trước để đảm bảo database được khởi tạo. Sau đó hãy tạo tài khoản admin sau
```bash
python create_admin.py
```
6. Truy cập ứng dụng:
```bash
localhost:5000
```

### Tài khoản Admin mặc định : admin - admin123
