from customtkinter import *
from tkinter import messagebox


class Create_TrangChu(CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="#FFFFFF")
        self.create_frameTop()
        
    def create_frameTop(self):
        self.frameTop = CTkFrame(self, height=200, fg_color="#243A83")
        self.frameTop.pack(side="top",fill="both", padx=5, pady=5)