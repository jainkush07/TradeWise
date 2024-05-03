from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include, re_path
from stockApp.views import deleteFKdataView, exporttoCSV, importFromCSV, adsenseTextView, render404Page
from django.contrib.sitemaps import views as siteMapViews
from websiteApp.views import robotsTextView
from blogHomeApp.views import searchBarView, tagBasedSearchView
from .sitemap import *

researchReportSiteMaps = {
	researchReportMap.name: researchReportMap,
}

blogSiteMaps = {
	videoBlogMap.name: videoBlogMap,
	videoShortsBlogMap.name: videoShortsBlogMap,
	articleBlogMap.name : articleBlogMap,
	newsBlogMap.name: newsBlogMap,
	newsWebBlogMap.name: newsWebBlogMap,
		
}

staticSiteMaps = {
	websiteStaticSiteMap.name : websiteStaticSiteMap,
}

sitemaps = {**staticSiteMaps, **researchReportSiteMaps, **blogSiteMaps}

urlpatterns = [
	path('ads.txt', adsenseTextView, name="adsenseTextUrl"),
	path('robots.txt', robotsTextView, name='robotsUrl'),
	path('whatsapp/', include('whatsappAuthApp.urls', namespace="whatsappAuthApp")),
	path('excel-utility/', include('excelUtilityApp.urls', namespace="excelUtilityApp")),
	path('', include('productPagesApp.urls', namespace='productPagesApp')),
	path('video/', include('videoBlogApp.urls', namespace='videoBlogApp')),
	path('article-blog/', include('articleBlogApp.urls', namespace='articleBlogApp')),
	path('media-coverage/', include('mediaBlogApp.urls', namespace='mediaBlogApp')),
	path('video-shorts/', include('videoShortsApp.urls', namespace='videoShortsApp')),
	path('blog/', include('blogHomeApp.urls', namespace='blogHomeApp')),
	path('employee/', include('employeeApp.urls', namespace='employeeApp')),
	path('research-report/', include('stockApp.urls', namespace='stockApp')),
	path('pg-integration/', include('cartApp.urls', namespace='cartApp')),
	path('stock-price-api-v1/', include('stockPriceApp.urls', namespace='stockPriceApp')),
	path('forms-submit-api-v1/', include('dmFormsApp.urls', namespace='dmFormsApp')),
	path('utilities/', include('utilityApp.urls', namespace='utilityApp')),
	path('summernote/', include('django_summernote.urls')),	
	path('deleteFKdata', deleteFKdataView, name='deleteFKdataUrl'),
	path('exportData', exporttoCSV, name="exportDataUrl"),
	path('importData', importFromCSV, name="importDataUrl"),
	path('social-auth/',include('social_django.urls', namespace='social')),
	path('sitemap.xml', siteMapViews.index, {'sitemaps': sitemaps}, name='sitemap-index'),
	path('sitemap-<section>.xml', siteMapViews.sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
	path('admin/', admin.site.urls),
	path('auth-ols/', include('authApp.urls', namespace='authApp')),
	path('auth/', include('authNewApp.urls', namespace='authNewApp')),
	path('investor/', include('investorApp.urls', namespace='investorApp')),
	path('404', render404Page, name="render404PageUrl"),
	path('manage-broken-link/', include('brokenRedirectApp.urls', namespace="brokenRedirectApp")),
	path('search/', searchBarView, name='contentSearch'),
	path('tag/<slug:tag_slug>', tagBasedSearchView, name='tagSearch'),
	# path('accounts/', include('allauth.urls', namespace='social-logins')),
	# // not on PROD
	re_path(r'^taggit_autosuggest/', include('taggit_autosuggest.urls')),
	re_path(r'^admin/django-ses/', include('django_ses.urls')),
	path('', include('websiteApp.urls', namespace='websiteApp')),
	path('', include('newsBlogApp.urls', namespace='newsBlogApp')),
	# not on PROD
	path('', include('staticPagesSlugApp.urls', namespace='staticPagesSlugApp')),
	# // not on PROD
]
if settings.DEBUG:
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
	urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
