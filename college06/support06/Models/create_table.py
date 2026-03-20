from Models.Users import Users
from Models.KnowledgeBase import KnowledgeBase
from Models.Base import *
from Models.Category import Category
from Models.Comment import Comment
from Models.Role import Role
from Models.Status import Status
from Models.Ticket import Ticket
from Models.Type import Type


def create_tables():
    connect().create_tables(
        [
            Users,
            Type,
            Comment,
            Role,
            Status,
            Ticket,
            Category,
            KnowledgeBase,
        ]
    )


def seed_roles():
    default_roles = [
        (Role.USER, "Пользователь"),
        (Role.SPECIALIST, "Специалист"),
        (Role.ADMIN, "Администратор"),
    ]

    for role_id, name in default_roles:
        Role.get_or_create(id=role_id, defaults={"name": name})


def seed_statuses():
    default_statuses = [
        (Status.NEW, "Новое"),
        (Status.IN_PROGRESS, "Выполняется"),
        (Status.DONE, "Завершенно"),
    ]

    for status_id, name in default_statuses:
        Status.get_or_create(id=status_id, defaults={"name": name})


def seed_categories():
    default_categories = [
        (Category.INCIDENT, "Инцидент", "при обнаружении неполадок"),
        (Category.MAINTENANCE, "Обслуживание оборудования", "Наладка, ремонт, перенос, подсоединение устройств"),
        (Category.SOFTWARE, "Установка/обновление ПО", "Инсталляция программ, драйверов, обновлений"),
        (Category.ACCESS, "Проблемы авторизации", "Вход в систему, права доступа, разграничение полномочий"),
        (Category.CONSULTING, "Консультация", "Разъяснения по работе систем и программ"),
        (Category.IMPROVEMENT, "Запрос на доработку", "Изменение параметров, добавление возможностей"),
        (Category.ACCOUNT, "Управление учетными записями", "Создание/изменение/блокировка учетных записей"),
        (Category.INFORMATION, "Информационная поддержка", "Веб-сайт, СДО, отчетность, электронный журнал"),
        (Category.OTHER, "Разное", "Прочие запросы")
    ]

    for cat_id, title, description in default_categories:
        Category.get_or_create(
            id=cat_id,
            defaults={
                "title": title,
                "description": description,
            },
        )
def seed_types():
    default_types = [
        (Type.PUBLIC, "Публичный"),
        (Type.INTERNAL, "Внутренний"),
    ]
    for type_id, name in default_types:
        Type.get_or_create(id=type_id, defaults={"name": name})


if __name__ == "__main__":
    create_tables()
    seed_roles()
    seed_statuses()
    seed_categories()
    seed_types()