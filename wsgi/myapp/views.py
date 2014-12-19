from django.shortcuts import render, render_to_response, get_object_or_404
from django.http import HttpResponse
from django.template import RequestContext
from django.views.generic import View

class Index(View):
    def get(self,request):
        context = RequestContext(request)
        return render_to_response('myapp/index.html', context)
    
    
