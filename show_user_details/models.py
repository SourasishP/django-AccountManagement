from django.db import models
from datetime import datetime

class user(models.Model):
    uname=models.CharField(max_length=10,unique=True)
    email=models.CharField(max_length=50,unique=True)
    pswd=models.CharField(max_length=15)
    status=models.CharField(max_length=13,default="complete")
    user_type=models.CharField(max_length=8,default="normal")
    verified=models.CharField(max_length=4,default="no")

class management_user(models.Model):
    uname=models.CharField(max_length=10,unique=True)
    acc_no=models.CharField(max_length=10,unique=True)
    amt=models.FloatField()
	
class perform_user(models.Model):
    trn_id=models.CharField(max_length=10,unique=True)
    from_acc=models.CharField(max_length=10)
    to_acc=models.CharField(max_length=10)
    amt=models.FloatField()
    remarks=models.CharField(max_length=50)
    date=models.DateField(default=datetime.now)

class user_profile(models.Model):
    uname=models.CharField(max_length=10,unique=True)
    photo=models.CharField(max_length=50,default="Picture.jpg")
    occupation=models.CharField(max_length=50,default="")
    dob=models.DateField(default=datetime.now)
