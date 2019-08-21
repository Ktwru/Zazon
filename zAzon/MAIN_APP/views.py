from django.shortcuts import render

def main_page(request):
    return render(request, "main_page.html")


def TVs(request):
    return render(request, "boards/TVs.html")


def raccoons(request):
    return render(request, "boards/raccoons.html")


def magic(request):
    return render(request, "boards/magic.html")


def chill(request):
    return render(request, "boards/chill.html")