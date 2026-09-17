"""
Финальное тестирование ЛР2.

Проверка:
1. Иерархии исключений
2. Абстрактного класса MediaProcessor
3. Конкретного ImageProcessor на реальных и битых файлах
4. Обработки всех типов ошибок
"""
import os
import numpy as np
import cv2

from media_exceptions import (
    MediaError,
    FileLoadError,
    InvalidDataError,
    InvalidImageError,
    CorruptedImageDataError,
)
from media_processor import MediaProcessor, ImageProcessor


def section(title):
    print("\n" + "=" * 60)
    print(title)
    print("=" * 60)


def create_test_image(path, w=200, h=150, color=(120, 80, 200)):
    img = np.full((h, w, 3), color, dtype=np.uint8)
    cv2.imwrite(path, img)
    return img


def main():
    section("1. Иерархия исключений")

    excs = [
        FileLoadError("a.jpg"),
        InvalidDataError("b.png"),
        InvalidImageError("c.pdf", "PDF"),
        CorruptedImageDataError("d.jpg", "test"),
    ]
    for e in excs:
        assert isinstance(e, MediaError)
        print(f"  {type(e).__name__:<28} → MediaError? {isinstance(e, MediaError)}")

    section("2. MediaProcessor — абстрактный класс")

    try:
        MediaProcessor()
        print("  ОШИБКА: удалось создать абстрактный класс!")
    except TypeError as e:
        print(f"  Нельзя создать: {type(e).__name__}")

    processor = ImageProcessor()
    print(f"  ImageProcessor создан: {processor}")

    section("3. Подготовка тестовых файлов")

    create_test_image("test_good.jpg", 200, 150)
    print(f"  test_good.jpg создан ({os.path.getsize('test_good.jpg')} байт)")

    with open("test_empty.png", "wb") as f:
        pass
    print("  test_empty.png создан (пустой)")

    with open("test_bad.jpg", "wb") as f:
        f.write(b"NOT_AN_IMAGE_AT_ALL")
    print("  test_bad.jpg создан (мусор)")

    with open("test_doc.pdf", "wb") as f:
        f.write(b"%PDF-1.4 fake pdf")
    print("  test_doc.pdf создан (PDF, не изображение)")

    section("4. Валидация — все виды ошибок")

    try:
        processor.validate("nope.jpg")
    except FileLoadError as e:
        print(f"  [FileLoadError]        {e}")

    try:
        processor.validate("test_doc.pdf")
    except InvalidImageError as e:
        print(f"  [InvalidImageError]    {e}")

    try:
        processor.validate("test_empty.png")
    except CorruptedImageDataError as e:
        print(f"  [CorruptedImageData]   {e}")

    try:
        processor.process("test_bad.jpg")
    except CorruptedImageDataError as e:
        print(f"  [CorruptedImageData]   {e}")

    section("5. Успешная обработка изображения")

    img = processor.process("test_good.jpg")
    print(f"  process():  shape={img.shape}, dtype={img.dtype}")

    info = processor.get_info("test_good.jpg")
    print("  get_info():")
    for k, v in info.items():
        print(f"    {k}: {v}")

    section("6. Полиморфизм — обработка через MediaProcessor")

    processors = [ImageProcessor()]
    files = ["test_good.jpg", "nope.jpg", "test_doc.pdf", "test_bad.jpg"]

    for p in processors:
        print(f"  Обработчик: {p}")
        for f in files:
            try:
                p.validate(f)
                img = p.process(f)
                print(f"    + {f}: OK, shape={img.shape}")
            except MediaError as e:
                print(f"    - {f}: {type(e).__name__} -> {e}")

    section("7. Безопасная обработка (без падения программы)")

    def safe_process(proc, file_path):
        try:
            proc.validate(file_path)
            return proc.process(file_path)
        except MediaError as e:
            print(f"  Ошибка: {type(e).__name__} — {e}")
            return None

    for f in files:
        print(f"\n  Файл: {f}")
        result = safe_process(processor, f)
        if result is not None:
            print(f"    Успех, shape={result.shape}")

    section("8. Очистка временных файлов")
    for f in ["test_good.jpg", "test_empty.png", "test_bad.jpg", "test_doc.pdf"]:
        if os.path.exists(f):
            os.remove(f)
            print(f"  Удалён: {f}")

    section("ТЕСТ ЛР2 ЗАВЕРШЁН")


if __name__ == "__main__":
    main()
