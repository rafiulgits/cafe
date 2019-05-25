from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, HttpResponse
from generic.service import verify_email
from user.forms import ProfileUpdateForm, AddMoneyForm


@login_required(login_url='/signin/')
def view(request):
	user = request.user
	context = {
		'user' : user
	}
	return render(request, 'user/profile/view.html', context)



@login_required(login_url='/signin/')
def update(request):
	context = {}
	user = request.user

	if request.method == 'POST':
		form = ProfileUpdateForm(request.POST, user=user)
		if form.is_valid():
			if form.is_new_email():
				user = form.save(commit=False)
				user.is_active = False
				user.save()
				verify_email(request, user)
				return HttpResponse('<h1 align="center">Verify Your Email. Check Your Mailbox</h1>')
			form.save()
			return redirect('/profile/')
	else:
		form = ProfileUpdateForm(user=request.user)

	context['form'] = form

	return render(request, 'user/profile/update.html', context)



@login_required(login_url='/signin/')
def add_money(request):
	if request.method == 'POST':
		form = AddMoneyForm(request.POST, user=request.user)
		if form.is_valid():
			form.save()
			return redirect('/profile/')
	else:
		form = AddMoneyForm(user=request.user)

	context = {'form' : form}
	return render(request, 'user/profile/add_money.html', context)