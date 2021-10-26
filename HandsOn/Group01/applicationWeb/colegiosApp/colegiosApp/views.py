from django.shortcuts import render
# Create your views here.

from django.http import HttpResponse


def index(request):
    return render(request, "index.html")


def municipios(request):
    return render(request, "municipios.html")


def colegios(request):
    return render(request, "colegios.html")
