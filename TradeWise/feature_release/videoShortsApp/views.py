from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from django.contrib import messages
import datetime
from taggit.models import Tag
from django.db.models import Q
from planifyMain.paginators import StandardResultsSetPagination
from .forms import *
from .models import *
from django.db.models.functions import TruncMonth
from .serializers import *
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import authentication
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from rest_framework.filters import SearchFilter
from rest_framework import serializers
from rest_framework import viewsets
from rest_framework import status
from rest_framework.filters import OrderingFilter


#


def searchBarView(request):
    query = request.GET.get('searchq')
    shortsObj = blogVideosShorts.objects.all().order_by('-releaseDate')
    dataList = {}
    if query:
        shortsSearchObj = shortsObj.filter(
            Q(title__icontains=query) | Q(content1__icontains=query) | Q(content2__icontains=query) | Q(
                content3__icontains=query) | Q(content4__icontains=query) | Q(content5__icontains=query)).distinct()
        latestVidShrtBlog = shortsSearchObj.first()
        dataList[query] = shortsSearchObj
    else:
        latestVidShrtBlog = shortsObj.first()
        dataList[query] = shortsObj
    return render(request, 'videoShorts/UI/shortsList.html',
                  {'latestVidShrtBlog': latestVidShrtBlog, 'dataList': dataList, 'query': query})


#


def shortsListView(request):
    createShortsCategoryOptions = videoShortsCategoryOptionsForm()
    createShortsSubCategoryOptions = videoShortsSubCategoryOptionsForm()
    createVideosShorts = blogVideosShortsForm()
    try:
        latestVidShrtBlog = blogVideosShorts.objects.filter(
            releaseDate__isnull=False).latest('releaseDate')
    except:
        latestVidShrtBlog = None
    categoryOpt = videoShortsCategoryOptions.objects.all()
    shortsVideo = blogVideosShorts.objects.all().order_by('-releaseDate')
    featuredShorts = shortsVideo.filter(featuredShots='Yes')[:3]
    months = shortsVideo.datetimes("releaseDate", kind="month")
    months = sorted(months, reverse=True)
    # years = shortsVideo.datetimes("releaseDate", kind="year")
    # years = sorted(years, reverse=True)
    dataList = {}
    dataListExtra = {}
    forCounter = 0
    for month in months:
        forCounter += 1
        queryMonth = month.month
        queryYear = month.year
        if forCounter < 4:
            month_Videos = shortsVideo.filter(
                releaseDate__month=queryMonth, releaseDate__year=queryYear)
            dataList[month] = month_Videos
        else:
            month_Videos = shortsVideo.filter(
                releaseDate__month=queryMonth, releaseDate__year=queryYear)
            dataListExtra[month] = month_Videos
    tags = blogVideosShorts.tags.most_common()[:5]

    try:
        blogShortsListingDMInst = blogShortsListingDM.objects.latest('-id')
    except:
        blogShortsListingDMInst = None
    createblogShortsListingDM = blogShortsListingDMForm(
        instance=blogShortsListingDMInst)
    slug = 'home'

    try:
        blogShortsHeadingDMInst = shortsHeadingDM.objects.latest('-id')
    except:
        blogShortsHeadingDMInst = None
    createblogShortsHeadingDM = shortsHeadingDMForm(
        instance=blogShortsHeadingDMInst)

    context = {
        'latestVidShrtBlog': latestVidShrtBlog,
        'categoryOpt': categoryOpt,
        'dataListExtra': dataListExtra,
        'tags': tags,
        'dataList': dataList,
        'createShortsCategoryOptions': createShortsCategoryOptions,
        'createShortsSubCategoryOptions': createShortsSubCategoryOptions,
        'createVideosShorts': createVideosShorts,
        'blogShortsListingDMInst': blogShortsListingDMInst,
        'createblogShortsListingDM': createblogShortsListingDM,
        'blogShortsHeadingDMInst': blogShortsHeadingDMInst,
        'createblogShortsHeadingDM': createblogShortsHeadingDM,
        'slug': slug,
        'featuredShorts': featuredShorts,
    }
    return render(request, 'videoShorts/UI/shortsList.html', context)


#

class shortsListViewAPIViews(APIView):
    serializer_class = shortsListSerializer
    permission_classes = [AllowAny]
    pagination_class = StandardResultsSetPagination
    filter_backends = [OrderingFilter]
    ordering = ['-releaseDate']

    @property
    def paginator(self):
        if not hasattr(self, '_paginator'):
            if self.pagination_class is None:
                self._paginator = None
            else:
                self._paginator = self.pagination_class()
        return self._paginator

    def paginate_queryset(self, queryset):
        if self.paginator is None:
            return None
        return self.paginator.paginate_queryset(queryset, self.request, view=self)

    def get_paginated_response(self, data):
        assert self.paginator is not None
        return self.paginator.get_paginated_response(data)

    def get(self, request):
        queryset = blogVideosShorts.objects.exclude(releaseDate=None).distinct().order_by('-releaseDate')
        page = self.paginate_queryset(queryset)
        serializer = self.serializer_class(page, many=True)
        return self.get_paginated_response(serializer.data)

    def post(self, request, formate=None):
        serializer = shortsListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


def shortsDetailView(request, slug=None):
    createVideoShortsDetailed = blogVideosShortsDetailedForm()
    obj = get_object_or_404(blogVideosShorts, slug=slug)
    similarVids = None
    requestFrom = request.GET.get('category')
    if requestFrom:
        similarVids = blogVideosShorts.objects.filter(
            category=requestFrom).order_by('-created')[0:3]
    try:
        blogShortsDetailedDMInst = blogShortsDetailedDM.objects.get(
            blogProfileName=obj)
    except:
        blogShortsDetailedDMInst = None
    createblogShortsDetailedDM = blogShortsDetailedDMForm(
        instance=blogShortsDetailedDMInst)

    context = {
        'createVideoShortsDetailed': createVideoShortsDetailed,
        'obj': obj,
        'similarVids': similarVids,
        'blogShortsDetailedDMInst': blogShortsDetailedDMInst,
        'createblogShortsDetailedDM': createblogShortsDetailedDM,
    }
    return render(request, 'videoShorts/UI/shortsDetail.html', context)


#


def blogShortsDMView(request):
    if request.method == 'POST':
        methodType = request.POST.get('submitType')
        redirectTo = request.POST.get('requestFrom')
        adminRequest = request.GET.get('requestFrom')
        parentProfile = None
        if methodType == 'new':
            objlnst = None
        else:
            pkId = request.POST.get('dataID')

        if adminRequest == 'blogShortsListing':
            if methodType == 'new':
                objlnst = None
            else:
                objlnst = get_object_or_404(blogShortsListingDM, pk=pkId)
            objForm = blogShortsListingDMForm(
                request.POST, request.FILES, instance=objlnst)

        elif adminRequest == 'blogShortsDetail':
            if methodType == 'new':
                parentID = request.POST.get('blogProfileName')
                parentProfile = get_object_or_404(
                    blogVideosShorts, pk=parentID)
            else:
                objlnst = get_object_or_404(blogShortsDetailedDM, pk=pkId)
            objForm = blogShortsDetailedDMForm(
                request.POST, request.FILES, instance=objlnst)

        if objForm.is_valid():
            cd = objForm.save(commit=False)
            if methodType == 'new' and parentProfile:
                cd.blogProfileName = parentProfile
            if request.user.is_authenticated:
                cd.analyst = request.user
            cd.save()
            objForm.save_m2m()
            cd.refresh_from_db()
            messages.success(request, 'Blog Shorts DM Sent For Verification')
        else:
            messages.error(request, 'Please Check An Error occurred')
        return redirect(redirectTo)
    return HttpResponse('Invalid Entry')


#


def videoShortsCategoryOptionsView(request):
    if request.method == 'POST':
        methodType = request.POST.get('submitType')
        redirectTo = request.POST.get('requestFrom')
        if methodType == 'new':
            objlnst = None
        else:
            pkID = request.POST.get('dataID')
            objlnst = get_object_or_404(videoShortsCategoryOptions, pk=pkID)
        objForm = videoShortsCategoryOptionsForm(
            request.POST, instance=objlnst)
        if objForm.is_valid():
            cd = objForm.save(commit=False)
            if request.user.is_authenticated:
                cd.analyst = request.user
            cd.save()
            cd.refresh_from_db()
            messages.success(request, 'Blog Shorts Sent For Verification')
        else:
            messages.error(request, 'Please Check An Error occurred')
        return redirect(redirectTo)
    return HttpResponse('Invalid Entry')


#


def videoShortsSubCategoryOptionsView(request):
    if request.method == 'POST':
        methodType = request.POST.get('submitType')
        redirectTo = request.POST.get('requestFrom')
        if methodType == 'new':
            objlnst = None
        else:
            pkID = request.POST.get('dataID')
            objlnst = get_object_or_404(videoShortsSubCategoryOptions, pk=pkID)

        objForm = videoShortsSubCategoryOptionsForm(
            request.POST, instance=objlnst)

        if objForm.is_valid():
            cd = objForm.save(commit=False)
            if request.user.is_authenticated:
                cd.analyst = request.user
            cd.save()
            cd.refresh_from_db()
            messages.success(request, 'Blog Shorts Sent For Verification')
        else:
            messages.error(request, 'Please Check An Error occurred')
        return redirect(redirectTo)
    return HttpResponse('Invalid Entry')


#


def blogVideosShortsView(request):
    if request.method == 'POST':
        methodType = request.POST.get('submitType')
        redirectTo = request.POST.get('requestFrom')
        if methodType == 'new':
            objlnst = None
        else:
            pkID = request.POST.get('dataID')
            objlnst = get_object_or_404(blogVideosShorts, pk=pkID)

        objForm = blogVideosShortsForm(
            request.POST, request.FILES, instance=objlnst)

        if objForm.is_valid():
            cd = objForm.save(commit=False)
            if request.user.is_authenticated:
                cd.analyst = request.user
            cd.save()
            objForm.save_m2m()
            cd.refresh_from_db()
            messages.success(request, 'Video Shorts Sent For Verification')
        else:
            messages.error(request, 'Please Check An Error occurred')
        return redirect(redirectTo)
    return HttpResponse('Invalid Entry')


#


def blogVideosShortsDetailedView(request):
    if request.method == 'POST':
        methodType = request.POST.get('submitType')
        redirectTo = request.POST.get('requestFrom')
        if methodType == 'new':
            objlnst = None
        else:
            pkID = request.POST.get('dataID')
            objlnst = get_object_or_404(blogVideosShorts, pk=pkID)

        objForm = blogVideosShortsDetailedForm(
            request.POST, request.FILES, instance=objlnst)

        if objForm.is_valid():
            cd = objForm.save(commit=False)
            if request.user.is_authenticated:
                cd.analyst = request.user
            cd.save()
            cd.refresh_from_db()
            messages.success(
                request, 'Blog Shorts Detail Sent For Verification')
        else:
            messages.error(request, 'Please Check An Error occurred')
        return redirect(redirectTo)
    return HttpResponse('Invalid Entry')


#


def tagList(request, tag_slug=None):
    object_list = blogVideosShorts.published.all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        object_list = object_list.filter(tags__in=[tag])
    return render(request, 'videoShorts/UI/shortsList.html', {'tag': tag, 'object_list': object_list})


#


def deleteFKdataView(request):
    if request.method == 'POST':
        deletePK = request.POST.get('deleteDataID')
        deleteFrom = request.POST.get('deleteFlag')
        requestedPage = request.POST.get('redirectTo')
        if deleteFrom == 'blogVideosShorts':
            try:
                objInst = blogVideosShorts.objects.get(pk=deletePK)
                objInst.delete()
                messages.success(request, 'Data Deleted')
            except:
                messages.error(request, 'Please Try Again Later')
        return redirect(requestedPage)
    return HttpResponse('Invalid Entry Point')


#


def tagBasedVideosShortsView(request, slug=None):
    tag = None
    tags = blogVideosShorts.tags.most_common()[:5]
    categoryOpt = videoShortsCategoryOptions.objects.all()
    dataList = {}
    if slug:
        try:
            tag = Tag.objects.get(slug=slug)
            videoShorts = blogVideosShorts.objects.filter(
                tags__in=[tag]).order_by('-releaseDate')
            latestVidShrtBlog = videoShorts.first()
            dataList[tag] = videoShorts
        except:
            # messages.error(request, 'Bad request!')
            # return redirect('videoShortsApp:shortsListURL')
            return redirect('render404PageUrl')
    else:
        return redirect('render404PageUrl')
    context = {
        'tags': tags,
        'categoryOpt': categoryOpt,
        'dataList': dataList,
        'latestVidShrtBlog': latestVidShrtBlog,
    }
    return render(request, 'videoShorts/UI/shortsList.html', context)


#


def shortsHeadingDMView(request):
    if request.method == 'POST':
        methodType = request.POST.get('submitType')
        redirectTo = request.POST.get('requestFrom')
        if methodType == 'new':
            objlnst = None
        else:
            pkID = request.POST.get('dataID')
            objlnst = get_object_or_404(shortsHeadingDM, pk=pkID)

        objForm = shortsHeadingDMForm(
            request.POST, request.FILES, instance=objlnst)

        if objForm.is_valid():
            cd = objForm.save(commit=False)
            if request.user.is_authenticated:
                cd.analyst = request.user
            cd.save()
            cd.refresh_from_db()
            messages.success(request, 'Shorts Detail Sent For Verification')
        else:
            messages.error(request, 'Please Check An Error occurred')
        return redirect(redirectTo)
    return HttpResponse('Invalid Entry')
