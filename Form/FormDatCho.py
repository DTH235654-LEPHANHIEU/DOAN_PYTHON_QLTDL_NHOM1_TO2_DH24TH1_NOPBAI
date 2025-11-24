from customtkinter import *
from tkinter import messagebox
from Form import BaseForm

class Create_DatCho(CTk):
    def __init__(self, ten_chuyendi = None, ten_diadiem = None, ten_dichvu =None, so_cho_con_lai=None, gia_nguoi_lon=None, gia_tre_em=None):
        super().__init__()

        self.title("ĐẶT TOUR")
        self.geometry("550x400")
        self.resizable(False, False)
        
        self.Create_frameTop()
        self.Create_FrameBottom(ten_chuyendi, ten_diadiem, ten_dichvu, so_cho_con_lai, gia_nguoi_lon, gia_tre_em)

    def Create_frameTop(self):
        self.frameTop = CTkFrame(self, height=100, fg_color="#242861")
        self.frameTop.pack(side="top", fill="x")
        
        self.lb_TieuDe = CTkLabel(self.frameTop,text="ĐẶT CHUYẾN ĐI", height=40, text_color="#ffffff",
                                  font=("Segoe UI", 23, "bold"))
        self.lb_TieuDe.pack(pady=20, anchor="center")

    def Create_FrameBottom(self, ten_chuyendi, ten_diadiem, ten_dichvu, so_cho_con_lai, gia_nguoi_lon, gia_tre_em):
        self.frameBottom = CTkFrame(self, height=360)
        self.frameBottom.pack(side="bottom", fill="both",expand=True)
        
        CTkLabel(self.frameBottom, text="Thông tin chuyến đi", font=("Segoe UI", 17, "bold")).pack(pady=15)

        CTkLabel(self.frameBottom, text=f"Tên chuyến: {ten_chuyendi}", font=("Segoe UI", 14)).pack(padx=10,pady=3, anchor="w")
        CTkLabel(self.frameBottom, text=f"Tên địa điểm: {ten_diadiem}", font=("Segoe UI", 14)).pack(padx=10,pady=3, anchor="w")
        CTkLabel(self.frameBottom, text=f"tên dịch vụ: {ten_dichvu}", font=("Segoe UI", 14)).pack(padx=10, pady=3, anchor="w")
        CTkLabel(self.frameBottom, text=f"Chỗ còn lại: {so_cho_con_lai}", font=("Segoe UI", 14)).pack(padx=10,pady=3, anchor="w")
        CTkLabel(self.frameBottom, text=f"Giá người lớn: {gia_nguoi_lon}", font=("Segoe UI", 14)).pack(padx=10, pady=3, anchor="w")
        CTkLabel(self.frameBottom, text=f"Giá trẻ em: {gia_tre_em}", font=("Segoe UI", 14)).pack(padx=10, pady=3,anchor="w")
        
        self.lb_SoNguoiLon = CTkLabel(self.frameBottom, text="Số lượng người lớn:",font=("Segoe UI", 14, "bold"))        
        self.lb_SoNguoiLon.place(x=280, y= 60)
        self.entry_NguoiLon = CTkEntry(self.frameBottom, width=60, height=10)
        self.entry_NguoiLon.place(x=430, y = 65)
        
        self.lb_SoNguoiTreEm = CTkLabel(self.frameBottom, text="Số lượng người lớn:",font=("Segoe UI", 14, "bold"))        
        self.lb_SoNguoiTreEm.place(x=280, y= 90)
        self.entry_TreEm = CTkEntry(self.frameBottom, width=60, height=10)
        self.entry_TreEm.place(x= 430, y = 93)
        
        self.lb_TongTien = CTkLabel(self.frameBottom, text="Tổng tiền:",font=("Segoe UI", 14, "bold"))        
        self.lb_TongTien.place(x=280, y= 120)
        self.entry_TongTien = CTkEntry(self.frameBottom, width=130, height=10, fg_color="#787583", text_color="#FFFFFF")
        self.entry_TongTien.place(x= 360, y = 123)        
        self.entry_TongTien.configure(state="disabled")
        
        self.btn_XacNhan = CTkButton(self.frameBottom, width=80, height=30, text="Xác nhận", 
                                     fg_color="#242861", font=("Segoe UI", 14, "bold"))
        self.btn_XacNhan.place(x=300, y= 160)
        
        self.btn_Xoa = CTkButton(self.frameBottom, width=80, height=30, text="Hủy",
                                    fg_color="#8D1313", font=("Segoe UI", 14, "bold"))
        self.btn_Xoa.place(x=390, y = 160)
        