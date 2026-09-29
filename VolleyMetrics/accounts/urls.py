from django.contrib import admin
from django.urls import path

import accounts.views
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('', LoginView.as_view(
            template_name='accounts/login.html',
            redirect_authenticated_user=True),
        name='login'),
    path('logout/', LogoutView.as_view(), name='logout',)

]