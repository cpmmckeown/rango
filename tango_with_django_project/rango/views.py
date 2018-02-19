from django.http import HttpResponse
from rango.forms import CategoryForm, PageForm
from django.shortcuts import render 
from rango.models import Category
from rango.models import Page


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
	return render(request, 'rango/index.html', context_dict)
	
def about(request):
	return render(request, 'rango/about.html')
	
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
	
