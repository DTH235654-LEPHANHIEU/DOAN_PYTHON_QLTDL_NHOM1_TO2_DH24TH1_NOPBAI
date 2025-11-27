def Luu(self):
    if not self.tree.get_children():
        messagebox.showwarning("Thông báo", "Không có dữ liệu để lưu!")
        return

    confirm = messagebox.askyesno("Xác nhận", 
        "Thao tác này sẽ XÓA TOÀN BỘ dữ liệu cũ trong database và thay thế bằng dữ liệu mới.\nBạn có chắc chắn?")
    if not confirm:
        return

    cursor = self.db.conn.cursor()
    
    try:
        # XÓA HẾT dữ liệu cũ
        cursor.execute("DELETE FROM TOUR")
        
        inserts = []
        invalid_rows = []

        for idx, item_id in enumerate(self.tree.get_children(), 1):
            values = self.tree.item(item_id, "values")
            
            try:
                ma_tour = str(values[0]).strip()
                ten_tour = str(values[1]).strip()
                dia_diem = str(values[2]).strip()
                mo_ta = str(values[3]).strip()
                
                # Chỉ cần parse 1 định dạng duy nhất: dd/mm/yyyy
                ngay_str = str(values[4]).strip()
                ngay_khoihanh = datetime.strptime(ngay_str, "%d/%m/%Y").date()
                
                socho_toi_da = int(str(values[5]).strip())
                socho_da_dat = int(str(values[6]).strip())
                gia_nguoilon = float(str(values[7]).strip())
                gia_treem = float(str(values[8]).strip())
                thoi_luong = int(str(values[9]).strip())

                inserts.append((ma_tour, ten_tour, dia_diem, mo_ta, ngay_khoihanh,
                              socho_toi_da, socho_da_dat, gia_nguoilon, gia_treem, thoi_luong))
            
            except (ValueError, TypeError, IndexError) as e:
                tour_id = values[0] if len(values) > 0 else 'N/A'
                invalid_rows.append(f"Tour {tour_id} (dòng {idx}): {str(e)}")

        # Thông báo lỗi nếu có
        if invalid_rows:
            error_msg = f"Có {len(invalid_rows)} dòng bị lỗi:\n\n" + "\n".join(invalid_rows[:5])
            if len(invalid_rows) > 5:
                error_msg += f"\n... và {len(invalid_rows)-5} lỗi khác"
            
            if not messagebox.askyesno("Cảnh báo", error_msg + "\n\nTiếp tục lưu các dòng hợp lệ?"):
                self.db.conn.rollback()
                return

        # INSERT dữ liệu mới
        if inserts:
            cursor.executemany("""
                INSERT INTO TOUR (MaTour, TenTour, DiaDiem, MoTa, NgayKhoiHanh,
                SoChoToiDa, SoChoDaDat, GiaNguoiLon, GiaTreEm, ThoiLuong)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, inserts)
            
            self.db.conn.commit()
            messagebox.showinfo("Thành công", 
                f"Lưu thành công {len(inserts)} tour!" +
                (f"\nBỏ qua {len(invalid_rows)} dòng lỗi" if invalid_rows else ""))
        else:
            messagebox.showwarning("Cảnh báo", "Không có dòng nào hợp lệ để lưu!")
            self.db.conn.rollback()

    except Exception as e:
        self.db.conn.rollback()
        messagebox.showerror("Lỗi", f"Lỗi khi lưu:\n{str(e)}")
    finally:
        cursor.close()