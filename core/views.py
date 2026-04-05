from django.shortcuts import render, get_object_or_404
from .models import Exercise
from .forms import AnswerForm

# Create your views here.


def home(request):
    exercises = Exercise.objects.all()
    context = {'exercises': exercises}
    return render(request, 'core/home.html', context)


def quiz(request, exercise_id):
    exercise = get_object_or_404(Exercise, id=exercise_id)

    message = ''
    is_correct = None

    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            user_input = form.cleaned_data['user_answer']
            if user_input.strip().lower() == exercise.answer.strip().lower():
                message = '✅ Верно! ✅'
                is_correct = True
            else:
                message = f' ❌Неверно.❌ Правильный ответ: {exercise.answer}'
                is_correct = False
    else:
        form = AnswerForm()

    context = {
        'exercise': exercise,
        'form': form,
        'message': message,
        'is_correct': is_correct,
    }

    return render(request, 'core/quiz.html', context)


