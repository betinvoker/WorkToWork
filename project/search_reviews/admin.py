from django.contrib import admin
from .models import Universities, Opinions, Ratings

#   Показывает комментарии относящиеся к выбранному университету
class UniversitiesInline(admin.TabularInline):
    model = Opinions

@admin.register(Universities)
class UniversitiesAdmin(admin.ModelAdmin):
    list_display = ("id", "abbreviated", "name", "link", "logo")
    list_display_links = ("id", "abbreviated", "name")
    search_fields = ("name",)
    empty_value_display = "---"
    list_per_page = 50
    #   Показывает комментарии относящиеся к выбранному университету
    inlines = [UniversitiesInline]

@admin.register(Opinions)
class OpinionsAdmin(admin.ModelAdmin):
    list_display = ("id", "text", "date_opinion", "status", "status_ai", "university_id")
    list_editable = ("text",)
    list_filter = ("status",)
    search_fields = ("text",)
    empty_value_display = "---"
    list_per_page = 15

@admin.register(Ratings)
class RatingsAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "link", "rating_summary", "rating_education", "rating_brand", "rating_research", "rating_socialization", "rating_internationalization", "rating_innovation")
    list_display_links = ("id", "name")
    search_fields = ("name",)
    empty_value_display = "---"