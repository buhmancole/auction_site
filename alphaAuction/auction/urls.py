from django.urls import path, include
from django.views.generic import TemplateView

from . import views

app_name = 'auction'
urlpatterns = [
    path('webpush/', include('webpush.urls')),
    path('', views.index, name='index'),
    path('validateAuction/', views.validateAuction, name='validateAuction'),
    path('auction/<str:phrase>/', views.auction, name='auction'),
    path('auction/<str:phrase>/item/<int:id>/', views.item, name='item'),
    path('login/', views.loginPage, name='login'),
    path('login/process', views.processLogin, name='processLogin'),
    path('login/forgotPassword', views.forgotPassword, name='forgotPassword'),
    path('login/forgotPassword/process', views.processForgotPassword, name='processForgotPassword'),
    path('login/resetPassword', views.resetPassword, name='resetPassword'),
    path('login/resetPassword/process', views.resetPasswordProcess, name='resetPasswordProcess'),
    path('profile/<int:id>/', views.profile, name='profile'),
    path('profile/', views.profile, name='profile'),
    path('myAuctions/', views.myAuctions, name='myAuctions'),
    path('signup/', views.signup, name='signup'),
    path('signup/process', views.processSignup, name='processSignup'),
    path('processLogout', views.processLogout, name='processLogout'),
    path('auction/<str:phrase>/item/<int:id>/bid', views.processBid, name='processBid'),
    path('auction/<str:phrase>/item/<int:id>/favorite', views.processFavorite, name='processFavorite'),
    path('sw.js', TemplateView.as_view(template_name='auction/sw.js', content_type='application/x-javascript')),
    path('auctionEnd/', views.auctionEndPush, name='testPush')
]
