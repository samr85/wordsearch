from django.shortcuts import render
from django.http import HttpResponse, QueryDict
from django.views.decorators.csrf import csrf_exempt

import solver

# Create your views here.
def index(request):
    return HttpResponse("hello1")

def detail(request, id):
    return HttpResponse("id: %s"%(id))

def gridInput(request, errorClass: solver.badInput = None):
    context = {"dictionaries": solver.wordLists.values()}
    if errorClass:
        context["error"] = errorClass.reason
    return render(request, "solverGui/input.html", context)


dummyArray = "\r\n".join(
           ['despoticskeetshoot',
            'teacupozglommedorr',
            'ieginbracingsailrs',
            'coexinyortezorabll',
            'windstifledowngate',
            'napleshmaayugnolan',
            'gnoowysumachfoxery',
            'boinksgrouceneider',
            'isfloplinxitsokerz',
            'expliscovarquodern'])


@csrf_exempt
def gridDisplay(request):
    post: QueryDict = request.POST.copy()
    if "gridContents" not in post:
        return gridInput(request)

    try:
        print(request.POST)
        arrayIn = post.get("gridContents")
        del post["gridContents"]
        arrayIn = arrayIn.splitlines(keepends=False)

        displayGrid = []
        workGrid = []
        for line in arrayIn:
            displayGrid.append(line.upper())
            workGrid.append(line.lower())
        matches = solver.parseGridSettings(workGrid, post)
        context = {"grid": displayGrid,
                   "wordList": matches}
        return render(request, "solverGui/display.html", context)
    except solver.badInput as e:
        return gridInput(request, e)

