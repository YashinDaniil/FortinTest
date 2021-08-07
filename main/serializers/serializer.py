import datetime

from rest_framework import serializers
from main.models import Clients, Wallets, Operations
from main.serializers.serializer_utils import get_days_count


class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallets
        fields = [
            'id',
            'amount'
        ]


class OperationSerializerMinimalize(serializers.ModelSerializer):
    class Meta:
        model = Operations
        fields = [
            'id',
            'type',
            'date',
            'operation_amount',
            'total_amount',
        ]


class ClientSerializer(serializers.ModelSerializer):
    wallet = serializers.SerializerMethodField('get_wallet')

    def get_wallet(self, client):
        qs = client.wallets_set.all()
        serializer = WalletSerializer(instance=qs, many=True)
        return serializer.data

    class Meta:
        model = Clients
        fields = [
            'id',
            'name',
            'birthday',
            'wallet'
        ]


class DetailClientSerializer(serializers.ModelSerializer):
    operations = serializers.SerializerMethodField('get_operations')
    wallet = serializers.SerializerMethodField('get_wallet')

    def get_operations(self, client):
        year = self.context.get('request').query_params.get('year')
        month = self.context.get('request').query_params.get('month')
        opa = {}
        for i in client.wallets_set.all():
            if year and month:
                opa[str(i.id)] = OperationSerializerMinimalize(instance=i.operations_set.order_by('-date').filter(
                    date__range=(
                        datetime.datetime(year=int(year), month=int(month), day=1),
                        datetime.datetime(year=int(year), month=int(month), day=get_days_count(int(year), int(month)))
                    )
                ), many=True).data
            elif year:
                opa[str(i.id)] = OperationSerializerMinimalize(instance=i.operations_set.order_by('-date').filter(
                    date__range=(
                        datetime.datetime(year=int(year), month=1, day=1),
                        datetime.datetime(year=int(year), month=12, day=1)
                    )
                ), many=True).data
            else:
                opa[str(i.id)] = OperationSerializerMinimalize(instance=i.operations_set.order_by('-date').all(), many=True).data
        return opa


    def get_wallet(self, client):
        qs = client.wallets_set.all()
        serializer = WalletSerializer(instance=qs, many=True)
        return serializer.data

    class Meta:
        model = Clients
        fields = [
            'id',
            'name',
            'birthday',
            'wallet',
            'operations'
        ]


class OperationSerializer(serializers.ModelSerializer):
    client = serializers.SerializerMethodField('get_client')

    def get_client(self, operation):
        return operation.wallet.client_id

    class Meta:
        model = Operations
        fields = [
            'id',
            'client',
            'wallet_id',
            'type',
            'date',
            'operation_amount',
            'total_amount',
        ]
