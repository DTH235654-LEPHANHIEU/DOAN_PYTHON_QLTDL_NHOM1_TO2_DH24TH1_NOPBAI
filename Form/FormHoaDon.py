from customtkinter import *
from tkinter import messagebox, ttk
from tkcalendar import DateEntry
from Form import BaseForm

class Create_HoaDon(CTkFrame):
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
        
        columns = ("MaThanhToan", "MaDatCho", "SoTien", "PhuongThuc", "NgayThanhToan", "TrangThaiTT")
        
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
            ("MaThanhToan", "Mã Thanh Toán", 150, "center"),
            ("MaDatCho", "Mã Đặt Chỗ", 150, "center"),
            ("SoTien", "Số Tiền", 150, "e"),
            ("PhuongThuc", "Phương Thức", 150, "center"),
            ("NgayThanhToan", "Ngày Thanh Toán", 150, "center"),
            ("TrangThaiTT", "Trạng Thái", 150, "center"),
        ]
        for col, text, width, anchor in cols:
            self.tree.heading(col, text=text)
            self.tree.column(col, width=width, anchor=anchor, stretch=False)
    
    def Create_frameTop(self):
        self.frameTop = CTkFrame(self, width=400, height=300, fg_color="#FFFFFF")
        self.frameTop.pack(side="top", fill="both", expand=True)
        
        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)
            
        self.lb_TieuDe = CTkLabel(self.frameTop, text="Thông tin chi tiết của Hóa Đơn", font=("Segoe UI", 17, "bold"))
        self.lb_TieuDe.place(x=20, y=65)
        
    #MaThanhToan
        self.lb_MaThanhToan = CTkLabel(self.frameTop, text="Mã thanh toán", font=("Segoe UI", 14))
        self.lb_MaThanhToan.place(x=20, y=100) 
        self.entry_MaThanhToan = CTkEntry(self.frameTop, width=250, height=20)
        self.entry_MaThanhToan.place(x=160, y=105)
        
    #MaDatCho
        self.lb_MaDatCho = CTkLabel(self.frameTop, text="Mã đặt chỗ", font=("Segoe UI", 14))
        self.lb_MaDatCho.place(x=20, y=140)
        self.cb_MaDatCho = CTkComboBox(self.frameTop, width=250, height=20, command=self.load_so_tien)
        self.cb_MaDatCho.place(x=160, y=145)              
        
    #PhuongThuc
        self.lb_PhuongThuc = CTkLabel(self.frameTop, text="Phương thức", font=("Segoe UI", 14))
        self.lb_PhuongThuc.place(x=20, y=180)
        self.cb_PhuongThuc = CTkComboBox(self.frameTop, width=250, height=20)
        self.cb_PhuongThuc.place(x=160, y=185)
        
    #TrangThaiTT
        self.lb_TrangThaiTT = CTkLabel(self.frameTop, text="Trạng thái", font=("Segoe UI", 14))
        self.lb_TrangThaiTT.place(x=20, y=220)
        self.cb_TrangThaiTT = CTkComboBox(self.frameTop, width=250, height=20)
        self.cb_TrangThaiTT.place(x=160, y=225)
        
    #SoTien (Disabled - Lấy từ DATCHO)
        self.lb_SoTien = CTkLabel(self.frameTop, text="Số tiền", font=("Segoe UI", 14))
        self.lb_SoTien.place(x=450, y=100)
        self.entry_SoTien = CTkEntry(self.frameTop, width=250, height=20, fg_color="#928FA7")
        self.entry_SoTien.place(x=550, y=105)
        self.entry_SoTien.configure(state="disabled")
        
    #NgayThanhToan
        self.lb_NgayThanhToan = CTkLabel(self.frameTop, text="Ngày thanh toán", font=("Segoe UI", 14))
        self.lb_NgayThanhToan.place(x=450, y=140)
        self.date_NgayThanhToan = DateEntry(self.frameTop, width=38, height=20)
        self.date_NgayThanhToan.place(x=595, y=145)

#--------------------------------------
# CHỨC NĂNG TÌM KIẾM
#--------------------------------------    
        self.cb_TimKiem = CTkComboBox(self.frameTop, width=130, height=20)
        self.cb_TimKiem.place(x=380, y=315)
        
        self.entry_TimKiem = CTkEntry(self.frameTop, width=330, height=20, fg_color="#FFFFFF")
        self.entry_TimKiem.place(x=520, y=315)
        
        self.btn_Timkiem = CTkButton(self.frameTop, width=40, height=14, text="🔍",
                                     font=("Segoe UI", 14, "bold"),
                                     text_color="#FFFFFF", command=self.TimKiem)
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
    
    def load_so_tien(self, *args):
        try:
            ma_dat_cho = self.cb_MaDatCho.get().strip().split(" - ")[0] if self.cb_MaDatCho.get() else ""
            if not ma_dat_cho:
                return
            
            # Lấy tổng tiền từ DATCHO
            sql = "SELECT TongTien FROM DATCHO WHERE MaDatCho = ?"
            result = self.db.query(sql, (ma_dat_cho,))
            
            if result:
                so_tien = result[0][0]
                self.entry_SoTien.configure(state="normal")
                self.entry_SoTien.delete(0, "end")
                self.entry_SoTien.insert(0, f"{so_tien:,.0f}")
                self.entry_SoTien.configure(state="disabled")
        except Exception as e:
            print(f"Lỗi load số tiền: {e}")
            
    def clear_entries(self):
        self.entry_MaThanhToan.delete(0, "end")
        self.cb_MaDatCho.set(" ")
        self.cb_PhuongThuc.set(" ")
        self.cb_TrangThaiTT.set(" ")
        self.entry_SoTien.configure(state="normal")
        self.entry_SoTien.delete(0, "end")
        self.entry_SoTien.configure(state="disabled")
    
    def load_data(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Load ComboBox Mã Đặt Chỗ
        try:
            datcho = self.db.query("SELECT MaDatCho, MaKhachHang FROM DATCHO")
            dc_list = [f"{dc[0]} - {dc[1]}" for dc in datcho]
            self.cb_MaDatCho.configure(values=dc_list)
        except:
            pass
        
        # Load Phương Thức
        list_PhuongThuc = ["Tiền mặt", "Chuyển khoản"]
        self.cb_PhuongThuc.configure(values=list_PhuongThuc)
        
        list_TimKiem = ["Mã thanh toán", "Mã đặt chỗ"]
        self.cb_TimKiem.configure(values=list_TimKiem)
        # Load Trạng Thái
        list_TrangThai = ["Đã thanh toán", "Chưa thanh toán"]
        self.cb_TrangThaiTT.configure(values=list_TrangThai)
        if BaseForm.UserSession.is_user():
            sql = """SELECT 
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
                    WHERE DC.MaKhachHang = ?
                    ORDER BY TT.NgayThanhToan DESC;
            """
            params = (BaseForm.UserSession.current_user,)
        else:
            sql = """
            SELECT MaThanhToan, MaDatCho, SoTien, PhuongThuc, NgayThanhToan, TrangThaiTT 
            FROM THANHTOAN
            """
            params = ()
            
        try:
            rows = self.db.query(sql, params)
            if rows:
                for row in rows:
                    ngay_tt = ""
                    if row[4]:
                        ngay_tt = row[4].strftime("%d/%m/%Y") if hasattr(row[4], "strftime") else str(row[4])
                    
                    so_tien = "{:,.0f} VND".format(row[2])                    
                    self.tree.insert("", "end", values=(
                        row[0], row[1], so_tien, row[3], ngay_tt, row[5]
                    ))
        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi truy vấn dữ liệu: {e}")
    
    def on_tree_select(self, event):
        self.clear_entries()
        selected_item = self.tree.selection()
        if selected_item:
            values = self.tree.item(selected_item[0], "values")
            
            self.entry_MaThanhToan.insert(0, str(values[0].strip()))
            self.cb_MaDatCho.set(str(values[1].strip()))
            self.entry_SoTien.configure(state="normal")
            self.entry_SoTien.insert(0, str(values[2].strip()))
            self.entry_SoTien.configure(state="disabled")
            self.cb_PhuongThuc.set(str(values[3].strip()) if values[3] else "")
            if values[4]:
                self.date_NgayThanhToan.set_date(values[4].strip())
            self.cb_TrangThaiTT.set(str(values[5].strip()))
    
    def Them(self):
        ma_thanh_toan = self.entry_MaThanhToan.get().strip()
        ma_dat_cho = self.cb_MaDatCho.get().strip().split(" - ")[0] if self.cb_MaDatCho.get() else ""
        so_tien = self.entry_SoTien.get().strip().replace(",", "")
        phuong_thuc = self.cb_PhuongThuc.get().strip()
        trang_thai = self.cb_TrangThaiTT.get().strip()
        ngay_tt = self.date_NgayThanhToan.get_date()
        
        if not all([ma_thanh_toan, ma_dat_cho, so_tien, phuong_thuc, trang_thai]):
            messagebox.showwarning("Cảnh báo", "Vui lòng điền đầy đủ thông tin bắt buộc.")
            return
        
        # Kiểm tra trùng lặp
        for item in self.tree.get_children():
            values = self.tree.item(item, "values")
            if values[0].strip() == ma_thanh_toan:
                messagebox.showwarning("Cảnh báo", "Mã thanh toán đã tồn tại.")
                return
        
        # Kiểm tra MaDatCho có tồn tại không
        check_sql = "SELECT COUNT(*) FROM DATCHO WHERE MaDatCho = ?"
        result = self.db.query(check_sql, (ma_dat_cho,))
        if not result or result[0][0] == 0:
            messagebox.showerror("Lỗi", "Mã đặt chỗ không tồn tại!")
            return
        
        self.tree.insert("", "end", values=(
            ma_thanh_toan, ma_dat_cho, so_tien, phuong_thuc, 
            ngay_tt.strftime("%d/%m/%Y"), trang_thai
        ))
        
        self.list_them.append((
            ma_thanh_toan, ma_dat_cho, so_tien, phuong_thuc, 
            ngay_tt.strftime("%Y-%m-%d"), trang_thai
        ))
        
        self.clear_entries()
        messagebox.showinfo("Thành công", "Đã thêm thanh toán vào danh sách chờ lưu.")
    
    def Xoa(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn thanh toán để xóa.")
            return
        
        ma_thanh_toan = self.tree.item(selected_item[0], "values")[0]
        
        for item in self.list_them:
            if item[0] == ma_thanh_toan:
                self.list_them.remove(item)
                break
        else:
            self.list_xoa.append(ma_thanh_toan)
        
        self.tree.delete(selected_item[0])
        self.clear_entries()
        messagebox.showinfo("Thành công", "Đã xóa thanh toán khỏi danh sách chờ lưu.")
    
    def Sua(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn thanh toán để sửa.")
            return
        
        ma_thanh_toan = self.entry_MaThanhToan.get().strip()
        ma_dat_cho = self.cb_MaDatCho.get().strip().split(" - ")[0] if self.cb_MaDatCho.get() else ""
        so_tien = self.entry_SoTien.get().strip().replace(",", "")
        phuong_thuc = self.cb_PhuongThuc.get().strip()
        trang_thai = self.cb_TrangThaiTT.get().strip()
        ngay_tt = self.date_NgayThanhToan.get_date()
        
        if not ma_thanh_toan:
            messagebox.showwarning("Cảnh báo", "Mã thanh toán không được để trống.")
            return
        
        original_ma_thanh_toan = self.tree.item(selected_item[0], "values")[0]
        if ma_thanh_toan != original_ma_thanh_toan:
            messagebox.showwarning("Lỗi", "Không được phép thay đổi mã thanh toán!")
            return
        
        self.tree.item(selected_item[0], values=(
            ma_thanh_toan, ma_dat_cho, so_tien, phuong_thuc, 
            ngay_tt.strftime("%d/%m/%Y"), trang_thai
        ))
        
        self.list_sua.append((
            ma_thanh_toan, ma_dat_cho, so_tien, phuong_thuc, 
            ngay_tt.strftime("%Y-%m-%d"), trang_thai
        ))
        
        self.clear_entries()
        messagebox.showinfo("Thành công", "Đã sửa thanh toán trong danh sách chờ lưu.")
    
    def Luu(self):
        cursor = self.db.conn.cursor()
        try:
            # INSERT
            for item in self.list_them:
                sql = """
                INSERT INTO THANHTOAN (MaThanhToan, MaDatCho, SoTien, PhuongThuc, NgayThanhToan, TrangThaiTT)
                VALUES (?, ?, ?, ?, ?, ?)
                """
                cursor.execute(sql, (item[0], item[1], float(item[2]), item[3], item[4], item[5]))
            
            # DELETE
            for ma_thanh_toan in self.list_xoa:
                sql = "DELETE FROM THANHTOAN WHERE MaThanhToan = ?"
                cursor.execute(sql, (ma_thanh_toan,))
            
            # UPDATE
            for item in self.list_sua:
                sql = """
                UPDATE THANHTOAN 
                SET MaDatCho=?, SoTien=?, PhuongThuc=?, NgayThanhToan=?, TrangThaiTT=?
                WHERE MaThanhToan=?
                """
                cursor.execute(sql, (item[1], float(item[2]), item[3], item[4], item[5], item[0]))
            
            cursor.commit()
            self.list_them.clear()
            self.list_xoa.clear()
            self.list_sua.clear()
            self.load_data()
            messagebox.showinfo("Thành công", "Đã lưu tất cả các thay đổi vào cơ sở dữ liệu.")
        except Exception as e:
            cursor.rollback()
            messagebox.showerror("Lỗi", f"Lỗi khi lưu dữ liệu: {e}")
            
    def TimKiem(self):
        # Lấy lựa chọn tìm kiếm từ Combobox
        loai_tim = self.cb_TimKiem.get().strip()
        tu_khoa = self.entry_TimKiem.get().strip().lower()  # chuyển về chữ thường để tìm không phân biệt hoa thường

        if not tu_khoa:
            messagebox.showwarning("Thông báo", "Vui lòng nhập từ khóa để tìm kiếm!")
            return

        # Xóa dữ liệu cũ trên Treeview
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Lấy tất cả dữ liệu từ database
        sql = "SELECT MaThanhToan, MaDatCho, SoTien, PhuongThuc, NgayThanhToan, TrangThaiTT FROM THANHTOAN"
        try:
            rows = self.db.query(sql)
            if rows:
                ketqua = []
                for row in rows:
                    # Chọn cột để so sánh dựa trên Combobox
                    if loai_tim == "Mã thanh toán":
                        cot_so_sanh = str(row[0])  # DiaDiem
                    elif loai_tim == "Mã đặt chỗ":
                        cot_so_sanh = str(row[1])  # TenTour
                    else:
                        cot_so_sanh = ""

                    # So sánh từ khóa
                    if tu_khoa in cot_so_sanh.lower():
                        ketqua.append(row)

                # Hiển thị kết quả
                for row in ketqua:
                    ngay_tt = ""
                    if row[4]:
                        ngay_tt = row[4].strftime("%d/%m/%Y") if hasattr(row[4], "strftime") else str(row[4])
                    
                    so_tien = row[2]                    
                    self.tree.insert("", "end", values=(
                        row[0], row[1], so_tien, row[3], ngay_tt, row[5]
                    ))
            else:
                messagebox.showinfo("Thông báo", "Không có dữ liệu trong cơ sở dữ liệu.")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi khi truy vấn dữ liệu:\n{e}")