
from django.urls import path
from . import views

app_name = 'videoShortsApp'

urlpatterns = [
	path('search', views.searchBarView, name='search'),
	path('videoShortsCategory/', views.videoShortsCategoryOptionsView, name='videoShortsCategoryOptionsUrl'),
	path('videoShortsSubCategory/', views.videoShortsSubCategoryOptionsView, name='videoShortsSubCategoryOptionsUrl'),
	path('videosShorts/', views.blogVideosShortsView, name='blogVideosShortsUrl'),
	path('videosShortsDetailed/', views.blogVideosShortsDetailedView, name='blogVideosShortsDetailedUrl'),	
	path('deleteFKdata', views.deleteFKdataView, name='deleteFKdataUrl'),
	path('tag/<slug:slug>', views.tagBasedVideosShortsView, name='tagBasedVideosShortsUrl'),
	path('shortsHeading', views.shortsHeadingDMView, name="shortsHeadingDMUrl"),
	path('', views.shortsListView, name='shortsListUrl'),
	path('blogShortsDM/', views.blogShortsDMView, name='blogShortsDMURL'),
	path('<slug>', views.shortsDetailView, name="shortsDetailUrl"),
	path('shortsListViewdata/', views.shortsListViewAPIViews.as_view(),name = 'shortsListViewdata'),
]

