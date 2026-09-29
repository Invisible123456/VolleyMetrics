from django.contrib import admin
from django.urls import path

import dashboard.views


urlpatterns = [
    
    path('home/', dashboard.views.home, name='home'), 

]