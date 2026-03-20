from tkinter import Tk, StringVar, END
from tkinter import ttk, messagebox

from Controllers.UserController import UserController
from Views.RegView import RegView
from Views.MainView import MainView


class LoginView(Tk):
    """
    Форма аутентификации пользователя.
    """

    def __init__(self) -> None:
        super().__init__()
        self.title("Авторизация")
        self.geometry("400x220")
        self.resizable(width=False, height=False)

        self.username = StringVar()
        self.passwd = StringVar()

        self._setup_interface()

    def _setup_interface(self) -> None:
        padding_opts = {"padx": 10, "pady": 5}

        ttk.Label(self, text="Логин:").pack()
        username_field = ttk.Entry(self, textvariable=self.username, width=30)
        username_field.pack()

        ttk.Label(self, text="Пароль:").pack()
        password_field = ttk.Entry(self, textvariable=self.passwd, width=30, show="*")
        password_field.pack(padx=5, pady=5)

        register_btn = ttk.Button(self, text="Регистрация", command=self.show_register_window)
        register_btn.pack(padx=5, pady=5)

        login_btn = ttk.Button(self, text="Войти", command=self.handle_login)
        login_btn.pack(padx=5, pady=5)

        username_field.focus_set()

    def handle_login(self) -> None:
        user_login = self.username.get().strip()
        user_password = self.passwd.get().strip()

        if not user_login or not user_password:
            messagebox.showwarning("Авторизация", "Заполните все поля")
            return

        authorized_user = UserController.authenticate(login=user_login, password=user_password)
        if authorized_user is None:
            messagebox.showerror("Авторизация", "Неверные учетные данные")
            return

        MainView(self, authorized_user)
        self.passwd.set("")
        self.withdraw()

    def show_register_window(self) -> None:
        """
        Открыть окно создания учетной записи.
        """
        RegView(self)


if __name__ == "__main__":
    app = LoginView()
    app.mainloop()