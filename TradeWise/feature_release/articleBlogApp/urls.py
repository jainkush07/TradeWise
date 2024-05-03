from django.urls import path
from . import views

app_name = 'articleBlogApp'

urlpatterns = [
    path('article-by-author/<slug>', views.articlesListView, name='articlesListByAuthorURL'),
    path('article-detail/<slug>', views.articleDetailView, name="articleDetailURL"),
    path('articleTagsOptions/', views.articleTagsOptionsView, name='articleTagsOptionsURL'),
    path('categoryOptions/', views.categoryOptionsView, name='categoryOptionsURL'),
    path('subCategoryOptions/', views.subCategoryOptionsView, name='subCategoryOptionsURL'),
    path('articleDM', views.articleDMView, name="articleDMUrl"),
    path('deleteFKdata', views.deleteFKdataView, name='deleteFKdataUrl'),
    path('blogArticles', views.blogArticlesView, name="blogArticlesURL"),
    path('blogArticle', views.blogArticlesDetailedView, name="blogArticlesDetailedURL"),
    path('search', views.searchView, name="searchURL"),
    path('', views.articlesListView, name='articlesListURL'),
    path('articles/', views.ArticleListView.as_view(), name='article_list_view'),
    path('articleListApi/<str:pk>/', views.ArticleDataView.as_view(), name='article_view'),
	path('articleListApi/',views.newArticleListApiView.as_view(),name='newArticleListApiView'),
	path('articleDetailViewsCount/',views.articleDetailViewsCount,name='articleDetailViewsCount'),
]
