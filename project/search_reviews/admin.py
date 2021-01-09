from django.contrib import admin
from .models import Universities, Opinions

#   Показывает комментарии относящиеся к выбранному университету
class UniversitiesInline(admin.TabularInline):
    model = Opinions

@admin.register(Universities)
class UniversitiesAdmin(admin.ModelAdmin):
    list_display = ("id", "abbreviated", "name", "link", "logo")
    search_fields = ("abbreviated",)
    #   Показывает комментарии относящиеся к выбранному университету
    inlines = [UniversitiesInline]

@admin.register(Opinions)
class OpinionsAdmin(admin.ModelAdmin):
    list_display = ("id", "text", "date_opinion", "status", "status_ai", "university_id")
    list_filter = ("status",)
    search_fields = ("text",)
