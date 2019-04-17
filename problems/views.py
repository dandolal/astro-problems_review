from django.shortcuts import get_object_or_404, render, redirect
from django.db.models import Count
from django.db.utils import OperationalError
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.core.files import File
from datetime import datetime
# from django.db.migrations.operations import TrigamExtention

from .models import Problem, Author, Event, Theme, Comment
from .forms import ProblemForm, ConfirmDeleteForm, AuthorSearchForm

MAX_COUNT = 100


def problems_list(request, order_by, order=0, problems=Problem.objects, flag=False):
    try:
        order = int(order)
        if order == 0:
            problems_list_ = problems.order_by(order_by)  # Problem.objects.order_by('theme)
        else:
            problems_list_ = problems.order_by(order_by).reverse()
        order ^= 1
        paginator = Paginator(problems_list_.all(), 20)
        page = request.GET.get('page')
        problems = paginator.get_page(page)
        context = {'problems': problems, 'order_by': order_by, 'order': order, 'user': request.user}
        if flag:
            return render(request, 'problems/problem_list.html', context)
        return render(request, 'problems/problem_list_all.html', context)
    except OperationalError:
        pass


def authors_list(request):
    try:
        form = AuthorSearchForm()
        authors_list_ = Author.objects.annotate(count=Count('problems')).order_by('-count')
        if request.method == 'POST':
            form = AuthorSearchForm(request.POST)
            if form.is_valid():
                authors_list_ = Author.objects.filter(
                    name__contains=form.cleaned_data['name']).annotate(
                    count=Count('problems')).order_by('-count')
        problem_count = [len(author.problems.all()) for author in authors_list_]
        context = {'authors_list': authors_list_, 'problem_count': problem_count, 'form': form}
        return render(request, 'problems/authors_list.html', context)  # return render
    except OperationalError:
        pass


def themes_list(request):
    try:
        themes_list_ = Theme.objects.annotate(count=Count('problems')).order_by('-count')
        problem_count = [len(author.problems.all()) for author in themes_list_]
        context = {'themes_list': themes_list_, 'problem_count': problem_count}
        return render(request, 'problems/themes_list.html', context)
    except OperationalError:
        pass


def theme_view(request, theme_id):
    try:
        theme_ = get_object_or_404(Theme, pk=theme_id)
        # context = {
        #     'theme': theme_, 'description': theme_.description, 'problems': theme_.problems
        # }
        # if request.method == 'POST':
        return problems_list(request, 'id', 0, theme_.problems, True)
        # return render(request, 'problems/event.html', context)
    except OperationalError:
        pass


def problem(request, problem_id):
    try:
        problem_ = get_object_or_404(Problem, pk=problem_id)
        authors = problem_.author_set.all()
        themes = problem_.theme_set.all()

        events = problem_.event_set.all()
        problem_.text = parseToHtml(problem_.text)
        problem_.solution = parseToHtml(problem_.solution)
        problem_.save()

        context = {
            'problem': problem_, 'authors': authors, 'themes': themes, 'events': events,
            'user': request.user
        }
        return render(request, 'problems/problem.html', context)
    except OperationalError:
        pass


def add_rating(request, problem_id):
    problem_ = Problem.objects.get(pk=problem_id)
    voted_users = list(problem_.liked_users.all().values('id'))
    if request.user.id is not None and {'id': request.user.id} not in voted_users:
        problem_.liked_users.add(request.user)
        problem_.rating += 1
        problem_.save()
    return redirect('/problems/{}'.format(problem_id))


def reduce_rating(request, problem_id):
    problem_ = Problem.objects.get(pk=problem_id)
    voted_users = list(problem_.liked_users.all().values('id'))
    if request.user.id is not None and {'id': request.user.id} not in voted_users:
        problem_.liked_users.add(request.user)
        problem_.rating -= 1
        problem_.save()
    return redirect('/problems/{}'.format(problem_id))


def download_problem(request, problem_id):
    some_file = open('problems/static/problems/latex/tex_template.tex', "r")
    django_file = File(some_file)
    return render(request, 'problems/problem.html', {'download_file': django_file})


def event(request, event_id):
    try:
        event_ = get_object_or_404(Event, pk=event_id)
        # context = {
        #     'event': event_, 'description': event_.description, 'problems': event_.problems
        # }
        # if request.method == 'POST':
        return problems_list(request, 'id', 0, event_.problems, True)
        # return render(request, 'problems/event.html', context)
    except OperationalError:
        pass


def view_solution(request, problem_id):
    try:
        problem_ = get_object_or_404(Problem, pk=problem_id)

        if request.method == 'POST':
            comment = Comment(text=request.POST.get('comment'), author=request.user,
                              problem=problem_)
            comment.save()
            return redirect('/problems/{}/solution/'.format(problem_.id))

        return render(request, 'problems/solution.html', {
            'problem': problem_, 'comments': problem_.comment_set.all(), 'user': request.user
        })
    except OperationalError:
        pass


def parseToHtml(string):
    string = string.replace('\r\n\r\n', '</p><p>').replace('~', '&nbsp;').replace('---', '&mdash;').replace('\r\n', ' ').replace('\par', '</p><p>').replace('\\\\', '</p><p>')
    if string[:3] == '<p>':
        return string
    return '<p>{}</p>'.format(string)


def problem_new(request):
    if request.method == 'POST':

        problem_ = Problem(title=request.POST.get('title'),
                           complexity=int(request.POST.get('complexity')),
                           text=parseToHtml(request.POST.get('text')),
                           solution=parseToHtml(request.POST.get('solution')),
                           year=int(request.POST.get('year')),
                           min_level=int(request.POST.get('min_level')),
                           max_level=int(request.POST.get('max_level')))

        problem_.save()

        for theme in Theme.objects.order_by('id'):
            if request.POST.get('theme_{}'.format(theme.id)):
                theme.problems.add(problem_)

        for i in range(MAX_COUNT):
            event_name = request.POST.get('event_name{}'.format(i))
            if not event_name:
                break
            try:
                event = Event.objects.get(name=event_name)
            except ObjectDoesNotExist:
                event = Event(name=event_name)
                event.save()
            event.problems.add(problem_)

        for i in range(MAX_COUNT):
            print('author_name{}'.format(i))
            author_name = request.POST.get('author_name{}'.format(i))
            if not author_name:
                print(author_name)
                break
            try:
                author = Author.objects.get(name=author_name)
            except ObjectDoesNotExist:
                author = Author(name=author_name)
                author.save()
            print(author.id)
            author.problems.add(problem_)
        return redirect('/problems/{}'.format(problem_.id))

    context = {
        'author_list': Author.objects.order_by('name'),
        'theme_list': Theme.objects.order_by('name'), 'years': [2019 - i for i in range(100)],
        'complexity': [1, 2, 3, 4, 5],
    }
    return render(request, 'problems/new_problem.html', context)


def delete_problem(request, problem_id):
    try:
        if request.method == 'POST':
            form = ConfirmDeleteForm(request.POST)
            if form.is_valid():
                problem_ = get_object_or_404(Problem, pk=problem_id)
                if str(form.cleaned_data['is_confirmed']) == 'True':
                    problem_.delete()
                    return redirect('/problems')
                else:
                    return redirect('/problems/{}'.format(problem_.id))
        else:
            form = ConfirmDeleteForm()
        return render(request, 'problems/delete_problem.html', {'form': form})
    except OperationalError:
        print('OperationalError')
        pass


def view_author(request, author_id):
    try:
        author = get_object_or_404(Author, pk=author_id)
        # problems = author.problems.all()
        # print(problems)
        # context = {'author': author}
        return problems_list(request, 'id', 0, author.problems, True)
        # return render(request, 'problems/author.html', context)
    except OperationalError:
        pass


def events_list(request):
    try:
        events_list_ = Event.objects.annotate(count=Count('problems')).order_by('-count')
        problem_count = [len(event.problems.all()) for event in events_list_]
        # paginator = Paginator(events_list_, 20)
        # page = request.GET.get('page')
        # events = paginator.get_page(page)
        context = {'events': events_list_, 'problem_count': problem_count}
        return render(request, 'problems/events.html', context)
    except OperationalError:
        pass


def edit_problem(request, problem_id):
    try:
        problem_ = Problem.objects.get(pk=problem_id)
        if request.method == 'POST':

            problem_.title = request.POST.get("title")
            problem_.complexity = request.POST.get("complexity")
            problem_.text = request.POST.get("text")
            problem_.solution = request.POST.get("solution")
            problem_.year = request.POST.get("year")

            problem_.save()

            try:
                event = Event.objects.get(name=request.POST.get('event_name'))
            except ObjectDoesNotExist:
                event = Event(name=request.POST.get('event_name'))
                event.save()
            event.problems.add(problem_)
            event.save()

            for theme in Theme.objects.order_by('id'):
                if request.POST.get('theme_{}'.format(theme.id)):
                    theme.problems.add(problem_)

            for author in Author.objects.order_by('id'):
                if request.POST.get('theme_{}'.format(author.id)):
                    author.problems.add(problem_)

            for ind in range(10):
                try:
                    author_name = request.POST.get('existing_authors_{}'.format(ind))
                    print(author_name)
                    author = Author.objects.get(name=author_name)
                    author.problems.add(problem_)
                except ObjectDoesNotExist:
                    break

            authors = request.POST.get('authors')
            # for author_id in existing_authors:
            #     try:
            #         author = Author.objects.get(pk=author_id)
            #         authors = author.name + ', ' + authors
            #     except ObjectDoesNotExist:
            #         pass

            for name in authors.split(','):
                name = name.strip()
                if name != '':
                    try:
                        author = Author.objects.get(name=name)
                    except Author.DoesNotExist:
                        author = Author(name=name)
                        author.save()
                    author.problems.add(problem_)
            return redirect('/problems/{}'.format(problem_.id))

        context = {
            'problem': problem_, 'authors': Author.objects.order_by('name'),
            'themes': Theme.objects.order_by('name'), 'years': [2019 - i for i in range(100)],
            'complexity': [i + 1 for i in range(10)]
        }
        return render(request, 'problems/edit_problem.html', context)
    except OperationalError:
        pass


def search(request):
    if request.method == 'POST':
        title_ = request.POST.get('title')
        text_ = request.POST.get('text')
        solution_ = request.POST.get('solution')
        year_from_, year_to_ = int(request.POST.get('year_from')), int(request.POST.get('year_to'))
        complexity_from, complexity_to = int(request.POST.get('complexity_from')), int(
            request.POST.get('complexity_to'))

        level_from_, level_to_ = int(request.POST.get('level_from')), int(
            request.POST.get('level_to'))
        problems_ = Problem.objects.none()

        for theme in Theme.objects.order_by('id'):
            if request.POST.get('theme_{}'.format(theme.id)):
                temp_problems = theme.problems
                problems_ = temp_problems.union(problems_)

        if len(problems_) == 0:
            problems_ = Problem.objects.all()

        problems_event = Problem.objects.none()
        for i in range(MAX_COUNT):
            event_name = request.POST.get('event_name{}'.format(i))
            if not event_name:
                break
            try:
                event_ = Event.objects.get(name=event_name)
                temp_problems = event_.problems
                problems_event = temp_problems.union(problems_event)
            except ObjectDoesNotExist:
                continue

        problems_author = Problem.objects.none()
        for i in range(MAX_COUNT):
            author_name = request.POST.get('author_name{}'.format(i))
            if not author_name:
                break
            try:
                author = Author.objects.get(name=author_name)
                temp_problems = author.problems
                problems_author = temp_problems.union(problems_author)
            except ObjectDoesNotExist:
                continue

        problems_level = Problem.objects.all()
        for problem_ in Problem.objects.all():
            if not problem_.min_level <= level_from_ <= problem_.max_level and not level_from_ <= problem_.min_level <= level_to_:
                problems_level = problems_level.exclude(pk=problem_.id)

        if len(problems_event) != 0:
            problems_ = problems_.intersection(problems_event)
        if len(problems_author) != 0:
            problems_ = problems_.intersection(problems_author)
        if len(problems_level) != 0:
            problems_ = problems_.intersection(problems_level)

        problems_ = problems_.filter(year__range=[year_from_, year_to_])
        problems_ = problems_.filter(title__trigram_similar=title_).union(
            problems_.filter(title__contains=title_))
        problems_ = problems_.filter(text__trigram_similar=text_).union(
            problems_.filter(text__contains=text_))
        problems_ = problems_.filter(solution__trigram_similar=solution_).union(
            problems_.filter(solution__contains=solution_))
        problems_ = problems_.filter(complexity__range=[complexity_from, complexity_to])

        return problems_list(request, 'id', 0, problems_, True)

    else:
        context = {
            'author_list': Author.objects.order_by('name'),
            'theme_list': Theme.objects.order_by('name'),
            'years': [i for i in reversed(range(1948, int(datetime.now().strftime('%Y'))))],
            'first_year': 1947, 'last_year': int(datetime.now().strftime('%Y')),
            'complexity': [2, 3, 4],
        }
        return render(request, 'problems/search.html', context)
