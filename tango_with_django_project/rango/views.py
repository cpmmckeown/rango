from django.http import HttpResponse
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