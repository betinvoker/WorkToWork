from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import View, DetailView, ListView
from django.views.generic.base import ContextMixin
from django.db.models import Count
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Universities, Opinions, Ratings
from django.db.models import Q

#   Главная страница
class UniversitiesListView(ListView):
    context_object_name = 'universities'
    template_name = "search_reviews/index.html"
    
    queryset = Universities.objects.raw('SELECT search_reviews_universities.*, COUNT(search_reviews_opinions.id) AS count_opinions,'
        +' SUM(search_reviews_opinions.status = "True") as sum_opinion_true,'
        +' SUM(search_reviews_opinions.status = "False") as sum_opinion_false'
        +' FROM search_reviews_universities LEFT JOIN search_reviews_opinions ON search_reviews_universities.id = search_reviews_opinions.university_id'
        +' GROUP BY search_reviews_universities.id')

    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['popular_universities'] = Universities.objects.raw('SELECT search_reviews_universities.id, abbreviated,'
        +' COUNT(search_reviews_opinions.id) as count_opinion, SUM(search_reviews_opinions.status = "True") as sum_opinion_true,'
        +' SUM(search_reviews_opinions.status = "False") as sum_opinion_false'
        +' FROM search_reviews_universities LEFT JOIN search_reviews_opinions ON search_reviews_universities.id = search_reviews_opinions.university_id'
        +' GROUP BY search_reviews_universities.id ORDER BY count_opinion DESC LIMIT 5')

        return context

#   Выбранный университет
class OpinionsListView(ListView):
    context_object_name = 'university'
    template_name = "search_reviews/reviews.html"

    def get(self, request, id, *args, **kwargs):
        university = Universities.objects.get(id=id)
        opinions = Opinions.objects.filter(university_id = id)
        positive_opinions = Opinions.objects.filter(university_id = id).filter(status = "True").count
        negative_opinions = Opinions.objects.filter(university_id = id).filter(status = "False").count

        #   Пагинатор выбирает из таблицы Opinions 5 комментариев, на странице может быть не меньше двух комментариев
        paginator = Paginator(opinions, 5, orphans = 2)

        page_number = request.GET.get('page')
        try:
            page_obj = paginator.page(page_number)
        except PageNotAnInteger:
            page_obj = paginator.page(1)
        except EmptyPage:
            page_obj = paginator.page(paginator.num_pages)

        return render(request, "search_reviews/reviews.html", context = { "page_obj" : page_obj, "university" : university, "opinions" : opinions,
                                 "positive_opinions" : positive_opinions, "negative_opinions" : negative_opinions })


def rating_universities(request):
    rating = Ratings.objects.all()

    return render(request, "search_reviews/rating_universities.html", context = {"rating" : rating})
