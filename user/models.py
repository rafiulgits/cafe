from django.contrib.auth.models import (
	AbstractBaseUser, BaseUserManager,PermissionsMixin, 
	_user_has_module_perms, _user_has_perm, _user_get_all_permissions)
from django.db import models


_GENDER = (
	('F', 'Female'),
	('M', 'Male'),
	('O', 'Other'),
	('*', 'Not to say'),
)

_USER_TYPE = (
	('DB', 'Director of the Board'),
	('BM', 'Board Member'),
	('CM', 'Cafe Manager'),
	('CF', 'Cafe Staff'),
	('US', 'UTas Student'),
	('UE', 'UTas Employee')
)


class UserManager(BaseUserManager):
	"""
	Doc here
	"""
	def create_user(self, userid, name, phone, email, gender, card, password=None, is_staff=False, is_superuser=False):

		if not userid or not name or not email or not phone:
			raise ValueError('name, userid, email, phone required')

		if not password:
			raise ValueError('password required')

		if not card:
			raise ValueError('Card number required')


		user = self.model(userid=userid, name=name, phone=phone, email=email, gender=gender, card=card)
		user.is_staff = is_staff
		user.is_superuser = is_superuser
		user.set_password(password)
		user.save()

		return user


	def create_staffuser(self, userid, name, phone, email, gender, card, password=None):
		user = self.create_user(userid, name, phone, email, gender, card, password, True, False)
		return user


	def create_superuser(self, userid, name, phone, email, gender, card, password=None):
		user = self.create_user(userid, name, phone, email, gender, card, password, True, True)



class Account(AbstractBaseUser,PermissionsMixin):
	"""
	Doc here
	"""
	userid = models.CharField(max_length=6, unique=True)
	name = models.CharField(max_length=80)
	phone = models.CharField(max_length=16, unique=True)
	email = models.EmailField(max_length=45, unique=True)
	gender = models.CharField(max_length=1, choices=_GENDER)
	card = models.CharField(max_length=16)
	balance = models.FloatField(default=0)
	image = models.ImageField(upload_to='image/user/', null=True, blank=True)
	
	is_active = models.BooleanField(default=True)
	is_staff = models.BooleanField(default=False)
	is_superuser = models.BooleanField(default=False)

	USERNAME_FIELD = 'userid'
	REQUIRED_FIELDS = ['name', 'phone', 'email', 'gender', 'card']

	objects = UserManager()

	def __str__(self):
		return self.name + ': '+self.phone

	def get_username(self):
		return self.phone


	def has_perm(self, perm, obj=None):
		if self.is_superuser:
			return True
		return False


	def has_module_perm(self, app_label):
		if self.is_superuser:
			return True
		return False

	def has_module_perms(self, perms, obj=None):
		return all(self.has_perm(perm, obj) for perm in perms)