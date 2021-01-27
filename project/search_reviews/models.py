from django.db import models

class Universities(models.Model):
    abbreviated = models.CharField(max_length=100, verbose_name="Аббревиатура", null=False)
    name = models.CharField(max_length=300, verbose_name="Полное название", null=False)
    link = models.CharField(max_length=300, verbose_name="Ссылка на страницу ресурса", null=False)
    logo = models.CharField(max_length=50, verbose_name="Герб университета", null=False)

    class Meta:
        verbose_name = "Университет"
        verbose_name_plural = "Университеты"
        unique_together = ("abbreviated", "name", "link", "logo")

    def __str__(self):
        return f"{self.id}, {self.abbreviated}, {self.name}, {self.link} , {self.logo}"

class Opinions(models.Model):
    text = models.TextField(verbose_name="Отзыв", null=False)
    date_opinion = models.CharField(max_length=40, verbose_name="Дата отзыва", null=False)
    status = models.CharField(max_length=5, verbose_name="Статус", null=False)
    status_ai = models.CharField(max_length=5, verbose_name="Статус ИИ", null=True)
    university = models.ForeignKey(Universities, on_delete=models.CASCADE, verbose_name="Университет", null=False)

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"

    def __str__(self):
        return f"{self.id}, {self.text}, {self.date_opinion}, {self.status}, {self.status_ai}, {self.university}"

class Ratings(models.Model):
    name = models.TextField(verbose_name="Название университета", null=False)
    link = models.TextField(verbose_name="Ссылка на его страницу", null=False)
    rating_summary = models.IntegerField(verbose_name="Сводный рейтинг", null=True)
    rating_education = models.IntegerField(verbose_name="Образование", null=True)
    rating_brand = models.IntegerField(verbose_name="Бренд", null=True)
    rating_research = models.IntegerField(verbose_name="Исследования", null=True)
    rating_socialization = models.IntegerField(verbose_name="Социализация", null=True)
    rating_internationalization = models.IntegerField(verbose_name="Интернационализация", null=True)
    rating_innovation = models.IntegerField(verbose_name="Инновации", null=True)

    class Meta:
        verbose_name = "Рейтинги университета"
        verbose_name_plural = "Рейтинги университетов"

        ordering = [
            ['name'],
            ['-rating_summary'],
            ['-rating_education'],
            ['-rating_brand'],
            ['-rating_research'],
            ['-rating_socialization'],
            ['-rating_internationalization'],
            ['-rating_innovation'],
        ]

    def __str__(self):
        return f"{self.id}, {self.name}, {self.link} , {self.rating_summary} , {self.rating_education} , {self.rating_brand} , {self.rating_research} , {self.rating_socialization} , {self.rating_internationalization} , {self.rating_innovation}"