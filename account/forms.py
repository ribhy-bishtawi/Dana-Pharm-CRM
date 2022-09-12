import django_filters

from account.customer import Customer


class CustomerFilter(django_filters.FilterSet):
    class Meta:
        model = Customer
        fields = '__all__'
