from django.contrib import admin
from .models import Exercise

# Register your models here.


@admin.register(Exercise)
class ExerciseAdmin(admin.ModelAdmin):
    list_display = ['topic', 'question', 'answer', 'difficulty', 'created_at']
    list_filter = ['topic', 'difficulty']
    search_fields = ['question', 'answer']
    list_editable = ['answer']

