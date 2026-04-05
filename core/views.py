from django.shortcuts import render, get_object_or_404, redirect
from .models import Exercise, Attempt
from .forms import AnswerForm
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.db import models


# Create your views here.


def home(request):
    exercises = Exercise.objects.all()

    if request.user.is_authenticated:
        solved_ids = Attempt.objects.filter(
            user=request.user,
            is_correct=True,
        ).values_list('exercise_id', flat=True)

        for ex in exercises:
            ex.is_solved = ex.id in solved_ids
    else:
        for ex in exercises:
            ex.is_solved = False

    context = {'exercises': exercises}
    return render(request, 'core/home.html', context)


@login_required
def quiz(request, exercise_id):
    exercise = get_object_or_404(Exercise, id=exercise_id)
    form = AnswerForm()

    is_solved = Attempt.objects.filter(
        user=request.user, exercise=exercise, is_correct=True
    ).exists()

    message = ''
    is_correct = None
    show_form = not is_solved

    if request.method == 'POST':
        if request.POST.get('retry'):
            show_form = True
            message = 'Введи ответ заново:'
            is_correct = None
        else:
            form = AnswerForm(request.POST)
            if form.is_valid():
                user_input = form.cleaned_data['user_answer']

                if user_input.strip().lower() == exercise.answer.strip().lower():
                    is_correct = True
                    message = '✅ Верно! ✅'
                    show_form = False
                    is_solved = True
                else:
                    is_correct = False
                    message = '❌ Неверно. Попробуй ещё раз! ❌'
                    show_form = True

                Attempt.objects.create(
                    user=request.user,
                    exercise=exercise,
                    is_correct=is_correct
                )

    all_exercises = list(Exercise.objects.order_by('id').values_list('id', flat=True))
    current_index = all_exercises.index(exercise_id) if exercise_id in all_exercises else 0
    prev_exercise = all_exercises[current_index - 1] if current_index > 0 else None
    next_exercise = all_exercises[current_index + 1] if current_index < len(all_exercises) - 1 else None

    context = {
        'exercise': exercise,
        'form': form,
        'message': message,
        'is_correct': is_correct,
        'is_solved': is_solved,
        'show_form': show_form,
        'prev_exercise': prev_exercise,
        'next_exercise': next_exercise,
    }
    return render(request, 'core/quiz.html', context)


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {"form": form})


@login_required
def profile(request):
    attempts_qs = Attempt.objects.filter(user=request.user).select_related('exercise')

    total_attempts = attempts_qs.count()
    correct_count = attempts_qs.filter(is_correct=True).count()
    solved_count = attempts_qs.filter(is_correct=True).values('exercise_id').distinct().count()

    solved_by_difficulty = attempts_qs.filter(
        is_correct=True
    ).values('exercise__difficulty').annotate(
        count=models.Count('exercise_id', distinct=True)
    )

    difficulty_stats = {}
    for item in solved_by_difficulty:
        diff = item['exercise__difficulty']
        difficulty_stats[diff] = item['count']

    context = {
        'attempts': attempts_qs.order_by('-created_at')[:10],
        'total_attempts': total_attempts,
        'correct_count': correct_count,
        'solved_count': solved_count,

        'easy_solved': difficulty_stats.get('easy', 0),
        'medium_solved': difficulty_stats.get('medium', 0),
        'hard_solved': difficulty_stats.get('hard', 0),
    }
    return render(request, 'registration/profile.html', context)
