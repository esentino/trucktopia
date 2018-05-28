from django.shortcuts import render, redirect

# Create your views here.
from django.views import View
from django.views.generic import ListView

from .models import ContractModel
from .celery import finish_trip
truck_weight = 500
truck_speed = 60

game_speed = 60

class ContractList(ListView):
    model = ContractModel
    context_object_name = 'contracts'
    paginate_by = 50

class SendTruck(View):
    def get(self, request, contract_id):
        from contractor.models import ContractModel
        contract = ContractModel.objects.get(pk=contract_id)
        to_delivered = contract.weight - contract.on_road - contract.delivered
        #contract.weight -= truck_weight if to_delivered > truck_weight else to_delivered
        contract.on_road += truck_weight if to_delivered > truck_weight else to_delivered
        contract.save()
        finish_trip.apply_async((contract_id, contract.weight), countdown=contract.distance / truck_speed * game_speed)
        return redirect('/')
