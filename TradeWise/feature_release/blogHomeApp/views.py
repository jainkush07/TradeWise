from django.shortcuts import render, HttpResponse, get_object_or_404, redirect
from taggit.models import Tag
from videoBlogApp.models import blogVideos, subCategoryOptions as vidSubCats, categoryOptions as vidCats
from mediaBlogApp.models import blogMedia
from newsBlogApp.models import blogNews 
from videoShortsApp.models import blogVideosShorts, videoShortsCategoryOptions, videoShortsSubCategoryOptions
from articleBlogApp.models import blogArticles, subCategoryOptions, categoryOptions as articlesCat
from django.db import connections
from newsBlogApp.views import dictfetchall
from django.db.models import Q
from django.contrib import messages
from .models import *
from newsBlogApp.models import *
from .forms import *
from .serializers import blogNewsSerializer
from videoShortsApp.forms import blogVideosShortsForm
from stockApp.models import stockBasicDetail
from dmFormsApp.models import metaDetailForDM
from django.http import JsonResponse
from rest_framework.response import Response
from .serializers import *
from rest_framework.decorators import api_view
from websiteApp.serializers import buyPreIPOStockListGETSerializer
from websiteApp.models import buyPreIPOStockList
from stockApp.models import startupCategoryOptions, categoryOptions, stockInvestmentChecklist, stockBasicDetail, \
    stockEssentials
from newsBlogApp.serializers import blogNewsSerializer as newsSerializer
from videoShortsApp.serializers import shortsListSerializer
from videoBlogApp.serializers import blogVideosSerializer as videosSerializer
from articleBlogApp.serializers import BlogArticleSerializer as articleSerializer
import datetime
import threading
from django.contrib.sites.shortcuts import get_current_site

from rest_framework.pagination import PageNumberPagination

@api_view(['GET'])
def tagBasedSearchViewApi(request, tag_slug=None):
	if request.method == 'GET':
		if tag_slug:
			tag = get_object_or_404(Tag, slug=tag_slug)
			tag_detail = {}
			if tag:
				tag_detail = tagSerializer(tag)
				tag_detail = tag_detail.data
			allMetawithThisTag = metaDetailForDM.objects.filter(meta_tags__in=[tag])
			videoSearchObj = []
			shortsSearchObj = []
			researchReportObj = []
			articlesSearchObj = []
			newsSearchObj = []
			mediaSearchObj = []
			staticPagesObj = []
			for item in allMetawithThisTag:
				if item.static_page == 'videoBlog':
					if len(videoSearchObj) < 3:
						if item.video_blog not in videoSearchObj and item.video_blog is not None:
							videoSearchObj.append(item.video_blog)
				elif item.static_page == 'shortsBlog':
					if len(shortsSearchObj) < 6:
						if item.video_shorts_blog not in shortsSearchObj and item.video_shorts_blog is not None:
							shortsSearchObj.append(item.video_shorts_blog)
				elif item.static_page == 'researchReports':
					if len(researchReportObj) < 3:
						if item.research_report not in researchReportObj and item.research_report is not None:
							researchReportObj.append(item.research_report)
				elif item.static_page == 'articleBlog':
					if len(articlesSearchObj) < 3:
						if item.articles_blog not in articlesSearchObj and item.articles_blog is not None:
							articlesSearchObj.append(item.articles_blog)
				elif item.static_page == 'newsBlog':
					if len(newsSearchObj) < 3:
						if item.news_blog not in newsSearchObj and item.news_blog is not None:
							newsSearchObj.append(item.news_blog)
				# elif item.static_page == 'mediaBlog':
				#   if len(mediaSearchObj) < 3:
				#       if item.media_blog not in mediaSearchObj and item.media_blog is not None:
				#           mediaSearchObj.append(item.media_blog)
				else:
					staticPagesObj.append(item)
			if videoSearchObj:
				videoSearchObj = sorted(videoSearchObj, key=lambda x: x.releasedDate, reverse=True)
			if shortsSearchObj:
				shortsSearchObj = sorted(shortsSearchObj, key=lambda x: x.releaseDate, reverse=True)
			if articlesSearchObj:
				articlesSearchObj = sorted(articlesSearchObj, key=lambda x: x.dateForListing, reverse=True)
			if newsSearchObj:
				newsSearchObj = sorted(newsSearchObj, key=lambda x: x.dateOfNews, reverse=True)
			# if mediaSearchObj:
			#   mediaSearchObj = sorted(mediaSearchObj, key=lambda x: x.dateForMediaPost, reverse=True)

		else :
			messages.error(request, 'Invalid Tag, Kindly choose some other for proper information.')
			return redirect('blogHomeApp:blogHomeURL')

		newsSearchObj_list = []
		if newsSearchObj:
			for each in newsSearchObj:
				newsSearchObj_serial = blogNewsSerializer(each)
				data = newsSearchObj_serial.data
				data = data.get("title")
				newsSearchObj_list.append(data)

		# mediaSearchObj_list = []
		# if mediaSearchObj:
		#   for each in mediaSearchObj:
		#       mediaSearchObj_serial = blogNewsSerializer(each)
		#       data = newsSearchObj_serial.data
		#       data = data.get("title")
		#       mediaSearchObj_list.append(data)

		shortsSearchObj_list = []
		if shortsSearchObj:
			for each in shortsSearchObj:
				shortsSearchObj_serial = blogNewsSerializer(each)
				data = shortsSearchObj_serial.data
				data = data.get("title")
				shortsSearchObj_list.append(data)

		videoSearchObj_list = []
		if videoSearchObj:
			for each in videoSearchObj:
				videoSearchObj_serial = blogVideosSerializer(each)
				data = videoSearchObj_serial.data
				data = data.get("title")
				videoSearchObj_list.append(data)

		articlesSearchObj_list = []
		if articlesSearchObj:
			for each in articlesSearchObj:
				articlesSearchObj_serial = blogArticlesSerializer(each)
				data = articlesSearchObj_serial.data
				data = data.get("title")
				articlesSearchObj_list.append(data)

		researchReportObj_list = []
		if researchReportObj:
			for each in researchReportObj:
				researchReportObj_serial = stockBasicDetailSerializer(each)
				data = researchReportObj_serial.data
				data = data.get("seoTitle")
				researchReportObj_list.append(data)

		staticPagesObj_list = []
		if staticPagesObj:
		  for each in staticPagesObj:
			  staticPagesObj_serial = metaDetailForDMSerializer(each)
			  data = staticPagesObj_serial.data
			  data = data.get("static_page")
			  staticPagesObj_list.append(data)
		context = {
			'newsSearchObj':newsSearchObj_list,
			# 'mediaSearchObj':mediaSearchObj,
			'shortsSearchObj': shortsSearchObj_list,
			'videoSearchObj': videoSearchObj_list,
			'articlesSearchObj':articlesSearchObj_list,
			'researchReportObj':researchReportObj_list,
			'staticPagesObj': staticPagesObj_list,
			'query':tag_detail,
		}
		return Response({'response': context})

#
def loadMoreSearchTagView(request):    
	loaded_item = request.GET.get('loaded_item')    
	loaded_item_int = int(loaded_item)    
	limit = 30
	post_obj = list(blogVideosShorts.objects.values() [loaded_item_int:loaded_item_int+limit])    
	data = {'posts': post_obj}    
	return JsonResponse(data=data)

#
def searchBarView(request):
	query = request.GET.get('searchq')
	showLoadMore = True
	newsLoadMore = mediaLoadMore = shortsLoadMore = videoLoadMore = articleLoadMore = rrLoadMore = staticLoadMore = False
	if query:
		newsSearchAllObj = blogNews.objects.filter(
			Q(title__icontains=query) |
			Q(excerptContent__icontains=query) |
			Q(content1__icontains=query) |
			Q(content2__icontains=query) |
			Q(content3__icontains=query) |
			Q(content4__icontains=query) |
			Q(content5__icontains=query)
			).distinct().order_by('-dateOfNews')
		newsCount = newsSearchAllObj.count()
		newsSearchObj = newsSearchAllObj[:2]
		if newsCount > 2:
			newsLoadMore = True

		mediaSearchAllObj = blogMedia.objects.filter(
			Q(title__icontains=query) |
			Q(excerptContent__icontains=query) |
			Q(content2__icontains=query) |
			Q(content3__icontains=query) |
			Q(content4__icontains=query) |
			Q(content5__icontains=query)
			).distinct().order_by('-dateForMediaPost')
		mediaCount = mediaSearchAllObj.count()
		mediaSearchObj = mediaSearchAllObj[:2]
		if mediaCount > 2:
			mediaLoadMore = True

		shortsSearchAllObj = blogVideosShorts.objects.filter(
			Q(title__icontains=query) |
			Q(excerptContent__icontains=query) |
			Q(content1__icontains=query) |
			Q(content2__icontains=query) |
			Q(content3__icontains=query) |
			Q(content4__icontains=query) |
			Q(content5__icontains=query)
			).distinct().order_by('-releaseDate')
		shortsCount = shortsSearchAllObj.count()
		shortsSearchObj = shortsSearchAllObj[:6]
		if shortsCount > 6:
			shortsLoadMore = True

		videoSearchAllObj = blogVideos.objects.filter(
			Q(title__icontains=query) |
			Q(excerptContent__icontains=query) |
			Q(content__icontains=query)
			).distinct().order_by('-releasedDate')
		videoCount = videoSearchAllObj.count()
		videoSearchObj = videoSearchAllObj[:3]
		if videoCount > 3:
			videoLoadMore = True

		articlesSearchAllObj = blogArticles.objects.filter(
			Q(title__icontains=query) |
			Q(excerptContent__icontains=query) |
			Q(content1__icontains=query) |
			Q(content2__icontains=query) |
			Q(content3__icontains=query) |
			Q(content4__icontains=query) |
			Q(content5__icontains=query)
			).distinct().order_by('-dateForListing')
		articleCount = articlesSearchAllObj.count()
		articlesSearchObj = articlesSearchAllObj[:3]
		if articleCount > 3:
			articleLoadMore = True

		researchReportAllObj = stockBasicDetail.objects.filter(status='published').filter(
				Q(stockName__icontains=query) |
				Q(seoTitle__icontains=query) |
				Q(ticker__icontains=query)
			).distinct().order_by('-publish')
		rrCount = researchReportAllObj.count()
		researchReportObj = researchReportAllObj[:3]
		if rrCount > 3:
			rrLoadMore = True

		if not request.GET.get('search') == 'home':
			staticPagesAllObj = metaDetailForDM.objects.filter(
				Q(meta_title__icontains=query) | 
				Q(meta_description__icontains=query) | 
				Q(meta_keywords__icontains=query) | 
				Q(meta_tags__name__icontains=query)
				).exclude(Q(static_page__in=['videoBlog','shortsBlog','articleBlog','newsBlog','researchReports',])).distinct()[:3]
			staticCount = staticPagesAllObj.count()
			staticPagesObj = staticPagesAllObj[:3]
			if staticCount > 3:
				staticLoadMore = True
		else:
			staticPagesObj = None
		with connections['cralwer'].cursor() as cursor:
			status = "'published'"
			if query:
				searchPage = True
				query = query.replace("'", "\\'")
				queryToSearch = "'%"+query+"%'"
				queryToExecute = 'Select * from "crawlApp_googlenewsstore" \
				where status='+status+' AND (title ILIKE E'+queryToSearch+' OR "desc" ILIKE E'+queryToSearch+' OR site ILIKE E'+queryToSearch+') ORDER BY date DESC LIMIT 10;'
			cursor.execute(queryToExecute)
			newsWebObj = dictfetchall(cursor)
	else :
		messages.error(request, 'Enter an Query to Search')
		return redirect('blogHomeApp:blogHomeURL')
	total_video_obj = blogVideos.objects.count()
	context = {
		'newsSearchObj':newsSearchObj,
		'mediaSearchObj':mediaSearchObj,
		'shortsSearchObj':shortsSearchObj,
		'videoSearchObj':videoSearchObj,
		'articlesSearchObj':articlesSearchObj,
		'researchReportObj':researchReportObj,
		'staticPagesObj':staticPagesObj,
		'newsWebObj': newsWebObj,
		'query':query,
		'total_video_obj' : total_video_obj,
		'newsLoadMore': newsLoadMore,
		'mediaLoadMore': mediaLoadMore,
		'shortsLoadMore': shortsLoadMore,
		'videoLoadMore': videoLoadMore,
		'articleLoadMore': articleLoadMore,
		'rrLoadMore': rrLoadMore,
		'staticLoadMore': staticLoadMore,
		'showLoadMore': showLoadMore,
	}
	return render(request, 'blogHome/UI/search.html', context)

#
def search_load_more_view(request):
	offset = request.GET.get('offset')
	query = request.GET.get('query')
	loadFor = request.GET.get('loadFor')
	offset_int = int(offset)
	limit = 30
	if loadFor == 'video':
		querySetLength = blogVideos.objects.filter(Q(title__icontains=query) | 
			Q(excerptContent__icontains=query) | 
			Q(content__icontains=query)
			).distinct().order_by('-releasedDate')
	elif loadFor == 'short':
		querySetLength = blogVideosShorts.objects.filter(
			Q(title__icontains=query)|
			Q(excerptContent__icontains=query) |
			Q(content1__icontains=query) |
			Q(content2__icontains=query) |
			Q(content3__icontains=query) |
			Q(content4__icontains=query) |
			Q(content5__icontains=query)
			).distinct().order_by('-releaseDate')
	elif loadFor == 'researchReport':
		querySetLength = stockBasicDetail.objects.filter(status='published').filter(
				Q(stockName__icontains=query) |
				Q(seoTitle__icontains=query) |
				Q(ticker__icontains=query)
			).distinct().order_by('-publish')
	elif loadFor == 'staticPage':
		querySetLength = metaDetailForDM.objects.filter(
				Q(meta_title__icontains=query) | 
				Q(meta_description__icontains=query) | 
				Q(meta_keywords__icontains=query) | 
				Q(meta_tags__name__icontains=query)
				).exclude(Q(static_page__in=['videoBlog','shortsBlog','articleBlog','newsBlog','researchReports',])).distinct()
	elif loadFor == 'feed':
		querySetLength = blogNews.objects.filter(
			Q(title__icontains=query) |
			Q(excerptContent__icontains=query) |
			Q(content1__icontains=query) |
			Q(content2__icontains=query) |
			Q(content3__icontains=query) |
			Q(content4__icontains=query) |
			Q(content5__icontains=query)
			).distinct().order_by('-dateOfNews')
	elif loadFor == 'article':
		querySetLength = blogArticles.objects.filter(
			Q(title__icontains=query) |
			Q(excerptContent__icontains=query) |
			Q(content1__icontains=query) |
			Q(content2__icontains=query) |
			Q(content3__icontains=query) |
			Q(content4__icontains=query) |
			Q(content5__icontains=query)
			).distinct().order_by('-dateForListing')
	searchObj = list(querySetLength.values()[offset_int:offset_int+limit])
	querySetCount = querySetLength.count()
	data = {
		'querySetLength': searchObj,
		'querySetCount': querySetCount,
		'query': query,
	}
	return JsonResponse(data=data)

#
def tagBasedSearchView(request, tag_slug=None):
	if tag_slug:
		tag = get_object_or_404(Tag, slug=tag_slug)
		print(tag)
		allMetawithThisTag = metaDetailForDM.objects.filter(meta_tags__in=[tag])
		print(allMetawithThisTag)
		videoSearchObj = []
		shortsSearchObj = []
		researchReportObj = []
		articlesSearchObj = []
		newsSearchObj = []
		mediaSearchObj = []
		staticPagesObj = []
		for item in allMetawithThisTag:
			# print(item)

			if item.static_page == 'videoBlog':
				if len(videoSearchObj) < 3:
					# print(item.video_blog)
					if item.video_blog:
						if item.video_blog not in videoSearchObj:
							videoSearchObj.append(item.video_blog)
						# print(f'thisi {videoSearchObj}')
			elif item.static_page == 'shortsBlog':
				if len(shortsSearchObj) < 6:
					if item.video_shorts_blog:
						if item.video_shorts_blog not in shortsSearchObj:
							shortsSearchObj.append(item.video_shorts_blog)
			elif item.static_page == 'researchReports':
				if len(researchReportObj) < 3:
					if item.research_report:
						if item.research_report not in researchReportObj:
							researchReportObj.append(item.research_report)
			elif item.static_page == 'articleBlog':
				if len(articlesSearchObj) < 3:
					if item.articles_blog:
						if item.articles_blog not in articlesSearchObj:
							articlesSearchObj.append(item.articles_blog)
			elif item.static_page == 'newsBlog':
				if len(newsSearchObj) < 3:
					if item.news_blog:
						if item.news_blog not in newsSearchObj:
							newsSearchObj.append(item.news_blog)
			elif item.static_page == 'mediaBlog':
				if len(mediaSearchObj) < 3:
					if item.media_blog:
						if item.media_blog not in mediaSearchObj:
							mediaSearchObj.append(item.media_blog)
			else:
				staticPagesObj.append(item)
		# print(videoSearchObj)
		videoSearchObj = sorted(videoSearchObj, key=lambda x: x.releasedDate, reverse=True)
		shortsSearchObj = sorted(shortsSearchObj, key=lambda x: x.releaseDate, reverse=True)
		articlesSearchObj = sorted(articlesSearchObj, key=lambda x: x.dateForListing, reverse=True)
		newsSearchObj = sorted(newsSearchObj, key=lambda x: x.dateOfNews, reverse=True)
		mediaSearchObj = sorted(mediaSearchObj, key=lambda x: x.dateForMediaPost, reverse=True)

	else :
		messages.error(request, 'Invalid Tag, Kindly choose some other for proper information.')
		return redirect('blogHomeApp:blogHomeURL')

	context = {
		'newsSearchObj':newsSearchObj,
		'mediaSearchObj':mediaSearchObj,
		'shortsSearchObj':shortsSearchObj,
		'videoSearchObj':videoSearchObj,
		'articlesSearchObj':articlesSearchObj,
		'researchReportObj':researchReportObj,
		'staticPagesObj': staticPagesObj,
		'query':tag,
	}
	return render(request, 'blogHome/UI/search.html', context)


#
def fetchTopXNews(callingFunction=None):
	newsList = None
	with connections['cralwer'].cursor() as cursor:
		status = "'published'"
		query = 'Select * from "crawlApp_googlenewsstore" where status='+status+' and Date is not null ORDER BY DATE DESC limit 10;'
		cursor.execute(query)
		newsList = dictfetchall(cursor)
	return newsList

#
def blogHomeView(request):
	homePageBlogVideo = blogVideos.objects.all().order_by('-releasedDate')[0:10]
	try:
		homePageBlogMedia = blogArticles.objects.latest('-dateForListing')
	except:
		homePageBlogMedia = None
	homePageBlogNews = blogNews.objects.all().order_by('-dateOfNews')[:10]
	homePageBlogArticle = blogArticles.objects.all().order_by('-dateForListing')[0:5]
	homePageBlogShorts = blogVideosShorts.objects.all().order_by('-releaseDate')[0:30]
	# homePageCrawledNews = googleNewsStore.objects.all().order_by('-id')[0:10]
	categoryOpt = articlesCat.objects.all()
	# tagCount = Tag.objects.all().count()
	# tagsArticles = blogArticles.tags.most_common()[:3]
	# tagsVideo = blogVideos.tags.most_common()[:5]
	# tags = tagsArticles.union(tagsVideo)
	tags = metaDetailForDM.meta_tags.most_common()[:15]
	try:
		imagevar = newsCommonImageHomeModel.objects.latest('id')
	except:
		imagevar = None
	newsImageForm = newsCommonImageHomeModelForm()
	homePageCrawledNews = fetchTopXNews()
	# return HttpResponse(str(homePageCrawledNews))

	try:
		latestDMInst = homeBlogDM.objects.latest('id')
	except:
		latestDMInst = None

	for item in categoryOpt:
		print(item)

	context = {
		'homePageBlogVideo':homePageBlogVideo,
		'homePageBlogMedia':homePageBlogMedia,
		'homePageBlogNews':homePageBlogNews,
		'homePageBlogArticle':homePageBlogArticle,
		'homePageBlogShorts':homePageBlogShorts,
		'homePageCrawledNews':homePageCrawledNews,
		'categoryOpt':categoryOpt,
		'tags':tags,
		# 'tagCount':tagCount,
		'imagevar':imagevar,
		'newsImageForm':newsImageForm,
		'latestDMInst':latestDMInst,
	}
	return render(request, 'blogHome/UI/home.html', context)

#
def tagsListView(request):
	tags = Tag.objects.all().order_by('name')
	tagDict = {}
	for tag in tags:
		# videoCount = blogVideos.objects.filter(tags__in=[tag]).count()
		# articleCount = blogArticles.objects.filter(tags__in=[tag]).count()
		# shortsCount = blogVideosShorts.objects.filter(tags__in=[tag]).count()
		totalTag = metaDetailForDM.objects.filter(meta_tags__in=[tag]).count()
		# totalTag = videoCount + articleCount + shortsCount
		tagDict[tag] = totalTag
	tagCount = tags.count()
	try:
		imagevar = tagModel.objects.latest('id')
	except:
		imagevar = None
	tagImageForm = tagModelForm()
	context = {
		'tagDict':tagDict,
		'tags':tags,
		'tagCount':tagCount,
		'imagevar':imagevar,
		'tagImageForm':tagImageForm,
	}
	return render(request, 'blogHome/UI/tags.html', context)

#
def tagModelView(request):
	if request.method == 'POST':
		methodType = request.POST.get('submitType')
		redirectTo = request.POST.get('requestFrom')
		if methodType == 'new':
			objlnst = None
		else:
			pkID = request.POST.get('dataID')
			objlnst = get_object_or_404(tagModel, pk=pkID)  #change model name
		objForm = tagModelForm(request.POST, request.FILES, instance=objlnst) #change form name
		if objForm.is_valid():
			cd = objForm.save(commit=False)
			cd.save()
			cd.refresh_from_db()
			messages.success(request, 'Details sent for verification')
		else:
			messages.error(request, 'Please check An Error occurred')
		return redirect(redirectTo)
	return HttpResponse('Invalid Entry')

#
def categoryImageModelView(request):
	if request.method == 'POST':
		methodType = request.POST.get('submitType')
		redirectTo = request.POST.get('requestFrom')
		if methodType == 'new':
			objlnst = None
		else:
			pkID = request.POST.get('dataID')
			objlnst = get_object_or_404(categoryImageModel, pk=pkID)  #change model name
		objForm = categoryImageModelForm(request.POST, request.FILES, instance=objlnst) #change form name
		if objForm.is_valid():
			cd = objForm.save(commit=False)
			cd.save()
			cd.refresh_from_db()
			messages.success(request, 'Details sent for verification')
		else:
			messages.error(request, 'Please check An Error occurred')
		return redirect(redirectTo)
	return HttpResponse('Invalid Entry')

#
def newsCommonImageHomeModelView(request):
	if request.method == 'POST':
		methodType = request.POST.get('submitType')
		redirectTo = request.POST.get('requestFrom')
		if methodType == 'new':
			objlnst = None
		else:
			pkID = request.POST.get('dataID')
			objlnst = get_object_or_404(newsCommonImageHomeModel, pk=pkID)  #change model name
		objForm = newsCommonImageHomeModelForm(request.POST, request.FILES, instance=objlnst) #change form name
		if objForm.is_valid():
			cd = objForm.save(commit=False)
			cd.save()
			cd.refresh_from_db()
			messages.success(request, 'Details sent for verification')
		else:
			messages.error(request, 'Please check An Error occurred')
		return redirect(redirectTo)
	return HttpResponse('Invalid Entry')

#
def categoryListView(request):
	catSubCatRelation = {}
	requestFrom = request.GET.get('type')
	pageFlag = None
	try:
		imagevar = categoryImageModel.objects.latest('id')
	except:
		imagevar = None
	if requestFrom == 'articles':
		pageFlag = 'articles'
		vidCategories = categoryOptions.objects.all()
		for category in vidCategories:
			subCats = subCategoryOptions.objects.filter(category=category)
			catSubCatRelation[category] = subCats
	elif requestFrom == 'shorts':
		pageFlag = 'shorts'
		vidCategories = videoShortsCategoryOptions.objects.all()
		for category in vidCategories:
			subCats = videoShortsSubCategoryOptions.objects.filter(category=category)
			catSubCatRelation[category] = subCats
	else :
		try:
			pageFlag = 'video'
			vidCategories = vidCats.objects.all()
			for category in vidCategories:
				subCats = vidSubCats.objects.filter(category=category)
				catSubCatRelation[category] = subCats
		except:
			messages.error(request, 'Invalid request.')
			return redirect('blogHomeApp:blogHomeURL')
	categoryImageForm = categoryImageModelForm()
	context = {
		'pageFlag':pageFlag,
		'catSubCatRelation':catSubCatRelation,
		'imagevar':imagevar,
		'categoryImageForm':categoryImageForm,
	}
	return render(request, 'blogHome/UI/categories.html', context)

#
def tagBasedListView(request, slug=None):
	flag =1
	flags = 0
	tag = None
	page = 'tag'
	dataList = {}
	pageType = request.GET.get('type')
	tags = Tag.objects.all()
	if slug:
		tag = get_object_or_404(Tag, slug=slug)
		if pageType == 'shorts':
			blogShorts = blogVideosShorts.objects.filter(tags__in=[tag]).order_by('-releaseDate')
			dataList[tag] = blogShorts
			flags = True
			categoryOpt = videoShortsCategoryOptions.objects.all()
			latestVidShrtBlog = blogShorts.first()
			createVideosShorts = blogVideosShortsForm()
			context = {
				'page':page,
				'dataList':dataList,
				'flag':flag,
				'flags':flags,
				'latestVidShrtBlog':latestVidShrtBlog,
				'categoryOpt':categoryOpt,
				'createVideosShorts':createVideosShorts,
				'tags':tags,
			}
			return render(request, 'videoShorts/UI/shortsList.html', context)
		elif pageType == 'articles':
			blogArticle = blogArticles.objects.filter(tags__in=[tag]).order_by('-dateForListing')
			dataList[tag] = blogArticle
			flags = True
		else:			
			blogVideo = blogVideos.objects.filter(tags__in=[tag]).order_by('-releasedDate')
			dataList[tag] = blogVideo
			flags = True
	else:
		tags = Tag.objects.all()
		for tag in tags :
			blogVideo = blogVideos.objects.filter(tags__in=[tag]).order_by('-releasedDate')
			dataList[tag] = blogVideo
			flag = True
	context = {
		'page':page,
		'dataList':dataList,
		'flag':flag,
		'flags':flags,
	}
	return render(request, 'blogHome/UI/listing.html', context)

#
def categoryBasedListView(request, slug=None):
	category = None
	page = 'category'
	dataList = {}
	requestFrom = request.GET.get('type')
	pageFlag = None
	tags = Tag.objects.all()
	if requestFrom == 'articles':
		pageFlag = 'articles'
		if slug:
			try:
				category = articlesCat.objects.get(slug=slug)
				blogList = blogArticles.objects.filter(category=category).order_by('-created')
				dataList[category] = blogList
			except:
				pass
	elif requestFrom == 'shorts':
		pageFlag = 'shorts'
		if slug:
			try:
				category = videoShortsCategoryOptions.objects.get(slug=slug)
				blogList = blogVideosShorts.objects.filter(category=category).order_by('-created')
				dataList[category] = blogList
				latestVidShrtBlog = blogList.first()
				categoryOpt = videoShortsCategoryOptions.objects.all()
				createVideosShorts = blogVideosShortsForm()
				context = {
					'page':page,
					'dataList':dataList,
					'pageFlag':pageFlag,
					'latestVidShrtBlog':latestVidShrtBlog,
					'categoryOpt':categoryOpt,
					'createVideosShorts':createVideosShorts,
					'tags':tags,
				}
				return render(request, 'videoShorts/UI/shortsList.html', context)
			except:
				pass
	else:
		pageFlag = 'video'
		if slug:
			try:
				category = vidCats.objects.get(slug=slug)
				blogVideo = blogVideos.objects.filter(category=category).order_by('-created')
				dataList[category] = blogVideo
			except:
				pass
	context = {
		'page':page,
		'dataList':dataList,
		'pageFlag':pageFlag,
	}
	return render(request, 'blogHome/UI/listing.html', context)

#
def subCategoryBasedListView(request, slug=None):
	subCategory = None
	page = 'subCategory'
	dataList = {}
	requestFrom = request.GET.get('type')
	pageFlag = None
	if requestFrom == 'articles':
		pageFlag = 'articles'
		if slug:
			try:
				subCategory = subCategoryOptions.objects.get(slug=slug)
				blogList = blogArticles.objects.filter(subCategory=subCategory).order_by('-created')
				dataList[subCategory] = blogList
			except:
				pass
	elif requestFrom == 'shorts':
		pageFlag = 'shorts'
		if slug:
			try:
				subCategory = videoShortsSubCategoryOptions.objects.get(slug=slug)
				blogList = blogVideosShorts.objects.filter(subCategory=subCategory).order_by('-created')
				dataList[subCategory] = blogList
			except:
				pass
	else:
		pageFlag = 'video'
		if slug:
			try:
				subCategory = vidSubCats.objects.get(slug=slug)
				blogList = blogVideos.objects.filter(subCategory=subCategory).order_by('-created')
				dataList[subCategory] = blogList
			except:
				pass
	context = {
		'page':page,
		'dataList':dataList,
		'pageFlag':pageFlag,

	}
	return render(request, 'blogHome/UI/listing.html', context)


#
def homeBlogDMView(request):
	if request.method == 'POST':
		try:
			objInst = homeBlogDM.objects.latest('id')
		except:
			objInst = None
		objForm = homeBlogDMForm(request.POST, request.FILES, instance=objInst)
		if objForm.is_valid():
			cd = objForm.save()
			cd.save()
			cd.refresh_from_db()
			messages.success(request, 'DM Details sent for verification')
		else:
			messages.error(request, 'Please check An Error occurred')
		return redirect('blogHomeApp:blogHomeURL')
	return HttpResponse('Invalid Entry')




#
@api_view(['GET'])
def searchBarViewApi(request):
	query = request.GET.get('searchq')
	showLoadMore = True
	newsLoadMore = mediaLoadMore = shortsLoadMore = videoLoadMore = articleLoadMore = rrLoadMore = staticLoadMore = False
	if query:
		newsSearchAllObj = blogNews.objects.filter(
			Q(title__icontains=query) |
			Q(excerptContent__icontains=query) |
			Q(content1__icontains=query) |
			Q(content2__icontains=query) |
			Q(content3__icontains=query) |
			Q(content4__icontains=query) |
			Q(content5__icontains=query)
			).distinct().order_by('-dateOfNews')
		newsCount = newsSearchAllObj.count()
		newsSearchObj = newsSearchAllObj[:2]
		newsSearchObj_list = []
		if newsSearchObj:
			for each in newsSearchObj:
				temp_data = blogNewsSerializer(each).data
				temp_data['source'] = each.source_self()
				try:
					temp_data['date'] = datetime.datetime.strptime(str(each.dateOfNews), '%Y-%m-%d').strftime('%d %B %Y')
				except:
					temp_data['date'] = None
				newsSearchObj_list.append(temp_data)

		if newsCount > 2:
			newsLoadMore = True

		mediaSearchAllObj = blogMedia.objects.filter(
			Q(title__icontains=query) |
			Q(excerptContent__icontains=query) |
			Q(content2__icontains=query) |
			Q(content3__icontains=query) |
			Q(content4__icontains=query) |
			Q(content5__icontains=query)
			).distinct().order_by('-dateForMediaPost')
		mediaCount = mediaSearchAllObj.count()
		mediaSearchObj = mediaSearchAllObj[:2]

		mediaSearchObj_list = []
		if mediaSearchObj:
			for each in mediaSearchObj:
				temp_data = blogMediaSerializer(each).data
				temp_data['source'] = each.publishMedia
				try:
					temp_data['date'] = datetime.datetime.strptime(str(each.dateForMediaPost), '%Y-%m-%d').strftime('%d %B %Y')
				except:
					temp_data['date'] = None

				mediaSearchObj_list.append(temp_data)

		if mediaCount > 2:
			mediaLoadMore = True

		shortsSearchAllObj = blogVideosShorts.objects.filter(
			Q(title__icontains=query) |
			Q(excerptContent__icontains=query) |
			Q(content1__icontains=query) |
			Q(content2__icontains=query) |
			Q(content3__icontains=query) |
			Q(content4__icontains=query) |
			Q(content5__icontains=query)
			).distinct().order_by('-releaseDate')
		shortsCount = shortsSearchAllObj.count()
		shortsSearchObj = shortsSearchAllObj[:6]

		shortsSearchObj_list = []
		if shortsSearchObj:
			for each in shortsSearchObj:
				temp_data = blogVideosShortsSerializer(each).data
				temp_data['source'] = each.source_self()
				temp_data['videoLink'] = 'http://youtu.be/'+each.videoLink
				try:
					temp_data['date'] = datetime.datetime.strptime(str(each.releaseDate)[:10], '%Y-%m-%d').strftime('%d %B %Y')
				except:
					temp_data['date'] = None
				shortsSearchObj_list.append(temp_data)

		if shortsCount > 6:
			shortsLoadMore = True

		videoSearchAllObj = blogVideos.objects.filter(
			Q(title__icontains=query) |
			Q(excerptContent__icontains=query) |
			Q(content__icontains=query)
			).distinct().order_by('-releasedDate')
		videoCount = videoSearchAllObj.count()
		videoSearchObj = videoSearchAllObj[:3]

		videoSearchObj_list = []
		if videoSearchObj:
			for each in videoSearchObj:
				temp_data = blogVideosSerializer(each).data
				temp_data['source'] = each.source_self()
				temp_data['videoLink'] = 'http://youtu.be/'+each.videoLink
				try:
					temp_data['date'] = datetime.datetime.strptime(str(each.releasedDate), '%Y-%m-%d').strftime('%d %B %Y')
				except:
					temp_data['date'] = None
				videoSearchObj_list.append(temp_data)

		if videoCount > 3:
			videoLoadMore = True

		articlesSearchAllObj = blogArticles.objects.filter(
			Q(title__icontains=query) |
			Q(excerptContent__icontains=query) |
			Q(content1__icontains=query) |
			Q(content2__icontains=query) |
			Q(content3__icontains=query) |
			Q(content4__icontains=query) |
			Q(content5__icontains=query)
			).distinct().order_by('-dateForListing')
		articleCount = articlesSearchAllObj.count()
		articlesSearchObj = articlesSearchAllObj[:3]

		articlesSearchObj_list = []
		if articlesSearchObj:
			for each in articlesSearchObj:
				temp_data = blogArticlesSerializer(each).data
				temp_data['source'] = each.source_self()
				try:
					temp_data['date'] = datetime.datetime.strptime(str(each.dateForListing), '%Y-%m-%d').strftime('%d %B %Y')
				except:
					temp_data['date'] = None
				articlesSearchObj_list.append(temp_data)

		if articleCount > 3:
			articleLoadMore = True

		#category = buyPreIPOStockList.objects.filter(name__icontains=searchQuery).order_by('name')

		researchReportAllObj = stockBasicDetail.objects.filter(status='published').filter(
				Q(stockName__icontains=query) |
				Q(seoTitle__icontains=query) |
				Q(ticker__icontains=query)
			).distinct().order_by('-publish')
		rrCount = researchReportAllObj.count()
		researchReportObj = researchReportAllObj[:3]

		researchReportObj_list = []
		buyPreIPOStockList_object_list = []
		if researchReportObj:
			for each in researchReportObj:
				try:
					buyPreIPOStockList_object = buyPreIPOStockList.objects.get(stockName=each)
					if buyPreIPOStockList_object.stockName:
						try:
							serializer = buyPreIPOStockListGETSerializer(buyPreIPOStockList_object)
							data = serializer.data
							if not data['logo']:
								data['logo'] = "https://planify-main.s3.amazonaws.com/static/news/icons/planify-newlogo.png"
							essentialInst = stockEssentials.objects.filter(stockProfileName=buyPreIPOStockList_object.stockName).last()
							if essentialInst and essentialInst.category and essentialInst.category.name:
								data["category"] = essentialInst.category.name if essentialInst.category else None
							else:
								data["category"] = None
							if essentialInst and essentialInst.subSector and essentialInst.subSector.name:
								data["subSector"] = essentialInst.subSector.name if essentialInst.subSector else None
							else:
								data["subSector"] = None
							buyPreIPOStockList_object_list.append(data)
						except stockEssentials.DoesNotExist:
							pass
					else:
						serializer = buyPreIPOStockListGETSerializer(buyPreIPOStockList_object_list)
						data = serializer.data
						data["subSector"] = None
						data["category"] = None
						if not data['logo']:
							data['logo'] = "https://planify-main.s3.amazonaws.com/static/news/icons/planify-newlogo.png"	
						buyPreIPOStockList_object_list.append(data)
					researchReportObj_list.append(stockBasicDetailSerializer(each).data)
				except:
					continue

		if rrCount > 3:
			rrLoadMore = True

		if not request.GET.get('search') == 'home':
			staticPagesAllObj = metaDetailForDM.objects.filter(
				Q(meta_title__icontains=query) | 
				Q(meta_description__icontains=query) | 
				Q(meta_keywords__icontains=query) | 
				Q(meta_tags__name__icontains=query)
				).exclude(Q(static_page__in=['videoBlog','shortsBlog','articleBlog','newsBlog','researchReports',])).distinct()[:3]
			staticCount = staticPagesAllObj.count()
			staticPagesObj = staticPagesAllObj[:3]

			staticPagesObj_list = []
			if staticPagesObj:
				for each in staticPagesObj:
					staticPagesObj_list.append(metaDetailForDMSerializer(each).data)

			if staticCount > 3:
				staticLoadMore = True
		else:
			staticPagesObj = None
		with connections['cralwer'].cursor() as cursor:
			status = "'published'"
			if query:
				searchPage = True
				query = query.replace("'", "\\'")
				queryToSearch = "'%"+query+"%'"
				queryToExecute = 'Select * from "crawlApp_googlenewsstore" \
				where status='+status+' AND (title ILIKE E'+queryToSearch+' OR "desc" ILIKE E'+queryToSearch+' OR site ILIKE E'+queryToSearch+') ORDER BY date DESC LIMIT 10;'
			cursor.execute(queryToExecute)
			newsWebObj = dictfetchall(cursor)
			for each in newsWebObj:
				each['source'] = each['site']
				try:
					each['date'] = datetime.datetime.strptime(str(each['date']), '%Y-%m-%d').strftime('%d %B %Y')
				except:
					each['date'] = None
	else :
		messages.error(request, 'Enter an Query to Search')
		return redirect('blogHomeApp:blogHomeURL')
	total_video_obj = blogVideos.objects.count()
	context = {
		'newsSearchObj':newsSearchObj_list,
		'mediaSearchObj':mediaSearchObj_list,
		'shortsSearchObj':shortsSearchObj_list,
		'videoSearchObj':videoSearchObj_list,
		'articlesSearchObj':articlesSearchObj_list,
		'researchReportObj':buyPreIPOStockList_object_list,
		'staticPagesObj':staticPagesObj_list,
		'newsWebObj': newsWebObj,
		'query':query,
		'total_video_obj' : total_video_obj,
		'newsLoadMore': newsLoadMore,
		'mediaLoadMore': mediaLoadMore,
		'shortsLoadMore': shortsLoadMore,
		'videoLoadMore': videoLoadMore,
		'articleLoadMore': articleLoadMore,
		'rrLoadMore': rrLoadMore,
		'staticLoadMore': staticLoadMore,
		'showLoadMore': showLoadMore,
	}
	return Response(context)


#
@api_view(['GET'])
def search_load_more_view_api(request):
	offset = request.GET.get('offset')
	query = request.GET.get('query')
	loadFor = request.GET.get('loadFor')
	offset_int = int(offset)
	limit = 30
	if loadFor == 'video':
		querySetLength = blogVideos.objects.filter(Q(title__icontains=query) | 
			Q(excerptContent__icontains=query) | 
			Q(content__icontains=query)
			).distinct().order_by('-releasedDate')
		for each in querySetLength:
			each.source = each.source_self()
			each.videoLink = 'http://youtu.be/'+each.videoLink
			try:
				each.date = datetime.datetime.strptime(str(each.releasedDate), '%Y-%m-%d').strftime('%d %B %Y')
			except:
				each.date = None
	elif loadFor == 'short':
		querySetLength = blogVideosShorts.objects.filter(
			Q(title__icontains=query)|
			Q(excerptContent__icontains=query) |
			Q(content1__icontains=query) |
			Q(content2__icontains=query) |
			Q(content3__icontains=query) |
			Q(content4__icontains=query) |
			Q(content5__icontains=query)
			).distinct().order_by('-releaseDate')
		
		for each in querySetLength:
			each.source = each.source_self()
			each.videoLink = 'http://youtu.be/'+each.videoLink
			try:
				each.date = datetime.datetime.strptime(str(each.releaseDate)[:10], '%Y-%m-%d').strftime('%d %B %Y')
			except:
				each.date = None
	elif loadFor == 'researchReport':
		querySetLength = stockBasicDetail.objects.filter(status='published').filter(
				Q(stockName__icontains=query) |
				Q(seoTitle__icontains=query) |
				Q(ticker__icontains=query)
			).distinct().order_by('-publish')

		buyPreIPOStockList_object_list = []
		if querySetLength:
			for each in querySetLength:
				try:
					#print(each.stockName)
					buyPreIPOStockList_object = buyPreIPOStockList.objects.get(stockName=each)
					if buyPreIPOStockList_object.stockName:
						try:
							serializer = buyPreIPOStockListGETSerializer(buyPreIPOStockList_object)
							data = serializer.data
							if not data['logo']:
								data['logo'] = "https://planify-main.s3.amazonaws.com/static/news/icons/planify-newlogo.png"
							essentialInst = stockEssentials.objects.filter(stockProfileName=buyPreIPOStockList_object.stockName).last()
							if essentialInst and essentialInst.category and essentialInst.category.name:
								data["category"] = essentialInst.category.name if essentialInst.category else None
							else:
								data["category"] = None
							if essentialInst and essentialInst.subSector and essentialInst.subSector.name:
								data["subSector"] = essentialInst.subSector.name if essentialInst.subSector else None
							else:
								data["subSector"] = None
							buyPreIPOStockList_object_list.append(data)
						except stockEssentials.DoesNotExist:
							pass
					else:
						serializer = buyPreIPOStockListGETSerializer(buyPreIPOStockList_object_list)
						data = serializer.data
						data["subSector"] = None
						data["category"] = None
						if not data['logo']:
							data['logo'] = "https://planify-main.s3.amazonaws.com/static/news/icons/planify-newlogo.png"	
						buyPreIPOStockList_object_list.append(data)
				except:
					continue
	elif loadFor == 'staticPage':
		querySetLength = metaDetailForDM.objects.filter(
				Q(meta_title__icontains=query) | 
				Q(meta_description__icontains=query) | 
				Q(meta_keywords__icontains=query) | 
				Q(meta_tags__name__icontains=query)
				).exclude(Q(static_page__in=['videoBlog','shortsBlog','articleBlog','newsBlog','researchReports',])).distinct()
	elif loadFor == 'feed':
		querySetLength = blogNews.objects.filter(
			Q(title__icontains=query) |
			Q(excerptContent__icontains=query) |
			Q(content1__icontains=query) |
			Q(content2__icontains=query) |
			Q(content3__icontains=query) |
			Q(content4__icontains=query) |
			Q(content5__icontains=query)
			).distinct().order_by('-dateOfNews')
		
		each.source = each.source_self()
		try:
			each.date = datetime.datetime.strptime(str(each.dateOfNews), '%Y-%m-%d').strftime('%d %B %Y')
		except:
			each.date = None
	elif loadFor == 'article':
		querySetLength = blogArticles.objects.filter(
			Q(title__icontains=query) |
			Q(excerptContent__icontains=query) |
			Q(content1__icontains=query) |
			Q(content2__icontains=query) |
			Q(content3__icontains=query) |
			Q(content4__icontains=query) |
			Q(content5__icontains=query)
			).distinct().order_by('-dateForListing')

		each.source = each.source_self()
		try:
			each.date = datetime.datetime.strptime(str(each.dateForListing), '%Y-%m-%d').strftime('%d %B %Y')
		except:
			each.date = None
	searchObj = list(querySetLength.values()[offset_int:offset_int+limit])
	if loadFor == 'researchReport':
		searchObj = buyPreIPOStockList_object_list[offset_int:offset_int+limit]
	querySetCount = querySetLength.count()
	data = {
		'querySetLength': searchObj,
		'querySetCount': querySetCount,
		'query': query,
	}
	return Response(data)


@api_view(['GET'])
def searchBarSuggestionsApi(request):
	query = request.GET.get('searchq')
	data_list = []
	company_list = []

	def get_feed_suggestions(query):
		newsSearchAllObj = blogNews.objects.filter(
			Q(title__icontains=query) |
			Q(excerptContent__icontains=query) |
			Q(content1__icontains=query) |
			Q(content2__icontains=query) |
			Q(content3__icontains=query) |
			Q(content4__icontains=query) |
			Q(content5__icontains=query)
			).distinct().order_by('-dateOfNews').only('id', 'title', 'dateOfNews')

		if newsSearchAllObj:
			for each in newsSearchAllObj:
				data_list.append({'type': 'Feed', 'id': each.id, 'title': each.title, 'date': each.dateOfNews.strftime("%Y/%m/%d")})

	def get_shorts_suggestions(query):
		shortsSearchAllObj = blogVideosShorts.objects.filter(
			Q(title__icontains=query) |
			Q(excerptContent__icontains=query) |
			Q(content1__icontains=query) |
			Q(content2__icontains=query) |
			Q(content3__icontains=query) |
			Q(content4__icontains=query) |
			Q(content5__icontains=query)
			).distinct().order_by('-releaseDate').only('id', 'title', 'releaseDate')

		if shortsSearchAllObj:
			for each in shortsSearchAllObj:
				data_list.append({'type': 'Shorts',  'id': each.id, 'title': each.title, 'date': each.releaseDate.strftime("%Y/%m/%d")})


	def get_video_suggestions(query):
		videoSearchAllObj = blogVideos.objects.filter(
			Q(title__icontains=query) |
			Q(excerptContent__icontains=query) |
			Q(content__icontains=query)
			).distinct().order_by('-releasedDate').only('id', 'title', 'releasedDate')

		if videoSearchAllObj:
			for each in videoSearchAllObj:
				data_list.append({'type': 'Videos',  'id': each.id, 'title': each.title, 'date': each.releasedDate.strftime("%Y/%m/%d")})


	def get_articles_suggestions(query):
		articlesSearchAllObj = blogArticles.objects.filter(
			Q(title__icontains=query) |
			Q(excerptContent__icontains=query) |
			Q(content1__icontains=query) |
			Q(content2__icontains=query) |
			Q(content3__icontains=query) |
			Q(content4__icontains=query) |
			Q(content5__icontains=query)
			).distinct().order_by('-dateForListing').only('id', 'title', 'dateForListing')

		if articlesSearchAllObj:
			for each in articlesSearchAllObj:
				data_list.append({'type': 'Articles',  'id': each.id, 'title': each.title, 'date': each.dateForListing.strftime("%Y/%m/%d")})

	def get_company_suggestions(query):
		researchReportAllObj = stockBasicDetail.objects.filter(status='published').filter(
				Q(stockName__icontains=query) |
				Q(seoTitle__icontains=query) |
				Q(ticker__icontains=query)
			).distinct().order_by('-publish').only('id', 'stockName', 'publish')

		if researchReportAllObj:
			for each in researchReportAllObj:
				company_list.append({'type': 'Company',  'id': each.id, 'title': each.stockName, 'date': each.publish.strftime("%Y/%m/%d")})

	def get_news_suggestions(query):
		with connections['cralwer'].cursor() as cursor:
			status = "'published'"
			if query:
				searchPage = True
				query = query.replace("'", "\\'")
				queryToSearch = "'%"+query+"%'"
				queryToExecute = 'Select * from "crawlApp_googlenewsstore" \
				where status='+status+' AND (title ILIKE E'+queryToSearch+' OR "desc" ILIKE E'+queryToSearch+' OR site ILIKE E'+queryToSearch+') ORDER BY date DESC LIMIT 10;'
			cursor.execute(queryToExecute)
			newsWebObj = dictfetchall(cursor)
			for item in newsWebObj:
				data_list.append({'type': 'News',  'id': item['id'], 'title': item['title'], 'date': item['date'].strftime("%Y/%m/%d")})
	if query:
		t1 = threading.Thread(target=get_company_suggestions, args=(query,))
		t2 = threading.Thread(target=get_video_suggestions, args=(query,))
		t3 = threading.Thread(target=get_shorts_suggestions, args=(query,))
		t4 = threading.Thread(target=get_articles_suggestions, args=(query,))
		t5 = threading.Thread(target=get_news_suggestions, args=(query,))
		t6 = threading.Thread(target=get_feed_suggestions, args=(query,))
		t1.start()
		t2.start()
		t3.start()
		t4.start()
		t5.start()
		t6.start()
		t1.join()
		t2.join()
		t3.join()
		t4.join()
		t5.join()
		t6.join()
	else :
		messages.error(request, 'Enter an Query to Search')

	data_list = sorted(data_list, key=lambda d: d['date'], reverse=True)
	context = {
		'query': query,
		'total objects': len(company_list + data_list),
		'results': company_list + data_list
	}
	return Response(context)





@api_view(['GET'])
def loadSingleObject(request):
	entity_id = request.GET.get('id')
	entity_type = request.GET.get('type')
	if entity_type == 'Feed':
		response_obj = blogNews.objects.get(id=entity_id)
		response_obj = newsSerializer(response_obj).data

	elif entity_type == 'Shorts':
		response_obj = blogVideosShorts.objects.get(id=entity_id)
		response_obj = shortsListSerializer(response_obj).data

	elif entity_type == 'Videos':

		response_obj = blogVideos.objects.get(id=entity_id)
		response_obj = videosSerializer(response_obj).data

	elif entity_type == 'Articles':

		response_obj = blogArticles.objects.get(id=entity_id)
		response_obj = articleSerializer(response_obj).data

	elif entity_type == 'Static Page':
		response_obj = metaDetailForDM.objects.get(id=entity_id)
		response_obj = metaDetailForDMSerializer(response_obj).data

	elif entity_type == 'Company':

		researchReportObj = stockBasicDetail.objects.get(id=entity_id)
		
		if researchReportObj:
			buyPreIPOStockList_object = buyPreIPOStockList.objects.get(stockName=researchReportObj)
			if buyPreIPOStockList_object.stockName:
				try:
					serializer = buyPreIPOStockListGETSerializer(buyPreIPOStockList_object)
					data = serializer.data
					if not data['logo']:
						data['logo'] = "https://planify-main.s3.amazonaws.com/static/news/icons/planify-newlogo.png"
					essentialInst = stockEssentials.objects.filter(stockProfileName=buyPreIPOStockList_object.stockName).last()
					if essentialInst and essentialInst.category and essentialInst.category.name:
						data["category"] = essentialInst.category.name if essentialInst.category else None
					else:
						data["category"] = None
					if essentialInst and essentialInst.subSector and essentialInst.subSector.name:
						data["subSector"] = essentialInst.subSector.name if essentialInst.subSector else None
					else:
						data["subSector"] = None
					response_obj = data
				except stockEssentials.DoesNotExist:
					pass
				else:
					serializer = buyPreIPOStockListGETSerializer(buyPreIPOStockList_object)
					data = serializer.data
					data["subSector"] = None
					data["category"] = None
					if not data['logo']:
						data['logo'] = "https://planify-main.s3.amazonaws.com/static/news/icons/planify-newlogo.png"	
					response_obj = data
					


	elif entity_type == 'News':
		with connections['cralwer'].cursor() as cursor:
			status = "'published'"
			if True:
				searchPage = True
				#query = query.replace("'", "\\'")
				#queryToSearch = "'%"+query+"%'"
				queryToExecute = 'Select * from "crawlApp_googlenewsstore" \
				where status='+status+' AND (id='+str(entity_id)+')'
			cursor.execute(queryToExecute)
			newsWebObj = dictfetchall(cursor)
			response_obj = newsWebObj[0]
		
	context = {
		'id': entity_id,
		'type': entity_type,
		'data': response_obj
	}
	return Response(context)

@api_view(['GET'])
def searchBarSuggestionsApi_01(request):
	query = request.GET.get('searchq')
	data_list = []
	company_list = []
	def get_static_pages_suggestions(query):
		if	query.lower() != 'home':
			staticPagesAllObj = metaDetailForDM.objects.filter(
				Q(meta_title__icontains=query) | 
				Q(meta_description__icontains=query) | 
				Q(meta_keywords__icontains=query) | 
				Q(meta_tags__name__icontains=query)
				).exclude(Q(static_page__in=['videoBlog','shortsBlog','articleBlog','newsBlog','researchReports',])).only('id', 'meta_title', 'updated')
		if staticPagesAllObj:
			for each in set(staticPagesAllObj):
				data_list.append({'type': 'Static Page', 'id': each.id, 'title': each.meta_title, 'date': each.updated.strftime("%Y/%m/%d")})


	def get_feed_suggestions(query):
		newsSearchAllObj = blogNews.objects.filter(
			Q(title__icontains=query) |
			Q(excerptContent__icontains=query) |
			Q(content1__icontains=query) |
			Q(content2__icontains=query) |
			Q(content3__icontains=query) |
			Q(content4__icontains=query) |
			Q(content5__icontains=query)
			).distinct().order_by('-dateOfNews').only('id', 'title', 'dateOfNews')

		if newsSearchAllObj:
			for each in newsSearchAllObj:
				data_list.append({'type': 'Feed', 'id': each.id, 'title': each.title, 'date': each.dateOfNews.strftime("%Y/%m/%d")})

	def get_shorts_suggestions(query):
		shortsSearchAllObj = blogVideosShorts.objects.filter(
			Q(title__icontains=query) |
			Q(excerptContent__icontains=query) |
			Q(content1__icontains=query) |
			Q(content2__icontains=query) |
			Q(content3__icontains=query) |
			Q(content4__icontains=query) |
			Q(content5__icontains=query)
			).distinct().order_by('-releaseDate').only('id', 'title', 'releaseDate')

		if shortsSearchAllObj:
			for each in shortsSearchAllObj:
				data_list.append({'type': 'Shorts',  'id': each.id, 'title': each.title, 'date': each.releaseDate.strftime("%Y/%m/%d")})


	def get_video_suggestions(query):
		videoSearchAllObj = blogVideos.objects.filter(
			Q(title__icontains=query) |
			Q(excerptContent__icontains=query) |
			Q(content__icontains=query)
			).distinct().order_by('-releasedDate').only('id', 'title', 'releasedDate')

		if videoSearchAllObj:
			for each in videoSearchAllObj:
				data_list.append({'type': 'Videos',  'id': each.id, 'title': each.title, 'date': each.releasedDate.strftime("%Y/%m/%d")})


	def get_articles_suggestions(query):
		articlesSearchAllObj = blogArticles.objects.filter(
			Q(title__icontains=query) |
			Q(excerptContent__icontains=query) |
			Q(content1__icontains=query) |
			Q(content2__icontains=query) |
			Q(content3__icontains=query) |
			Q(content4__icontains=query) |
			Q(content5__icontains=query)
			).distinct().order_by('-dateForListing').only('id', 'title', 'dateForListing')

		if articlesSearchAllObj:
			for each in articlesSearchAllObj:
				data_list.append({'type': 'Articles',  'id': each.id, 'title': each.title, 'date': each.dateForListing.strftime("%Y/%m/%d")})

	def get_company_suggestions(query):
		researchReportAllObj = stockBasicDetail.objects.filter(status='published').filter(
				Q(stockName__icontains=query) |
				Q(seoTitle__icontains=query) |
				Q(ticker__icontains=query)
			).distinct().order_by('-publish').only('id', 'stockName', 'publish')

		if researchReportAllObj:
			for each in researchReportAllObj:
				company_list.append({'type': 'Company',  'id': each.id, 'title': each.stockName, 'date': each.publish.strftime("%Y/%m/%d")})

	def get_news_suggestions(query):
		with connections['cralwer'].cursor() as cursor:
			status = "'published'"
			if query:
				searchPage = True
				query = query.replace("'", "\\'")
				queryToSearch = "'%"+query+"%'"
				queryToExecute = 'Select * from "crawlApp_googlenewsstore" \
				where status='+status+' AND (title ILIKE E'+queryToSearch+' OR "desc" ILIKE E'+queryToSearch+' OR site ILIKE E'+queryToSearch+') ORDER BY date DESC LIMIT 10;'
			cursor.execute(queryToExecute)
			newsWebObj = dictfetchall(cursor)
			for item in newsWebObj:
				data_list.append({'type': 'News',  'id': item['id'], 'title': item['title'], 'date': item['date'].strftime("%Y/%m/%d")})
	if query:
		get_company_suggestions(query)
		get_static_pages_suggestions(query)
		get_video_suggestions(query)
		get_shorts_suggestions(query)
		get_articles_suggestions(query)
		get_news_suggestions(query)
		get_feed_suggestions(query)
		
	else :
		messages.error(request, 'Enter an Query to Search')

	data_list = sorted(data_list, key=lambda d: d['date'], reverse=True)
	context = {
		'query': query,
		'total objects': len(company_list + data_list),
		'results': company_list + data_list
	}
	return Response(context)

@api_view(['GET'])
def blogPageApiView(request, slug = None):
	flag = request.GET.get('slug')
	current_site= str(get_current_site(request))
	if request.method == 'GET':
		urls = {
			'blogVideoUrl': "http://"+current_site+'/blog/blogPageApiView/?slug=blogVideo',
			'blogNewsUrl': "http://"+current_site+'/blog/blogPageApiView/?slug=blogNews',
			'blogArticlesUrl': "http://"+current_site+'/blog/blogPageApiView/?slug=blogArticles',
			'blogVideosShortsUrl': "http://"+current_site+'/blog/blogPageApiView/?slug=blogVideosShorts',
			'crawledNewsUrl': "http://"+current_site+'/blog/blogPageApiView/?slug=crawledNews'
		}
		if flag == "blogVideo":
			blogVideoInst = blogVideos.objects.all().order_by('-releasedDate')[0:10]
			paginator = PageNumberPagination()
			paginator.page_size = 3
			blogPagination = paginator.paginate_queryset(blogVideoInst, request)
			blogVideosSerial = blogVideosSerializer(blogPagination , many= True)
			blogVideosSerial = blogVideosSerial.data
			msg = "Please use below urls to navigate to the different models and use the pagination url to navigate in btw the page !!"
			return paginator.get_paginated_response({'msg': msg,'url': urls,'blogVideosSerial': blogVideosSerial })

		if flag == "blogNews":
			blogNewsInst = blogNews.objects.all().order_by('-dateOfNews')[:10]
			paginator = PageNumberPagination()
			paginator.page_size = 3
			blogNewsPagination = paginator.paginate_queryset(blogNewsInst, request)
			blogNewsSerial = blogNewsSerializer(blogNewsPagination, many = True)
			blogNewsSerial = blogNewsSerial.data
			msg = "Please use below urls to navigate to the different models and use the pagination url to navigate in btw the page !!"
			return paginator.get_paginated_response({'msg': msg, 'url': urls, 'blogNewsSerial': blogNewsSerial})


		if flag == "blogArticles":
			blogArticleInst = blogArticles.objects.all().order_by('-dateForListing')[0:5]
			paginator = PageNumberPagination()
			paginator.page_size = 2
			blogArticlePagination = paginator.paginate_queryset(blogArticleInst, request)
			blogArticleSerial = blogArticlesSerializer(blogArticlePagination, many = True)
			blogArticleSerial = blogArticleSerial.data
			msg = "Please use below urls to navigate to the different models and use the pagination url to navigate in btw the page !!"
			return paginator.get_paginated_response({'msg': msg,'url': urls, 'blogArticleSerial': blogArticleSerial})


		if flag == "blogVideosShorts":
			blogShortsInst = blogVideosShorts.objects.all().order_by('-releaseDate')[0:30]
			paginator = PageNumberPagination()
			paginator.page_size = 5
			blogShortsPagination = paginator.paginate_queryset(blogShortsInst, request)
			blogShortsSerial = blogVideosShortsSerializer(blogShortsPagination, many = True)
			blogShortsSerial = blogShortsSerial.data
			msg = "Please use below urls to navigate to the different models and use the pagination url to navigate in btw the page !!"
			return paginator.get_paginated_response({'msg': msg,'url': urls, 'blogShortsSerial': blogShortsSerial})
		if flag == "crawledNews":
			paginator = PageNumberPagination()
			paginator.page_size = 5
			homePageCrawledNews = fetchTopXNews()
			crawledNewsPagination = paginator.paginate_queryset(homePageCrawledNews, request)
			msg = "Please use below urls to navigate to the different models and use the pagination url to navigate in btw the page !!"
			return paginator.get_paginated_response({'msg': msg,'url': urls,'crawledNewsPagination':crawledNewsPagination})

		return Response({'urls':urls})

