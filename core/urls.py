from django.urls import path

from . import views

app_name = 'core'
urlpatterns = [
    path('', views.index, name='index'),
    path("accounts/register", views.register, name="register"),
    path('add_list/', views.add_list, name='add_list'),
    path('list/<int:pk>', views.list_page, name='list_page'),
]
