from django import forms
from django.contrib.auth.models import User 
#the user object, 'considered to be the core of the 
#Django authentication system...
from rango.models import Page, Category, UserProfile

class CategoryForm(forms.ModelForm):
	name = forms.CharField(max_length=128,
							help_text="Please enter the category name.")
	views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
	likes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
	slug = forms.CharField(widget=forms.HiddenInput(), required=False) 
	
	# An inline class to provide additional information on the form. 
	class Meta: 
		# Provide an association between the ModelForm and a model 
		model = Category 
		fields = ('name',) 
		
class PageForm(forms.ModelForm): 
	title = forms.CharField(max_length=128, 
								help_text="Please enter the title of the page.")
	url = forms.URLField(max_length=200, 
								help_text="Please enter the URL of the page.") 
	views = forms.IntegerField(widget=forms.HiddenInput(), initial=0) 
		
	class Meta: 
			# Provide an association between the ModelForm and a model 
			model = Page 
			
			#what fields do we want to include in our form?
			#this way we don't need to worry about every field in the model being present/
			#Some fields may allow NULL
			#here we are hiding foreign key
			#we can exlucde the category field from the form
			#exclude = ('category',)
			#or specify the fields to include i.e.
			fields = ('title', 'url', 'views')
			
class UserForm(forms.ModelForm):
	password = forms.CharField(widget=forms.PasswordInput())
	#User models instance contains a password
	#but it would be visible. Updating the password
	#attribute can specify charfield instances to 
	#hide  input
	class Meta:
		model = User
		fields = ('username', 'email', 'password')

			
class UserProfileForm(forms.ModelForm):
	class Meta:
		model = UserProfile
		fields = ('website', 'picture')