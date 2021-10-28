from django.shortcuts import render
# Create your views here.

from django.http import HttpResponse
from django.template.response import TemplateResponse


def index(request):
    return render(request, "index.html")


def municipios(request):
    return render(request, "municipios.html")


def colegios(request):
    from .querysSparql import Colegios
    colegioAux = Colegios()
    if request.method == "POST":
        if request.POST["action"] == "1":
            colegio = request.POST["nombreColegio"]
            print("Nombre colegio:", colegio)
            nameColegios = colegioAux.nombreColegio(colegio)
            return render(request, "colegios.html", {'colList': nameColegios})
        else:
            print("Form buscar colegio")

    nColegios = colegioAux.numColegios()
    return render(request, "colegios.html", {'nColegios': nColegios})
