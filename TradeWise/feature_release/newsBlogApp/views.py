from django.shortcuts import render, HttpResponse, get_object_or_404, redirect
from django.contrib import messages
from django.db.models import Q
from django.db import connections
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import *
from .forms import *

from .serializers import blogNewsSerializer, feedDescriptionSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import generics
from planifyMain.paginators import StandardResultsSetPagination


#
def searchBarView(request):
    query = request.GET.get('searchq')
    createBlogNews = blogNewsForm()
    newsObj = blogNews.objects.all().order_by('-dateOfNews')
    flag = 'blogNewsListing'
    flagSearch = True
    if query:
        newsSearchObj = newsObj.filter(
            Q(title__icontains=query) | Q(subTitle__icontains=query) | Q(excerptContent__icontains=query) | Q(
                content1__icontains=query) | Q(content2__icontains=query) | Q(content3__icontains=query) | Q(
                content4__icontains=query) | Q(content5__icontains=query)).distinct()
    else:
        newsSearchObj = newsObj
    context = {
        'newsList': newsSearchObj,
        'flag': flag,
        'flagSearch': flagSearch,
        'query': query,
        'createBlogNews': createBlogNews,
    }
    return render(request, 'news/UI/newsList.html', context)


#
def blogNewsDMView(request):
    if request.method == 'POST':
        methodType = request.POST.get('submitType')
        redirectTo = request.POST.get('requestFrom')
        adminRequest = request.GET.get('requestFrom')
        parentProfile = None
        if methodType == 'new':
            objlnst = None
        else:
            pkId = request.POST.get('dataID')

        if adminRequest == 'blogNewsListing':
            if methodType == 'new':
                objlnst = None
            else:
                objlnst = get_object_or_404(blogNewsListingDM, pk=pkId)
            objForm = blogNewsListingDMForm(request.POST, request.FILES, instance=objlnst)

        elif adminRequest == 'blogNewsDetail':
            if methodType == 'new':
                parentID = request.POST.get('blogProfileName')
                parentProfile = get_object_or_404(blogNews, pk=parentID)
            else:
                objlnst = get_object_or_404(blogNewsDetailedDM, pk=pkId)
            objForm = blogNewsDetailedDMForm(request.POST, request.FILES, instance=objlnst)

        elif adminRequest == 'crawled':
            if methodType == 'new':
                objlnst = None
            else:
                objlnst = get_object_or_404(blogWebNewsListingDM, pk=pkId)
            objForm = blogWebNewsListingDMForm(request.POST, request.FILES, instance=objlnst)

        if objForm.is_valid():
            cd = objForm.save(commit=False)
            if methodType == 'new' and parentProfile:
                cd.blogProfileName = parentProfile
            if request.user.is_authenticated:
                cd.analyst = request.user
            cd.save()
            objForm.save_m2m()
            cd.refresh_from_db()
            messages.success(request, 'Blog DM  Sent For Verification')
        else:
            messages.error(request, 'Please Check An Error occurred')
        return redirect(redirectTo)
    return HttpResponse('Invalid Entry')


#
def newsListView(request):
    createBlogNews = blogNewsForm()
    query = request.GET.get('searchq')
    if query:
        newsList = blogNews.objects.filter(
            Q(title__icontains=query) | Q(subTitle__icontains=query) | Q(excerptContent__icontains=query) | Q(
                content1__icontains=query) | Q(content2__icontains=query) | Q(content3__icontains=query) | Q(
                content4__icontains=query) | Q(content5__icontains=query)).distinct().order_by('-dateOfNews',
                                                                                               '-created')
    else:
        newsList = blogNews.objects.all().order_by('-dateOfNews', '-created')
    flag = 'created'

    try:
        blogNewsListingDMInst = blogNewsListingDM.objects.latest('-id')
    except:
        blogNewsListingDMInst = None
    createBlogNewsListingDM = blogNewsListingDMForm(instance=blogNewsListingDMInst)
    try:
        blogNewsHeadingDMInst = newsHeadingDM.objects.latest('-id')
    except:
        blogNewsHeadingDMInst = None
    createblogNewsHeadingDM = newsHeadingDMForm(instance=blogNewsHeadingDMInst)
    paginator = Paginator(newsList, 5)
    page = request.GET.get('page')
    try:
        newsList = paginator.page(page)
    except PageNotAnInteger:
        newsList = paginator.page(1)
    except EmptyPage:
        newsList = paginator.page(paginator.num_pages)
    flag = 'blogNewsListing'
    totalPages = paginator.num_pages
    try:
        if int(page) > totalPages:
            messages.error(request, 'Invalid Page Number.')
            page = 1
    except:
        pass
    context = {
        'createBlogNews': createBlogNews,
        'newsList': newsList,
        'blogNewsListingDMInst': blogNewsListingDMInst,
        'createBlogNewsListingDM': createBlogNewsListingDM,
        'flag': flag,
        'blogNewsHeadingDMInst': blogNewsHeadingDMInst,
        'createblogNewsHeadingDM': createblogNewsHeadingDM,
        'page': page,
        'totalPages': totalPages,
    }
    return render(request, 'news/UI/newsList.html', context)


class newsfeedListApiView(generics.ListAPIView):
    queryset = blogNews.objects.all().order_by('-dateOfNews', '-created')
    serializer_class = blogNewsSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['title', 'subTitle', 'excerptContent', 'content1', 'content2', 'content3', 'content4', 'content5']


# ordering = ['-dateOfNews']


#
def newsDetailView(request, slug):
    obj = get_object_or_404(blogNews, slug=slug)

    try:
        blogNewsDetailedDMInst = blogNewsDetailedDM.objects.get(blogProfileName=obj)
    except:
        blogNewsDetailedDMInst = None
    createBlogNewsDetailedDM = blogNewsDetailedDMForm(instance=blogNewsDetailedDMInst)

    context = {
        'obj': obj,
        'blogNewsDetailedDMInst': blogNewsDetailedDMInst,
        'createBlogNewsDetailedDM': createBlogNewsDetailedDM,
    }
    return render(request, 'news/UI/newsDetail.html', context)


#
def dictfetchall(cursor):
    desc = cursor.description
    return [
        dict(zip([col[0] for col in desc], row))
        for row in cursor.fetchall()
    ]


#
def crawledNewsView(request):
    searchPage = False
    searchQuery = request.GET.get('searchq')
    with connections['cralwer'].cursor() as cursor:
        status = "'published'"
        if searchQuery:
            searchPage = True
            searchQuery = searchQuery.replace("'", "\\'")
            queryToSearch = "'%" + searchQuery + "%'"
            query = 'Select * from "crawlApp_googlenewsstore" \
			where status=' + status + ' AND (title ILIKE E' + queryToSearch + ' OR "desc" ILIKE E' + queryToSearch + ' OR site ILIKE E' + queryToSearch + ') ORDER BY date DESC;'
        else:
            query = 'select * from "crawlApp_googlenewsstore" where status=' + status + ' ORDER BY date DESC'
        cursor.execute(query)
        newsListRaw = dictfetchall(cursor)
    flag = 'crawled'
    paginator = Paginator(newsListRaw, 100)
    page = request.GET.get('page')
    totalPages = paginator.num_pages
    try:
        newsList = paginator.page(page)
    except PageNotAnInteger:
        newsList = paginator.page(1)
    except EmptyPage:
        newsList = paginator.page(totalPages)

    try:
        if int(page) > totalPages:
            messages.error(request, 'Invalid Page Number.')
            page = 1
    except:
        pass

    try:
        blogNewsListingDMInst = blogWebNewsListingDM.objects.latest('-id')
    except:
        blogNewsListingDMInst = None

    try:
        blogNewsHeadingDMInst = newsHeadingWebDM.objects.latest('-id')
    except:
        blogNewsHeadingDMInst = None
    createblogNewsWebHeadingDM = newsHeadingWebDMForm(instance=blogNewsHeadingDMInst)

    context = {
        'flag': flag,
        'newsList': newsList,
        'page': page,
        'blogNewsListingDMInst': blogNewsListingDMInst,
        'blogNewsHeadingDMInst': blogNewsHeadingDMInst,
        'createblogNewsWebHeadingDM': createblogNewsWebHeadingDM,
        'searchPage': searchPage,
        'totalPages': totalPages,
    }
    return render(request, 'news/UI/newsList.html', context)


class crawledNewsViewAPIViews(APIView):
    paginator = StandardResultsSetPagination()

    def get_paginated_response(self, data):
        assert self.paginator is not None
        return self.paginator.get_paginated_response(data)

    def get(self, request, formate=None):
        searchPage = False
        searchQuery = request.GET.get('searchq')
        with connections['cralwer'].cursor() as cursor:
            status = "'published'"
            if searchQuery:
                searchPage = True
                searchQuery = searchQuery.replace("'", "\\'")
                queryToSearch = "'%" + searchQuery + "%'"
                query = 'Select * from "crawlApp_googlenewsstore" \
				where status=' + status + ' AND (title ILIKE E' + queryToSearch + ' OR "desc" ILIKE E' + queryToSearch + ' OR site ILIKE E' + queryToSearch + ') ORDER BY date DESC;'
            else:
                query = 'select * from "crawlApp_googlenewsstore" where status=' + status + ' ORDER BY date DESC'
            cursor.execute(query)
            newsListRaw = dictfetchall(cursor)
        flag = 'crawled'

        try:
            blogNewsListingDMInst = blogWebNewsListingDM.objects.latest('-id')
        except:
            blogNewsListingDMInst = None

        try:
            blogNewsHeadingDMInst = newsHeadingWebDM.objects.latest('-id')
        except:
            blogNewsHeadingDMInst = None

        context = {
            'flag': str(flag),
            'blogNewsListingDMInst': str(blogNewsListingDMInst),
            'blogNewsHeadingDMInst': str(blogNewsHeadingDMInst),
            'searchPage': str(searchPage),
        }
        context = self.paginator.paginate_queryset(newsListRaw, request)
        return self.get_paginated_response(context)


#
def blogNewsView(request):
    if request.method == 'POST':
        methodType = request.POST.get('submitType')
        redirectTo = request.POST.get('requestFrom')
        if methodType == 'new':
            objlnst = None
        else:
            pkID = request.POST.get('dataID')
            objlnst = get_object_or_404(blogNews, pk=pkID)
        objForm = blogNewsForm(request.POST, request.FILES, instance=objlnst)
        if objForm.is_valid():
            cd = objForm.save(commit=False)
            if request.user.is_authenticated:
                cd.author = request.user
            cd.save()
            objForm.save_m2m()
            cd.refresh_from_db()
            messages.success(request, 'Blog Article Sent For Verification')
        else:
            messages.error(request, 'Please Check An Error occurred')
        return redirect(redirectTo)
    return HttpResponse('Invalid Entry')


#
def deleteFKdataView(request):
    if request.method == 'POST':
        deletePK = request.POST.get('deleteDataID')
        deleteFrom = request.POST.get('deleteFlag')
        requestedPage = request.POST.get('redirectTo')
        if deleteFrom == 'blogNews':
            try:
                objInst = blogNews.objects.get(pk=deletePK)
                objInst.delete()
                messages.success(request, 'Data Deleted')
            except:
                messages.error(request, 'Please Try Again Later')
        return redirect(requestedPage)
    return HttpResponse('Invalid Entry Point')


#
def newsHeadingDMView(request):
    if request.method == 'POST':
        methodType = request.POST.get('submitType')
        redirectTo = request.POST.get('requestFrom')
        if methodType == 'new':
            objlnst = None
        else:
            pkID = request.POST.get('dataID')
            objlnst = get_object_or_404(newsHeadingDM, pk=pkID)

        objForm = newsHeadingDMForm(request.POST, request.FILES, instance=objlnst)

        if objForm.is_valid():
            cd = objForm.save(commit=False)
            if request.user.is_authenticated:
                cd.analyst = request.user
            cd.save()
            cd.refresh_from_db()
            messages.success(request, 'Blog Detail Sent For Verification')
        else:
            messages.error(request, 'Please Check An Error occurred')
        return redirect(redirectTo)
    return HttpResponse('Invalid Entry')


#
def newsWebHeadingDMView(request):
    if request.method == 'POST':
        methodType = request.POST.get('submitType')
        redirectTo = request.POST.get('requestFrom')
        if methodType == 'new':
            objlnst = None
        else:
            pkID = request.POST.get('dataID')
            objlnst = get_object_or_404(newsHeadingWebDM, pk=pkID)

        objForm = newsHeadingWebDMForm(request.POST, request.FILES, instance=objlnst)

        if objForm.is_valid():
            cd = objForm.save(commit=False)
            if request.user.is_authenticated:
                cd.analyst = request.user
            cd.save()
            cd.refresh_from_db()
            messages.success(request, 'Blog Detail sssSent For Verification')
        else:
            messages.error(request, 'Please Check An Error occurred')
        return redirect(redirectTo)
    return HttpResponse('Invalid Entry')


class feedDescriptionApiView(APIView):
    def get(self, request, pk=None):
        id = pk
        if id is not None:
            data = blogNews.objects.get(id=id)
            serializer = feedDescriptionSerializer(data)
            return Response(serializer.data)
