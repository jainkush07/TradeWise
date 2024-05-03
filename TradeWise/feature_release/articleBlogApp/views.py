from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from django.contrib import messages
import datetime
from taggit.models import Tag
from .forms import *
from django.db.models import Count, Q
from .models import *
from rest_framework.views import APIView
from videoBlogApp.models import blogVideos
from planifyMain.paginators import StandardResultsSetPagination
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from articleBlogApp.serializers import BlogArticleListSerializer, BlogArticleSerializer, newBlogArticleSerializer
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from django.contrib.sites.shortcuts import get_current_site
from rest_framework.decorators import api_view


#
def searchView(request):
    query = request.GET.get('searchq')
    if query:
        articleList = blogArticles.objects.filter(
            Q(title__icontains=query) | Q(subTitle__icontains=query) | Q(excerptContent__icontains=query) | Q(
                content1__icontains=query) | Q(content2__icontains=query) | Q(content3__icontains=query) | Q(
                content4__icontains=query) | Q(content5__icontains=query)).distinct().order_by('-dateForListing')[:2]
    else:
        return redirect('articleBlogApp:articlesListURL')
    context = {
        'articleList': articleList,
        'query': query,
    }
    return render(request, 'articleBlog/UI/categoryList.html', context)


#
def articlesListView(request, slug=None):
    createCategoryOptions = categoryOptionsForm()
    createSubCategoryOptions = subCategoryOptionsForm()
    createBlogArticles = blogArticlesForm()
    createArticleTagsOptions = articleTagsOptionsForm()
    tagCount = Tag.objects.all().count()
    tagsArticles = blogArticles.tags.most_common()[:7]
    tagsVideo = blogVideos.tags.most_common()[:7]
    tags = tagsArticles.union(tagsVideo)
    categoryOpt = categoryOptions.objects.all()
    countDict = {}
    for item in categoryOpt:
        countDict[item] = blogArticles.objects.filter(category=item).count()
    sortedDictByPopular = sorted(countDict.items(), key=lambda x: x[1], reverse=True)
    sortedDictByPopular = sortedDictByPopular[:15]
    if slug:
        articleList = blogArticles.objects.all().order_by('-dateForListing')
        author = slug
    else:
        articleList = blogArticles.objects.all().order_by('-dateForListing')
        author = None

    context = {
        'createCategoryOptions': createCategoryOptions,
        'createSubCategoryOptions': createSubCategoryOptions,
        'createBlogArticles': createBlogArticles,
        'createArticleTagsOptions': createArticleTagsOptions,
        'tagCount': tagCount,
        'tags': tags,
        'articleList': articleList,
        'categoryOpt': categoryOpt,
        'sortedDictByPopular': sortedDictByPopular,
        'author': author,
    }
    return render(request, 'articleBlog/UI/categoryList.html', context)


#
def articleDetailView(request, slug):
    createBlogArticlesDetailed = blogArticlesDetailedForm()
    obj = get_object_or_404(blogArticles, slug=slug)
    obj.article_views = obj.article_views + 1
    obj.save()
    similarArticle = None
    requestFrom = request.GET.get('category')
    try:
        articleDMInst = articleDM.objects.latest('id')
    except:
        articleDMInst = None
    if requestFrom:
        similarArticle = blogArticles.objects.filter(category=requestFrom).order_by('-dateForListing')[0:3]
    context = {
        'obj': obj,
        'createBlogArticlesDetailed': createBlogArticlesDetailed,
        'similarArticle': similarArticle,
        'articleDMInst': articleDMInst,
    }
    return render(request, 'articleBlog/UI/categoryDetail.html', context)


#
def articleTagsOptionsView(request):
    if request.method == 'POST':
        methodType = request.POST.get('submitType')
        redirectTo = request.POST.get('requestFrom')
        if methodType == 'new':
            objlnst = None
        else:
            pkID = request.POST.get('dataID')
            objlnst = get_object_or_404(articleTagsOptions, pk=pkID)
        objForm = categoryOptionsForm(request.POST, instance=objlnst)
        if objForm.is_valid():
            cd = objForm.save(commit=False)
            if request.user.is_authenticated:
                cd.author = request.user
            cd.save()
            cd.refresh_from_db()
            messages.success(request, 'Blog Article Sent For Verification')
        else:
            messages.error(request, 'Please Check An Error occurred')
        return redirect(redirectTo)
    return HttpResponse('Invalid Entry')


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
                cd.author = request.user
            cd.save()
            cd.refresh_from_db()
            messages.success(request, 'Blog Article Sent For Verification')
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
                cd.author = request.user
            cd.save()
            cd.refresh_from_db()
            messages.success(request, 'Blog Video Sent For Verification')
        else:
            messages.error(request, 'Please Check An Error occurred')
        return redirect(redirectTo)
    return HttpResponse('Invalid Entry')


#
def blogArticlesView(request):
    if request.method == 'POST':
        methodType = request.POST.get('submitType')
        redirectTo = request.POST.get('requestFrom')
        if methodType == 'new':
            objlnst = None
        else:
            pkID = request.POST.get('dataID')
            objlnst = get_object_or_404(blogArticles, pk=pkID)
        objForm = blogArticlesForm(request.POST, request.FILES, instance=objlnst)
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
def blogArticlesDetailedView(request):
    if request.method == 'POST':
        methodType = request.POST.get('submitType')
        redirectTo = request.POST.get('requestFrom')
        if methodType == 'new':
            objlnst = None
        else:
            pkID = request.POST.get('dataID')
            objlnst = get_object_or_404(blogArticles, pk=pkID)
        objForm = blogArticlesDetailedForm(request.POST, request.FILES, instance=objlnst)
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
        if deleteFrom == 'blogArticlesDetailed':
            try:
                objInst = blogArticles.objects.get(pk=deletePK)
                objInst.delete()
                messages.success(request, 'Data Deleted')
                return redirect('articleBlogApp:articlesListURL')
            except:
                messages.error(request, 'Please Try Again Later')
        elif deleteFrom == 'blogArticles':
            try:
                objInst = blogArticles.objects.get(pk=deletePK)
                objInst.delete()
                messages.success(request, 'Data Deleted')
            except:
                messages.error(request, 'Please Try Again Later')
        return redirect(requestedPage)
    return HttpResponse('Invalid Entry Point')


#
def articleDMView(request):
    if request.method == 'POST':
        redirectTo = request.POST.get('requestFrom')
        try:
            obj = articleDM.objects.latest('id')
        except:
            obj = None
        objForm = articleDMForm(request.POST, request.FILES, instance=obj)
        if objForm.is_valid():
            var = objForm.save()
            var.save()
            var.refresh_from_db()
            messages.success(request, 'Data sent for verification')
        else:
            messages.error(request, 'Please check An Error occurred')
        return redirect(redirectTo)
    return HttpResponse('Invalid Entry')


class ArticleListView(APIView):
    paginator = StandardResultsSetPagination()

    @method_decorator(cache_page(60 * 60))
    def get(self, request):
        query = request.GET.get('search')
        if query:
            articleList = blogArticles.objects.filter(
                Q(title__icontains=query) | Q(subTitle__icontains=query) | Q(excerptContent__icontains=query) | Q(
                    content1__icontains=query) | Q(content2__icontains=query) | Q(content3__icontains=query) | Q(
                    content4__icontains=query) | Q(content5__icontains=query)).distinct().order_by('-dateForListing')[
                          :2]
        else:
            articleList = blogArticles.objects.all().order_by('-dateForListing')

        context = self.paginator.paginate_queryset(articleList, request)
        serializer = BlogArticleListSerializer(context, many=True)
        return self.paginator.get_paginated_response(serializer.data)


class ArticleListView(APIView):
    paginator = StandardResultsSetPagination()

    @method_decorator(cache_page(60 * 60))
    def get(self, request):
        query = request.GET.get('search')
        if query:
            articleList = blogArticles.objects.filter(
                Q(title__icontains=query) | Q(subTitle__icontains=query) | Q(excerptContent__icontains=query) | Q(
                    content1__icontains=query) | Q(content2__icontains=query) | Q(content3__icontains=query) | Q(
                    content4__icontains=query) | Q(content5__icontains=query)).distinct().order_by('-dateForListing')[
                          :2]
        else:
            articleList = blogArticles.objects.all().order_by('-dateForListing')

        context = self.paginator.paginate_queryset(articleList, request)
        serializer = BlogArticleListSerializer(context, many=True)
        return self.paginator.get_paginated_response(serializer.data)


class ArticleDataView(APIView):

    @method_decorator(cache_page(60 * 60))
    def get(self, request, pk):
        article = blogArticles.objects.filter(pk=pk).last()
        if article:
            serializer = newBlogArticleSerializer(article)
            articleurl = serializer.data['weburl'].split('/')
            articleurl = '/'.join(articleurl[3:])
            host_url = str(request.build_absolute_uri()).split('/')
            host_url = '/'.join(host_url[:3])
            articleurl = host_url + '/' + articleurl
            return Response({'status': True, "data": serializer.data, 'url': articleurl})
        else:
            return Response({'status': False, 'msg': "invalid request"})

class newArticleListApiView(generics.ListAPIView):
    queryset = blogArticles.objects.all().order_by('-dateForListing', '-created')
    serializer_class = newBlogArticleSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['title', 'subTitle', 'excerptContent', 'content1', 'content2', 'content3', 'content4', 'content5']

# class newArticleListApiView(APIView):
#     paginator = StandardResultsSetPagination()

#     @method_decorator(cache_page(60 * 60))
#     def get(self, request):
#         current = str(get_current_site(request))
#         global x_current_site_domain
#         x_current_site_domain = current
#         query = request.GET.get('search')
#         if query:
#             articleList = blogArticles.objects.filter(
#                 Q(title__icontains=query) | Q(subTitle__icontains=query) | Q(excerptContent__icontains=query) | Q(
#                     content1__icontains=query) | Q(content2__icontains=query) | Q(content3__icontains=query) | Q(
#                     content4__icontains=query) | Q(content5__icontains=query)).distinct().order_by('-dateForListing', '-created')[
#                           :2]
#         else:
#             articleList = blogArticles.objects.all().order_by('-dateForListing', '-created')
#         # print(request.build_absolute_uri())
#         # print("{0}://{1}/".format(request.scheme, request.get_host()))
#         context = self.paginator.paginate_queryset(articleList, request)
#         serializer = newBlogArticleSerializer(context, many=True)
#         return self.paginator.get_paginated_response(serializer.data)


@api_view(["POST"])
def articleDetailViewsCount(request):
    if request.method == 'POST':
        try:
            item_id = request.data.get("itemID")
            request_flag = request.data.get("countMe")
            if request_flag == "countMeFirst":
                objInst = blogArticles.objects.get(id = item_id)
                objInst.article_views = objInst.article_views + 1
                objInst.save()
                return Response({"msg": "Count is been increased for the article !", "status": True})
            else:
                return Response({"msg": "Please pass the correct flag !", "status": False})
        except:
            pass
    return Response({"msg": "Please send the correct request type !", "status": False})