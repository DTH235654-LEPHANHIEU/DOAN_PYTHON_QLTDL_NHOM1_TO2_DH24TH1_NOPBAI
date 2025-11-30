from customtkinter import *
from tkinter import messagebox, ttk
from Form import FormNhanVien
from Form import BaseForm
from tkcalendar import DateEntry
from datetime import datetime

class Create_TuyenDi(CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="#FFFFFF")
        
        self.db = BaseForm.ConnectionDatabase()
        self.Create_frameBottom()
        self.Create_frameTop()
        self.load_data()
        self.load_data_cbTimKiem()
        
        self.list_them = []
        self.list_xoa = []
        self.list_sua = []
 
 
#--------------------------------------
# TREE VIEW 
#--------------------------------------         
    def Create_frameBottom(self):
        self.frameBottom = CTkFrame(self, height=400, fg_color="#FFFFFF")
        self.frameBottom.pack(side="bottom", fill="x")
        
        columns = ("MaTuyen", "TenTuyen", "TenDiaDiem", "MoTa", "NgayKhoiHanh", "SoChoToiDa", "SoChoDaDat", "GiaNguoiLon", "GiaTreEm", "Thoiluong")
        self.tree = ttk.Treeview(self.frameBottom, columns=columns, show="headings")
  
        # Thanh cuộn
        scrollbar_y = CTkScrollbar(self.frameBottom, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar_y.set)
        
        scrollbar_x = CTkScrollbar(self.frameBottom, command=self.tree.xview, orientation="horizontal")
        self.tree.configure(xscrollcommand=scrollbar_x.set)
        
        scrollbar_y.pack(side="right", fill="y")
        scrollbar_x.pack(side="bottom", fill="x")
        self.tree.pack(side="left", fill="both", expand=True)
        #Màu của heading
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
        #Tên cột và độ rộng
        cols = [
            ("MaTuyen","Mã tuyến",100,"center"),
            ("TenTuyen","Tên tuyến",290,"w"),
            ("TenDiaDiem","Tên địa điểm",100,"w"),
            ("MoTa","Mô tả",500,"w"),
            ("NgayKhoiHanh","Ngày khởi hành",100,"center"),
            ("SoChoToiDa","Chỗ tối đa",100,"center"),
            ("SoChoDaDat","Chỗ đã đặt",100,"center"),
            ("GiaNguoiLon","Giá người lớn",110,"e"),
            ("GiaTreEm","Giá trẻ em",110,"e"),
            ("Thoiluong","Số Ngày",60,"center")
        ]

        for col, text, width, anchor in cols:
            self.tree.heading(col, text=text)
            self.tree.column(col, width=width, anchor=anchor, stretch=False)  
   
            
#--------------------------------------
# CÁC LABEL VÀ ENTRY
#-------------------------------------- 
    def Create_frameTop(self):
        self.frameTop = CTkFrame(self,width=400, height=300, fg_color="#FFFFFF")
        self.frameTop.pack(side="top", fill="both", expand=True)
        
        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)
            
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
        self.lb_NgayKhoihanh = CTkLabel(self.frameTop, text= "Ngày khởi hành", font=("Segoe UI", 14))
        self.lb_NgayKhoihanh.place(x=20, y = 220)
        self.date_NgayKhoihanh = DateEntry(self.frameTop, width=38, height=20, date_pattern="dd/mm/yyyy")
        self.date_NgayKhoihanh.place(x=120, y=225)        
    #Mota
        self.lb_MoTa = CTkLabel(self.frameTop, text= "Mô tả", font=("Segoe UI", 14))
        self.lb_MoTa.place(x=20, y = 260)
        self.entry_Mota = CTkEntry(self.frameTop, width=250, height=20)
        self.entry_Mota.place(x=120, y=265)        
    #SoChoToiDa
        self.lb_ChoToiDa = CTkLabel(self.frameTop, text= "Số chỗ tối đa", font=("Segoe UI", 14))
        self.lb_ChoToiDa.place(x=400, y = 100)
        self.entry_ChoToiDa = CTkEntry(self.frameTop, width=250, height=20)
        self.entry_ChoToiDa.place(x=510, y=105)         
    #SoChoConLai
        self.lb_ChoDaDat = CTkLabel(self.frameTop, text= "Số chỗ đã đặt", font=("Segoe UI", 14))
        self.lb_ChoDaDat.place(x=400, y = 140)
        self.entry_ChoDaDat = CTkEntry(self.frameTop, width=250, height=20)
        self.entry_ChoDaDat.place(x=510, y=145) 
    #GiaNguoiLon
        self.lb_GiaNguoiLon = CTkLabel(self.frameTop, text= "Giá người lớn", font=("Segoe UI", 14))
        self.lb_GiaNguoiLon.place(x=400, y = 180)
        self.entry_GiaNguoiLon = CTkEntry(self.frameTop, width=250, height=20)
        self.entry_GiaNguoiLon.place(x=510, y=185)         
    #GiaTreEm      
        self.lb_GiaTreEm = CTkLabel(self.frameTop, text= "Giá Trẻ em", font=("Segoe UI", 14))
        self.lb_GiaTreEm.place(x=400, y = 220)
        self.entry_GiaTreEm = CTkEntry(self.frameTop, width=250, height=20)
        self.entry_GiaTreEm.place(x=510, y=225) 
    #SoNgay
        self.lb_SoNgay = CTkLabel(self.frameTop, text= "Số ngày", font=("Segoe UI", 14))
        self.lb_SoNgay.place(x=400, y = 260)
        self.entry_SoNgay = CTkEntry(self.frameTop, width=250, height=20)
        self.entry_SoNgay.place(x=510, y=265)     
#--------------------------------------
# CHỨC NĂNG TÌM KIẾM
#--------------------------------------    
        self.cb_TimKiem = CTkComboBox(self.frameTop, width=130, height= 20)
        self.cb_TimKiem.place(x=380, y = 315)
        
        self.entry_TimKiem = CTkEntry(self.frameTop, width=330, height=20, fg_color="#FFFFFF")
        self.entry_TimKiem.place(x =520, y=315)
        
        self.btn_Timkiem = CTkButton(self.frameTop, width=40, height=14, text="🔍",
                                     font=("Segoe UI", 14, "bold"),
                                     text_color="#FFFFFF", command=self.TimKiem)
        self.btn_Timkiem.place(x=855,y=314)   
#--------------------------------------
# TẠO CÁC BUTTON
#--------------------------------------    
    #Đặt chỗ
        if BaseForm.UserSession.is_user():
            self.btn_DatCho = CTkButton(self.frameTop, width=70, height=25, text="➕ Đặt chỗ",
                                    fg_color="#1D8D13", font=("Segoe UI", 14, "bold"), command=self.open_form_dat_cho)
            self.btn_DatCho.place(x=20, y = 315)
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

    #--------------------------------------
    # CÁC HÀM CHỨC NĂNG CỦA CHƯƠNG TRÌNH
    #-------------------------------------- 

    def open_form_dat_cho(self):
        try:
            form = FormNhanVien.Create_DatCho()
            form.mainloop()
        except Exception as e:
            print(f"Lỗi mở form đặt chỗ: {e}")

    def load_data_cbTimKiem(self):
        list = ["Mã tuyến","Tên địa điểm", "Tên tuyến đi", "Số ngày"]
        self.cb_TimKiem.configure(values=[])
        self.cb_TimKiem.configure(values=list)
        if list:
            self.cb_TimKiem.set(list[0])

    def load_data(self):
            # 1. Xóa dữ liệu cũ trên bảng Treeview
            for item in self.tree.get_children():
                self.tree.delete(item)
            
            sql = "SELECT MaTour, TenTour, DiaDiem, MoTa, NgayKhoiHanh,SoChoToiDa, SoChoDaDat, GiaNguoiLon, GiaTreEm, ThoiLuong FROM TOUR"
            
            try:
                rows = self.db.query(sql) # Giả sử self.db.query trả về list các tuple
                if rows:
                    for row in rows:                
                        ma_tour = row[0]
                        ten_tour = row[1]
                        dia_diem = row[2]
                        mo_ta = row[3]
                        
                        ngay_khoihanh = row[4] 
                        if hasattr(ngay_khoihanh, 'strftime'):
                            ngay_khoihanh = ngay_khoihanh.strftime('%d/%m/%Y')
                        
                        cho_toida = row[5]
                        cho_dadat = row[6]
                        gia_nguoilon = row[7] # Format tiền tệ
                        gia_treem = row[8]
                        thoi_luong = row[9]       
                        self.tree.insert("", "end", values=(ma_tour, ten_tour, dia_diem, mo_ta, ngay_khoihanh, cho_toida, cho_dadat, gia_nguoilon, gia_treem, thoi_luong))
                else:
                        print("Không có dữ liệu hiển thị trong TreeView")
            except Exception as e:
                messagebox.showerror("Lỗi", f"Lỗi truy vấn dữ liệu: {e}")

    def on_tree_select(self, event):
        self.clear_entries()
        selected_item = self.tree.selection()
        if selected_item:
            values = self.tree.item(selected_item[0], "values")
                
            # Đổ dữ liệu ngược lại vào các ô nhập liệu
            self.entry_MaTuyen.insert(0, values[0].strip()) 
            self.entry_TenTuyen.insert(0, str(values[1].strip()))  
            self.entry_TenDiaDiem.insert(0, str(values[2].strip()))         
            self.entry_Mota.insert(0, str(values[3].strip()))     
            try:
                self.date_NgayKhoihanh.set_date(values[4].strip())  
            except:
                pass 
            self.entry_ChoToiDa.insert(0, values[5])        # SoChoToiDa
            self.entry_ChoDaDat.insert(0, values[6])         
            self.entry_GiaNguoiLon.insert(0, values[7])
            self.entry_GiaTreEm.insert(0, values[8])
            self.entry_SoNgay.insert(0, str(values[9]))

    def clear_entries(self):
        self.entry_MaTuyen.delete(0, 'end')
        self.entry_TenTuyen.delete(0, 'end')
        self.entry_TenDiaDiem.delete(0, "end")
        self.entry_Mota.delete(0, 'end')
        self.entry_ChoToiDa.delete(0, 'end')
        self.entry_ChoDaDat.delete(0, 'end')
        self.entry_GiaNguoiLon.delete(0, 'end')
        self.entry_GiaTreEm.delete(0, 'end')
        self.entry_SoNgay.delete(0, 'end')
        self.entry_TenTuyen.focus_set() # Focus vào tên tour vì Mã Tour tự động

    def Them(self):
        # Lấy dữ liệu từ giao diện
        ma_tour = self.entry_MaTuyen.get().strip()
        ten_tour = self.entry_TenTuyen.get().strip()
        dia_diem = self.entry_TenDiaDiem.get().strip()
        mo_ta = self.entry_Mota.get().strip()
            
        date_obj = self.date_NgayKhoihanh.get_date()
        ngay_khoihanh = date_obj.strftime("%d/%m/%Y")

        thoi_luong = self.entry_SoNgay.get().strip()
        gia_nguoilon = self.entry_GiaNguoiLon.get().strip()
        gia_treem = self.entry_GiaTreEm.get().strip()
        cho_toida = self.entry_ChoToiDa.get().strip()
        cho_dadat = self.entry_ChoDaDat.get().strip()
            
        # Mã tour kh được trống
        if ten_tour == "":
            messagebox.showwarning("Thông báo", "Tên tour không được để trống!")
            return
        #Số ngày, chỗ tối đa, chỗ đã đặt phải là số nguyên
        if not thoi_luong.isdigit() or not cho_toida.isdigit() or not cho_dadat.isdigit():
            messagebox.showwarning("Thông báo", "Thời lượng, Số chỗ phải là số nguyên!")
            return
        #Kiểm tra mã tuyến không được trùng
        for item_id in self.tree.get_children():
            values = self.tree.item(item_id, "values")
            if str(values[0]).strip() == ma_tour:
                messagebox.showwarning("Thông báo", f"Mã tour '{ma_tour}' đã tồn tại!")
                return
        self.tree.insert("", "end", values=(ma_tour, ten_tour, dia_diem, mo_ta, ngay_khoihanh, cho_toida, cho_dadat, gia_nguoilon, gia_treem, thoi_luong))
        ngay_khoihanh = date_obj.strftime("%Y%m%d")
        self.list_them.append((ma_tour, ten_tour, dia_diem, mo_ta, ngay_khoihanh, cho_toida, cho_dadat, gia_nguoilon, gia_treem, thoi_luong))
        messagebox.showinfo("Thông báo", "Thêm tour thành công!")
        self.clear_entries()

    def Xoa(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Thông báo", "Vui lòng chọn tour cần xóa")
            return
                
        # Lấy MaTour từ dòng đã chọn (cột đầu tiên - index 0)
        values = self.tree.item(selected[0], "values")
        ma_tour = values[0]
            
        confirm = messagebox.askyesno("Xác nhận", f"Bạn có chắc muốn xóa Tour ID: {ma_tour}?")
        if confirm:
            self.list_xoa.append(ma_tour)
            self.tree.delete(selected[0])
            messagebox.showinfo("Thông báo", "Xóa thành công")
            self.clear_entries()

    def Sua(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Thông báo", "Vui lòng chọn tour để sửa")
            return

        item_id = selected[0]

        # Lấy mã tour gốc từ Treeview
        values_goc = self.tree.item(item_id, "values")
        ma_tour_cu = str(values_goc[0]).strip()

        # Lấy mã tour mới từ Entry
        ma_tour_moi = self.entry_MaTuyen.get().strip()

        # Không cho phép đổi mã tour
        if ma_tour_moi != ma_tour_cu:
            messagebox.showwarning("Lỗi", "Không được phép thay đổi mã tour!")
            return

        # Lấy dữ liệu mới
        ten_tour = self.entry_TenTuyen.get().strip()
        dia_diem = self.entry_TenDiaDiem.get().strip()
        mo_ta = self.entry_Mota.get().strip()

        date_obj = self.date_NgayKhoihanh.get_date()
        ngay_khoihanh = date_obj.strftime("%d/%m/%Y")

        thoi_luong = self.entry_SoNgay.get().strip()
        gia_nguoilon = self.entry_GiaNguoiLon.get().strip()
        gia_treem = self.entry_GiaTreEm.get().strip()
        cho_toida = self.entry_ChoToiDa.get().strip()
        cho_dadat = self.entry_ChoDaDat.get().strip()

        if ten_tour == "":
            messagebox.showwarning("Lỗi", "Tên tour không được để trống")
            return
        self.tree.item(item_id, values=(ma_tour_cu, ten_tour, dia_diem, mo_ta, ngay_khoihanh, cho_toida, cho_dadat, gia_nguoilon, gia_treem, thoi_luong))
        #sql kh nhan dinh dang ngay dd-mm-yyyy(chuyen dinh dang)
        ngay_khoihanh = date_obj.strftime("%Y%m%d")
        self.list_sua.append((ma_tour_cu, ten_tour, dia_diem, mo_ta, ngay_khoihanh, cho_toida, cho_dadat, gia_nguoilon, gia_treem, thoi_luong))
        messagebox.showinfo("Thông báo", "Sửa tour thành công!")

    def Luu(self):
        if not self.tree.get_children():
            messagebox.showwarning("Thông báo", "Không có dữ liệu để lưu!")
            return
        
        cursor = self.db.conn.cursor()
        #INSERT
        for row in self.list_them:
            cursor.execute("""INSERT INTO TOUR 
                              (MaTour, TenTour, DiaDiem, MoTa, NgayKhoiHanh,SoChoToiDa, SoChoDaDat, GiaNguoiLon, GiaTreEm, ThoiLuong)
                              VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                              (row["MaTour"], row["TenTour"], row["DiaDiem"], row["MoTa"], row["NgayKhoiHanh"],
                              row["SoChoToiDa"], row["SoChoDaDat"], row["GiaNguoiLon"], row["GiaTreEm"], row["ThoiLuong"]))
        #UPDATE
        for row in self.list_sua:
            cursor.execute("""UPDATE TOUR SET
                                TenTour = ?, DiaDiem = ?, MoTa = ?, NgayKhoiHanh = ?,
                                SoChoToiDa = ?, SoChoDaDat = ?, GiaNguoiLon = ?, GiaTreEm = ?, ThoiLuong = ?
                              WHERE MaTour = ?    
                           """, 
                           (row["TenTour"], row["DiaDiem"], row["MoTa"], row["NgayKhoiHanh"],
                            row["SoChoToiDa"], row["SoChoDaDat"], row["GiaNguoiLon"], row["GiaTreEm"], row["ThoiLuong"],
                            row["MaTour"]))
        for ma in self.list_xoa:
            cursor.execute("DELETE FROM TOUR WHERE MaTour = ?", (ma,))
        count = cursor.fetchone()[0]
        if count > 0:
            messagebox.showwarning("Không thể xóa", "Tour này đã có khách đặt! Không thể xóa.")
            return
        cursor. commit()  

        messagebox.showinfo("Thông báo", "Lưu dữ liệu xuống Database thành công!")  
        
        self.list_them.clear()
        self.list_sua.clear()
        self.list_xoa.clear()


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
        sql = "SELECT MaTour, TenTour, DiaDiem, MoTa, NgayKhoiHanh, SoChoToiDa, SoChoDaDat, GiaNguoiLon, GiaTreEm, ThoiLuong FROM TOUR"
        try:
            rows = self.db.query(sql)
            if rows:
                ketqua = []
                for row in rows:
                    # Chọn cột để so sánh dựa trên Combobox
                    if loai_tim == "Tên địa điểm":
                        cot_so_sanh = str(row[2])  # DiaDiem
                    elif loai_tim == "Tên tuyến đi":
                        cot_so_sanh = str(row[1])  # TenTour
                    elif loai_tim == "Số ngày":
                        cot_so_sanh = str(row[9])  # ThoiLuong
                    elif loai_tim == "Mã tuyến":
                        cot_so_sanh = str(row[0])
                    else:
                        cot_so_sanh = ""

                    # So sánh từ khóa
                    if tu_khoa in cot_so_sanh.lower():
                        ketqua.append(row)

                # Hiển thị kết quả
                for row in ketqua:
                    ngay_khoihanh = row[4]
                    if hasattr(ngay_khoihanh, 'strftime'):
                        ngay_khoihanh = ngay_khoihanh.strftime('%d/%m/%Y')
                    self.tree.insert("", "end", values=(row[0], row[1], row[2], row[3], ngay_khoihanh,
                                                        row[5], row[6], row[7], row[8], row[9]))
            else:
                messagebox.showinfo("Thông báo", "Không có dữ liệu trong cơ sở dữ liệu.")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi khi truy vấn dữ liệu:\n{e}")
