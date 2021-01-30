from tkinter import Tk, Label, Button, Entry, Frame, Menu, PhotoImage, messagebox, Text
from CRUD import create, check_login, check_registered, register_user, query_site, submit_site


# Application class
class App:

    def __init__(self):
        # Create main window
        self.root = Tk()
        self.root.title("My PWords")
        self.root.geometry("800x500")
        self.root.minsize(400, 300)

        # Create the database and tables if not exist
        create()

        # Insert an image to the top bar
        self.lock_photo = PhotoImage("Images/padlock.ico")
        self.root.iconphoto(self.root, self.lock_photo)

        # Insert footer
        self.footer_text = Label(self.root, text="Copyrights potatoguy32 2021")
        self.footer_text.config(font=("Consolas", 8), bg="#1ABC9C")
        self.footer_text.pack(side="bottom", anchor="e")

        # Dictionary to store all the frames created and then control transitions
        self.frames = {}

    # Reset menu bar when transitioning
    def reset_menubar(self):
        self.dash_menu = Menu(self.root, relief="raised")
        self.about_menu = Menu(self.dash_menu, tearoff=0)
        self.dash_menu.add_cascade(label="About", menu=self.about_menu)
        self.about_menu.add_command(label="github repo")
        self.about_menu.add_command(label="version notes")
        self.exit_menu = Menu(self.dash_menu, tearoff=0)
        self.dash_menu.add_cascade(label="Exit", menu=self.exit_menu)
        self.exit_menu.add_command(label="Close app", command=self.root.quit)
        self.root.config(bg="#1ABC9C", menu=self.dash_menu)

    def clear_window(self):
        self.root.geometry("800x500")
        for F in self.frames.values():
            F.destroy()

    # Frame for the header text and color
    def make_header(self, my_text):
        self.header_frame = Frame(self.root)
        self.frames["header_frame"] = self.header_frame
        header_text = Label(self.header_frame, text=my_text)
        header_text.config(font=("Consolas", 16), bg="#D7AB5E")
        header_text.pack(anchor="center", expand=True, fill="both")
        self.header_frame.pack(side="top", anchor="n", fill="both")

    # Login window
    def login_window(self):
        self.reset_menubar()
        self.clear_window()
        self.make_header("Login into an existing account or create one")
        self.main_frame = Frame(self.root, bg="#1ABC9C")
        self.frames["main_frame"] = self.main_frame
        Label(self.main_frame, text="Username").pack(side="top", anchor="n")
        self.username_entry = Entry(self.main_frame, widt=30)
        self.username_entry.pack(side="top", anchor="n")

        Label(self.main_frame, text="Master Password").pack(side="top", anchor="n")
        self.password_entry = Entry(self.main_frame, width=30, show="*")
        self.password_entry.pack(side="top", anchor="n")

        Button(self.main_frame, text="Login", command=self.login).pack(side="top", anchor="n")
        Button(self.main_frame, text="Register", command=self.registerWindow).pack(side="top", anchor="n")

        self.main_frame.pack(anchor="center", side="top", fill="x", expand=True)

        self.root.mainloop()

    # Method to transition to the next window
    def login(self):
        if (self.username_entry.get() != "") and (self.password_entry.get() != ""):
            self.current_user_data = check_login(self.username_entry.get(), self.password_entry.get())

            if self.current_user_data is None:
                messagebox.showerror(title="Username/Password not recognized",
                                     message="Please register or correct the info")

            else:
                self.dashboard_window()

        else:
            messagebox.showinfo("Login error", "Please fill all the information")

    # Manager main content window
    def dashboard_window(self):
        self.reset_menubar()
        self.clear_window()
        self.dash_menu.add_command(label="Start", command=self.dashboard_window)
        self.dash_menu.add_command(label="See all your sites", command=self.query_site)
        self.dash_menu.add_command(label="Add site", command=self.add_site_window)
        self.exit_menu.add_command(label="Log out", command=self.login_window)
        self.make_header(f"Welcome back {self.current_user_data[1]}")
        self.dash_main_frame = Frame(self.root, bg="#1ABC9C")
        self.frames["dash_main_frame"] = self.dash_main_frame
        Label(self.dash_main_frame, text="Look for a site or paste the URL").pack(side="top", anchor="n")
        self.site_entry = Entry(self.dash_main_frame, width=50)
        self.site_entry.pack(side="top", anchor="n")
        Button(self.dash_main_frame, text="Search", command=self.query_site).pack(side="top", anchor="n")
        self.dash_main_frame.pack(anchor="center", side="top", fill="x", expand=True)

    # Look for a specific site, return an error window if not in db
    def query_site(self):
        site_query = query_site(self.current_user_data[0], self.site_entry.get())
        self.text_boxes = []
        if len(site_query) < 1:
            messagebox.showerror(title="Site not found",
                                 message="The site is not registered or misspelled")

        else:
            self.reset_menubar()
            self.clear_window()
            self.root.geometry("1050x500")
            self.make_header(f"I found {len(site_query)} sites, click on the text to copy !")
            self.query_site_frame = Frame(self.root, bg="#1ABC9C")
            self.frames["query_site_frame"] = self.query_site_frame

            Label(self.query_site_frame, text="Site name",
                  padx=15, pady=15, bg="#1ABC9C").grid(row=0, column=0, sticky="nsew")
            Label(self.query_site_frame, text="Site URL",
                  padx=15, pady=15, bg="#1ABC9C").grid(row=0, column=1, sticky="nsew")
            Label(self.query_site_frame, text="Email",
                  padx=15, pady=15, bg="#1ABC9C").grid(row=0, column=2, sticky="nsew")
            Label(self.query_site_frame, text="username",
                  padx=15, pady=15, bg="#1ABC9C").grid(row=0, column=3, sticky="nsew")
            Label(self.query_site_frame, text="password",
                  padx=15, pady=15, bg="#1ABC9C").grid(row=0, column=4, sticky="nsew")

            for i in range(len(site_query)):
                for j in range(5):
                    data = Text(self.query_site_frame, borderwidth=0, bg="#1ABC9C", bd=0)
                    data.insert(1.0, site_query[i][j])
                    data.config(width=20, height=1, highlightbackground="#1ABC9C", padx=5, pady=10,
                                state="disabled", cursor="plus")
                    if j == 1:
                        data.config(width=60)

                    data.grid(row=1 + i, column=j)
                    self.text_boxes.append(data)

            self.query_site_frame.pack(anchor="center", side="top", fill="both", expand=True)
            self.map_entries()

    def copy_to_clipboard(self, event):
        text_value = event.widget.get("1.0", "end")
        self.root.clipboard_clear()
        self.root.clipboard_append(text_value)

    def map_entries(self):
        for textbox in self.text_boxes:
            textbox.bind("<Button-1>", self.copy_to_clipboard)

    # Site registration window
    def add_site_window(self):
        self.clear_window()
        self.make_header("Fill the entries to register a new site")

        self.add_site_frame = Frame(self.root, bg="#1ABC9C")
        self.frames["add_site_frame"] = self.add_site_frame

        Label(self.add_site_frame, text="Site name *").pack()
        self.new_site = Entry(self.add_site_frame, width=30)
        self.new_site.pack()
        Label(self.add_site_frame, text="URL").pack()
        self.new_url = Entry(self.add_site_frame, width=30)
        self.new_url.pack()
        Label(self.add_site_frame, text="Registered email").pack()
        self.new_email = Entry(self.add_site_frame, width=30)
        self.new_email.pack()
        Label(self.add_site_frame, text="Registered username").pack()
        self.new_site_user = Entry(self.add_site_frame, width=30)
        self.new_site_user.pack()
        Label(self.add_site_frame, text="Password *").pack()
        self.new_site_password = Entry(self.add_site_frame, width=30, show="*")
        self.new_site_password.pack()
        Label(self.add_site_frame, text="Confirm password *").pack()
        self.confirm_site_password = Entry(self.add_site_frame, width=30, show="*")
        self.confirm_site_password.pack()

        Button(self.add_site_frame, text="Submit", command=self.submit_site).pack()
        Button(self.add_site_frame, text="Back", command=self.dashboard_window).pack()

        self.add_site_frame.pack(anchor="center", side="top", fill="x", expand=True)

    # Register the new site to Passwords table
    def submit_site(self):
        if (self.new_site.get() != "") and (self.new_site_password.get() != "") and\
             (self.new_site_password.get() == self.confirm_site_password.get()):

            submit_site(self.current_user_data[0], self.new_site.get(), self.new_url.get(),
                        self.new_email.get(), self.new_site_user.get(), self.new_site_password.get())

            messagebox.showinfo(title="Site correctly submited",
                                message="Your site is now available for you")
            self.add_site_window()

        else:
            messagebox.showerror(title="Submission error",
                                 message="Please fill the required entries correctly")

    # New user register page
    def registerWindow(self):
        self.reset_menubar()
        self.clear_window()

        self.make_header("Fill the entries to make a new account")

        self.register_frame = Frame(self.root, bg="#1ABC9C")
        self.frames["register_frame"] = self.register_frame

        Label(self.register_frame, text="New username").pack(side="top", anchor="n")
        self.new_username_entry = Entry(self.register_frame, width=30)
        self.new_username_entry.pack()

        Label(self.register_frame, text="New password").pack(side="top", anchor="n")
        self.new_password_entry = Entry(self.register_frame, width=30, show="*")
        self.new_password_entry.pack()

        Label(self.register_frame, text="Confirm password").pack(side="top", anchor="n")
        self.confirm_password_entry = Entry(self.register_frame, width=30, show="*")
        self.confirm_password_entry.pack()

        Button(self.register_frame, text="Create account", command=self.create_account).pack()
        Button(self.register_frame, text="Go to login", command=self.login_window).pack()

        self.register_frame.pack(anchor="center", side="top", fill="x", expand=True)

    # Add the new user into Users table
    def create_account(self):
        if (self.new_username_entry.get() != "") and (self.new_password_entry.get() != "") and \
         (self.confirm_password_entry.get() != ""):

            result = check_registered(self.new_username_entry.get())

            # If it already exist, show error
            if result is not None:
                messagebox.showinfo(title="User already exist",
                                    message="Choose another username")

            # Insert the new user if the passwords match
            if self.new_password_entry.get() == self.confirm_password_entry.get():
                register_user(self.new_username_entry.get(), self.new_password_entry.get())
                messagebox.showinfo(title="Successful registered !",
                                    message="Your account is registered, now you can login")
                self.login_window()

            else:
                messagebox.showerror(title="Passwords don't match",
                                     message="Please correct your password")

        else:
            messagebox.showerror(title="Entry error",
                                 message="Please fill all entries")


if __name__ == "__main__":
    testing = App()
    testing.login_window()
