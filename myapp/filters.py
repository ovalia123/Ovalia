import django_filters
from gestion.models import *
from django.forms.widgets import TextInput

class ProductFilter(django_filters.FilterSet):
    material = django_filters.MultipleChoiceFilter(
        field_name='materiaux',
        choices=Product.materiaux_choices,
        widget=django_filters.widgets.CSVWidget,
        label='Matériaux',
    )

    class Meta:
        model = Product
        fields = ['materiaux']