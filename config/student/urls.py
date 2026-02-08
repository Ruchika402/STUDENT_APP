from django.urls import path
from . import views


urlpatterns = [
    path('', views.home),
    path('index/', views.index),
    path('details/', views.details),
    path('version/', views.version),
    path('test/', views.test),
    path('test1/', views.test_method),
    path('greet/', views.greet),
    path('square/',views.square),
    path('all/',views.all_students),
    
    path('one/',views.one_student),
    path('teen/',views.teen),

    path('login/',views.Login_user),
    path('logout/',views.Logout_user),
    path('dashboard/',views.dashboard),

    path('list/', views.student_list),
    path('add/',views.add_student),
    path('update/<int:id>/', views.update_student),
    path('delete/<int:id>/', views.delete_student),
]