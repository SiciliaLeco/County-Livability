from django.shortcuts import render
from .models import Test
from .utils.county import sortCounty, readFile


def runoob(request):
    # showCounties = [County(1, "County1", "0.1", "100"), County(2, "County2", "0.2", "200")]
    # county = Test()
    # county.id = 2
    # county.name = "County2"
    # county.GDP = 100
    # county.save()
    return render(request, 'test.html', {'showCounties': Test.objects.get(id=2)})


def filter(request):
    return render(request, "filter.html")


def getSortedResult(request):
    res = request.GET
    returnNumber = 10  # default
    print(res)
    if res['returnNumber']:
        returnNumber = res['returnNumber']
    attributes = []
    for k, v in res.items():
        if k != "returnNumber":
            attributes.append(v)
    print(returnNumber)
    countyList = readFile()
    topKcounties = sortCounty(countyList, returnNumber, *attributes)
    return render(request, "filter.html", {'counties':topKcounties})
