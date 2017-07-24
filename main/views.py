#coding=utf-8
from __future__ import print_function
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.template import loader
from django.http import Http404
from django.views.decorators.csrf import csrf_exempt
from django.utils.encoding import smart_str
from video_process import sound_parse
from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger
import grpc
import movsearch_pb2
import movsearch_pb2_grpc
import sqlite3
import hashlib
import random
import json
#import cv2
import video_process
@csrf_exempt
# Create your views here.

def index(request):
    template = loader.get_template('index.html')
    return HttpResponse(template.render({},request))

def soundsearch(request):
    page=1
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
    hashk=str(hashlib.sha1(s).hexdigest())
    hashk+=str(random.randint(5000000,9999999))
    db=sqlite3.connect("database")
    cu=db.cursor()
    #print(n)
    channel=grpc.insecure_channel('183.172.193.106:50051')
    stub=movsearch_pb2_grpc.SearchSoundStub(channel)
    response=stub.search(movsearch_pb2.Query(filename=fname,data=s,num=n))
    res_num=response.num
    db=sqlite3.connect("database")
    cu=db.cursor()
    cu.execute('''insert into query(hashkey,result,num,dtype) values("'''+hashk+'''","'''+response.reslist+'''",'''+str(res_num)+''','''+str(1)+''');''')
    db.commit()
    filename_list=response.reslist.split("@@")
    filename_list.pop()
    filename_list=filename_list[(page-1)*5:]
    if len(filename_list)>5:
        filename_list=filename_list[:5]
    i=0
    for i in range(len(filename_list)):
        filename_temp=filename_list[i].split("/")
        filename_temp=filename_temp[-2]+"/"+filename_temp[-1]
        filename_list[i]=filename_temp.replace('.fft3','.mp4')
    rlist=list([])
    for i in range(len(filename_list)):
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
    response=HttpResponse(template.render({'page':str(page),'res_count':str(res_num), 'res_duplicate':'0','reslist':rlist},request))
    response.set_cookie("query_hash",hashk,3600)
    #print(filename_list)
    #res="<html>sucess</html>"
    #response=HttpResponse(res)
    return response
    

def upload(request):
    #"create table query( hashkey char(200) not null, result text not null, num int, dtype int);"
    rq=request.POST
    fl=request.FILES
    query_file=fl.get('query','$0')
    page=int(rq.get('page','$1'))
    #print(query_file)
    #print(query_file.name)
    s=b''
    for line in query_file.chunks():
        s+=line
    hashk=str(hashlib.sha1(s).hexdigest())
    hashk+=str(random.randint(1000000,4999999))
    db=sqlite3.connect("database")
    cu=db.cursor()
    name=query_file.name
    n=1
    n=len(s)
    channel=grpc.insecure_channel('silicon.grep.top:2333')
    stub=movsearch_pb2_grpc.SearchMovieStub(channel)
    response=stub.search(movsearch_pb2.Query(filename=name,data=s,num=n))
    res_num=response.num
    db=sqlite3.connect("database")
    cu=db.cursor()
    cu.execute('''insert into query(hashkey,result,num,dtype) values("'''+hashk+'''","'''+response.reslist+'''",'''+str(res_num)+''','''+str(0)+''');''')
    db.commit()
    filename_list=response.reslist.split("@@")
    filename_list.pop()
    filename_list=filename_list[(page-1)*5:]
    if len(filename_list)>5:
        filename_list=filename_list[:5]
    i=0
    for i in range(len(filename_list)):
        filename_list[i]=filename_list[i].replace('./thumbnail/','')
        filename_list[i]=filename_list[i].replace('.png','.mp4')
    rlist=list([])
    for i in range(len(filename_list)):
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
    #print(res_num)
    #print(rlist[0:5])
    #res_num=0
    #rlist=list([])
    response=HttpResponse(template.render({'page':str(page),'res_count':str(res_num), 'res_duplicate':'0','reslist':rlist},request))
    response.set_cookie("query_hash",hashk,3600)
    return response

def result(request):
    p=request.path
    p=p.split("/")
    p=p[len(p)-1]
    p=int(p)
    cks=request.COOKIES
    hashk=cks.get('query_hash','$0')
    if hashk=='$0':
        return HttpResponse('<script>window.location="1"</script>')
    db=sqlite3.connect("database")
    cu=db.cursor()
    cu.execute("select * from query where hashkey= '"+hashk+"'")
    entry=cu.fetchall()[0]
    reslist=entry[1]
    num=int(entry[2])
    dtype=int(entry[3])
    if (p*5>num):
        return HttpResponse('<script>window.location="1"</script>')
    filename_list=reslist.split("@@")
    filename_list.pop()
    filename_list=filename_list[(p-1)*5:]
    if len(filename_list)>5:
        filename_list=filename_list[:5]
    i=0
    if dtype==0:
        for i in range(len(filename_list)):
            filename_list[i]=filename_list[i].replace('./thumbnail/','')
            filename_list[i]=filename_list[i].replace('.png','.mp4')
    else:
        for i in range(len(filename_list)):
            filename_temp=filename_list[i].split("/")
            filename_temp=filename_temp[-2]+"/"+filename_temp[-1]
            filename_list[i]=filename_list[i].replace('.fft3','.mp4')
    rlist=list([])
    for i in range(len(filename_list)):
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
    #print(res_num)
    #print(rlist[0:5])
    response=HttpResponse(template.render({'page':str(p),'res_count':str(num),'res_duplicate':'1', 'reslist':rlist},request))
    response.set_cookie("query_hash",hashk,3600)
    #res="<html>"+str(p)+"</html>"
    #response=HttpResponse(res)
    return response

