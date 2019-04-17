from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect, get_object_or_404

from problems.models import Problem, Event, Author, Theme


def index(request):
    problem_count = Problem.objects.count()
    problem_end = ''
    if problem_count % 100 in range(11, 20):
        pass
    elif problem_count % 10 in [1]:
        problem_end = 'а'
    elif problem_count % 10 in [2, 3, 4]:
        problem_end = 'и'

    author_count = Author.objects.count()
    author_end = 'ов'
    if problem_count % 100 in range(11, 20):
        pass
    elif author_count % 10 in [1]:
        author_end = ''
    elif author_count % 10 in [2, 3, 4]:
        author_end = 'а'

    theme_count = Theme.objects.count()
    theme_end = 'ов'
    if problem_count % 100 in range(11, 20):
        pass
    elif theme_count % 10 in [1]:
        theme_end = ''
    elif theme_count % 10 in [2, 3, 4]:
        theme_end = 'а'

    event_count = Event.objects.count()
    event_end = 'ов'
    if theme_count % 100 in [11, 12, 13, 14]:
        pass
    elif theme_count % 10 in [1]:
        theme_end = ''
    elif theme_count % 10 in [2, 3, 4]:
        theme_end = 'а'

    context = {
        'problem_count': problem_count, 'problem_end': problem_end, 'author_count': author_count,
        'author_end': author_end, 'theme_count': theme_count, 'theme_end': theme_end,
        'event_count': event_count, 'event_end': event_end
    }
    return render(request, 'index.html', context)


def command(request):
    return render(request, 'command.html')


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})


def signout(request):
    logout(request)
    return redirect('/')


def profile(request):
    return render(request, 'registration/profile.html', {'user': request.user})
