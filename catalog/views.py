
import random

from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .forms import ContentItemForm
from .models import ContentItem, Genre, Country





def home(request):
    """Главная страница с ежедневными рекомендациями."""

    today = timezone.localdate()
    rng = random.Random(today.toordinal())

    all_items = list(
        ContentItem.objects.prefetch_related(
            "genres",
            "countries"
        ).all()
    )

    # Рекомендации формируются из всей библиотеки
    featured_items = all_items.copy()
    rng.shuffle(featured_items)
    featured_items = featured_items[:6]

    categories = [
        ("film", "Фильмы"),
        ("series", "Сериалы"),
        ("anime", "Аниме"),
        ("cartoon", "Мультфильмы"),
    ]

    shelves = []

    for category_value, category_label in categories:
        category_items = [
            item for item in all_items
            if item.category == category_value
        ]

        rng.shuffle(category_items)

        shelves.append({
            "value": category_value,
            "label": category_label,
            "items": category_items[:10],
        })

    return render(
        request,
        "catalog/home.html",
        {
            "featured_items": featured_items,
            "shelves": shelves,
        }
    )



def catalog(request, category=None):
    items = ContentItem.objects.prefetch_related(
        "genres",
        "countries"
    ).all()

    if category:
        items = items.filter(category=category)

    query = request.GET.get("q", "").strip()
    genre_id = request.GET.get("genre", "")
    country_id = request.GET.get("country", "")
    year = request.GET.get("year", "")
    sort = request.GET.get("sort", "-year")

    if query:
        items = items.filter(
            Q(title__icontains=query) |
            Q(original_title__icontains=query)
        )

    if genre_id.isdigit():
        items = items.filter(genres__id=int(genre_id))

    if country_id.isdigit():
        items = items.filter(countries__id=int(country_id))

    if year.isdigit():
        items = items.filter(year=int(year))

    allowed_sorts = {
        "-year",
        "year",
        "title",
        "-personal_rating",
        "-imdb_rating",
        "-kinopoisk_rating",
    }

    if sort not in allowed_sorts:
        sort = "-year"

    items = items.order_by(sort, "title").distinct()

    context = {
        "items": items,
        "genres": Genre.objects.all(),
        "countries": Country.objects.all(),
        "years": ContentItem.objects.exclude(
            year__isnull=True
        ).values_list(
            "year", flat=True
        ).distinct().order_by("-year"),

        "selected_category": category or "",
        "query": query,
        "selected_genre": genre_id,
        "selected_country": country_id,
        "selected_year": year,
        "selected_sort": sort,
        "categories": ContentItem.Category.choices,
    }

    return render(request, "catalog/catalog.html", context)


def item_detail(request, pk):
    item = get_object_or_404(
        ContentItem.objects.prefetch_related("genres", "countries"),
        pk=pk
    )

    return render(request, "catalog/detail.html", {"item": item})


def item_create(request):
    if request.method == "POST":
        form = ContentItemForm(request.POST)

        if form.is_valid():
            item = form.save()
            return redirect("item_detail", pk=item.pk)
    else:
        form = ContentItemForm()

    return render(
        request,
        "catalog/item_form.html",
        {"form": form, "page_title": "Добавить произведение"}
    )


def item_edit(request, pk):
    item = get_object_or_404(ContentItem, pk=pk)

    if request.method == "POST":
        form = ContentItemForm(request.POST, instance=item)

        if form.is_valid():
            form.save()
            return redirect("item_detail", pk=item.pk)
    else:
        form = ContentItemForm(instance=item)

    return render(
        request,
        "catalog/item_form.html",
        {"form": form, "page_title": "Редактировать произведение"}
    )


def update_item_status(request, pk):
    item = get_object_or_404(ContentItem, pk=pk)

    if request.method == "POST":
        new_status = request.POST.get("status")

        if new_status in ContentItem.Status.values:
            item.status = new_status
            item.save(update_fields=["status"])

    return redirect("item_detail", pk=item.pk)


def toggle_watchlist(request, pk):
    item = get_object_or_404(ContentItem, pk=pk)

    if request.method == "POST":
        item.is_watchlisted = not item.is_watchlisted
        item.save(update_fields=["is_watchlisted"])

    return redirect("item_detail", pk=item.pk)


def watchlist(request):
    items = ContentItem.objects.filter(
        is_watchlisted=True
    ).prefetch_related(
        "genres",
        "countries"
    ).order_by("-year", "title")

    return render(
        request,
        "catalog/catalog.html",
        {
            "items": items,
            "watchlist_page": True,
        }
    )
