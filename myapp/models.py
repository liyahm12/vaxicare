from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Users(models.Model):
    name=models.CharField(max_length=100)
    place=models.CharField(max_length=100)
    state=models.CharField(max_length=100)
    city=models.CharField(max_length=100)
    pincode=models.CharField(max_length=100)
    gender=models.CharField(max_length=100)
    Dob=models.DateField()
    Upload_photo=models.CharField(max_length=300)
    email=models.CharField(max_length=100)
    phone=models.CharField(max_length=100)
    AUTHUSER=models.OneToOneField(User,on_delete=models.CASCADE)



class Hospital(models.Model):
    hospitalname=models.CharField(max_length=100)
    hospitalplace=models.CharField(max_length=100)
    city=models.CharField(max_length=100)
    hospitalstate=models.CharField(max_length=100)
    hospitalpincode=models.CharField(max_length=100)
    email=models.CharField(max_length=100)
    phone=models.CharField(max_length=100)
    Upload_photo=models.CharField(max_length=300)
    licensenumber=models.CharField(max_length=100)
    status=models.CharField(max_length=100)
    AUTHUSER = models.OneToOneField(User, on_delete=models.CASCADE)


class vaccine_information(models.Model):
   Vaccinename = models.CharField(max_length=500)
   Age = models.BigIntegerField()
   Dose_number = models.CharField(max_length=100)
   Description = models.CharField(max_length=1000)
   Side_effect = models.CharField(max_length=500)
   Manufacture = models.CharField(max_length=100)
   Emergency_type = models.CharField(max_length=100)

class country_vaccine(models.Model):
    Destination_country= models.CharField(max_length=100)
    Discription = models.CharField(max_length=1000)
    VACCINATIONINFORMATION=models.ForeignKey(vaccine_information,on_delete=models.CASCADE)

class slot(models.Model):
    VACCINATIONINFORMATION=models.ForeignKey(vaccine_information,on_delete=models.CASCADE)
    Fromtime=models.TimeField()
    Date=models.DateField()
    HOSPITAL=models.ForeignKey(Hospital,on_delete=models.CASCADE)

class Booking(models.Model):
    Discription = models.CharField(max_length=1000)
    SLOT = models.ForeignKey(slot, on_delete=models.CASCADE)
    USER=models.ForeignKey(Users,on_delete=models.CASCADE)
    status=models.CharField(max_length=1002)
    Type= models.CharField(max_length=100)
    Date =models.DateField()
    Cid=models.CharField(max_length=100)

class VaccineDocument(models.Model):
    Document=models.CharField(max_length=100)
    status=models.CharField(max_length=100)
    Date = models.DateField()
    USER=models.ForeignKey(Users,on_delete=models.CASCADE)
    HOSPITAL=models.ForeignKey(Hospital,on_delete=models.CASCADE)


class Vaccinestock(models.Model):
    VACCINATIONINFORMATION=models.ForeignKey(vaccine_information,on_delete=models.CASCADE)
    HOSPITAL=models.ForeignKey(Hospital,on_delete=models.CASCADE)
    stock_no = models.IntegerField(default=1)

class Child(models.Model):
    Name = models.CharField(max_length=100)
    gender = models.CharField(max_length=100)
    USER=models.ForeignKey(Users,on_delete=models.CASCADE)
    Dob = models.DateField()
    blood_group= models.CharField(max_length=10)
    relation=models.CharField(max_length=100)







