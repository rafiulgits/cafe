from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist

from home.cart import Cart,CartItem
from home.models import CafeBranch, BranchFood, OrderCart, Order, BranchStaff

from generic.helper import random_string
from generic.period import available, all_slots

from re import split
from datetime import time

def index(request):
	branch_list = CafeBranch.objects.all()
	context = {
		'branch_list' : branch_list
	}
	return render(request, 'home/basic/index.html', context)


@login_required(login_url='/signin/')
def branch(request, uid, name):
	try:
		cafe_branch = CafeBranch.objects.get(id=uid, name__iexact=name)
		food_list = BranchFood.objects.filter(branch=cafe_branch)
		context = {
			'cafe_branch' : cafe_branch,
			'food_list' : food_list
		}
		return render(request, 'home/basic/branch.html', context)
	except ObjectDoesNotExist as e:
		return HttpResponse('<h1 align="center">404</h1>')


@login_required(login_url='/signin/')
def cart(request):
	cart = Cart(request)
	item_list, total = Cart(request).get_items()
	if len(item_list) == 0:
		context = {
			'has_items' : False
		}
	else:
		cafe_branch_id = cart.get_branch_id()
		cafe_branch = CafeBranch.objects.get(id=cafe_branch_id)
		time_slots = available(cafe_branch)
		print(time_slots)
		context = {
			'has_items' : True,
			'item_list' : item_list,
			'total' : total,
			'time_slots' : time_slots,
		}

	return render(request, 'home/basic/cart.html', context)


@login_required(login_url='/signin/')
def add_cart(request):
	if request.method != 'GET':
		return HttpResponse('<h1 align="center">404</h1>')
	branch_food_id = request.GET.get('branch_food_id', None)
	branch_id = request.GET.get('branch_id', None)
	if not branch_food_id:
		return HttpResponse('invalid')
	if not branch_id:
		return HttpResponse('invalid')
	try:
		branch_food = BranchFood.objects.get(id=branch_food_id)
		cart = Cart(request)
		if cart.get_branch_id() is None:
			cart.set_branch_id(branch_id)
			cart.add(branch_food.id)
		elif cart.get_branch_id() == branch_id:
			cart.add(branch_food.id)
		else:
			cart.clear()
			cart = Cart(request)
			cart.set_branch_id(branch_id)
			cart.add(branch_food.id)
		return HttpResponse('Ok')
	except ObjectDoesNotExist as e:
		return HttpResponse('invalid')


@login_required(login_url='/signin/')
def cart_checkout(request):
	if request.method != 'POST':
		return HttpResponse('<h1 align="center">404</h1>')
	cart = Cart(request)
	item_list, total = cart.get_items()
	if len(item_list) == 0:
		return HttpResponse('<h1 align="center">No item in cart</h1>')
	if total > request.user.balance:
		return HttpResponse('<h1 align="center">Not enough balance available</h1>')

	collection_time_str = request.POST.get('collection_time')
	split_list = split('[: ]', collection_time_str)
	if split_list[2].lower() == 'p.m.':
		hour = int(split_list[0])+12
		if hour == 24:
			hour = 0
		collection_time = time(hour, int(split_list[1]))
	else:
		collection_time = time(int(split_list[0]), int(split_list[1]))
	cart_number = random_string(size=6)
	while Order.objects.filter(cart_number=cart_number).exists():
		cart_number = random_string(size=6)

	for item in item_list:
		OrderCart.objects.create(
			branch_food = item.branch_food,
			quantity = item.quantity,
			price = item.branch_food.food.price,
			sub_total = item.sub_total,
			cart_number = cart_number
		)

	branch_id = cart.get_branch_id()
	order = Order.objects.create(
		user = request.user,
		cart_number = cart_number,
		total = total,
		branch_id = branch_id,
		collection_time=collection_time
	)

	cart.clear()
	request.user.balance -= total
	request.user.save()

	context = {
		'order' : order
	}

	return render(request,'home/basic/checkout.html',context)


@login_required(login_url='/signin/')
def update_cart(request):
	if request.method != 'GET':
		return HttpResponse('<h1 align="center">404</h1>')
	op = request.GET.get('op', None)
	branch_food_id = request.GET.get('branch_food_id', None)
	if op is None or branch_food_id is None:
		return HttpResponse('<h1 align="center">404</h1>')
	op = op.lower()
	if op == 'add':
		Cart(request).add(branch_food_id)	
	elif op == 'rem':
		Cart(request).remove(branch_food_id)
	return redirect('/cart/')


@login_required(login_url='/signin/')
def my_orders(request):
	orders = Order.objects.filter(user=request.user).order_by('-request_on')
	context = {'orders':orders}
	return render(request, 'home/basic/my_orders.html', context)