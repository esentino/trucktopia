import os
from random import randint

from celery import Celery
from django.db.models import F

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'trucktopia.settings')

app = Celery('contractor')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


@app.on_after_configure.connect
def setup_schedule_tasks(sender, **kwargs):
    sender.add_periodic_task(15.0, create_contract.s(), name="Create the contract")
    sender.add_periodic_task(15.0, finish_contract.s(), name="Finish contract")


@app.task
def create_contract():
    from contractor.models import ContractModel
    """
    Utworzenie nowego zlecenia
    :return:
    """
    contract = ContractModel()
    contract.weight = randint(10, 1000)
    contract.price = randint(1000, 10000)
    contract.distance = randint(10, 1000)
    contract.save()


@app.task
def finish_contract():
    """
    Realiacja zlecenia
    :return:
    """
    from contractor.models import ContractModel
    contracts = ContractModel.objects.filter(weight__lte=F('delivered'))
    for contract in contracts.all():
        contract.delete()


@app.task
def finish_trip(contract_id, weight):
    from contractor.models import ContractModel
    contract = ContractModel.objects.get(pk=contract_id)
    contract.on_road -= weight
    contract.delivered += weight
    contract.save()
