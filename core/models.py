from django.db import models
from django.contrib.auth.models import User
from typing_extensions import reveal_type


# Create your models here.


class Exercise(models.Model):
    DIFFICULTY_CHOICES = [
        ('easy', 'Легко'),
        ('medium', 'Средне'),
        ('hard', 'Сложно'),
    ]

    topic = models.CharField(
        max_length=100,
        verbose_name='Тема',
        help_text='Например синтаксис, циклы, функции'
    )

    question = models.TextField(
        verbose_name='Вопрос',
        help_text='Текст задания'
    )

    answer = models.CharField(
        max_length=100,
        verbose_name='Ответ',
        help_text='Правильный ответ'
    )

    difficulty = models.CharField(
        max_length=10,
        choices=DIFFICULTY_CHOICES,
        default='easy',
        verbose_name='Сложность'
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )

    class Meta:
        verbose_name = 'Задание'
        verbose_name_plural = 'Задания'
        ordering = ['topic', 'difficulty']

    def __str__(self):
        return f'{self.topic}: {self.question[:50]}...'


class Attempt(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    exercise = models.ForeignKey('Exercise', on_delete=models.CASCADE, verbose_name='Задание')
    is_correct = models.BooleanField(verbose_name='Верный ответ')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата попытки')

    class Meta:
        verbose_name = 'Попытка'
        verbose_name_plural = 'Попытки'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.user.username}: {self.exercise.topic}'
