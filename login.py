import pyperclip
from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk

from master import master
import CRUD
import encrypter


class App(Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.main_frame = Frame(self.master, bg=self.master.BGCOLOR)
        self.pack()
        self.loginMenubar()
        self.loginWindow()

    def loginMenubar(self):
        self.dash_menu = Menu(self.master, relief="raised")
        self.about_menu = Menu(self.dash_menu, tearoff=0)
        self.dash_menu.add_cascade(label="About", menu=self.about_menu)
        self.about_menu.add_command(label="github repo")
        self.about_menu.add_command(label="version notes")
        self.exit_menu = Menu(self.dash_menu, tearoff=0)
        self.dash_menu.add_cascade(label="Exit", menu=self.exit_menu)
        self.exit_menu.add_command(label="Close app", command=self.master.quit)
        self.master.config(menu=self.dash_menu)

    def loginWindow(self):
        self.master.header_text.config(text="Welcome! \n Login or create a new account")
        self.main_frame = Frame(self.master, bg=self.master.BGCOLOR)
        logo = Image.open("Images/lock.ico")
        logo = logo.resize((200, 200))
        logo = ImageTk.PhotoImage(logo)
        logo_label = Label(self.main_frame, image=logo)
        logo_label.image = logo
        logo_label.pack(side="top", anchor="n")
        Label(self.main_frame, text="Username", font=self.master.DEFAULTFONT,
              bg=self.master.BGCOLOR).pack(side="top", anchor="n")
        self.username_entry = Entry(self.main_frame, widt=50)
        self.username_entry.pack(side="top", anchor="n")
        Label(self.main_frame, text="Password", font=self.master.DEFAULTFONT,
              bg=self.master.BGCOLOR).pack(side="top", anchor="n")
        self.password_entry = Entry(self.main_frame, widt=50, show="*")
        self.password_entry.pack(side="top", anchor="n")
        Button(self.main_frame, text="Login", command=self.check_login).pack(side="top", anchor="n")
        Button(self.main_frame, text="Register", command=self.registerWindow).pack(side="top", anchor="n")

        self.main_frame.pack(anchor="center", side="top", fill="x", expand=True)

    def check_login(self):
        self.current_user = [self.username_entry.get(), self.password_entry.get()]
        if self.current_user[0] == "" or self.current_user[1] == "":
            messagebox.showinfo(title="Empty fields",
                message="Please fill both fields")
            return 1

        if CRUD.can_login(self.current_user[0], self.current_user[1]):
            self.current_user.extend(CRUD.get_id(self.current_user[0]))
            self.mainWindow()
            return 0

        messagebox.showinfo(title="User not found or not registered",
            message="Please check your info or register")
        return 1


    def registerWindow(self):
        self.main_frame.destroy()
        self.master.header_text.config(text="Fill the text fields to create an account :D")
        self.main_frame = Frame(self.master, bg=self.master.BGCOLOR)
        Label(self.main_frame, text="Username", font=self.master.DEFAULTFONT,
              bg=self.master.BGCOLOR).pack(side="top", anchor="n")
        self.new_username = Entry(self.main_frame, widt=50)
        self.new_username.pack(side="top", anchor="n")
        Label(self.main_frame, text="Main password", font=self.master.DEFAULTFONT,
              bg=self.master.BGCOLOR).pack(side="top", anchor="n")
        self.new_password = Entry(self.main_frame, widt=50, show="*")
        self.new_password.pack(side="top", anchor="n")
        Label(self.main_frame, text="Confirm password", font=self.master.DEFAULTFONT,
              bg=self.master.BGCOLOR).pack(side="top", anchor="n")
        self.confirmpass = Entry(self.main_frame, widt=50, show="*")
        self.confirmpass.pack(side="top", anchor="n")
        Button(self.main_frame, text="Register", command=self.register_user).pack(side="top", anchor="n")
        Button(self.main_frame, text="Back to login", command=self.loginTransition).pack(side="top", anchor="n")
        self.main_frame.pack(anchor="center", side="top", fill="x", expand=True)

    def register_user(self):
        new_user_data = (self.new_username.get(), self.new_password.get(), self.confirmpass.get())
        if new_user_data[1] != new_user_data[2]:
            messagebox.showinfo(title="Register error", message="password don't match")
            return 2

        if new_user_data[0] == "" or new_user_data[1] == "" or new_user_data[0] == "":
            messagebox.showinfo(title="Register error", message="Please fill all the fields")
            return 2

        if CRUD.is_registered(new_user_data[0]):
            messagebox.showinfo(title="Register error", message="Username already taken")
            return 2

        CRUD.register_user(new_user_data[0], new_user_data[1])
        messagebox.showinfo(title="Successful registered",
                            message="Your account has been created, now you can login")
        self.main_frame.destroy()
        self.login()
        return 0

    def mainWindow(self):
        self.main_frame.destroy()
        self.mainMenubar()
        self.master.header_text.config(text="Welcome back {}!".format(self.current_user[0]))
        self.main_frame = Frame(self.master, bg=self.master.BGCOLOR)
        Label(self.main_frame, text="Search for a specific service or copy an URL",
              pady=4, font=self.master.DEFAULTFONT,
              bg=self.master.BGCOLOR).pack(anchor="n", side="top")
        self.search_entry = Entry(self.main_frame, widt=70)
        self.search_entry.pack(anchor="center", side="top")
        Button(self.main_frame, text="Search", command=self.search_site).pack(anchor="n", side="top")
        self.main_frame.pack(anchor="center", side="top", fill="x", expand=True)

    def mainMenubar(self):
        self.dash_menu.destroy()
        self.dash_menu = Menu(self.master, relief="raised")
        self.dash_menu.add_command(label="Start", command=self.mainWindow)
        self.dash_menu.add_command(label="See all your passwords", command=self.show_sites)
        self.dash_menu.add_command(label="Add new password", command=self.addPassWindow)
        self.dash_menu.add_command(label="Delete or cofig your passwords", command=self.deletePassWindow)
        self.about_menu = Menu(self.dash_menu, tearoff=0)
        self.dash_menu.add_cascade(label="About", menu=self.about_menu)
        self.about_menu.add_command(label="github repo")
        self.about_menu.add_command(label="version notes")
        self.exit_menu = Menu(self.dash_menu, tearoff=0)
        self.dash_menu.add_cascade(label="Exit", menu=self.exit_menu)
        self.exit_menu.add_command(label="Log out", command=self.loginTransition)
        self.exit_menu.add_command(label="Close app", command=self.master.quit)
        self.master.config(menu=self.dash_menu)

    def show_sites(self):
        self.datalist = CRUD.query_site(self.current_user[2])
        self.main_frame.destroy()
        self.sitesList()
        return 0

    def search_site(self):
        self.datalist = CRUD.query_site(self.current_user[2], self.search_entry.get())
        self.main_frame.destroy()
        if len(self.datalist) == 0:
            self.notFound()
            return 4

        self.sitesList()
        return 0

    def notFound(self):
        self.master.header_text.config(text="Sorry, that service isn't registered, try again or add a new one")
        self.main_frame = Frame(self.master, bg=self.master.BGCOLOR)
        self.main_frame.pack(anchor="center", side="top", fill="x", expand=True)

    def sitesList(self):
        self.text_boxes = []
        self.passwords = []
        self.master.header_text.config(
            text="I found {} entries, click on the field to copy".format(len(self.datalist)))
        self.main_frame = Frame(self.master, bg=self.master.BGCOLOR)
        Label(self.main_frame, text="Site / Service", font=self.master.DEFAULTFONT,
              padx=15, pady=15, bg=self.master.BGCOLOR).grid(row=0, column=0, sticky="nsew")
        Label(self.main_frame, text="URL", font=self.master.DEFAULTFONT,
              padx=15, pady=15, bg=self.master.BGCOLOR).grid(row=0, column=1, sticky="nsew")
        Label(self.main_frame, text="Email", font=self.master.DEFAULTFONT,
              padx=15, pady=15, bg=self.master.BGCOLOR).grid(row=0, column=2, sticky="nsew")
        Label(self.main_frame, text="Username", font=self.master.DEFAULTFONT,
              padx=15, pady=15, bg=self.master.BGCOLOR).grid(row=0, column=3, sticky="nsew")
        Label(self.main_frame, text="Password", font=self.master.DEFAULTFONT,
              padx=15, pady=15, bg=self.master.BGCOLOR).grid(row=0, column=4, sticky="nsew")

        for i in range(len(self.datalist)):
            for j in range(5):
                data = Text(self.main_frame, borderwidth=0, bg=self.master.BGCOLOR, bd=0)
                data.insert(1.0, self.datalist[i][j])
                data.config(width=22, height=1, highlightbackground=self.master.BGCOLOR,
                            padx=5, pady=10, state="disabled", cursor="plus ")
                data.grid(row=1 + i, column=j)
                if j == 4:
                    self.passwords.append(data)
                    continue

                self.text_boxes.append(data)

        self.main_frame.pack(anchor="center", side="top", fill="both", expand=True)
        self.map_entries()

    def map_entries(self):
        for textbox in self.text_boxes:
            textbox.bind("<Button-1>", self.copy_to_clipboard)

        for password in self.passwords:
            password.bind("<Button-1>", self.copy_password)


    def copy_password(self, event):
        text_value = event.widget.get("1.0", "end")
        text_value = encrypter.decrypt(text_value)
        self.master.clipboard_clear()
        self.master.clipboard_append(text_value)

    def copy_to_clipboard(self, event):
        text_value = event.widget.get("1.0", "end")
        self.master.clipboard_clear()
        self.master.clipboard_append(text_value)

    def loginTransition(self):
        self.main_frame.destroy()
        self.dash_menu.destroy()
        self.loginMenubar()
        self.loginWindow()

    def addPassWindow(self):
        self.master.header_text.config(text="Fill the required fields to add a new password")
        self.main_frame.destroy()
        self.main_frame = Frame(self.master, bg=self.master.BGCOLOR)
        Label(self.main_frame, text="service or application *", font=self.master.DEFAULTFONT,
              bg=self.master.BGCOLOR).pack(side="top", anchor="n")
        self.site_entry = Entry(self.main_frame, widt=50)
        self.site_entry.pack(side="top", anchor="n")
        Label(self.main_frame, text="URL", font=self.master.DEFAULTFONT,
              bg=self.master.BGCOLOR).pack(side="top", anchor="n")
        self.url_entry = Entry(self.main_frame, widt=50)
        self.url_entry.pack(side="top", anchor="n")
        Label(self.main_frame, text="Registered Email", font=self.master.DEFAULTFONT,
              bg=self.master.BGCOLOR).pack(side="top", anchor="n")
        self.email_entry = Entry(self.main_frame, widt=50)
        self.email_entry.pack(side="top", anchor="n")
        Label(self.main_frame, text="Registered username", font=self.master.DEFAULTFONT,
              bg=self.master.BGCOLOR).pack(side="top", anchor="n")
        self.username_entry = Entry(self.main_frame, widt=50)
        self.username_entry.pack(side="top", anchor="n")
        Label(self.main_frame, text="Password *", font=self.master.DEFAULTFONT,
              bg=self.master.BGCOLOR).pack(side="top", anchor="n")
        self.pass_entry = Entry(self.main_frame, widt=50, show="*")
        self.pass_entry.pack(side="top", anchor="n")
        Label(self.main_frame, text="Confirm password *", font=self.master.DEFAULTFONT,
              bg=self.master.BGCOLOR).pack(side="top", anchor="n")
        self.confirm_entry = Entry(self.main_frame, widt=50, show="*")
        self.confirm_entry.pack(side="top", anchor="n")
        Button(self.main_frame, text="Register", command=self.validate_password).pack(anchor="n", side="top")
        Button(self.main_frame, text="Cancel", command=self.mainWindow).pack(anchor="n", side="top")
        self.main_frame.pack(anchor="center", side="top", fill="x", expand=True)

    def validate_password(self):
        new_pass_data = (self.site_entry.get(), self.url_entry.get(),
            self.email_entry.get(), self.username_entry.get(),
            self.pass_entry.get(), self.confirm_entry.get())
        if "" in (new_pass_data[0], new_pass_data[4], new_pass_data[5]):
            messagebox.showinfo(title="Entry fields error",
                message="Please fill in all the required fields")
            return 3

        if new_pass_data[4] != new_pass_data[5]:
            messagebox.showinfo(title="Match error",
                message="Your passwords don't match please repeat")
            self.pass_entry.delete(0, 50)
            self.confirm_entry.delete(0, 50)
            return 3

        encrypted_password = encrypter.encrypt(new_pass_data[4])
        CRUD.submit_site(self.current_user[2], new_pass_data[0], new_pass_data[1],
            new_pass_data[2], new_pass_data[3], encrypted_password)
        messagebox.showinfo(title="Successfully registered !",
            message="Your password has been saved, you'll be redirected to start window")
        self.mainWindow()

    def deletePassWindow(self):
        sites_data = CRUD.get_data_to_config(self.self.current_user[2])
        self.master.header_text.config(text="Select what you want you want to do")
        self.main_frame.destroy()
        self.main_frame = Frame(self.master, bg=self.master.BGCOLOR)
        Label(self.main_frame, text="Site or service", font=self.master.DEFAULTFONT,
            bg=self.master.BGCOLOR).grid(column=0, row=0, sticky="nsew")
        Label(self.main_frame, text="Email", font=self.master.DEFAULTFONT,
            bg=self.master.BGCOLOR).grid(column=1, row=0, sticky="nsew")
        Label(self.main_frame, text="Username", font=self.master.DEFAULTFONT,
            bg=self.master.BGCOLOR).grid(column=2, row=0, sticky="nsew")
        self.main_frame.pack(anchor="center", side="top", fill="x", expand=True)
        


if __name__ == "__main__":
    CRUD.create_db()
    app = App(master=master)
    app.mainloop()
