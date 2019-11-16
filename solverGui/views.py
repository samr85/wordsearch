from django.shortcuts import render
from django.http import HttpResponse

import solver

# Create your views here.
def index(request):
    return HttpResponse("hello1")

def detail(request, id):
    return HttpResponse("id: %s"%(id))

def gridInput(request):
    context = {}
    return render(request, "solverGui/input.html", context)

def gridDisplay(request):
    arrayIn =['despoticskeetshoot',
            'teacupozglommedorr',
            'ieginbracingsailrs',
            'coexinyortezorabll',
            'windstifledowngate',
            'napleshmaayugnolan',
            'gnoowysumachfoxery',
            'boinksgrouceneider',
            'isfloplinxitsokerz',
            'expliscovarquodern']

    displayGrid = []
    workGrid = []
    for line in arrayIn:
        displayGrid.append(line.upper())
        workGrid.append(line.lower())
    context = {"grid": displayGrid,
               "wordList": solver.getGridMatches(workGrid)}
    return render(request, "solverGui/display.html", context)
