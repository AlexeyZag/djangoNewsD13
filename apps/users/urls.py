from django.urls import path
from allauth.account.views import LoginView, LogoutView
from .views import UserPage, upgrade_me, EditProfile

urlpatterns = [

    path('login/', LoginView.as_view(template_name='account/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='account/logout.html'), name='logout'),
    path('', UserPage.as_view(), name='mypage'),
    path('upgrade/', upgrade_me, name = 'upgrade'),
    path('edit/<int:pk>', EditProfile.as_view(), name= 'edit')

]