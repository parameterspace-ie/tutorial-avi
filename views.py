from django.shortcuts import render

def index(request):
    context = {
        "name": "John Smith"
    }
    return render(request, 'avi/index.html', context)