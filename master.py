from tkinter import *


master = Tk()
master.title("My PWords")
master.tk_width = 900
master.tk_height = 500
master.geometry(f"{master.tk_width}x{master.tk_height}")
master.minsize(400, 300)
x_coord = int((master.winfo_screenwidth() - master.tk_width)/2)
y_coord = int((master.winfo_screenheight() - master.tk_height)/2)
master.geometry(f"+{x_coord}+{y_coord}")
master.DEFAULTFONT = ("Consolas", 13)
master.BGCOLOR = "#1ABC9C"
master.HEADERFONT = ("Consolas", 18)
master.HEADERBG = "#D7AB5E"

footer_text = Label(master, text="Potatoguy32 2021")
footer_text.config(font=master.DEFAULTFONT, bg=master.BGCOLOR)
footer_text.pack(side="bottom", anchor="e")
header_frame = Frame(master)
master.header_text = Label(header_frame, font=master.HEADERFONT, bg=master.HEADERBG)
master.header_text.pack(anchor="center", expand=True, fill="both")
header_frame.pack(side="top", anchor="n", fill="both")
master.config(bg="#1ABC9C")
