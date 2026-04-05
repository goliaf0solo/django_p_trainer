from django.db import models

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
