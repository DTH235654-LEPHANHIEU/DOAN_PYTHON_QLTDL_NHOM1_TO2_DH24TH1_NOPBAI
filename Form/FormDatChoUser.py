from customtkinter import *
from tkinter import messagebox
from Form import BaseForm

class Create_DatCho(CTkToplevel):
    def __init__(self, master=None, ma_tour=None, ten_chuyendi=None, ten_diadiem=None, 
                 mota=None, ngay_khoihanh=None, so_chotoi_da=None, so_cho_da_dat=None, 
                 gia_nguoi_lon=None, gia_tre_em=None):
        super().__init__(master)
        
        self.ma_tour = ma_tour
        self.gia_nguoi_lon = float(gia_nguoi_lon) if gia_nguoi_lon else 0
        self.gia_tre_em = float(gia_tre_em) if gia_tre_em else 0

        self.title("ĐẶT TOUR")
        self.geometry("500x650")
        self.resizable(False, False)
        
        self.Create_frameTop()
        self.Create_FrameBottom(ma_tour, ten_chuyendi, ten_diadiem, mota, ngay_khoihanh, 
                               so_chotoi_da, so_cho_da_dat, gia_nguoi_lon, gia_tre_em)

    def Create_frameTop(self):
        self.frameTop = CTkFrame(self, height=100, fg_color="#242861")
        self.frameTop.pack(side="top", fill="x")
        
        self.lb_TieuDe = CTkLabel(self.frameTop, text="ĐẶT CHUYẾN ĐI", height=40, 
                                  text_color="#ffffff", font=("Segoe UI", 23, "bold"))
        self.lb_TieuDe.pack(pady=20, anchor="center")

    def Create_FrameBottom(self, ma_tour, ten_chuyendi, ten_diadiem, mota, ngay_khoihanh, 
                          so_chotoi_da, so_cho_da_dat, gia_nguoi_lon, gia_tre_em):
        self.frameBottom = CTkFrame(self, height=360)
        self.frameBottom.pack(side="bottom", fill="both", expand=True)
        
        # Thông tin chuyến đi
        CTkLabel(self.frameBottom, text="Thông tin chuyến đi", 
                font=("Segoe UI", 17, "bold")).pack(pady=15)
        CTkLabel(self.frameBottom, text=f"Mã tour: {ma_tour}", 
                font=("Segoe UI", 14)).pack(padx=10, pady=3, anchor="w")
        CTkLabel(self.frameBottom, text=f"Tên chuyến: {ten_chuyendi}", 
                font=("Segoe UI", 14)).pack(padx=10, pady=3, anchor="w")
        CTkLabel(self.frameBottom, text=f"Tên địa điểm: {ten_diadiem}", 
                font=("Segoe UI", 14)).pack(padx=10, pady=3, anchor="w")
        CTkLabel(self.frameBottom, text=f"Mô tả: {mota}", 
                font=("Segoe UI", 14)).pack(padx=10, pady=3, anchor="w")
        CTkLabel(self.frameBottom, text=f"Ngày khởi hành: {ngay_khoihanh}", 
                font=("Segoe UI", 14)).pack(padx=10, pady=3, anchor="w")
        CTkLabel(self.frameBottom, text=f"Chỗ tối đa: {so_chotoi_da}", 
                font=("Segoe UI", 14)).pack(padx=10, pady=3, anchor="w")
        CTkLabel(self.frameBottom, text=f"Chỗ đã đặt: {so_cho_da_dat}", 
                font=("Segoe UI", 14)).pack(padx=10, pady=3, anchor="w")
        CTkLabel(self.frameBottom, text=f"Giá người lớn: {gia_nguoi_lon} VNĐ", 
                font=("Segoe UI", 14)).pack(padx=10, pady=3, anchor="w")
        CTkLabel(self.frameBottom, text=f"Giá trẻ em: {gia_tre_em} VNĐ", 
                font=("Segoe UI", 14)).pack(padx=10, pady=3, anchor="w")
        
        # Số lượng người lớn
        self.lb_SoNguoiLon = CTkLabel(self.frameBottom, text="Số lượng người lớn:", 
                                     font=("Segoe UI", 14, "bold"))        
        self.lb_SoNguoiLon.pack(padx=10, pady=3, anchor="w")
        self.entry_NguoiLon = CTkEntry(self.frameBottom, width=60, height=25)
        self.entry_NguoiLon.place(x=180, y=345)
        self.entry_NguoiLon.insert(0, "0")
        self.entry_NguoiLon.bind("<KeyRelease>", self.TinhTongTien)
        
        # Số lượng trẻ em
        self.lb_SoNguoiTreEm = CTkLabel(self.frameBottom, text="Số lượng trẻ em:", 
                                       font=("Segoe UI", 14, "bold"))        
        self.lb_SoNguoiTreEm.pack(padx=10, pady=3, anchor="w")
        self.entry_TreEm = CTkEntry(self.frameBottom, width=60, height=25)
        self.entry_TreEm.place(x=180, y=375)
        self.entry_TreEm.insert(0, "0")
        self.entry_TreEm.bind("<KeyRelease>", self.TinhTongTien)
        
        # Tổng tiền
        self.lb_TongTien = CTkLabel(self.frameBottom, text="Tổng tiền:", 
                                    font=("Segoe UI", 14, "bold"))        
        self.lb_TongTien.pack(padx=10, pady=3, anchor="w")
        self.entry_TongTien = CTkEntry(self.frameBottom, width=200, height=25, 
                                       fg_color="#787583", text_color="#FFFFFF")
        self.entry_TongTien.place(x=180, y=405)        
        self.entry_TongTien.insert(0, "0 VNĐ")
        self.entry_TongTien.configure(state="disabled")
        
        # Buttons
        self.btn_XacNhan = CTkButton(self.frameBottom, width=110, height=30, text="Xác nhận", 
                                     fg_color="#242861", font=("Segoe UI", 14, "bold"), 
                                     command=self.DatCho)
        self.btn_XacNhan.place(x=120, y=460)
        
        self.btn_Huy = CTkButton(self.frameBottom, width=110, height=30, text="Hủy",
                                 fg_color="#8D1313", font=("Segoe UI", 14, "bold"), 
                                 command=self.destroy)
        self.btn_Huy.place(x=270, y=460)

    def TinhTongTien(self, event=None):
        """Tính tổng tiền khi người dùng nhập số lượng"""
        try:
            so_nguoi_lon = int(self.entry_NguoiLon.get().strip()) if self.entry_NguoiLon.get().strip() else 0
            so_tre_em = int(self.entry_TreEm.get().strip()) if self.entry_TreEm.get().strip() else 0
            
            tong_tien = (so_nguoi_lon * self.gia_nguoi_lon) + (so_tre_em * self.gia_tre_em)
            
            self.entry_TongTien.configure(state="normal")
            self.entry_TongTien.delete(0, 'end')
            self.entry_TongTien.insert(0, f"{tong_tien:,.0f} VNĐ")
            self.entry_TongTien.configure(state="disabled")
        except ValueError:
            self.entry_TongTien.configure(state="normal")
            self.entry_TongTien.delete(0, 'end')
            self.entry_TongTien.insert(0, "0 VNĐ")
            self.entry_TongTien.configure(state="disabled")

    def DatCho(self):
        """Xử lý đặt chỗ tour"""
        try:
            # Lấy số lượng
            so_nguoi_lon_text = self.entry_NguoiLon.get().strip()
            so_tre_em_text = self.entry_TreEm.get().strip()
            
            if not so_nguoi_lon_text or not so_tre_em_text:
                messagebox.showwarning("Cảnh báo", "Vui lòng nhập đầy đủ số lượng!")
                return
            
            so_nguoi_lon = int(so_nguoi_lon_text)
            so_tre_em = int(so_tre_em_text)
            
            # Kiểm tra số lượng hợp lệ
            if so_nguoi_lon < 0 or so_tre_em < 0:
                messagebox.showwarning("Cảnh báo", "Số lượng phải là số dương!")
                return
            
            if so_nguoi_lon == 0 and so_tre_em == 0:
                messagebox.showwarning("Cảnh báo", "Phải đặt ít nhất 1 người!")
                return
            
            # Kết nối database
            db = BaseForm.ConnectionDatabase()
            cursor = db.conn.cursor()
            
            # Thêm vào database
            sql = """
                INSERT INTO DATCHO (MaKhachHang, MaNhanVien, MaTour, 
                                  SoLuongNguoiLon, SoLuongTreEm)
                VALUES (?, ?, ?, ?, ?)
            """
            cursor.execute(sql, (BaseForm.UserSession.current_user, "NV004", 
                               self.ma_tour, so_nguoi_lon, so_tre_em))
            db.conn.commit()
            
            messagebox.showinfo("Thành công", "Đặt chỗ thành công!")
            self.destroy()
            
        except ValueError:
            messagebox.showerror("Lỗi", "Số lượng phải là số nguyên!")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi khi đặt chỗ: {e}")