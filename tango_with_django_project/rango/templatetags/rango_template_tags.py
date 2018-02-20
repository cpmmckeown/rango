from django import template 
from rango.models import Category 

register = template.Library() 

@register.inclusion_tag('rango/cats.html') 
def get_category_list(cat=None): 
	return {'cats': Category.objects.all(),
	'act_cat': cat} 
	
	#Note : the inclusion of the cat parameter
	#to the get_category_list() which is optional
	# ...but what does act_cat do???
	# ah! act_cat will be = none... if there is none. 
