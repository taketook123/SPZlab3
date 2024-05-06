
class InMemoryFS:
    """
    Класс файлової системи, що зберігає дані в пам'яті. (In-Memory File System)

    Імітує базові функціональні можливості файлової системи, 
    такі як створення, відкриття, закриття, читання, запис, видалення 
    та перелік файлів. Всі дані зберігаються у пам'яті.
    """

    def __init__(self):
        """
        Ініціалізує файлову систему in-memory.

        Словники використовуються для зберігання даних файлів (self.files),
        відстеження відкритих файлів (self.open_files) 
        та твердих посилань (self.links).
        self.next_fd - лічильник для призначення наступного доступного дескриптора файлу.
        """
        self.files = {}  # Словник для зберігання файлів (ім'я: дані)
        self.links = {}
        self.open_files = {}  # Словник для відстеження відкритих файлів (fd: (ім'я, зміщення))
        self.next_fd = 0  # Лічильник для наступного доступного дескриптора файлу

    def create(self, name):
        """
        Створити новий файл з вказаною назвою.

        Перевіряє чи файл з такою назвою вже існує. 
        Якщо так - викликає виняток FileExistsError.
        Якщо ні - створює новий елемент у словнику self.files 
        з пустими даними (b"").
        """
        if name in self.files:
            raise FileExistsError(f"Файл '{name}' вже існує")
        self.files[name] = b""

    def open(self, name):
        """
        Відкриває файл для читання/запису.

        Перевіряє чи файл з такою назвою існує. 
        Якщо ні - викликає виняток FileNotFoundError.
        Якщо так - призначає новий дескриптор файлу (fd) з self.next_fd 
        та зберігає інформацію про відкритий файл у self.open_files 
        (ім'я файлу та його поточне зміщення).
        Потім збільшує self.next_fd для уникнення конфліктів дескрипторів.
        Повертає призначений дескриптор файлу.
        """
        if name not in self.files:
            raise FileNotFoundError(f"Файл '{name}' не знайдено")
        fd = self.next_fd
        self.next_fd += 1
        self.open_files[fd] = (name, 0)
        return fd

    def close(self, fd):
        """
        Закрити файл.
        """
        if fd not in self.open_files:
            raise ValueError(f"Недійсний дескриптор файлу {fd}")
        del self.open_files[fd]

    def read(self, fd, size):
        """
        Читає дані з відкритого файлу.

        Перевіряє чи дескриптор файлу (fd) є дійсним.
        Якщо ні - викликає виняток ValueError.
        Якщо так - отримує інформацію про відкритий файл з self.open_files 
        (ім'я файлу та його поточне зміщення).
        Читає дані з файлу розміром size починаючи з поточного зміщення.
        Оновлює поточне зміщення у self.open_files.
        Повертає прочитані дані.
        """
        if fd not in self.open_files:
            raise ValueError(f"Недійсний дескриптор файлу {fd}")
        name, offset = self.open_files[fd]
        data = self.files[name]
        available = len(data) - offset
        read_size = min(size, available)
        result = data[offset:offset + read_size]
        self.open_files[fd] = (name, offset + read_size)
        return result

    def write(self, fd, data):
        """
        Записати у файл.
        """
        if fd not in self.open_files:
            raise ValueError(f"Недійсний дескриптор файлу {fd}")
        name, offset = self.open_files[fd]
        self.files[name] = self.files[name][:offset] + data + self.files[name][offset + len(data):]

    def ls(self):
        """
        Повернути список файлів.
        """
        return list(self.files.keys())

    def link(self, name1, name2):
        """
        Створити тверде посилання.
        """
        if name1 not in self.files:
            raise FileNotFoundError(f"Файл '{name1}' не знайдено")
        self.links[name2] = name1

    def unlink(self, name):
        """
        Видалити тверде посилання.
        """
        if name not in self.links:
            raise FileNotFoundError(f"Тверде посилання '{name}' не знайдено")
        del self.links[name]

    def truncate(self, name, size):
        """
        Обрізати файл до певного розміру.
        """
        if name not in self.files:
            raise FileNotFoundError(f"Файл '{name}' не знайдено")
        self.files[name] = self.files[name][:size] + b"\0" * (size - len(self.files[name]))
