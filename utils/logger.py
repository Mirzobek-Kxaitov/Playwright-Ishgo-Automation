import logging
import os
from datetime import datetime


def setup_logger(name: str) -> logging.Logger:
    """
    Logging tizimini sozlash.
    Har bir test uchun alohida log fayl yaratadi.
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # Agar logger allaqachon handler'larga ega bo'lsa, qayta qo'shmaslik
    if logger.handlers:
        return logger

    # Logs papkasini yaratish
    logs_dir = "logs"
    if not os.path.exists(logs_dir):
        os.makedirs(logs_dir)

    # Bugungi sana uchun log fayl
    log_filename = f"{logs_dir}/test_{datetime.now().strftime('%Y-%m-%d')}.log"

    # File handler - faylga yozish
    file_handler = logging.FileHandler(log_filename, encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)

    # Console handler - terminalga chiqarish
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    # Format - qanday ko'rinishda log yoziladi
    formatter = logging.Formatter(
        '%(asctime)s | %(name)s | %(levelname)s | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger