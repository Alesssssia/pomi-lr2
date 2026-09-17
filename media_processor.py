"""
Модуль с обработчиками медиафайлов.

Вариант 1: Изображения (JPEG, PNG).
Абстрактный класс MediaProcessor + конкретный ImageProcessor.
"""
import os
from abc import ABC, abstractmethod

import cv2

from media_exceptions import (
    FileLoadError,
    InvalidDataError,
    InvalidImageError,
    CorruptedImageDataError,
)


class MediaProcessor(ABC):
    """Абстрактный класс для обработчиков медиафайлов.

    Наследники обязаны реализовать методы process() и validate().
    """

    @abstractmethod
    def process(self, file_path):
        """Обрабатывает медиафайл и возвращает результат."""
        pass

    @abstractmethod
    def validate(self, file_path):
        """Валидирует медиафайл. Возвращает True или выбрасывает исключение."""
        pass

    def __str__(self):
        return f"<{self.__class__.__name__}>"


class ImageProcessor(MediaProcessor):
    """Обработчик изображений (JPEG, PNG)."""

    SUPPORTED_EXTENSIONS = (".jpg", ".jpeg", ".png")

    def validate(self, file_path):
        """Проверяет файл изображения.

        Выбрасывает:
            FileLoadError — файл не найден
            InvalidImageError — неверное расширение
            CorruptedImageDataError — файл не читается как изображение
        """
        if not os.path.exists(file_path):
            raise FileLoadError(file_path, "Файл не найден")

        if not os.path.isfile(file_path):
            raise FileLoadError(file_path, "Это не файл")

        ext = os.path.splitext(file_path)[1].lower()
        if ext not in self.SUPPORTED_EXTENSIONS:
            raise InvalidImageError(file_path, ext or "без расширения")

        if os.path.getsize(file_path) == 0:
            raise CorruptedImageDataError(file_path, "файл пустой")

        return True

    def process(self, file_path):
        """Загружает изображение через OpenCV. Возвращает numpy-массив."""
        self.validate(file_path)

        img = cv2.imread(file_path)

        if img is None:
            raise CorruptedImageDataError(
                file_path,
                "cv2.imread не смог прочитать данные"
            )

        if img.size == 0:
            raise CorruptedImageDataError(file_path, "изображение пустое")

        return img

    def get_info(self, file_path):
        """Возвращает словарь с информацией об изображении."""
        img = self.process(file_path)
        h, w = img.shape[:2]
        channels = img.shape[2] if len(img.shape) == 3 else 1
        return {
            "filename": os.path.basename(file_path),
            "width": w,
            "height": h,
            "channels": channels,
            "size_bytes": os.path.getsize(file_path),
        }


if __name__ == "__main__":
    print("=" * 60)
    print("Проверка абстрактного класса и ImageProcessor")
    print("=" * 60)

    try:
        p = MediaProcessor()
    except TypeError as e:
        print(f"  MediaProcessor нельзя создать: {type(e).__name__}")

    processor = ImageProcessor()
    print(f"  Создан: {processor}")

    try:
        processor.validate("nonexistent.jpg")
    except FileLoadError as e:
        print(f"  Поймали FileLoadError: {e}")
