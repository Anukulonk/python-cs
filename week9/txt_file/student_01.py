import os
from pathlib import Path

class TXT:
    def __init__(self):
        dir = Path("D:\python\python-cs\week9\txt_file\student.txt")
        self.dir = dir
    def Created(self):
        text_data = """Error In line 24"""
        with open("student.txt", "w", encoding="utf-8") as file:
            try:
                file.write(text_data)
                print("บันทึกไฟล์เรียบร้อยแล้ว")
            except:
                print("บันทึกไฟล์ไม่ได้")

    def Reader(self):
        with open("student.txt", "r", encoding="utf-8") as file:
            try:
                print(file.read())
            except:
                print("อ่านไฟล์ไม่ได้")
    def Updated(self, data_update):
        with open("student.txt", "w", encoding="utf-8") as file:
            try:
                file.write(data_update)
                print("อัพเดทข้อมูลเรียบร้อย")
            except:
                print("อัพเดทข้อมูลไม่ได้")
    def Del(self, fileName):
        file = fileName
        if(os.path.exists(file)):
            os.remove(file)
            print("ลบไฟล์เรียบร้อย")
        else:
            print("ไม่พบไฟล์", file)
#-----------------------------------------------------------------------
txt = TXT()
while True:
    print("------------------------ Menu ------------------------")
    print("Q = Quit, C = Create, R = Read, U = Update, D = Delete")
    print("------------------------ Menu ------------------------")
    status = input ("please select menu : ")
    if(status.lower() == "q"):
        break
    elif(status.lower() == "c"):
        txt.Created()
    elif(status.lower() == "r"):
        txt.Reader()
    elif(status.lower() == "u"):
        inp = input("Data Update: ")
        txt.Updated(inp)
    elif(status.lower() == "d"):
        txt.Del("student.txt")
