import cv2 as cv
from tkinter import *
import tkinter.messagebox as msg
import numpy as np
from pyzbar.pyzbar import decode
import pyzbar.pyzbar as pyz
from tkinter import filedialog
from PIL import ImageTk, Image
import webbrowser as wb 

root = Tk()
root.title("Qr-Reader")
root.geometry("1200x700")
root.resizable(False, False)
root.config(bg="#081029")

ent_var = StringVar()


def open():
    try:
        path = filedialog.askopenfilename()
        timage = Image.open(path)
        timage = timage.resize((300, 200), Image.ANTIALIAS)
        img = ImageTk.PhotoImage(timage)
        qrlbl.configure(image=img)
        qrlbl.timage = img
        for barcode in decode(timage):
            mydata = barcode.data.decode('utf-8')
            print(mydata)
            ent_box.delete(0, END)
            ent_box.insert(0, mydata)
            url = mydata
            # wb.open_new_tab(url)
            wb.register('chrome', None)
            wb.open_new_tab(url)

    except Exception as es:
        print(es)


def realtime():
    cap = cv.VideoCapture(0, cv.CAP_DSHOW)
    detector = cv.QRCodeDetector()
    while True:
        _, far = cap.read()
        f_frame = cv.flip(far, 1)
        grey = cv.cvtColor(f_frame, cv.COLOR_BGR2GRAY)

        for barcode in decode(grey):
            mydata = barcode.data.decode('utf-8')
            points = np.array([barcode.polygon], np.int32)
            points = points.reshape((-1, 1, 2))
            cv.polylines(f_frame, [points], True, (43, 227, 62), 5)
            points2 = barcode.rect
            cv.putText(f_frame, mydata, (points2[0], points2[1]), cv.FONT_HERSHEY_COMPLEX, 0.9, (26, 205, 232), 3)
        cv.imshow('win', f_frame)
        if cv.waitKey(30) == 13:
            wb.open_new_tab(mydata)
            ent_box.delete(0, END)
            ent_box.insert(0, str(mydata))
            break

    cap.release()
    cv.destroyAllWindows()


#######images #########
head = PhotoImage(file=r"E:\Python_Dev2\Qr_reader\img\head.png")
scan = PhotoImage(file=r"E:\Python_Dev2\Qr_reader\img\scan.png")
cam = PhotoImage(file=r"E:\Python_Dev2\Qr_reader\img\cam.png")
exits = PhotoImage(file=r"E:\Python_Dev2\Qr_reader\img\exit.png")

frame = Frame(root, bg="#121545")  # 121539
frame.place(x=70, y=75, height=580, width=1050)

head_img = Label(root, image=head, bg="#081029")
head_img.place(x=430, y=5)

qrlbl = Label(frame, bd=0, bg="#121545")
qrlbl.pack(padx=50, pady=60, side="top")

ent_box = Entry(frame, textvariable=ent_var, bd=0, font="sans-serif 12 bold")
ent_box.place(x=280, y=350, height=40, width=500)

scan_btn = Button(frame, image=scan, bg="#121545", bd=0, command=open)
scan_btn.place(x=100, y=478)

cam_btn = Button(frame, image=cam, bg="#121545", bd=0, command=realtime)
cam_btn.place(x=500, y=478)

exit_btn = Button(frame, image=exits, bg="#121545", bd=0, command=lambda: exit())
exit_btn.place(x=900, y=477)

about = Label(root, text="Created By Vedika with ❤", font="Verdana 10 bold", bg="#081029", fg="#fff")
about.place(x=500, y=665)

root.mainloop()
