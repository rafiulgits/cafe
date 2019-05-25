from django import forms
from home.models import BranchFood, Order, CafeBranch


class CafeBranchUpdateForm(forms.ModelForm):
	class Meta:
		model = CafeBranch
		fields = ['opening_time', 'closing_time']
		widgets = {
			'opening_time' : forms.TimeInput(attrs=
				{'class':'form-control', 'type':'time'}),
			'closing_time' : forms.TimeInput(attrs=
				{'class':'form-control', 'type':'time'}),
		}

	def clean(self):
		cleaned_data = self.cleaned_data
		opening_time = cleaned_data['opening_time']
		closing_time = cleaned_data['closing_time']
		if opening_time >= closing_time:
			raise forms.ValidationError('invalid time period')
		return cleaned_data

	def save(self, commit=True):
		self.cafe_branch.opening_time = self.cleaned_data['opening_time']
		self.cafe_branch.closing_time = self.cleaned_data['closing_time']
		if commit:
			self.cafe_branch.save()
		return self.cafe_branch

	def __init__(self, *args, **kwargs):
		cafe_branch = kwargs.pop('cafe_branch', None)
		self.cafe_branch = cafe_branch
		super(CafeBranchUpdateForm, self).__init__(*args, **kwargs)
		self.fields['opening_time'].initial = self.cafe_branch.opening_time
		self.fields['closing_time'].initial = self.cafe_branch.closing_time