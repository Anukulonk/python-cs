import sys, os
import sqlite3
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QTableWidgetItem

DB_PATH = os.path.join(os.path.dirname(__file__), 'durable_a.db')

def init_db():
    conn = sqlite3.connect(DB_PATH)
    try:
        cur = conn.cursor()
        cur.execute("""
                    CREATE TABLE IF NOT EXISTS profile(
                    id  BLOB PRIMARY KEY NOT NULL,
                    da_id  BLOB,
                    da_name   BLOB,
                    da_detail    BLOB,
                    da_room    BLOB,
                    da_locate   BLOB)""")
        conn.commit()
    finally:
        conn.close()

class DurableForm(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('durable_articles_form.ui', self)

        init_db()

        self.pushButton.clicked.connect(self.saveData)
        #Load Data
        self.loadData()

        self.tableWidget.cellClicked.connect(self.on_row_clicked)

        self.btn_edit.clicked.connect(self.update_record)

        self.btn_delete.clicked.connect(self.delete_record)

    def on_row_clicked(self, row, column):
        id = self.tableWidget.item(row, 0).text() if self.tableWidget.item(row, 0) else ""
        da_id  = self.tableWidget.item(row, 1).text() if self.tableWidget.item(row, 1) else ""
        da_name  = self.tableWidget.item(row, 2).text() if self.tableWidget.item(row, 2) else ""
        da_detail  = self.tableWidget.item(row, 3).text() if self.tableWidget.item(row, 3) else ""
        da_room  = self.tableWidget.item(row, 4).text() if self.tableWidget.item(row, 4) else ""
        da_locate  = self.tableWidget.item(row, 5).text() if self.tableWidget.item(row, 5) else ""

        self.lineEdit.setText(id)
        self.lineEdit_2.setText(da_id)
        self.lineEdit_3.setText(da_name)
        self.lineEdit_4.setText(da_detail)
        self.lineEdit_5.setText(da_room)
        self.lineEdit_6.setText(da_locate)


    def saveData(self):
        id = self.lineEdit.text()
        da_id = self.lineEdit_2.text()
        da_name = self.lineEdit_3.text()
        da_detail = self.lineEdit_4.text()
        da_room = self.lineEdit_5.text()
        da_locate = self.lineEdit_6.text()

        #### INSERT TO DATYABASE ####
        if not all ([id, da_id, da_name, da_detail, da_room, da_locate]):
            QMessageBox.warning(self, "ข้อมูลไม่ครบถ้วน", "กรุณากรอกข้อมูลให้ครบทุกช่อง")
            return
        try:
            conn = sqlite3.connect(DB_PATH)
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO profile (id, da_id, da_name, da_detail, da_room, da_locate) VALUES (?, ?, ?, ?, ?, ?)",
                (id, da_id, da_name, da_detail, da_room, da_locate)
            )
            conn.commit()
        except Exception as e:
            QMessageBox.critical(self, "บันทึกข้อมูล ล้มเหลว" , f"เกิดข้อผิดพลาด\n{e}")
            return
        finally:
            conn.close()

        QMessageBox.information(self, "สำเร็จ", "บันทึกข้อมูลสำเร็จ")
        self.loadData()



        #############################

        QMessageBox.information(
            self,
            "ข้อมูลครุภัณฑ์สาขาวิชาวิทยาการคอมพิวเตอร์",
            f"รหัส: {id}\n"
            f"รหัสครุภัณฑ์: {da_id}\n"
            f"ชื่อครุภัณฑ์: {da_name}\n"
            f"รายละเอียด: {da_detail}\n"
            f"ห้อง/อาคาร: {da_room}\n"
            f"พิกัด: {da_locate}"
        )


    def loadData(self):
        try:
            conn = sqlite3.connect(DB_PATH)
            cur = conn.cursor()
            cur.execute("SELECT * FROM profile")
            rows = cur.fetchall()
        except Exception as e:
            QMessageBox.critical(self, "โหลดข้อมูลล้มเหลว", f"เกิดความผิดพลาด\n{e}")
            return
        finally:
            conn.close()

        #กำหนดแถว
        self.tableWidget.setRowCount(len(rows))
        self.tableWidget.setColumnCount(6)
        self.tableWidget.setHorizontalHeaderLabels(['รหัส', 'รหัสครุภัณฑ์', 'ชื่อครุภัณฑ์', 'รายละเอียด', 'ห้อง/อาคาร', 'พิกัด'])

        #load ข้อมูลมาทีละแถว
        for r,row in enumerate(rows):
            for c, val in enumerate(row):
                self.tableWidget.setItem(r, c, QtWidgets.QTableWidgetItem(str(val)))

        self.tableWidget.resizeColumnsToContents()


    def delete_record(self):
        code = self.lineEdit.text().strip()
        if not code:
            QMessageBox.warning(self, "ไม่พบรหัส", "กรุณาเลือกรายการจากตารางก่อน")
            return

        confirm = QMessageBox.question(self, "ยืนยันการลบ", f"ต้องการลบข้อมูลหรือไม่ '{code}' ใช่หรือไม่ ",
        QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if confirm != QMessageBox.Yes:
            return

        try:
            conn = sqlite3.connect(DB_PATH)
            cur = conn.cursor()
            cur.execute("DELETE FROM profile WHERE id = ?", (code,)) ##SQL
            conn.commit()
            QMessageBox.information(self, "สำเร็จ", "ลบข้อมูลเรียบร้อย")
        except Exception as e:
            QMessageBox.critical(self, "ลบข้อมูลล้มเหลว", f"เกิดความผิดพลาด\n{e}")
        finally:
            conn.close()
            self.loadData()

    def update_record(self):
        id = self.lineEdit.text().strip()
        da_id = self.lineEdit_2.text().strip()
        da_name = self.lineEdit_3.text().strip()
        da_detail = self.lineEdit_4.text().strip()
        da_room = self.lineEdit_5.text().strip()
        da_locate = self.lineEdit_6.text().strip()

        if not id:
            QMessageBox.warning(self, "ไม่พบรหัส", "กรุณาเลือกรายการจากตารางก่อน")
            return

        if not (da_id and da_name and da_detail and da_room and da_locate):
            QMessageBox.warning(self, "ข้อมูลไม่ครบ", "กรุณากรอกข้อมูลใหม่")
            return

        try:
            conn = sqlite3.connect(DB_PATH)
            cur = conn.cursor()
            cur.execute("""
                UPDATE profile
                SET da_id=?, da_name=?, da_detail=?, da_room=?, da_locate=?
                WHERE id=?
            """, (da_id, da_name, da_detail, da_room, da_locate, id))
            conn.commit()
            QMessageBox.information(self, "สำเร็จ", "แก้ไขข้อมูลเรียบร้อย")
        except Exception as e:
            QMessageBox.critical(self, "แก้ไขข้อมูลล้มเหลว", f"เกิดข้อผิดพลาด\n{e}")
        finally:
            conn.close()
            self.loadData()

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = DurableForm()
    window.show()
    sys.exit(app.exec_())