# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from .models import Editor,Publication
import base64
import mymodule
import os


# Create your views here.
def index(request):

   return HttpResponse("there are no thing here")

def success(request):
    return HttpResponse("upload success!")

def toUpload(request):

    current_path = request.path
    current_message_list = current_path.split('/')
    current_message = current_message_list[len(current_message_list)-2]
    current_state = current_message_list[len(current_message_list)-3]

    get_message = base64.decodestring(current_message)
    message = get_message.split('!')
    Editor_current = message[0]
    Publication_current = message[1]

    if (current_state == u"modification"):
        print "in the modification"
        Editor_modification = Editor.objects.get(Editor = Editor_current)
        context = {'Editor':Editor_modification,}
        if request.method == 'POST':
            _POST = request.POST
            if "Email" in _POST:
                Editor_modification.Email = _POST['Email']
                Editor_modification.Title = _POST['Title']
                Editor_modification.Name = _POST['Name']
                Editor_modification.Surname = _POST['Surname']
                Editor_modification.InternationalPhoneNumber = _POST['InternationalPhoneNumber']
                Editor_modification.save()
                return HttpResponseRedirect(current_path.replace("/modification",""))


        return render(request,'upload/adminEditor.html',context)
    if (current_state != u"upload"):
        return HttpResponse("Page not found")

    if request.method == 'POST':
        _POST = request.POST
        # CASE 1
        if "resumableChunkNumber" in _POST:
            Resumablefile= request.FILES.get('file')
            mymodule.handler_rs_POST(_POST, Resumablefile)
        # CASE 2
        else:

            mymodule.handler_no_POST(_POST,Publication_current.decode('utf-8'))
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
        elif 'Editor' in _GET:
            print "Editor in the GET"
            #Editor_modif = _GET['Editor']
            return HttpResponseRedirect(reverse('upload:modification'))



    dictionary = {}
    if os.path.isfile("/tmp/resumable_images/configuration.txt"):
        f = file("/tmp/resumable_images/configuration.txt")
        while True:
            line = f.readline()
            if len(line) == 0:
                break
            print line,
            a = line.split('::')
            contrainte = a[1].replace('\n','').split('/')
            dictionary[a[0]]  = contrainte
            print dictionary
        f.close()

    Editor_input = Editor.objects.get( Editor = Editor_current)
    Publication_input = Publication.objects.get(PublicationTitle = Publication_current)

    configuration = dictionary[Publication_current]
    print configuration

    typeAsk = configuration[0]
    sizeMax = configuration[1]

    context = {'Editor':Editor_input,'Publication':Publication_input,'typeAsk':typeAsk,'sizeMax':sizeMax}
    return render(request,'upload/index.html',context)

