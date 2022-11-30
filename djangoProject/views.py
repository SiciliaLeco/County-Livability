from django.shortcuts import render
from .models import Test


def runoob(request):
    # showCounties = [County(1, "County1", "0.1", "100"), County(2, "County2", "0.2", "200")]
    # county = Test()
    # county.id = 2
    # county.name = "County2"
    # county.GDP = 100
    # county.save()
    return render(request, 'project.html', {'showCounties': Test.objects.get(id=2)})
