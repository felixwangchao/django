# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from .models import Editor,Publication
import base64
import mymodule


# Create your views here.
def index(request):

   return HttpResponse("there are no thing here")

def success(request):
    return HttpResponse("upload success!")

def toUpload(request):

    current_path = request.path
    current_message_list = current_path.split('/')
    current_message = current_message_list[len(current_message_list)-2]
    get_message = base64.decodestring(current_message)
    message = get_message.split('!')
    Editor_current = message[0]
    Publication_current = message[1]

    if request.method == 'POST':
        _POST = request.POST
        # CASE 1
        if "resumableChunkNumber" in _POST:
            Resumablefile= request.FILES.get('file')
            mymodule.handler_rs_POST(_POST, Resumablefile)
        # CASE 2
        else:
            mymodule.handler_no_POST(_POST)
            return HttpResponseRedirect(reverse('upload:success'))

        return HttpResponse()


    elif request.method == 'GET':
        _GET = request.GET
        print "****************MÉTHOD GET*********************"
        if 'resumableChunkNumber' in _GET:
            if mymodule.handler_rs_GET(_GET) == True:
                return 'ok'
            else:
                print "HTTP/1.0 404 Not Found"
                return HttpResponse('chunk not found', status=404)
        elif 'filename_delete' in _GET:
            mymodule.handler_delete_GET(_GET)
            return HttpResponse('delete finish',status=200)


    Editor_input = Editor.objects.get( Editor = Editor_current)
    Publication_input = Publication.objects.get(PublicationTitle = Publication_current)
    print Editor_input
    print Publication_input

    context = {'Editor':Editor_input,'Publication':Publication_input}
    return render(request,'upload/index.html',context)

