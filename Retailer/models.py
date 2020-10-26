from django.db import models
from django.db.models.deletion import CASCADE
from django.contrib.auth.models import User
from datetime import datetime
from VishwamaniJio import settings
from Row_Data.models import FOS

# Create your models here.
class Profile(models.Model):
    cr_date = models.DateTimeField(auto_now_add=True)
    user = models.OneToOneField(to=User, on_delete=CASCADE)
    PRM_ID = models.IntegerField()
    Jio_ID = models.IntegerField(null=True,blank=True)
    Retailer_Name = models.CharField(max_length=100)
    Mobile_No = models.IntegerField()
    Whatsapp_No = models.IntegerField()
    Email_ID = models.EmailField()
    Adharcard_no = models.IntegerField()
    Address = models.TextField()
    FOS_Assign =models.ForeignKey(to=FOS , default= "Vishwamani",on_delete=models.SET_DEFAULT, null=True, blank=True)
    def __str__(self):
        return self.Retailer_Name


class Report(models.Model):
    cr_date = models.DateTimeField(auto_now_add=True)
    Payment_Fill_Date = models.DateField()
    PRM_ID = models.IntegerField()
    Retailer_Name = models.CharField(max_length=100)
    Amount = models.IntegerField()
    Rifill_mode = models.CharField(max_length=20, default='AUTOREFILL MORNING', choices=(('AUTOREFILL MORNING','AUTOREFILL MORNING'),('AUTOREFILL AFTERNOON','AUTOREFILL AFTERNOON')))
    Payment_Remark = models.CharField(max_length=10, default = 'Pending',choices = (('Pending','Pending'),('Cash','Cash'),('Cheque','Cheque'),('UPI','UPI'),('NEFT','NEFT')))
    Payment_Date = models.DateField(null=True,blank=True)
    Cheque_No = models.IntegerField(null=True,blank=True)
    Bank_Name = models.CharField(max_length=100,null=True,blank=True)
    Distributor_Remark = models.CharField(max_length=100, default='Pending', null=True, blank=True, choices=(('Pending','Pending'),('Cheque_Bounce','Cheque_Bounce'),('Received','Received')))
    Payment_collected_by =models.ForeignKey(to=FOS , default= 1,on_delete=models.SET_DEFAULT, null=True, blank=True)
    def __str__(self):
        return self.Retailer_Name

class Order(models.Model):
    cr_date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(to=User, on_delete=CASCADE , null = True, blank =True)
    PRM_ID = models.IntegerField(null = True, blank =True)
    Retailer_Name = models.CharField(max_length=100, null = True, blank =True)
    Product = models.CharField(max_length=100, default='Sim Card', choices=(('Sim Card','Sim Card'),('jio_Phone','Jio Phone'),('Jio_Balance','Jio_Balance'),('Other','Other')))
    Quantity = models.IntegerField()
    Description = models.CharField(max_length=200)
    Order_Status= models.CharField(max_length=100, default='Pending', choices=(('Pending','Pending'),('In-Process','In-Process'),('Complete','Complete')))
    Distributor_Remark = models.CharField(max_length=100,null=True,blank=True)
    def __str__(self):
        return self.Retailer_Name

class Notice(models.Model):
    cr_date = models.DateTimeField(auto_now_add=True)
    Notice = models.TextField()
    Visible = models.BooleanField(default=True)

