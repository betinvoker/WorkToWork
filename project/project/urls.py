from django.contrib import admin
from django.urls import path, re_path
from django.conf.urls import url
from django.views.generic import View, TemplateView, DetailView, ListView
from search_reviews import views

urlpatterns = [
    path('', views.UniversitiesListView.as_view(), name='review'),
    path('review/<int:id>/', views.OpinionsListView.as_view(), name='review'),
    path('admin/', admin.site.urls),
]