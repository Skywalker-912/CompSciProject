from django.shortcuts import render
import csv
from BookTicket.models import Account
import os
import mysql.connector
con=mysql.connector.connect(host="localhost", user="root", passwd="root",database="project")
# Create your views here.
x=[]
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
    curs=con.cursor()
    curs.execute('Select * from bookticket_train')
    train=curs.fetchall()
    return render(request,'Schedule.html',{'train':train})
