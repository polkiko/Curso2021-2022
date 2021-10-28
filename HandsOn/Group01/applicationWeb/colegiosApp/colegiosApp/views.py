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
    nColegios = colegioAux.numColegios()
    if request.method == "POST":
        if request.POST["action"] == "1":
            colegio = request.POST["nombreColegio"]
            nameColegios = colegioAux.nombreColegio(colegio)
            return render(request, "colegios.html", {'colList': nameColegios, 'nColegios': nColegios})
        else:
            print("Form buscar colegio")

    return render(request, "colegios.html", {'nColegios': nColegios})
