from django.contrib import admin
from rango.models import Category, Page

class PageAdmin(admin.ModelAdmin):
	list_display = ('title', 'category', 'url')
	
	def __str__(self): # For Python 2, use __unicode__ too 
		return self.title 

# Register your models here.
admin.site.register(Category)
admin.site.register(Page, PageAdmin)

