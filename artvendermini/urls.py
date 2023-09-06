from django.urls import path
from . import views

urlpatterns = [
    path('',views.login_view, name='login'),
    path('signup',views.signup, name='signup'),
    path('Artist_view',views.Artist_view,name='Artist_view'),
    path('logout/', views.logout_view, name='logout'),
]