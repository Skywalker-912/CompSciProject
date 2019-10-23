from django.shortcuts import render
import csv
from BookTicket.models import Account
import os
import mysql.connector
import datetime
from django.http import HttpResponseRedirect

con=mysql.connector.connect(host="localhost", user="root", passwd="root",database="project")
curs=con.cursor()

# Create your views here.

x=[]
train=[]
datedict={'Jan':1,'Feb':2,'Mar':3,'Apr':4,'May':5,'Jun':6,'Jul':7,'Aug':8,'Sep':9,'Oct':10,'Nov':11,'Dec':12}
daydict={1:'MON',2:'TUE',3:'WED',4:'THU',5:'FRI',6:'SAT',7:'SUN'}

def seehomepg(request):
    return render(request,'Home_Page.html',{'al':[]})
def seehome(request):
    global x
    return render(request,'Home_Page.html',{'al':x})
def seelogin(request):
    global x
    if request.method=="POST":
        email=request.POST['email']
        pwd=request.POST['password']
        a=Account.objects.all()
        a_list=list(a)
        for i in range(len(a_list)):
            print(a_list)
            if email==a_list[i].aemail and pwd==a_list[i].apwd:
                x=a_list[i:i+1]
                return render(request,'Home_Page.html',{'al':x})
            else:
                return render(request,'Login.html')
    else:
        return render(request,'Login.html',{'al':[]})
def seepnr(request):
    global x
    return render(request,'PNR status.html',{'al':x})
def seesearch(request):
    global train
    global x
    global datedict
    if request.method=="POST":
        fromstat=request.POST['fromstat']
        tostat=request.POST['tostat']
        date=request.POST['date']
        month=datedict[date[0:3]]
        year=date[8:]
        dat=date[4:6]
        day=datetime.datetime(int(year),int(month),int(dat))
        day=day.isoweekday()
        curs.execute("select train_no,station_id from bookticket_stops where station_id in ('{}','{}')".format(fromstat,tostat))
        sid=curs.fetchall()
        stop=[]
        for i in range(len(sid)):
            for j in range(len(sid)):
                if j!=i and sid[i][0]==sid[j][0]:
                    if [sid[i],sid[j]][::-1] not in stop:
                        stop+=[[sid[i],sid[j]]]
        train=[]
        for t in stop:
            train_no=t[0][0]
            source=t[0][1]
            dest=t[1][1]
            curs.execute("select station_id,arrival_time from bookticket_stops where station_id in ('{}','{}')".format(source,dest))
            at=curs.fetchall()
            for i in at:
                if i[0]==source:
                    artime=i[1]
                if i[0]==dest:
                    deptime=i[1]
            curs.execute("select train_no,train_name from bookticket_train")
            tr=curs.fetchall()
            for i in tr:
                if i[0]==train_no:
                    train_name=i[1]
            curs.execute("select day from bookticket_stops where train_no={} and station_id='{}'".format(train_no,source))
            daycheck=curs.fetchall()
            for i in daycheck:
                if i[0]==daydict[day]:
                    train+=[(train_no,train_name,source,dest,artime,deptime)]
            
        return HttpResponseRedirect('../schedule',{'train':train,'btest':True})
    else:
        return render(request,'Search.html',{'al':x})
def seereg(request):
    if request.method=="POST":
        name=request.POST['name']
        email=request.POST['email']
        pwd=request.POST['password']
        repwd=request.POST['repassword']
        age=request.POST['age']
        with open('data.csv','a') as file:
            wcs=csv.writer(file)
            wcs.writerow(["name",name])
            wcs.writerow(["email",email])
            wcs.writerow(["pwd",pwd])
            wcs.writerow(["repwd",repwd])
            wcs.writerow(["age",age])
        lst=Account()
        lst.aname=name
        lst.aemail=email
        lst.apwd=pwd
        lst.aage=age
        lst.save()
        a_list=Account.objects.all()
        a_list=list(a_list)
        print(a_list)    
        k=a_list[-1:]
        print(k)
        return render(request,'Home_Page.html',{'al':k}) 
    else:
        return render(request,'Register.html')
def seeschedule(request):
    global x
    global train
    if request.method=="POST":
        return HttpResponseRedirect('../home')
    else:
        if not train:
            curs.execute('Select * from bookticket_train')
            trainall=curs.fetchall()
            return render(request,'Schedule.html',{'train':trainall,'al':x})
        else:
            t=train
            train=[]
            return render(request,'Schedule.html',{'train':t,'al':x,'btest':True})
# def seeform(request):
    # if request.method=="POST":
        # print(request.POST)
        # print('xyz')
        # return HttpResponseRedirect('home/')
