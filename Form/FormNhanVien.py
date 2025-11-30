from customtkinter import *
from tkinter import messagebox, ttk
from tkcalendar import DateEntry
from Form import BaseForm

class Create_NhanVien(CTkFrame):
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
        
        columns = ("MaNhanVien", "HoTen", "NgaySinh", "GioiTinh", "SoDienThoai", 
                  "Email", "ChucVu", "NgayVaoLam", "DiaChi")
        
        self.tree = ttk.Treeview(self.frameBottom, columns=columns, show="headings")
        
        # Thanh cuộn
        scrollbar_y = CTkScrollbar(self.frameBottom, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar_y.set)
        
        scrollbar_x = CTkScrollbar(self.frameBottom, command=self.tree.xview, orientation="horizontal")
        self.tree.configure(xscrollcommand=scrollbar_x.set)
        
        scrollbar_y.pack(side="right", fill="y")
        scrollbar_x.pack(side="bottom", fill="x")
        self.tree.pack(side="left", fill="both", expand=True)
        
        # Style cho Treeview
        style = ttk.Style()
        style.theme_use("default")
        style.configure(
            "Treeview.Heading",
            background="#244f88",
            foreground="white",
            font=("Segoe UI", 10, "bold")
        )
        style.map(
            "Treeview.Heading",
            background=[("active", "#1a5bb8")]
        )
        
        # Tạo tiêu đề cột
        cols = [
            ("MaNhanVien", "Mã NV", 100, "center"),
            ("HoTen", "Họ Tên", 180, "w"),
            ("NgaySinh", "Ngày Sinh", 100, "center"),
            ("GioiTinh", "Giới Tính", 80, "center"),
            ("SoDienThoai", "SĐT", 110, "center"),
            ("Email", "Email", 180, "w"),
            ("ChucVu", "Chức Vụ", 130, "center"),
            ("NgayVaoLam", "Ngày Vào Làm", 120, "center"),
            ("DiaChi", "Địa Chỉ", 200, "w"),
        ]
        for col, text, width, anchor in cols:
            self.tree.heading(col, text=text)
            self.tree.column(col, width=width, anchor=anchor, stretch=False)
    
    def Create_frameTop(self):
        self.frameTop = CTkFrame(self, width=400, height=300, fg_color="#FFFFFF")
        self.frameTop.pack(side="top", fill="both", expand=True)
        
        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)
            
        self.lb_TieuDe = CTkLabel(self.frameTop, text="Thông tin chi tiết Nhân Viên", font=("Segoe UI", 17, "bold"))
        self.lb_TieuDe.place(x=20, y=65)
        
    #MaNhanVien
        self.lb_MaNhanVien = CTkLabel(self.frameTop, text="Mã nhân viên", font=("Segoe UI", 14))
        self.lb_MaNhanVien.place(x=20, y=100) 
        self.entry_MaNhanVien = CTkEntry(self.frameTop, width=250, height=20)
        self.entry_MaNhanVien.place(x=150, y=105)
        
    #HoTen
        self.lb_HoTen = CTkLabel(self.frameTop, text="Họ tên", font=("Segoe UI", 14))
        self.lb_HoTen.place(x=20, y=140)
        self.entry_HoTen = CTkEntry(self.frameTop, width=250, height=20)
        self.entry_HoTen.place(x=150, y=145)              
        
    #NgaySinh
        self.lb_NgaySinh = CTkLabel(self.frameTop, text="Ngày sinh", font=("Segoe UI", 14))
        self.lb_NgaySinh.place(x=20, y=180)
        self.date_NgaySinh = DateEntry(self.frameTop, width=36, height=20)
        self.date_NgaySinh.place(x=150, y=185)
        
    #GioiTinh
        self.lb_GioiTinh = CTkLabel(self.frameTop, text="Giới tính", font=("Segoe UI", 14))
        self.lb_GioiTinh.place(x=20, y=220)
        self.cb_GioiTinh = CTkComboBox(self.frameTop, width=250, height=20)
        self.cb_GioiTinh.place(x=150, y=225)
        
    #ChucVu
        self.lb_ChucVu = CTkLabel(self.frameTop, text="Chức vụ", font=("Segoe UI", 14))
        self.lb_ChucVu.place(x=20, y=260)
        self.cb_ChucVu = CTkComboBox(self.frameTop, width=250, height=20)
        self.cb_ChucVu.place(x=150, y=265)
        
    #SoDienThoai
        self.lb_SoDienThoai = CTkLabel(self.frameTop, text="Số điện thoại", font=("Segoe UI", 14))
        self.lb_SoDienThoai.place(x=450, y=100)
        self.entry_SoDienThoai = CTkEntry(self.frameTop, width=250, height=20)
        self.entry_SoDienThoai.place(x=580, y=105)
        
    #Email
        self.lb_Email = CTkLabel(self.frameTop, text="Email", font=("Segoe UI", 14))
        self.lb_Email.place(x=450, y=140)
        self.entry_Email = CTkEntry(self.frameTop, width=250, height=20)
        self.entry_Email.place(x=580, y=145)
        
    #NgayVaoLam
        self.lb_NgayVaoLam = CTkLabel(self.frameTop, text="Ngày vào làm", font=("Segoe UI", 14))
        self.lb_NgayVaoLam.place(x=450, y=180)
        self.date_NgayVaoLam = DateEntry(self.frameTop, width=36, height=20)
        self.date_NgayVaoLam.place(x=580, y=185)
        
    #DiaChi
        self.lb_DiaChi = CTkLabel(self.frameTop, text="Địa chỉ", font=("Segoe UI", 14))
        self.lb_DiaChi.place(x=450, y=220)
        self.entry_DiaChi = CTkEntry(self.frameTop, width=250, height=20)
        self.entry_DiaChi.place(x=580, y=225)

#--------------------------------------
# CHỨC NĂNG TÌM KIẾM
#--------------------------------------    
        self.cb_TimKiem = CTkComboBox(self.frameTop, width=130, height=20)
        self.cb_TimKiem.place(x=380, y=315)
        
        self.entry_TimKiem = CTkEntry(self.frameTop, width=330, height=20, fg_color="#FFFFFF")
        self.entry_TimKiem.place(x=520, y=315)
        
        self.btn_Timkiem = CTkButton(self.frameTop, width=40, height=14, text="🔍",
                                     font=("Segoe UI", 14, "bold"),
                                     text_color="#FFFFFF")
        self.btn_Timkiem.place(x=855, y=314)   

#--------------------------------------
# TẠO CÁC BUTTON
#--------------------------------------    
        if BaseForm.UserSession.is_admin():
    #Thêm
            self.btn_Them = CTkButton(self.frameTop, width=70, height=25, text="➕ Thêm",
                                    fg_color="#1D8D13", font=("Segoe UI", 14, "bold"), command=self.Them)
            self.btn_Them.place(x=20, y=315)            
    #Xóa
            self.btn_Xoa = CTkButton(self.frameTop, width=70, height=25, text="🗑️Xóa",
                                    fg_color="#8D1313", font=("Segoe UI", 14, "bold"), command=self.Xoa)
            self.btn_Xoa.place(x=100, y=315)
    #Sửa
            self.btn_Sua = CTkButton(self.frameTop, width=70, height=25, text="✍️ Sửa",
                                    fg_color="#6A138D", font=("Segoe UI", 14, "bold"), command=self.Sua)
            self.btn_Sua.place(x=190, y=315)
    #Lưu 
        self.btn_Luu = CTkButton(self.frameTop, width=70, height=25, text="♻️ Lưu",
                                    fg_color="#132F8D", font=("Segoe UI", 14, "bold"), command=self.Luu)
        self.btn_Luu.place(x=270, y=315)
            
    def clear_entries(self):
        self.entry_MaNhanVien.delete(0, "end")
        self.entry_HoTen.delete(0, "end")
        self.cb_GioiTinh.set(" ")
        self.cb_ChucVu.set(" ")
        self.entry_SoDienThoai.delete(0, "end")
        self.entry_Email.delete(0, "end")
        self.entry_DiaChi.delete(0, "end")
    
    def load_data(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Load Giới Tính
        list_GioiTinh = ["Nam", "Nữ"]
        self.cb_GioiTinh.configure(values=list_GioiTinh)
        
        # Load Chức Vụ
        list_ChucVu = ["Hướng dẫn viên", "Tư vấn viên"]
        self.cb_ChucVu.configure(values=list_ChucVu)
        
        # Load dữ liệu nhân viên
        sql = """
        SELECT MaNhanVien, HoTen, NgaySinh, GioiTinh, SoDienThoai, 
               Email, ChucVu, NgayVaoLam, DiaChi 
        FROM NHANVIEN
        """
        try:
            rows = self.db.query(sql)
            if rows:
                for row in rows:
                    ngay_sinh = row[2].strftime("%d/%m/%Y") if row[2] and hasattr(row[2], "strftime") else ""
                    ngay_vao_lam = row[7].strftime("%d/%m/%Y") if row[7] and hasattr(row[7], "strftime") else ""
                    
                    self.tree.insert("", "end", values=(
                        row[0], row[1], ngay_sinh, row[3], row[4], 
                        row[5], row[6], ngay_vao_lam, row[8]
                    ))
        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi truy vấn dữ liệu: {e}")
    
    def on_tree_select(self, event):
        self.clear_entries()
        selected_item = self.tree.selection()
        if selected_item:
            values = self.tree.item(selected_item[0], "values")
            
            self.entry_MaNhanVien.insert(0, str(values[0].strip()))
            self.entry_HoTen.insert(0, str(values[1].strip()))
            if values[2]:
                self.date_NgaySinh.set_date(values[2].strip())
            self.cb_GioiTinh.set(str(values[3].strip()) if values[3] else "")
            self.entry_SoDienThoai.insert(0, str(values[4].strip()) if values[4] else "")
            self.entry_Email.insert(0, str(values[5].strip()) if values[5] else "")
            self.cb_ChucVu.set(str(values[6].strip()) if values[6] else "")
            if values[7]:
                self.date_NgayVaoLam.set_date(values[7].strip())
            self.entry_DiaChi.insert(0, str(values[8].strip()) if values[8] else "")
    
    def Them(self):
        ma_nhan_vien = self.entry_MaNhanVien.get().strip()
        ho_ten = self.entry_HoTen.get().strip()
        ngay_sinh = self.date_NgaySinh.get_date()
        gioi_tinh = self.cb_GioiTinh.get().strip()
        so_dien_thoai = self.entry_SoDienThoai.get().strip()
        email = self.entry_Email.get().strip()
        chuc_vu = self.cb_ChucVu.get().strip()
        ngay_vao_lam = self.date_NgayVaoLam.get_date()
        dia_chi = self.entry_DiaChi.get().strip()
        
        if not all([ma_nhan_vien, ho_ten, gioi_tinh, chuc_vu]):
            messagebox.showwarning("Cảnh báo", "Vui lòng điền đầy đủ thông tin bắt buộc (Mã NV, Họ tên, Giới tính, Chức vụ).")
            return
        
        # Kiểm tra trùng lặp mã nhân viên
        for item in self.tree.get_children():
            values = self.tree.item(item, "values")
            if values[0].strip() == ma_nhan_vien:
                messagebox.showwarning("Cảnh báo", "Mã nhân viên đã tồn tại.")
                return
        
        # Kiểm tra trùng số điện thoại
        if so_dien_thoai:
            for item in self.tree.get_children():
                values = self.tree.item(item, "values")
                if values[4].strip() == so_dien_thoai:
                    messagebox.showwarning("Cảnh báo", "Số điện thoại đã tồn tại.")
                    return
        
        # Kiểm tra trùng email
        if email:
            for item in self.tree.get_children():
                values = self.tree.item(item, "values")
                if values[5].strip() == email:
                    messagebox.showwarning("Cảnh báo", "Email đã tồn tại.")
                    return
        
        self.tree.insert("", "end", values=(
            ma_nhan_vien, ho_ten, ngay_sinh.strftime("%d/%m/%Y"), gioi_tinh, 
            so_dien_thoai, email, chuc_vu, ngay_vao_lam.strftime("%d/%m/%Y"), dia_chi
        ))
        
        self.list_them.append((
            ma_nhan_vien, ho_ten, ngay_sinh.strftime("%Y-%m-%d"), gioi_tinh, 
            so_dien_thoai, email, chuc_vu, ngay_vao_lam.strftime("%Y-%m-%d"), dia_chi
        ))
        
        self.clear_entries()
        messagebox.showinfo("Thành công", "Đã thêm nhân viên vào danh sách chờ lưu.")
    
    def Xoa(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn nhân viên để xóa.")
            return
        
        ma_nhan_vien = self.tree.item(selected_item[0], "values")[0]
        
        # Kiểm tra ràng buộc với DATCHO
        check_sql = "SELECT COUNT(*) FROM DATCHO WHERE MaNhanVien = ?"
        result = self.db.query(check_sql, (ma_nhan_vien,))
        if result and result[0][0] > 0:
            messagebox.showerror("Lỗi", f"Không thể xóa nhân viên này vì đã có {result[0][0]} đặt chỗ liên quan!")
            return
        
        for item in self.list_them:
            if item[0] == ma_nhan_vien:
                self.list_them.remove(item)
                break
        else:
            self.list_xoa.append(ma_nhan_vien)
        
        self.tree.delete(selected_item[0])
        self.clear_entries()
        messagebox.showinfo("Thành công", "Đã xóa nhân viên khỏi danh sách chờ lưu.")
    
    def Sua(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn nhân viên để sửa.")
            return
        
        ma_nhan_vien = self.entry_MaNhanVien.get().strip()
        ho_ten = self.entry_HoTen.get().strip()
        ngay_sinh = self.date_NgaySinh.get_date()
        gioi_tinh = self.cb_GioiTinh.get().strip()
        so_dien_thoai = self.entry_SoDienThoai.get().strip()
        email = self.entry_Email.get().strip()
        chuc_vu = self.cb_ChucVu.get().strip()
        ngay_vao_lam = self.date_NgayVaoLam.get_date()
        dia_chi = self.entry_DiaChi.get().strip()
        
        if not ma_nhan_vien:
            messagebox.showwarning("Cảnh báo", "Mã nhân viên không được để trống.")
            return
        
        original_ma_nhan_vien = self.tree.item(selected_item[0], "values")[0]
        if ma_nhan_vien != original_ma_nhan_vien:
            messagebox.showwarning("Lỗi", "Không được phép thay đổi mã nhân viên!")
            return
        
        # Kiểm tra trùng số điện thoại (trừ chính nó)
        if so_dien_thoai:
            for item in self.tree.get_children():
                if item != selected_item[0]:
                    values = self.tree.item(item, "values")
                    if values[4].strip() == so_dien_thoai:
                        messagebox.showwarning("Cảnh báo", "Số điện thoại đã tồn tại.")
                        return
        
        # Kiểm tra trùng email (trừ chính nó)
        if email:
            for item in self.tree.get_children():
                if item != selected_item[0]:
                    values = self.tree.item(item, "values")
                    if values[5].strip() == email:
                        messagebox.showwarning("Cảnh báo", "Email đã tồn tại.")
                        return
        
        self.tree.item(selected_item[0], values=(
            ma_nhan_vien, ho_ten, ngay_sinh.strftime("%d/%m/%Y"), gioi_tinh, 
            so_dien_thoai, email, chuc_vu, ngay_vao_lam.strftime("%d/%m/%Y"), dia_chi
        ))
        
        self.list_sua.append((
            ma_nhan_vien, ho_ten, ngay_sinh.strftime("%Y-%m-%d"), gioi_tinh, 
            so_dien_thoai, email, chuc_vu, ngay_vao_lam.strftime("%Y-%m-%d"), dia_chi
        ))
        
        self.clear_entries()
        messagebox.showinfo("Thành công", "Đã sửa nhân viên trong danh sách chờ lưu.")
    
    def Luu(self):
        cursor = self.db.conn.cursor()
        try:
            # INSERT
            for item in self.list_them:
                sql = """
                INSERT INTO NHANVIEN (MaNhanVien, HoTen, NgaySinh, GioiTinh, SoDienThoai, 
                                     Email, ChucVu, NgayVaoLam, DiaChi)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """
                cursor.execute(sql, item)
            
            # DELETE
            for ma_nhan_vien in self.list_xoa:
                sql = "DELETE FROM NHANVIEN WHERE MaNhanVien = ?"
                cursor.execute(sql, (ma_nhan_vien,))
            
            # UPDATE
            for item in self.list_sua:
                sql = """
                UPDATE NHANVIEN 
                SET HoTen=?, NgaySinh=?, GioiTinh=?, SoDienThoai=?, 
                    Email=?, ChucVu=?, NgayVaoLam=?, DiaChi=?
                WHERE MaNhanVien=?
                """
                cursor.execute(sql, (item[1], item[2], item[3], item[4], item[5], item[6], item[7], item[8], item[0]))
            
            cursor.commit()
            self.list_them.clear()
            self.list_xoa.clear()
            self.list_sua.clear()
            self.load_data()
            messagebox.showinfo("Thành công", "Đã lưu tất cả các thay đổi vào cơ sở dữ liệu.")
        except Exception as e:
            cursor.rollback()
            messagebox.showerror("Lỗi", f"Lỗi khi lưu dữ liệu: {e}")