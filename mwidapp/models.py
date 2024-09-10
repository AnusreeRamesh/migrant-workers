from django.db import models

# Create your models here.
class Authority(models.Model):
	username=models.CharField(max_length=200)
	email=models.EmailField(max_length=70,blank=True)
	district=models.CharField(max_length=200)
	mobile=models.CharField(max_length=200)
	password=models.CharField(max_length=200)
	def __str__(self):
		return self.username

class Worker(models.Model):
	username=models.CharField(max_length=200)
	email=models.EmailField(max_length=70)
	district=models.CharField(max_length=200)
	mobile=models.CharField(max_length=200)
	status=models.CharField(max_length=200,default="Pending")
	aplcn=models.CharField(max_length=20,default = "Not Applied")
	password=models.CharField(max_length=200)

	first_name=models.CharField(max_length=200)
	last_name=models.CharField(max_length=200)
	gender=models.CharField(max_length=2,choices=(('1','Male'),('0', 'Female')) , default = 1)
	address=models.CharField(max_length=200)
	marital_status=models.CharField(max_length=2,choices=(('1','Single'),('0', 'Married')) , default = 1)
	photo=models.ImageField(upload_to='images')  
	identification_mark=models.CharField(max_length=200)
	blood_group=models.CharField(max_length=200)
	uid_aadhar_driv=models.CharField(max_length=200)
	mwuid=models.CharField(max_length=200)

	def __str__(self):
		return self.username