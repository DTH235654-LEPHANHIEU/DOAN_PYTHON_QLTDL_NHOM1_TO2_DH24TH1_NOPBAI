from customtkinter import *
from Form import FormDangNhap


def main():   
    root = CTk()
    FormDangNhap.Create_DangNhap(root)
    root.mainloop()

if __name__ == "__main__":
    main() 