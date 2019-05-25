from django import forms
from django.contrib.auth import authenticate
from user.models import Account

_USER_TYPE = (
	('DB', 'Director of the Board'),
	('BM', 'Board Member'),
	('CM', 'Cafe Manager'),
	('CS', 'Cafe Staff'),
	('US', 'UTas Student'),
	('UE', 'UTas Employee')
)


class SignupForm(forms.ModelForm):
	password = forms.CharField(widget=forms.PasswordInput(attrs=
		{'placeholder' : 'Password (min 6 length)', 'class' : 'form-control', 
		'minLength': '6', 'maxLength':'12'}))
	confirm_password = forms.CharField(widget=forms.PasswordInput(attrs=
		{'placeholder' : 'Confirm Password', 'class' : 'form-control'}))
	user_type = forms.CharField(widget=forms.Select(choices=_USER_TYPE, attrs={'class':'custom-select'}))
	id_number = forms.CharField(max_length=4, widget=forms.TextInput(
		attrs={'placeholder': 'XXXX format','class':'form-control'}))

	class Meta:
		model = Account
		fields = ['name', 'phone', 'email', 'gender', 'card', 'image']

		widgets = {
			'name' : forms.TextInput(attrs={'class':'form-control'}),
			'phone' : forms.TextInput(attrs={'class':'form-control'}),
			'email' : forms.EmailInput(attrs={'class':'form-control'}),
			'card' : forms.TextInput(attrs={'class':'form-control'}),
			'gender' :forms.Select(attrs={'class':'custom-select'}),
			'image' : forms.FileInput(attrs={'class':'form-control'})
		}


	def clean_id_number(self):
		id_number = self.cleaned_data['id_number']
		user_type = self.cleaned_data['user_type']
		userid = user_type+id_number
		query = Account.objects.filter(userid=userid)
		if query.exists():
			raise forms.ValidationError('ID already registered')
		return id_number

	def phone(self):
		phone = self.cleaned_data['phone']
		query = Account.objects.filter(phone=phone)
		if query.exists():
			raise forms.ValidationError('phone already registered')
		return phone

	def email(self):
		email = self.cleaned_data['email']
		query = Account.objects.filter(email=email)
		if query.exists():
			raise forms.ValidationError('email already registered')
		return email

	def clean_confirm_password(self):
		password = self.cleaned_data['password']
		confirm_password = self.cleaned_data['confirm_password']
		if len(password) < 6:
			raise forms.ValidationError('password should be at least 6 length')
		if len(password) > 12:
			raise forms.ValidationError('password should be at most 12 length')
		if not any(char.isdigit() for char in password):
			raise forms.ValidationError('password must contain at least 1 digit')
		if not any(char.isupper() for char in password):
			raise forms.ValidationError('password must contain at least 1 upper letter')
		if not any(char.islower() for char in password):
			raise forms.ValidationError('password must contain at least 1 upper letter')
		if not any(symbol in password for symbol in ['~','!','#','$']):
			raise forms.ValidationError("use any of '~','!','#','$'")
		if not password or not confirm_password or password != confirm_password:
			raise forms.ValidationError('passwords are not matched')
		return confirm_password

	def save(self, commit=True):
		user = Account(
			userid = self.cleaned_data['user_type']+self.cleaned_data['id_number'],
			phone = self.cleaned_data['phone'],
			email = self.cleaned_data['email'],
			gender = self.cleaned_data['gender'],
			card = self.cleaned_data['card'],
			name = self.cleaned_data['name'],
			image = self.cleaned_data['image'],
			)
		user.set_password(self.cleaned_data['confirm_password'])
		if commit:
			user.save()
		return user


class SigninForm(forms.Form):
	userid = forms.CharField(max_length=6, widget=forms.TextInput(attrs={'class':'form-control'}))
	password = forms.CharField(max_length=12, min_length=6, widget=forms.PasswordInput(
		attrs={'class':'custom-select'}))

	def clean(self):
		cleaned_data = self.cleaned_data
		userid = cleaned_data['userid']
		password = cleaned_data['password']

		user = authenticate(userid=userid, password=password)
		if user:
			self.user = user
			return cleaned_data
		raise forms.ValidationError('invalid information')



class PasswordChangeForm(forms.Form):

	current_password = forms.CharField(widget=forms.PasswordInput(attrs=
		{'placeholder' : 'Current Password', 'class' : 'form-control'}))
	new_password = forms.CharField(widget=forms.PasswordInput(attrs=
		{'placeholder' : 'New Password', 'class' : 'form-control', 'minLength':'6'}))
	confirm_password = forms.CharField(widget=forms.PasswordInput(attrs=
		{'placeholder' : 'Confirm Password', 'class' : 'form-control'}))

	def clean_current_password(self):
		current_password = self.cleaned_data['current_password']
		isvalid = self.user.check_password(current_password)
		if not isvalid:
			raise forms.ValidationError('invalid password')
		return current_password

	def clean_confirm_password(self):
		password = self.cleaned_data['new_password']
		confirm_password = self.cleaned_data['confirm_password']
		if len(password) < 6:
			raise forms.ValidationError('password should be at least 6 length')
		if len(password) > 12:
			raise forms.ValidationError('password should be at most 12 length')
		if not any(char.isdigit() for char in password):
			raise forms.ValidationError('password must contain at least 1 digit')
		if not any(char.isupper() for char in password):
			raise forms.ValidationError('password must contain at least 1 upper letter')
		if not any(char.islower() for char in password):
			raise forms.ValidationError('password must contain at least 1 upper letter')
		if not any(symbol in password for symbol in ['~','!','#','$']):
			raise forms.ValidationError("use any of '~','!','#','$'")
		if not password or not confirm_password or password != confirm_password:
			raise forms.ValidationError('passwords are not matched')
		return confirm_password


	def save(self, commit=True):
		new_password = self.cleaned_data['confirm_password']
		self.user.set_password(new_password)
		if commit:
			self.user.save()
		return self.user


	def __init__(self, *args, **kwargs):
		self.user = kwargs.pop('user', None)

		super(PasswordChangeForm, self).__init__(*args, **kwargs)



class ProfileUpdateForm(forms.ModelForm):
	password = forms.CharField(widget=forms.PasswordInput(attrs=
		{'class' : 'form-control', 'placeholder' : 'Your Password'}))

	class Meta:
		model = Account
		fields = ['name','phone', 'email', 'gender']

		widgets = {
			'name' : forms.TextInput(attrs={
				'placeholder' : 'Name', 'class' : 'form-control'
				}),
			'phone' : forms.TextInput(attrs={
				'placeholder' : 'Phone Number', 'class':'form-control'
				}),

			'email' : forms.EmailInput(attrs={
				'placeholder' : 'Email (optional)', 'class' : 'form-control'
				}),

			'gender' : forms.Select(attrs={
				'class' : 'custom-select'
				}),
		}

	def clean(self):
		cleaned_data = self.cleaned_data

		password = cleaned_data['password']
		phone = cleaned_data['phone']
		email = cleaned_data['email']
		gender = cleaned_data['gender']

		valid = self.user.check_password(password)
		if not valid:
			raise forms.ValidationError('invalid password')

		duplicate_email = Account.objects.filter(email=email).exclude(id=self.user.id)
		if duplicate_email.exists():
			raise forms.ValidationError('This email is already registered')

		duplicate_phone = Account.objects.filter(phone=phone).exclude(id=self.user.id)
		if duplicate_phone.exists():
			raise forms.ValidationError('This phone is already registered')

		if gender is None:
			raise forms.ValidationError('set a gender')

		return cleaned_data


	def is_new_email(self):
		if self.user.email.lower() != self.cleaned_data.get('email').lower():
			return True
		return False


	def save(self, commit=True):
		name = self.cleaned_data['name']
		email = self.cleaned_data['email']
		gender = self.cleaned_data['gender']
		phone = self.cleaned_data['phone']
		self.user.name = name
		self.user.phone = phone
		self.user.email = email
		self.user.gender = gender

		if commit:
			self.user.save()
		return self.user


	def __init__(self, *args, **kwargs):
		self.user = kwargs.pop('user', None)

		super(ProfileUpdateForm, self).__init__(*args, **kwargs)		

		self.fields['name'].initial = self.user.name
		self.fields['phone'].initial = self.user.phone
		self.fields['email'].initial = self.user.email
		self.fields['gender'].initial = self.user.gender



class AddMoneyForm(forms.Form):

	money = forms.FloatField(widget=forms.NumberInput(attrs={'class':'form-control'}))

	def __init__(self, *args, **kwargs):
		self.user = kwargs.pop('user', None)
		super(AddMoneyForm, self).__init__(*args, **kwargs)

	def save(self, commit=True):
		self.user.balance += self.cleaned_data['money']
		if commit:
			self.user.save()
		return self.user