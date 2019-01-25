from django.contrib import admin
from django.urls import path
from analysis import views


urlpatterns = [
	    path('home/', views.home,name="home"),
	    path('select/', views.select, name="select"),
	    path('result/', views.result, name="result"),
]