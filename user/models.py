from django.db import models

class Product(models.Model):
    pid=models.AutoField(primary_key=True)
    pname=models.CharField(max_length=50,unique=True)
    subcatname=models.CharField(max_length=50)
    pdescription=models.CharField(max_length=500)
    bprice=models.IntegerField()
    piconname=models.CharField(max_length=100) 
    uid=models.CharField(max_length=50)
    info=models.CharField(max_length=100)

class Funds(models.Model):
    txnid=models.AutoField(primary_key=True)
    uid=models.CharField(max_length=50)
    amt=models.IntegerField()
    info=models.CharField(max_length=50)

class Bidding(models.Model):
    bidid=models.AutoField(primary_key=True)
    pid=models.IntegerField()
    uid=models.CharField(max_length=50)
    bidprice=models.IntegerField()
    info=models.CharField(max_length=50)     
    
