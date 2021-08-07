import datetime
from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.pagination import PageNumberPagination

from main.models import Operations, Clients
from main.serializers.serializer import ClientSerializer, DetailClientSerializer, OperationSerializer
from main.serializers.serializer_utils import get_days_count


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 100


class ClientsListView(ListAPIView):
    serializer_class = ClientSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        return Clients.objects.prefetch_related('wallets_set').all()


class ClientDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = DetailClientSerializer

    def get_queryset(self):
        return Clients.objects.prefetch_related('wallets_set').prefetch_related('wallets_set__operations_set').filter(pk=self.kwargs.get('pk'))


class HistoryListView(ListAPIView):
    serializer_class = OperationSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        month = self.request.GET.get('month')
        year = self.request.GET.get('year')
        if year and month:
            return Operations.objects.select_related('wallet').select_related('wallet__client').order_by('-date')\
                .filter(date__range=(
                    datetime.datetime(year=int(year), month=int(month), day=1),
                    datetime.datetime(year=int(year), month=int(month), day=get_days_count(int(year), int(month)))
                ))
        elif year:
            return Operations.objects.select_related('wallet').select_related('wallet__client').order_by('-date')\
                .filter(date__range=(
                    datetime.datetime(year=int(year), month=1, day=1),
                    datetime.datetime(year=int(year), month=12, day=31)
                ))
        else:
            return Operations.objects.select_related('wallet').select_related('wallet__client').order_by('-date').all()

