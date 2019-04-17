from django import template
from datetime import datetime
# from django.template.loader_tags import do_extends
# import tokenize
# import StringIO

register = template.Library()


@register.filter
def get_at_index(list, index):
    return list[index]


@register.filter
def cut_string(string, size):
    if len(string) > size:
        string = string[:size] + '...'
    elif len(string) == 0:
        string = '---'
    return string


@register.filter
def authors_to_string(authors, size):
    string = ''
    size = int(size)
    for author in authors:
        string += author.name + ', '

    string = string[:-2]
    if len(string) > size:
        string = string[:size] + '...'
    elif len(string) == 0:
        string = '---'
    return string


@register.filter
def problems_count(event):
    return event.problem_set.count


@register.filter
def add_rating(problem, user):
    if user not in problem.voted_users:
        problem.voted_users.append(user)
        problem.rating += 1
    return


@register.filter
def add_rating(problem, user):
    if user not in problem.voted_users:
        problem.voted_users.append(user)
        problem.rating -= 1
    return


@register.filter
def datetime_format(dt):
    return dt.strftime('%H:%M:%S  %d-%m-%Y UT+0')

