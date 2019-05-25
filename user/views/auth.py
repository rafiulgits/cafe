from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, HttpResponse
from generic.helper import decode as token_decode
from generic.service import verify_email
from user.models import Account
from user.forms import SignupForm, SigninForm, PasswordChangeForm


def signup(request):
	if request.user.is_authenticated:
		return redirect('/')

	if request.method == 'POST':
		form = SignupForm(request.POST, request.FILES)
		if form.is_valid():
			user = form.save(commit=False)
			user.is_active = False
			user.save()
			verify_email(request, user)
			return HttpResponse('<h1 align="center">Verify Your Email. Check Your Mailbox</h1>')

	else:
		form = SignupForm()
	context = {
		'form' : form
	}
	return render(request, 'user/auth/signup.html', context)


def verify(request, token):
	data = token_decode(token)
	if data is None:
		return views.invalid_request(request)

	user_id = data['user_id']
	email = data['email']

	user = Account.objects.get(id=user_id)
	user.is_active = True
	user.save()
	login(request, user)
	return HttpResponse('<h1 align="center">Email verified</h1>')


def signin(request):
	if request.user.is_authenticated:
		return redirect('/')
	if request.method == 'POST':
		form = SigninForm(request.POST)
		if form.is_valid():
			user = form.user
			login(request, user)
			return redirect('/profile/')
	else:
		form = SigninForm()

	context = {
		'form' : form
	}

	return render(request, 'user/auth/signin.html', context)



@login_required(login_url='/signin/')
def signout(request):
	logout(request)
	return redirect('/')


@login_required(login_url='/signin/')
def change_password(request):
	context = {}

	if request.method == 'POST':
		form = PasswordChangeForm(request.POST, user=request.user)
		if form.is_valid():
			user = form.save()
			logout(request)
			login(request, user)

			return redirect('/profile/')
	else:
		form = PasswordChangeForm(user=request.user)
	context['form'] = form

	return render(request, 'user/password/change.html', context)