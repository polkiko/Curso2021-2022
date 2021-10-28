from django.shortcuts import render
# Create your views here.

from django.http import HttpResponse


def index(request):
    return render(request, "index.html")


def municipios(request):
    return render(request, "municipios.html")


def colegios(request):
    if request.method == "POST":
        print("Estoy en POST")
        if request.POST["action"] == "1":
            print("Form nombre")
            print("Nombre colegio:", request.POST["nombreColegio"])
        else:
            print("Form buscar colegio")
    return render(request, "colegios.html")
