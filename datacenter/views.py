from django.shortcuts import render
from django.http import HttpResponse
from datacenter.models import Department

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


def show_departments(request):
    return render(request, "departments.html", {'departments': Department.objects.all()})
