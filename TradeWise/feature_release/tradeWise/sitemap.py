from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from stockApp import models as stockModels
from videoBlogApp.models import blogVideos
from videoShortsApp.models import blogVideosShorts
from articleBlogApp.models import blogArticles
from newsBlogApp.models import blogNews




class researchReportMap(Sitemap):
	name = 'research-report'
	changefreq = 'hourly'
	limit = 50000
	priority = 0.9
	protocol = 'https'

	def items(self):
		querySet = []
		querySetSnapshot = stockModels.stockBasicDetail.objects.filter(status='published').order_by('id')
		querySetKeyRatio = stockModels.keyratioUrlsForSitemap.objects.filter(status='published').order_by('id')
		querySetPeers = stockModels.peersUrlsForSitemap.objects.filter(status='published').order_by('id')
		querySetFinancials = stockModels.financialUrlsForSitemap.objects.filter(status='published').order_by('id')
		querySetOwnership = stockModels.ownershipUrlsForSitemap.objects.filter(status='published').order_by('id')
		querySetNews = stockModels.newsUrlsForSitemap.objects.filter(status='published').order_by('id')
		querySetEvents = stockModels.eventsUrlsForSitemap.objects.filter(status='published').order_by('id')
		for item in querySetSnapshot:
			querySet.append(item)
		for item in querySetKeyRatio:
			querySet.append(item)
		for item in querySetPeers:
			querySet.append(item)
		for item in querySetFinancials:
			querySet.append(item)
		for item in querySetOwnership:
			querySet.append(item)
		for item in querySetNews:
			querySet.append(item)
		for item in querySetEvents:
			querySet.append(item)
		return querySet


class stockListStatic(Sitemap):
	name = 'stocks-list'
	changefreq = 'hourly'
	priority = 0.8
	protocol = 'https'

	def items(self):
		return ['stockApp:stockListURL',]

	def location(self, item):
		return reverse(item)

class videoBlogMap(Sitemap):
	name = 'video-blog'
	changefreq = 'hourly'
	limit = 50000
	priority = 0.9
	protocol = 'https'

	def items(self):
		querySet = blogVideos.objects.all().order_by('id')
		return querySet


class videoShortsBlogMap(Sitemap):
	name = 'video-shorts-blog'
	changefreq = 'hourly'
	limit = 50000
	priority = 0.9
	protocol = 'https'

	def items(self):
		querySet = blogVideosShorts.objects.all().order_by('id')
		return querySet


class articleBlogMap(Sitemap):
	name = 'articles-blog'
	changefreq = 'hourly'
	limit = 50000
	priority = 0.8
	protocol = 'https'

	def items(self):
		querySet = blogArticles.objects.all().order_by('id')
		return querySet


class newsBlogMap(Sitemap):
	name = 'feed'
	changefreq = 'hourly'
	limit = 50000
	priority = 0.9
	protocol = 'https'

	def items(self):
		querySet = blogNews.objects.all().order_by('id')
		return querySet

class newsWebBlogMap(Sitemap):
	name = 'news'
	changefreq = 'hourly'
	limit = 50000
	priority = 0.9
	protocol = 'https'

	def items(self):
		querySet = blogNews.objects.all().order_by('id')
		return querySet


class websiteStaticSiteMap(Sitemap):
	name = 'website-site-map'
	changefreq = 'hourly'
	protocol = 'https'

	def items(self):
		return [
			'websiteApp:buypreIPOUrl',
			'websiteApp:preIpoUrl', 
			'websiteApp:homePageUrl',
			'websiteApp:careerUrl',
			'websiteApp:contactUsUrl',
			'websiteApp:aboutUsUrl',
			'websiteApp:teamsUrl',
			'websiteApp:channelPartnerUrl',
			'productPagesApp:seedFundingUrl',
			'productPagesApp:earlyFundingUrl',
			'productPagesApp:growthFundingUrl',
			'productPagesApp:sellESOPUrl',
			'productPagesApp:sellYourStartupUrl'
		]

	def location(self, item):
		return reverse(item)

	def priority(self, item):
		return {
			'websiteApp:buypreIPOUrl':0.9, 
			'websiteApp:preIpoUrl': 0.8, 
			'websiteApp:homePageUrl': 1.0, 
			'websiteApp:careerUrl':0.8,
			'websiteApp:contactUsUrl':0.9,
			'websiteApp:aboutUsUrl':0.8,
			'websiteApp:teamsUrl':0.8,
			'websiteApp:channelPartnerUrl':0.8,
			'productPagesApp:seedFundingUrl':0.8,
			'productPagesApp:earlyFundingUrl':0.8,
			'productPagesApp:growthFundingUrl':0.8,
			'productPagesApp:sellESOPUrl':0.8,
			'productPagesApp:sellYourStartupUrl':0.8
		}[item]















