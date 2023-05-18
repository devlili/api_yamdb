import django_filters

from reviews.models import Title


class TitleFilter(django_filters.FilterSet):
    genre = django_filters.AllValuesFilter(field_name="genre__slug")
    category = django_filters.AllValuesFilter(field_name="category__slug")
    year = 'year'
    name = django_filters.CharFilter(field_name='name', lookup_expr='contains')

    class Meta:
        model = Title
        fields = ("genre", "category", "year", "name")
