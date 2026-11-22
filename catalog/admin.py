
from django.contrib import admin
from .models import ContentItem, Genre, Country


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    search_fields = ["name"]


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    search_fields = ["name"]


@admin.register(ContentItem)
class ContentItemAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "category",
        "year",
        "imdb_rating",
        "kinopoisk_rating",
        "personal_rating",
        "status",
    )

    list_filter = ("category", "status", "year", "genres", "countries")
    search_fields = ("title", "original_title", "description")
    filter_horizontal = ("genres", "countries")
    list_per_page = 30
