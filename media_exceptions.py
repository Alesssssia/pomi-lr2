"""
Модуль с пользовательскими исключениями для мультимедийных приложений.

Вариант 1: Изображения (JPEG, PNG).
Иерархия исключений:
    MediaError
    ├── FileLoadError
    ├── InvalidDataError
    ├── InvalidImageError
    └── CorruptedImageDataError
"""


class MediaError(Exception):
    """Базовое исключение для ошибок работы с медиафайлами."""

    def __init__(self, message, file_path=None):
        self.file_path = file_path
        super().__init__(message)

    def __str__(self):
        if self.file_path:
            return f"[{self.file_path}] {super().__str__()}"
        return super().__str__()


class FileLoadError(MediaError):
    """Ошибка при загрузке медиафайла (файл не найден, не читается)."""

    def __init__(self, file_path, reason="Не удалось загрузить файл"):
        super().__init__(f"{reason}: {file_path}", file_path)


class InvalidDataError(MediaError):
    """Ошибка при обработке некорректных данных."""

    def __init__(self, file_path, data_type="изображение"):
        super().__init__(
            f"Некорректные данные в файле {file_path} ({data_type})",
            file_path
        )


class InvalidImageError(MediaError):
    """Ошибка неверного формата изображения (не JPEG/PNG)."""

    def __init__(self, file_path, actual_format=None):
        reason = "Файл не является изображением JPEG/PNG"
        if actual_format:
            reason += f" (обнаружен: {actual_format})"
        super().__init__(f"{reason}: {file_path}", file_path)


class CorruptedImageDataError(MediaError):
    """Ошибка повреждённых данных изображения."""

    def __init__(self, file_path, details="данные повреждены"):
        super().__init__(
            f"Повреждённые данные изображения {file_path}: {details}",
            file_path
        )


if __name__ == "__main__":
    print("=" * 60)
    print("Проверка иерархии исключений")
    print("=" * 60)

    tests = [
        FileLoadError("test.jpg", "Файл не найден"),
        InvalidDataError("broken.png", "изображение"),
        InvalidImageError("doc.pdf", "PDF"),
        CorruptedImageDataError("bad.jpg", "обрезанный заголовок"),
    ]

    for exc in tests:
        print(f"  Тип: {type(exc).__name__}")
        print(f"  Сообщение: {exc}")
        print(f"  file_path: {exc.file_path}")
        print()

    try:
        raise CorruptedImageDataError("x.jpg", "test")
    except MediaError as e:
        print(f"  Поймано как MediaError: {e}")
