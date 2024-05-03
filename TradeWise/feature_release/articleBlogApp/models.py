from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
from taggit.managers import TaggableManager
from django.urls import reverse
from stockApp.models import stockBasicDetail
# from planifyMain.settings.base import BASE_URL
from django.conf import settings


STATUS_CHOICES = (
	('Draft','Draft'),
	('Published','Published'),
	('Pending For Review','Pending For Review'),
	('Feedback Shared','Feedback Shared'),
	('Rejected','Rejected'),

)

class articleTagsOptions(models.Model):
	author = models.ForeignKey(User,on_delete=models.CASCADE, related_name='authorATO')
	name = models.CharField(max_length=250)
	slug = models.SlugField(max_length=250, unique=True)
	description = models.TextField(null=True, blank=True)
	publish = models.DateTimeField(default=timezone.now)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	status = models.CharField(max_length=50,choices=STATUS_CHOICES, default='draft')

	def __str__(self):
		return self.name or '--Name not provided--'

	class Meta:
		verbose_name_plural = 'Article Tags Details'


class categoryOptions(models.Model):
	author = models.ForeignKey(User,on_delete=models.CASCADE, related_name='authorArticleCO')
	name = models.CharField(max_length=250)
	slug = models.SlugField(max_length=250, unique=True)
	description = models.TextField(null=True, blank=True)
	publish = models.DateTimeField(default=timezone.now)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	status = models.CharField(max_length=50,choices=STATUS_CHOICES, default='draft')

	def __str__(self):
		return self.name or '--Name not provided--'

	class Meta:
		verbose_name_plural = 'Article Category Details'


class subCategoryOptions(models.Model):
	author = models.ForeignKey(User,on_delete=models.CASCADE, related_name='authorArticleSCO')
	name = models.CharField(max_length=250)
	slug = models.SlugField(max_length=250, unique=True)
	category = models.ForeignKey(categoryOptions, on_delete=models.SET_NULL, null=True, blank=True)
	description = models.TextField(null=True, blank=True)
	publish = models.DateTimeField(default=timezone.now)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	status = models.CharField(max_length=50,choices=STATUS_CHOICES, default='draft')

	def __str__(self):
		return self.name or '--Name not provided--'

	class Meta:
		verbose_name_plural = 'Article Sub Category Details'


class blogArticles(models.Model):
	ALLOWED_TYPES = ['mp4']
	author = models.ForeignKey(User,on_delete=models.CASCADE, related_name='authorBA')
	title = models.CharField(max_length=250)
	slug = models.SlugField(max_length=250, unique_for_date='publish')
	articleImage = models.ImageField(upload_to='blog/images', null=True, blank=True)
	dateForListing = models.DateField(null=True, blank=True)
	subTitle = models.CharField(max_length=250,null=True, blank=True)
	excerptContent = models.TextField(null=True, blank=True)
	content1 = models.TextField(null=True, blank=True)
	content2 = models.TextField(null=True, blank=True)
	content3 = models.TextField(null=True, blank=True)
	content4 = models.TextField(null=True, blank=True)
	content5 = models.TextField(null=True, blank=True)
	article_views = models.IntegerField(default=0)
	articleVideo = models.FileField(upload_to ='blog/videos/', null=True, blank=True, validators=[FileExtensionValidator(ALLOWED_TYPES)])
	tags = TaggableManager(blank=True)
	category = models.ManyToManyField(categoryOptions,blank=True, related_name='categoryBA')
	subCategory = models.ManyToManyField(subCategoryOptions,blank=True, related_name='subCategoryBA')
	relatedResearchReports = models.ManyToManyField(stockBasicDetail,blank=True, related_name='relatedResearchReportsBA')
	publish = models.DateTimeField(default=timezone.now)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	status = models.CharField(max_length=50,choices=STATUS_CHOICES, default='draft')

	def __str__(self):
		return self.title or '--Name not provided--'

	class Meta:
		verbose_name_plural = 'Blog Article Profile'

	def get_absolute_url(self):
		return reverse('articleBlogApp:articleDetailURL', args=[self.slug])

	def get_absolute_url_newForAPI(self):
		return settings.BASE_URL +reverse('articleBlogApp:articleDetailURL', args=[self.slug])

	def get_current_image(self):
		if self.articleImage:
			return self.articleImage.url
		else:
			return 'https://planify-reports.s3.amazonaws.com/static/stocks/imgs/planify-logo.png'

	def source_self(self):
		return 'News Articles'

class Comment(models.Model):
	articlePost = models.ForeignKey(blogArticles,blank=True, on_delete=models.SET_NULL,null=True, related_name='articlePostC')
	name = models.CharField(max_length=250)
	email = models.EmailField(max_length=200, null=True, blank=True)
	website =  models.URLField(max_length=1000,null=True,blank=True)
	body = models.TextField(null=True, blank=True)
	publish = models.DateTimeField(default=timezone.now)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	status = models.CharField(max_length=50,choices=STATUS_CHOICES, default='draft')

	def __str__(self):
		return 'Comment by {} on {}'.format(self.name, self.articlePost)

	class Meta:
		verbose_name_plural = 'Article Comment Details'


#dm
class articleDM(models.Model):
	metaTitle = models.CharField(max_length=1000, null=True, blank=True)
	metaDescription = models.CharField(max_length=1000, null=True, blank=True)
	tags = models.CharField(max_length=1000, null=True, blank=True)
	metaFeaturedImage = models.ImageField(upload_to='images/documents', null=True, blank=True, validators=[FileExtensionValidator(['jpg','png','jpeg'])])
	metaKeywords = models.CharField(max_length=1000, null=True, blank=True)
	author = models.CharField(max_length=100, null=True, blank=True)
	publish = models.DateTimeField(default=timezone.now)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now_add=True)
	status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='draft')

	def __str__(self):
		return self.metaTitle or '--Name not provided' 

		class Meta:
			verbose_name_plural = 'Article DM Form'






