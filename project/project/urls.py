from django.contrib import admin
from django.urls import path, re_path
from django.conf.urls import url
from django.views.generic import TemplateView, ListView
from search_reviews import views

urlpatterns = [
    path('', views.index),
    path('review/<int:id>/', views.reviews, name='review'),
    path('admin/', admin.site.urls),
]