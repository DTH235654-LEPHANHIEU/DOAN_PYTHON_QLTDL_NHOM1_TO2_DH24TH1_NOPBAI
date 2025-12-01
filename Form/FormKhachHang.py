from customtkinter import *
from tkinter import messagebox, ttk
from tkcalendar import DateEntry
from Form import BaseForm
 
class Create_KhachHang(CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="#FFFFFF")
        
        self.db = BaseForm.ConnectionDatabase()
        self.Create_frameBottom()
        self.Create_frameTop()
        self.load_data()
        self.list_them = []
        self.list_xoa = []
        self.list_sua = []
        
    def Create_frameBottom(self):
        self.frameBottom = CTkFrame(self, height=400, fg_color="#FFFFFF")
        self.frameBottom.pack(side="bottom", fill="x")
        
        columns = ("MaKhachHang", "HoTen", "NgaySinh", "CCCD" ,"GioiTinh", "SoDienThoai", "Email", "DiaChi", "SoTourDaDat")
        
        self.tree = ttk.Treeview(self.frameBottom, columns=columns, show="headings")
        
        # Thanh cuộn
        # Thanh cuộn
        scrollbar_y = CTkScrollbar(self.frameBottom, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar_y.set)
        
        scrollbar_x = CTkScrollbar(self.frameBottom, command=self.tree.xview, orientation="horizontal")
        self.tree.configure(xscrollcommand=scrollbar_x.set)
        
        scrollbar_y.pack(side="right", fill="y")
        scrollbar_x.pack(side="bottom", fill="x")
        self.tree.pack(side="left", fill="both", expand=True)
        
        style = ttk.Style()
        style.theme_use("default")
        style.configure(
            "Treeview.Heading",
            background="#244f88",   # màu nền heading
            foreground="white",     # màu chữ heading
            font=("Segoe UI", 10, "bold")
        )
        style.map(
            "Treeview.Heading",
            background=[("active", "#1a5bb8")]  # màu khi hover
        )
        # Tạo tiêu đề cột
        cols =[
            ("MaKhachHang", "Mã khách hàng",  120, "center"),
            ("HoTen",       "Tên khách hàng", 150, "w"),
            ("NgaySinh",    "Ngày sinh",      100, "center"),
            ("CCCD",        "CCCD",           100, "center"),
            ("GioiTinh",    "Giới tính",       60, "center"),
            ("SoDienThoai", "Số điện thoại",  100, "center"),
            ("Email",       "Email",          200, "w"),
            ("DiaChi",      "Địa chỉ",        200, "w"),
            ("SoTourDaDat", "Số Tour đã đặt", 200, "center"),
        ]
        for col, text, width, anchor in cols:
            self.tree.heading(col, text = text)
            #stretch khong cho dieu chinh do rong cot
            self.tree.column(col, width=width, anchor=anchor, stretch=False )

     
    def Create_frameTop(self):
        self.frameTop = CTkFrame(self,width=400, height=300, fg_color="#FFFFFF")
        self.frameTop.pack(side="top", fill="both", expand=True)
        
        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)
        
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
        self.date_NgaySinh = DateEntry(self.frameTop, width=38, height=20, date_pattern="dd/mm/yyyy")
        self.date_NgaySinh.place(x=120, y=185)
    #GioiTinh    
        self.lb_GioiTinh = CTkLabel(self.frameTop, text= "Giới tính", font=("Segoe UI", 14))
        self.lb_GioiTinh.place(x=20, y = 220)
        self.cb_GioiTinh = CTkComboBox(self.frameTop, width=250, height=20)
        self.cb_GioiTinh.place(x=120, y=225)  
    #TenDichVu
        self.lb_SoDienThoai= CTkLabel(self.frameTop, text= "Số điện thoại", font=("Segoe UI", 14))
        self.lb_SoDienThoai.place(x=400, y = 100)
        self.entry_SoDienThoai = CTkEntry(self.frameTop, width=250, height=20)
        self.entry_SoDienThoai.place(x=510, y=105)
    #SoTourDaDat
        self.lb_SoTourDaDat = CTkLabel(self.frameTop, text= "Tour đã đặt", font=("Segoe UI", 14))
        self.lb_SoTourDaDat.place(x=20, y = 260)
        self.entry_SoTourDaDat = CTkEntry(self.frameTop, width=250, height=20)
        self.entry_SoTourDaDat.place(x=120, y=265)
    #SoNgay
        self.lb_CCCD = CTkLabel(self.frameTop, text= "CCCD", font=("Segoe UI", 14))
        self.lb_CCCD.place(x=400, y = 140)
        self.entry_CCCD = CTkEntry(self.frameTop, width=250, height=20)
        self.entry_CCCD.place(x=510, y=145)        
    #SoChoToiDa
        self.lb_Email = CTkLabel(self.frameTop, text= "Email", font=("Segoe UI", 14))
        self.lb_Email.place(x=400, y = 180)
        self.entry_Email = CTkEntry(self.frameTop, width=250, height=20)
        self.entry_Email.place(x=510, y=185) 
    #Địa chỉ
        self.lb_DiaChi = CTkLabel(self.frameTop, text= "Địa chỉ", font=("Segoe UI", 14))
        self.lb_DiaChi.place(x=400, y = 220)
        self.entry_DiaChi = CTkEntry(self.frameTop, width=250, height=20)
        self.entry_DiaChi.place(x=510, y=225) 
#Thao tac tim kiem
        self.cb_TimKiem = CTkComboBox(self.frameTop, width=130, height= 20)
        self.cb_TimKiem.place(x=380, y = 315)
        
        self.entry_TimKiem = CTkEntry(self.frameTop, width=330, height=20, fg_color="#FFFFFF")
        self.entry_TimKiem.place(x =520, y=315)
        
        self.btn_Timkiem = CTkButton(self.frameTop, width=40, height=14, text="🔍",
                                     font=("Segoe UI", 14, "bold"),
                                     text_color="#FFFFFF")
        self.btn_Timkiem.place(x=855,y=314)         
#Các thao tác thêm xóa sửa lưu
        if BaseForm.UserSession.is_admin():
    #Thêm
            self.btn_Them = CTkButton(self.frameTop, width=70, height=25, text="➕ Thêm",
                                    fg_color="#1D8D13", font=("Segoe UI", 14, "bold"), command=self.Them)
            self.btn_Them.place(x=20, y = 315)
    #Xóa
            self.btn_Xoa = CTkButton(self.frameTop, width=70, height=25, text="🗑️Xóa",
                                    fg_color="#8D1313", font=("Segoe UI", 14, "bold"), command=self.Xoa)
            self.btn_Xoa.place(x=100, y = 315)
    #Sửa
        self.btn_Sua = CTkButton(self.frameTop, width=70, height=25, text="✍️ Sửa",
                                  fg_color="#6A138D", font=("Segoe UI", 14, "bold"), command=self.Sua)
        
        self.btn_Sua.place(x=190, y = 315)
    #Lưu 
        self.btn_Luu = CTkButton(self.frameTop, width=70, height=25, text="♻️ Lưu",
                                  fg_color="#132F8D", font=("Segoe UI", 14, "bold"), command=self.Luu)
        self.btn_Luu.place(x=270, y = 315)   
  
    def clear_entries(self):
        self.entry_SoTourDaDat.configure(state="normal")
        self.entry_MaKhachHang.delete(0, "end")
        self.entry_HoTen.delete(0, "end")
        self.entry_CCCD.delete(0, "end")
        self.entry_SoDienThoai.delete(0, "end")
        self.entry_DiaChi.delete(0, "end")
        self.entry_Email.delete(0, "end")
        self.entry_SoTourDaDat.delete(0, "end")
        self.entry_SoTourDaDat.configure(state="disabled")
        self.cb_GioiTinh.set("")
        self.entry_MaKhachHang.focus()
        
    def load_data(self):      
        for item in self.tree.get_children():
            self.tree.delete(item)
        #load Cb Gioi tinh
        list_GioiTinh = ["Nam", "Nữ"]
        self.cb_GioiTinh.configure(values= [])
        self.cb_GioiTinh.configure(values=list_GioiTinh)
        
        if list_GioiTinh:
            self.cb_TimKiem.set(list_GioiTinh[0])
            
        #load cb tim kiem
        list_timkiem = ["Mã khách hàng", "Tên khách hàng"]
        self.cb_TimKiem.configure(values=[])
        self.cb_TimKiem.configure(values= list_timkiem)
        if list_timkiem:
            self.cb_TimKiem.set(list_timkiem[0])
        
        if BaseForm.UserSession.is_user():
            sql = "SELECT *FROM KHACHHANG WHERE MaKhachHang = ?"
            params = (BaseForm.UserSession.current_user,)
        else:
            sql = "SELECT *FROM KHACHHANG"
            params = ()
        
        try:
            rows = self.db.query(sql, params)
            if rows:
                for row in rows:
                    ma_kh = row[0]
                    ten_kh = row[1]
                    ngay_sinh = row[2]
                    if hasattr (ngay_sinh, "strftime"):
                        ngay_sinh = ngay_sinh.strftime("%d/%m/%Y")
                    cccd = row[3]
                    gioi_tinh = row[4]
                    sdt = row[5]
                    email= row[6]
                    diachi = row[7]
                    tour_da_dat = row[8]
                    self.tree.insert("", "end", values=(ma_kh, ten_kh, ngay_sinh, cccd, gioi_tinh, sdt, email, diachi, tour_da_dat))                    
        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi truy vấn dữ liệu: {e}")

    def on_tree_select(self, event):
        self.clear_entries()
        selected_item = self.tree.selection()
        if selected_item:
            values = self.tree.item(selected_item[0], "values")
            self.entry_SoTourDaDat.configure(state="normal")
            self.entry_MaKhachHang.insert(0,str(values[0].strip()))
            self.entry_HoTen.insert(0, str(values[1].strip()))
            self.date_NgaySinh.set_date(values[2].strip())
            self.entry_CCCD.insert(0, values[3].strip())
            self.cb_GioiTinh.set(values[4].strip())
            self.entry_SoDienThoai.insert(0,values[5].strip())
            self.entry_DiaChi.insert(0,values[7].strip())
            self.entry_Email.insert(0, values[6].strip())
            self.entry_SoTourDaDat.insert(0, values[8].strip())
            self.entry_SoTourDaDat.configure(state="disabled")
                
    def Them(self):
        ma_kh = self.entry_MaKhachHang.get().strip()
        ho_ten = self.entry_HoTen.get().strip()
        ngay_sinh = self.date_NgaySinh.get_date()
        cccd = self.entry_CCCD.get().strip()
        gioi_tinh = self.cb_GioiTinh.get().strip()
        so_dien_thoai = self.entry_SoDienThoai.get().strip()
        dia_chi = self.entry_DiaChi.get().strip()
        email = self.entry_Email.get().strip()
        so_tour_da_dat = self.entry_SoTourDaDat.get().strip()
        
        
        for item in self.tree.get_children():
            values = self.tree.item(item, "values")
            if values[0].strip() == ma_kh.strip() and ma_kh != "":
                messagebox.showwarning("Cảnh báo", "Mã khách hàng đã tồn tại.")
                return
            if values[3].strip() == cccd.strip() and cccd != "":
                messagebox.showwarning("Cảnh báo", "CCCD đã tồn tại.")
                return
            if values[5].strip() == so_dien_thoai.strip() and so_dien_thoai != "":
                messagebox.showwarning("Cảnh báo", "Số điện thoại đã tồn tại.")
                return
            if values[6].strip() == email.strip() and email != "":
                messagebox.showwarning("Cảnh báo", "Email đã tồn tại.")
                return
        
        self.list_them.append((ma_kh, ho_ten, ngay_sinh, cccd, gioi_tinh, so_dien_thoai, email, dia_chi, so_tour_da_dat))
        
        self.tree.insert("", "end", values=(ma_kh, ho_ten, ngay_sinh.strftime("%d/%m/%Y"), cccd, gioi_tinh, so_dien_thoai, email, dia_chi, so_tour_da_dat))
        self.clear_entries()
        messagebox.showinfo("Thành công", "Đã thêm khách hàng vào danh sách chờ lưu.")
        
    def Xoa(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn khách hàng để xóa.")
            return
        
        ma_kh = self.tree.item(selected_item[0], "values")[0]
        
        for item in self.list_them:
            if item[0] == ma_kh:
                self.list_them.remove(item)
                break
        else:
            self.list_xoa.append(ma_kh)
        
        self.tree.delete(selected_item[0])
        self.clear_entries()
        messagebox.showinfo("Thành công", "Đã xóa khách hàng khỏi danh sách chờ lưu.")
        
    def Sua(self):  
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn khách hàng để sửa.")
            return
        
        ma_kh = self.entry_MaKhachHang.get().strip()
        ho_ten = self.entry_HoTen.get().strip()
        ngay_sinh = self.date_NgaySinh.get_date()
        cccd = self.entry_CCCD.get().strip()
        gioi_tinh = self.cb_GioiTinh.get().strip()
        so_dien_thoai = self.entry_SoDienThoai.get().strip()
        dia_chi = self.entry_DiaChi.get().strip()
        email = self.entry_Email.get().strip()
        so_tour_da_dat = self.entry_SoTourDaDat.get().strip()
        
        if not ma_kh or not ho_ten:
            messagebox.showwarning("Cảnh báo", "Mã khách hàng và Họ tên không được để trống.")
            return
        
        original_ma_kh = self.tree.item(selected_item[0], "values")[0]
        if ma_kh != original_ma_kh:
            for item in self.tree.get_children():
                if self.tree.item(item, "values")[0] == ma_kh:
                    messagebox.showwarning("Cảnh báo", "Mã khách hàng đã tồn tại.")
                    return
        if ma_kh != original_ma_kh:            
            messagebox.showwarning("Lỗi", "Không được phép thay đổi mã khách hàng!")
            return
        self.tree.item(selected_item[0], values=(ma_kh, ho_ten, ngay_sinh.strftime("%d/%m/%Y"), cccd, gioi_tinh, so_dien_thoai, email, dia_chi, so_tour_da_dat))
        
        found_in_them = False
        for index, item in enumerate(self.list_them):
            if item[0] == original_ma_kh:
                self.list_them[index] = (ma_kh, ho_ten, ngay_sinh, cccd, gioi_tinh, so_dien_thoai, email, dia_chi, so_tour_da_dat)
                found_in_them = True
                break
        
        if not found_in_them:
            self.list_sua.append((ma_kh, ho_ten, ngay_sinh, cccd, gioi_tinh, so_dien_thoai, email, dia_chi, so_tour_da_dat))
        
        self.clear_entries()
        messagebox.showinfo("Thành công", "Đã sửa khách hàng trong danh sách chờ lưu.")

    def Luu(self):
        cursor = self.db.conn.cursor()
        try:
            for item in self.list_them:
                sql = """
                INSERT INTO KHACHHANG (MaKhachHang, HoTen, NgaySinh, CCCD, GioiTinh, SoDienThoai, Email, DiaChi, SoTourDaDat)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """
                cursor.execute(sql, (item[0], item[1], item[2], item[3], item[4], item[5], item[6], item[7], item[8]))
            
            for ma_kh in self.list_xoa:
                sql = "DELETE FROM KHACHHANG WHERE MaKhachHang = ?"
                cursor.execute(sql, (ma_kh,))
            
            for item in self.list_sua:
                sql = """
                UPDATE KHACHHANG
                SET HoTen=?, NgaySinh=?, CCCD=?, GioiTinh=?, SoDienThoai=?, Email=?, DiaChi=?
                WHERE MaKhachHang=?
                """
                cursor.execute(sql, (item[1], item[2], item[3], item[4], item[5], item[6], item[7], item[0]))
            
            cursor.commit()
            self.list_them.clear()
            self.list_xoa.clear()
            self.list_sua.clear()
            self.load_data()
            messagebox.showinfo("Thành công", "Đã lưu tất cả các thay đổi vào cơ sở dữ liệu.")
        except Exception as e:
            cursor.rollback()
            messagebox.showerror("Lỗi", f"Lỗi khi lưu dữ liệu: {e}")
