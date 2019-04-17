from django.contrib import admin

from .models import Problem, Author, Event, Theme


# class AuthorInline(admin.TabularInline):
#     model = Author
#     extra = 1


# class ProblemAdmin(admin.ModelAdmin):
#     fieldsets = [
#         (None, {'fields': ['problem_text']}),
#         ('Date information', {'fields': ['pub_date'],
#                               'classes': ['collapse']}),
#     ]
#     inlines = [AuthorInline]
#     # list_display = ('problem_text')
#     # list_filter = ['pub_date']
#     # search_fields = ['question_text']

admin.site.register(Problem)
admin.site.register(Author)
admin.site.register(Event)
admin.site.register(Theme)

