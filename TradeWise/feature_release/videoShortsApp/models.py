from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
from taggit.managers import TaggableManager
from django.urls import reverse
from stockApp.models import stockBasicDetail


STATUS_CHOICES = (
	('Draft','Draft'),
	('Published','Published'),
	('Pending For Review','Pending For Review'),
	('Feedback Shared','Feedback Shared'),
	('Rejected','Rejected'),

)

class videoShortsCategoryOptions(models.Model):
	author = models.ForeignKey(User,on_delete=models.CASCADE, related_name='authorVSCO',null=True, blank=True)
	name = models.CharField(max_length=250)
	slug = models.SlugField(max_length=250, unique=True)
	description = models.TextField(null=True, blank=True)
	publish = models.DateTimeField(default=timezone.now)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	status = models.CharField(max_length=50,choices=STATUS_CHOICES, default='Draft')

	def __str__(self):
		return self.name or '--Name not provided--'

	class Meta:
		verbose_name_plural = 'Videos Shorts Category Details'

class videoShortsSubCategoryOptions(models.Model):
	author = models.ForeignKey(User,on_delete=models.CASCADE, related_name='authorVideoShortsSCO',null=True, blank=True)
	name = models.CharField(max_length=250)
	slug = models.SlugField(max_length=250, unique=True)
	category = models.ForeignKey(videoShortsCategoryOptions, on_delete=models.SET_NULL, null=True, blank=True)
	description = models.TextField(null=True, blank=True)
	publish = models.DateTimeField(default=timezone.now)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	status = models.CharField(max_length=50,choices=STATUS_CHOICES, default='Draft')

	def __str__(self):
		return self.name or '--Name not provided--'

	class Meta:
		verbose_name_plural = 'Videos Shorts Sub Category Details'


class blogVideosShorts(models.Model):
	FEATURED_CHOICES = (
		('Yes','Yes'),
		('No','No'),
	)
	ALLOWED_TYPES = ['mp4']
	author = models.ForeignKey(User,on_delete=models.CASCADE, related_name='authorBVShorts', null=True, blank=True)
	title = models.CharField(max_length=250)
	slug = models.SlugField(max_length=250, unique=True)
	tags = TaggableManager(blank=True)
	category = models.ManyToManyField(videoShortsCategoryOptions,blank=True, related_name='categoryBVS')
	subCategory = models.ManyToManyField(videoShortsSubCategoryOptions,blank=True, related_name='subCategoryBVS')
	relatedResearchReports = models.ManyToManyField(stockBasicDetail,blank=True, related_name='relatedResearchReportsBVS')
	featuredShots = models.CharField(max_length=50,choices=FEATURED_CHOICES, default='No')
	blogImage = models.ImageField(upload_to='blog/images', null=True, blank=True)
	blogVideo = models.FileField(upload_to ='blog/videos/', null=True, blank=True, validators=[FileExtensionValidator(ALLOWED_TYPES)])
	videoLink = models.CharField(max_length=250, null=True, blank=True)
	releaseDate = models.DateTimeField(null=True, blank=True)
	subTitle = models.CharField(max_length=250,null=True, blank=True)
	excerptContent = models.TextField(null=True, blank=True)
	content1 = models.TextField(null=True, blank=True)
	content2 = models.TextField(null=True, blank=True)
	content3 = models.TextField(null=True, blank=True)
	content4 = models.TextField(null=True, blank=True)
	content5 =  models.TextField(null=True, blank=True)
	publish = models.DateTimeField(default=timezone.now)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	status = models.CharField(max_length=50,choices=STATUS_CHOICES, default='Draft')

	def __str__(self):
		return self.title or '--Name not provided--'

	class Meta:
		verbose_name_plural = 'Video Shorts Profile'

	def get_absolute_url(self):
		return reverse('videoShortsApp:shortsDetailUrl', args=[self.slug])

	def get_current_image(self):
		if self.blogImage:
			return self.blogImage.url
		else:
			return 'javascript:void(0);'

	def releaseDate_self(self):
		if self.releaseDate:
			return self.releaseDate
		elif self.updated:
			return self.updated
		else:
			return 'No Date'
	
	def get_current_image(self):
		if self.blogImage:
			return self.blogImage.url
		else:
			return 'javascript:void(0);'

	def source_self(self):
		return 'Video Shorts'

class blogShortsListingDM(models.Model):
	metaTitleShorts = models.CharField(max_length=1000,null=True, blank=True)
	metaDescriptionShorts = models.TextField(null=True, blank=True)
	metaKeywordsShorts = models.TextField(null=True, blank=True)
	tagsShorts = models.CharField(max_length=1000, null=True, blank=True)
	featuredImage = models.ImageField(upload_to='blog/images', null=True, blank=True)
	publish = models.DateTimeField(default=timezone.now)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	status = models.CharField(max_length=50,choices=STATUS_CHOICES, default='Draft')

	def __str__(self):
		return self.metaTitleShorts or '--Name not provided--'

	class Meta:
		verbose_name_plural = 'Blog Shorts Listing DM'

class blogShortsDetailedDM(models.Model):
	blogProfileName = models.OneToOneField(blogVideosShorts, on_delete=models.CASCADE, related_name='blogProfileNameBNDDM')
	metaTitleShorts = models.CharField(max_length=1000,null=True, blank=True)
	metaDescriptionShorts = models.TextField(null=True, blank=True)
	metaKeywordsShorts = models.TextField(null=True, blank=True)
	tagsShorts = models.CharField(max_length=1000, null=True, blank=True)
	featuredImage = models.ImageField(upload_to='blog/images', null=True, blank=True)
	publish = models.DateTimeField(default=timezone.now)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	status = models.CharField(max_length=50,choices=STATUS_CHOICES, default='Draft')

	def __str__(self):
		return self.metaTitleShorts or '--Name not provided--'

	class Meta:
		verbose_name_plural = 'Blog Shorts Detailed DM'

class shortsHeadingDM(models.Model):
	videoShorts = models.ForeignKey(blogVideosShorts,on_delete=models.CASCADE, related_name='videoBlogSHDM', null=True, blank=True)
	name = models.CharField(max_length=1000, null=True, blank=True)
	description = models.TextField(null=True, blank=True)
	publish = models.DateTimeField(default=timezone.now)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	status = models.CharField(max_length=50,choices=STATUS_CHOICES, default='draft')

	def __str__(self):
		return self.name or '--Name not provided--'



