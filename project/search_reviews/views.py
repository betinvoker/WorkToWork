from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import View, DetailView, ListView
from django.views.generic.base import ContextMixin
from django.db.models import Count
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Universities, Opinions

#   Список университетов
def index(request):
    universities = Universities.objects.raw('SELECT search_reviews_universities.*, COUNT(search_reviews_opinions.id) AS count_opinions,'
        +' SUM(search_reviews_opinions.status = "True") as sum_opinion_true,'
        +' SUM(search_reviews_opinions.status = "False") as sum_opinion_false'
        +' FROM search_reviews_universities LEFT JOIN search_reviews_opinions ON search_reviews_universities.id = search_reviews_opinions.university_id'
        +' GROUP BY search_reviews_universities.id')
    
    popular_universities = Universities.objects.raw('SELECT search_reviews_universities.id, abbreviated,'
        +' COUNT(search_reviews_opinions.id) as count_opinion, SUM(search_reviews_opinions.status = "True") as sum_opinion_true,'
        +' SUM(search_reviews_opinions.status = "False") as sum_opinion_false'
        +' FROM search_reviews_universities LEFT JOIN search_reviews_opinions ON search_reviews_universities.id = search_reviews_opinions.university_id'
        +' GROUP BY search_reviews_universities.id ORDER BY count_opinion DESC LIMIT 5')
    #   Пагинатор выбирает из таблицы Universities 8 университета и выводит их на страницу
    paginator = Paginator(universities, 8, orphans = 3)

    page_number = request.GET.get('page')
    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    return render(request, "search_reviews/index.html", context = {"page_obj" : page_obj, "popular_universities" : popular_universities })

#   Выбранный университет
def reviews(request, id):
    university = Universities.objects.get(pk = id)
    opinions = Opinions.objects.filter(university_id = id)
    count_opinions = Opinions.objects.filter(university_id = id).count
    positive_opinions = Opinions.objects.filter(university_id = id).filter(status = "True").count
    negative_opinions = Opinions.objects.filter(university_id = id).filter(status = "False").count
    #   Пагинатор выбирает из таблицы Universities 8 университета и выводит их на страницу
    paginator = Paginator(opinions, 5, orphans = 2)

    page_number = request.GET.get('page')
    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    return render(request, "search_reviews/reviews.html", context = { "page_obj" : page_obj, "university" : university, "opinions" : opinions, 
        "count_opinions" : count_opinions, "positive_opinions" : positive_opinions, "negative_opinions" : negative_opinions })