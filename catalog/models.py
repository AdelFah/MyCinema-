
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Genre(models.Model):
    name = models.CharField("Название", max_length=60, unique=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "жанр"
        verbose_name_plural = "жанры"

    def __str__(self):
        return self.name


class Country(models.Model):
    name = models.CharField("Название", max_length=80, unique=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "страна"
        verbose_name_plural = "страны"

    def __str__(self):
        return self.name


class ContentItem(models.Model):
    class Category(models.TextChoices):
        FILM = "film", "Фильмы"
        SERIES = "series", "Сериалы"
        ANIME = "anime", "Аниме"
        CARTOON = "cartoon", "Мультфильмы"

    class Status(models.TextChoices):
        WATCHED = "watched", "Просмотрено"
        WATCHING = "watching", "Смотрю"
        PLANNED = "planned", "В планах"

    title = models.CharField("Название", max_length=200)
    original_title = models.CharField(
        "Оригинальное название",
        max_length=200,
        blank=True
    )
    category = models.CharField(
        "Раздел",
        max_length=12,
        choices=Category.choices,
        default=Category.FILM
    )
    year = models.PositiveSmallIntegerField(
        "Год выхода",
        null=True,
        blank=True,
        validators=[MinValueValidator(1888), MaxValueValidator(2100)]
    )
    description = models.TextField("Краткое описание", blank=True)

    poster_url = models.URLField(
        "Ссылка на постер",
        blank=True
    )
    
    backdrop_url = models.URLField(
        "Ссылка на баннер",
        blank=True,
        max_length=500
    )

    trailer_url = models.URLField(
        "Ссылка для встраивания YouTube",
        max_length=500,
        blank=True
    )
    watch_url = models.URLField(
        "Ссылка на просмотр",
        blank=True
    )

    genres = models.ManyToManyField(
        Genre,
        blank=True,
        related_name="items",
        verbose_name="Жанры"
    )
    countries = models.ManyToManyField(
        Country,
        blank=True,
        related_name="items",
        verbose_name="Страны производства"
    )

    imdb_rating = models.DecimalField(
        "IMDb",
        max_digits=3,
        decimal_places=1,
        null=True,
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(10)]
    )
    kinopoisk_rating = models.DecimalField(
        "Кинопоиск",
        max_digits=3,
        decimal_places=1,
        null=True,
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(10)]
    )
    personal_rating = models.PositiveSmallIntegerField(
        "Моя оценка (из 10)",
        null=True,
        blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )

    status = models.CharField(
        "Статус",
        max_length=10,
        choices=Status.choices,
        default=Status.WATCHED
    )
    is_watchlisted = models.BooleanField(
        "В списке «Буду смотреть»",
        default=False
    )
    watched_on = models.DateField(
        "Дата просмотра",
        null=True,
        blank=True
    )
    seasons = models.PositiveSmallIntegerField(
        "Количество сезонов",
        null=True,
        blank=True
    )
    episodes = models.PositiveSmallIntegerField(
        "Количество серий",
        null=True,
        blank=True
    )
    created_at = models.DateTimeField(
        "Добавлено",
        auto_now_add=True
    )

    class Meta:
        ordering = ["-year", "title"]
        verbose_name = "произведение"
        verbose_name_plural = "произведения"

    def __str__(self):
        return f"{self.title} ({self.year})" if self.year else self.title
