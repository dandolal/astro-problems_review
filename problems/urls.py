from django.urls import path

from . import views

app_name = 'problems'
urlpatterns = [# ex: /polls/
    path('<str:order_by>/<int:order>/', views.problems_list, name='problems_list'),
    # path('', views.problems_list, name='problems_list'),
    # ex: /polls/5/
    path('<int:problem_id>/', views.problem, name='problem'), # ex: /polls/5/results/
    path('<int:problem_id>/solution/', views.view_solution, name='view_solution'),

    path('<int:problem_id>/delete/', views.delete_problem, name='delete_problem'), # new
    path('<int:problem_id>/edit/', views.edit_problem, name='edit_problem'), # new
    path('new/', views.problem_new, name='problem_new'),

    path('authors/', views.authors_list, name='authors_list'),

    path('authors/<int:author_id>', views.view_author, name='view_author'),

    path('themes/', views.themes_list, name='themes_list'),
    path('themes/<int:theme_id>', views.theme_view, name='theme_view'),

    path('events/', views.events_list, name='events_list'),

    path('events/<int:event_id>', views.event, name='event'),

    # path('search/', views.search, name='search'),

    path('<int:problem_id>/add_rating/', views.add_rating, name='add_rating'),
    path('<int:problem_id>/reduce_rating/', views.reduce_rating, name='reduce_rating'),
    path('<int:problem_id>/download/', views.download_problem, name='download_problem'),
    path('search/', views.search, name='search'),

    path('game/<int:game_id>', views.ugame, name='game'),
    path('start_game/', views.start_game, name='start_game'),
    path('end_game/<int:result>', views.end_game, name='end_game'),
    path('continue_game/<int:playerid>', views.get_player_game, name='continue_game')
]
