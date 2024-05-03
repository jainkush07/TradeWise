from django.urls import path, reverse_lazy
from django.views.generic.base import RedirectView
from . import views

app_name = 'newsBlogApp'

urlpatterns = [
	path('search/', views.searchBarView, name='search'),
	path('planify-news/', views.crawledNewsView, name='crawledNewsUrl'),	
	path('blogNews', views.blogNewsView, name='blogNewsUrl'),
	path('deleteFKdata', views.deleteFKdataView, name='deleteFKdataUrl'),	
	path('blogNewsListingDM/', views.blogNewsDMView, name='blogNewsListingDMURL'),
	path('newsHeading', views.newsHeadingDMView, name="newsHeadingDMUrl"),
	path('newsHeadingWeb', views.newsWebHeadingDMView, name="newsWebHeadingDMUrl"),
	path('planify-feed/', views.newsListView, name='newsListUrl'),
	path('planify-feed/<slug>', views.newsDetailView, name="newsDetailURL"),
	path('', RedirectView.as_view(url=reverse_lazy('newsBlogApp:newsListUrl'), permanent=True), name='newsRedirectUrl'),
	path('newsfeedListApi/',views.newsfeedListApiView.as_view(),name='allnewsfeedListApi'),
	path('crawledNewsViews/', views.crawledNewsViewAPIViews.as_view(), name="crawledNewsViews"),
	path('feedDescription/<int:pk>', views.feedDescriptionApiView.as_view(), name="feedDescription"),
]
