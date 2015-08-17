# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from .models import Editor,Publication,Contact
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from pdf_validator import PdfValidator
from random import randint
import base64
import mymodule
import os
import subprocess
from sendMail import notification

email = ""
code = 0


#**************************************************************************************
# The page for authenticate
#**************************************************************************************

def my_view(request):
    yellowPages = {'wangchao@eisti.fr':'Le Monde'}
    if request.method == 'POST':
        if not request.POST.get('rememberMe'):
            print "Not remember me"
            request.session.set_expiry(0)
        email = request.POST['username']
        password = request.POST['password']
        username = yellowPages[email]

        user = authenticate(username=username,password=password)
        print "authenticate"
        if user is not None:
            if user.is_active:
                login(request,user)
                #Editor_current = yellowPages[username]
                return HttpResponseRedirect('/upload/Editor/tab-account/'+username)
            else:
                print "user is disabled"

        else:
            print "Log in failed"

    return render(request,'upload/login.html')

def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/upload/login/')


def forget_password(request):
    user = User.objects.get(id = 1)
    email =""
    code = 0
    if request.method == 'GET':
        _GET = request.GET
        if 'email' in _GET:
            email = _GET['email']
            print "email in the get is:",email
            user = User.objects.get(email = email)
            if user is not None:
                code = randint(1000,9999)
                notification(code,email)
                return HttpResponse(str(code),status=200)
            else:
                print "user not found"

    elif request.method == 'POST':
        _POST = request.POST
        print "in a post method"
        if 'email' in _POST:
            print "there is a email"
            context = {'email':request.POST['email']}
            return render(request,'upload/changePassword.html',context)

        if 'newpass' in _POST:
            email = _POST['emailFix']
            user = User.objects.get(email = email)
            user.set_password( str(_POST['newpass']))
            user.save()
            print "save success"
            return HttpResponseRedirect('/upload/login/')

    return render(request,'upload/Forget.html')

#****************************************************************************************
# The page for user
#****************************************************************************************


def tab_account_change(request):
    current_path = request.path
    current_message_list = current_path.split('/')
    Editor_current = current_message_list[len(current_message_list)-2]
    if not (request.user.username == Editor_current):
        return HttpResponseRedirect('/upload/login')
    id_current = current_message_list[len(current_message_list)-3]
    Contact_input = Contact.objects.get(id = id_current)


    if request.method == 'POST':
        _POST = request.POST
        Contact_input.Email = _POST['Email']
        Contact_input.Title = _POST['Title']
        Contact_input.Name = _POST['Name']
        Contact_input.Surname = _POST['Surname']
        Contact_input.Type = _POST['Type']
        Contact_input.Language = _POST['Language']
        Contact_input.InternationalFixPhoneNumber = _POST['InternationalFixPhoneNumber']
        Contact_input.InternationalMobilePhoneNumber = _POST['InternationalMobilePhoneNumber']
        Contact_input.save()
        return HttpResponseRedirect('/upload/Editor/tab-account-contact/'+Editor_current)
    context = {'Contact':Contact_input}
    return render(request,'upload/tab-account-change.html',context)

def tab_publication_change(request):
    current_path = request.path
    current_message_list = current_path.split('/')
    Editor_current = current_message_list[len(current_message_list)-2]
    if not (request.user.username == Editor_current):
        return HttpResponseRedirect('/upload/login')
    id_current = current_message_list[len(current_message_list)-3]
    Editor_input = Editor.objects.get( Editor = Editor_current)
    Publication_input = Publication.objects.get(id = id_current)

    if request.method == 'POST':
        _POST = request.POST
        Publication_input.PublicationTitle = _POST['PublicationTitle']
        Publication_input.Periodicity = _POST['Periodicity']
        print _POST['Periodicity']
        Publication_input.PublicationDay = _POST['PublicationDay']
        Publication_input.Language = _POST['Language']
        print _POST['Language']
        Publication_input.Website = _POST['Website']
        Publication_input.TypeAsk = "pdf"
        if _POST['Periodicity'] == "Daily":
            Publication_input.SizeMax = 20000000
        else:
            Publication_input.SizeMax = 250000000
        Publication_input.save()
        return HttpResponseRedirect('/upload/Editor/tab-publication/'+Editor_current)

    context = {'Publication':Publication_input}
    return render(request,'upload/tab-publication-change.html',context)

def tab_publication(request):
    current_path = request.path
    current_message_list = current_path.split('/')
    Editor_current = current_message_list[len(current_message_list)-2]
    if not (request.user.username == Editor_current):
        return HttpResponseRedirect('/upload/login')
    Editor_input = Editor.objects.get( Editor = Editor_current)
    Publication_input = Publication.objects.filter(editor = Editor_input)

    if request.method == 'GET':
        _GET = request.GET
        print "in a get"
        if 'Pub_id' in _GET:
            print "in a delete"
            delete_id = _GET['Pub_id']
            print delete_id
            e = Publication.objects.get(id = delete_id)
            e.delete()
            return HttpResponse('delete success',status=200)

    context = {'Editor':Editor_input,'Publication':Publication_input}
    return render(request,'upload/tab-publication.html',context)

def tab_publication_add(request):
    current_path = request.path
    current_message_list = current_path.split('/')
    Editor_current = current_message_list[len(current_message_list)-2]
    if not (request.user.username == Editor_current):
        return HttpResponseRedirect('/upload/login')
    Editor_input = Editor.objects.get( Editor = Editor_current)


    if request.method == 'POST':
        _POST = request.POST
        Publication_input = Publication(editor = Editor_input)
        Publication_input.PublicationTitle = _POST['PublicationTitle']
        Publication_input.Periodicity = _POST['Periodicity']
        Publication_input.PublicationDay = _POST['PublicationDay']
        Publication_input.Language = _POST['Language']
        print _POST['Language']
        Publication_input.Website = _POST['Website']
        Publication_input.typeAsk = "pdf"
        print "after set the TypeAsk"
        print
        if _POST['Periodicity'] == "Daily":
            Publication_input.sizeMax = "20000000"
        else:
            Publication_input.sizeMax = "250000000"
        Publication_input.save()
        return HttpResponseRedirect('/upload/Editor/tab-publication/'+Editor_current)

    return render(request,'upload/tab-publication-add.html')

def tab_account_contact(request):
    current_path = request.path
    current_message_list = current_path.split('/')
    Editor_current = current_message_list[len(current_message_list)-2]
    if not (request.user.username == Editor_current):
        return HttpResponseRedirect('/upload/login')
    Editor_input = Editor.objects.get( Editor = Editor_current)
    Contact_input = Contact.objects.filter(editor = Editor_input)
    if request.method == 'GET':
        _GET = request.GET
        print "in a get"
        if 'Contact_id' in _GET:
            print "in a delete"
            delete_id = _GET['Contact_id']
            print delete_id
            e = Contact.objects.get(id = delete_id)
            e.delete()
            return HttpResponse('delete success',status=200)
    context = {'Editor':Editor_input,'Contact':Contact_input}
    return render(request,'upload/tab-account-contact.html',context)

def tab_account_add(request):
    current_path = request.path
    current_message_list = current_path.split('/')
    Editor_current = current_message_list[len(current_message_list)-2]
    if not (request.user.username == Editor_current):
        return HttpResponseRedirect('/upload/login')
    Editor_input = Editor.objects.get( Editor = Editor_current)


    if request.method == 'POST':
        _POST = request.POST
        contact = Contact(editor = Editor_input)
        contact.Title = _POST['Title']
        contact.Name = _POST['Name']
        contact.Surname = _POST['Surname']
        contact.Type = _POST['Type']
        contact.Language = _POST['Language']
        contact.Email = _POST['Email']
        contact.InternationalFixPhoneNumber = _POST['InternationalFixPhoneNumber']
        contact.InternationalMobilePhoneNumber = _POST['InternationalMobilePhoneNumber']
        contact.save()
        return HttpResponseRedirect('/upload/Editor/tab-account-contact/'+Editor_current)
    return render(request,'upload/tab-account-add.html')

def tab_account(request):
    current_path = request.path
    current_message_list = current_path.split('/')
    Editor_current = current_message_list[len(current_message_list)-2]

    if not (request.user.username == Editor_current):
        return HttpResponseRedirect('/upload/login')

    Editor_input = Editor.objects.get( Editor = Editor_current)
    context = {'Editor':Editor_input}
    return render(request,'upload/tab-account.html',context)

def tab_account_general(request):
    current_path = request.path
    current_message_list = current_path.split('/')
    Editor_current = current_message_list[len(current_message_list)-2]

    if not (request.user.username == Editor_current):
        return HttpResponseRedirect('/upload/login')

    Editor_input = Editor.objects.get( Editor = Editor_current)
    context = {'Editor':Editor_input}
    return render(request,'upload/tab-account-general.html',context)

def tab_account_general_change(request):
    current_path = request.path
    current_message_list = current_path.split('/')
    Editor_current = current_message_list[len(current_message_list)-2]
    if not (request.user.username == Editor_current):
        return HttpResponseRedirect('/upload/login')
    Editor_input = Editor.objects.get( Editor = Editor_current)
    if request.method == 'POST':
        _POST = request.POST
        Editor_input.Name = _POST['Name']
        Editor_input.Website = _POST['Website']
        Editor_input.Address = _POST['Address']
        Editor_input.Zipcode = _POST['Zipcode']
        Editor_input.Country = _POST['Country']
        Editor_input.Language = _POST['Language']
        Editor_input.PhoneNumber = _POST['PhoneNumber']
        Editor_input.save()
        return HttpResponseRedirect('/upload/Editor/tab-account/'+Editor_current)


    context = {'Editor':Editor_input}
    return render(request,'upload/tab-account-general-change.html',context)



#****************************************************************************************
# New page end
#****************************************************************************************

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
                    parameters = {'pdf_validation_tests':'test.zip'}
                    issue_context = {'parameters':parameters,'working_directory':'/tmp/resumable_images/'}
                    a = PdfValidator(issue_context)
                    pdfCheck = "ok"

                    pdfStatus = a.get_pdfinfo_data(path_final)
                    pdfExplore = a.get_explode_dump()
                    pdfPortrait = a.check_portrait()
                    pdfDict = {'pdfStatus':pdfStatus,'pdfExplore':pdfExplore,'pdfPortrait':pdfPortrait}

                    context = {'filename':file_name_final,'size':file_size_final,'pdfCheck':pdfCheck,'pdfDict':pdfDict}

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
    print "before Contact"
    try:
        Contact_input = Contact.objects.get(Type = "Technical",editor = Editor_input)
        context = {'Editor':Editor_input,'Publication':Publication_input,'Contact':Contact_input}
    except:
        context = {'Editor':Editor_input,'Publication':Publication_input}

    return render(request,'upload/index.html',context)

