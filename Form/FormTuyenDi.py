from customtkinter import *
from tkinter import messagebox, ttk
from Form import BaseForm, FormDatCho

class Create_TuyenDi(CTkFrame):
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
        self.lb_TieuDe = CTkLabel(self.frameTop, text="Thông tin chi tiết của tuyến", font=("Segoe UI", 17, "bold"))
        self.lb_TieuDe.place(x=20, y=65)
    #MaTuyen
        self.lb_MaTuyen = CTkLabel(self.frameTop, text= "Mã tuyến", font=("Segoe UI", 14))
        self.lb_MaTuyen.place(x=20, y = 100) 
        self.entry_MaTuyen = CTkEntry(self.frameTop, width=250, height=20)
        self.entry_MaTuyen.place(x=120, y=105)
    #TenTuyen
        self.lb_TenTuyen = CTkLabel(self.frameTop, text= "Tên tuyến", font=("Segoe UI", 14))
        self.lb_TenTuyen.place(x=20, y = 140)
        self.entry_TenTuyen = CTkEntry(self.frameTop, width=250, height=20)
        self.entry_TenTuyen.place(x=120, y=145)              
    #TenDiaDiem
        self.lb_TenDiaDiem = CTkLabel(self.frameTop, text= "Tên địa điểm", font=("Segoe UI", 14))
        self.lb_TenDiaDiem.place(x=20, y = 180)
        self.entry_TenDiaDiem = CTkEntry(self.frameTop, width=250, height=20)
        self.entry_TenDiaDiem.place(x=120, y=185)
    #TenDichVu
        self.lb_TenDichVu = CTkLabel(self.frameTop, text= "Tên dịch vụ", font=("Segoe UI", 14))
        self.lb_TenDichVu.place(x=20, y = 220)
        self.entry_TenDichVu = CTkEntry(self.frameTop, width=250, height=20)
        self.entry_TenDichVu.place(x=120, y=225)        
    #SoNgay
        self.lb_SoNgay = CTkLabel(self.frameTop, text= "Số ngày", font=("Segoe UI", 14))
        self.lb_SoNgay.place(x=20, y = 260)
        self.entry_SoNgay = CTkEntry(self.frameTop, width=250, height=20)
        self.entry_SoNgay.place(x=120, y=265)        
    #SoChoToiDa
        self.lb_ChoToiDa = CTkLabel(self.frameTop, text= "Số chỗ tối đa", font=("Segoe UI", 14))
        self.lb_ChoToiDa.place(x=400, y = 100)
        self.entry_SoNgay = CTkEntry(self.frameTop, width=250, height=20)
        self.entry_SoNgay.place(x=510, y=105)         
    #SoChoConLai
        self.lb_ChoConLai = CTkLabel(self.frameTop, text= "Số chỗ còn lại", font=("Segoe UI", 14))
        self.lb_ChoConLai.place(x=400, y = 140)
        self.entry_SoNgay = CTkEntry(self.frameTop, width=250, height=20)
        self.entry_SoNgay.place(x=510, y=145) 
    #GiaNguoiLon
        self.lb_GiaNguoiLon = CTkLabel(self.frameTop, text= "Giá người lớn", font=("Segoe UI", 14))
        self.lb_GiaNguoiLon.place(x=400, y = 180)
        self.entry_SoNgay = CTkEntry(self.frameTop, width=250, height=20)
        self.entry_SoNgay.place(x=510, y=185)         
    #GiaTreEm      
        self.lb_GiaTreEm = CTkLabel(self.frameTop, text= "Giá Trẻ em", font=("Segoe UI", 14))
        self.lb_GiaTreEm.place(x=400, y = 220)
        self.entry_SoNgay = CTkEntry(self.frameTop, width=250, height=20)
        self.entry_SoNgay.place(x=510, y=225) 
    
#Các thao tác thêm xóa sửa lưu
    #Đặt chỗ
        if BaseForm.UserSession.is_user():
            self.btn_DatCho = CTkButton(self.frameTop, width=70, height=25, text="➕ Đặt chỗ",
                                    fg_color="#1D8D13", font=("Segoe UI", 14, "bold"), command=self.open_form_dat_cho)
            self.btn_DatCho.place(x=20, y = 330)
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

        if rows:
            for row in rows:
                # row là một tuple: (1, 'T010', datetime..., 12000000, 27)
                
                # Xử lý định dạng hiển thị đẹp hơn
                ma_chuyen_di = row[0]
                ma_tuyen = row[1]
                
                # Format ngày tháng (dd/mm/yyyy)
                ngay_khoi_hanh = row[2].strftime("%d/%m/%Y") if row[2] else ""
                
                # Format tiền tệ (thêm dấu phẩy ngăn cách)
                gia = "{:,.0f} VNĐ".format(row[3])
                
                so_cho = row[4]

                # Thêm vào Treeview
                self.tree.insert("", "end", values=(ma_chuyen_di, ma_tuyen, ngay_khoi_hanh, gia, so_cho))
        else:
            print("Không có dữ liệu trong bảng CHUYENDI")
    def open_form_dat_cho(self):
        # Tạo cửa sổ form mới
        form = FormDatCho.Create_DatCho()
        form.mainloop()  # nếu dùng CTk       