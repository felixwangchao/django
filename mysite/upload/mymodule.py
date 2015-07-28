# -*- coding: utf-8 -*-
# Auteur: Chao
# Filename: mymodule.py

import os,os.path
import sys
import logging
import time
import shutil
from ctypes import *


# extention: only the file who's extension is in this set "extention" can be identified
# eg:        LeMonde.pdf ----> LeMonde_07_07_2015.pdf       LeMonde.txt ----> LeMonde.txt_07_07_2015
extension = set(['pdf',])
# temp_base: we will store the file uploaded in this directory
temp_base = '/tmp/resumable_images/'
# CurrentFile: store the name of the file we have already uploaded
CurrentFile = []



# handler: for trait the GET from resumable.js
def handler_rs_GET(_GET): 
    '''This function is used to deal with the GET sended by resumable.js

        _GET = cgi.parse_qs(environ['QUERY_STRING'])'''
    # create a tempory directory
    temp_dir = "{}{}".format(temp_base, _GET['resumableIdentifier'])
    # create a path for the chunk
    resumableFilename = (_GET['resumableFilename']).encode('utf-8')
    chunk_file = "{}/{}.part{}".format(temp_dir, resumableFilename,  _GET['resumableChunkNumber'])
    # if this directory has already been created, it means that this chunk has already been sended

    if not os.path.isfile(chunk_file):
        return False
    else:
        return True

# handler: for delete a file
def handler_delete_GET(_GET):
    deleteFileName =  (_GET['filename_delete']).encode('utf-8')
    delete_file_path = os.path.join(temp_base,deleteFileName)
    delete_dir_path = os.path.join(temp_base,_GET['filename_delete_uniqueIdentifier'])
    if os.path.isfile(delete_file_path):
        print "file exist"
        os.remove(delete_file_path)
    if os.path.isdir(delete_dir_path):
        shutil.rmtree(delete_dir_path)


def handler_integration_GET(_GET):
    try:
        temp_dir = "{}{}".format(temp_base, _GET['resumableIdentifier'])
        resumableFilename = (_GET['resumableFilename']).encode('utf-8')
        target_file_name = "{}{}".format(temp_base,resumableFilename)
        stored_chunk_file_name = "{}{}/{}.part".format(temp_base,_GET['resumableIdentifier'], resumableFilename)
        start_place = int(_GET['start_place'])
        end_place = int(_GET['end_place'])
        libtest = cdll.LoadLibrary(os.getcwd() + '/upload/libtest.so')
        libtest.collectFile(stored_chunk_file_name,target_file_name,start_place,end_place)
        if "lastFile" in _GET:
            shutil.rmtree(temp_dir)
            CurrentFile.append(target_file_name)
        return True
    except:
        return False



# handler: for trait the POST from resumable.js
def handler_rs_POST(_POST,Resumablefile):
    ''' This function is used to deal with the POST sended by resumable.js

        the _POST = _POST = cgi.FieldStorage(...) '''

    temp_dir = "{}{}".format(temp_base, _POST['resumableIdentifier'])
    resumableFilename = (_POST['resumableFilename']).encode('utf-8')
    chunk_file = "{}/{}.part{}".format(temp_dir, resumableFilename, _POST['resumableChunkNumber'])
    file_path = chunk_file
    fileitem = Resumablefile


    # If the path not exist, create a new one
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)

    if int(_POST['resumableCurrentChunkSize']) > (int(_POST['resumableChunkSize'])):
        time.sleep(2)
        pass


    # Save the file in the tempory directory
    counter = 0
    # Write on binary



    with open(file_path, 'wb') as output_file:
        while 1:
            data = fileitem.file.read(1024)
            if not data:
                break
            output_file.write(data)
            counter += 1
            if counter == 100:
                counter = 0


    collect(_POST)




#$  total_files * $chunkSize >=  ($totalSize - $chunkSize + 1)
def collect(_POST):
    ''' This function is used to collect all the small chunk and write them in a new file

        the _POST = _POST = cgi.FieldStorage(...) '''
    # Because the last chunk is bigge   r than a normal chunk
    temp_dir = "{}{}".format(temp_base, _POST['resumableIdentifier'])
    resumableFilename = (_POST['resumableFilename']).encode('utf-8')

    total_file = len([name for name in os.listdir(temp_dir) if os.path.isfile(os.path.join(temp_dir, name))])

    currentSize =  total_file * (int(_POST['resumableChunkSize']))
    filesize = int(_POST['resumableTotalSize'])
    # $total_files * $chunkSize >=  ($totalSize - $chunkSize + 1)
    # if all the chunks were been received, collect all the chunk and delete all the tempory directory
    #if currentSize >= (filesize-int(_POST['resumableChunkSize'])+1):
        #pass


# handler for trait the POST from form
def handler_no_POST(_POST,Publication_current):
    ''' This function is used to deal with a normal request POST submit from "form"

        the _POST = _POST = cgi.FieldStorage(...) ''' 
    # Get the date from the form
    Date_p = _POST["date_p"]
    Date_f_p = _POST["date_f_p"]
    Pub_number = _POST["pub_number"]
    
    # update all the path into the CurrentFile
    
    # Open every path and rename the file    

    print "new try"
    file_real = CurrentFile.pop()

    if not os.path.isfile(file_real):
        return False
    else:
        path_final = rename_file(file_real, Date_p,Date_f_p,Pub_number,Publication_current)
        return path_final



def rename_file(file_real, Date_p,Date_f_p,Pub_number,Publication_current):
    '''This function is used to rename a file with his path and the publication date

       file_real is his path, Date publication is the date'''

    file_name_old = os.path.basename(file_real)
    List = file_name_old.split('.')

    Date_p_tmp_1 = Date_p.split('/')
    Date_p_tmp_1.reverse()
    Date_p_tmp = "".join(Date_p_tmp_1)

    Date_f_p_tmp_1 = Date_f_p.split('/')
    Date_f_p_tmp_1.reverse()
    Date_f_p_tmp = "".join(Date_f_p_tmp_1)

    #Date_f_p_tmp = "_".join((Date_f_p.split('/')).reverse())
    logging.warning('WARNING! extention probleme '+List[len(List)-1])
    if len(List) > 1 and (List[len(List)-1] == 'pdf'):
        filename_tmp = ".".join(List[0:len(List)-1])
        file_name_final = Publication_current +'_'+ Date_p_tmp + '_'+Date_f_p_tmp+'_'+Pub_number+ '.' + List[len(List)-1]
        path_old = os.path.join(temp_base,file_name_old.decode('utf-8'))
        path_final = os.path.join(temp_base,file_name_final)
        os.rename(path_old.encode('utf-8'),path_final.encode('utf-8'))
        return path_final
    else:
        file_name_final = Publication_current + '_'+Date_p_tmp+'_'+Date_f_p_tmp+'_'+Pub_number
        path_old = os.path.join(temp_base,file_name_old.decode('utf-8'))
        path_final = os.path.join(temp_base,file_name_final)
        os.rename(path_old.encode('utf-8'),path_final.encode('utf-8'))
        return path_final
