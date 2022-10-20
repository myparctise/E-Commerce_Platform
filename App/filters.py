import django_filters
from .models import Product_details
from django_filters import CharFilter,BooleanFilter

class SearchingFilter(django_filters.FilterSet):
    product_title = CharFilter(field_name="product_title",label="Product name",lookup_expr="icontains")
    on_sale = BooleanFilter(field_name="on_sale",label="Sale ")
    class Meta:
        model = Product_details
        fields = {"product_title","on_sale"}

