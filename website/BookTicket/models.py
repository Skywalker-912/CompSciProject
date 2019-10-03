from django.db import models
# from sqlserver_ado.fields import DateField, DateTimeField, TimeField

# Create your models here.
class user(models.Model):
    User_id = models.IntegerField(primary_key=True)
    Password = models.CharField(max_length=25)
    User_Name = models.CharField(max_length=100)
    Gender = models.CharField(max_length=1)
    Age = models.IntegerField()
    Email = models.CharField(max_length=100)
    City = models.CharField(max_length=50)
class Journey(models.Model):
    PNR_No = models.CharField(max_length=10)
    Train_No = models.CharField(max_length=50)
    Coach_No = models.CharField(max_length=5)
    Seat_No = models.IntegerField()
    Date = models.DateField()
    time = models.TimeField()
    Booked_user=models.CharField(max_length=50)
    Passenger_id=models.CharField(max_length=50)
    Quota=models.CharField(max_length=100)
class Station(models.Model):
    Station_Code = models.CharField(primary_key=True,max_length=10)
    Station_name = models.CharField(max_length=100)
    No_of_Platforms = models.IntegerField()
class Train(models.Model):
    Train_No = models.CharField(primary_key=True,max_length=50)
    Train_name = models.CharField(max_length=100)
    Source = models.CharField(max_length=10)
    Destination = models.CharField(max_length=10)
    Departure_time = models.TimeField()
    Arrival_time = models.TimeField()
    Capacity = models.IntegerField()
class passenger(models.Model):
    Passenger_id = models.IntegerField(primary_key=True)
    Passenger_name = models.CharField(max_length=100)
    Gender = models.CharField(max_length=1)
    Age = models.IntegerField()
class Stops(models.Model):
    Train_No = models.CharField(max_length=50)
    Station_id = models.CharField(max_length=50)
    Day = models.CharField(max_length=10)
    Arrival_time = models.TimeField()
    Departure_time = models.TimeField()
    Platform_no = models.IntegerField()
    Distance = models.IntegerField()
    class Meta:
        unique_together=('Train_No','Day','Arrival_time')
class Seats(models.Model):
    Train_No = models.CharField(max_length=50)
    Station_id = models.CharField(max_length=50)
    Type_of_seat = models.CharField(max_length=50)
    Date = models.DateField()
    Time = models.TimeField()
    Availability = models.IntegerField()
    class Meta:
        unique_together=('Train_No','Type_of_seat','Date','Time')
class Account(models.Model):
    aname=models.CharField(max_length=100)
    aemail=models.CharField(max_length=200)
    apwd=models.CharField(max_length=100)
    aage=models.IntegerField()
    agender=models.CharField(max_length=1)