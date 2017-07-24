#coding=utf-8
from __future__ import print_function
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.template import loader
from django.http import Http404
from django.views.decorators.csrf import csrf_exempt
from django.utils.encoding import smart_str
from video_process import sound_parse

import grpc
import movsearch_pb2
import movsearch_pb2_grpc
import sqlite3
#import cv2
import video_process
@csrf_exempt
# Create your views here.

def index(request):
    template = loader.get_template('index.html')
    return HttpResponse(template.render({},request))

def soundsearch(request):
    rq=request.POST
    fl=request.FILES
    query_file=fl.get('sound_query','$0')
    fname=query_file.name
    tfname='temp.wav'
    f=open(tfname,'wb')
    for line in query_file.chunks():
        f.write(line)
    f.close()
    sound_parse(tfname)
    f=open('temp.fft3','rb')
    s=f.read()
    f.close()
    n=1
    n=len(s)
    #print(n)
    channel=grpc.insecure_channel('101.5.209.114:50051')
    stub=movsearch_pb2_grpc.SearchSoundStub(channel)
    response=stub.search(movsearch_pb2.Query(filename=fname,data=s,num=n))
    res_num=response.num
    filename_list=response.reslist.split("@@")
    filename_list.pop()
    print(filename_list)
    res="<html>sucess</html>"
    response=HttpResponse(res)
    return response
    

def upload(request):
    rq=request.POST
    fl=request.FILES
    query_file=fl.get('query','$0')
    #print(query_file)
    #print(query_file.name)
    s=b''
    for line in query_file.chunks():
        s+=line
    name=query_file.name
    n=1
    n=len(s)
    channel=grpc.insecure_channel('silicon.grep.top:2333')
    stub=movsearch_pb2_grpc.SearchMovieStub(channel)
    response=stub.search(movsearch_pb2.Query(filename=name,data=s,num=n))
    res_num=response.num
    filename_list=response.reslist.split("@@")
    filename_list.pop()
    i=0
    for i in range(len(filename_list)):
        filename_list[i]=filename_list[i].replace('./thumbnail/','')
        filename_list[i]=filename_list[i].replace('.png','.mp4')
    rlist=list([])
    for i in range(res_num):
        mode=0
        if mode>0:
            fileurl="//main//static//video//"+filename_list[i]
            video=cv2.VideoCapture(fileurl)
            fps=video.get(cv2.CAP_PROP_FPS)
            length=int(video.get(cv2.CAP_PROP_FRAME_COUNT))
            ctlength=int(length/4)
            for j in range(ctlength):
                (success,frame)=video.read()
            (success,frame)=video.read()     
            filesnap=frame
        fileurl="/static/video/"
        fileurl+=filename_list[i]
        fileurl+=""
        tempsnap="FAKE_SNAP"
        retuple={'filename':filename_list[i],'fileurl':fileurl,'filesnap':tempsnap}
        rlist.append(retuple)
    template=loader.get_template('result.html')
    print(res_num)
    print(rlist[0:5])
    res_num=0
    rlist=list([])
    response=HttpResponse(template.render({'res_count':str(res_num), 'reslist':rlist},request))
    return response


