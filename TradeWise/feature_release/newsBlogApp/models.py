from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
from django.urls import reverse
from stockApp.models import stockBasicDetail


STATUS_CHOICES = (
	('Draft','Draft'),
	('Published','Published'),
	('Pending For Review','Pending For Review'),
	('Feedback Shared','Feedback Shared'),
	('Rejected','Rejected'),

)

STATUS_PROFILE = (
	('Investor','Investor'),
	('Partner','Partner'),
	('Shareholder','Shareholder'),
	('Institution','Institution'),
	('Employee','Employee'),
)

#
class blogNews(models.Model):
	ALLOWED_TYPES = ['mp4']
	author = models.ForeignKey(User,on_delete=models.CASCADE, related_name='authorBN')
	title = models.CharField(max_length=1000)
	subTitle = models.CharField(max_length=1000, null=True, blank=True)
	slug = models.SlugField(max_length=1000, unique=True)
	researchReportForLogo = models.ForeignKey(stockBasicDetail, on_delete=models.SET_NULL, null=True, blank=True, related_name='researchReportForLogoBN')
	dateOfNews = models.DateField(default=timezone.now, null=True, blank=True)
	timeOfNews = models.TimeField(null=True, blank=True)
	relatedResearchReports = models.ManyToManyField(stockBasicDetail,blank=True, related_name='relatedResearchReportsBN')
	pdfForNews = models.FileField(upload_to='blog/newsPDFS', null=True, blank=True)
	pptForNews = models.FileField(upload_to='blog/newsPPTS', null=True, blank=True)
	imageUpload = models.ImageField(upload_to='blog/images', null=True, blank=True)
	excerptContent = models.TextField(null=True, blank=True)
	content1 = models.TextField(null=True, blank=True)
	content2 = models.TextField(null=True, blank=True)
	content3 = models.TextField(null=True, blank=True)
	content4 = models.TextField(null=True, blank=True)
	content5 = models.TextField(null=True, blank=True)
	publish = models.DateTimeField(default=timezone.now)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	status = models.CharField(max_length=50,choices=STATUS_CHOICES, default='draft')

	def __str__(self):
		return self.title or '--Name not provided--'

	class Meta:
		verbose_name_plural = 'Blog News Profile'

	def get_absolute_url(self):
		return reverse('newsBlogApp:newsDetailURL', args=[self.slug])

	def releaseDate_self(self):
		if self.dateOfNews:
			return self.dateOfNews
		elif self.updated:
			return self.updated
		else:
			return 'No Date'

	def get_current_image(self):
		try:
			return self.researchReportForLogo.logo.url
		except:
			return 'javascript:void(0);'

	def source_self(self):
		return 'News Feed'

class blogNewsListingDM(models.Model):
	metaTitleNews = models.CharField(max_length=1000,null=True, blank=True)
	metaDescriptionNews = models.TextField(null=True, blank=True)
	metaKeywordsNews = models.TextField(null=True, blank=True)
	tagsNews = models.CharField(max_length=1000, null=True, blank=True)
	featuredImage = models.ImageField(upload_to='blog/images', null=True, blank=True)
	publish = models.DateTimeField(default=timezone.now)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	status = models.CharField(max_length=50,choices=STATUS_CHOICES, default='Draft')

	def __str__(self):
		return self.metaTitleNews or '--Name not provided--'

	class Meta:
		verbose_name_plural = 'Blog News Listing DM'

class blogNewsDetailedDM(models.Model):
	blogProfileName = models.OneToOneField(blogNews, on_delete=models.CASCADE, related_name='blogProfileNameBNDDM')
	metaTitleNews = models.CharField(max_length=1000,null=True, blank=True)
	metaDescriptionNews = models.TextField(null=True, blank=True)
	metaKeywordsNews = models.TextField(null=True, blank=True)
	tagsNews = models.CharField(max_length=1000, null=True, blank=True)
	featuredImage = models.ImageField(upload_to='blog/images', null=True, blank=True)
	publish = models.DateTimeField(default=timezone.now)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	status = models.CharField(max_length=50,choices=STATUS_CHOICES, default='Draft')

	def __str__(self):
		return self.metaTitleNews or '--Name not provided--'

	class Meta:
		verbose_name_plural = 'Blog News Detailed DM'

class blogWebNewsListingDM(models.Model):
	metaTitleNews = models.CharField(max_length=1000,null=True, blank=True)
	metaDescriptionNews = models.TextField(null=True, blank=True)
	metaKeywordsNews = models.TextField(null=True, blank=True)
	tagsNews = models.CharField(max_length=1000, null=True, blank=True)
	featuredImage = models.ImageField(upload_to='blog/images', null=True, blank=True)
	publish = models.DateTimeField(default=timezone.now)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	status = models.CharField(max_length=50,choices=STATUS_CHOICES, default='Draft')

	def __str__(self):
		return self.metaTitleNews or '--Name not provided--'

	class Meta:
		verbose_name_plural = 'Blog Web News Listing DM'



class newsHeadingDM(models.Model):
	newsBlog = models.ForeignKey(blogNews,on_delete=models.CASCADE, related_name='videoBlogNHDM', null=True, blank=True)
	name = models.CharField(max_length=1000, null=True, blank=True)
	description = models.TextField(null=True, blank=True)
	publish = models.DateTimeField(default=timezone.now)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	status = models.CharField(max_length=50,choices=STATUS_CHOICES, default='draft')

	def __str__(self):
		return self.name or '--Name not provided--'

class newsHeadingWebDM(models.Model):
	newsBlog = models.ForeignKey(blogNews,on_delete=models.CASCADE, related_name='videoBlogNHWebDM', null=True, blank=True)
	name = models.CharField(max_length=1000, null=True, blank=True)
	description = models.TextField(null=True, blank=True)
	publish = models.DateTimeField(default=timezone.now)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	status = models.CharField(max_length=50,choices=STATUS_CHOICES, default='draft')

	def __str__(self):
		return self.name or '--Name not provided--'


