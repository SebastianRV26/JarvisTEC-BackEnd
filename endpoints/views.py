from django.shortcuts import render
from django.views import View
from django.http import JsonResponse


class Endpoints(View):
    def get(self, request):
        response = {'code': 200, 'data': {}}
        return JsonResponse(response)  # Falso: array de JSON, True devolver un JSON


class GetByValue(View):
    @staticmethod
    def get(request, value):
        response = {'code': 200, 'data': value}
        return JsonResponse(response)  # Falso: array de JSON, True devolver un JSON

