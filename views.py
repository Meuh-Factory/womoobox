from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from womoobox.forms import GetMooForm
from django.http import HttpResponse


# Create your views here.
def get_map(request):
    return render(request, 'map.html', {})


# Simple form to test the Moo getting process
@csrf_exempt # no csrf check in forms
def moo_get_form(request):
    f = GetMooForm()
    return render(request, 'get_moo_form.html', {'form': f.as_table()})
