from django.forms.widgets import DateInput
from django_filters import FilterSet, DateFilter
from .models import Post


class PostFilter(FilterSet):
    class Meta:
        model = Post

        fields = {

            'title': ['icontains'],
            # количество товаров должно быть больше или равно
            # 'quantity': ['gt'],
            # 'price': [
            #     'lt',  # цена должна быть меньше или равна указанной
            #     'gt',  # цена должна быть больше или равна указанной
            # ],
        }


class SearchFilter(FilterSet):
    created = DateFilter(label="Topic newer then: ", field_name='created_at', lookup_expr='gt',
                         widget=DateInput(attrs={'type': 'date'}, format=('%d/%m/%Y')))

    class Meta:
        model = Post

        fields = {
            'title': ['icontains'],
            'category_id': ['exact'],
            # 'created_at': ['lt','gt'],
        }
