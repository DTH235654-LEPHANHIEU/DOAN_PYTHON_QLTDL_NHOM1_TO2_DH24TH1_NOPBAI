from customtkinter import *
from tkinter import messagebox
from Form import FormDatChoAD
from Form import BaseForm, FormTuyenDi, FormKhachHang, FormDangNhap, FormHoaDon, FormNhanVien


class FormDashboard(CTkFrame):
    def __init__(self, root):
        super().__init__(root)      # Frame chính
        self.root = root
        self.root.geometry("1100x600")
        self.root.title("QUẢN LÝ TUYẾN DU LỊCH")
        self.root.resizable(True, True)
        set_appearance_mode("light")
        BaseForm.center_window(self.root)

        # ================================
        #       Giao diện chính
        # ================================
        self.create_left_menu()
        self.create_top_frame()
        self.current_page = None
        self.open_TuyenDi(None)
    # ----------------------------------------
    # TẠO MENU BÊN TRÁI
    # ----------------------------------------
    def create_left_menu(self):

        self.frame_left = CTkFrame(self.root, width=190, fg_color="#242861")
        self.frame_left.pack(side="left", fill="y", padx=5, pady=5)

        lbl_Logo = CTkLabel(self.frame_left, text="☲ TRAVEL",
                            text_color="#FFFFFF",
                            font=("Segoe UI", 24, "bold", "italic"))
        lbl_Logo.pack(fill="x", pady=30)

        # Danh sách nút để đổi màu khi chọn
        self.list_button = []

        # Tạo từng button

        if BaseForm.UserSession.is_admin():
        #btn dùng cho cả user và admin          
            self.btn_QuanLyTour = self.create_menu_button("🗺  Tuyến đi", self.open_TuyenDi)
            self.btn_QuanLyKhachHang = self.create_menu_button("👥  Khách hàng", self.open_KhachHang)
            self.btn_QuanLyHoaDon = self.create_menu_button("🧾  Hóa đơn", self.open_HoaDon)
            self.btn_QuanLyDichVu = self.create_menu_button("🛎  Đặt chỗ", self.open_DatCho_AD)
        if BaseForm.UserSession.is_admin():
            self.btn_QuanLyNhanVien = self.create_menu_button("👨‍💼  Nhân viên", self.open_NhanVien)
        self.btn_DangXuat = self.create_menu_button("📤  Đăng xuất", self.logout)
        

        # Tạo nút thoát
        btn_Thoat = CTkButton(
            self.frame_left,
            text="⬅️ Thoát",
            anchor="w",
            fg_color="#242861",
            text_color="#D4D1D1",
            hover_color="#1A1C4D",
            font=("Segoe UI", 14, "bold"),
            command=self.exit_app
        )
        btn_Thoat.pack(side="bottom", fill="x", pady=15)

    # Hàm tạo button + gán vào danh sách
    def create_menu_button(self, text, command):
        btn = CTkButton(
            self.frame_left,
            text=text,
            anchor="w",
            fg_color="#242861",
            text_color="#D4D1D1",
            hover_color="#1A1C4D",
            width=150,
            height=40,
            font=("Segoe UI", 14, "bold"),
            command=lambda b=text: command(b)
        )
        btn.pack(fill="x", pady=5)
        self.list_button.append(btn)
        return btn

    # ----------------------------------------
    # TẠO FRAME BÊN PHẢI
    # ----------------------------------------
    def create_top_frame(self):
        self.frame_content = CTkFrame(self.root, fg_color="#FFFFFF")
        self.frame_content.pack(side="left", fill="both",padx=5,pady=5, expand=True)

    # ----------------------------------------
    # ĐỔI MÀU KHI CHỌN BUTTON MENU
    # ----------------------------------------
    def select_button(self, btn):
        for b in self.list_button:
            b.configure(fg_color="#242861", text_color="#D4D1D1")
        btn.configure(fg_color="#FFFFFF", text_color="#000000")

    # ----------------------------------------
    # CÁC HÀM XỬ LÝ NÚT BẤM (TRANG)
    # ----------------------------------------

    def open_TuyenDi(self, b):
        self.select_button(self.btn_QuanLyTour)
        self.clear_content()
        if self.current_page is not None:
            self.current_page.destroy()
        self.current_page = FormTuyenDi.Create_TuyenDi(self.frame_content)
        self.current_page.pack(fill="both", expand=True)

    def open_KhachHang(self, b):
        self.select_button(self.btn_QuanLyKhachHang)
        self.clear_content()
        if self.current_page is not None:
            self.current_page.destroy()
        self.current_page = FormKhachHang.Create_KhachHang(self.frame_content)
        self.current_page.pack(fill="both", expand=True)

    def open_HoaDon(self, b):
        self.select_button(self.btn_QuanLyHoaDon)
        self.clear_content()
        if self.current_page is not None:
            self.current_page.destroy()
        self.current_page = FormHoaDon.Create_HoaDon(self.frame_content)
        self.current_page.pack(fill="both", expand=True)

    def open_DatCho_AD(self, b):
        self.select_button(self.btn_QuanLyDichVu)
        self.clear_content()
        if self.current_page is not None:
            self.current_page.destroy()
        self.current_page = FormDatChoAD.Create_DatCho(self.frame_content)
        self.current_page.pack(fill="both", expand=True)
        
    def open_NhanVien(self, b):
        self.select_button(self.btn_QuanLyNhanVien)
        self.clear_content()
        if self.current_page is not None:
            self.current_page.destroy()
        self.current_page = FormNhanVien.Create_NhanVien(self.frame_content)
        self.current_page.pack(fill="both", expand=True)

    def logout(self, b):
        self.select_button(self.btn_DangXuat)
        result = messagebox.askquestion("Thông báo","Bạn có muốn đăng xuất")
        if result == "yes":
            for widget in self.root.winfo_children():
                widget.destroy()
            FormDangNhap.Create_DangNhap(self.root)

    def exit_app(self):
        result = messagebox.askyesno("Thông báo", "Bạn có muốn thoát?")
        if result:
            self.root.destroy()

    # ----------------------------------------
    # XÓA FRAME NỘI DUNG MỖI KHI ĐỔI TRANG
    # ----------------------------------------
    def clear_content(self):
        for w in self.frame_content.winfo_children():    
            w.destroy()
