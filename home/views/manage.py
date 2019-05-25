from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist

from home.models import (CafeBranch, BranchFood, OrderCart, Order, BranchStaff,
	FoodItem)
from home.forms import CafeBranchUpdateForm
from datetime import date

@login_required(login_url='/signin/')
def dashboard(request):
	if not request.user.is_staff:
		return HttpResponse('<h1 align="center">404</h1>')

	branch_staff = BranchStaff.objects.filter(staff=request.user).first()
	if branch_staff is None:
		return HttpResponse('<h1 align="center">404</h1>')
	cafe_branch = branch_staff.branch
	today = date.today()
	orders = Order.objects.filter(branch_id=cafe_branch.id, request_on__date=today)
	context = {
		'branch_staff' : branch_staff,
		'cafe_branch' : cafe_branch,
		'orders' : orders
	}

	return render(request, 'home/manage/dashboard.html', context)


@login_required(login_url='/signin/')
def order(request, cart_number):
	if not request.user.is_staff:
		return HttpResponse('<h1 align="center">404</h1>')
	try:
		order = Order.objects.get(cart_number=cart_number)
		branch = CafeBranch.objects.get(id=order.branch_id)
		query = BranchStaff.objects.filter(branch=branch, staff=request.user).first()
		item_list = OrderCart.objects.filter(cart_number=cart_number)
		if query is None:
			return HttpResponse('<h1 align="center">404</h1>')

		if request.method == 'POST':
			order.delivered = True
			order.save()
			return redirect('/dashboard/')
		context = {
			'order' : order,
			'item_list' : item_list
		}
		return render(request, 'home/manage/order.html', context)
	except ObjectDoesNotExist as e:
		return HttpResponse('<h1 align="center">404</h1>')


@login_required(login_url='/signin/')
def branch_time_update(request, uid, name):
	if not request.user.is_staff:
		return HttpResponse('<h1 align="center">404</h1>')
	try:
		cafe_branch = CafeBranch.objects.get(id=uid, name__iexact=name)
		if request.user != cafe_branch.manager:
			return HttpResponse('<h1 align="center">404</h1>')
		if request.method == 'POST':
			form = CafeBranchUpdateForm(request.POST, cafe_branch=cafe_branch)
			if form.is_valid():
				form.save()
				return redirect('/dashboard/')
		else:
			form = CafeBranchUpdateForm(cafe_branch=cafe_branch)
		context = {
			'form' : form
		}
		return render(request, 'home/manage/branch_time_update.html', context)
	except ObjectDoesNotExist as e:
		pass
	return HttpResponse('<h1 align="center">404</h1>')


@login_required(login_url='/signin/')
def branch_food_update(request, uid, name):
	if not request.user.is_staff:
		return HttpResponse('<h1 align="center">404</h1>')
	try:
		cafe_branch = CafeBranch.objects.get(id=uid, name__iexact=name)
		if request.user != cafe_branch.manager:
			return HttpResponse('<h1 align="center">404</h1>')

		if request.method == 'GET':
			req = request.GET.get('req', None)
			food_id = request.GET.get('food_id', None)
			if req is not None and food_id is not None:
				req = req.lower()
				food_id = int(food_id)
				if req == 'add':
					return __add_food_to_branch(food_id, cafe_branch)
				elif req == 'rem':
					return __remove_food_from_branch(food_id, cafe_branch)

		current_food_list = BranchFood.objects.only('food').filter(branch=cafe_branch)
		available_food_list = FoodItem.objects.all().exclude(id__in=current_food_list.values('id'))
		context = {
			'current_food_list' : current_food_list,
			'available_food_list' : available_food_list
		}
		return render(request, 'home/manage/branch_food_update.html', context)
	except ObjectDoesNotExist as e:
		pass
	return HttpResponse('<h1 align="center">404</h1>')



def __add_food_to_branch(food_id, cafe_branch):
	query = BranchFood.objects.filter(branch=cafe_branch, food_id=food_id)
	if not query.exists():
		try:
			food = FoodItem.objects.get(id=food_id)
			BranchFood.objects.create(branch=cafe_branch, food=food)
		except ObjectDoesNotExist as e:
			pass
	return redirect('/branch/'+str(cafe_branch.id)+'/'+cafe_branch.name+'/update/food/')


def __remove_food_from_branch(food_id, cafe_branch):
	query = BranchFood.objects.filter(branch=cafe_branch, food_id=food_id)
	if query.exists():
		query.delete()
	return redirect('/branch/'+str(cafe_branch.id)+'/'+cafe_branch.name+'/update/food/')
