# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from .models import Editor,Publication
import base64
import mymodule
import os
import subprocess



# Create your views here.
def index(request):
   return HttpResponse("there are no thing here")

# if upload was succeed
def success(request):
    return render(request,'upload/uploadStatus.html')

#*****************
# to upload a file
#*****************
def toUpload(request):

    # get current url
    current_path = request.path
    current_message_list = current_path.split('/')
    current_message = current_message_list[len(current_message_list)-2]
    current_state = current_message_list[len(current_message_list)-3]

    # get the information sended by method GET
    get_message = base64.decodestring(current_message)
    # The message is sended in form of: "editor"!"publicaiton title"
    message = get_message.split('!')
    # Get the name of editor
    Editor_current = message[0]
    # Get the name of publicaiton
    Publication_current = message[1]

    #*********************************************************
    # if this is a url to modif the Editor contatc information
    #*********************************************************

    if (current_state == u"modification"):
        # Find the object editor in the database
        Editor_modification = Editor.objects.get(Editor = Editor_current)
        context = {'Editor':Editor_modification,}
        # if this is a form submit, we save the information into the data base
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
        # if this is a Get method, we will return the page of modification
        return render(request,'upload/adminEditor.html',context)
    # if here is neither a modification, nor a upload, so url is not right
    if (current_state != u"upload"):
        return HttpResponse("Page not found")



    #********************************************************
    # if this is a page of upload
    #********************************************************

    # if we receive a method POST
    if request.method == 'POST':
        _POST = request.POST
        # CASE 1: this is a POST sended by resumable.js
        if "resumableChunkNumber" in _POST:
            Resumablefile= request.FILES.get('file')
            mymodule.handler_rs_POST(_POST, Resumablefile)
                    #shutil.rmtree(temp_dir)

        # CASE 2: this is a POST sended by form
        else:
            # Becasue we need to rename the file by also the name of the publication, so add the publication number
            path_final = mymodule.handler_no_POST(_POST,Publication_current.decode('utf-8'))
            try:
                file_test_size = float(os.path.getsize(path_final))
                file_name_final = path_final.split('/').pop()
                mesure = "octets"
                if file_test_size/1000 > 1:
                    file_test_size = file_test_size/1000
                    mesure = "Ko"
                    if file_test_size/1000>1:
                        file_test_size = file_test_size/1000
                        mesure = "Mo"
                        if file_test_size/1000>1:
                            file_test_size = file_test_size/1000
                            mesure = "Go"
                file_size_tmp = round(file_test_size,1)
                file_size_final = str(file_size_tmp) + mesure

                info={}
                command = "pdfinfo "+ path_final.replace(' ','\\ ')
                print command
                p = subprocess.Popen(command,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
                sout = p.stdout.readlines()
                serr = p.stderr.readlines()
                streamdata = p.communicate()[0]

                if p.returncode != 0:
                    print "exit code:",p.returncode
                    print serr
                    pdfCheck = "exit code:"+str(p.returncode)
                    error_list = serr
                    context = {'filename':file_name_final,'size':file_size_final,'pdfCheck':pdfCheck,'error_list':error_list}
                    os.remove(path_final)
                else:
                    pdfCheck = "ok"
                    context = {'filename':file_name_final,'size':file_size_final,'pdfCheck':pdfCheck}

                return render(request,'upload/uploadStatus.html',context)
            except:
                print "file not exist"
                return render(request,'upload/uploadStatus.html')

        return HttpResponse()

    # if we receive a method GET
    elif request.method == 'GET':
        _GET = request.GET
        print "a get"
        # if this is a GET sended by resumable.js
        if 'resumableChunkNumber' in _GET:
            if mymodule.handler_rs_GET(_GET) == True:
                return HttpResponse('chunk found',status=200)
            else:
                return HttpResponse('chunk not found', status=404)
        # if this is a GET normal
        elif 'filename_delete' in _GET:
            print "in the delete"
            mymodule.handler_delete_GET(_GET)
            return HttpResponse('delete finish',status=200)
        # if this is a GET ask to redirect to the page modification
        elif 'Editor' in _GET:
            #Editor_modif = _GET['Editor']
            return HttpResponseRedirect(reverse('upload:modification'))
        elif 'start_place' in _GET:
            if mymodule.handler_integration_GET(_GET):
                return HttpResponse('integration',status=200)
            else:
                return HttpResponse('integration fail',status=500)


    # get the Editor et Publication object
    Editor_input = Editor.objects.get( Editor = Editor_current)
    Publication_input = Publication.objects.get(PublicationTitle = Publication_current)


    # set the site
    context = {'Editor':Editor_input,'Publication':Publication_input}
    return render(request,'upload/index.html',context)

