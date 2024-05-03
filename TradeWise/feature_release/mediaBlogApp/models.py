from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator

#
STATUS_CHOICES = (
	('Draft','Draft'),
	('Published','Published'),
	('Pending For Review','Pending For Review'),
	('Feedback Shared','Feedback Shared'),
	('Rejected','Rejected'),

)

#
class blogMedia(models.Model):
	ALLOWED_TYPES = ['mp4']
	author = models.ForeignKey(User,on_delete=models.CASCADE, related_name='authorBM')
	title = models.CharField(max_length=250)
	subTitle = models.CharField(max_length=250, null=True, blank=True)
	slug = models.SlugField(max_length=250, unique_for_date='publish')
	excerptContent = models.TextField(null=True, blank=True)
	mediaImage = models.ImageField(upload_to='media/images', null=True, blank=True)	
	publishMedia = models.CharField(max_length=250, null=True, blank=True) #for mention that article posted in which magazine etc.
	publishMediaWebsiteLink = models.URLField(null=True, blank=True) 
	dateForMediaPost = models.DateField(null=True, blank=True)
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
		verbose_name_plural = 'Blog Media Profile'


class mediaBlogDM(models.Model):
	metaTitleListing = models.CharField(max_length=1000,null=True, blank=True)
	metaDescriptionListing = models.TextField(null=True, blank=True)
	metaKeywordsListing = models.TextField(null=True, blank=True)
	tagsListing = models.CharField(max_length=1000, null=True, blank=True)
	metaFeaturedImage = models.ImageField(upload_to='media/images/featured', null=True, blank=True)
	publish = models.DateTimeField(default=timezone.now)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	status = models.CharField(max_length=50,choices=STATUS_CHOICES, default='draft')

	def __str__(self):
		return self.metaTitleListing or '--Name not provided--'

	class Meta:
		verbose_name_plural = 'Media Listing DM Information'