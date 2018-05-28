from django.contrib.auth.models import User
from django.db import models


class ContractModel(models.Model):
    weight = models.IntegerField()
    on_road = models.IntegerField(default=0)
    delivered = models.IntegerField(default=0)
    price = models.IntegerField()
    distance = models.IntegerField()
    taken = models.ForeignKey(User, default=None, null=True, on_delete=models.SET_NULL)
