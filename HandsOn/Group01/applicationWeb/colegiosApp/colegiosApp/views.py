from django.shortcuts import render
# Create your views here.

from django.http import HttpResponse
from django.template.response import TemplateResponse


def index(request):
    return render(request, "index.html")


def municipios(request):
    return render(request, "municipios.html")


def colegios(request):
    if request.method == "POST":
        if request.POST["action"] == "1":
            colegio = request.POST["nombreColegio"]
            print("Nombre colegio:", colegio)
            #buscar datos nombre de colegio con sparql
            aux = ['colegio 1', 'colegio 2', 'colegio 3']
            return render(request, "colegios.html", {'colList': aux})
        else:
            print("Form buscar colegio")

    numeroPrueba = "11"
    return render(request, "colegios.html", {'numeroPrueba': numeroPrueba})
