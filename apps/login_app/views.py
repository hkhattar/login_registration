from django.shortcuts import render, HttpResponse, redirect
from .models import User
from django.contrib import messages
import re
import bcrypt

# Create your views here.
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
NAME_REGEX = re.compile(r'^[a-zA-Z]+$')
def index(request):
	# User.userManager.login("speros@codingdojo.com", "Speros") 
	return render(request,"login_app/index.html")


def register(request):
	if request.method == 'POST':
		x = False
		if not EMAIL_REGEX.match(request.POST['email']):
			messages.info(request, ' Invalid email ')
			x = True
			# return redirect('/')
		if not NAME_REGEX.match(request.POST['first_name']):
			messages.info(request, ' Invalid name ')
			x = True
			# return redirect('/')
		if not NAME_REGEX.match(request.POST['last_name']):
			messages.info(request, ' Invalid name ')
			x = True
			# return redirect('/')
		if len(request.POST['password']) < 8:
			messages.info(request,'Password must be atleast 8 characters long')
			x = True
			# return redirect('/')
		elif request.POST['password'] != request.POST['confirm_password']:
			messages.info(request,'Password and confirm password are not matched')
			x = True
			# return redirect('/')

		if x:
			return redirect('/')

		else:
			password = request.POST['password'].encode()
			hashed = bcrypt.hashpw(password, bcrypt.gensalt())
			User.userManager.create(first_name=request.POST['first_name'],last_name=request.POST['last_name'],email = request.POST['email'],password=hashed )
	print ('**************')
	request.session['first_name'] = request.POST['first_name']
	return redirect('/success')

def success(request):

	return render(request,"login_app/success.html")


def login(request):
	email = request.POST['email']
	password = request.POST['password']
	password = password.encode()
	user = User.userManager.get(email = email)
	ps_hashed = user.password
	ps_hashed = ps_hashed.encode()
	request.session['first_name'] = user.first_name
	if bcrypt.hashpw(password, ps_hashed) == ps_hashed:
		return render(request, 'login_app/success.html')
	else:
		messages.error(request, "email or password does not match")
		return redirect('/')







