from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from taggit_autosuggest.managers import TaggableManager
from django.urls import reverse
from django.shortcuts import redirect

from videoBlogApp.models import blogVideos
from videoShortsApp.models import blogVideosShorts
from stockApp.models import stockBasicDetail
from articleBlogApp.models import blogArticles
from newsBlogApp.models import blogNews
from mediaBlogApp.models import blogMedia
from staticPagesSlugApp.models import staticPagesSlugs

STATUS_CHOICES = (
	('Draft','Draft'),
	('Published','Published'),
	('Pending For Review','Pending For Review'),
	('Feedback Shared','Feedback Shared'),
	('Rejected','Rejected'),
)

research_report_pages_choices = (
	('snapshot', 'snapshot'),
	('key-ratio', 'key-ratio'),
	('peers', 'peers'),
	('financials', 'financials'),
	('ownership', 'ownership'),
	('news', 'news'),
	('events', 'events'),
)

Listing_Pages = (
	('homepage', 'homepage'),
	('loginPage', 'loginPage'),
	('homepageContact', 'homepageContact'),
	('aboutpage', 'aboutpage'),
	('contactpage', 'contactpage'),
	('careerpage', 'careerpage'),
	('teampage', 'teampage'),
	
	('seedFundingPage', 'seedFundingPage'),
	('earlyFundingPage', 'earlyFundingPage'),
	('growthFundingPage', 'growthFundingPage'),
	('sellYourStartupPage', 'sellYourStartupPage'),
	('sellESOPPage', 'sellESOPPage'),
	#
	('seedFundingSignupPage', 'seedFundingSignupPage'),
	('earlyFundingSignupPage', 'earlyFundingSignupPage'),
	('growthFundingSignupPage', 'growthFundingSignupPage'),
	('sellYourStartupSignupPage', 'sellYourStartupSignupPage'),
	('sellESOPSignupPage', 'sellESOPSignupPage'),
	('privateBoutiquePage', 'privateBoutiquePage'),
	('privateBoutiqueContactPage', 'privateBoutiqueContactPage'),
	#
	('preIPOPage', 'preIPOPage'),

	('blogHomePage', 'blogHomePage'),
	('videoBlogListPage', 'videoBlogListPage'),
	('newsBlogListPage', 'newsBlogListPage'),
	('stockListPage', 'stockListPage'),
	('mediaListPage', 'mediaListPage'),
	('videoShortsListPage', 'videoShortsListPage'),
	('newsFeedListPage', 'newsFeedListPage'),
	('articleListPage', 'articleListPage'),


	('buyPreIPOPage', 'buyPreIPOPage'),
	('startupAndMarketplacePage','startupAndMarketplacePage'),
	('channelPartnerPage', 'channelPartnerPage'),
	#
	('channelPartnerSignupPage', 'channelPartnerSignupPage'),
	('offersPage', 'offersPage'),
	('stockRecosPage', 'stockRecosPage'),
	#
	# for dynamic pages
	('videoBlog', 'videoBlog'),
	('shortsBlog', 'shortsBlog'),
	('articleBlog', 'articleBlog'),
	('newsBlog', 'newsBlog'),
	('researchReports', 'researchReports'),
)

class metaDetailForDM(models.Model):
	# Models Connection
	video_blog = models.OneToOneField(blogVideos, on_delete=models.SET_NULL, null=True, blank=True, related_name='video_blogBVDDM')
	video_shorts_blog = models.OneToOneField(blogVideosShorts, on_delete=models.SET_NULL, null=True, blank=True, related_name='video_shorts_blogBVDDM')
	articles_blog = models.OneToOneField(blogArticles, on_delete=models.SET_NULL, null=True, blank=True, related_name='articles_blog_blogBVDDM')
	news_blog = models.OneToOneField(blogNews, on_delete=models.SET_NULL, null=True, blank=True, related_name='news_blog_blogBVDDM')
	# media_blog = models.OneToOneField(blogMedia, on_delete=models.SET_NULL, null=True, blank=True, related_name='media_blog_blogBVDDM')
	research_report = models.ForeignKey(stockBasicDetail, on_delete=models.SET_NULL, null=True, blank=True, related_name='research_reportBVDDM')
	# Static Pages Connection
	static_page = models.CharField(max_length=256, null=True, blank=True, choices=Listing_Pages)
	research_report_pages = models.CharField(max_length=256, null=True, blank=True, choices=research_report_pages_choices)
	# meta data
	meta_title = models.CharField(max_length=1000,null=True, blank=True)
	meta_description = models.TextField(null=True, blank=True)
	meta_keywords = models.TextField(null=True, blank=True)
	meta_tags = TaggableManager(blank=True)
	featured_image = models.ImageField(upload_to='dm/featured-images', null=True, blank=True)
	end_point = models.TextField(null=True, blank=True)
	author = models.ForeignKey(User,on_delete=models.SET_NULL, related_name='authorBVDDM',null=True, blank=True)
	publish = models.DateTimeField(default=timezone.now)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	status = models.CharField(max_length=50,choices=STATUS_CHOICES, default='Draft')

	def __str__(self):		
		if self.video_blog:
			return f'Video Post with Title: {self.video_blog.title}'
		elif self.video_shorts_blog:
			return f'Video Short Post with Title: {self.video_shorts_blog.title}'
		elif self.research_report and self.research_report_pages:
			return f'Research Report Post Page: {self.research_report_pages} with Title: {self.research_report.stockName}'
		elif self.static_page:
			return f'Static Page for: {self.static_page}'

	def get_static_page_link(self):
		if self.static_page == 'homepage':
			try:
				redirectInst = staticPagesSlugs.objects.get(page='Home Page')
				return reverse('staticPagesSlugApp:staticSlugUrl', args=[redirectInst.slug])
			except:
				return reverse('websiteApp:homePageUrl')

		if self.static_page == 'homepageContact':
			try:
				redirectInst = staticPagesSlugs.objects.get(page='Home Page Contact Page')
				return reverse('staticPagesSlugApp:staticSlugUrl', args=[redirectInst.slug])
			except:
				return reverse('websiteApp:homePageContactUrl')

		elif self.static_page == 'aboutpage':
			try:
				redirectInst = staticPagesSlugs.objects.get(page='About Us')
				return reverse('staticPagesSlugApp:staticSlugUrl', args=[redirectInst.slug])
			except:
				return reverse('websiteApp:aboutUsUrl')

		elif self.static_page == 'teampage':
			try:
				redirectInst = staticPagesSlugs.objects.get(page='Team')
				return reverse('staticPagesSlugApp:staticSlugUrl', args=[redirectInst.slug])
			except:
				return reverse('websiteApp:teamsUrl')

		elif self.static_page == 'contactpage':
			try:
				redirectInst = staticPagesSlugs.objects.get(page='Contact Us')
				return reverse('staticPagesSlugApp:staticSlugUrl', args=[redirectInst.slug])
			except:
				return reverse('websiteApp:contactUsUrl')

		elif self.static_page == 'careerpage':
			try:
				redirectInst = staticPagesSlugs.objects.get(page='Careers')
				return reverse('staticPagesSlugApp:staticSlugUrl', args=[redirectInst.slug])
			except:
				return reverse('websiteApp:careerUrl')

		elif self.static_page == 'seedFundingPage':
			try:
				redirectInst = staticPagesSlugs.objects.get(page='Seed Funding')
				return reverse('staticPagesSlugApp:staticSlugUrl', args=[redirectInst.slug])
			except:
				return reverse('productPagesApp:seedFundingUrl')

		elif self.static_page == 'earlyFundingPage':
			try:
				redirectInst = staticPagesSlugs.objects.get(page='Early Funding')
				return reverse('staticPagesSlugApp:staticSlugUrl', args=[redirectInst.slug])
			except:
				return reverse('productPagesApp:earlyFundingUrl')

		elif self.static_page == 'growthFundingPage':
			try:
				redirectInst = staticPagesSlugs.objects.get(page='Growth Funding')
				return reverse('staticPagesSlugApp:staticSlugUrl', args=[redirectInst.slug])
			except:
				return reverse('productPagesApp:growthFundingUrl')


		elif self.static_page == 'sellYourStartupPage':
			try:
				redirectInst = staticPagesSlugs.objects.get(page='Sell Your Startup')
				return reverse('staticPagesSlugApp:staticSlugUrl', args=[redirectInst.slug])
			except:
				return reverse('productPagesApp:sellYourStartupUrl')

		elif self.static_page == 'preIPOPage':
			try:
				redirectInst = staticPagesSlugs.objects.get(page='Pre IPO')
				return reverse('staticPagesSlugApp:staticSlugUrl', args=[redirectInst.slug])
			except:
				return reverse('websiteApp:preIpoUrl')

		elif self.static_page == 'sellESOPPage':
			try:
				redirectInst = staticPagesSlugs.objects.get(page='Sell ESOP')
				return reverse('staticPagesSlugApp:staticSlugUrl', args=[redirectInst.slug])
			except:
				return reverse('productPagesApp:sellESOPUrl')
		elif self.static_page == 'seedFundingSignupPage':
			try:
				redirectInst = staticPagesSlugs.objects.get(page='seedFundingSignupPage')
				return reverse('staticPagesSlugApp:staticSlugUrl', args=[redirectInst.slug])
			except:
				return reverse('productPagesApp:seedFundingUrl')
		elif self.static_page == 'earlyFundingSignupPage':
			try:
				redirectInst = staticPagesSlugs.objects.get(page='earlyFundingSignupPage')
				return reverse('staticPagesSlugApp:staticSlugUrl', args=[redirectInst.slug])
			except:
				return reverse('productPagesApp:earlyFundingUrl')
		elif self.static_page == 'growthFundingSignupPage':
			try:
				redirectInst = staticPagesSlugs.objects.get(page='growthFundingSignupPage')
				return reverse('staticPagesSlugApp:staticSlugUrl', args=[redirectInst.slug])
			except:
				return reverse('productPagesApp:growthFundingUrl')
		elif self.static_page == 'sellYourStartupSignupPage':
			try:
				redirectInst = staticPagesSlugs.objects.get(page='sellYourStartupSignupPage')
				return reverse('staticPagesSlugApp:staticSlugUrl', args=[redirectInst.slug])
			except:
				return reverse('productPagesApp:sellYourStartupUrl')
		elif self.static_page == 'sellESOPSignupPage':
			try:
				redirectInst = staticPagesSlugs.objects.get(page='sellESOPSignupPage')
				return reverse('staticPagesSlugApp:staticSlugUrl', args=[redirectInst.slug])
			except:
				return reverse('productPagesApp:sellESOPUrl')
		elif self.static_page == 'channelPartnerSignupPage':
			try:
				redirectInst = staticPagesSlugs.objects.get(page='channelPartnerSignupPage')
				return reverse('staticPagesSlugApp:staticSlugUrl', args=[redirectInst.slug])
			except:
				return reverse('websiteApp:channelPartnerSignupPageUrl')
		elif self.static_page == 'blogHomePage':
			try:
				redirectInst = staticPagesSlugs.objects.get(page='Blog')
				return reverse('staticPagesSlugApp:staticSlugUrl', args=[redirectInst.slug])
			except:
		 		return reverse('blogHomeApp:blogHomeURL')
		elif self.static_page == 'videoShortsListPage':
			try:
				redirectInst = staticPagesSlugs.objects.get(page='Video Shorts')
				return reverse('staticPagesSlugApp:staticSlugUrl', args=[redirectInst.slug])
			except:
				return reverse('videoShortsApp:shortsListUrl')

		elif self.static_page == 'videoBlogListPage':
			try:
				redirectInst = staticPagesSlugs.objects.get(page='Videos')
				return reverse('staticPagesSlugApp:staticSlugUrl', args=[redirectInst.slug])
			except:
				return reverse('videoBlogApp:videoListURL')

		elif self.static_page == 'newsBlogListPage':
			try:
				redirectInst = staticPagesSlugs.objects.get(page='Planify News')
				return reverse('staticPagesSlugApp:staticSlugUrl', args=[redirectInst.slug])
			except:
				return reverse('newsBlogApp:crawledNewsUrl')

		elif self.static_page == 'newsFeedListPage':
			try:
				redirectInst = staticPagesSlugs.objects.get(page='Feed')
				return reverse('staticPagesSlugApp:staticSlugUrl', args=[redirectInst.slug])
			except:
				return reverse('newsBlogApp:newsListUrl')

		elif self.static_page == 'mediaListPage':
			try:
				redirectInst = staticPagesSlugs.objects.get(page='Media Coverage')
				return reverse('staticPagesSlugApp:staticSlugUrl', args=[redirectInst.slug])
			except:
				return reverse('mediaBlogApp:mediaListURL')


		elif self.static_page == 'stockListPage':
			try:
				redirectInst = staticPagesSlugs.objects.get(page='Research Reports')
				return reverse('staticPagesSlugApp:staticSlugUrl', args=[redirectInst.slug])
			except:
				return reverse('stockApp:stockListURL')
		
		elif self.static_page == 'articleListPage':
			try:
				redirectInst = staticPagesSlugs.objects.get(page='Articles')
				return reverse('staticPagesSlugApp:staticSlugUrl', args=[redirectInst.slug])
			except:
				return reverse('articleBlogApp:articlesListURL')

		elif self.static_page == 'buyPreIPOPage':
			try:
				redirectInst = staticPagesSlugs.objects.get(page='Buy pre IPO')
				return reverse('staticPagesSlugApp:staticSlugUrl', args=[redirectInst.slug])
			except:
				return reverse('websiteApp:buypreIPOUrl')
		
		elif self.static_page == 'startupAndMarketplacePage':
			try:
				redirectInst = staticPagesSlugs.objects.get(page='Startup Funding')
				return reverse('staticPagesSlugApp:staticSlugUrl', args=[redirectInst.slug])
			except:
				return reverse('websiteApp:startupPageUrl')

		elif self.static_page == 'loginPage':
			try:
				redirectInst = staticPagesSlugs.objects.get(page='Login Page')
				return reverse('staticPagesSlugApp:staticSlugUrl', args=[redirectInst.slug])
			except:
				return reverse('authApp:loginUsernameHandlerUrl')

		elif self.static_page == 'channelPartnerPage':
			try:
				redirectInst = staticPagesSlugs.objects.get(page='Channel Partner')
				return reverse('staticPagesSlugApp:staticSlugUrl', args=[redirectInst.slug])
			except:
				return reverse('websiteApp:channelPartnerUrl')
		elif self.static_page == 'privateBoutiquePage':
			try:
				redirectInst = staticPagesSlugs.objects.get(page='Private Boutique Page')
				return reverse('staticPagesSlugApp:staticSlugUrl', args=[redirectInst.slug])
			except:
				return reverse('productPagesApp:privateBoutiqueUrl')
		elif self.static_page == 'privateBoutiqueContactPage':
			try:
				redirectInst = staticPagesSlugs.objects.get(page='Private Boutique Contact Page')
				return reverse('staticPagesSlugApp:staticSlugUrl', args=[redirectInst.slug])
			except:
				return reverse('productPagesApp:privateBoutiqueContactUsSignupUrl')
		elif self.static_page == 'offersPage':
			try:
				redirectInst = staticPagesSlugs.objects.get(page='Offers Page')
				return reverse('staticPagesSlugApp:staticSlugUrl', args=[redirectInst.slug])
			except:
				return reverse('websiteApp:offerViews')

		elif self.static_page == 'stockRecosPage':
			try:
				redirectInst = staticPagesSlugs.objects.get(page='Stock Recommendations')
				return reverse('staticPagesSlugApp:staticSlugUrl', args=[redirectInst.slug])
			except:
				return reverse('websiteApp:search')
	def save(self):
		static_url = self.get_static_page_link()
		self.end_point = static_url
		super(metaDetailForDM, self).save()

	class Meta:
		verbose_name_plural = 'Meta Description For Whole Website'
