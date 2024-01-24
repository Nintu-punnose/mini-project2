from django.urls import path
from django.conf.urls.static import static
from artvendor import settings
from . import views
from django.contrib.auth import views as auth_views
from django.contrib import admin
from django.urls import path



urlpatterns = [
    path('',views.login, name='login'),
    path('signup',views.signup, name='signup'),
    path('Artist_view/',views.Artist_view,name='Artist_view'),
    path('logout_view/', views.logout_view, name='logout_view'),
    path('upload_art/', views.upload_art, name='upload_art'),
    path('index/', views.index, name='index'),
    path('admin_pannel/', views.admin_pannel, name='admin_pannel'),
    path('update_art/<int:art_id>/',views.update_art,name='update_art'),
    path('delete_art/<int:art_id>/', views.delete_art, name='delete_art'),
    path('seller_profile/',views.seller_profile,name="seller_profile"),
    path('images/',views.images,name='images'),
    path('image_detail/<int:id>/',views.image_detail,name='image_detail'),
    path('admin_dashboard/',views.admin_dashboard,name='admin_dashboard'),
    path('Artist/',views.Artist,name='Artist'),
    path('Artist_detail/<int:id>/',views.Artist_detail,name='Artist_detail'),

    path('password_reset/',auth_views.PasswordResetView.as_view(),name='password_reset'),
    path('password_reset/done/',auth_views.PasswordResetDoneView.as_view(),name='password_reset_done'),
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(),name='password_reset_confirm'),
    path('reset/done/',auth_views.PasswordResetCompleteView.as_view(),name='password_reset_complete'),

    path('addtype/', views.addtype, name='addtype'),
    path('addsize/', views.addsize, name='addsize'),
    path('delete_art_type/<int:type_id>/', views.delete_art_type, name='delete_art_type'),
    path('delete_art_size/<int:size_id>/', views.delete_art_size, name='delete_art_size'),

    # cart
    path('add_to_cart/<int:art_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<int:art_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/', views.view_cart, name='cart'),

    #email
    path('email/', views.email, name='email'),

    #alluser
    path('alluser/', views.alluser, name='alluser'),

    #payment
    path('payment/', views.payment, name='payment'),
    path('paymenthandler/', views.paymenthandler, name='paymenthandler'),
    path('admin/', admin.site.urls),
    path('orders', views.orders, name='orders'),

    #auction
    path('auction',views.auction,name='auction'),
    path('auction_uploadform',views.auction_uploadform,name='auction_uploadform'),
    path('auction_bid/<int:auction_id>/', views.auction_bid, name='auction_bid'),

    path('get_latest_bid/<int:auction_id>/', views.get_latest_bid, name='get_latest_bid'),



]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
