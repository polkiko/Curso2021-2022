from django.shortcuts import render


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
        elif request.POST["action"] == "2":
            # tipoCentro = request.POST["tipoCentro"]
            # print(tipoCentro)
            municipio = request.POST["municipioC"]
            cp = request.POST["codigoP"]
            tipoCentro = request.POST["tipoCentro"]
            titCentro = request.POST["titCentro"]

            print(tipoCentro, titCentro, municipio, cp)
            nameColegios = []
            return render(request, "colegios.html", {'colList2': nameColegios, 'nColegios': nColegios})
    return render(request, "colegios.html", {'nColegios': nColegios})
