
from django.urls import path
from .views import index, create_classroom_view, classroom_view_individual, classroom_view_computed, delete_classroom, edit_classroom, state_thread

urlpatterns = [
    path('', index, name='index'),
    path('classroom/create/', create_classroom_view, name='create_classroom'),
    path('classroom/<str:name>/individual', classroom_view_individual, name='classroom-individual'),
    path('classroom/<str:name>/computed', classroom_view_computed, name='classroom-computed'),
    path('classroom/delete/<str:name>', delete_classroom, name='delete_classroom'),
    path('classroom/edit/<str:name>', edit_classroom, name='edit_classroom'),
    path('classroom/thread/<str:name>', state_thread, name='thread'),
]
