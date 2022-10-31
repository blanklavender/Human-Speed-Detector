from tkinter import *
import tkinter as tk
import os
import time
from tkinter import messagebox
from tkinter import filedialog
import PIL.Image, PIL.ImageTk
import cv2
import speed4
import speed3
import speed2
import sys


def on_close():
    close = messagebox.askokcancel("Close", "Would you like to close the program?")
    if close:
        quit()
        root.destroy()
        sys.exit()


class main_page:
    def __init__(self, window, window_title):
        self.window = window
        self.window.title(window_title)
        window.geometry("1000x600")
        window.configure(bg="#ffffff")
        canvas = Canvas(
            window,
            bg="#ffffff",
            height=600,
            width=1000,
            bd=0,
            highlightthickness=0,
            relief="ridge")
        canvas.place(x=0, y=0)

        background_img = PhotoImage(file=f"./comp/main_bg.png")
        background = canvas.create_image(
            508.0, 327.0,
            image=background_img)

        window.resizable(False, False)

        img0 = PhotoImage(file=f"./comp/main_img0.png")
        self.b0 = Button(
            image=img0,
            borderwidth=0,
            highlightthickness=0,
            command=self.athlete,
            relief="flat")

        self.b0.place(
            x=121, y=423,
            width=285,
            height=99)

        img1 = PhotoImage(file=f"./comp./main_img1.png")
        self.b1 = Button(
            image=img1,
            borderwidth=0,
            highlightthickness=0,
            command=self.thief,
            relief="flat")

        self.b1.place(
            x=579, y=423,
            width=285,
            height=99)

        self.delay = 5  # ms
        self.window.iconbitmap('./comp/ouri.ico')
        self.window.mainloop()

    def athlete(self):
        self.window.destroy()
        runGUI()

    def thief(self):
        self.window.destroy()
        catchGUI()

class catchGUI:
    def __init__(self):
        window = tk.Tk()
        self.window = window
        self.window.title("Burglar Mode")
        self.window.geometry("1000x600")
        self.window.configure(bg="#ffffff")
        self.canvas = Canvas(
            window,
            bg="#ffffff",
            height=600,
            width=1000,
            bd=0,
            highlightthickness=0,
            relief="ridge")
        self.canvas.place(x=0, y=0)

        background_img = PhotoImage(file=f"./comp/b_bg.png")
        background = self.canvas.create_image(
            500.0, 300.0,
            image=background_img)

        self.window.resizable(width=False, height=False)

        img0 = PhotoImage(file=f"./comp/b_img0.png")
        self.b0 = Button(
            image=img0,
            borderwidth=0,
            highlightthickness=0,
            command=self.startpro,
            relief="flat")

        self.b0.place(
            x=122, y=359,
            width=376,
            height=82)

        img1 = PhotoImage(file=f"./comp/b_img1.png")
        self.b1 = Button(
            image=img1,
            borderwidth=0,
            highlightthickness=0,
            command=self.open_file,
            relief="flat")

        self.b1.place(
            x=119, y=270,
            width=376,
            height=82)

        self.delay = 5  # ms
        self.window.iconbitmap('./comp/ouri.ico')
        window.mainloop()

    def open_file(self):
        self.pause = False

        self.filename = filedialog.askopenfilename(title="Select file",
                                                   filetypes=(("MP4 files", "*.mp4"), ("M4V files", "*.m4v"),
                                                              ("WMV files", "*.wmv"), ("AVI files", "*.avi")))
        # print(self.filename)
        self.input_name = self.filename
        temp = str(os.path.dirname(os.path.abspath(__file__)))
        self.output_name = temp + "\out" + str(time.strftime("%Y%m%d-%H%M%S")) + ".avi"

    def startpro(self):
        y1 = 'y'
        y2 = 'y'
        if self.input_name != 'init':
            Msgbox1 = tk.messagebox.askquestion('Show Processing Video',
                                                'Do you want to see the video being processed?')
            if Msgbox1 == 'yes':
                y1 = 'n'
            Msgbox2 = tk.messagebox.askquestion('Save Graph', 'Do you want to save graph plotting speed vs time ?')
            if Msgbox2 == 'no':
                y2 = 'n'
            print(self.input_name)
            print(self.output_name)
            self.window.destroy()
            store = speed4.functionCall(self.input_name, self.output_name, y1, y2)
            if store == (1, 0):
                print('Processing Finished..')
                file_name = os.path.basename(self.output_name)
                index_of_dot = file_name.index('.')
                file_name_without_extension = file_name[:index_of_dot]
                nmm = file_name_without_extension + '.avi'
                pathname = os.path.split(self.output_name)[0]
                pathname = pathname + '\\' + file_name_without_extension
                root1 = tk.Tk()
                mess = 'For Output Video and Graphs, please go to current directory of the script. Output file name will be ' + nmm + ' and graphs will be available in folder ' + pathname
                tk.messagebox.showwarning('Processing Over', mess)
                root1.destroy()
            elif store == (1, 1):
                root1 = tk.Tk()
                tk.messagebox.showwarning('Warning', 'SUSPICIOUS ACTIVITY DETECTED!')
                root1.destroy()
            else:
                root1 = tk.Tk()
                mess = "Sorry but your video does not satisfy the constraints such as proper length or proper fps"
                tk.messagebox.showwarning('Error', mess)
                root1.destroy()

class runGUI:
    def __init__(self):
        window = tk.Tk()
        self.window = window
        self.window.title("Athlete Mode")
        self.base_input = "init"
        self.live = 0

        self.window.geometry("1000x600")
        self.window.configure(bg="#ffffff")
        self.canvas = Canvas(
            window,
            bg="#ffffff",
            height=600,
            width=1000,
            bd=0,
            highlightthickness=0,
            relief="ridge")
        self.canvas.place(x=0, y=0)

        background_img = PhotoImage(file=f"./comp/background.png")
        background = self.canvas.create_image(
            491.0, 300.0,
            image=background_img)

        self.window.resizable(width=False, height=False)

        # self.canvas = Canvas(top_frame)
        # self.canvas.pack()

        self.input_name = "init"
        self.output_name = "wow_final_output.avi"

        # Buttons
        img0 = PhotoImage(file=f"./comp/img0.png")
        self.btn_rec = Button(
            image=img0,
            borderwidth=0,
            highlightthickness=0,
            command=self.startRec,
            relief="flat")

        self.btn_rec.place(
            x=500, y=406,
            width=376,
            height=82)

        img1 = PhotoImage(file=f"./comp/img1.png")
        self.btn_spro = Button(
            image=img1,
            borderwidth=0,
            highlightthickness=0,
            command=self.startpro,
            relief="flat")

        self.btn_spro.place(
            x=500, y=317,
            width=376,
            height=82)

        img2 = PhotoImage(file=f"./comp/img2.png")
        self.btn_select = Button(
            image=img2,
            borderwidth=0,
            highlightthickness=0,
            command=self.open_file,
            relief="flat")

        self.btn_select.place(
            x=500, y=228,
            width=376,
            height=82)

        # self.btn_exit=B

        self.delay = 5  # ms
        self.window.iconbitmap('./comp/ouri.ico')
        self.window.mainloop()

    def startpro(self):
        y1 = 'y'
        y2 = 'y'
        if self.input_name != 'init':
            Msgbox1 = tk.messagebox.askquestion('Show Processing Video',
                                                'Do you want to see the video being processed?')
            if Msgbox1 == 'yes':
                y1 = 'n'
            Msgbox2 = tk.messagebox.askquestion('Save Graph', 'Do you want to save graph plotting speed vs time ?')
            if Msgbox2 == 'no':
                y2 = 'n'
            print(self.input_name)
            print(self.output_name)
            self.window.destroy()
            if self.live == 0:
                if speed3.functionCall(self.input_name, self.output_name, y1, y2) == 1:
                    print('Processing Finished..')
                    file_name = os.path.basename(self.output_name)
                    index_of_dot = file_name.index('.')
                    file_name_without_extension = file_name[:index_of_dot]
                    nmm = file_name_without_extension + '.avi'
                    pathname = os.path.split(self.output_name)[0]
                    pathname = pathname + '\\' + file_name_without_extension
                    root1 = tk.Tk()
                    mess = 'For Output Video and Graphs, please go to current directory of the script. Output file name will be ' + nmm + ' and graphs will be available in folder ' + pathname
                    tk.messagebox.showwarning('Processing Over', mess)
                    root1.destroy()
                else:
                    root1 = tk.Tk()
                    mess = "Sorry but your video does not satisfy the constraints such as proper length or proper fps"
                    tk.messagebox.showwarning('Error', mess)
                    root1.destroy()
            else:
                if speed2.functionCall(self.input_name, self.output_name, y1, y2) == 1:
                    print('Processing Finished..')
                    file_name = os.path.basename(self.output_name)
                    index_of_dot = file_name.index('.')
                    file_name_without_extension = file_name[:index_of_dot]
                    nmm = file_name_without_extension + '.avi'
                    pathname = os.path.split(self.output_name)[0]
                    pathname = pathname + '\\' + file_name_without_extension
                    root1 = tk.Tk()
                    mess = 'For Output Video and Graphs, please go to current directory of the script. Output file name will be ' + nmm + ' and graphs will be availabe in folder ' + pathname
                    tk.messagebox.showwarning('Processing Over', mess)
                    root1.destroy()
                else:
                    root1 = tk.Tk()
                    mess = "Sorry but your video does not satisfy the constraints such as proper length or proper fps"
                    tk.messagebox.showwarning('Error', mess)
                    root1.destroy()

    def startRec(self):
        self.live = 1
        cap = cv2.VideoCapture(0)
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        self.base_input = "inp" + str(time.strftime("%Y%m%d-%H%M%S")) + ".avi"
        out1 = cv2.VideoWriter(self.base_input, fourcc, 20.0, (640, 480))

        flag = FALSE
        while (flag == False):
            ret, frame = cap.read()
            out1.write(frame)
            cv2.imshow('video', frame)
            if cv2.waitKey(1) & 0xFF == ord('a'):
                break

        cap.release()
        out1.release()
        cv2.destroyAllWindows()

        cap1 = cv2.VideoCapture(self.base_input)
        self.input_name = "inp" + str(time.strftime("%Y%m%d-%H%M%S")) + "_comp.avi"
        temp = str(os.path.dirname(os.path.abspath(__file__)))
        self.output_name = temp + "\out" + str(time.strftime("%Y%m%d-%H%M%S")) + ".avi"
        out2 = cv2.VideoWriter(self.input_name, fourcc, 10.0, (640, 480))

        # Frame compression
        fps_in = 20
        fps_out = 10
        index_in = -1
        index_out = -1

        while True:
            success = cap1.grab()  # boolean value of frame captured or not
            if not success:
                break
            index_in += 1  # counter for total frames

            out_due = int(index_in / fps_in * fps_out)  # out total frames
            if index_out < index_in:
                success, frame = cap1.read()
                if not success:
                    break
                # if index_out % 2 == 0:
                else:
                    out2.write(frame)
                index_out += 1

        cap1.release()
        out2.release()


    def open_file(self):
        self.live = 0
        self.pause = False

        self.filename = filedialog.askopenfilename(title="Select file",
                                                   filetypes=(("MP4 files", "*.mp4"), ("M4V files", "*.m4v"),
                                                              ("WMV files", "*.wmv"), ("AVI files", "*.avi")))
        # print(self.filename)
        self.input_name = self.filename
        temp = str(os.path.dirname(os.path.abspath(__file__)))
        self.output_name = temp + "\out" + str(time.strftime("%Y%m%d-%H%M%S")) + ".avi"


# Create a window and pass it to videoGUI Class
while 1:
    root = tk.Tk()
    root.protocol("WM_DELETE_WINDOW", on_close)
    main_page(root, "Human Speed Detection")

