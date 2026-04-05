#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from core.models import Exercise

DATA = [

    {"topic": "Синтаксис", "question": "Как вывести текст 'Hello' в консоль?", "answer": "print('Hello')", "difficulty": "easy"},
    {"topic": "Переменные", "question": "Как присвоить переменной age значение 25?", "answer": "age = 25", "difficulty": "easy"},
    {"topic": "Типы данных", "question": "Какой тип данных у значения 3.14?", "answer": "float", "difficulty": "easy"},
    {"topic": "Комментарии", "question": "Какой символ ставится перед однострочным комментарием?", "answer": "#", "difficulty": "easy"},
    {"topic": "Типы данных", "question": "Как преобразовать строку '10' в целое число?", "answer": "int('10')", "difficulty": "easy"},

    {"topic": "Условия", "question": "Какое ключевое слово заменяет else if в Python?", "answer": "elif", "difficulty": "medium"},
    {"topic": "Циклы", "question": "Что выведет list(range(3))?", "answer": "[0, 1, 2]", "difficulty": "medium"},
    {"topic": "Списки", "question": "Как добавить элемент 'apple' в конец списка fruits?", "answer": "fruits.append('apple')", "difficulty": "medium"},
    {"topic": "Функции", "question": "Какое ключевое слово возвращает значение из функции?", "answer": "return", "difficulty": "medium"},
    {"topic": "Словари", "question": "Как получить значение по ключу 'name' из словаря user?", "answer": "user['name']", "difficulty": "medium"},

    {"topic": "ООП", "question": "Как называется метод, вызываемый при создании объекта класса?", "answer": "__init__", "difficulty": "hard"},
    {"topic": "Исключения", "question": "Какой блок используется для перехвата ошибок?", "answer": "try-except", "difficulty": "hard"},
    {"topic": "Списки", "question": "Что выведет [1, 2, 3][1:]?", "answer": "[2, 3]", "difficulty": "hard"},
    {"topic": "Функции", "question": "Как передать произвольное количество позиционных аргументов?", "answer": "*args", "difficulty": "hard"},
    {"topic": "Условия", "question": "Какой оператор проверяет равенство двух значений?", "answer": "==", "difficulty": "hard"},
]

print("Проверка и заполнение базы данных...")
created_count = 0
skipped_count = 0

for item in DATA:
    obj, created = Exercise.objects.get_or_create(
        question=item["question"],
        defaults={
            "topic": item["topic"],
            "answer": item["answer"],
            "difficulty": item["difficulty"]
        }
    )
    if created:
        created_count += 1
    else:
        skipped_count += 1

print(f"Создано: {created_count}, Пропущено (уже есть): {skipped_count}")