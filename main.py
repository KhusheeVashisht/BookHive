import tkinter as tk
from Gui.login import LoginPage
from Gui.register import RegistrationPage
from Gui.admin_login import AdminLoginPage  

class BookHiveApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("BookHive")
        self.state('zoomed')
        self.minsize(800, 600)
        self.current_frame = None
        self.show_login()

    def show_login(self):
        if self.current_frame:
            self.current_frame.destroy()
        self.current_frame = LoginPage(self, switch_to_register=self.show_register, switch_to_admin_login=self.show_admin_login)
        self.current_frame.pack(fill="both", expand=True)

    def show_register(self):
        if self.current_frame:
            self.current_frame.destroy()
        self.current_frame = RegistrationPage(self, switch_to_login=self.show_login)
        self.current_frame.pack(fill="both", expand=True)

    def show_admin_login(self):
        if self.current_frame:
            self.current_frame.destroy()
        self.current_frame = AdminLoginPage(self, switch_to_user_login=self.show_login)
        self.current_frame.pack(fill="both", expand=True)

if __name__ == "__main__":
    app = BookHiveApp()
    app.mainloop()
