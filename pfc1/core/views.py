from django.shortcuts import render


def pacman_view(request):
    if request.method == 'GET':
        return render(request, 'pacman.html')
