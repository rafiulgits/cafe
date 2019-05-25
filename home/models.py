from django.db import models
from user.models import Account

# Create your models here.

class FoodItem(models.Model):
	name = models.CharField(max_length=50)
	description = models.TextField()
	image = models.ImageField(upload_to='image/food/')
	price = models.FloatField()
	expired_date = models.DateField()

	def __str__(self):
		return self.name


class CafeBranch(models.Model):
	name = models.CharField(max_length=30)
	manager = models.ForeignKey(Account, on_delete=models.CASCADE)
	opening_time = models.TimeField()
	closing_time = models.TimeField()

	def __str__(self):
		return self.name


class BranchFood(models.Model):
	branch = models.ForeignKey(CafeBranch, on_delete=models.CASCADE)
	food = models.ForeignKey(FoodItem, on_delete=models.CASCADE)

	class Meta:
		unique_together = ('branch', 'food')

	def __str__(self):
		return self.branch.name+ ' : '+self.food.name



class BranchStaff(models.Model):
	branch = models.ForeignKey(CafeBranch, on_delete=models.CASCADE)
	staff = models.ForeignKey(Account, on_delete=models.CASCADE)

	def __str__(self):
		return self.staff.name + ' : '+self.branch.name


class OrderCart(models.Model):
	branch_food = models.ForeignKey(BranchFood, on_delete=models.CASCADE)
	quantity = models.PositiveSmallIntegerField()
	price = models.FloatField()
	sub_total = models.PositiveIntegerField()
	cart_number = models.CharField(max_length=6)

	def __str__(self):
		return  str(self.id) + ' : '+self.cart_number


class Order(models.Model):
	user = models.ForeignKey(Account, on_delete=models.CASCADE)
	branch = models.ForeignKey(CafeBranch, on_delete=models.CASCADE)
	cart_number = models.CharField(max_length=6, unique=True)
	total = models.PositiveIntegerField()
	request_on = models.DateTimeField(auto_now_add=True)
	collection_time = models.TimeField()
	delivered = models.BooleanField(default=False)

	def __str__(self):
		return self.cart_number
