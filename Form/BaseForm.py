from customtkinter import CTk
from tkinter import messagebox
import pyodbc

#Kết nối với Database
class ConectionDatabase:
    def __init__(self):
        try:
            self.conn = pyodbc.connect(
                "Driver={ODBC Driver 17 for SQL Server};"
                "Server=DESKTOP-8P2GBHE\MSSQLSERVER1;"
                "Database=QLTDL;"
                "Trusted_Connection=yes;"
            )
            self.cursor = self.conn.cursor()   
        except Exception as e:
            print(e)
    
    def query(self, sql, params=None):
        try:
            if params:
                self.cursor.execute(sql, params)
            else:
                self.cursor.execute(sql)
            return self.cursor.fetchall()
        except Exception as e:
            print(e)
            return []

    # INSERT – UPDATE – DELETE
    def execute(self, sql, params=None):
        try:
            if params:
                self.cursor.execute(sql, params)
            else:
                self.cursor.execute(sql)
            self.conn.commit()
            return True
        except Exception as e:
            print(e)
            return False
#Lưu thông tin người dùng hiện tại
class UserSession:
    current_user = None
    user_role = None
    #classmethod: Phương thức thuộc về class
    @classmethod
    def set_user(cls, username, role):
        cls.current_user = username
        cls.user_role = role    
    @classmethod
    def clear_user(cls):
        cls.current_user = None
        cls.user_role = None
    @classmethod
    def is_admin(cls):
        return cls.user_role and cls.user_role.lower() == "admin"
    @classmethod
    def is_user(cls):
        """Kiểm tra có phải user không"""
        return cls.user_role and cls.user_role.lower() == 'user'    
    
#Điều chỉnh cửa sổ ở giữa màn hình       
def center_window(self, width: int = None, height: int = None):
        """Đặt cửa sổ ở giữa màn hình"""
        self.update_idletasks()
        
        if width is None:
            width = self.winfo_width()
        if height is None:
         height = self.winfo_height()
        
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')
