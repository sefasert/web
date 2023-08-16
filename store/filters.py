import django_filters

from .models import Product

class ProductFilter(django_filters.FilterSet):
    price_gt = django_filters.NumberFilter(field_name="price", lookup_expr="gte")
    price_lt = django_filters.NumberFilter(field_name="price", lookup_expr="lte")

    class Meta:
        model = Product
        fields = ["category", "brand", "yeni"]
