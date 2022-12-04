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
    attrs = res.getlist("interest8")

    topKCounties = sortCounty(countyList, returnNumber, *attrs)
    return render(request, "filter.html", {'counties': topKCounties})


def findSimilar(request):
    counties = dict()
    i = 0
    for county in countyList:
        counties[county.countyName] = i
        i += 1
    return render(request, "findSimilar.html", {'counties': counties})


def format(str: str):
    new_str = ""
    for i in range(len(str)):
        if "A" <= str[i] <= "Z":
            new_str += " "
        new_str += str[i]
    return new_str


def getSimilarResult(request):
    res = request.GET
    print(res)
    attributes = []
    returnNumber = 10  # default
    print(res)
    attrs = res.getlist("interest8")
    print(attrs)
    displayAttrs = attrs[-1]
    if len(attrs) > 1:
        displayAttrs = ", ".join(attrs[:-1]) + " and " + displayAttrs
    displayAttrs = format(displayAttrs)
    print(displayAttrs)
    if res['returnNumber']:
        returnNumber = int(res['returnNumber'])
    target = int(res['selectCounty'])

    res = clusterCounty(countyList, target, returnNumber, *attrs)
    # print(res)
    resultDict = dict()
    for r in res:
        resultDict[r[0]] = r[1]
        # resultDict.append([r[0].countyName])
    d = {'resultDict': resultDict, 'center': countyList[target],
         "attributes": displayAttrs.title().replace("And", "and")}
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
