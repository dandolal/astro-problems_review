from django import forms

from .models import Problem, Author


class ProblemForm(forms.Form):
    title = forms.CharField(required=False, initial='', max_length=100, label='Название',
                            label_suffix='::')
    text = forms.CharField(required=True, widget=forms.Textarea)
    complexity = forms.IntegerField(initial=0)
    solution = forms.CharField(required=True, widget=forms.Textarea)
    # AUTHORS = [(author.id, author.name) for author in Author.objects.order_by('name')]
    AUTHORS = ([(0, 'Да'), (1, 'Нет')])
    existing_authors = forms.MultipleChoiceField(required=False, choices=AUTHORS,
                                                 widget=forms.CheckboxSelectMultiple)
    authors = forms.CharField(widget=forms.Textarea)

    THEMES = ([('Астрофизика', 'Астрофизика'),
               ('Оптика', 'Оптика'),
               ('Небесная сфера', 'Небесная сфера'),
               ('Небесная механика', 'Небесная механика'),
               ('Геометрия', 'Геометрия'),
               ('Время', 'Время'),
               ('Космология', 'Космология')])
    themes = forms.MultipleChoiceField(required=True, choices=THEMES,
                                       widget=forms.CheckboxSelectMultiple)

    year = forms.IntegerField(initial=0, required=False)
    event_name = forms.CharField(initial='', required=False)


class ConfirmDeleteForm(forms.Form):
    CHOICES = ([(True, 'Да'), (False, 'Нет')])
    is_confirmed = forms.ChoiceField(required=True, choices=CHOICES,
                                     widget=forms.RadioSelect(attrs={'class': 'Radio'}),
                                     initial=False)


class AuthorSearchForm(forms.Form):
    name = forms.CharField(required=True, initial='', max_length=100)

