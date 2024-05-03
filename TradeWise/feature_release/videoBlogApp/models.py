from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
from taggit.managers import TaggableManager
from mptt.models import MPTTModel, TreeForeignKey
from django.urls import reverse
from stockApp.models import stockBasicDetail


STATUS_CHOICES = (
	('Draft','Draft'),
	('Published','Published'),
	('Pending For Review','Pending For Review'),
	('Feedback Shared','Feedback Shared'),
	('Rejected','Rejected'),

)

class videoBlogGenericData(models.Model):
	author = models.ForeignKey(User,on_delete=models.CASCADE, related_name='authorBBGD',null=True, blank=True)
	blogMainImage = models.ImageField(upload_to='blog/images', null=True, blank=True)
	publish = models.DateTimeField(default=timezone.now)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	status = models.CharField(max_length=50,choices=STATUS_CHOICES, default='Draft')

	class Meta:
		verbose_name_plural = 'Blog Videos Main Image'


class categoryOptions(models.Model):
	author = models.ForeignKey(User,on_delete=models.CASCADE, related_name='authorVideoCO',null=True, blank=True)
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
		verbose_name_plural = 'Blog Videos Category Details'

	def get_absolute_url(self):
		return reverse('videoBlogApp:categoryBasedVideosUrl', args=[self.slug])

	def model_name(self):
		return 'categoryOptions'

	def delete_this_object(self):
		return reverse('videoBlogApp:deleteUsingORMUrl', kwargs={'slug': self.id,'model': 'categoryOptions'})


class subCategoryOptions(models.Model):
	author = models.ForeignKey(User,on_delete=models.CASCADE, related_name='authorVideoSCO',null=True, blank=True)
	name = models.CharField(max_length=250)
	slug = models.SlugField(max_length=250, unique=True)
	category = models.ForeignKey(categoryOptions, on_delete=models.SET_NULL, null=True, blank=True)
	description = models.TextField(null=True, blank=True)
	publish = models.DateTimeField(default=timezone.now)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	status = models.CharField(max_length=50,choices=STATUS_CHOICES, default='Draft')

	def __str__(self):
		return self.name or '--Name not provided--'

	class Meta:
		verbose_name_plural = 'Blog Videos Sub Category Details'

	def model_name(self):
		return 'subCategoryOptions'
	
	def get_absolute_url(self):
		return reverse('videoBlogApp:subCategoryBasedVideosUrl', args=[self.slug])

	def delete_this_object(self):
		return reverse('videoBlogApp:deleteUsingORMUrl', kwargs={'slug': self.id, 'model': 'subCategoryOptions'})


class marketingData(models.Model):
	daysForTrending = models.PositiveIntegerField()
	latestByDate = models.PositiveIntegerField()
	hitCountPopular = models.PositiveIntegerField()
	maxLimitForExplore = models.PositiveIntegerField()
	lastUpdateBy = models.ForeignKey(User,on_delete=models.CASCADE, related_name='lastUpdateByMD', null=True, blank=True)

	def __str__(self):
		return str(self.daysForTrending) or '--Name not provided--'

	class Meta:
		verbose_name_plural = 'Marketing Data For X Days'	


class blogVideos(models.Model):	
	EXPLORE_CHOICES = (
		('Yes','Yes'),
		('No','No'),
	)
	ALLOWED_TYPES = ['mp4']
	author = models.ForeignKey(User,on_delete=models.CASCADE, related_name='authorBV', null=True, blank=True)
	title = models.CharField(max_length=250)
	slug = models.SlugField(max_length=250, unique='publish')
	subTitle = models.CharField(max_length=250,null=True, blank=True)
	explore = models.CharField(max_length=50,choices=EXPLORE_CHOICES, default='No')
	excerptContent = models.TextField(null=True, blank=True)
	content = models.TextField(null=True, blank=True)
	blogImage = models.ImageField(upload_to='blog/images', null=True, blank=True)
	blogVideo = models.FileField(upload_to ='blog/videos/', null=True, blank=True, validators=[FileExtensionValidator(ALLOWED_TYPES)])
	videoLink = models.CharField(max_length=250, null=True, blank=True)
	tags = TaggableManager(blank=True)
	category = models.ManyToManyField(categoryOptions,blank=True, related_name='categoryBV')
	subCategory = models.ManyToManyField(subCategoryOptions,blank=True, related_name='subCategoryBV')
	relatedResearchReports = models.ManyToManyField(stockBasicDetail,blank=True, related_name='relatedResearchReportsBV')
	releasedDate = models.DateField(null=True, blank=True)
	publish = models.DateTimeField(default=timezone.now)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	status = models.CharField(max_length=50,choices=STATUS_CHOICES, default='Draft')
	showinpitch = models.BooleanField(null=True, blank=True, default=False)
	showinhead = models.BooleanField(null=True, blank=True, default=False)

	def __str__(self):
		return self.title or '--Name not provided--'

	class Meta:
		verbose_name_plural = 'Blog Video Profile'

	def get_absolute_url(self):
		return reverse('videoBlogApp:videoDetailURL', args=[self.slug])

	def get_current_image(self):
		if self.blogImage:
			return self.blogImage.url
		else:
			return 'javascript:void(0);'

	def releaseDate_self(self):
		if self.releasedDate:
			return self.releasedDate
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
		return 'Video Blog'


class blogVideoListingDM(models.Model):
	metaTitleVideo = models.CharField(max_length=1000,null=True, blank=True)
	metaDescriptionVideo = models.TextField(null=True, blank=True)
	metaKeywordsVideo = models.TextField(null=True, blank=True)
	tags = TaggableManager(blank=True)
	featuredImage = models.ImageField(upload_to='blog/images', null=True, blank=True)
	publish = models.DateTimeField(default=timezone.now)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	status = models.CharField(max_length=50,choices=STATUS_CHOICES, default='Draft')

	def __str__(self):
		return self.metaTitleVideo or '--Name not provided--'

	class Meta:
		verbose_name_plural = 'Blog Video Listing DM'

class blogVideoDetailedDM(models.Model):
	blogProfileName = models.OneToOneField(blogVideos, on_delete=models.CASCADE, related_name='blogProfileNameBVDDM')
	metaTitleVideo = models.CharField(max_length=1000,null=True, blank=True)
	metaDescriptionVideo = models.TextField(null=True, blank=True)
	metaKeywordsVideo = models.TextField(null=True, blank=True)
	tagsVideo = models.CharField(max_length=1000, null=True, blank=True)
	featuredImage = models.ImageField(upload_to='blog/images', null=True, blank=True)
	publish = models.DateTimeField(default=timezone.now)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	status = models.CharField(max_length=50,choices=STATUS_CHOICES, default='Draft')

	def __str__(self):
		return self.metaTitleVideo or '--Name not provided--'

	class Meta:
		verbose_name_plural = 'Blog Video Detailed DM'




class blogPageSectionsOrdering(models.Model):
	displayedCategories = models.ManyToManyField(categoryOptions,blank=True, related_name='categoryDCBPSO')
	displayedSubCategories = models.ManyToManyField(subCategoryOptions,blank=True, related_name='subCategoryDCBPSO')
	lastUpdateBy = models.ForeignKey(User,on_delete=models.CASCADE, related_name='authorDCBPSO', null=True, blank=True)

	class Meta:
		verbose_name_plural = 'Do Not Touch This Model-1'


class videoBlogHits(models.Model):
	videoBlog = models.ForeignKey(blogVideos,on_delete=models.CASCADE, related_name='videoBlogVBH', null=True, blank=True)
	hitBy = models.ForeignKey(User,on_delete=models.CASCADE, related_name='hitByVBH', null=True, blank=True)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)

	def __str__(self):
		return str(self.videoBlog) or '--Name not provided--'

	class Meta:
		verbose_name_plural = 'Blog Video Hits'


class Comment(MPTTModel):
	videoPost = models.ForeignKey(blogVideos,blank=True, on_delete=models.SET_NULL,null=True, related_name='videoPostC')
	parent = TreeForeignKey('self', on_delete=models.CASCADE,null=True, blank=True, related_name='children')
	name = models.CharField(max_length=250)
	content = models.TextField(null=True, blank=True)
	publish = models.DateTimeField(default=timezone.now)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	status = models.CharField(max_length=50,choices=STATUS_CHOICES, default='draft')
	
	class MPTTMeta:
		order_insertion_by = ['publish']

	def __str__(self):
		return self.name or '--Name not provided--'

	class Meta:
		verbose_name_plural = 'Video Comment Details'


class videosHeadingDM(models.Model):
	videoBlog = models.ForeignKey(blogVideos,on_delete=models.CASCADE, related_name='videoBlogVBDM', null=True, blank=True)
	name = models.CharField(max_length=1000, null=True, blank=True)
	description = models.TextField(null=True, blank=True)
	publish = models.DateTimeField(default=timezone.now)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	status = models.CharField(max_length=50,choices=STATUS_CHOICES, default='draft')

	def __str__(self):
		return self.name or '--Name not provided--'



