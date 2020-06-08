from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from accounts.forms import CreateUserForm

@login_required(login_url='authentication:login')
def home(request):
	context = {}
	return render(request, 'home.html', context)

def register(request):
	from ipdb import set_trace; set_trace()
	form = CreateUserForm()
	if request.method == 'POST':
		form = CreateUserForm(request.POST)
		if form.is_valid():
			user = form.cleaned_data.get('identifier')
			form.save()
			messages.success(request, 'Account was created for ' + user)
			return redirect('authentication:login')
	context = {'form': form}
	return render(request, 'register.html', context)

def login_page(request):
	if request.method == 'POST':
		userid = request.POST['email']
		password = request.POST['password']

		user = authenticate(request, identifier=userid, password=password)

		if user is not None:
			login(request, user)
			return redirect('mrs_app:search')
		else:
			messages.info(request, 'Username or password is incorrect')

	context = {}
	return render(request, 'login.html', context)

def logout_page(request):
	logout(request)
	return redirect('/')