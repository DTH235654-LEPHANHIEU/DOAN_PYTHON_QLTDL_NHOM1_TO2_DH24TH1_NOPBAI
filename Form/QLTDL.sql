CREATE DATABASE QLTDL
ON
(
    NAME = 'QLTDLd',
    FILENAME = 'D:\CNTT\Năm 3 - Kì 1\Python\DoAn\CSDL\QLTDL_data.mdf',
    SIZE = 8,
    MAXSIZE = 80,
    FILEGROWTH = 5
)
LOG ON
(
    NAME = 'QLTDLl',
    FILENAME = 'D:\CNTT\Năm 3 - Kì 1\Python\DoAn\CSDL\QLTDL_log.ldf',
    SIZE = 8,
    MAXSIZE = 80,
    FILEGROWTH = 5
);

USE QLTDL

-- =============================================
-- 1. Bảng TAIKHOAN (Chỉ lưu thông tin đăng nhập)
-- =============================================
CREATE TABLE TAIKHOAN (
    TenDangNhap VARCHAR(50) UNIQUE NOT NULL,
    MatKhau VARCHAR(255) NOT NULL DEFAULT '123',
);
GO

-- =============================================
-- 2. Bảng KHACHHANG (Thông tin hồ sơ - Profile)
-- =============================================
CREATE TABLE KHACHHANG (
    MaKhachHang INT IDENTITY(1,1) PRIMARY KEY,
    HoTen NVARCHAR(100) NOT NULL,
    NgaySinh DATE,
    GioiTinh NVARCHAR(3),
    SoDienThoai VARCHAR(15) UNIQUE,
    Email VARCHAR(100),
    DiaChi NVARCHAR(255),

);
GO

-- =============================================
-- 3. Bảng TOUR 
-- =============================================

CREATE TABLE TOUR (
    MaTour CHAR(5) PRIMARY KEY,
    TenTour NVARCHAR(255) NOT NULL,
    DiaDiem NVARCHAR(100),         -- Lưu text để search nhanh
    MoTa NVARCHAR(MAX),
    NgayKhoiHanh DATE NOT NULL,
    ThoiLuong INT,                 -- Số ngày (ví dụ: 3 ngày)
    GiaNguoiLon DECIMAL(18,2) NOT NULL,
    GiaTreEm DECIMAL(18,2) DEFAULT 0,
    SoChoToiDa INT NOT NULL,
    SoChoDaDat INT DEFAULT 0
);
GO

-- =============================================
-- 4. Bảng DATCHO (Booking - Lưu trạng thái giữ chỗ)
-- =============================================
CREATE TABLE DATCHO (
    MaDatCho CHAR(5) PRIMARY KEY,
    MaKhachHang INT NOT NULL,
    MaTour CHAR(5) NOT NULL,
    SoLuongNguoiLon INT DEFAULT 1,
    SoLuongTreEm INT DEFAULT 0,
    TongTien DECIMAL(18,2) NOT NULL,
    NgayDat DATETIME DEFAULT GETDATE(),
    TrangThaiBooking NVARCHAR(20) DEFAULT 'Đã đặt',  
);
GO

-- =============================================
-- 5. Bảng THANHTOAN (Giao dịch tiền tệ)
-- =============================================
CREATE TABLE THANHTOAN (
    MaThanhToan CHAR(5) PRIMARY KEY,
    MaDatCho CHAR(5) NOT NULL,
    SoTien DECIMAL(18,2) NOT NULL,
    PhuongThuc NVARCHAR(20) CHECK (PhuongThuc IN (N'Tiền mặt', N'Chuyển khoản')),
    NgayThanhToan DATETIME DEFAULT GETDATE(),
    TrangThaiTT NVARCHAR(20) DEFAULT N'Chưa thanh toán' CHECK(TrangThaiTT IN(N'Đã thanh toán',N'Chưa thanh toán')), 
);
GO

-- 2. Liên kết DATCHO -> KHACHHANG
ALTER TABLE DATCHO
ADD CONSTRAINT FK_DATCHO_KHACHHANG
FOREIGN KEY (MaKhachHang) REFERENCES KHACHHANG(MaKhachHang)
ON DELETE CASCADE; -- Cảnh báo: Xóa khách hàng thì xóa luôn lịch sử đặt vé của họ
GO

-- 3. Liên kết DATCHO -> TOUR
ALTER TABLE DATCHO
ADD CONSTRAINT FK_DATCHO_TOUR
FOREIGN KEY (MaTour) REFERENCES TOUR(MaTour)
ON DELETE CASCADE; -- Cảnh báo: Xóa Tour thì các booking của tour đó cũng mất
GO

-- 4. Liên kết THANHTOAN -> DATCHO
ALTER TABLE THANHTOAN
ADD CONSTRAINT FK_THANHTOAN_DATCHO
FOREIGN KEY (MaDatCho) REFERENCES DATCHO(MaDatCho)
ON DELETE CASCADE; -- Xóa booking thì xóa luôn lịch sử thanh toán
GO


-- =============================================
-- NHẬP DỮ LIỆU (INSERT DATA)
-- =============================================

-- 1. TAIKHOAN
INSERT INTO TAIKHOAN (TenDangNhap) VALUES
('admin'), ('user1'), ('user2'), ('user3'), ('user4'), ('user5');

-- =============================================
-- 1. THÊM DỮ LIỆU BẢNG KHACHHANG
-- =============================================
INSERT INTO KHACHHANG (HoTen, NgaySinh, GioiTinh, SoDienThoai, Email, DiaChi) VALUES
(N'Nguyễn Văn An', '1990-05-15', N'Nam', '0901234567', 'an.nguyen@gmail.com', N'123 Lê Lợi, Q1, TP.HCM'),
(N'Trần Thị Bích', '1995-08-20', N'Nữ', '0912345678', 'bich.tran@yahoo.com', N'45 Hai Bà Trưng, Q3, TP.HCM'),
(N'Lê Minh Cường', '1988-12-10', N'Nam', '0987654321', 'cuong.le@outlook.com', N'12 Nguyễn Trãi, Hà Đông, Hà Nội'),
(N'Phạm Thu Hà', '2000-02-28', N'Nữ', '0933445566', 'ha.pham@gmail.com', N'88 Trần Hưng Đạo, Đà Nẵng'),
(N'Hoàng Văn Nam', '1992-07-07', N'Nam', '0977889900', 'nam.hoang@company.com', N'56 Lý Thường Kiệt, Huế');
GO

-- =============================================
-- 2. THÊM DỮ LIỆU BẢNG TOUR
-- =============================================
INSERT INTO TOUR (MaTour,TenTour, DiaDiem, MoTa, NgayKhoiHanh, ThoiLuong, GiaNguoiLon, GiaTreEm, SoChoToiDa, SoChoDaDat) VALUES
('T001',N'Đà Nẵng - Hội An - Bà Nà Hills', N'Đà Nẵng', N'Khám phá Cầu Rồng, Phố Cổ Hội An và vui chơi tại Bà Nà Hills.', '2023-12-20 07:00:00', 3, 5000000.00, 2500000.00, 30, 0),
('T002',N'Du thuyền Hạ Long 5 Sao', N'Quảng Ninh', N'Ngủ đêm trên vịnh, chèo thuyền Kayak, thăm hang Sửng Sốt.', '2023-12-25 08:00:00', 2, 3500000.00, 1750000.00, 20, 0),
('T003',N'Phú Quốc - Đảo Ngọc Tình Yêu', N'Kiên Giang', N'Lặn ngắm san hô, thăm VinWonders và Safari.', '2024-01-10 09:00:00', 4, 6000000.00, 3000000.00, 25, 0),
('T004',N'Sapa - Chinh phục đỉnh Fansipan - Bản Cát Cát', N'Lào Cai', N'Săn mây trên đỉnh Fansipan, thăm bản làng người H''mông và thưởng thức lẩu cá tầm.', '2024-02-14 06:00:00', 3, 4500000.00, 2250000.00, 25, 0),
('T005',N'Nha Trang - Thiên đường biển đảo - VinWonders', N'Khánh Hòa', N'Du ngoạn 4 đảo, lặn ngắm san hô tại Hòn Mun và vui chơi không giới hạn tại VinWonders.', '2024-03-10 07:30:00', 4, 5500000.00, 2750000.00, 40, 0),
('T006',N'Lục tỉnh Miền Tây: Cần Thơ - Sóc Trăng - Cà Mau', N'Cần Thơ', N'Tham quan Chợ nổi Cái Răng, nhà công tử Bạc Liêu và Đất Mũi Cà Mau cực Nam tổ quốc.', '2024-01-20 05:00:00', 4, 3800000.00, 1900000.00, 30, 0),
('T007',N'Quy Nhơn - Kỳ Co - Eo Gió - Gành Đá Đĩa', N'Bình Định', N'Khám phá Maldives phiên bản Việt Nam, ngắm bình minh tại Eo Gió.', '2024-04-30 08:00:00', 3, 4200000.00, 2100000.00, 35, 0),
('T008',N'Ninh Bình - Tràng An - Bái Đính - Tuyệt Tình Cốc', N'Ninh Bình', N'Du thuyền trên danh thắng Tràng An, chiêm bái chùa Bái Đính lớn nhất Đông Nam Á.', '2024-02-18 07:00:00', 2, 2500000.00, 1250000.00, 45, 0);
GO

-- =============================================
-- 3. THÊM DỮ LIỆU BẢNG DATCHO (Booking)
-- =============================================

INSERT INTO DATCHO (MaKhachHang, MaTour, SoLuongNguoiLon, SoLuongTreEm, TongTien, NgayDat, TrangThaiBooking) VALUES
(1, 'T001', 2, 1, 12500000.00, '2023-12-01 10:00:00', 'Đã đặt'),
(2, 'T005', 1, 0, 3500000.00, '2023-12-05 14:30:00', 'Đã đặt'),
(3, 'T008', 4, 0, 20000000.00, '2023-12-06 09:15:00', 'Đã đặt'),
(4, 'T003', 2, 2, 18000000.00, '2023-12-10 11:00:00', 'Đã hủy'); 
GO

-- =============================================
-- 4. THÊM DỮ LIỆU BẢNG THANHTOAN

INSERT INTO THANHTOAN (MaDatCho, SoTien, PhuongThuc, NgayThanhToan, TrangThaiTT) VALUES
(1, 12500000.00, N'Chuyển khoản', '2023-12-01 10:05:00', N'Đã thanh toán'),
(2, 3500000.00, N'Tiền mặt', '2023-12-05 15:00:00', N'Đã thanh toán'),
(3, 0.00, N'Chuyển khoản', NULL, N'Chưa thanh toán'),
(4, 18000000.00, N'Chuyển khoản', '2023-12-10 11:05:00', N'Đã thanh toán');
GO
-- =============================================
-- BONUS: Cập nhật lại số chỗ đã đặt trong bảng TOUR
-- =============================================
UPDATE t
SET t.SoChoDaDat = (
    SELECT ISNULL(SUM(d.SoLuongNguoiLon + d.SoLuongTreEm), 0)
    FROM DATCHO d
    WHERE d.MaTour = t.MaTour AND d.TrangThaiBooking = 'Đã đặt'
)
FROM TOUR t;
GO


SELECT * FROM THANHTOAN
SELECT * FROM KHACHHANG
SELECT * FROM DATCHO
SELECT * FROM TOUR

SELECT MaTour, TenTour, DiaDiem, MoTa, NgayKhoiHanh, SoChoToiDa, SoChoDaDat, GiaNguoiLon, GiaTreEm, ThoiLuong FROM TOUR

Delete from TOUR where MaTour = 2