from django.shortcuts import render
from django.http import JsonResponse
import requests


# Create your views here.



import requests

def ping(request):
    return JsonResponse({'data': 'pong'})