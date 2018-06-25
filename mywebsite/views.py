from django.shortcuts import render


def index(request):
    """ website index """
    return render(request, 'index.html')