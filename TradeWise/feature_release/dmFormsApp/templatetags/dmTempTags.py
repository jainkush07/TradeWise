from django import template
from taggit.models import Tag
from videoBlogApp.models import blogVideos
from videoShortsApp.models import blogVideosShorts
from stockApp.models import stockBasicDetail
from articleBlogApp.models import blogArticles
from newsBlogApp.models import blogNews
from ..models import metaDetailForDM
from ..forms import metaDetailForDMForm

register = template.Library()

#
@register.inclusion_tag('templateTagsHTML/dmTemplateTags/dmForm.html')
def dmFormRenderTag(request, pageKey, dataID = None, subPageKey=None):
	dmInst = None
	if pageKey == 'videoBlog':
		try:
			fkInst = blogVideos.objects.get(pk=dataID)
			dmInst = metaDetailForDM.objects.get(video_blog=fkInst)
		except:
			pass
	elif pageKey == 'shortsBlog':
		try:
			fkInst = blogVideosShorts.objects.get(pk=dataID)
			dmInst = metaDetailForDM.objects.get(video_shorts_blog=fkInst)
		except:
			pass
	elif pageKey == 'articleBlog':
		try:
			fkInst = blogArticles.objects.get(pk=dataID)
			dmInst = metaDetailForDM.objects.get(articles_blog=fkInst)
		except:
			pass
	elif pageKey == 'newsBlog':
		try:
			fkInst = blogNews.objects.get(pk=dataID)
			dmInst = metaDetailForDM.objects.get(news_blog=fkInst)
		except:
			pass
	elif pageKey == 'researchReports':
		try:
			fkInst = stockBasicDetail.objects.get(pk=dataID)
			if subPageKey == 'snapshot':
				dmInst = metaDetailForDM.objects.get(research_report=fkInst, research_report_pages=subPageKey)
			elif subPageKey == 'key-ratio':
				dmInst = metaDetailForDM.objects.get(research_report=fkInst, research_report_pages=subPageKey)
			elif subPageKey == 'peers':
				dmInst = metaDetailForDM.objects.get(research_report=fkInst, research_report_pages=subPageKey)
			elif subPageKey == 'financials':
				dmInst = metaDetailForDM.objects.get(research_report=fkInst, research_report_pages=subPageKey)
			elif subPageKey == 'ownership':
				dmInst = metaDetailForDM.objects.get(research_report=fkInst, research_report_pages=subPageKey)
			elif subPageKey == 'news':
				dmInst = metaDetailForDM.objects.get(research_report=fkInst, research_report_pages=subPageKey)
			elif subPageKey == 'events':
				dmInst = metaDetailForDM.objects.get(research_report=fkInst, research_report_pages=subPageKey)
		except:
			pass
	else:
		try:
			dmInst = metaDetailForDM.objects.get(static_page=pageKey)
		except:
			pass
	submitForm = metaDetailForDMForm(instance=dmInst)
	context = {
		'dmInst': dmInst,
		'request': request,
		'pageKey': pageKey,
		'subPageKey': subPageKey,
		'dataID': dataID,
		'submitForm': submitForm,
	}
	return context

#
@register.inclusion_tag('templateTagsHTML/dmTemplateTags/metatags.html')
def tagsRenderTag(request, pageKey, dataID = None, subPageKey=None):
	dmInst = None
	if pageKey == 'videoBlog':
		try:
			fkInst = blogVideos.objects.get(pk=dataID)
			dmInst = metaDetailForDM.objects.get(video_blog=fkInst)
		except:
			pass
	elif pageKey == 'shortsBlog':
		try:
			fkInst = blogVideosShorts.objects.get(pk=dataID)
			dmInst = metaDetailForDM.objects.get(video_shorts_blog=fkInst)
		except:
			pass
	elif pageKey == 'articleBlog':
		try:
			fkInst = blogArticles.objects.get(pk=dataID)
			dmInst = metaDetailForDM.objects.get(articles_blog=fkInst)
		except:
			pass
	elif pageKey == 'newsBlog':
		try:
			fkInst = blogNews.objects.get(pk=dataID)
			dmInst = metaDetailForDM.objects.get(news_blog=fkInst)
		except:
			pass
	elif pageKey == 'researchReports':
		try:
			fkInst = stockBasicDetail.objects.get(pk=dataID)
			if subPageKey == 'snapshot':
				dmInst = metaDetailForDM.objects.get(research_report=fkInst, research_report_pages=subPageKey)
			elif subPageKey == 'key-ratio':
				dmInst = metaDetailForDM.objects.get(research_report=fkInst, research_report_pages=subPageKey)
			elif subPageKey == 'peers':
				dmInst = metaDetailForDM.objects.get(research_report=fkInst, research_report_pages=subPageKey)
			elif subPageKey == 'financials':
				dmInst = metaDetailForDM.objects.get(research_report=fkInst, research_report_pages=subPageKey)
			elif subPageKey == 'ownership':
				dmInst = metaDetailForDM.objects.get(research_report=fkInst, research_report_pages=subPageKey)
			elif subPageKey == 'news':
				dmInst = metaDetailForDM.objects.get(research_report=fkInst, research_report_pages=subPageKey)
			elif subPageKey == 'events':
				dmInst = metaDetailForDM.objects.get(research_report=fkInst, research_report_pages=subPageKey)
		except:
			pass
	else:
		try:
			dmInst = metaDetailForDM.objects.get(static_page=pageKey)
		except:
			pass
	context = {
		'request': request,
		'dmInst': dmInst,
	}
	return context

#
@register.inclusion_tag('templateTagsHTML/dmTemplateTags/tagsTag.html')
def listAllTagsView():
	tags = metaDetailForDM.meta_tags.most_common()[:13]
	tagsMobile = metaDetailForDM.meta_tags.most_common()[:6]
	context = {
		'tags': tags,
		'tagsMobile':tagsMobile,
	}
	return context