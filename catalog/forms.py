
from django import forms
from .models import ContentItem


class ContentItemForm(forms.ModelForm):
    class Meta:
        model = ContentItem

        fields = [
            "title",
            "original_title",
            "category",
            "year",
            "description",
            "poster_url",
            "backdrop_url",
            "watch_url",
            "genres",
            "countries",
            "imdb_rating",
            "kinopoisk_rating",
            "personal_rating",
            "status",
            "seasons",
            "episodes",
        ]

        labels = {
            "watch_url": "Ссылка на просмотр фильма",
            "countries": "Страны производства",
            "poster_url": "Ссылка на вертикальный постер",
            "backdrop_url": "Ссылка на горизонтальный баннер",
        }

        widgets = {
            "description": forms.Textarea(attrs={"rows": 4}),

            "genres": forms.SelectMultiple(attrs={
                "class": "genre-select",
            }),

            "countries": forms.SelectMultiple(attrs={
                "class": "country-select",
            }),

            "poster_url": forms.URLInput(attrs={
                "placeholder": "Ссылка на вертикальный постер",
            }),

            "backdrop_url": forms.URLInput(attrs={
                "placeholder": "Ссылка на изображение 16:9",
            }),

            "watch_url": forms.URLInput(attrs={
                "placeholder": "Ссылка на сайт для просмотра",
                "style": "width: 100%;",
            }),

            "personal_rating": forms.Select(
                choices=[("", "Не оценено")] + [
                    (i, f"{i}/10") for i in range(1, 11)
                ]
            ),
        }
