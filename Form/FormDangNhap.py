from customtkinter import *
from tkinter import messagebox
from pathlib import Path
from PIL import Image, ImageTk
from Form import BaseForm


class Create_DangNhap:
    def __init__(self, root, on_exit_callback=None):
        self.root = root
        self.on_exit_callback = on_exit_callback

        self.root.title("Đăng nhập hệ thống")
        self.root.geometry("600x400")
        self.root.resizable(False, False)
        set_appearance_mode("light")
        BaseForm.center_window(self.root)

        self.Folder = Path("D:\\CNTT\\Năm 3 - Kì 1\\Python\\DoAn\\DOAN_PYTHON\\Anh")

        self.create_widgets()

    # TẠO GIAO DIỆN
    def create_widgets(self):

        # ===== ẢNH =====
        imgNen = Image.open(self.Folder / "Nen1.jpg")
        imgNen = imgNen.resize((250, 400))
        self.photo_Nen = ImageTk.PhotoImage(imgNen)

        self.Label_imgNen = CTkLabel(self.root, image=self.photo_Nen, width=250, height=400, text=" ")
        self.Label_imgNen.place(x=0, y=0)

        # ===== TEXT =====
        self.lable_Signin = CTkLabel(self.root, text="Hello there,", text_color="#000000",
                                     font=("Segoe UI", 18, "italic"))
        self.lable_Signin.place(x=300, y=50)

        self.lable_Welcome = CTkLabel(self.root, text="Welcome back", text_color="#000000",
                                      font=("Segoe UI", 20, "bold"))
        self.lable_Welcome.place(x=300, y=80)

        # ===== USERNAME =====
        CTkLabel(self.root, text="Username", text_color="#000000",
                 font=("Segoe UI", 14, "bold")).place(x=300, y=130)

        self.entry_Username = CTkEntry(self.root, width=250, fg_color="#D9D9D9",
                                       font=("Segoe UI", 15, "bold"))
        self.entry_Username.place(x=300, y=160)

        # ===== PASSWORD =====
        CTkLabel(self.root, text="Password", text_color="#000000",
                 font=("Segoe UI", 14, "bold")).place(x=300, y=190)

        self.entry_Password = CTkEntry(self.root, show="•", width=250, fg_color="#D9D9D9",
                                       font=("Segoe UI", 15, "bold"))
        self.entry_Password.place(x=300, y=220)

        # Checkbox hiển thị mật khẩu
        self.checkHienthi = IntVar()
        self.checkbutton_Hienthi = CTkCheckBox(
            self.root,
            text="Hiển thị mật khẩu",
            text_color="#000000",
            variable=self.checkHienthi,
            font=("Segoe UI", 12),
            command=self.HienThi
        )
        self.checkbutton_Hienthi.place(x=300, y=270)

        # ===== BUTTON ĐĂNG NHẬP =====
        
        self.BtnDangNhap = CTkButton(
            self.root,
            text="Đăng nhập",
            text_color="#FFFFFF",
            fg_color="#000000",
            font=("Segoe UI", 12, "bold"),
            width=120,
            command=self.DangNhap
        )
        self.BtnDangNhap.place(x=300, y=310)

        # ===== BUTTON THOÁT =====
        
        self.btnThoat = CTkButton(
            self.root,
            text="Thoát",
            text_color="#FFFFFF",
            fg_color="#000000",
            font=("Segoe UI", 12, "bold"),
            width=120,
            command=self.Thoat
        )
        self.btnThoat.place(x=430, y=310)

        # Enter để đăng nhập
        self.entry_Password.bind("<Return>", lambda e: self.DangNhap())

    # HÀM: HIỂN THỊ / ẨN MẬT KHẨU

    def HienThi(self):
        if self.checkHienthi.get() == 1:
            self.entry_Password.configure(show="")
        else:
            self.entry_Password.configure(show="•")
            
    # HÀM: ĐĂNG NHẬP
    
    def DangNhap(self):
        username = self.entry_Username.get()
        password = self.entry_Password.get()

        if not username or not password:
            messagebox.showwarning("Thông báo", "Tài khoản hoặc mật khẩu chưa được nhập")
            return
        try:
            db = BaseForm.ConectionDatabase()
            sql = "SELECT * FROM TAIKHOAN WHERE TenDangNhap = ? AND MatKhau = ?"
            params=(username, password)
            
            result = db.query(sql, params)
            if result:
                user_role = "admin" if username.lower() == "admin" else "User"
                #lưu thông tin người dùng
                BaseForm.UserSession.set_user(username, user_role)
                # Xóa hết widget cũ
                for widget in self.root.winfo_children():
                    widget.destroy()

                # Mở Dashboard
                from Form import FormDashboard
                FormDashboard.FormDashboard(self.root)
            else:
                # Nếu result rỗng => Sai thông tin
                messagebox.showerror("Lỗi", "Tên đăng nhập hoặc mật khẩu không đúng!")           
        except Exception as e:
            messagebox.showerror("Lỗi Hệ Thống", f"Không thể kết nối đến CSDL.\nChi tiết: {e}")

    # -----------------------------
    # HÀM: THOÁT
    # -----------------------------
    def Thoat(self):
        result = messagebox.askyesno("Thông báo", "Bạn có muốn thoát")
        if result:
            self.root.destroy()
