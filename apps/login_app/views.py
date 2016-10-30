from django.shortcuts import render, HttpResponse, redirect
from .models import User, Destination
from django.contrib import messages
import re
import bcrypt
from datetime import date 

# Create your views here.
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
NAME_REGEX = re.compile(r'^[a-zA-Z]+$')
DESTINATION_REGEX = re.compile(r'^(.*?[a-zA-Z]){4,}.*$')
def index(request):
	# User.objects.login("speros@codingdojo.com", "Speros") 
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
			email= request.POST['email']
			password = request.POST['password'].encode()
			hashed = bcrypt.hashpw(password, bcrypt.gensalt())
			User.objects.create(first_name=request.POST['first_name'],last_name=request.POST['last_name'],email = request.POST['email'],password=hashed )
	print ('**************')

	user = User.objects.get(email = email)
	request.session['first_name'] = request.POST['first_name']
	request.session['id'] = user.id
	return redirect('/success')

def success(request):
	
	user = User.objects.get(id = request.session['id'])
	context = {
		# 'trip_schedule' : Destination.objects.filter(user = user)
		'trip_schedule' : Destination.objects.all()
	}
	return render(request,"login_app/success.html",context)





def login(request):
	email = request.POST['email']
	password = request.POST['password']
	x = False;

	if len(email) == 0:
		messages.error(request, "email is required")
		x = True;

	elif not User.objects.filter(email = email).exists():
		messages.error(request, "email is not in the database")
		x=True;

	if x:
		return redirect('/')
	else:
		password = password.encode()
		user = User.objects.get(email = email)
		ps_hashed = user.password
		ps_hashed = ps_hashed.encode()
		request.session['first_name'] = user.first_name
		if bcrypt.hashpw(password, ps_hashed) == ps_hashed:
			request.session['id'] = user.id
			request.session['first_name'] = user.first_name
			return render(request, 'login_app/success.html')
		else:
			messages.error(request, "email or password does not match")
			return redirect('/')


def create(request):
	return render(request,"login_app/create.html")

def plan_process(request):
	destination = request.POST['destination']
	description = request.POST['description']
	travel_date_from = request.POST['travel_date_from']
	travel_date_to = request.POST['travel_date_to']

	
	if request.method == 'POST':
		x = False
		if not DESTINATION_REGEX.match(destination):
			messages.info(request, ' Invalid destination ')
			x = True
		elif not DESTINATION_REGEX.match(description):
			messages.info(request, ' Invalid description ')
			x = True
		elif len(travel_date_from) < 4:
			messages.info(request, "invalid date")
			x = True;

		elif len(travel_date_to) < 4:
			messages.info(request, "invalid date")
			x = True;
		elif travel_date_from > travel_date_to:
			messages.info(request, "travel date to should not be before the travel date from ")
			x = True;
		# elif travel_date_from < date.today():
			# messages.info(request, "travel date should be future dated ")
			# x = True;

		# if not DESTINATION_REGEX.match(travel_date_from):
		# 	messages.info(request, ' Invalid date ')
		# 	x = True
		# if not DESTINATION_REGEX.match(travel_date_to):
		# 	messages.info(request, ' Invalid date ')
		# 	x = True
		if x:
			return redirect('/create')
		Destination.objects.create(name=destination,description=description,travel_date_from=travel_date_from,travel_date_to=travel_date_to)

	return redirect('/success')

	
def show(request,id):
	plan = Destination.objects.get(id=id)
	context={'name': plan.name, 'description':plan.description,'travel_date_from':plan.travel_date_from,'travel_date_to':plan.travel_date_to
			}

	return render(request,"login_app/show.html",context)
	


def remove(request,id):
	# context ={
	# 	'id' : id,
	# 	'item' : Wish_list.objects.get(id=id),
	# 	'added_by' : Wish_list.objects.get(id=id)
	# }

	plan = Destination.objects.get(id=id)
	plan.delete()
	return redirect('/success')



















