from functools import wraps
from PyQt6.QtWidgets import QMessageBox

# Предположим, у вас есть функция для проверки роли по логину
def check_user_role(login):
    # Эта функция должна возвращать роль пользователя на основе логина
    # Например:
    user_roles = {
        "admin_user": "админ",
        "normal_user": "пользователь",
        # Добавьте других пользователей и их роли
    }
    return user_roles.get(login, "неизвестный")

# Декоратор для проверки роли
def admin_required(method):
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        login = self.current_user_login  # Предполагаем, что у вас есть атрибут с текущим логином
        if check_user_role(login) != "админ":
            QMessageBox.warning(self, "Ошибка доступа", "У вас нет прав для выполнения этого действия.")
            return  # Не выполняем метод, если роль не админ
        return method(self, *args, **kwargs)
    return wrapper