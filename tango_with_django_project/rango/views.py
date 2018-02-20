from rango.forms import CategoryForm, PageForm
from django.shortcuts import render 
from rango.models import Category
from rango.models import Page
from rango.forms import UserForm, UserProfileForm 
from django.contrib.auth import authenticate, login 
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse 
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout  


def index(request):
	#query database for list of all categories currently stored.
	#order cats by no. of likes in DESCENDING order
	#retrieve top 5 only or all if less than 5
	#place list in context_dict
	#that will be passed to template engine
	category_list = Category.objects.order_by('-likes')[:5]
	pages_list = Page.objects.order_by('-views')[:5]
	context_dict = {'categories': category_list, 'pages': pages_list}
	
	#Render response, send it back
	response = render(request, 'rango/index.html', context=context_dict)
	return response
	
def about(request):
	return render(request, 'rango/about.html', {}) 
	# The '{}' at the end is an empty dictionary because we have 
	# no additional data to give the template.
	# p. 106. 
	
#adding in the definition for the form from chapter 7
def add_category(request):
	form = CategoryForm()
	
	#Check to see if something is a HTTP post. If it is...
	if request.method == 'POST':
		form = CategoryForm(request.POST)
		
		# Check to see if 'we' have been provided with a valid form.
		if form.is_valid():
			#If it's valid, save the new category to the DBase
			form.save(commit=True)
			#With the new Cat saved, we could give a conf request 
			#but sending the user back to the index page 
			#is better
			return index(request)
			#just in case something goes wrong though...
			#we print a wrong form in the terminal.
			
		else: 
			print(form.errors)
	return render(request, 'rango/add_category.html', {'form': form})
		#finally, this handles the form (or no form) and generates 
		#a suitable view with error messages, if any.
			
def add_page(request, category_name_slug):
    try:
        category = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        category = None

    form = PageForm()
    if request.method == 'POST':
        form = PageForm(request.POST)
        if form.is_valid():
            if category:
                page = form.save(commit=False)
                page.category = category
                page.views = 0
                page.save()
                # probably better to use a redirect here.
            return show_category(request, category_name_slug)
        else:
            print(form.errors)

    context_dict = {'form':form, 'category': category}

    return render(request, 'rango/add_page.html', context_dict)
	
def show_category(request, category_name_slug):
	context_dict = {}
	
	try:
		category = Category.objects.get(slug=category_name_slug)
		
		pages = Page.objects.filter(category=category)
		
		context_dict['pages'] = pages
		
		context_dict['category'] = category
	except Category.DoesNotExist:
		context_dict['category'] = None
		context_dict['pages'] = None
		
	return render(request, 'rango/category.html', context_dict)
	
def register(request):
#A boolean value telling template whether reg. was success
#set false orig. code change value to true when reg. succeed
	registered = False
	
	#if HTTP POST, we process form data
	if request.method == 'POST':
		#try to grab info from raw form info
		#note: use of USERFORM and USERPROFILEFORM
		user_form = UserForm(data=request.POST)
		profile_form = UserProfileForm(data=request.POST)

		#if BOTH forms are valid...
		if user_form.is_valid() and profile_form.is_valid():
			user = user_form.save()
			
			#Now hash the password with the set_password method
			#once hashed update user object
			user.set_password(user.password)
			user.save()
			
			#now sort the USerProfile instance
			#need to set the user attribute ourselves,
			#set commit=False. This delays
			#saving the model until we're ready.
			#this avoids integrity problems.
			profile = profile_form.save(commit=False)
			#After creating a new User model instance
			#we reference it in the UserProfile instance
			#with the line below:
			profile.user = user
			#This is where we populate the user attribute
			#of the UserProfile form, 
			#which we hid from users.
			
			#check if user provided picture
			#if so get it from input form
			#put it in UserProfile model
			if 'picture' in request.FILES:
				profile.picture = request.FILES['picture']
				
			#save the UserProfile model instance
			profile.save()
				
			#update variable to indicate the the template reg.
			#was successful.
			registered = True
		else:
			#invalid form - print to terminal
			print(user_form.errors, profile_form.errors)
	else:
	# not HTTP POST, render our form using 
	#two model form instances
	#these will be blank ready for 
	#user input... huh... what does that mean???
		user_form = UserForm()
		profile_form = UserProfileForm()
	#render the template depending on context.
	return render(request,
			'rango/register.html',
			{'user_form': user_form,
			'profile_form': profile_form,
			'registered': registered})
	
def user_login(request):
	#if the request is HHTP POST try to extract relevant info
	if request.method == 'POST':
		#get username + password provided
		#this info obtained via login form
		#use request.POST.get('<variable>') as 
		# opposed request.POST.['<variable>'] because
		# the request.POST.get('<variable>') returns 
		# NONE if the value does not exist while reuqest.POST['<variable>']
		#will raise a KeyError exception
		username = request.POST.get('username')
		password = request.POST.get('password')
		
		#use Django's internals to see if usernm/psswrd combo
		#is valid
		user = authenticate(username=username, password=password)
		
		#if...
		if user:
			if user.is_active:
				login(request, user)
				return HttpResponseRedirect(reverse('index'))
			else:
				return HttpResponse("Your Rango account is disabled.")
		else:
			print("Invalid login details: {0}, {1}".format(username, password))
			return HttpResponse("Invalid login details supplied.")
			
	# The request is not a HTTP POST so display the login form
	else:
		return render(request, 'rango/login.html', {})
		
@login_required 
def restricted(request): 
	return render(request, 'rango/restricted.html') 
	
@login_required 
def user_logout(request): 
# Since we know the user is logged in, we can now just log them out. logout(request) 
# Take the user back to the homepage. 
	return HttpResponseRedirect(reverse('index')) 
		
		
