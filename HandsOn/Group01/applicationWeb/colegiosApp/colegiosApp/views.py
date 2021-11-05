from .querysSparql import Colegios
from django.shortcuts import render
from json import dumps


def index(request):
    return render(request, "index.html")


def municipios(request):
    return render(request, "municipios.html")


def colegios(request):
    colegioAux = Colegios()
    if request.method == "POST":
        if request.POST["action"] == "1":  # Búsqueda sólo por nombre de colegio
            colegio = request.POST["nombreColegio"]
            nameColegios = colegioAux.nombreColegio(colegio.upper())
            return render(request, "colegios.html",
                          {'nColegios': len(nameColegios), 'colList': nameColegios, 'jsonList': dumps(nameColegios),
                           'action': 1})
        elif request.POST["action"] == "2":  # Búsqueda avanzada de colegios
            municipio = request.POST["municipioC"]
            cp = request.POST["codigoP"]
            tipoCentro = request.POST["tipoCentro"]
            titCentro = request.POST["titCentro"]
            limite = request.POST["limiteColegio2"]
            nameColegios = colegioAux.nombreColAvanzada(tipoCentro, titCentro, municipio, cp, limite)
            return render(request, "colegios.html",
                          {'colList2': nameColegios, 'nColegios': len(nameColegios), 'jsonList': dumps(nameColegios),
                           'action': 2})
    return render(request, "colegios.html", {'nColegios': 0})
