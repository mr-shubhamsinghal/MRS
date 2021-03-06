from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from accounts.decorators import unauthenticated_user
from accounts.forms import CustomUserCreationForm


@unauthenticated_user
def home(request):
	context = {}
	return render(request, 'home.html', context)


@unauthenticated_user
def register(request):
	form = CustomUserCreationForm()
	if request.method == 'POST':
		form = CustomUserCreationForm(request.POST)
		if form.is_valid():
			user = form.cleaned_data.get('email')
			form.save()
			messages.success(request, 'Account was created for ' + user)
			return redirect('authentication:login')
	context = {'form': form}
	return render(request, 'register.html', context)


@unauthenticated_user
def login_page(request):
	if request.method == 'POST':
		email = request.POST['email']
		password = request.POST['password']

		user = authenticate(request, email=email, password=password)

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