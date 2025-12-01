CREATE DATABASE QLTDL
ON
(
    NAME = 'QLTDL_data',
    FILENAME = 'D:\CNTT\Năm 3 - Kì 1\Python\DoAn\CSDL\QLTDL_data.mdf',
    SIZE = 10MB,
    MAXSIZE = 100MB,
    FILEGROWTH = 5MB
)
LOG ON
(
    NAME = 'QLTDL_log',
    FILENAME = 'D:\CNTT\Năm 3 - Kì 1\Python\DoAn\CSDL\QLTDL_log.ldf',
    SIZE = 5MB,
    MAXSIZE = 50MB,
    FILEGROWTH = 2MB
);
GO

USE QLTDL;
GO

-- =============================================
-- 1. Bảng TAIKHOAN
-- =============================================
CREATE TABLE TAIKHOAN (
    TenDangNhap VARCHAR(50) PRIMARY KEY,
    MatKhau VARCHAR(255) NOT NULL DEFAULT '123',
);
GO

-- =============================================
-- 2. Bảng NHANVIEN
-- =============================================
CREATE TABLE NHANVIEN (
    MaNhanVien CHAR(5) PRIMARY KEY,
    HoTen NVARCHAR(100) NOT NULL,
    NgaySinh DATE,
    GioiTinh NVARCHAR(3) CHECK (GioiTinh IN (N'Nam', N'Nữ')),
    SoDienThoai VARCHAR(15) UNIQUE,
    Email VARCHAR(100) UNIQUE,
    ChucVu NVARCHAR(50) CHECK (ChucVu IN (N'Hướng dẫn viên', N'Tư vấn viên')),
    NgayVaoLam DATE DEFAULT GETDATE(),
    DiaChi NVARCHAR(255)
);
GO

-- =============================================
-- 3. Bảng KHACHHANG
-- =============================================
CREATE TABLE KHACHHANG (
    MaKhachHang CHAR(5) PRIMARY KEY,
    HoTen NVARCHAR(100) NOT NULL,
    NgaySinh DATE,
    CCCD CHAR(12) UNIQUE,
    GioiTinh NVARCHAR(3) CHECK (GioiTinh IN (N'Nam', N'Nữ')),
    SoDienThoai CHAR(10) UNIQUE,
    Email VARCHAR(100),
    DiaChi NVARCHAR(255),
    SoTourDaDat INT DEFAULT 0
);
GO

-- =============================================
-- 4. Bảng TOUR
-- =============================================
CREATE TABLE TOUR (
    MaTour CHAR(5) PRIMARY KEY,
    TenTour NVARCHAR(255) NOT NULL,
    DiaDiem NVARCHAR(100),
    MoTa NVARCHAR(MAX),
    NgayKhoiHanh DATE NOT NULL,
    ThoiLuong INT CHECK (ThoiLuong > 0),
    GiaNguoiLon DECIMAL(18,2) NOT NULL CHECK (GiaNguoiLon > 0),
    GiaTreEm DECIMAL(18,2) DEFAULT 0 CHECK (GiaTreEm >= 0),
    SoChoToiDa INT NOT NULL CHECK (SoChoToiDa > 0),
    SoChoDaDat INT DEFAULT 0 CHECK (SoChoDaDat >= 0),
);
GO

-- =============================================
-- 5. Bảng DATCHO
-- =============================================
CREATE TABLE DATCHO (
    MaDatCho CHAR(5) PRIMARY KEY,
    MaKhachHang CHAR(5) NOT NULL,
    MaNhanVien CHAR(5) NOT NULL,
    MaTour CHAR(5) NOT NULL,
    SoLuongNguoiLon INT DEFAULT 1 CHECK (SoLuongNguoiLon >= 0),
    SoLuongTreEm INT DEFAULT 0 CHECK (SoLuongTreEm >= 0),
    TongTien DECIMAL(18,2) DEFAULT 0 CHECK (TongTien >= 0),
    NgayDat DATETIME DEFAULT GETDATE(),
    TrangThaiBooking NVARCHAR(20) DEFAULT N'Chưa đặt' 
        CHECK (TrangThaiBooking IN (N'Đã đặt', N'Chưa đặt'))
);
GO

-- =============================================
-- 6. Bảng THANHTOAN
-- =============================================
CREATE TABLE THANHTOAN (
    MaThanhToan CHAR(5) PRIMARY KEY,
    MaDatCho CHAR(5) NOT NULL,
    SoTien DECIMAL(18,2) NOT NULL CHECK (SoTien >= 0),
    PhuongThuc NVARCHAR(20) CHECK (PhuongThuc IN (N'Tiền mặt', N'Chuyển khoản')),
    NgayThanhToan DATETIME,
    TrangThaiTT NVARCHAR(20) DEFAULT N'Chưa thanh toán' 
        CHECK (TrangThaiTT IN (N'Đã thanh toán', N'Chưa thanh toán'))
);
GO

-- =============================================
-- RÀNG BUỘC KHÓA NGOẠI
-- =============================================
ALTER TABLE DATCHO
ADD CONSTRAINT FK_DATCHO_KHACHHANG FOREIGN KEY (MaKhachHang) REFERENCES KHACHHANG(MaKhachHang) ON DELETE CASCADE;
GO

ALTER TABLE DATCHO
ADD CONSTRAINT FK_DATCHO_NHANVIEN FOREIGN KEY (MaNhanVien) REFERENCES NHANVIEN(MaNhanVien);
GO

ALTER TABLE DATCHO
ADD CONSTRAINT FK_DATCHO_TOUR FOREIGN KEY (MaTour) REFERENCES TOUR(MaTour) ON DELETE CASCADE;
GO

ALTER TABLE THANHTOAN
ADD CONSTRAINT FK_THANHTOAN_DATCHO FOREIGN KEY (MaDatCho) REFERENCES DATCHO(MaDatCho) ON DELETE CASCADE;
GO

-- =============================================
-- TRIGGER 1: CẬP NHẬT SoChoDaDat TRONG TOUR
-- =============================================
CREATE TRIGGER TRG_UpdateSoChoDaDat
ON DATCHO
AFTER INSERT, UPDATE, DELETE
AS
BEGIN
    UPDATE TOUR 
    SET SoChoDaDat = (
        SELECT ISNULL(SUM(SoLuongNguoiLon + SoLuongTreEm), 0)
        FROM DATCHO 
        WHERE MaTour = TOUR.MaTour AND TrangThaiBooking = N'Đã đặt'
    )
    WHERE MaTour IN (
        SELECT DISTINCT MaTour FROM inserted
        UNION
        SELECT DISTINCT MaTour FROM deleted
    );
END;
GO

-- =============================================
-- TRIGGER 2: CẬP NHẬT SoTourDaDat TRONG KHACHHANG
-- =============================================
CREATE TRIGGER TRG_UpdateSoTourDaDat
ON DATCHO
AFTER INSERT, UPDATE, DELETE
AS
BEGIN
    UPDATE KHACHHANG 
    SET SoTourDaDat = (
        SELECT COUNT(*)
        FROM DATCHO
        WHERE MaKhachHang = KHACHHANG.MaKhachHang AND TrangThaiBooking = N'Đã đặt'
    )
    WHERE MaKhachHang IN (
        SELECT DISTINCT MaKhachHang FROM inserted
        UNION
        SELECT DISTINCT MaKhachHang FROM deleted
    );
END;
GO

CREATE TRIGGER TRG_AutoCreateThanhToan
ON DATCHO
AFTER INSERT
AS
BEGIN
    -- Tạo mã thanh toán mới TTxxx
    DECLARE @NewTT CHAR(5);

    SELECT @NewTT = 
        'TT' + RIGHT('000' + CAST(
            (SELECT ISNULL(MAX(CAST(SUBSTRING(MaThanhToan, 3, 3) AS INT)), 0) + 1 FROM THANHTOAN)
        AS VARCHAR(3)), 3);

    -- Thêm hóa đơn mới tương ứng đơn đặt chỗ
    INSERT INTO THANHTOAN (MaThanhToan, MaDatCho, SoTien, PhuongThuc, NgayThanhToan, TrangThaiTT)
    SELECT 
        @NewTT, 
        i.MaDatCho,
        0,                -- chưa thanh toán
        NULL,             -- chưa có phương thức
        NULL,             -- chưa thanh toán
        N'Chưa thanh toán'
    FROM inserted i;
END;
GO

CREATE TRIGGER TRG_TinhTongTien
ON DATCHO
AFTER INSERT, UPDATE
AS
BEGIN
    UPDATE DATCHO
    SET TongTien = (
        SELECT (i.SoLuongNguoiLon * t.GiaNguoiLon) + (i.SoLuongTreEm * t.GiaTreEm)
        FROM inserted i
        INNER JOIN TOUR t ON i.MaTour = t.MaTour
        WHERE DATCHO.MaDatCho = i.MaDatCho
    )
    WHERE MaDatCho IN (SELECT MaDatCho FROM inserted);
END;
GO

CREATE TRIGGER trg_Auto_MaDatCho
ON DATCHO
INSTEAD OF INSERT
AS
BEGIN
    DECLARE @inputMa CHAR(5);

    -- Lấy mã đặt chỗ từ bản ghi được INSERT
    SELECT @inputMa = MaDatCho FROM inserted;

    IF (@inputMa IS NULL OR LTRIM(RTRIM(@inputMa)) = '')
    BEGIN
        -- === TRƯỜNG HỢP: KHÔNG NHẬP MÃ → TỰ SINH ===

        DECLARE @lastMa CHAR(5);

        -- Lấy mã lớn nhất hiện có
        SELECT TOP 1 @lastMa = MaDatCho
        FROM DATCHO
        ORDER BY MaDatCho DESC;

        -- Nếu chưa có dữ liệu
        IF (@lastMa IS NULL)
            SET @lastMa = 'DC000';

        -- Tăng số
        DECLARE @num INT = CAST(SUBSTRING(@lastMa, 3, 3) AS INT) + 1;

        -- Tạo mã mới
        SET @inputMa = 'DC' + RIGHT('000' + CAST(@num AS VARCHAR(3)), 3);
    END

    -- === CHÈN DỮ LIỆU (DÙNG MÃ NHẬP HOẶC MÃ TỰ SINH) ===
    INSERT INTO DATCHO
    (MaDatCho, MaKhachHang, MaNhanVien, MaTour,
     SoLuongNguoiLon, SoLuongTreEm, TongTien, NgayDat, TrangThaiBooking)
    SELECT
        @inputMa,
        MaKhachHang,
        MaNhanVien,
        MaTour,
        SoLuongNguoiLon,
        SoLuongTreEm,
        TongTien,
        NgayDat,
        TrangThaiBooking
    FROM inserted;
END;
GO
-- =============================================
-- 1. THÊM TAIKHOAN
-- =============================================
INSERT INTO TAIKHOAN (TenDangNhap) VALUES
('nv004'), ('nv005'), ('nv006'), ('nv007'), ('nv008'),
('KH005'),('KH006'),('KH007'),('KH008'),('KH009'),('KH010'),('KH011'),('KH012');
GO
INSERT INTO TAIKHOAN (TenDangNhap) VALUES
('admin');
GO
-- =============================================
-- 2. THÊM NHANVIEN (5 nhân viên mới)
-- =============================================
INSERT INTO NHANVIEN VALUES
('NV004', N'Phạm Văn Tuấn', '1992-05-12', N'Nam', '0933344556', 'tuan@company.com', N'Tư vấn viên', '2023-01-10', N'88 Trần Hưng Đạo, Đà Nẵng'),
('NV005', N'Hoàng Thị Ngọc', '1987-09-25', N'Nữ', '0944455667', 'ngoc@company.com', N'Hướng dẫn viên', '2021-08-01', N'56 Lý Thường Kiệt, Huế'),
('NV006', N'Vũ Minh Đức', '1989-02-18', N'Nam', '0955566778', 'duc@company.com', N'Tư vấn viên', '2020-06-15', N'200 Nguyễn Văn Cừ, Q5'),
('NV007', N'Nguyễn Hồng Phúc', '1991-12-03', N'Nam', '0966677889', 'phuc@company.com', N'Hướng dẫn viên', '2022-09-10', N'300 Phạm Văn Đồng, Gò Vấp'),
('NV008', N'Trần Thị Kim', '1993-07-30', N'Nữ', '0977788990', 'kim@company.com', N'Tư vấn viên', '2023-03-05', N'400 Trường Chinh, Tân Bình');
GO

-- =============================================
-- 3. THÊM KHACHHANG (8 khách hàng mới)
-- =============================================
INSERT INTO KHACHHANG (
    MaKhachHang, HoTen, NgaySinh, CCCD, GioiTinh, 
    SoDienThoai, Email, DiaChi, SoTourDaDat
) VALUES
('KH005', N'Hoàng Văn Nam', '1992-07-07', '031234567890', N'Nam', '0977889900', 'nam.hoang@company.com', N'56 Lý Thường Kiệt, Huế', 0),
('KH006', N'Vũ Thị Lan', '1989-11-11', '031234567891', N'Nữ', '0966778899', 'lan.vu@gmail.com', N'200 Nguyễn Văn Cừ, Q5', 0),
('KH007', N'Đặng Quốc Bảo', '1993-04-22', '031234567892', N'Nam', '0955667788', 'bao.dang@yahoo.com', N'300 Phạm Văn Đồng, Gò Vấp', 0),
('KH008', N'Ngô Thị Thu', '1991-10-05', '031234567893', N'Nữ', '0944778899', 'thu.ngo@outlook.com', N'400 Trường Chinh, Tân Bình', 0),
('KH009', N'Lý Văn Hùng', '1986-08-14', '031234567894', N'Nam', '0928899001', 'hung.ly@gmail.com', N'500 Cách Mạng Tháng 8, Q3', 0),
('KH010', N'Mai Thị Hồng', '1994-03-27', '031234567895', N'Nữ', '0939900112', 'hong.mai@yahoo.com', N'600 Lê Văn Việt, Q9', 0),
('KH011', N'Phan Văn Long', '1984-12-01', '031234567896', N'Nam', '0940011223', 'long.phan@outlook.com', N'700 Huỳnh Tấn Phát, Q7', 0),
('KH012', N'Tạ Thị Dung', '1990-06-19', '031234567897', N'Nữ', '0951122334', 'dung.ta@gmail.com', N'800 Nguyễn Thị Minh Khai, Q3', 0);
GO


-- =============================================
-- 4. THÊM TOUR (10 tour mới)
-- =============================================
INSERT INTO TOUR VALUES
('T004', N'Sapa - Fansipan - Bản Cát Cát', N'Lào Cai', N'Săn mây Fansipan, thăm bản H''mông, lẩu cá tầm', '2025-12-28', 3, 4500000, 2250000, 25, 0),
('T005', N'Nha Trang - VinWonders - 4 đảo', N'Khánh Hòa', N'Lặn Hòn Mun, vui chơi VinWonders không giới hạn', '2026-01-15', 4, 5500000, 2750000, 40, 0),
('T006', N'Miền Tây - Chợ nổi Cái Răng', N'Cần Thơ', N'Chợ nổi, nhà Công tử Bạc Liêu, Đất Mũi Cà Mau', '2025-12-18', 4, 3800000, 1900000, 30, 0),
('T007', N'Quy Nhơn - Eo Gió - Kỳ Co', N'Bình Định', N'Maldives Việt Nam, Gành Đá Đĩa, Eo Gió', '2026-02-01', 3, 4200000, 2100000, 35, 0),
('T008', N'Ninh Bình - Tràng An - Bái Đính', N'Ninh Bình', N'Du thuyền Tràng An, chùa Bái Đính lớn nhất Đông Nam Á', '2025-12-22', 2, 2500000, 1250000, 45, 0),
('T009', N'Đà Lạt - Thác Datanla - Langbiang', N'Lâm Đồng', N'Thành phố ngàn hoa, săn mây Langbiang', '2026-01-20', 3, 3200000, 1600000, 30, 0),
('T010', N'Huế - Phong Nha - Kẻ Bàng', N'Thừa Thiên Huế', N'Đại Nội Huế, hang Sơn Đoòng, Phong Nha', '2026-02-10', 4, 4800000, 2400000, 25, 0),
('T011', N'Vũng Tàu - Hồ Mây - Suối nước nóng', N'Bà Rịa Vũng Tàu', N'Nghỉ dưỡng cuối tuần gần Sài Gòn', '2025-12-15', 2, 1800000, 900000, 50, 0),
('T012', N'Đồng Hới - Nhật Lệ - Bảo Ninh', N'Quảng Bình', N'Biển Nhật Lệ, Cồn Cát Quang Phú', '2026-01-05', 3, 2800000, 1400000, 35, 0),
('T013', N'Pleiku - Biển Hồ - Chè Tám Tạng', N'Gia Lai', N'Tây Nguyên huyền bí, ruộng bậc thang', '2026-02-15', 4, 4100000, 2050000, 28, 0);
GO

-- =============================================
-- 5. THÊM DATCHO (15 booking mới)
-- =============================================
INSERT INTO DATCHO (MaDatCho, MaKhachHang, MaNhanVien, MaTour, SoLuongNguoiLon, SoLuongTreEm, NgayDat, TrangThaiBooking)VALUES
('DC005', 'KH005', 'NV004', 'T005', 1, 1, '2025-11-25 15:30', N'Đã đặt'),
('DC006', 'KH006', 'NV005', 'T006', 4, 0, '2025-11-26 08:45', N'Đã đặt'),
('DC009', 'KH008', 'NV007', 'T007', 3, 1, '2025-11-28 16:00', N'Đã đặt'),
('DC013', 'KH009', 'NV006', 'T011', 3, 2, '2025-11-29 14:00', N'Đã đặt'),
('DC014', 'KH010', 'NV007', 'T012', 1, 0, '2025-11-29 16:30', N'Đã đặt'),
('DC015', 'KH011', 'NV008', 'T013', 2, 1, '2025-11-30 10:00', N'Đã đặt'),
('DC018', 'KH006', 'NV004', 'T006', 1, 0, '2025-12-01 14:15', N'Chưa đặt'),
('DC019', 'KH007', 'NV005', 'T008', 5, 0, '2025-12-02 11:00', N'Đã đặt');
GO
INSERT INTO DATCHO (MaDatCho, MaKhachHang, MaNhanVien, MaTour, SoLuongNguoiLon, SoLuongTreEm, NgayDat, TrangThaiBooking)VALUES
('DC020', 'KH005', 'NV004', 'T005', 1, 1, '2025-11-25 15:30', N'Đã đặt')
-- =============================================
-- 6. THÊM THANHTOAN (15 thanh toán mới)
-- =============================================
INSERT INTO THANHTOAN VALUES
('TT005', 'DC005', 8250000, N'Tiền mặt', '2025-11-25 16:00', N'Đã thanh toán'),
('TT006', 'DC006', 15200000, N'Chuyển khoản', '2025-11-26 09:30', N'Đã thanh toán'),
('TT009', 'DC009', 14700000, N'Chuyển khoản', NULL, N'Chưa thanh toán'),
('TT013', 'DC013', 7200000, N'Chuyển khoản', '2025-11-29 14:15', N'Đã thanh toán'),
('TT014', 'DC014', 2800000, N'Tiền mặt', '2025-11-29 17:00', N'Đã thanh toán'),
('TT015', 'DC015', 10250000, N'Chuyển khoản', NULL, N'Chưa thanh toán'),
('TT018', 'DC018', 0, N'Tiền mặt', NULL, N'Chưa thanh toán'),
('TT019', 'DC019', 12500000, N'Chuyển khoản', '2025-12-02 11:30', N'Đã thanh toán');
GO



Select * from NHANVIEN
Select * from TOur
Select * from DATCHO
Select * from THANHTOAN
Select * from KHACHHANG
Select * from TAIKHOAN
 --Kiem tra ngay dat tour neu ngay dat tour > ngay khoi hanh -- kh xoa tour
 --Kiem tra ngay dat tour neu ngay dat tour < ngay khoi hanh --  xoa tour
INSERT INTO TOUR VALUES
('T015', N'Sapa - Fansipan - Bản Cát Cát', N'Lào Cai', N'Săn mây Fansipan, thăm bản H''mông, lẩu cá tầm', '2025-12-28', 3, 4500000, 2250000, 25, 0)

update TOUR set TenTour = 'Hieu'
where MaTour = 'T005'

SELECT MaTour, TenTour, DiaDiem, MoTa, NgayKhoiHanh,SoChoToiDa, SoChoDaDat, GiaNguoiLon, GiaTreEm, ThoiLuong
FROM TOUR
WHERE MaTour = 'T005'

        SELECT MaTour, TenTour, DiaDiem, MoTa, NgayKhoiHanh,
               SoChoToiDa, SoChoDaDat, GiaNguoiLon, GiaTreEm, ThoiLuong
        FROM TOUR
        WHERE MaTour IN (
            SELECT MaTour
            FROM DATCHO
            WHERE MaKhachHang = 'KH005')

SELECT 
    TT.MaThanhToan,
    TT.MaDatCho,
    T.TenTour,
    TT.SoTien,
    TT.PhuongThuc,
    TT.NgayThanhToan,
    TT.TrangThaiTT
FROM THANHTOAN TT
JOIN DATCHO DC ON TT.MaDatCho = DC.MaDatCho
JOIN TOUR T ON DC.MaTour = T.MaTour
WHERE DC.MaKhachHang = 'KH005'
ORDER BY TT.NgayThanhToan DESC;