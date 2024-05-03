from urllib import response
from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from django.contrib import messages
import datetime
from django.db.models import Q
from taggit.models import Tag
from django.db.models import Count
from django.contrib.admin.views.decorators import staff_member_required
from .forms import *
from .models import *
from dmFormsApp.models import metaDetailForDM
from planifyMain.paginators import StandardResultsSetPagination
from .serializers import *
from videoBlogApp.services.video import VideoService
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from rest_framework.decorators import api_view


#
def searchBarView(request):
    query = request.GET.get('searchq')
    videoObj = blogVideos.objects.all().order_by('-releasedDate')
    dataList = {}
    if query:
        videoSearchObj = videoObj.filter(Q(title__icontains=query) | Q(content__icontains=query)).distinct()
        latestVidBlog = videoSearchObj.first()
        dataList[query] = videoSearchObj
    else:
        latestVidBlog = videoObj.first()
        dataList[query] = videoObj
    return render(request, 'videoBlog/UI/videoList.html',
                  {'latestVidBlog': latestVidBlog, 'dataList': dataList, 'query': query})


#
def genericForms(requestFrom=None):
    createCategoryOptions = categoryOptionsForm()
    createSubCategoryOptions = subCategoryOptionsForm()
    createBlogVideos = blogVideosForm()
    createGenericData = videoBlogGenericDataForm()
    return createCategoryOptions, createSubCategoryOptions, createBlogVideos, createGenericData


#
def blogVideoLatestByReleaseDate():
    try:
        latestVidBlog = blogVideos.objects.filter(releasedDate__isnull=False).latest('releasedDate')
    except:
        latestVidBlog = None
    return latestVidBlog


#
def videoListView(request):
    if request.user.is_staff:
        createCategoryOptions, createSubCategoryOptions, createBlogVideos, createGenericData = genericForms(
            'videoListPage')
    else:
        createCategoryOptions = createSubCategoryOptions = createBlogVideos = createGenericData = None
    latestVidBlog = blogVideoLatestByReleaseDate()
    try:
        genericDataInst = videoBlogGenericData.objects.latest('id')
    except:
        genericDataInst = None

    tags = blogVideos.tags.most_common()[:10]
    dataList = {}
    categoryOpt = categoryOptions.objects.all()
    mainForCount = 0
    try:
        sectionOrderingInst = blogPageSectionsOrdering.objects.get(pk=1)
    except:
        sectionOrderingInst = None
    for cats in sectionOrderingInst.displayedCategories.all():
        videoOnCatBasis = blogVideos.objects.filter(category=cats).order_by('-releasedDate')[0:3]
        dataList[cats] = videoOnCatBasis

    for subCats in sectionOrderingInst.displayedSubCategories.all():
        videoOnSubCatBasis = blogVideos.objects.filter(subCategory=subCats).order_by('-releasedDate')[0:3]
        dataList[subCats] = videoOnSubCatBasis

    catsSubCatsDict = {}
    for cats in categoryOpt:
        subCats = subCategoryOptions.objects.filter(category=cats)
        catsSubCatsDict[cats] = subCats
    try:
        blogVideoListingDMInst = blogVideoListingDM.objects.latest('-id')
    except:
        blogVideoListingDMInst = None
    createblogVideoListingDM = blogVideoListingDMForm(instance=blogVideoListingDMInst)
    slug = 'home'

    try:
        blogVideoHeadingDMInst = videosHeadingDM.objects.latest('-id')
    except:
        blogVideoHeadingDMInst = None
    createblogVideoHeadingDM = videosHeadingDMForm(instance=blogVideoHeadingDMInst)
    homeFlag = True

    context = {
        'createCategoryOptions': createCategoryOptions,
        'createSubCategoryOptions': createSubCategoryOptions,
        'createBlogVideos': createBlogVideos,
        'createGenericData': createGenericData,
        'categoryOpt': categoryOpt,
        'tags': tags,
        'dataList': dataList,
        'genericDataInst': genericDataInst,
        'latestVidBlog': latestVidBlog,
        'catsSubCatsDict': catsSubCatsDict,
        'sectionOrderingInst': sectionOrderingInst,
        'blogVideoListingDMInst': blogVideoListingDMInst,
        'createblogVideoListingDM': createblogVideoListingDM,
        'slug': slug,
        'blogVideoHeadingDMInst': blogVideoHeadingDMInst,
        'createblogVideoHeadingDM': createblogVideoHeadingDM,
        'homeFlag': homeFlag,
    }
    return render(request, 'videoBlog/UI/videoList.html', context)


class videoListApiView(generics.ListAPIView):
    queryset = blogVideos.objects.all().distinct()
    serializer_class = blogVideosSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['title', 'slug', 'category', 'subCategory',
                        'relatedResearchReports__stockProfileNameSE__category']
    search_fields = ['title', 'category__name', 'relatedResearchReports__stockName']
    ordering = ['-publish']

    @method_decorator(cache_page(60 * 60 * 24))
    def get(self, *args, **kwargs):
        if args[0].GET.get('stockCategory'):
            args[0].GET['relatedResearchReports__stockProfileNameSE__category'] = args[0].GET.get('stockCategory')
        return super().get(*args, **kwargs)


#
def themeVideoList(request, slug=None):
    latestVidBlog = None
    if request.user.is_staff:
        createCategoryOptions, createSubCategoryOptions, createBlogVideos, createGenericData = genericForms(
            'videoListPage')
    else:
        createCategoryOptions = createSubCategoryOptions = createBlogVideos = createGenericData = None
    tags = blogVideos.tags.most_common()[:5]
    dataList = {}
    categoryOpt = categoryOptions.objects.all()
    categoryObjs = None
    if slug:
        try:
            markData = marketingData.objects.latest('id')
        except:
            markData = None
        if slug == 'trending':
            try:
                xDays = markData.daysForTrending
            except:
                xDays = 30
            videoListByCount = list(videoBlogHits.objects.filter(created__lte=datetime.datetime.today(), \
                                                                 created__gt=datetime.datetime.today() - datetime. \
                                                                 timedelta(days=xDays)).values('videoBlog').annotate(
                Count('videoBlog')).order_by('-videoBlog__count'))
            items = []
            flaga = True
            for item in videoListByCount:
                for key, value in item.items():
                    if key == 'videoBlog':
                        blog = get_object_or_404(blogVideos, pk=value)
                        items.append(blog)
                        if flaga:
                            latestVidBlog = blog
                        flaga = False
            dataList['Trending'] = items
        elif slug == 'explore':
            maxLimitForExplore = marketingData.objects.latest('id')
            maxLimit = maxLimitForExplore.maxLimitForExplore
            items = blogVideos.objects.filter(explore='Yes').order_by('-releasedDate')[:maxLimit]
            # latestVidBlog = items.first()  #explore first
            latestVidBlog = blogVideoLatestByReleaseDate()  # database first
            dataList['Explore'] = items
        elif slug == 'popular':
            try:
                hitCount = markData.hitCountPopular
            except:
                hitCount = 10000
            videoListByCount = list(
                videoBlogHits.objects.values('videoBlog').annotate(Count('videoBlog')).order_by('-videoBlog__count'))
            items = []
            flaga = True
            for item in videoListByCount:
                if item['videoBlog__count'] >= hitCount:
                    blog = get_object_or_404(blogVideos, pk=item['videoBlog'])
                    items.append(blog)
                    if flaga:
                        latestVidBlog = blog
                    flaga = False
            dataList['Popular'] = items
        elif slug == 'latest':
            latestVidBlog = blogVideoLatestByReleaseDate()
            try:
                latestBy = markData.latestByDate
            except:
                latestBy = 30
            items = blogVideos.objects.filter(
                publish__gte=datetime.datetime.today() - datetime.timedelta(latestBy)).order_by('-releasedDate')
            dataList['Latest'] = items
        elif slug == 'all' or None:
            items = blogVideos.objects.all().order_by('-releasedDate')
            latestVidBlog = items.first()
            dataList['All'] = items
    else:
        categoryObjs = categoryOpt
    if categoryObjs:
        for item in categoryObjs:
            blogVideo = blogVideos.objects.filter(category=item).order_by('-created')
            dataList[item] = blogVideo
    context = {
        'createCategoryOptions': createCategoryOptions,
        'createSubCategoryOptions': createSubCategoryOptions,
        'createBlogVideos': createBlogVideos,
        'createGenericData': createGenericData,
        'tags': tags,
        'categoryOpt': categoryOpt,
        'slug': slug,
        'latestVidBlog': latestVidBlog,
        'dataList': dataList,
    }
    return render(request, 'videoBlog/UI/videoList.html', context)


#
def tagBasedVideosView(request, slug=None):
    if request.user.is_staff:
        createCategoryOptions, createSubCategoryOptions, createBlogVideos, createGenericData = genericForms(
            'videoListPage')
    else:
        createCategoryOptions = createSubCategoryOptions = createBlogVideos = createGenericData = None
    tag = None
    tags = blogVideos.tags.most_common()[:5]
    categoryOpt = categoryOptions.objects.all()
    dataList = {}
    if slug:
        tag = get_object_or_404(Tag, slug=slug)
        blogVideo = blogVideos.objects.filter(tags__in=[tag]).order_by('-created')
        latestVidBlog = blogVideo.first()
        dataList[tag] = blogVideo
    else:
        return redirect('videoBlogApp:videoListURL')
    context = {
        'createCategoryOptions': createCategoryOptions,
        'createSubCategoryOptions': createSubCategoryOptions,
        'createBlogVideos': createBlogVideos,
        'createGenericData': createGenericData,
        'tags': tags,
        'categoryOpt': categoryOpt,
        'dataList': dataList,
        'latestVidBlog': latestVidBlog,
    }
    return render(request, 'videoBlog/UI/videoList.html', context)


#
def categoryBasedVideosView(request, slug=None):
    if request.user.is_staff:
        createCategoryOptions, createSubCategoryOptions, createBlogVideos, createGenericData = genericForms(
            'videoListPage')
    else:
        createCategoryOptions = createSubCategoryOptions = createBlogVideos = createGenericData = None
    tags = blogVideos.tags.most_common()[:5]
    categoryOpt = categoryOptions.objects.all()
    dataList = {}
    if slug:
        try:
            item = categoryOptions.objects.get(slug=slug)
        except:
            item = None
        if item:
            blogVideo = blogVideos.objects.filter(category=item).order_by('-releasedDate')
            latestVidBlog = blogVideo.first()
            dataList[item] = blogVideo
        else:
            messages.error(request, 'Bad Request!')
            return redirect('videoBlogApp:videoListURL')
    else:
        return redirect('videoBlogApp:videoListURL')
    context = {
        'createCategoryOptions': createCategoryOptions,
        'createSubCategoryOptions': createSubCategoryOptions,
        'createBlogVideos': createBlogVideos,
        'createGenericData': createGenericData,
        'tags': tags,
        'categoryOpt': categoryOpt,
        'dataList': dataList,
        'latestVidBlog': latestVidBlog,
    }
    return render(request, 'videoBlog/UI/videoList.html', context)


#
def subCategoryBasedVideosView(request, slug=None):
    if request.user.is_staff:
        createCategoryOptions, createSubCategoryOptions, createBlogVideos, createGenericData = genericForms(
            'videoListPage')
    else:
        createCategoryOptions = createSubCategoryOptions = createBlogVideos = createGenericData = None
    tags = blogVideos.tags.most_common()[:5]
    categoryOpt = categoryOptions.objects.all()
    dataList = {}
    if slug:
        try:
            item = subCategoryOptions.objects.get(slug=slug)
        except:
            item = None
        if item:
            blogVideo = blogVideos.objects.filter(subCategory=item).order_by('-releasedDate')
            latestVidBlog = blogVideo.first()
            dataList[item] = blogVideo
        else:
            messages.error(request, 'Bad Request!')
            return redirect('videoBlogApp:videoListURL')
    else:
        return redirect('videoBlogApp:videoListURL')
    context = {
        'createCategoryOptions': createCategoryOptions,
        'createSubCategoryOptions': createSubCategoryOptions,
        'createBlogVideos': createBlogVideos,
        'createGenericData': createGenericData,
        'tags': tags,
        'categoryOpt': categoryOpt,
        'dataList': dataList,
        'latestVidBlog': latestVidBlog,
    }
    return render(request, 'videoBlog/UI/videoList.html', context)


#
def updateHits(hitPage, hitBy=None, requestFrom=None):
    if requestFrom == 'videoDetail':
        cd = videoBlogHits.objects.create(videoBlog=hitPage, hitBy=hitBy)
        cd.save()


#
def videoDetailView(request, slug):
    blogVideo = get_object_or_404(blogVideos, slug=slug)

    createBlogDetailedVideos = blogVideosDetailedForm()
    similarVids = None
    requestFrom = request.GET.get('category')
    obj = get_object_or_404(blogVideos, slug=slug)
    if request.user.is_authenticated:
        updateHits(obj, request.user, 'videoDetail')
    else:
        updateHits(obj, None, 'videoDetail')
    if requestFrom:
        similarVids = blogVideos.objects.filter(category=requestFrom).order_by('-created')[0:3]

    try:
        blogVideoDetailedDMInst = metaDetailForDM.objects.get(video_blog=blogVideo)
    except:
        blogVideoDetailedDMInst = None
    createblogVideoDetailedDM = blogVideoDeatiledDMForm(instance=blogVideoDetailedDMInst)
    context = {
        'obj': obj,
        'createBlogDetailedVideos': createBlogDetailedVideos,
        'similarVids': similarVids,
        'blogVideoDetailedDMInst': blogVideoDetailedDMInst,
        'createblogVideoDetailedDM': createblogVideoDetailedDM,
    }
    print("@@@@@@@@@@@@@@@@@@@@@@@@", context)
    return render(request, 'videoBlog/UI/videoDetail.html', context)


class videoDetailAPIView(APIView):
    def get(self, request, pk=None, format=None):
        if pk is not None:
            item = blogVideos.objects.filter(id=pk).first()
            serializer = blogVideosDetailedSerializer(item)
            data = serializer.data
            data["tags"] = metaDetailForDM.meta_tags.most_common().values()[:13]
            data["category"] = categoryOptions.objects.filter(id__in=data["category"]).values('id', 'name', 'slug') if \
                data["category"] else []
            return Response({'data': data, 'status': True})
        else:
            return Response({'data': None, 'status': False})


class VideoScreenCategoryList(APIView):
    def get(self, request):
        category_options = [{"Label": "Startup Up", "Value": "Startups"},
                            {"Label": "PreIPO", "Value": "PreIPO"},
                            {"Label": "Upcoming", "Value": "Upcoming IPO"},
                            {"Label": "Seed Funding", "Value": "Seed Funding"},
                            {"Label": "Unicorns", "Value": "Unicorns"},
                            {"Label": "Ideas", "Value": "Ideas"},
                            {"Label": "Market News", "Value": "Market News & Economy"},
                            {"Label": "Interviews", "Value": "Interviews - Young Entrepreneurs"},
                            {"Label": "Recommendations", "Value": "Stock Recommendations"},
                            {"Label": "Beginner Guide", "Value": "Beginner Guide - Funding"},
                            {"Label": "Beginner Guide", "Value": "Beginner Guide - PreIPO"},
                            {"Label": "ESOP", "Value": "Employee Stock Options - ESOP"},
                            {"Label": "Large Cap", "Value": "Large Cap"},
                            {"Label": "Mid Cap", "Value": "Mid Cap"},
                            {"Label": "Small Cap", "Value": "Small Cap"},
                            {"Label": "Micro Cap", "Value": "Micro Cap"},
                            {"Label": "Delisted Stock", "Value": "Delisted Stock"},
                            {"Label": "LSE", "Value": "Listed on Small Exchange - Suspended/Liquidation Phase - LSE"},
                            {"Label": "Listed Stocks", "Value": "Listed Stocks"},
                            {"Label": "Diversified Stocks", "Value": "Diversified Stocks"},
                            {"Label": "Channel Partner", "Value": "Channel Partner Videos"},
                            {"Label": "Financial Planning", "Value": "Financial Planning"},
                            {"Label": "Investment Strategy", "Value": "Investment Strategy"},
                            ]
        return Response(category_options)


#
def categoryOptionsView(request):
    if request.method == 'POST':
        methodType = request.POST.get('submitType')
        redirectTo = request.POST.get('requestFrom')
        if methodType == 'new':
            objlnst = None
        else:
            pkID = request.POST.get('dataID')
            objlnst = get_object_or_404(categoryOptions, pk=pkID)
        objForm = categoryOptionsForm(request.POST, instance=objlnst)
        if objForm.is_valid():
            cd = objForm.save(commit=False)
            if request.user.is_authenticated:
                cd.analyst = request.user
            cd.save()
            cd.refresh_from_db()
            messages.success(request, 'Blog Video Sent For Verification')
        else:
            messages.error(request, 'Please Check An Error occurred')
        return redirect(redirectTo)
    return HttpResponse('Invalid Entry')


#
def subCategoryOptionsView(request):
    if request.method == 'POST':
        methodType = request.POST.get('submitType')
        redirectTo = request.POST.get('requestFrom')
        if methodType == 'new':
            objlnst = None
        else:
            pkID = request.POST.get('dataID')
            objlnst = get_object_or_404(subCategoryOptions, pk=pkID)

        objForm = subCategoryOptionsForm(request.POST, instance=objlnst)

        if objForm.is_valid():
            cd = objForm.save(commit=False)
            if request.user.is_authenticated:
                cd.analyst = request.user
            cd.save()
            cd.refresh_from_db()
            messages.success(request, 'Blog Video Sent For Verification')
        else:
            messages.error(request, 'Please Check An Error occurred')
        return redirect(redirectTo)
    return HttpResponse('Invalid Entry')


#
def blogVideosView(request):
    if request.method == 'POST':
        methodType = request.POST.get('submitType')
        redirectTo = request.POST.get('requestFrom')
        if methodType == 'new':
            objlnst = None
        else:
            pkID = request.POST.get('dataID')
            objlnst = get_object_or_404(blogVideos, pk=pkID)

        objForm = blogVideosForm(request.POST, request.FILES, instance=objlnst)

        if objForm.is_valid():
            cd = objForm.save(commit=False)
            if request.user.is_authenticated:
                cd.analyst = request.user
            cd.save()
            objForm.save_m2m()
            cd.refresh_from_db()
            messages.success(request, 'Blog Video Sent For Verification')
        else:
            messages.error(request, 'Please Check An Error occurred')
        return redirect(redirectTo)
    return HttpResponse('Invalid Entry')


#
def blogVideoListingDMView(request):
    if request.method == 'POST':
        methodType = request.POST.get('submitType')
        redirectTo = request.POST.get('requestFrom')
        adminRequest = request.GET.get('requestFrom')
        parentProfile = None
        if methodType == 'new':
            objlnst = None
        else:
            pkId = request.POST.get('dataID')

        if adminRequest == 'blogVideosListing':
            if methodType == 'new':
                objlnst = None
            else:
                objlnst = get_object_or_404(blogVideoListingDM, pk=pkId)
            objForm = blogVideoListingDMForm(request.POST, request.FILES, instance=objlnst)

        elif adminRequest == 'blogVideosDetail':
            if methodType == 'new':
                parentID = request.POST.get('blogProfileName')
                parentProfile = get_object_or_404(blogVideos, pk=parentID)
            else:
                objlnst = get_object_or_404(blogVideoDetailedDM, pk=pkId)
            objForm = blogVideoDeatiledDMForm(request.POST, request.FILES, instance=objlnst)

        if objForm.is_valid():
            cd = objForm.save(commit=False)
            if methodType == 'new' and parentProfile:
                cd.blogProfileName = parentProfile
            if request.user.is_authenticated:
                cd.analyst = request.user
            cd.save()
            objForm.save_m2m()
            cd.refresh_from_db()
            messages.success(request, 'Blog Video DM Sent For Verification')
        else:
            messages.error(request, 'Please Check An Error occurred')
        return redirect(redirectTo)
    return HttpResponse('Invalid Entry')


#
def blogVideosDetailedView(request):
    if request.method == 'POST':
        methodType = request.POST.get('submitType')
        redirectTo = request.POST.get('requestFrom')
        if methodType == 'new':
            objlnst = None
        else:
            pkID = request.POST.get('dataID')
            objlnst = get_object_or_404(blogVideos, pk=pkID)

        objForm = blogVideosDetailedForm(request.POST, request.FILES, instance=objlnst)

        if objForm.is_valid():
            cd = objForm.save(commit=False)
            if request.user.is_authenticated:
                cd.analyst = request.user
            cd.save()
            cd.refresh_from_db()
            messages.success(request, 'Blog Video Detail Sent For Verification')
        else:
            messages.error(request, 'Please Check An Error occurred')
        return redirect(redirectTo)
    return HttpResponse('Invalid Entry')


#
def videosHeadingDMView(request):
    if request.method == 'POST':
        methodType = request.POST.get('submitType')
        redirectTo = request.POST.get('requestFrom')
        if methodType == 'new':
            objlnst = None
        else:
            pkID = request.POST.get('dataID')
            objlnst = get_object_or_404(videosHeadingDM, pk=pkID)

        objForm = videosHeadingDMForm(request.POST, request.FILES, instance=objlnst)

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
def videoBlogGenericDataView(request):
    if request.method == 'POST':
        methodType = request.POST.get('submitType')
        redirectTo = request.POST.get('requestFrom')
        if methodType == 'new':
            objlnst = None
        else:
            pkID = request.POST.get('dataID')
            objlnst = get_object_or_404(videoBlogGenericData, pk=pkID)

        objForm = videoBlogGenericDataForm(request.POST, request.FILES, instance=objlnst)

        if objForm.is_valid():
            cd = objForm.save(commit=False)
            if request.user.is_authenticated:
                cd.analyst = request.user
            cd.save()
            cd.refresh_from_db()
            messages.success(request, 'Blog Video Detail Sent For Verification')
        else:
            messages.error(request, 'Please Check An Error occurred')
        return redirect(redirectTo)
    return HttpResponse('Invalid Entry')


#
def tagList(request, tag_slug=None):
    object_list = blogVideos.published.all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        object_list = object_list.filter(tags__in=[tag])
    return render(request, 'videoBlog/UI/videoList.html', {'tag': tag, 'object_list': object_list})


#
@staff_member_required
def deleteObjectORM(request, slug=None, model=None):
    if slug and model:
        if model == 'categoryOptions':
            try:
                objInst = categoryOptions.objects.get(pk=slug)
                objInst.delete()
                messages.success(request, 'Category Deleted')
            except:
                messages.error(request, 'Please Try Again Later')
        elif model == 'subCategoryOptions':
            try:
                objInst = subCategoryOptions.objects.get(pk=slug)
                objInst.delete()
                messages.success(request, 'Sub Category Deleted')
            except:
                messages.error(request, 'Please Try Again Later')
        return redirect('videoBlogApp:videoListURL')
    else:
        messages.error(request, 'Invalid Attempt!')
        return redirect('videoBlogApp:videoListURL')


#
def deleteFKdataView(request):
    if request.method == 'POST':
        deletePK = request.POST.get('deleteDataID')
        deleteFrom = request.POST.get('deleteFlag')
        requestedPage = request.POST.get('redirectTo')
        if deleteFrom == 'blogVideos':
            try:
                objInst = blogVideos.objects.get(pk=deletePK)
                objInst.delete()
                messages.success(request, 'Data Deleted')
            except:
                messages.error(request, 'Please Try Again Later')
        elif deleteFrom == 'categoryOptions':
            try:
                objInst = categoryOptions.objects.get(pk=deletePK)
                objInst.delete()
                messages.success(request, 'Data Deleted')
            except:
                messages.error(request, 'Please Try Again Later')
        elif deleteFrom == 'videoBlogGenericData':
            try:
                objInst = videoBlogGenericData.objects.get(pk=deletePK)
                objInst.delete()
                messages.success(request, 'Data Deleted')
            except:
                messages.error(request, 'Please Try Again Later')
        return redirect(requestedPage)
    return HttpResponse('Invalid Entry Point')


def videoPageSectionVisiblityView(request):
    if request.method == 'POST':
        updateInst = get_object_or_404(blogPageSectionsOrdering, pk=1)
        cdForm = blogPageSectionsOrderingForm(request.POST, request.FILES, instance=updateInst)
        if cdForm.is_valid():
            cdForm.save()
            messages.success(request, 'Page Elements Updated Successfully')
        else:
            messages.error(request, 'Please Try Again Later')
        return redirect('videoBlogApp:videoListURL')
    return HttpResponse('Invalid Entry Point')


class VideoFiltersView(APIView):
    @method_decorator(cache_page(60 * 60 * 24))
    def get(self, request):
        filter_data = VideoService.get_video_filters()
        resp = {'status': True, "data": {'filters': filter_data}}
        return Response(resp)


#
@api_view(['GET'])
def getCategoryBasedVideosView(request, slug=None):
    response_dict = {}
    if request.user.is_staff:
        createCategoryOptions, createSubCategoryOptions, createBlogVideos, createGenericData = genericForms(
            'videoListPage')
    else:
        createCategoryOptions = createSubCategoryOptions = createBlogVideos = createGenericData = None
    tags = blogVideos.tags.most_common()[:5]
    tags_list = []
    try:
        if tags:
            for each in tags:
                tags_ser = blogVideosSerializer(each)
                tags_list.append(tags_ser.data)
    except:
        tags_list = []

    categoryOpt = categoryOptions.objects.all()
    categoryOpt_list = []
    try:
        if categoryOpt:
            for each in categoryOpt:
                categoryOpt_ser = categoryOptionsSerializer(each)
                categoryOpt_list.append(categoryOpt_ser.data)
    except:
        categoryOpt_list = []

    dataList = {}
    if slug:
        try:
            item = categoryOptions.objects.get(slug=slug)
            item_details = categoryOptionsSerializer(item)
            item_details = item_details.data
        except:
            item = None
            item_details = ""
        if item:
            blogVideo = blogVideos.objects.filter(category=item).order_by('-releasedDate')
            blogVideo_list = []
            try:
                if blogVideo:
                    for each in blogVideo:
                        blogVideo_ser = blogVideosSerializer(each)
                        blogVideo_list.append(blogVideo_ser.data)
            except:
                blogVideo_list = []

            latestVidBlog = blogVideo.first()
            try:
                if latestVidBlog:
                    latestVidBlog_details = blogVideosSerializer(latestVidBlog)
                    latestVidBlog_details = latestVidBlog_details.data
            except:
                latestVidBlog_details = ""
            dataList[item_details["name"]] = blogVideo_list
        else:
            messages.error(request, 'Bad Request!')
            return redirect('videoBlogApp:videoListURL')
    else:
        return redirect('videoBlogApp:videoListURL')
    response_dict.update({
        # 'createCategoryOptions': createCategoryOptions,
        # 'createSubCategoryOptions': createSubCategoryOptions,
        # 'createBlogVideos': createBlogVideos,
        # 'createGenericData': createGenericData,
        'tags': tags_list,
        'categoryOpt': categoryOpt_list,
        'dataList': dataList,
        'latestVidBlog': latestVidBlog_details,
    })
    return Response({'response': response_dict})
