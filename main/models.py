from django.db import models
from uuid import uuid4
from psqlextra.types import PostgresPartitioningMethod
from psqlextra.models import PostgresPartitionedModel


class BaseModal(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4())

    class Meta:
        abstract = True


class Clients(BaseModal):
    name = models.CharField(max_length=255)
    birthday = models.DateField()

    class Meta:
        db_table = 'clients'


class Wallets(BaseModal):
    client = models.ForeignKey(Clients, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=20, decimal_places=2)

    class Meta:
        db_table = 'wallets'


class Operations(BaseModal, PostgresPartitionedModel):
    method = PostgresPartitioningMethod.RANGE
    key = ['date']

    OPERATION_TYPE = (
        ('OUT', 'Outcome'),
        ('IN', 'Income'),
    )

    wallet = models.ForeignKey(Wallets, on_delete=models.CASCADE)
    type = models.CharField(max_length=10, choices=OPERATION_TYPE)
    date = models.DateTimeField()
    operation_amount = models.DecimalField(max_digits=20, decimal_places=2)
    total_amount = models.DecimalField(max_digits=20, decimal_places=2)

    class Meta:
        db_table = 'operations'
