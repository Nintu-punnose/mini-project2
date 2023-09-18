from django.urls import path
from django.conf.urls.static import static
from artvendor import settings
from . import views


urlpatterns = [
    path('login',views.login, name='login'),
    path('signup',views.signup, name='signup'),
    path('Artist_view/',views.Artist_view,name='Artist_view'),
    path('logout_view/', views.logout_view, name='logout_view'),
    path('upload_art/', views.upload_art, name='upload_art'),
    path('', views.index, name='index'),
    path('admin_pannel/', views.admin_pannel, name='admin_pannel'),
    path('update_art/<int:art_id>/',views.update_art,name='update_art'),
    path('delete_art/<int:art_id>/', views.delete_art, name='delete_art'),
    path('seller_profile/',views.seller_profile,name="seller_profile"),
    path('images/',views.images,name='images'),
    path('image_detail/<int:id>/',views.image_detail,name='image_detail'),
    path('admin_dashboard/',views.admin_dashboard,name='admin_dashboard'),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)