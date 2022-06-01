"""
this file contain the routes of the different endpoints. 
"""

from django.urls import path 
from . import views


"""
We have one route ‘/todos’ as a demonstration. What we want to achieve is that when a request is made to localhost:8000/api/todos, 
you should get a JSON response with the list of todo instances. 
"""
urlpatterns = [ 
    path('todos/', views.TodoListCreate.as_view()), #we define TodoList view in the api/views.py 
    path('todos/<int:pk>',views.TodoRetrieveUpdateDestroy.as_view()),
    path('todos/<int:pk>/complete', views.TodoToggleComplete.as_view()), #That is, if a request is sent to localhost:8000/api/todos/123/complete, the todo with id ‘123’ will be marked as complete.
    path('signup/', views.signup),
    path('login/', views.login),
]