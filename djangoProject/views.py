from django.shortcuts import render
from .models import Test
from .utils.county import sortCounty, readFile, clusterCounty

countyList = readFile()


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
        returnNumber = int(res['returnNumber'])
    attributes = []
    for k, v in res.items():
        if k != "returnNumber":
            attributes.append(v)
    print(returnNumber)

    topKCounties = sortCounty(countyList, returnNumber, *attributes)
    return render(request, "filter.html", {'counties': topKCounties})


def findSimilar(request):
    counties = dict()
    i = 0
    for county in countyList:
        counties[county.countyName] = i
        i += 1
    return render(request, "findSimilar.html", {'counties': counties})


def getSimilarResult(request):
    res = request.GET
    print(res)
    attributes = []
    returnNumber = 10  # default
    print(res)
    if res['returnNumber']:
        returnNumber = int(res['returnNumber'])
    for k, v in res.items():
        if k != "returnNumber" and k != "selectCounty":
            attributes.append(v)
    target = int(res['selectCounty'])
    res = clusterCounty(countyList, target, returnNumber, *attributes)
    print(res)
    resultDict = dict()
    for r in res:
        resultDict[r[0].countyName] = r[1]
        # resultDict.append([r[0].countyName])
    d = {'resultDict': resultDict, 'center': countyList[target].countyName}
    print(d)
    return render(request, "visualizeSimilar.html", d)


def search(request):
    counties = dict()
    i = 0
    for county in countyList:
        counties[county.countyName] = i
        i += 1
    return render(request, 'welcome.html', {'counties': counties})


def display(request):
    res = request.GET
    target = int(res['selectCounty'])
    county = countyList[target]
    return render(request, 'countyTemplate.html', {'county': county})
