from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.template import loader
from django.shortcuts import render_to_response
from django.http import Http404
from django.views.decorators.csrf import csrf_exempt
@csrf_exempt

def index(request):
    return HttpResponse('<script>window.location="main"</script>')
