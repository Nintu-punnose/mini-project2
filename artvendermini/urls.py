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
    path('artist_uploaded_auction/', views.artist_uploaded_auction, name='artist_uploaded_auction'),
    path('artist_auction_view/<int:art_id>/', views.artist_auction_view, name='artist_auction_view'),
    path('artist_auction_view_all/<int:bid_id>/', views.artist_auction_view_all, name='artist_auction_view_all'),

    
    path('notification/',views.notification,name='notification'),
    path('notification_view/<int:art_id>',views.notification_view,name='notification_view'),

    path('update_auction/',views.update_auction, name='update_auction'),
    path('delete_auction/', views.delete_auction, name='delete_auction'),
    # path('approve_bid/<int:art_id>/', views.approve_bid, name='approve_bid'),


    path('AuctionPayment/<int:id>', views.AuctionPayment, name='AuctionPayment'),
    path('paymenthandler/', views.paymenthandler, name='paymenthandler'),
    path('admin_auction/',views.admin_auction,name='admin_auction'),
    path('admin_auction_details/<int:id>/',views.admin_auction_details,name='admin_auction_details'),

    path('admin_rejection/',views.admin_rejection,name='admin_rejection'),

    path('invoice', views.invoice, name='invoice'),
    

    #delivary Agent

    path('delivary_agent_registration',views.delivary_agent_registration,name="delivary_agent_registration"),
    path('admin_delivary_view/',views.admin_delivary_view,name="admin_delivary_view"),
    path('admin_delivary_registration/<int:delivary_id>/',views.admin_delivary_registration,name="admin_delivary_registration"),
    path('delivary_profile/',views.delivary_profile,name="delivary_profile"),
    path('admin_delivary_approval/',views.admin_delivary_approval,name="admin_delivary_approval"),
  
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)





   