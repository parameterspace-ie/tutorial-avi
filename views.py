from django.shortcuts import render
from avi.models import TutorialModel

def index(request):
    context = {
        "name": "John Smith"
    }
    return render(request, 'avi/index.html', context)

def create(request, fib):
    tutmod, created = TutorialModel.objects.get_or_create(
        fib_num=fib
    )
    context = {
        "tutmod": tutmod,
        "fib": fib
    }
    return render(request, 'avi/create.html', context)