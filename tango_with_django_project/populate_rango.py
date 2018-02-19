import os
import random
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
						'tango_with_django_project.settings')
						
import django
django.setup()
from rango.models import Category, Page

def populate():
	#1st, create lists of dictionaries, containing pages
	#we desire to add to each cat.
	#create dictionary of dictionaries for cats
	
	python_pages = [
		{"title": "Official Python Tutorial",
		"url": "https://docs.python.org/2/tutorial/"},
		{"title":"How to Think like a Computer Scientist",
		"url":"http://www.greenteapress.com/thinkpython/"},
		{"title":"Learn Python in 10 Minutes",
		"url":"https://www.korokithakis.net/tutorials/python/"} ]
		
	django_pages = [
		{"title":"Official Django Tutorial",
		"url":"https://docs.djangoproject.com/en/1.9/intro/tutorial01/"},
		{"title":"Django Rocks",
		"url":"https://www.djangorocks.com/"},
		{"title":"How to Tango with Django",
		"url":"https://www.tangowithdjango.com/"} ]
		
	other_pages = [
		{"title":"Bottle",
		"url":"https://bottlepy.org/docs/dev/"},
		{"title":"Flask",
		"url":"http://flask.pocoo.org"} ]
		
	cats = {"Python": {"pages": python_pages},
			"Django": {"pages": django_pages},
			"Other Frameworks": {"pages": other_pages} }
			
# If you want to add more categories or pages
# add them to the dictionaries above. 
# The code below goes through the cats dictionary, then adds each category, 
# and then adds all the associated pages for that category. 
# if you are using Python 2.x then use cats.iteritems() see 
# http://docs.quantifiedcode.com/python-anti-patterns/readability/ 
# for more information about how to iterate over a dictionary properly.

	for cat, cat_data in cats.items():
		c = add_cat(cat)
		for p in cat_data["pages"]:
			add_page(c, p["title"], p["url"])
			
	#Print out the cats we've added.
	for c in Category.objects.all():
		for p in Page.objects.filter(category=c):
			print("- {0} - {1}".format(str(c), str(p)))
			
def add_page(cat, title, url, views=0):
	p = Page.objects.get_or_create(category=cat, title=title)[0]
	p.url=url
	p.views= random.randint(1,128)
	p.save()
	return p
	
def add_cat(name):
	c = Category.objects.get_or_create(name=name)[0]
	if c.name == "Python":
		c.views = 128
		c.likes = 64
	else:
		if c.name == "Django":
			c.views = 64
			c.likes = 32
		else:
			c.views = random.randint(1,128)
			c.likes = random.randint(1,128)
	
		
	c.save()
	return c
	
#start execution here!
if __name__ == '__main__':
	print("Starting Rango population script...")
	populate()