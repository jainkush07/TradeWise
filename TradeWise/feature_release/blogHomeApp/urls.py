from django.urls import path
from . import views

app_name = 'blogHomeApp'

urlpatterns = [
	path('search', views.searchBarView, name='search'),
	path('tags/', views.tagsListView, name='tagsListUrl'),
	path('tag-image', views.tagModelView, name='tagModelUrl'),
	path('news-image', views.newsCommonImageHomeModelView, name='newsCommonImageHomeModelUrl'),
	path('category-image', views.categoryImageModelView, name='categoryImageModelUrl'),
	path('categories', views.categoryListView, name='categoryListUrl'),
	path('all-tags/', views.tagBasedListView, name='allTagBasedListUrl'),
	path('tag/<slug:slug>', views.tagBasedListView, name='tagBasedListUrl'),
	path('category/<slug:slug>', views.categoryBasedListView, name='categoryBasedListUrl'),
	path('sub-category/<slug:slug>', views.subCategoryBasedListView, name='subCategoryBasedListUrl'),
	path('homeBlogDM', views.homeBlogDMView, name='homeBlogDMUrl'),
	path('api-v1-search-load-more/', views.search_load_more_view, name="search_load_more_url"),
	path('', views.blogHomeView, name='blogHomeURL'),
	path('searchApi', views.searchBarViewApi, name='searchApi'),
	path('api-v2-search-load-more/', views.search_load_more_view_api, name="search_load_more_api"),
	path('searchSuggestionsApi', views.searchBarSuggestionsApi_01, name='searchSuggestionsApi'),
	path('searchSuggestionsApi/loadSingleObject', views.loadSingleObject, name='loadSingleObject'),
	path('blogPageApiView/', views.blogPageApiView, name='blogPageApiView'),
]
