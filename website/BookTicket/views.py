from django.shortcuts import render
import csv
from BookTicket.models import Account
import os
import mysql.connector
import datetime

con=mysql.connector.connect(host="localhost", user="root", passwd="root",database="project")
curs=con.cursor()

# Create your views here.

x=[]
datedict={'Jan':1,'Feb':2,'Mar':3,'Apr':4,'May':5,'Jun':6,'Jul':7,'Aug':8,'Sep':9,'Oct':10,'Nov':11,'Dec':12}
daydict={1:'MON',2:'TUE',3:'WED',4:'THU',5:'FRI',6:'SAT',7:'SUN'}
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
        print(sid)
        stop=[]
        for i in range(len(sid)):
            for j in range(len(sid)):
                if j!=i and sid[i][0]==sid[j][0]:
                    if [sid[i],sid[j]][::-1] not in stop:
                        stop+=[[sid[i],sid[j]]]
        print(stop)
        return render(request,'Schedule.html')
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
    
    curs.execute('Select * from bookticket_train')
    train=curs.fetchall()
    return render(request,'Schedule.html',{'train':train})
