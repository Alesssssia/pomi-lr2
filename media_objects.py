"""
Модуль с классами для мультимедийных объектов.
Вариант 1: Изображения (JPEG, PNG).
"""


class MediaObject:
    """Базовый класс для всех мультимедийных объектов.

    Атрибуты:
        filename (str): имя файла
        duration (float): длительность в секундах (для изображений = 0)
    """

    def __init__(self, filename, duration=0):
        # Проверка корректности имени файла
        if not filename or not isinstance(filename, str):
            raise ValueError("Имя файла не может быть пустым")
        # Проверка длительности
        if duration < 0:
            raise ValueError("Длительность не может быть отрицательной")

        self.filename = filename
        self.duration = duration

    def get_info(self):
        """Возвращает строку с информацией об объекте."""
        return f"{self.filename}: {self.duration} сек"

    def __str__(self):
        """Строковое представление — используется в print()."""
        return f"<{self.__class__.__name__}({self.filename})>"



class Image(MediaObject):
    """Класс для работы с изображениями."""

    COLOR_SPACES = {1: "Grayscale", 3: "RGB", 4: "RGBA"}

    def __init__(self, filename, width=0, height=0, channels=3):
        super().__init__(filename, duration=0)
        if width < 0 or height < 0:
            raise ValueError("Ширина и высота не могут быть отрицательными")
        if channels not in self.COLOR_SPACES:
            raise ValueError(
                f"Недопустимое число каналов: {channels}. "
                f"Допустимо: {list(self.COLOR_SPACES.keys())}"
            )
        self.width = width
        self.height = height
        self.channels = channels

    def get_resolution(self):
        """Возвращает разрешение изображения."""
        return f"{self.width}x{self.height}"

    def get_color_space(self):
        """Возвращает цветовое пространство по числу каналов."""
        return self.COLOR_SPACES[self.channels]

    def get_info(self):
        info = super().get_info()
        return f"{info}, {self.get_resolution()}, {self.get_color_space()} ({self.channels} кан.)"


class Video(MediaObject):
    """Класс для работы с видеофайлами."""

    def __init__(self, filename, duration, resolution, fps=0, codec="unknown"):
        super().__init__(filename, duration)
        if fps < 0:
            raise ValueError("FPS не может быть отрицательным")
        self.resolution = resolution
        self.fps = fps
        self.codec = codec

    def get_fps(self):
        return self.fps

    def get_codec(self):
        return self.codec

    def get_info(self):
        info = super().get_info()
        return f"{info}, {self.resolution}, {self.fps} FPS, кодек {self.codec}"


class Audio(MediaObject):
    """Класс для работы с аудиофайлами."""

    def __init__(self, filename, duration, sample_rate=44100, bitrate=320):
        super().__init__(filename, duration)
        if sample_rate <= 0:
            raise ValueError("Частота дискретизации должна быть положительной")
        if bitrate <= 0:
            raise ValueError("Битрейт должен быть положительным")
        self.sample_rate = sample_rate
        self.bitrate = bitrate

    def get_sample_rate(self):
        return self.sample_rate

    def get_bitrate(self):
        return self.bitrate

    def get_info(self):
        info = super().get_info()
        return f"{info}, {self.sample_rate} Гц, {self.bitrate} кбит/с"





class MediaLibrary:
    """Класс для управления коллекцией медиафайлов."""

    def __init__(self):
        """Создаёт пустую коллекцию."""
        self.media_objects = []

    def add(self, media_obj):
        """Добавляет объект в коллекцию."""
        if not isinstance(media_obj, MediaObject):
            raise TypeError("Можно добавлять только объекты MediaObject и его наследников")
        self.media_objects.append(media_obj)

    def get_total_duration(self):
        """Возвращает общую длительность всех объектов (в секундах)."""
        return sum(obj.duration for obj in self.media_objects)

    def filter_by_type(self, media_type):
        """Возвращает список объектов заданного типа."""
        return [obj for obj in self.media_objects if isinstance(obj, media_type)]

    def __len__(self):
        """Позволяет использовать len(library)."""
        return len(self.media_objects)

    def __str__(self):
        return f"<MediaLibrary: {len(self.media_objects)} объектов>"


