from customtkinter import *
from tkinter import messagebox, ttk
from tkcalendar import DateEntry
from Form import BaseForm
 
class Create_KhachHang(CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="#FFFFFF")
        
        self.db = BaseForm.ConectionDatabase()
        self.Create_frameBottom()
        self.Create_frameTop()
        self.load_data()
        
    def Create_frameBottom(self):
        self.frameBottom = CTkFrame(self, height=400, fg_color="#FFFFFF")
        self.frameBottom.pack(side="bottom", fill="x")
        
        columns = ("MaChuyenDi", "MaTuyen", "NgayKhoiHanh", "GiaNguoiLon", "SoChoConLai")
        
        self.tree = ttk.Treeview(self.frameBottom, columns=columns, show="headings")
  
        # Tạo tiêu đề cột
        self.tree.heading("MaChuyenDi", text="ID")
        self.tree.heading("MaTuyen", text="Mã Tuyến")
        self.tree.heading("NgayKhoiHanh", text="Ngày Khởi Hành")
        self.tree.heading("GiaNguoiLon", text="Giá Người Lớn")
        self.tree.heading("SoChoConLai", text="Chỗ Còn")
        
        # Chỉnh kích thước cột
        self.tree.column("MaChuyenDi", width=50, anchor="center")
        self.tree.column("MaTuyen", width=100, anchor="center")
        self.tree.column("NgayKhoiHanh", width=150, anchor="center")
        self.tree.column("GiaNguoiLon", width=150, anchor="e") # anchor="e" để căn phải số tiền
        self.tree.column("SoChoConLai", width=100, anchor="center")

        # Thanh cuộn
        scrollbar = CTkScrollbar(self.frameBottom, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        scrollbar.pack(side="right", fill="y")
        self.tree.pack(side="left", fill="both", expand=True)
     
    def Create_frameTop(self):
        self.frameTop = CTkFrame(self,width=400, height=300, fg_color="#FFFFFF")
        self.frameTop.pack(side="top", fill="both", expand=True)
        
#Thao tac tim kiem
        self.cb_TimKiem = CTkComboBox(self.frameTop, width=130, height= 20)
        self.cb_TimKiem.place(x=380, y = 330)
        
        self.entry_TimKiem = CTkEntry(self.frameTop, width=330, height=20, fg_color="#FFFFFF")
        self.entry_TimKiem.place(x =520, y=330)
        
        self.btn_Timkiem = CTkButton(self.frameTop, width=40, height=14, text="🔍",
                                     font=("Segoe UI", 14, "bold"),
                                     text_color="#FFFFFF")
        self.btn_Timkiem.place(x=855,y=329)
        
#Thao tac hien thi thong tin  
        self.lb_TieuDe = CTkLabel(self.frameTop, text="Thông tin chi tiết của khách hàng", font=("Segoe UI", 17, "bold"))
        self.lb_TieuDe.place(x=20, y=65)
    #MaTuyen
        self.lb_MaKhachHang = CTkLabel(self.frameTop, text= "Mã khách hàng", font=("Segoe UI", 14))
        self.lb_MaKhachHang.place(x=20, y = 100) 
        self.entry_MaKhachHang = CTkEntry(self.frameTop, width=250, height=20)
        self.entry_MaKhachHang.place(x=120, y=105)
    #TenTuyen
        self.lb_HoTen = CTkLabel(self.frameTop, text= "Họ tên", font=("Segoe UI", 14))
        self.lb_HoTen.place(x=20, y = 140)
        self.entry_HoTen = CTkEntry(self.frameTop, width=250, height=20)
        self.entry_HoTen.place(x=120, y=145)              
    #TenDiaDiem
        self.lb_NgaySinh = CTkLabel(self.frameTop, text= "Ngày sinh", font=("Segoe UI", 14))
        self.lb_NgaySinh.place(x=20, y = 180)
        self.entry_NgaySinh = DateEntry(self.frameTop, width=38, height=20, date_pattern="dd/mm/yyyy")
        self.entry_NgaySinh.place(x=120, y=185)
    #TenDichVu
        self.lb_SoDienThoai= CTkLabel(self.frameTop, text= "Số điện thoại", font=("Segoe UI", 14))
        self.lb_SoDienThoai.place(x=400, y = 100)
        self.entry_SoDienThoai = CTkEntry(self.frameTop, width=250, height=20)
        self.entry_SoDienThoai.place(x=510, y=105)        
    #SoNgay
        self.lb_CCCD = CTkLabel(self.frameTop, text= "CCCD", font=("Segoe UI", 14))
        self.lb_CCCD.place(x=400, y = 140)
        self.entry_CCCD = CTkEntry(self.frameTop, width=250, height=20)
        self.entry_CCCD.place(x=510, y=145)        
    #SoChoToiDa
        self.lb_DiaChi = CTkLabel(self.frameTop, text= "Địa chỉ", font=("Segoe UI", 14))
        self.lb_DiaChi.place(x=400, y = 180)
        self.entry_DiaChi = CTkEntry(self.frameTop, width=250, height=20)
        self.entry_DiaChi.place(x=510, y=185)          
#Các thao tác thêm xóa sửa lưu
        if BaseForm.UserSession.is_admin():
    #Thêm
            self.btn_Them = CTkButton(self.frameTop, width=70, height=25, text="➕ Thêm",
                                    fg_color="#1D8D13", font=("Segoe UI", 14, "bold"))
            self.btn_Them.place(x=20, y = 330)
    #Xóa
            self.btn_Xoa = CTkButton(self.frameTop, width=70, height=25, text="🗑️Xóa",
                                    fg_color="#8D1313", font=("Segoe UI", 14, "bold"))
            self.btn_Xoa.place(x=100, y = 330)
    #Sửa
        self.btn_Sua = CTkButton(self.frameTop, width=70, height=25, text="✍️ Sửa",
                                  fg_color="#6A138D", font=("Segoe UI", 14, "bold"))
        
        self.btn_Sua.place(x=190, y = 330)
    #Lưu 
        self.btn_Luu = CTkButton(self.frameTop, width=70, height=25, text="♻️ Lưu",
                                  fg_color="#132F8D", font=("Segoe UI", 14, "bold"))
        self.btn_Luu.place(x=270, y = 330)   
        
    def load_data(self):
        """Truy vấn SQL và đổ dữ liệu vào Treeview"""
        # Xóa dữ liệu cũ trên bảng (nếu có)
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Truy vấn dữ liệu
        sql = "SELECT MaChuyenDi, MaTuyen, NgayKhoiHanh, GiaNguoiLon, SoChoConLai FROM CHUYENDI"
        rows = self.db.query(sql)


