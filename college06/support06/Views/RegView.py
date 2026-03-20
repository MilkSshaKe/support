from tkinter import Toplevel, StringVar
from tkinter import ttk, messagebox

from Controllers.UserController import UserController
from Controllers.ReferenceController import ReferenceController


class RegView(Toplevel):
    """
    Окно регистрации пользователя.
    """

    def __init__(self, master=None) -> None:
        super().__init__(master)
        self.title("Регистрация")
        self.geometry("350x450")
        self.resizable(width=False, height=False)

        self.name_var = StringVar()
        self.login_var = StringVar()
        self.password_var = StringVar()
        self.password2_var = StringVar()
        self.role_var = StringVar()

        self._roles = []
        self._role_map: dict[str, int] = {}

        self._load_roles()
        self._setup_interface()

    def _load_roles(self) -> None:
        """
        Загружаем роли из БД для выпадающего списка.
        """
        try:
            self._roles = list(ReferenceController.get_roles())
            if not self._roles:
                from Models.create_table import seed_roles

                seed_roles()
                self._roles = list(ReferenceController.get_roles())
            self._role_map = {role.name: int(role.id) for role in self._roles}
        except Exception:
            self._roles = []
            self._role_map = {}

    def _setup_interface(self) -> None:
        padding_opts = {"padx": 20, "pady": 5}

        container = ttk.Frame(self)
        container.pack(expand=True)

        # Имя
        ttk.Label(container, text="Имя:").pack(anchor="w", **padding_opts)
        name_field = ttk.Entry(container, textvariable=self.name_var, width=30)
        name_field.pack(fill="x", padx=20)

        # Логин
        ttk.Label(container, text="Логин:").pack(anchor="w", **padding_opts)
        login_field = ttk.Entry(container, textvariable=self.login_var, width=30)
        login_field.pack(fill="x", padx=20)

        # Роль
        ttk.Label(container, text="Роль:").pack(anchor="w", **padding_opts)
        role_selector = ttk.Combobox(
            container,
            textvariable=self.role_var,
            values=list(self._role_map.keys()),
            state="readonly",
            width=28,
        )
        role_selector.pack(fill="x", padx=20)
        if self._role_map:
            role_selector.current(0)

        # Пароль
        ttk.Label(container, text="Пароль:").pack(anchor="w", **padding_opts)
        password_field = ttk.Entry(container, textvariable=self.password_var, width=30, show="*")
        password_field.pack(fill="x", padx=20)

        # Повтор пароля
        ttk.Label(container, text="Подтверждение пароля:").pack(anchor="w", **padding_opts)
        confirm_field = ttk.Entry(container, textvariable=self.password2_var, width=30, show="*")
        confirm_field.pack(fill="x", padx=20)

        # Фрейм для кнопок (в ряд)
        buttons_frame = ttk.Frame(container)
        buttons_frame.pack(fill="x", padx=20, pady=(15, 10))

        # Кнопка возвращения
        cancel_btn = ttk.Button(buttons_frame, text="Вернуться", command=self.close_window)
        cancel_btn.pack(side="left", expand=True, fill="x", padx=(0, 5))

        # Кнопка регистрации
        register_btn = ttk.Button(buttons_frame, text="Зарегистрироваться", command=self.handle_register)
        register_btn.pack(side="right", expand=True, fill="x", padx=(5, 0))

        name_field.focus_set()

    def handle_register(self) -> None:
        full_name = self.name_var.get().strip()
        user_login = self.login_var.get().strip()
        user_password = self.password_var.get().strip()
        confirm_password = self.password2_var.get().strip()
        selected_role = self.role_var.get().strip()

        if not all([user_login, user_password, confirm_password, selected_role]):
            messagebox.showwarning("Регистрация", "Заполните все обязательные поля")
            return

        if len(user_login) > 10:
            messagebox.showwarning("Регистрация", "Логин не должен превышать 10 символов")
            return

        if user_password != confirm_password:
            messagebox.showwarning("Регистрация", "Введенные пароли не совпадают")
            return

        role_id = self._role_map.get(selected_role)
        if role_id is None:
            messagebox.showerror("Регистрация", "Выбранная роль не найдена")
            return

        is_success, message = UserController.register(
            name=full_name,
            login=user_login,
            password=user_password,
            role_id=role_id,
        )
        if not is_success:
            messagebox.showerror("Регистрация", str(message))
            return

        messagebox.showinfo("Регистрация", "Пользователь успешно зарегистрирован")
        self.close_window()

    def close_window(self) -> None:
        """
        Закрыть окно регистрации.
        """
        self.destroy()


if __name__ == "__main__":
    from tkinter import Tk

    root = Tk()
    root.withdraw()
    registration = RegView(root)
    registration.mainloop()