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

        # --- THEME SETUP ---
        self.current_theme = "light"  # can be 'light' or 'dark'
        self.themes = {
            "light": {
                "bg": "#E6E6FA",    # Lavender for user pages
                "fg": "#4B0082",    # Indigo text
                "button_bg": "#D8BFD8",
                "button_fg": "#2E0854"
            },
            "dark": {
                "bg": "#2E0854",    # Deep purple for admin / dark mode
                "fg": "#E6E6FA",    # Light lavender text
                "button_bg": "#4B0082",
                "button_fg": "#E6E6FA"
            }
        }

        # Top bar toggle (optional)
        self.create_theme_toggle()

        self.current_frame = None
        self.show_login()

    def create_theme_toggle(self):
        """Adds a simple button to toggle light/dark mode."""
        self.theme_button = tk.Button(
            self, text="Switch to Dark Mode",
            command=self.toggle_theme,
            bg=self.themes[self.current_theme]["button_bg"],
            fg=self.themes[self.current_theme]["button_fg"]
        )
        self.theme_button.pack(anchor="ne", padx=10, pady=10)

    def toggle_theme(self):
        """Switch between light and dark modes manually."""
        self.current_theme = "dark" if self.current_theme == "light" else "light"
        theme = self.themes[self.current_theme]

        self.configure(bg=theme["bg"])
        self.theme_button.config(
            text="Switch to Light Mode" if self.current_theme == "dark" else "Switch to Dark Mode",
            bg=theme["button_bg"], fg=theme["button_fg"]
        )

        # Re-render the current frame with new colors
        if self.current_frame:
            self.current_frame.destroy()
        self.show_login()  # reload the frame with new theme colors

    def get_theme(self):
        """Provides current theme to child frames."""
        return self.themes[self.current_theme]

    # --- PAGE SWITCHING ---
    def show_login(self):
        if self.current_frame:
            self.current_frame.destroy()
        self.current_frame = LoginPage(
            self,
            switch_to_register=self.show_register,
            switch_to_admin_login=self.show_admin_login
        )
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
