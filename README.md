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

- Dự án này tôi sử dụng miniconda để tạo biến môi trường ảo.

- Nếu bạn chưa có miniconda, hãy mở Windows Powershell chạy lệnh sau để cài đặt:
```bash
winget install -e --id Anaconda.Miniconda3
```
- Sau khi đã cài đặt miniconda, bạn chỉ cần mở $CMD$ chạy script $install.bat$ để tạo môi trường ảo và cài đặt các thư viện cần thiết để chạy ứng dụng:

```bash
install.bat
```
## Tài khoản Admin mặc định : admin - admin123
