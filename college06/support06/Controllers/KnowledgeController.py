from typing import Iterable, Optional

from peewee import DoesNotExist

from Models.KnowledgeBase import KnowledgeBase
from Models.Ticket import Ticket
from Models.Users import Users


class KnowledgeController:
    """
    Контроллер для работы с базой знаний (KnowledgeBase).
    """

    @classmethod
    def get_all(cls) -> Iterable[KnowledgeBase]:
        """
        Получить все статьи.
        """
        return KnowledgeBase.select().order_by(KnowledgeBase.id.desc())

    @classmethod
    def get_by_id(cls, Knowledge_id: int) -> Optional[KnowledgeBase]:
        """
        Получить статью по id.
        """
        try:
            return KnowledgeBase.get_by_id(Knowledge_id)
        except DoesNotExist:
            return None

    @classmethod
    def get_for_ticket(cls, ticket_id: int) -> Iterable[KnowledgeBase]:
        """
        Статьи, связанные с определённой заявкой.
        """
        return KnowledgeBase.select().where(KnowledgeBase.ticket_id == ticket_id)

    @classmethod
    def search_by_title(cls, query: str) -> Iterable[KnowledgeBase]:
        """
        Поиск статей по названию (используется на форме «Поиск по названию»).
        """
        like_expr = f"%{query}%"
        return KnowledgeBase.select().where(KnowledgeBase.title.contains(query) | (KnowledgeBase.title ** like_expr))

    @classmethod
    def create_Knowledge(
        cls,
        title: str,
        description: str,
        ticket_id: int,
        executor_id: int,
    ) -> tuple[bool, str | KnowledgeBase]:
        """
        Создать новую статью базы знаний.
        Как правило, вызывается из формы заявки («Создать статью»).
        """
        try:
            ticket = Ticket.get_by_id(ticket_id)
        except DoesNotExist:
            return False, "Заявка не найдена"

        try:
            executor = Users.get_by_id(executor_id)
        except DoesNotExist:
            return False, "Исполнитель не найден"

        try:
            Knowledge = KnowledgeBase.create(
                title=title,
                description=description,
                ticket_id=ticket,
                executor_id=executor,
            )
            return True, Knowledge
        except Exception as exc:  # noqa: BLE001
            return False, f"Ошибка создания статьи: {exc}"

    @classmethod
    def delete_Knowledge(cls, Knowledge_id: int) -> tuple[bool, str]:
        """
        Удалить статью (кнопка «Удалить» в экране базы знаний).
        """
        try:
            Knowledge = KnowledgeBase.get_by_id(Knowledge_id)
        except DoesNotExist:
            return False, "Статья не найдена"

        try:
            Knowledge.delete_instance()
            return True, "Статья удалена"
        except Exception as exc:  # noqa: BLE001
            return False, f"Ошибка удаления статьи: {exc}"


__all__ = ["KnowledgeController"]

