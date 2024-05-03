from django.urls import path
from .  import views

app_name = 'mediaBlogApp'

urlpatterns = [
	path('search', views.searchBarView, name='search'),
	path('deleteFKdata', views.deleteFKdataView, name='deleteFKdataURL'),	
	path('blog-media', views.blogMediaView, name='blogMediaURL'),
	path('mediaBlogDM', views.mediaBlogDMView, name='mediaBlogDMUrl'),
	path('', views.mediaListView, name='mediaListURL'),
]


