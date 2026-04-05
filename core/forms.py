from django import forms


class AnswerForm(forms.Form):
    user_answer = forms.CharField(
        label='Ваш ответ',
        max_length=100,
        widget=forms.TextInput(attrs={'placeholder': 'Введите ваш ответ...', 'class': 'form-control'}),
    )

