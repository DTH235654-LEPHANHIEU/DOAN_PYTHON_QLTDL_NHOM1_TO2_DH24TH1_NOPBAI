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

-- -----------------------------------------------------
-- Bảng 1: TAIKHOAN
-- -----------------------------------------------------
CREATE TABLE TAIKHOAN (
    TenDangNhap VARCHAR(50),
    MatKhau VARCHAR(255) DEFAULT '123',
    CONSTRAINT PK_TAIKHOAN PRIMARY KEY (TenDangNhap)
);

-- -----------------------------------------------------
-- Bảng 2: KHACHHANG
-- -----------------------------------------------------
CREATE TABLE KHACHHANG (
    MaKhachHang CHAR(5),
    HoTen NVARCHAR(100) NOT NULL,
    NgaySinh DATE,
    GioiTinh NVARCHAR(3) CHECK (GioiTinh IN (N'Nam', N'Nữ')),
    SoDienThoai VARCHAR(10) UNIQUE NOT NULL,
    CCCD VARCHAR(12) UNIQUE NOT NULL,
    DiaChi NVARCHAR(255),
    CONSTRAINT PK_KHACHHANG PRIMARY KEY (MaKhachHang)
);

-- -----------------------------------------------------
-- Bảng 3: DIADIEM
-- -----------------------------------------------------
CREATE TABLE DIADIEM (
    MaDiaDiem INT IDENTITY(1,1),
    TenDiaDiem NVARCHAR(255) NOT NULL,
    CONSTRAINT PK_DIADIEM PRIMARY KEY (MaDiaDiem)
);

-- -----------------------------------------------------
-- Bảng 4: DICHVU
-- -----------------------------------------------------
CREATE TABLE DICHVU (
    MaDichVu CHAR(5),
    TenDichVu NVARCHAR(100),
    GiaDichVu DECIMAL(18,2),
    CONSTRAINT PK_DICHVU PRIMARY KEY (MaDichVu)
);

-- -----------------------------------------------------
-- Bảng 5: TUYENDULICH
-- -----------------------------------------------------
CREATE TABLE TUYENDULICH (
    HinhAnh VARBINARY(MAX),
    MaTuyen CHAR(5),
    TenTuyen NVARCHAR(255) NOT NULL,
    MaDiaDiem INT,
    SoNgay INT,
    MoTa NVARCHAR(200),
    NgayDi DATETIME NOT NULL,
    NgayVe DATETIME NOT NULL,
    MaDichVu CHAR(5),
    CONSTRAINT PK_TUYENDULICH PRIMARY KEY (MaTuyen)
);

-- -----------------------------------------------------
-- Bảng 6: CHUYENDI
-- -----------------------------------------------------
CREATE TABLE CHUYENDI (
    MaChuyenDi INT IDENTITY(1,1),
    MaTuyen CHAR(5) NOT NULL,
    GiaNguoiLon DECIMAL(18,2) NOT NULL,
    GiaTreEm DECIMAL(18,2) NOT NULL,
    SoChoToiDa INT NOT NULL,
    SoChoConLai INT NOT NULL,
    CONSTRAINT PK_CHUYENDI PRIMARY KEY (MaChuyenDi)
);

-- =============================================
-- 7. THANHTOAN
-- =============================================
CREATE TABLE THANHTOAN (
    MaThanhToan INT IDENTITY(1,1) PRIMARY KEY,
    MaTuyen CHAR(5) NOT NULL,
    MaDichVu CHAR(5) NOT NULL,
    PhuongThuc NVARCHAR(20) CHECK (PhuongThuc IN (N'Tiền mặt', N'Chuyển khoản')),
    NgayThanhToan DATETIME,
    SoTien DECIMAL(18,2) NOT NULL,
    TrangThaiDat NVARCHAR(50) CHECK (TrangThaiDat IN (N'Thành công', N'Thất bại'))
);

-- =============================================
-- 8. DATCHO
-- =============================================
CREATE TABLE DATCHO (
    MaDatCho INT IDENTITY(1,1) PRIMARY KEY,
    MaKhachHang CHAR(5) NOT NULL,
    MaChuyenDi INT NOT NULL,
    SoLuongNguoiLon INT CHECK (SoLuongNguoiLon >= 0),
    SoLuongTreEm INT CHECK (SoLuongTreEm >= 0),
    TongTien DECIMAL(18,2) NOT NULL,
    NgayDat DATETIME DEFAULT GETDATE(),
    MaThanhToan INT NULL
);
-- -----------------------------------------------------
-- Khóa ngoại (FOREIGN KEY) được khai báo ngoài
-- -----------------------------------------------------
-- TUYENDULICH
ALTER TABLE TUYENDULICH
ADD CONSTRAINT FK_TUYENDULICH_DIADIEM FOREIGN KEY (MaDiaDiem) REFERENCES DIADIEM(MaDiaDiem);

ALTER TABLE TUYENDULICH
ADD CONSTRAINT FK_TUYENDULICH_DICHVU FOREIGN KEY (MaDichVu) REFERENCES DICHVU(MaDichVu);

-- CHUYENDI
ALTER TABLE CHUYENDI
ADD CONSTRAINT FK_CHUYENDI_TUYENDULICH FOREIGN KEY (MaTuyen) REFERENCES TUYENDULICH(MaTuyen);

-- THANHTOAN
ALTER TABLE THANHTOAN
ADD CONSTRAINT FK_THANHTOAN_TUYENDULICH FOREIGN KEY (MaTuyen) REFERENCES TUYENDULICH(MaTuyen);

ALTER TABLE THANHTOAN
ADD CONSTRAINT FK_THANHTOAN_DICHVU FOREIGN KEY (MaDichVu) REFERENCES DICHVU(MaDichVu);

-- DATCHO
ALTER TABLE DATCHO
ADD CONSTRAINT FK_DATCHO_KHACHHANG FOREIGN KEY (MaKhachHang) REFERENCES KHACHHANG(MaKhachHang);

ALTER TABLE DATCHO
ADD CONSTRAINT FK_DATCHO_CHUYENDI FOREIGN KEY (MaChuyenDi) REFERENCES CHUYENDI(MaChuyenDi);

ALTER TABLE DATCHO
ADD CONSTRAINT FK_DATCHO_THANHTOAN FOREIGN KEY (MaThanhToan) REFERENCES THANHTOAN(MaThanhToan);


--Dữ liệu
-- =============================================
-- 1. TAIKHOAN
-- =============================================
INSERT INTO TAIKHOAN (TenDangNhap) VALUES
('admin'),
('user1'),
('user2'),
('user3'),
('user4'),
('user5');

-- =============================================
-- 2. KHACHHANG
-- =============================================
INSERT INTO KHACHHANG (MaKhachHang, HoTen, NgaySinh, GioiTinh, SoDienThoai, CCCD, DiaChi) VALUES
('KH010', N'Nguyễn Minh Hùng', '1985-11-30', N'Nam', '0909000001', '031234567890', N'Quận 1, TP.HCM'),
('KH011', N'Lê Thị Ánh', '1993-06-12', N'Nữ', '0909000002', '031234567891', N'Quận 3, TP.HCM'),
('KH012', N'Huỳnh Văn Bình', '1978-02-20', N'Nam', '0909000003', '031234567892', N'Quận 5, TP.HCM'),
('KH013', N'Phan Thị Ngọc', '2001-08-05', N'Nữ', '0909000004', '031234567893', N'Tp. Thủ Đức, TP.HCM'),
('KH014', N'Đỗ Văn Sơn', '1990-09-15', N'Nam', '0909000005', '031234567894', N'Biên Hòa, Đồng Nai');

-- =============================================
-- 3. DIADIEM
-- =============================================
INSERT INTO DIADIEM (TenDiaDiem) VALUES
(N'Phú Quốc'),
(N'Đà Nẵng'),
(N'Hạ Long'),
(N'Đà Lạt'),
(N'Nha Trang');

-- =============================================
-- 4. DICHVU
-- =============================================
INSERT INTO DICHVU (MaDichVu, TenDichVu, GiaDichVu) VALUES
('DV010', N'Khách sạn 5 sao + Buffet sáng', 12000000),
('DV011', N'Xe Limousine đưa đón', 8000000),
('DV012', N'Vé tham quan trọn gói', 5000000),
('DV013', N'Bảo hiểm du lịch cao cấp', 6500000),
('DV014', N'Hướng dẫn viên riêng', 7000000);

-- =============================================
-- 5. TUYENDULICH
-- =============================================
INSERT INTO TUYENDULICH (HinhAnh, MaTuyen, TenTuyen, MaDiaDiem, SoNgay, MoTa, NgayDi, NgayVe, MaDichVu) VALUES
(NULL, 'T010', N'Tour Phú Quốc - Đảo Ngọc', 1, 4, N'Nghỉ dưỡng resort, tham quan Hòn Thơm & VinWonders', '2025-12-20', '2025-12-23', 'DV010'),
(NULL, 'T011', N'Tour Đà Nẵng - Hội An', 2, 3, N'Khám phá Bà Nà Hills và Phố cổ Hội An', '2025-11-05', '2025-11-07', 'DV011'),
(NULL, 'T012', N'Tour Du thuyền Hạ Long', 3, 2, N'Ngủ đêm trên vịnh, chèo Kayak', '2025-10-15', '2025-10-16', 'DV012'),
(NULL, 'T013', N'Tour Đà Lạt Săn Mây', 4, 3, N'Cắm trại, săn mây Cầu Đất, Lang Biang', '2025-09-18', '2025-09-20', 'DV013'),
(NULL, 'T014', N'Tour Nha Trang Biển Đảo', 5, 5, N'Lặn ngắm san hô, tắm bùn khoáng', '2025-08-22', '2025-08-26', 'DV014');

-- =============================================
-- 6. CHUYENDI
-- =============================================
INSERT INTO CHUYENDI (MaTuyen, GiaNguoiLon, GiaTreEm, SoChoToiDa, SoChoConLai) VALUES
('T010', 12000000, 7000000, 30, 27),
('T011', 8000000, 4500000, 40, 39),
('T012', 5000000, 3000000, 20, 16),
('T013', 6500000, 3800000, 25, 23),
('T014', 7000000, 4000000, 35, 32);

-- =============================================
-- 7. THANHTOAN
-- =============================================
INSERT INTO THANHTOAN (MaTuyen, MaDichVu, PhuongThuc, NgayThanhToan, SoTien, TrangThaiDat) VALUES
('T010', 'DV010', N'Chuyển khoản', '2025-12-01', 15000000, N'Đã thanh toán'),
('T011', 'DV011', N'Tiền mặt', '2025-10-25', 8000000, N'Đã thanh toán'),
('T012', 'DV012', N'Chuyển khoản', '2025-10-02', 16000000, N'Đã thanh toán'),
('T013', 'DV013', N'Chuyển khoản', '2025-09-10', 10300000, N'Đã thanh toán'),
('T014', 'DV014', N'Tiền mặt', NULL, 0, N'Chưa thanh toán');

-- =============================================
-- 8. DATCHO
-- =============================================
INSERT INTO DATCHO (MaKhachHang, MaChuyenDi, SoLuongNguoiLon, SoLuongTreEm, TongTien, MaThanhToan) VALUES
('KH010', 1, 2, 1, 31000000, 1),
('KH011', 2, 1, 2, 17000000, 2),
('KH012', 3, 2, 0, 10000000, 3),
('KH013', 4, 1, 1, 14100000, 4),
('KH014', 5, 3, 1, 25000000, 5);


SELECT * FROM TUYENDULICH
SELECT * FROM DIADIEM
SELECT * FROM DICHVU
SELECT * FROM CHUYENDI
SELECT * FROM THANHTOAN

SELECT tdl.MaTuyen, TenTuyen, TenDiaDiem, MoTa, NgayDi, NgayVe, TenDichVu, SoChoToiDa, SoChoConLai, GiaNguoiLon, GiaTreEm 
FROM TUYENDULICH tdl, DIADIEM dd, DICHVU dv, CHUYENDI cd
WHERE dd.MaDiaDiem = tdl.MaDiaDiem 
      AND dv.MaDichVu = tdl.MaDichVu
      AND cd.MaTuyen = tdl.MaTuyen
      