from django import forms
from accounts.models import Custom_user


class CreateUserForm(forms.ModelForm):
	identifier = forms.CharField(max_length=254, widget=forms.TextInput
								(attrs={'placeholder': 'Email or Phone Number',
										'class': 'input100', 'required': ''}))
	dob = forms.DateField(widget=forms.DateInput
						  (attrs={'placeholder': 'Date of birth - MM/DD/YY',
						  		  'class': 'input100', 'required': ''}))
	password = forms.CharField(max_length=254, widget=forms.PasswordInput
							   (attrs={'placeholder': 'Password',
							   	'class': 'input100'}))
	# password1 = forms.CharField(max_length=254, widget=forms.PasswordInput
	# 							(attrs={'placeholder': 'Confirm Password',
	# 							 'class': 'input100'}))
	class Meta:
		model = Custom_user
		fields = ['identifier', 'dob', 'password']
		# fields = '__all__'