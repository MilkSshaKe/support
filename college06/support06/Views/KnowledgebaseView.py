from tkinter import Toplevel, StringVar, END
from tkinter import ttk, messagebox

from Controllers import KnowledgeController
from Models.Users import Users
from Models.Role import Role


class KnowledgeBaseView(Toplevel):
    """
    Окно «База знаний» с поиском по названию и списком статей.
    """

    def __init__(self, master, current_user: Users) -> None:
        super().__init__(master)
        self.title("База знаний")
        self.geometry("800x450")
        self.resizable(width=True, height=True)

        self.current_user = current_user
        role_id = int(current_user.role_id)
        self.is_admin_or_specialist = role_id in (Role.ADMIN, Role.SPECIALIST)

        self.search_var = StringVar()

        self._build_ui()
        self._load_Knowledges()

    def _build_ui(self) -> None:
        top_frame = ttk.Frame(self)
        top_frame.pack(fill="x", padx=10, pady=5)

        ttk.Label(top_frame, text="Поиск по названию:").pack(side="left", padx=(0, 5))
        entry = ttk.Entry(top_frame, textvariable=self.search_var, width=40)
        entry.pack(side="left", padx=(0, 5))

        btn_search = ttk.Button(top_frame, text="Поиск", command=self.on_search)
        btn_search.pack(side="left", padx=5)

        btn_reset = ttk.Button(top_frame, text="Сброс", command=self.on_reset)
        btn_reset.pack(side="left", padx=5)

        if self.is_admin_or_specialist:
            btn_delete = ttk.Button(top_frame, text="Удалить", command=self.on_delete)
            btn_delete.pack(side="right", padx=5)

        btn_back = ttk.Button(top_frame, text="Назад", command=self.destroy)
        btn_back.pack(side="right", padx=5)

        table_frame = ttk.Frame(self, borderwidth=1, relief="solid", padding=5)
        table_frame.pack(fill="both", expand=True, padx=10, pady=10)

        columns = ("id", "title", "description", "ticket_id", "executor")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings")
        self.tree.pack(side="left", fill="both", expand=True)

        headers = ("ID", "Название", "Описание", "Заявка", "Исполнитель")
        for col, header in zip(columns, headers):
            self.tree.heading(col, text=header)
            self.tree.column(col, stretch=True, width=120)

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        scrollbar.pack(side="right", fill="y")
        self.tree.configure(yscrollcommand=scrollbar.set)

    def _load_Knowledges(self, Knowledges=None) -> None:
        for item in self.tree.get_children():
            self.tree.delete(item)

        if Knowledges is None:
            Knowledges = KnowledgeController.get_all()

        for Knowledge in Knowledges:
            executor_name = getattr(Knowledge.executor_id, "name", "")
            self.tree.insert(
                "",
                END,
                values=(
                    Knowledge.id,
                    Knowledge.title,
                    Knowledge.description,
                    getattr(Knowledge.ticket_id, "id", ""),
                    executor_name,
                ),
            )

    def _get_selected_Knowledge_id(self) -> int | None:
        selected = self.tree.selection()
        if not selected:
            return None
        item_id = selected[0]
        values = self.tree.item(item_id, "values")
        if not values:
            return None
        try:
            return int(values[0])
        except (TypeError, ValueError):
            return None

    # ------------------------------------------------------------------
    # Обработчики
    # ------------------------------------------------------------------

    def on_search(self) -> None:
        query = self.search_var.get().strip()
        if not query:
            self._load_Knowledges()
            return

        Knowledges = KnowledgeController.search_by_title(query)
        self._load_Knowledges(Knowledges)

    def on_reset(self) -> None:
        self.search_var.set("")
        self._load_Knowledges()

    def on_delete(self) -> None:
        if not self.is_admin_or_specialist:
            return

        Knowledge_id = self._get_selected_Knowledge_id()
        if Knowledge_id is None:
            messagebox.showwarning("Удаление", "Выберите статью для удаления")
            return

        if messagebox.askyesno("Удаление", "Удалить выбранную статью?"):
            ok, msg = KnowledgeController.delete_Knowledge(Knowledge_id)
            if not ok:
                messagebox.showerror("Удаление", msg)
                return
            self._load_Knowledges()


__all__ = ["KnowledgeBaseView"]

