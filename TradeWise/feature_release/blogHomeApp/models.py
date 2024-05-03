from django.db import models
from django.utils import timezone

#
class tagModel(models.Model):
	image = models.ImageField(upload_to='blog/tag-featured/images', null=True, blank=True)
	publish = models.DateTimeField(default=timezone.now)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)

	def __str__(self):
		return '--Name not provided--'

#
class categoryImageModel(models.Model):
	image = models.ImageField(upload_to='blog/category-featured/images', null=True, blank=True)
	publish = models.DateTimeField(default=timezone.now)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)

	def __str__(self):
		return '--Name not provided--'

#
class newsCommonImageHomeModel(models.Model):
	image = models.ImageField(upload_to='blog/home/images', null=True, blank=True)
	publish = models.DateTimeField(default=timezone.now)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)

	def __str__(self):
		return '--Name not provided--'

class homeBlogDM(models.Model):
	metaTitleListing = models.CharField(max_length=1000,null=True, blank=True)
	metaDescriptionListing = models.TextField(null=True, blank=True)
	metaKeywordsListing = models.TextField(null=True, blank=True)
	tagsListing = models.CharField(max_length=1000, null=True, blank=True)
	metaFeaturedImage = models.ImageField(upload_to='media/images/featured', null=True, blank=True)
	publish = models.DateTimeField(default=timezone.now)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.metaTitleListing or '--Name not provided--'

	class Meta:
		verbose_name_plural = 'Blog Home DM Information'