from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .forms import *
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.views.generic import *
from django.contrib.auth.decorators import login_required
from random import randrange
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
import os
from qr_code.qrcode import *
import qrcode
from django.db.models import Q


# Create your views here.
def home(request):
	return render(request,'base.html')

def about(request):
	return render(request,'about.html')

def contact(request):
	return render(request,'contact.html')

def authority_registration(request):
	if request.method=='POST':
		try:
			a=Authority.objects.get(district=request.POST.get("district"))
		except:
			form=AuthorityForm(request.POST,request.FILES)
			if form.is_valid():
				instance=form.save(commit=False)
				instance.save()
				username = request.POST['username']
				email = request.POST['email']				
				password = request.POST['password']
				myuser = User.objects.create_user(username,email,password)
				myuser.is_active=False
				myuser.is_staff=True
				myuser.save()  
				messages.success(request, 'Authority Registered Succesfully.')
				return HttpResponseRedirect('/login1') 
			else:
				form=AuthorityForm()
				context={"form":form}
				messages.error(request, 'Form Not Valid.')
				return render(request,'authority_registration.html',context)
		else:
			form=AuthorityForm()
			context={"form":form}
			messages.error(request, 'Authority Exists.')
			return render(request,'authority_registration.html',context)
	else:
		form=AuthorityForm()
		context={"form":form}
		return render(request,'authority_registration.html',context)


def user_registration(request):
	if request.method=='POST':
		form=UserForm(request.POST,request.FILES)
		if form.is_valid():
			instance=form.save(commit=False)
			instance.save()
			username = request.POST['username']
			email = request.POST['email']				
			password = request.POST['password']
			myuser = User.objects.create_user(username,email,password)
			myuser.is_active=False
			myuser.save()  
			messages.success(request, 'Worker Registered Succesfully.')
			return HttpResponseRedirect('/login1')
		else:
			form=AuthorityForm()
			context={"form":form}
			messages.error(request, 'Form Not Valid.')
			return render(request,'user_registration.html',context)
	else:
		form=AuthorityForm()
		context={"form":form}
		return render(request,'user_registration.html',context)



@login_required
def view_card(request, pk =None):
    if pk is None:
        return HttpResponse("Employee ID is Invalid")
    else:
        context = {}
        context['emp'] = Worker.objects.get(id=pk)
        return render(request, 'view_id.html', context)




def login1(request):
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(username=username, password=password)
		if user is not None:
			if user.is_staff==True:
				login(request, user)
				messages.success(request, "Logged In Sucessfully !")
				return redirect('authority_base')
			else:
				login(request, user)
				messages.success(request, "Logged In Sucessfully !")
				return redirect('user_base')
		else:
			messages.error(request, "Invalid Username or Password")
			return redirect('login1')
	return render(request, "login.html")

@login_required(login_url='login1')
def authority_base(request):
	dist=Authority.objects.get(username=request.user.username)
	# print(dist.district)
	wkrno=Worker.objects.filter(status='Approved').count()
	wkrno_appr=Worker.objects.filter(status='Approved').filter(district=dist.district).count()
	wkrno_rej=Worker.objects.filter(status='Rejected').filter(district=dist.district).count()
	return render(request, "authority_base.html",{'wkrno':wkrno,'wkrno_appr':wkrno_appr,'wkrno_rej':wkrno_rej})

@login_required(login_url='login1')
def user_base(request):
	wkr=Worker.objects.get(username=request.user.username)
	return render(request, "user_base.html",{'worker':wkr})

@login_required(login_url='login1')
def logout1(request):
	logout(request)
	return redirect('home')

@login_required(login_url='login1')
def authority_details(request,name):
	authr=Authority.objects.get(username=request.user.username)
	return render(request,'authority_detail_view.html',{'authority':authr})

@login_required(login_url='login1')
def authorityEdit(request, id=None):
	ath = Authority.objects.get(username=request.user.username)
	form = AuthorityForm(instance=ath)
	if request.method == 'POST':
		form = AuthorityForm(request.POST, instance=ath)
		if form.is_valid():
			form.save()
			return redirect('/')
	context = {'form':form}
	return render(request,'authorityEditForm.html',context)

@login_required(login_url='login1')
def user_details(request,name):
	usr=Worker.objects.get(username=request.user.username)
	return render(request,'user_detail_view.html',{'users':usr})

@login_required(login_url='login1')
def userEdit(request, id=None):
	wk = Worker.objects.get(username=request.user.username)
	form = ApplyUserForm(instance=wk)
	if request.method == 'POST':
		form = ApplyUserForm(request.POST,request.FILES, instance=wk)
		if form.is_valid():
			form.save()
	context = {'form':form,'wks':wk}
	return render(request,'userEditForm.html',context)

@login_required(login_url='login1')
def view_users(request):
	dist=Authority.objects.get(username=request.user.username)
	wks = Worker.objects.filter(aplcn='Applied').filter(district=dist.district).values() | Worker.objects.filter(aplcn='1').filter(district=dist.district).values()
	
	if len(request.GET) > 0:
	    search_query = request.GET.get('q')
	    wks = wks.filter(Q(first_name__icontains=search_query) |
	    	Q(last_name__icontains=search_query) |
	    	Q(district__icontains=search_query)).distinct()
	context={"workers":wks}
	return render(request,'view_users.html',context)

@login_required(login_url='login1')
def view_full_data(request,name):
	usr=Worker.objects.get(username=name)
	return render(request,'user_detail_view_full.html',{'users':usr})

@login_required(login_url='login1')
def approve_user(request,name):
	usr=Worker.objects.get(username=name)
	# usr.update(status=True)
	usr.aplcn='Applied'
	usr.status='Approved'
	usr.mwuid=str(randrange(1, 10**6)).zfill(6)
	usr.save()
	return render(request,'user_detail_view_full.html',{'users':usr})

@login_required(login_url='login1')
def reject_user(request,name):
	usr=Worker.objects.get(username=name)
	# usr.update(status=True)
	usr.mwuid=''
	usr.status='Rejected'
	usr.aplcn='Applied'
	usr.save()
	return render(request,'user_detail_view_full.html',{'users':usr})

@login_required(login_url='login1')
def approved_user_list(request):
	dist=Authority.objects.get(username=request.user.username)
	wks=Worker.objects.filter(status='Approved').filter(district=dist.district).values()
	
	if len(request.GET) > 0:
		search_query = request.GET.get('q')
		wks = wks.filter(Q(first_name__icontains=search_query) |
			Q(last_name__icontains=search_query) |
			Q(district__icontains=search_query)).distinct()
	return render(request,'view_users.html',{"workers":wks})

@login_required(login_url='login1')
def rejected_user_list(request):
	dist=Authority.objects.get(username=request.user.username)
	wks=Worker.objects.filter(status='Rejected').filter(district=dist.district).values()

	if len(request.GET) > 0:
		search_query = request.GET.get('q')
		wks = wks.filter(Q(first_name__icontains=search_query) |
			Q(last_name__icontains=search_query) |
			Q(district__icontains=search_query)).distinct()
	return render(request,'view_users.html',{"workers":wks})

@login_required(login_url='login1')
def submit_application(request):
	usr=Worker.objects.get(username=request.user.username)
	usr.aplcn='Applied'
	usr.save()
	return render( request, 'submit_application.html')

@login_required(login_url='login1')
def download_card(request,name):
	root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
	usr=Worker.objects.get(id=name)
    #Qr code
	data = usr.mwuid
	qr = qrcode.QRCode(box_size=100)
	qr.add_data(data)
	qr_image = qr.make_image()
	root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
	qr_image.save("pdf/"+'id_card.png')
    # PDF Format
	c = canvas.Canvas("pdf/"+'id_card.pdf')
	width = 210*mm
	height = 297*mm
	c.setPageSize((width, height))

	c.roundRect(100, 400, 180, 280, 5, stroke=1, fill=0)
	c.roundRect(300, 400, 180, 280, 5, stroke=1, fill=0)

	c.setFont('Helvetica-Bold', 10)
	c.drawString(120, 650, "Migrant Workers ID Card")
	c.drawString(135, 630, "MW ID No: "+usr.mwuid)
	c.drawImage(root+usr.photo.url, 145, 480, height=120, width=100)

	c.drawString(135, 450, usr.first_name+" "+usr.last_name)
	c.drawString(135, 440, usr.email)
	c.drawString(135, 430, usr.district)

	c.drawString(335, 650, "Address")
	if len(usr.address)>30: 
		c.drawString(335, 640, usr.address[0:15])
		c.drawString(335, 630, usr.address[15:])
	elif len(usr.address)>15:
		c.drawString(335, 640, usr.address[0:15])
		c.drawString(335, 630, usr.address[15:])
	else:
		c.drawString(335, 640, usr.address)

	c.drawString(335, 610, "Marital Status")
	if usr.marital_status=='1':
		c.drawString(335, 600, "Single")
	else:
		c.drawString(335, 600, 'Married')

	c.drawString(335, 580, "Identification Mark")
	c.drawString(335, 570, usr.identification_mark)
	c.drawString(335, 550, "Blood Group")
	c.drawString(335, 540, usr.blood_group)
	c.drawString(335, 520, "Aadhar/Driving No")
	c.drawString(335, 510, usr.uid_aadhar_driv)
	c.drawImage("pdf/"+'id_card.png', 335, 410, height=100, width=100)

	# c.drawString(30*mm, 280*mm, "Branch")
	c.save()

	response = HttpResponse(open("pdf"+'/id_card.pdf', 'rb').read(), content_type='application/zip')
	response['Content-Disposition'] = 'attachment; filename=ID_CARD.pdf'
	return response

	return render( request, 'download_html.html')



@login_required(login_url='login1')
def download_noc(request,name):
	root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
	usr=Worker.objects.get(id=name)
    
    # PDF Format
	c = canvas.Canvas("pdf/"+'NOC.pdf')
	width = 210*mm
	height = 297*mm
	c.setPageSize((width, height))
	c.setFont('Helvetica-Bold', 14)
	c.drawString(225, 750, "No Objection Certificate")
	c.drawString(225, 747, "_____________________")		
	c.setFont('Helvetica', 11)
	c.drawString(100, 650, "This is to certify that Mr./Ms./Mrs.")
	c.drawString(270, 646, "..........................................................................")
	c.setFont('Helvetica-Bold', 11)
	c.drawString(275, 650, usr.first_name+"  "+usr.last_name)
	c.setFont('Helvetica', 11)
	c.drawString(100, 620, "a resident of..............................................................................................................") 	
	c.setFont('Helvetica-Bold', 11)
	c.drawString(175, 624,usr.address)
	c.setFont('Helvetica', 11)
	c.drawString(100, 590,"is allowed to do work in any location in" + "..................................." + "district.")
	c.drawString(300, 593,usr.district)
	c.setFont('Helvetica', 11)
	c.drawString(100, 563,"This NOC has been issued as per the request of the worker and can be used by")
	c.drawString(100, 533,"him/her for the specific purpose mentioned above.")
	c.drawString(100, 470,"District: ..........................")
	c.setFont('Helvetica-Bold', 11)
	c.drawString(150, 473,usr.district)
	c.drawImage("pdf/"+'SEAL.JPG', 335, 410)
	c.save()

	response = HttpResponse(open("pdf"+'/NOC.pdf', 'rb').read(), content_type='application/zip')
	response['Content-Disposition'] = 'attachment; filename=NOC.pdf'
	return response
	return render( request, 'download_html.html')