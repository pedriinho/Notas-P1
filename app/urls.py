
from django.urls import path
from .views import index, create_classroom_view, classroom_view, delete_classroom, edit_classroom

urlpatterns = [
    path('', index, name='index'),
    path('classroom/create/', create_classroom_view, name='create_classroom'),
    path('classroom/<str:name>', classroom_view, name='classroom'),
    path('classroom/delete/<str:name>', delete_classroom, name='delete_classroom'),
    path('classroom/edit/<str:name>', edit_classroom, name='edit_classroom'),
]
