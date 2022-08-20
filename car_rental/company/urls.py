from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('Automobiles', views.display, name='display'),
    path('Contact-Us', views.contact, name='contact'),
    path('Automobiles/<int:car_id>', views.automobile, name='automobile'),
    path('Automobiles/reserve', views.reserve, name='reserve'),
    path('admins/', views.admins, name='admins'),
    path('admins/car_clear', views.clearing, name='clearing'),
    path('admins/hire_out/<int:reserve_id>', views.hire_out, name='hire_out'),
    path('admins/car_clear/<int:reserve_id>',
         views.car_clear, name='car_clear'),
    path('admins/feedback', views.feedback, name='feedback'),
   









]
