from django.conf.urls import url
from rango import views

urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^about/$', views.about, name='about'),
	url(r'^add_category/$', views.add_category, name='add_category'),
	# These are the add page and add category URL patterns
	# these are in a different order than the text book
	# but seem to work. 
	url(r'^category/(?P<category_name_slug>[\w\-]+)/add_page/$', 
		views.add_page, 
		name='add_page'),
	url(r'^category/(?P<category_name_slug>[\w\-]+)/$', 
		views.show_category, 
		name='show_category'),
	#This is the register URL pattern from chapter 9. 
	url(r'^register/$',
		views.register,
		name='register'),
	#login from chpt 9
	url(r'^login/$', views.user_login, name='login'),
	url(r'^restricted/', views.restricted, name='restricted'),
	url(r'^logout/$', views.user_logout, name='logout'), 
]
