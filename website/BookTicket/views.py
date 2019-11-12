from django.shortcuts import render
import csv
from BookTicket.models import Account
import os
import mysql.connector
import datetime
from django.http import HttpResponseRedirect
import random
import time

con=mysql.connector.connect(host="localhost", user="root", passwd="root",database="project")
curs=con.cursor()

# Create your views here.

x=[]
train=[]
pnrlist=[]
tno=''
fdate=''
pnr=0
cost=0
datedict={'Jan':1,'Feb':2,'Mar':3,'Apr':4,'May':5,'Jun':6,'Jul':7,'Aug':8,'Sep':9,'Oct':10,'Nov':11,'Dec':12}
daydict={1:'MON',2:'TUE',3:'WED',4:'THU',5:'FRI',6:'SAT',7:'SUN'}
flag=True

def seehomepg(request):
    global x
    x=[]
    return render(request,'Home_Page.html',{'al':x})
def seehome(request):
    global x
    if request.method=="POST":
        name=request.POST['name']
        email=request.POST['email']
        phone=request.POST['phone']
        msg=request.POST['msg']
        curs.execute("insert into bookticket_message(name,email,phone,msg) values('{}','{}','{}','{}')".format(name,email,phone,msg))
        con.commit()
        return render(request,'Home_Page.html',{'al':x,'ftest':True})
    else:
        return render(request,'Home_Page.html',{'al':x})
def seelogin(request):
    global x
    if request.method=="POST":
        email=request.POST['email']
        pwd=request.POST['password']
        curs.execute("select * from bookticket_account")
        acc=curs.fetchall()
        for i in acc:
            if i[2]==email and i[3]==pwd:
                x=i
                return render(request,'Home_Page.html',{'al':i})
        else:
            return render(request,'Login.html',{'ltest':False})
    else:
        return render(request,'Login.html',{'al':[],'ltest':True})
def seepnr(request):
    global x
    if request.method=='POST':
        pnrno=request.POST['pnr']
        curs.execute("select pnr_no from bookticket_journey")
        pnrcheck=curs.fetchall()
        for i in pnrcheck:
            if i[0]==pnrno:
                flag=True
                break
            else:
                flag=False
        if flag==True:
            curs.execute("select passenger_name,pnr_no,train_no,seat_no,date,time,quota,status from bookticket_passenger p,bookticket_journey j where p.passenger_id=j.passenger_id and PNR_No={}".format(pnrno))
            pnrdetails=curs.fetchall()
            return render(request,'Tickets.html',{'al':x,'tickets':pnrdetails,'btest':False})
        else:
            return render(request,'PNR status.html',{'al':x,'ptest':True})
    else:
        return render(request,'PNR status.html',{'al':x})
def seesearch(request):
    global train
    global x
    global datedict
    global fdate
    global cost
    if request.method=="POST":
        fromstat=request.POST['fromstat']
        tostat=request.POST['tostat']
        date=request.POST['date']
        datesplit=date.split('-')
        if len(datesplit)!=3:
            return render(request,'Search.html',{'al':x})
        year,month,dat=datesplit
        fdate=datetime.datetime(int(year),int(month),int(dat))
        day=fdate.isoweekday()
        curs.execute("select train_no,station_id from bookticket_stops where station_id in ('{}','{}')".format(fromstat,tostat))
        sid=curs.fetchall()
        stop=[]
        for i in range(len(sid)):
            for j in range(len(sid)):
                if j!=i and sid[i][0]==sid[j][0]:
                    if [sid[i],sid[j]][::-1] not in stop:
                        stop+=[[sid[i],sid[j]]]
        train=[]
        print(stop)
        for t in stop:
            train_no=t[0][0]
            source=t[0][1]
            dest=t[1][1]
            curs.execute("select station_id,arrival_time,train_no from bookticket_stops where station_id in ('{}','{}')".format(source,dest))
            at=curs.fetchall()
            for i in at:
                if i[2]==train_no:
                    if i[0]==source:
                        artime=i[1]
                    if i[0]==dest:
                        deptime=i[1]
            curs.execute("select train_no,train_name from bookticket_train")
            tr=curs.fetchall()
            for i in tr:
                if i[0]==train_no:
                    train_name=i[1]
            print(i)
            curs.execute("select distance from bookticket_stops where train_no={} and station_id in ('{}','{}') ORDER BY FIELD (station_id,'{}','{}')".format(train_no,fromstat,tostat,fromstat,tostat) )
            discheck=curs.fetchall()
            if discheck[0][0]<discheck[1][0]:
                flag=True
                dis=discheck[1][0]-discheck[0][0]
            else:
                flag=False
            if dis<=50:
                cost=200
            elif dis>=500:
                cost=5000
            else:
                cost=dis*10
            if flag:
                curs.execute("select day from bookticket_stops where train_no={} and station_id='{}'".format(train_no,source))
                daycheck=curs.fetchall()
                for i in daycheck:
                    if i[0]==daydict[day]:
                        train+=[(train_no,train_name,source,dest,artime,deptime)]
                print(train)

        if not train:
            return render(request,'Search.html',{'al':x,'ttest':True,'train':[]})
        return HttpResponseRedirect('../schedule')
    else:
        return render(request,'Search.html',{'al':x})
def seereg(request):
    global x
 
    if request.method=="POST":
        name=request.POST['name']      
        email=request.POST['email']        
        pwd=request.POST['password']       

        age=request.POST['age']      
        gender=request.POST['gender']

        curs.execute("select aemail from bookticket_account")
        emaillist=curs.fetchall()
        for i in emaillist:
            if i[0]==email:
                flag=True
                break
            else:
                flag=False
        if flag==False:
            
            curs.execute("insert into bookticket_account (aname,aemail,apwd,aage,agender) values('{}','{}','{}',{},'{}')".format(name,email,pwd,age,gender))
            con.commit()
            curs.execute('select * from bookticket_account')
            acc=curs.fetchall()
            x=acc[-1]
            return render(request,'Home_Page.html',{'al':x}) 
        else:
            return render(request,'Register.html',{'rtest':True})
    else:
        return render(request,'Register.html')
def seeschedule(request):
    global x
    global train
    global tno
    global pnrlist
    global pnr
    tno=''
    if request.method=="POST":
        if x:
            for i in request.POST:
                if request.POST[i]=='Book':
                    tno=i
            pnr=random.randint(1000000000,9999999999)
            while True:
                if pnr not in pnrlist:
                    pnrlist+=[pnr]
                    break
            else:
                pnr=str(random.randint(1000000000,9999999999))
            return HttpResponseRedirect('../form')
        else:
            return HttpResponseRedirect('../login')
    else:
        return render(request,'Schedule.html',{'train':train,'al':x})

def seeform(request):
    global x
    global train
    global pnrlist
    global tno
    global fdate
    global pnr
    global cost
    ptest=True
    if request.method=="POST":
        psgname=request.POST['name']
        age=request.POST['age']
        gender=request.POST['gender']
        quota=request.POST['quota']
        for i in train:
            if i[0]==tno:
                trtup=i
        tno=''
        seat=random.randint(1,50)
        date=fdate
        fdate=''
        user=x[1]
        if quota=="Divyaang":
            cost1=cost*3/4
        elif quota=="Tatkal":
            cost1=cost*1.5
        else:
            cost1=cost
        print(cost,cost1)
        # curs.execute("insert into bookticket_passenger (Passenger_name,Gender,Age) values ('{}','{}',{})".format(psgname,gender,age))
        # curs.execute("select passenger_id from bookticket_passenger")
        # pid=curs.fetchall()[-1][0]
        # curs.execute("insert into bookticket_journey (PNR_No,Train_No,Seat_No,Date,Time,Booked_user,Passenger_id,Quota,Status)values('{}','{}',{},'{}','{}','{}',{},'{}','Booked')".format(pnr,trtup[0],seat,date,trtup[4],user,pid,quota))
        # con.commit()
        return render(request,'Confirmation.html',{'al':x,'name':psgname,'age':age,'gender':gender,'quota':quota,'cost':cost1})
    else:
        return render(request,"Passenger Details.html",{'al':x,'pnr':pnr})
def seeticket(request):
    global x
    
    if request.method=="POST":
        for i in request.POST:
            if request.POST[i]=='Cancel':
                curs.execute("update bookticket_journey set status='Cancelled' where pnr_no={}".format(i))
                con.commit()
                curs.execute("select passenger_name,pnr_no,train_no,seat_no,date,time,quota from bookticket_passenger p,bookticket_journey j where p.passenger_id=j.passenger_id and booked_user='{}' and status='Booked'".format(x[1]))
                tickbook=curs.fetchall()
                curs.execute("select passenger_name,pnr_no,train_no,seat_no,date,time,quota from bookticket_passenger p,bookticket_journey j where p.passenger_id=j.passenger_id and booked_user='{}' and status='Cancelled'".format(x[1]))
                tickcancel=curs.fetchall()
                time.sleep(2)
        return render(request,'Tickets.html',{'al':x,'tickets':tickbook,'cancel':tickcancel,'btest':True})
        
    else:
        if x:
            curs.execute("select passenger_name,pnr_no,train_no,seat_no,date,time,quota from bookticket_passenger p,bookticket_journey j where p.passenger_id=j.passenger_id and booked_user='{}' and status='Booked'".format(x[1]))
            tickbook=curs.fetchall()
            curs.execute("select passenger_name,pnr_no,train_no,seat_no,date,time,quota from bookticket_passenger p,bookticket_journey j where p.passenger_id=j.passenger_id and booked_user='{}' and status='Cancelled'".format(x[1]))
            tickcancel=curs.fetchall()
            return render(request,'Tickets.html',{'al':x,'tickets':tickbook,'cancel':tickcancel,'btest':True})
        else:
            return HttpResponseRedirect('../login')
def seetrschedule(request):
    global x
    curs.execute('Select * from bookticket_train')
    trainall=curs.fetchall()
    return render(request,'TrainSchedule.html',{'train':trainall,'al':x})
def seeconfirm(request):
    global x
    if request.method=="POST":
        psgname=request.POST['name']
        age=request.POST['age']
        gender=request.POST['gender']
        quota=request.POST['quota']
        curs.execute("insert into bookticket_passenger (Passenger_name,Gender,Age) values ('{}','{}',{})".format(psgname,gender,age))
        curs.execute("select passenger_id from bookticket_passenger")
        pid=curs.fetchall()[-1][0]
        curs.execute("insert into bookticket_journey (PNR_No,Train_No,Seat_No,Date,Time,Booked_user,Passenger_id,Quota,Status)values('{}','{}',{},'{}','{}','{}',{},'{}','Booked')".format(pnr,trtup[0],seat,date,trtup[4],user,pid,quota))
        con.commit()
        return render(request,'Home_Page.html',{'al':x})