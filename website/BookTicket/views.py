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

#List of all global variables.
x=[]
train=[]
pnrlist=[]
confdets=[]
tno=''
fdate=''
pnr=0
cost=0
datedict={'Jan':1,'Feb':2,'Mar':3,'Apr':4,'May':5,'Jun':6,'Jul':7,'Aug':8,'Sep':9,'Oct':10,'Nov':11,'Dec':12}
daydict={1:'MON',2:'TUE',3:'WED',4:'THU',5:'FRI',6:'SAT',7:'SUN'}
flag=True

#LOGGED OUT HOME PAGE
#On clicking on the logout button the home page is loaded. 'al' is the list that contains the user details, on logging out x is cleared.
def seehomepg(request):
    global x
    x=[]
    return render(request,'Home_Page.html',{'al':x})

#HOME PAGE
#If the method is GET the home page is loaded.
#The method is POST when the user gives feedback. The name,email,phone and the maessage is added to the database.
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

#LOGIN PAGE
#If the method is post the login page is loaded.
#If the method is post the email and password is taken. The password is checked using the values stored in the database.
#If the password and the username do not match a message is shown. If it is correct it loads the home page.
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

#PNR DETAILS
#The PNR number is taken as an input. 
#If the PNR doesn't exist in the database a message is shown. If it exists the details of the tickets are sent to the schedule page.
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

#SEARCH
#If the method is get the from station,to station and date is taken from the user. A train is found satisfying the conditions.
#If any train is found the details of the train is sent to the html and it is displayed. If there is no train a message is shown saying that no train is found
#If the method is get the search page is loaded.
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

#REGISTER
#If the method is get, the register page is loaded.
#If the method is post name,email,password,age and gender are taken from the user.
#If the email already exists in the database error message is displayed.If it doesnt exist,the details are added to the database and homepage is reloaded,logging in with the respective account.
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

#DETAILS OF TRAINS BASED ON INPUT
#If the method is get,respective train details are shown.
#If the method is post and the user is logged in, a random PNR number is generated and page is redirected to show the passenger details form
#If the user is not logged in,page is redirected to login. 
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

#PASSENGER DETAILS
#If the method is get,the passenger details form is shown.
#If the method is post,the entered details are taken and stored.Depending on distance and quota cost is calculated.
#The page is redirected to confirm page.
def seeform(request):
    global x
    global train
    global pnrlist
    global tno
    global fdate
    global pnr
    global cost
    global confdets
    ptest=True
    if request.method=="POST":
        psgname=request.POST['name']
        age=request.POST['age']
        gender=request.POST['gender']
        quota=request.POST['quota']
        user=x[1]
        if quota=="Divyaang":
            cost1=cost*3/4
        elif quota=="Tatkal":
            cost1=cost*1.5
        else:
            cost1=cost
        confdets=[x,psgname,age,gender,quota,cost1]
        print(cost,cost1)
        return HttpResponseRedirect('../confirm')
    else:
        return render(request,"Passenger Details.html",{'al':x})

#TICKET DETAILS
#If the method is get and the user is logged in,the details of booked and cancelled tickets are displayed.
#If the user is not logged in,the page is redirected to login.
#If the method is post,the selected ticket is cancelled.
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

#TRAIN SCHEDULE
#The details of all the trains are retrieved from the database and displayed.
def seetrschedule(request):
    global x
    curs.execute('Select Train_no,station_id from bookticket_stops')
    stops=curs.fetchall()
    stopdict={}
    for i in stops:
        stopdict[i[0]]=[]
    for i in stops:
        stopdict[i[0]]+=[i[1]]
    print(stopdict)
    print(stops)
    curs.execute('Select Train_No,Train_name,Source,Destination,Departure_time,Arrival_time from bookticket_train')
    trainall=curs.fetchall()
    t=(1,2)
    t+=(2,4)
    print(t)
    trainfinal=[]
    for i in trainall:
        for j in stopdict:
            print(str(stopdict[j])[1:-1])
            if i[0]==j:
                print('x')
                i+=(str(stopdict[j])[1:-1],)
                trainfinal+=[i]
    print(trainfinal)
    return render(request,'TrainSchedule.html',{'train':trainfinal,'al':x})

#CONFIRM DETAILS    
#If the method is get, the confirm page is loaded along woth the details entered in the passenger details page.
#If thhe method is post on clicking confirm, the details of the passenger is added to the database and the page is redirected to the home page.
#If the method is post on clicking edit, the page is redirected back to passenger details page.
def seeconfirm(request):
    global x
    global confdets
    global pnr
    global train
    global fdate
    global tno
    if request.method=="POST":
        print(request.POST)
        for i in request.POST:
            if request.POST[i]=='Confirm':
                act='Confirm'
            else:
                act='Edit'
        if act=='Confirm':
            for i in train:
                if i[0]==tno:
                    trtup=i
            tno=''
            seat=random.randint(1,50)
            date=fdate
            fdate=''
            user=x[1]
            curs.execute("insert into bookticket_passenger (Passenger_name,Gender,Age) values ('{}','{}',{})".format(confdets[1],confdets[3],confdets[2]))
            curs.execute("select passenger_id from bookticket_passenger")
            pid=curs.fetchall()[-1][0]
            curs.execute("insert into bookticket_journey (PNR_No,Train_No,Seat_No,Date,Time,Booked_user,Passenger_id,Quota,Status)values('{}','{}',{},'{}','{}','{}',{},'{}','Booked')".format(pnr,trtup[0],seat,date,trtup[4],user,pid,confdets[4]))
            con.commit()
            time.sleep(2)
            return render(request,'Home_Page.html',{'al':x})
        else:
            return HttpResponseRedirect('../form')
    else:
        return render(request,'Confirmation.html',{'al':x,'name':confdets[1],'age':confdets[2],'gender':confdets[3],'quota':confdets[4],'cost':confdets[5],'pnr':pnr})
