from django.db import models
from django.core.validators import FileExtensionValidator
import datetime
from django.utils import timezone
from django.contrib.auth.models import User
from employeeApp.models import city, state, country
from stockApp.models import categoryOptions, stockEssentials, stockBasicDetail
from stockApp.peersCrawl import getScreenerPriceForStockByUrl
from screenerStoreApp.models import stockPriceScreener


STATUS_CHOICES = (
	('published', 'Published'),
	('draft', 'Draft'),
	)

PACKAGE_TYPE = (
	('Regular', 'Regular'),
	('Premium', 'Premium'),
	)

DURATION_CHOICES = (
	('one_off', 'One Off'),
	('premium', 'Premium'),
	)

SHARE_CHOICES = (
	('financial_year', 'Financial year'),
	('convertible_equity', 'Convertible Equity'),
	)

# Create your models here.

class seedFundingBanner(models.Model):
	#productMainPage = models.OneToOneField(productBanner, on_delete=models.CASCADE, related_name='productMainPageSFB')
	title = models.TextField(null=True, blank=True)
	content = models.TextField(null=True, blank=True)
	image = models.ImageField(upload_to='images/documents', null=True, blank=True, validators=[FileExtensionValidator(['jpg', 'png', 'jpeg'])])
	image_alt_tag = models.CharField(max_length=256, null=True, blank=True)
	button_1_ActionUrl = models.URLField(null=True, blank=True)
	button_2_ActionUrl = models.URLField(null=True, blank=True)
	backgroundImage = models.ImageField(upload_to='images/documents', null=True, blank=True, validators=[FileExtensionValidator(['jpg', 'png', 'jpeg'])])
	backgroundImage_alt_tag = models.CharField(max_length=1000, null=True, blank=True)
	author = models.CharField(max_length=100, null=True, blank=True)
	publish = models.DateTimeField(default=timezone.now)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now_add=True)
	status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
	

	def __str__(self):
		return self.title or '--Name not provided'

	class Meta:
			verbose_name_plural = 'Seed Funding Banner'

class seedFundRaisingJourney(models.Model):
	#productMainPage = models.OneToOneField(productBanner, on_delete=models.CASCADE, related_name='productMainPageSFRJ')
	excerptContent = models.TextField(null=True, blank=True)
	image = models.ImageField(upload_to='images/documents', null=True, blank=True, validators=[FileExtensionValidator(['jpg', 'png', 'jpeg'])])
	image_alt_tag = models.CharField(max_length=256, null=True, blank=True)
	author = models.CharField(max_length=100, null=True, blank=True)
	publish = models.DateTimeField(default=timezone.now)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now_add=True)
	status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')


	def __str__(self):
		return '--Name not provided'

	class Meta:
		verbose_name_plural = 'Seed Fund Raising Journey'



class seedFundingAppFeature(models.Model):
	#productMainPage = models.ForeignKey('productBanner', on_delete=models.SET_NULL, related_name='productMainPageSFAF', null=True, blank=True)
	title = models.CharField(max_length=1000, null=True, blank=True)
	excerptContent = models.TextField(null=True, blank=True)
	headingOneTitle = models.CharField(max_length=100, null=True, blank=True)
	headingOneContent = models.TextField(null=True, blank=True)
	headingTwoTitle = models.CharField(max_length=100, null=True, blank=True)
	headingTwoContent = models.TextField(null=True, blank=True)
	image = models.ImageField(upload_to='images/documents', null=True, blank=True, validators=[FileExtensionValidator(['jpg', 'png', 'jpeg'])])
	image_alt_tag = models.CharField(max_length=256, null=True, blank=True)

	author = models.CharField(max_length=100, null=True, blank=True)
	publish = models.DateTimeField(default=timezone.now)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now_add=True)
	status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')


	def __str__(self):
		return '--Name not provided'

	class Meta:
		verbose_name_plural = 'Seed Funding App Feature'


class seedFundingFAQMain(models.Model):
	# productMainPage = models.OneToOneField(seedFundingFAQMain, on_delete=models.CASCADE, related_name='productMainPageSFFM')
	excerptContent = models.TextField(null=True, blank=True)


	author = models.CharField(max_length=100, null=True, blank=True)
	publish = models.DateTimeField(default=timezone.now)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now_add=True)
	status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='regular')

	def __str__(self):
		return '--Name not provided'

	class Meta:
		verbose_name_plural = 'Seed Funding FAQ Main'



class seedFundingFAQs(models.Model):
	FAQ = models.ForeignKey('seedFundingFAQMain', on_delete=models.SET_NULL, related_name='faqSFF', null=True, blank=True)
	questions = models.CharField(max_length=1000, null=True, blank=True)
	answers = models.TextField(null=True, blank=True)

	author = models.CharField(max_length=100, null=True, blank=True)
	publish = models.DateTimeField(default=timezone.now)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now_add=True)
	status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

	def __str__(self):
		return '--Name not provided' 

	class Meta:
		verbose_name_plural = 'Seed Funding FAQs'


class seedFundingPricingPlan(models.Model):
	#productMainPage = models.OneToOneField(productBanner, on_delete=models.CASCADE, related_name='productMainPageSFPP')
	image = models.ImageField(upload_to='images/documents', null=True, blank=True, validators=[FileExtensionValidator(['jpg', 'png', 'jpeg'])])
	image_alt_tag = models.CharField(max_length=256, null=True, blank=True)
	excerptContent = models.TextField(null=True, blank=True)

	author = models.CharField(max_length=100, null=True, blank=True)
	publish = models.DateTimeField(default=timezone.now)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now_add=True)
	status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

	def __str__(self):
		return '--Name not provided' 

	class Meta:
		verbose_name_plural = 'Seed Funding Pricing Plan'



class earlyFundingBanner(models.Model):
	#productMainPage = models.OneToOneField(productBanner, on_delete=models.CASCADE, related_name='productMainPageSFB')
	title = models.TextField(null=True, blank=True)
	content = models.TextField(null=True, blank=True)
	image = models.ImageField(upload_to='images/documents', null=True, blank=True, validators=[FileExtensionValidator(['jpg','png','jpeg'])])
	image_alt_tag = models.CharField(max_length=256, null=True, blank=True)
	button_1_ActionUrl = models.CharField(max_length=100, null=True, blank=True)
	button_2_ActionUrl = models.CharField(max_length=100, null=True, blank=True)
	
	
	author = models.CharField(max_length=100, null=True, blank=True)
	publish = models.DateTimeField(default=timezone.now)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now_add=True)
	status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
	

	def __str__(self):
		return self.title or '--Name not provided'

	class Meta:
			verbose_name_plural = 'Early Funding Banner'


class earlyFundRaisingJourney(models.Model):
	excerptContent = models.TextField(null=True, blank=True)
	image = models.ImageField(upload_to='images/documents', null=True, blank=True, validators=[FileExtensionValidator(['jpg','png','jpeg'])])
	image_alt_tag = models.CharField(max_length=256, null=True, blank=True)
	author = models.CharField(max_length=100, null=True, blank=True)
	publish = models.DateTimeField(default=timezone.now)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now_add=True)
	status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')


	def __str__(self):
		return '--Name not provided'

	class Meta:
		verbose_name_plural = 'Early Fund Raising Journey'



class earlyFundingAppFeature(models.Model):
	title = models.CharField(max_length=1000, null=True, blank=True)
	excerptContent = models.TextField(null=True, blank=True)
	headingOneTitle = models.CharField(max_length=1000, null=True, blank=True)
	headingOneContent = models.TextField(null=True, blank=True)
	headingTwoTitle = models.CharField(max_length=1000, null=True, blank=True)
	headingTwoContent = models.TextField(null=True, blank=True)
	image = models.ImageField(upload_to='images/documents', null=True, blank=True, validators=[FileExtensionValidator(['jpg', 'png', 'jpeg'])])
	image_alt_tag = models.CharField(max_length=256, null=True, blank=True)

	author = models.CharField(max_length=100, null=True, blank=True)
	publish = models.DateTimeField(default=timezone.now)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now_add=True)
	status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')


	def __str__(self):
		return '--Name not provided'

	class Meta:
		verbose_name_plural = 'Early Funding App Feature'


class earlyFundingFAQMain(models.Model):
	#productMainPage = models.OneToOneField(productBanner, on_delete=models.CASCADE, related_name='productMainPageSFFM')
	excerptContent = models.TextField(null=True, blank=True)


	author = models.CharField(max_length=100, null=True, blank=True)
	publish = models.DateTimeField(default=timezone.now)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now_add=True)
	status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Regular')

	def __str__(self):
		return '--Name not provided'

	class Meta:
		verbose_name_plural = 'Early Funding FAQ Main'



class earlyFundingFAQs(models.Model):
	faq = models.ForeignKey('earlyFundingFAQMain', on_delete=models.SET_NULL, related_name='faqEFF', null=True, blank=True)
	questions = models.CharField(max_length=1000, null=True, blank=True)
	answers = models.TextField(null=True, blank=True)

	author = models.CharField(max_length=100, null=True, blank=True)
	publish = models.DateTimeField(default=timezone.now)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now_add=True)
	status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

	def __str__(self):
		return '--Name not provided' 

	class Meta:
		verbose_name_plural = 'Early Funding FAQs'


class earlyFundingPricingPlan(models.Model):
	#productMainPage = models.OneToOneField(productBanner, on_delete=models.CASCADE, related_name='productMainPageSFPP')
	excerptContent = models.TextField(null=True, blank=True)
	image = models.ImageField(upload_to='images/documents', null=True, blank=True, validators=[FileExtensionValidator(['jpg', 'png', 'jpeg'])])
	image_alt_tag = models.CharField(max_length=256, null=True, blank=True)
	
	author = models.CharField(max_length=100, null=True, blank=True)
	publish = models.DateTimeField(default=timezone.now)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now_add=True)
	status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

	def __str__(self):
		return '--Name not provided' 

	class Meta:
		verbose_name_plural = 'Early Funding Pricing Plan'



class earlyFundingPackages(models.Model):
	duration = models.CharField(max_length=10, choices=DURATION_CHOICES, default='one_off') 
	pitchDeckImage = models.ImageField(upload_to='images/documents', null=True, blank=True, validators=[FileExtensionValidator(['jpg', 'png', 'jpeg'])])
	pitchDeckImage_alt_tag = models.CharField(max_length=256, null=True, blank=True)
	pitchDeckTitle = models.CharField(max_length=1000,null=True, blank=True)
	pitchDeckAmount = models.BigIntegerField(null=True, blank=True)

	investmentDeckImage = models.ImageField(upload_to='images/documents', null=True, blank=True, validators=[FileExtensionValidator(['jpg', 'png', 'jpeg'])])
	investmentDeckImage_alt_tag = models.CharField(max_length=256, null=True, blank=True)
	investmentDeckTitle = models.CharField(max_length=1000,null=True, blank=True)
	investmentDeckAmount = models.BigIntegerField(null=True, blank=True)

	equityResearchReportImage = models.ImageField(upload_to='images/documents', null=True, blank=True, validators=[FileExtensionValidator(['jpg', 'png', 'jpeg'])])
	equityResearchReportImage_alt_tag = models.CharField(max_length=256, null=True, blank=True)
	equityResearchReportTitle = models.CharField(max_length=1000,null=True, blank=True)
	equityResearchReportAmount = models.BigIntegerField(null=True, blank=True)

	valuationReportImage = models.ImageField(upload_to='images/documents', null=True, blank=True, validators=[FileExtensionValidator(['jpg', 'png', 'jpeg'])])
	valuationReportImage_alt_tag = models.CharField(max_length=256, null=True, blank=True)
	valuationReportTitle = models.CharField(max_length=1000,null=True, blank=True)
	valuationReportAmount = models.BigIntegerField(null=True, blank=True)

	projectionsImage = models.ImageField(upload_to='images/documents', null=True, blank=True, validators=[FileExtensionValidator(['jpg', 'png', 'jpeg'])])
	projectionsImage_alt_tag = models.CharField(max_length=256, null=True, blank=True)
	projectionsTitle = models.CharField(max_length=1000,null=True, blank=True)
	projectionsAmount = models.BigIntegerField(null=True, blank=True)

	equityRestructuringImage = models.ImageField(upload_to='images/documents', null=True, blank=True, validators=[FileExtensionValidator(['jpg', 'png', 'jpeg'])])
	equityRestructuringImage_alt_tag = models.CharField(max_length=256, null=True, blank=True)
	equityRestructuringTitle = models.CharField(max_length=1000,null=True, blank=True)
	equityRestructuringAmount = models.BigIntegerField(null=True, blank=True)
	total = models.BigIntegerField(null=True, blank=True)
	
	author = models.CharField(max_length=100, null=True, blank=True)
	publish = models.DateTimeField(default=timezone.now)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now_add=True)
	status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')


	def __str__(self):
		return '--Name not provided' 
		
	class Meta:
		verbose_name_plural = 'Early Funding Packages'


class growthFundingBanner(models.Model):
	# productMainPage = models.OneToOneField(productBanner, on_delete=models.CASCADE, related_name='productMainPageSFB')
	title = models.TextField(null=True, blank=True)
	content = models.TextField(null=True, blank=True)
	image = models.ImageField(upload_to='images/documents', null=True, blank=True, validators=[FileExtensionValidator(['jpg','png','jpeg'])])
	image_alt_tag = models.CharField(max_length=256, null=True, blank=True)
	button_1_ActionUrl = models.CharField(max_length=100, null=True, blank=True)
	button_2_ActionUrl = models.URLField(null=True, blank=True)

	
	author = models.CharField(max_length=100, null=True, blank=True)
	publish = models.DateTimeField(default=timezone.now)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now_add=True)
	status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
	

	def __str__(self):
		return self.title or '--Name not provided'

	class Meta:
			verbose_name_plural = 'Growth Funding Banner'


class growthFundRaisingJourney(models.Model):
	# productMainPage = models.OneToOneField(productBanner, on_delete=models.CASCADE, related_name='productMainPageSFRJ')
	excerptContent = models.TextField(null=True, blank=True)
	image = models.ImageField(upload_to='images/documents', null=True, blank=True, validators=[FileExtensionValidator(['jpg','png','jpeg'])])
	image_alt_tag = models.CharField(max_length=256, null=True, blank=True)
	
	author = models.CharField(max_length=100, null=True, blank=True)
	publish = models.DateTimeField(default=timezone.now)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now_add=True)
	status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')


	def __str__(self):
		return '--Name not provided'

	class Meta:
		verbose_name_plural = 'Growth Fund Raising Journey'



class growthFundingAppFeature(models.Model):
	# productMainPage = models.ForeignKey('productBanner', on_delete=models.SET_NULL, related_name='productMainPageSFAF', null=True, blank=True)
	title = models.CharField(max_length=1000, null=True, blank=True)
	excerptContent = models.TextField(null=True, blank=True)
	headingOneTitle = models.CharField(max_length=1000, null=True, blank=True)
	headingOneContent = models.TextField(null=True, blank=True)
	headingTwoTitle = models.CharField(max_length=1000, null=True, blank=True)
	headingTwoContent = models.TextField(null=True, blank=True)
	image = models.ImageField(upload_to='images/documents', null=True, blank=True, validators=[FileExtensionValidator(['jpg','png','jpeg'])])
	image_alt_tag = models.CharField(max_length=256, null=True, blank=True)
	

	author = models.CharField(max_length=100, null=True, blank=True)
	publish = models.DateTimeField(default=timezone.now)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now_add=True)
	status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')


	def __str__(self):
		return '--Name not provided'

	class Meta:
		verbose_name_plural = 'Growth Funding App Feature'


class growthFundingFAQMain(models.Model):
	# productMainPage = models.OneToOneField(productBanner, on_delete=models.CASCADE, related_name='productMainPageSFFM')
	excerptContent = models.TextField(null=True, blank=True)


	author = models.CharField(max_length=100, null=True, blank=True)
	publish = models.DateTimeField(default=timezone.now)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now_add=True)
	status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='regular')

	def __str__(self):
		return '--Name not provided'

	class Meta:
		verbose_name_plural = 'Growth Funding FAQ Main'


class privateBoutiqueFAQNRI(models.Model):
	question = models.CharField(max_length=1000, null=True, blank=True)
	answer = models.TextField(null=True, blank=True)
	author = models.CharField(max_length=100, null=True, blank=True)
	publish = models.DateTimeField(default=timezone.now)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now_add=True)
	status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
	
	def __str__(self):
		return '--Name not provided'

	class Meta:
			verbose_name_plural = 'Private Boutique FAQs NRI'


class privateBoutiqueFAQLegality(models.Model):
	question = models.CharField(max_length=1000, null=True, blank=True)
	answer = models.TextField(null=True, blank=True)
	author = models.CharField(max_length=100, null=True, blank=True)
	publish = models.DateTimeField(default=timezone.now)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now_add=True)
	status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
	
	def __str__(self):
		return '--Name not provided'

	class Meta:
			verbose_name_plural = 'Private Boutique FAQs Legality'


class growthFundingFAQs(models.Model):
	FAQ = models.ForeignKey('growthFundingFAQMain', on_delete=models.SET_NULL, related_name='faqSFF', null=True, blank=True)
	questions = models.CharField(max_length=1000,null=True, blank=True)
	answers = models.TextField(null=True, blank=True)

	author = models.CharField(max_length=100, null=True, blank=True)
	publish = models.DateTimeField(default=timezone.now)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now_add=True)
	status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

	def __str__(self):
		return '--Name not provided' 

	class Meta:
		verbose_name_plural = 'Growth Funding FAQs'


class growthFundingPricingPlan(models.Model):
	# productMainPage = models.OneToOneField(productBanner, on_delete=models.CASCADE, related_name='productMainPageSFPP')
	excerptContent = models.TextField(null=True, blank=True)
	image = models.ImageField(upload_to='images/documents', null=True, blank=True, validators=[FileExtensionValidator(['jpg','png','jpeg'])])
	image_alt_tag = models.CharField(max_length=256, null=True, blank=True)
	

	author = models.CharField(max_length=100, null=True, blank=True)
	publish = models.DateTimeField(default=timezone.now)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now_add=True)
	status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

	def __str__(self):
		return '--Name not provided' 

	class Meta:
		verbose_name_plural = 'Growth Funding Pricing Plan'



class growthFundingPackages(models.Model):
	duration = models.CharField(max_length=10, choices=DURATION_CHOICES, default='one_off') 
	pitchDeckImage = models.ImageField(upload_to='images/documents', null=True, blank=True, validators=[FileExtensionValidator(['jpg', 'png', 'jpeg'])])
	pitchDeckImage_alt_tag = models.CharField(max_length=256, null=True, blank=True)
	pitchDeckTitle = models.CharField(max_length=1000,null=True, blank=True)
	pitchDeckAmount = models.BigIntegerField(null=True, blank=True)

	investmentDeckImage = models.ImageField(upload_to='images/documents', null=True, blank=True, validators=[FileExtensionValidator(['jpg', 'png', 'jpeg'])])
	investmentDeckImage_alt_tag = models.CharField(max_length=256, null=True, blank=True)
	investmentDeckTitle = models.CharField(max_length=1000,null=True, blank=True)
	investmentDeckAmount = models.BigIntegerField(null=True, blank=True)

	equityResearchReportImage = models.ImageField(upload_to='images/documents', null=True, blank=True, validators=[FileExtensionValidator(['jpg', 'png', 'jpeg'])])
	equityResearchReportImage_alt_tag = models.CharField(max_length=256, null=True, blank=True)
	equityResearchReportTitle = models.CharField(max_length=1000,null=True, blank=True)
	equityResearchReportAmount = models.BigIntegerField(null=True, blank=True)

	valuationReportImage = models.ImageField(upload_to='images/documents', null=True, blank=True, validators=[FileExtensionValidator(['jpg', 'png', 'jpeg'])])
	valuationReportImage_alt_tag = models.CharField(max_length=256, null=True, blank=True)
	valuationReportTitle = models.CharField(max_length=1000,null=True, blank=True)
	valuationReportAmount = models.BigIntegerField(null=True, blank=True)

	projectionsImage = models.ImageField(upload_to='images/documents', null=True, blank=True, validators=[FileExtensionValidator(['jpg', 'png', 'jpeg'])])
	projectionsImage_alt_tag = models.CharField(max_length=256, null=True, blank=True)
	projectionsTitle = models.CharField(max_length=1000,null=True, blank=True)
	projectionsAmount = models.BigIntegerField(null=True, blank=True)

	equityRestructuringImage = models.ImageField(upload_to='images/documents', null=True, blank=True, validators=[FileExtensionValidator(['jpg', 'png', 'jpeg'])])
	equityRestructuringImage_alt_tag = models.CharField(max_length=256, null=True, blank=True)
	equityRestructuringTitle = models.CharField(max_length=1000,null=True, blank=True)
	equityRestructuringAmount = models.BigIntegerField(null=True, blank=True)
	total = models.BigIntegerField(null=True, blank=True)
	
	author = models.CharField(max_length=100, null=True, blank=True)
	publish = models.DateTimeField(default=timezone.now)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now_add=True)
	status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')


	def __str__(self):
		return '--Name not provided' 

	class Meta:
		verbose_name_plural = 'Growth Funding Packages'

#
class seedFundingContactUsSignup(models.Model):
	contactPerson = models.CharField(max_length=1000, null=True, blank=True)
	email = models.EmailField(max_length=1000,null=True, blank=True)
	mobile = models.BigIntegerField(null=True, blank=True)
	city = models.ForeignKey(city, on_delete=models.CASCADE, null=True, blank=True)
	nameOfOrganization = models.CharField(max_length=1000,null=True, blank=True)
	presentRole = models.CharField(max_length=1000, null=True, blank=True)
	annualTurnover = models.BigIntegerField(null=True, blank=True)

	author = models.CharField(max_length=100, null=True, blank=True)
	publish = models.DateTimeField(default=timezone.now)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now_add=True)
	status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

	def __str__(self):
		return self.contactPerson or "--Name not Provided"
	class Meta:
		verbose_name_plural = 'Seed Funding Contact Us Form'


class seedFundingContactUsBanner(models.Model):
	bannerImage = models.ImageField(upload_to='images/documents', null=True, blank=True, validators=[FileExtensionValidator(['jpg','png','jpeg'])])
	bannerImage_alt_tag = models.CharField(max_length=1000, null=True, blank=True)


	author = models.CharField(max_length=100, null=True, blank=True)
	publish = models.DateTimeField(default=timezone.now)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now_add=True)
	status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

	def __str__(self):
		return "--Name not Provided"
	class Meta:
		verbose_name_plural = 'Seed Funding Contact Us Banner'


class seedFundingContactUsKnowMore(models.Model):
	title = models.CharField(max_length=1000, null=True, blank=True)
	excerptContent = models.TextField(null=True, blank=True)

	author = models.CharField(max_length=100, null=True, blank=True)
	publish = models.DateTimeField(default=timezone.now)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now_add=True)
	status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

	def __str__(self):
		return "--Name not Provided"
	class Meta:
		verbose_name_plural = 'Seed Funding Contact Us Know More'


class seedFundingContactUsKnowMoreFAQs(models.Model):
	heading = models.CharField(max_length=1000, null=True, blank=True)
	content = models.TextField(null=True, blank=True)

	author = models.CharField(max_length=100, null=True, blank=True)
	publish = models.DateTimeField(default=timezone.now)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now_add=True)
	status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

	def __str__(self):
		return "--Name not Provided"
	class Meta:
		verbose_name_plural = 'Seed Funding Contact Us Know More FAQs'


class seedFundingDM(models.Model):
	metaTitle = models.CharField(max_length=1000, null=True, blank=True)
	metaDescription = models.CharField(max_length=1000, null=True, blank=True)
	metaTags = models.CharField(max_length=1000, null=True, blank=True)
	metaFeaturedImage = models.ImageField(upload_to='images/documents', null=True, blank=True, validators=[FileExtensionValidator(['jpg','png','jpeg'])])
	metaKeywords = models.CharField(max_length=1000, null=True, blank=True)


	author = models.CharField(max_length=100, null=True, blank=True)
	publish = models.DateTimeField(default=timezone.now)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now_add=True)
	status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

	def __str__(self):
		return self.metaTitle or '--Name not provided' 

	class Meta:
		verbose_name_plural = 'Seed Funding DM'

class seedFundingContactDM(models.Model):
	metaTitle = models.CharField(max_length=1000, null=True, blank=True)
	metaDescription = models.CharField(max_length=1000, null=True, blank=True)
	metaTags = models.CharField(max_length=1000, null=True, blank=True)
	metaFeaturedImage = models.ImageField(upload_to='images/documents', null=True, blank=True, validators=[FileExtensionValidator(['jpg','png','jpeg'])])
	metaKeywords = models.CharField(max_length=1000, null=True, blank=True)


	author = models.CharField(max_length=100, null=True, blank=True)
	publish = models.DateTimeField(default=timezone.now)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now_add=True)
	status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

	def __str__(self):
		return self.metaTitle or '--Name not provided' 

	class Meta:
		verbose_name_plural = 'Seed Funding Contact DM'

class growthFundingDM(models.Model):
	metaTitle = models.CharField(max_length=1000, null=True, blank=True)
	metaDescription = models.CharField(max_length=1000, null=True, blank=True)
	metaTags = models.CharField(max_length=1000, null=True, blank=True)
	metaFeaturedImage = models.ImageField(upload_to='images/documents', null=True, blank=True, validators=[FileExtensionValidator(['jpg','png','jpeg'])])
	metaKeywords = models.CharField(max_length=1000, null=True, blank=True)


	author = models.CharField(max_length=100, null=True, blank=True)
	publish = models.DateTimeField(default=timezone.now)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now_add=True)
	status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

	def __str__(self):
		return self.metaTitle or '--Name not provided' 

	class Meta:
		verbose_name_plural = 'Growth Funding DM'

class growthFundingContactDM(models.Model):
	metaTitle = models.CharField(max_length=1000, null=True, blank=True)
	metaDescription = models.CharField(max_length=1000, null=True, blank=True)
	metaTags = models.CharField(max_length=1000, null=True, blank=True)
	metaFeaturedImage = models.ImageField(upload_to='images/documents', null=True, blank=True, validators=[FileExtensionValidator(['jpg','png','jpeg'])])
	metaKeywords = models.CharField(max_length=1000, null=True, blank=True)


	author = models.CharField(max_length=100, null=True, blank=True)
	publish = models.DateTimeField(default=timezone.now)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now_add=True)
	status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

	def __str__(self):
		return self.metaTitle or '--Name not provided'

	class Meta:
		verbose_name_plural = 'Growth Funding Contact DM'

class earlyFundingDM(models.Model):
	metaTitle = models.CharField(max_length=1000, null=True, blank=True)
	metaDescription = models.CharField(max_length=1000, null=True, blank=True)
	metaTags = models.CharField(max_length=1000, null=True, blank=True)
	metaFeaturedImage = models.ImageField(upload_to='images/documents', null=True, blank=True, validators=[FileExtensionValidator(['jpg','png','jpeg'])])
	metaKeywords = models.CharField(max_length=1000, null=True, blank=True)


	author = models.CharField(max_length=100, null=True, blank=True)
	publish = models.DateTimeField(default=timezone.now)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now_add=True)
	status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

	def __str__(self):
		return self.metaTitle or '--Name not provided' 

	class Meta:
		verbose_name_plural = 'Early Funding DM'

class earlyFundingContactDM(models.Model):
	metaTitle = models.CharField(max_length=1000, null=True, blank=True)
	metaDescription = models.CharField(max_length=1000, null=True, blank=True)
	metaTags = models.CharField(max_length=1000, null=True, blank=True)
	metaFeaturedImage = models.ImageField(upload_to='images/documents', null=True, blank=True, validators=[FileExtensionValidator(['jpg','png','jpeg'])])
	metaKeywords = models.CharField(max_length=1000, null=True, blank=True)


	author = models.CharField(max_length=100, null=True, blank=True)
	publish = models.DateTimeField(default=timezone.now)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now_add=True)
	status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

	def __str__(self):
		return self.metaTitle or '--Name not provided' 

	class Meta:
		verbose_name_plural = 'Early Funding Contact DM'


class growthFundingContactUsSignup(models.Model):
	contactPerson = models.CharField(max_length=1000, null=True, blank=True)
	email = models.EmailField(max_length=1000,null=True, blank=True)
	mobile = models.BigIntegerField(null=True, blank=True)
	city = models.ForeignKey(city, on_delete=models.CASCADE, null=True, blank=True)
	nameOfOrganization = models.CharField(max_length=1000,null=True, blank=True)
	presentRole = models.CharField(max_length=1000, null=True, blank=True)
	annualTurnover = models.BigIntegerField(null=True, blank=True)

	author = models.CharField(max_length=100, null=True, blank=True)
	publish = models.DateTimeField(default=timezone.now)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now_add=True)
	status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

	def __str__(self):
		return self.contactPerson or "--Name not Provided"
	class Meta:
		verbose_name_plural = 'Growth Funding Contact Us Form'


class growthFundingContactUsBanner(models.Model):
	bannerImage = models.ImageField(upload_to='images/documents', null=True, blank=True, validators=[FileExtensionValidator(['jpg','png','jpeg'])])
	bannerImage_alt_tag = models.CharField(max_length=1000, null=True, blank=True)


	author = models.CharField(max_length=100, null=True, blank=True)
	publish = models.DateTimeField(default=timezone.now)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now_add=True)
	status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

	def __str__(self):
		return "--Name not Provided"
	class Meta:
		verbose_name_plural = 'Growth Funding Contact Us Banner'


class growthFundingContactUsKnowMore(models.Model):
	title = models.CharField(max_length=1000, null=True, blank=True)
	excerptContent = models.TextField(null=True, blank=True)

	author = models.CharField(max_length=100, null=True, blank=True)
	publish = models.DateTimeField(default=timezone.now)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now_add=True)
	status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

	def __str__(self):
		return "--Name not Provided"
	class Meta:
		verbose_name_plural = 'Growth Funding Contact Us Know More'


class growthFundingContactUsKnowMoreFAQs(models.Model):
	heading = models.CharField(max_length=1000, null=True, blank=True)
	content = models.TextField(null=True, blank=True)

	author = models.CharField(max_length=100, null=True, blank=True)
	publish = models.DateTimeField(default=timezone.now)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now_add=True)
	status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

	def __str__(self):
		return "--Name not Provided"
	class Meta:
		verbose_name_plural = 'Growth Funding Contact Us Know More FAQs'


class earlyFundingContactUsSignup(models.Model):
	contactPerson = models.CharField(max_length=1000, null=True, blank=True)
	email = models.EmailField(max_length=1000,null=True, blank=True)
	mobile = models.BigIntegerField(null=True, blank=True)
	city = models.ForeignKey(city, on_delete=models.CASCADE, null=True, blank=True)
	nameOfOrganization = models.CharField(max_length=1000,null=True, blank=True)
	presentRole = models.CharField(max_length=1000, null=True, blank=True)
	annualTurnover = models.BigIntegerField(null=True, blank=True)

	author = models.CharField(max_length=100, null=True, blank=True)
	publish = models.DateTimeField(default=timezone.now)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now_add=True)
	status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

	def __str__(self):
		return self.contactPerson or "--Name not Provided"
	class Meta:
		verbose_name_plural = 'Early Funding Contact Us Form'


class earlyFundingContactUsBanner(models.Model):
	bannerImage = models.ImageField(upload_to='images/documents', null=True, blank=True, validators=[FileExtensionValidator(['jpg','png','jpeg'])])
	bannerImage_alt_tag = models.CharField(max_length=1000, null=True, blank=True)


	author = models.CharField(max_length=100, null=True, blank=True)
	publish = models.DateTimeField(default=timezone.now)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now_add=True)
	status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

	def __str__(self):
		return "--Name not Provided"
	class Meta:
		verbose_name_plural = 'Early Funding Contact Us Banner'


class earlyFundingContactUsKnowMore(models.Model):
	title = models.CharField(max_length=1000, null=True, blank=True)
	excerptContent = models.TextField(null=True, blank=True)

	author = models.CharField(max_length=100, null=True, blank=True)
	publish = models.DateTimeField(default=timezone.now)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now_add=True)
	status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

	def __str__(self):
		return "--Name not Provided"
	class Meta:
		verbose_name_plural = 'Early Funding Contact Us Know More'


class earlyFundingContactUsKnowMoreFAQs(models.Model):
	heading = models.CharField(max_length=1000, null=True, blank=True)
	content = models.TextField(null=True, blank=True)

	author = models.CharField(max_length=100, null=True, blank=True)
	publish = models.DateTimeField(default=timezone.now)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now_add=True)
	status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

	def __str__(self):
		return "--Name not Provided"
	class Meta:
		verbose_name_plural = 'Early Funding Contact Us Know More FAQs'



#sell ESOP starts 

from django.db import models
from django.core.validators import FileExtensionValidator
import datetime
from django.utils import timezone
from django.contrib.auth.models import User

STATUS_CHOICES = (
	('published', 'Published'),
	('draft', 'Draft'),
)

DEMAT_CHOICES = (
       ('yes, in demat','Yes, in Demat'),
       ('vested, not in demat', 'Vested, Not in Demat'),
       ('not fully vested','Not Fully Vested'),
   )

ROFR_CHOICES = (
	('yes', 'Yes'),
	('no', 'No'),
	)
# Create your models here.
class sellESOPBanner(models.Model):
	title = models.CharField(max_length=1000, null=True, blank=True)
	content = models.TextField(null=True, blank=True)
	image = models.ImageField(upload_to='images/documents', null=True, blank=True, validators=[FileExtensionValidator(['jpg','png','jpeg'])])
	image_alt_tag = models.CharField(max_length=1000, null=True, blank=True)
	button_ActionUrl = models.URLField(null=True, blank=True)
	
	
	author = models.CharField(max_length=1000, null=True, blank=True)
	publish = models.DateTimeField(default=timezone.now)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now_add=True)
	status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
	

	def __str__(self):
		return self.title or '--Name not provided'

	class Meta:
		verbose_name_plural = 'Sell ESOP Banner'


class sellESOPAboutUs(models.Model):
	title = models.TextField(null=True, blank=True)
	excerptContent = models.TextField(null=True, blank=True)
	author = models.CharField(max_length=1000, null=True, blank=True)
	publish = models.DateTimeField(default=timezone.now)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now_add=True)
	status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
	

	def __str__(self):
		return '--Name not provided'

	class Meta:
		verbose_name_plural = 'Sell ESOP About Us'


class sellESOPFineWordsAboutUs(models.Model):
	title = models.TextField(null=True, blank=True)
	# image = models.ImageField(upload_to='images/documents', null=True, blank=True, validators=[FileExtensionValidator(['jpg','png','jpeg'])])
	# image_alt_tag = models.CharField(max_length=256, null=True, blank=True)
	upload_Gif = models.FileField(upload_to='videos/gif', null=True, blank=True)
	excerptContent = models.TextField(null=True, blank=True)
	author = models.CharField(max_length=1000, null=True, blank=True)
	publish = models.DateTimeField(default=timezone.now)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now_add=True)
	status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
	

	def __str__(self):
		return '--Name not provided'

	class Meta:
		verbose_name_plural = 'Sell ESOP Fine Words About Us'


class sellESOPVideo(models.Model):
	videoID = models.CharField(max_length=1000, null=True, blank=True)

	author = models.CharField(max_length=1000, null=True, blank=True)
	publish = models.DateTimeField(default=timezone.now)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now_add=True)
	status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
	

	def __str__(self):
		return '--Name not provided'

	class Meta:
		verbose_name_plural = 'Sell ESOP Video'


class sellESOPJourney(models.Model):
	image = models.ImageField(upload_to='images/documents', null=True, blank=True, validators=[FileExtensionValidator(['jpg','png','jpeg'])])
	image_alt_tag = models.CharField(max_length=1000, null=True, blank=True)
	excerptContent = models.TextField(null=True, blank=True)
	author = models.CharField(max_length=100, null=True, blank=True)
	publish = models.DateTimeField(default=timezone.now)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now_add=True)
	status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
	

	def __str__(self):
		return '--Name not provided'

	class Meta:
		verbose_name_plural = 'Sell ESOP Journey'


class sellESOPAppFeatures(models.Model):
	title = models.CharField(max_length=1000, null=True, blank=True)
	excerptContent = models.TextField(null=True, blank=True)
	author = models.CharField(max_length=1000, null=True, blank=True)
	publish = models.DateTimeField(default=timezone.now)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now_add=True)
	status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
	

	def __str__(self):
		return '--Name not provided'

	class Meta:
		verbose_name_plural = 'Sell ESOP App Features'


class sellESOPCards(models.Model):
	icon = models.ImageField(upload_to='images/documents', null=True, blank=True, validators=[FileExtensionValidator(['jpg','png','jpeg'])])
	icon_alt_tag = models.CharField(max_length=1000, null=True, blank=True)
	heading = models.CharField(max_length=1000, null=True, blank=True)
	content = models.TextField(null=True, blank=True)
	imageOnHover = models.ImageField(upload_to='images/documents', null=True, blank=True, validators=[FileExtensionValidator(['jpg','png','jpeg'])])
	imageOnHover_alt_tag = models.CharField(max_length=256, null=True, blank=True)
	

	author = models.CharField(max_length=1000, null=True, blank=True)
	publish = models.DateTimeField(default=timezone.now)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now_add=True)
	status = models.CharField(max_length=1000, choices=STATUS_CHOICES, default='draft')
	

	def __str__(self):
		return self.heading or '--Name not provided'

	class Meta:
		verbose_name_plural = 'Sell ESOP Cards'


class sellESOPRunningNumbers(models.Model):
	number = models.BigIntegerField(null=True, blank=True)
	numberContent = models.CharField(max_length=1000, null=True, blank=True)

	author = models.CharField(max_length=100, null=True, blank=True)
	publish = models.DateTimeField(default=timezone.now)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now_add=True)
	status = models.CharField(max_length=1000, choices=STATUS_CHOICES, default='draft')
	

	def __str__(self):
		return self.numberContent or '--Name not provided'

	class Meta:
		verbose_name_plural = 'Sell ESOP Running Numbers'

class sellESOPFAQMain(models.Model):
	excerptContent = models.TextField(null=True, blank=True)


	author = models.CharField(max_length=1000, null=True, blank=True)
	publish = models.DateTimeField(default=timezone.now)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now_add=True)
	status = models.CharField(max_length=1000, choices=STATUS_CHOICES, default='regular')

	def __str__(self):
		return '--Name not provided'

	class Meta:
		verbose_name_plural = 'Sell ESOP FAQ Main'



class sellESOPFAQs(models.Model):
	faq = models.ForeignKey('sellESOPFAQMain', on_delete=models.SET_NULL, related_name='faqSFF', null=True, blank=True)
	questions = models.CharField(max_length=1000, null=True, blank=True)
	answers = models.TextField(null=True, blank=True)

	author = models.CharField(max_length=100, null=True, blank=True)
	publish = models.DateTimeField(default=timezone.now)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now_add=True)
	status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

	def __str__(self):
		return '--Name not provided' 

	class Meta:
		verbose_name_plural = 'Sell ESOP FAQs'

class sellESOPDM(models.Model):
	metaTitle = models.CharField(max_length=1000, null=True, blank=True)
	metaDescription = models.CharField(max_length=1000, null=True, blank=True)
	metaTags = models.CharField(max_length=1000, null=True, blank=True)
	metaFeaturedImage = models.ImageField(upload_to='images/documents', null=True, blank=True, validators=[FileExtensionValidator(['jpg','png','jpeg'])])
	metaKeywords = models.CharField(max_length=1000, null=True, blank=True)


	author = models.CharField(max_length=100, null=True, blank=True)
	publish = models.DateTimeField(default=timezone.now)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now_add=True)
	status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

	def __str__(self):
		return self.metaTitle or '--Name not provided' 

	class Meta:
		verbose_name_plural = 'Sell ESOP DM'

class sellESOPContactDM(models.Model):
	metaTitle = models.CharField(max_length=1000, null=True, blank=True)
	metaDescription = models.CharField(max_length=1000, null=True, blank=True)
	metaTags = models.CharField(max_length=1000, null=True, blank=True)
	metaFeaturedImage = models.ImageField(upload_to='images/documents', null=True, blank=True, validators=[FileExtensionValidator(['jpg','png','jpeg'])])
	metaKeywords = models.CharField(max_length=1000, null=True, blank=True)


	author = models.CharField(max_length=100, null=True, blank=True)
	publish = models.DateTimeField(default=timezone.now)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now_add=True)
	status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

	def __str__(self):
		return self.metaTitle or '--Name not provided' 

	class Meta:
		verbose_name_plural = 'Sell ESOP Contact DM'


class sellESOPContactUs(models.Model):
	contactPerson = models.CharField(max_length=1000, null=True, blank=True)
	email = models.EmailField(max_length=1000, null=True, blank=True)
	mobile = models.BigIntegerField(null=True, blank=True)
	nameOfOrganization = models.CharField(max_length=1000, null=True, blank=True)
	websiteURL = models.URLField(max_length=1000, null=True, blank=True)
	# sharesDemat = models.CharField(max_length=1000,choices=DEMAT_CHOICES, default='yes_in_demat')
	numberOfShares = models.BigIntegerField(null=True, blank=True)
	# rofrRequired = models.CharField(max_length=100, choices=ROFR_CHOICES, default='Yes')

	author = models.CharField(max_length=100, null=True, blank=True)
	publish = models.DateTimeField(default=timezone.now)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now_add=True)
	status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

	def __str__(self):
		return self.contactPerson or '--Name not provided'

	class Meta:
		verbose_name_plural = 'Sell ESOP Contact Us'

class sellESOPContactUsBanner(models.Model):
	bannerImage = models.ImageField(upload_to='images/documents', null=True, blank=True, validators=[FileExtensionValidator(['jpg','png','jpeg'])])
	bannerImage_alt_tag = models.CharField(max_length=1000, null=True, blank=True)


	author = models.CharField(max_length=100, null=True, blank=True)
	publish = models.DateTimeField(default=timezone.now)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now_add=True)
	status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

	def __str__(self):
		return "--Name not Provided"
	class Meta:
		verbose_name_plural = 'sellESOP Contact Us Banner'


class sellESOPContactUsKnowMore(models.Model):
	title = models.CharField(max_length=1000, null=True, blank=True)
	excerptContent = models.TextField(null=True, blank=True)

	author = models.CharField(max_length=100, null=True, blank=True)
	publish = models.DateTimeField(default=timezone.now)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now_add=True)
	status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

	def __str__(self):
		return "--Name not Provided"
	class Meta:
		verbose_name_plural = 'sellESOP Contact Us Know More'


class sellESOPContactUsKnowMoreFAQs(models.Model):
	heading = models.CharField(max_length=1000, null=True, blank=True)
	content = models.TextField(null=True, blank=True)

	author = models.CharField(max_length=100, null=True, blank=True)
	publish = models.DateTimeField(default=timezone.now)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now_add=True)
	status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

	def __str__(self):
		return "--Name not Provided"
	class Meta:
		verbose_name_plural = 'sellESOP Contact Us Know More FAQs'


#
# private-botique


class privateBoutiqueBanner(models.Model):
	title = models.TextField(null=True, blank=True)
	content = models.TextField(null=True, blank=True)
	bannerImage = models.ImageField(upload_to='images/documents', null=True, blank=True, validators=[FileExtensionValidator(['jpg', 'png', 'jpeg'])])
	bannerImage_alt_tag = models.CharField(max_length=1000, null=True, blank=True)
	
	author = models.CharField(max_length=100, null=True, blank=True)
	publish = models.DateTimeField(default=timezone.now)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now_add=True)
	status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
	

	def __str__(self):
		return self.title or '--Name not provided'

	class Meta:
			verbose_name_plural = 'Private Boutique Banner'


class privateBoutiqueRunningCards(models.Model):
	cardImage = models.ImageField(upload_to='images/documents', null=True, blank=True, validators=[FileExtensionValidator(['jpg', 'png', 'jpeg'])])
	cardImage_alt_tag = models.CharField(max_length=1000, null=True, blank=True)
	content = models.TextField(null=True, blank=True)

	author = models.CharField(max_length=100, null=True, blank=True)
	publish = models.DateTimeField(default=timezone.now)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now_add=True)
	status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
	

	def __str__(self):
		return '--Name not provided'

	class Meta:
			verbose_name_plural = 'Private Boutique Running Cards'


class privateBoutiqueInvestingProcessImage(models.Model):
	image = models.ImageField(upload_to='images/documents', null=True, blank=True, validators=[FileExtensionValidator(['jpg', 'png', 'jpeg'])])
	image_alt_tag = models.CharField(max_length=1000, null=True, blank=True)

	author = models.CharField(max_length=100, null=True, blank=True)
	publish = models.DateTimeField(default=timezone.now)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now_add=True)
	status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
	

	def __str__(self):
		return '--Name not provided'

	class Meta:
			verbose_name_plural = 'Private Boutique Investing Process Image'



class privateBoutiqueInvestingProcessCards(models.Model):
	image = models.ImageField(upload_to='images/documents', null=True, blank=True, validators=[FileExtensionValidator(['jpg', 'png', 'jpeg'])])
	imageOnHover = models.ImageField(upload_to='images/documents', null=True, blank=True, validators=[FileExtensionValidator(['jpg', 'png', 'jpeg'])])
	cardContent = models.TextField(null=True, blank=True)
	image_alt_tag = models.CharField(max_length=1000, null=True, blank=True)
	imageOnHover_alt_tag = models.CharField(max_length=1000, null=True, blank=True)

	author = models.CharField(max_length=100, null=True, blank=True)
	publish = models.DateTimeField(default=timezone.now)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now_add=True)
	status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
	

	def __str__(self):
		return '--Name not provided'

	class Meta:
			verbose_name_plural = 'Private Boutique Investing Process Cards'


class privateBoutiqueSellingProcessImage(models.Model):
	image = models.ImageField(upload_to='images/documents', null=True, blank=True, validators=[FileExtensionValidator(['jpg', 'png', 'jpeg'])])
	image_alt_tag = models.CharField(max_length=1000, null=True, blank=True)

	author = models.CharField(max_length=100, null=True, blank=True)
	publish = models.DateTimeField(default=timezone.now)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now_add=True)
	status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
	

	def __str__(self):
		return '--Name not provided'

	class Meta:
			verbose_name_plural = 'Private Boutique Selling Process Image'

class privateBoutiqueSellingProcessCards(models.Model):
	image = models.ImageField(upload_to='images/documents', null=True, blank=True, validators=[FileExtensionValidator(['jpg', 'png', 'jpeg'])])
	imageOnHover = models.ImageField(upload_to='images/documents', null=True, blank=True, validators=[FileExtensionValidator(['jpg', 'png', 'jpeg'])])
	cardContent = models.TextField(null=True, blank=True)
	image_alt_tag = models.CharField(max_length=1000, null=True, blank=True)
	imageOnHover_alt_tag = models.CharField(max_length=1000, null=True, blank=True)

	author = models.CharField(max_length=100, null=True, blank=True)
	publish = models.DateTimeField(default=timezone.now)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now_add=True)
	status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
	

	def __str__(self):
		return '--Name not provided'

	class Meta:
			verbose_name_plural = 'Private Boutique Selling Process Cards'



class privateBoutiqueWhyToInvestCards(models.Model):
	image = models.ImageField(upload_to='images/documents', null=True, blank=True, validators=[FileExtensionValidator(['jpg', 'png', 'jpeg'])])
	image_alt_tag = models.CharField(max_length=1000, null=True, blank=True)
	title = models.CharField(max_length=1000, null=True, blank=True)
	content = models.TextField(null=True, blank=True)
	author = models.CharField(max_length=100, null=True, blank=True)
	publish = models.DateTimeField(default=timezone.now)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now_add=True)
	status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
	

	def __str__(self):
		return '--Name not provided'

	class Meta:
			verbose_name_plural = 'Private Boutique Why To Invest Cards'

class privateBoutiqueWhyToInvestContent(models.Model):
	excerptContent = models.TextField(null=True, blank=True)
	author = models.CharField(max_length=100, null=True, blank=True)
	publish = models.DateTimeField(default=timezone.now)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now_add=True)
	status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
	
	def __str__(self):
		return '--Name not provided'

	class Meta:
			verbose_name_plural = 'Private Boutique Why To Invest Content'


class privateBoutiqueFAQInvestment(models.Model):
	question = models.CharField(max_length=1000, null=True, blank=True)
	answer = models.TextField(null=True, blank=True)
	author = models.CharField(max_length=100, null=True, blank=True)
	publish = models.DateTimeField(default=timezone.now)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now_add=True)
	status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
	
	def __str__(self):
		return '--Name not provided'

	class Meta:
			verbose_name_plural = 'Private Boutique FAQs Investment'


class privateBoutiqueFAQTaxImplications(models.Model):
	question = models.CharField(max_length=1000, null=True, blank=True)
	answer = models.TextField(null=True, blank=True)

	author = models.CharField(max_length=100, null=True, blank=True)
	publish = models.DateTimeField(default=timezone.now)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now_add=True)
	status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
	
	def __str__(self):
		return '--Name not provided'

	class Meta:
			verbose_name_plural = 'Private Boutique FAQs Tax Implications'


class privateBoutiqueDM(models.Model):
	metaTitle = models.CharField(max_length=1000, null=True, blank=True)
	metaDescription = models.CharField(max_length=1000, null=True, blank=True)
	metaTags = models.CharField(max_length=1000, null=True, blank=True)
	metaFeaturedImage = models.ImageField(upload_to='images/documents', null=True, blank=True, validators=[FileExtensionValidator(['jpg','png','jpeg'])])
	metaKeywords = models.CharField(max_length=1000, null=True, blank=True)
	author = models.CharField(max_length=100, null=True, blank=True)
	publish = models.DateTimeField(default=timezone.now)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now_add=True)
	status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

	def __str__(self):
		return self.metaTitle or '--Name not provided' 

	class Meta:
		verbose_name_plural = 'Private Boutique DM'
class privateBoutiqueContactUsBanner(models.Model):
	bannerImage = models.ImageField(upload_to='images/documents', null=True, blank=True, validators=[FileExtensionValidator(['jpg','png','jpeg'])])
	bannerImage_alt_tag = models.CharField(max_length=1000, null=True, blank=True)
	author = models.CharField(max_length=100, null=True, blank=True)
	publish = models.DateTimeField(default=timezone.now)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now_add=True)
	status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

	def __str__(self):
		return "--Name not Provided"
	class Meta:
		verbose_name_plural = 'Private Boutique Contact Us Banner'


class privateBoutiqueContactUsKnowMore(models.Model):
	title = models.CharField(max_length=1000, null=True, blank=True)
	excerptContent = models.TextField(null=True, blank=True)
	author = models.CharField(max_length=100, null=True, blank=True)
	publish = models.DateTimeField(default=timezone.now)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now_add=True)
	status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

	def __str__(self):
		return "--Name not Provided"
	class Meta:
		verbose_name_plural = 'Private Boutique Contact Us Know More'



class privateBoutiqueContactUsKnowMoreFAQs(models.Model):
	heading = models.CharField(max_length=1000, null=True, blank=True)
	content = models.TextField(null=True, blank=True)
	author = models.CharField(max_length=100, null=True, blank=True)
	publish = models.DateTimeField(default=timezone.now)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now_add=True)
	status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

	def __str__(self):
		return "--Name not Provided"
	class Meta:
		verbose_name_plural = 'Private Boutique Contact Us Know More FAQs'


class privateBoutiqueContactUs(models.Model):
	contactPerson = models.CharField(max_length=1000, null=True, blank=True)
	email = models.EmailField(max_length=1000,null=True, blank=True)
	mobile = models.BigIntegerField(null=True, blank=True)
	countryCode = models.ForeignKey(country, on_delete=models.CASCADE, null=True, blank=True)
	state = models.ForeignKey(state, on_delete=models.CASCADE, null=True, blank=True)
	city = models.ForeignKey(city, on_delete=models.CASCADE, null=True, blank=True)

	author = models.CharField(max_length=100, null=True, blank=True)
	publish = models.DateTimeField(default=timezone.now)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now_add=True)
	status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

	def __str__(self):
		return self.contactPerson or "--Name not Provided"
	class Meta:
		verbose_name_plural = 'Private Boutique Contact Us Form'


class privateBoutiqueContactDM(models.Model):
	metaTitle = models.CharField(max_length=1000, null=True, blank=True)
	metaDescription = models.CharField(max_length=1000, null=True, blank=True)
	metaTags = models.CharField(max_length=1000, null=True, blank=True)
	metaFeaturedImage = models.ImageField(upload_to='images/documents', null=True, blank=True, validators=[FileExtensionValidator(['jpg','png','jpeg'])])
	metaKeywords = models.CharField(max_length=1000, null=True, blank=True)
	author = models.CharField(max_length=100, null=True, blank=True)
	publish = models.DateTimeField(default=timezone.now)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now_add=True)
	status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

	def __str__(self):
		return self.metaTitle or '--Name not provided' 

	class Meta:
		verbose_name_plural = 'Private Boutique Contact DM'


class privateBoutiqueCategory(models.Model):
	categoryName = models.CharField(max_length=100, null=True, blank=True)
	category = models.OneToOneField('stockApp.categoryOptions', on_delete=models.CASCADE, null=True, blank=True)	
	publish = models.DateTimeField(default=timezone.now)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

	def __str__(self):
		return self.categoryName or '--Name not provided'

	class Meta:
		verbose_name_plural = 'Private Boutique Categories'


class privateBoutiqueSuccessStories(models.Model):
	stockName = models.OneToOneField(stockBasicDetail, on_delete=models.CASCADE, related_name='stockNamePBSS', null=True, blank=True)
	stockLogo = models.ImageField(upload_to='images/documents', null=True, blank=True, validators=[FileExtensionValidator(['jpg','png','jpeg'])])
	stockLogo_alt_tag = models.CharField(max_length=100, null=True, blank=True)
	investmentPrice = models.DecimalField(max_digits=1000, decimal_places=2, null=True, blank=True)
	listingPrice = models.DecimalField(max_digits=1000, decimal_places=2, null=True, blank=True)
	ipoBandPrice = models.DecimalField(max_digits=1000, decimal_places=2, null=True, blank=True)
	presentPrice = models.DecimalField(max_digits=1000, decimal_places=2, null=True, blank=True, help_text='This will be visible only if we are not able to fetch Price from Screener or Planify Marketplace')
	publish = models.DateTimeField(default=timezone.now)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

	
	def get_current_price(self):
		currentPrice = 0
		try:
			if self.stockName:
				if self.stockName.stockProfileNameSE.screenerLink:
					currentPrice = getScreenerPriceForStockByUrl(self.stockName.stockProfileNameSE.screenerLink)
				elif self.stockName.stockNameBPISL.investorPrice:
					currentPrice = self.stockName.stockNameBPISL.investorPrice
			elif self.presentPrice:
				currentPrice = self.presentPrice
		except:
			pass
		return currentPrice

	def get_current_logo(self):
		currentLogo = 'https://planify-main.s3.amazonaws.com/static/stocks/imgs/planify-logo.png'
		if self.stockName:
			if self.stockName.logo:
				currentLogo = self.stockName.logo.url
		elif self.stockLogo:
			currentLogo = self.stockLogo.url
		return currentLogo

	def __str__(self):
		return str(self.stockName) or '--Name not provided'

	class Meta:
		verbose_name_plural = 'Private Boutique Success Stories'



# 
class sellYourStartupBanner(models.Model):
	title = models.CharField(max_length=1000, null=True, blank=True)
	content = models.TextField(null=True, blank=True)
	button_ActionUrl = models.URLField(null=True, blank=True)
	image = models.ImageField(upload_to='images/documents', null=True, blank=True, validators=[FileExtensionValidator(['jpg','png','jpeg'])])
	image_alt_tag = models.CharField(max_length=1000, null=True, blank=True)	
	author = models.CharField(max_length=1000, null=True, blank=True)
	publish = models.DateTimeField(default=timezone.now)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now_add=True)
	status = models.CharField(max_length=1000, choices=STATUS_CHOICES, default='draft')
	

	def __str__(self):
		return self.title or '--Name not provided'

	class Meta:
			verbose_name_plural = 'sellYourStartup Banner'


class sellYourStartupExposure(models.Model):
	icon = models.ImageField(upload_to='images/documents', null=True, blank=True, validators=[FileExtensionValidator(['jpg','png','jpeg'])])
	icon_alt_tag = models.CharField(max_length=1000, null=True, blank=True)
	titleOnHover = models.TextField(null=True, blank=True)
	content = models.TextField(null=True, blank=True)
	buttonOnHover_ActionUrl = models.URLField(null=True, blank=True)
	author = models.CharField(max_length=1000, null=True, blank=True)
	publish = models.DateTimeField(default=timezone.now)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now_add=True)
	status = models.CharField(max_length=1000, choices=STATUS_CHOICES, default='draft')
	

	def __str__(self):
		return '--Name not provided'

	class Meta:
			verbose_name_plural = 'Sell Your Startup Exposure'


class sellYourStartupUnparalleledExposure(models.Model):
	excerptContent = models.TextField(null=True, blank=True)
	image = models.ImageField(upload_to='images/documents', null=True, blank=True, validators=[FileExtensionValidator(['jpg','png','jpeg'])])
	image_alt_tag = models.CharField(max_length=1000, null=True, blank=True)
	author = models.CharField(max_length=1000, null=True, blank=True)
	publish = models.DateTimeField(default=timezone.now)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now_add=True)
	status = models.CharField(max_length=100, choices=STATUS_CHOICES, default='draft')


	def __str__(self):
		return '--Name not provided'

	class Meta:
		verbose_name_plural = 'Sell Your Startup Unparalleled Exposure'


class sellYourStartupBusinessList(models.Model):
	image = models.ImageField(upload_to='images/documents', null=True, blank=True, validators=[FileExtensionValidator(['jpg','png','jpeg'])])
	image_alt_tag = models.CharField(max_length=1000, null=True, blank=True)
	excerptContent = models.TextField(null=True, blank=True)
	button_ActionUrl = models.URLField(null=True, blank=True)
	author = models.CharField(max_length=1000, null=True, blank=True)
	publish = models.DateTimeField(default=timezone.now)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now_add=True)
	status = models.CharField(max_length=1000, choices=STATUS_CHOICES, default='draft')


	def __str__(self):
		return '--Name not provided'

	class Meta:
		verbose_name_plural = 'Sell Your Startup Business List'



class sellYourStartupBusinessWorth(models.Model):
	excerptContent = models.TextField(null=True, blank=True)
	button_ActionUrl = models.URLField(null=True, blank=True)
	image = models.ImageField(upload_to='images/documents', null=True, blank=True, validators=[FileExtensionValidator(['jpg','png','jpeg'])])
	image_alt_tag = models.CharField(max_length=1000, null=True, blank=True)
	author = models.CharField(max_length=1000, null=True, blank=True)
	publish = models.DateTimeField(default=timezone.now)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now_add=True)
	status = models.CharField(max_length=1000, choices=STATUS_CHOICES, default='draft')


	def __str__(self):
		return '--Name not provided'

	class Meta:
		verbose_name_plural = 'Sell Your Startup Business Worth'


class sellYourStartupFAQMain(models.Model):
	excerptContent = models.TextField(null=True, blank=True)
	author = models.CharField(max_length=1000, null=True, blank=True)
	publish = models.DateTimeField(default=timezone.now)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now_add=True)
	status = models.CharField(max_length=100, choices=STATUS_CHOICES, default='regular')

	def __str__(self):
		return '--Name not provided'

	class Meta:
		verbose_name_plural = 'Sell Your Startup FAQ Main'


class sellYourStartupFAQs(models.Model):
	faqMain = models.ForeignKey('sellYourStartupFAQMain', on_delete=models.SET_NULL, related_name='sellYourStartupSYSF', null=True, blank=True)
	questions = models.CharField(max_length=1000, null=True, blank=True)
	answers = models.TextField(null=True, blank=True)
	author = models.CharField(max_length=1000, null=True, blank=True)
	publish = models.DateTimeField(default=timezone.now)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now_add=True)
	status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

	def __str__(self):
		return '--Name not provided' 

	class Meta:
		verbose_name_plural = 'Sell Your Startup FAQs'

class sellYourStartupDM(models.Model):
	metaTitle = models.CharField(max_length=1000, null=True, blank=True)
	metaDescription = models.CharField(max_length=1000, null=True, blank=True)
	metaTags = models.CharField(max_length=1000, null=True, blank=True)
	metaFeaturedImage = models.ImageField(upload_to='images/documents', null=True, blank=True, validators=[FileExtensionValidator(['jpg','png','jpeg'])])
	metaKeywords = models.CharField(max_length=1000, null=True, blank=True)
	author = models.CharField(max_length=100, null=True, blank=True)
	publish = models.DateTimeField(default=timezone.now)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now_add=True)
	status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

	def __str__(self):
		return self.metaTitle or '--Name not provided' 

	class Meta:
		verbose_name_plural = 'Sell Your Startup DM'

class sellYourStartupContactDM(models.Model):
	metaTitle = models.CharField(max_length=1000, null=True, blank=True)
	metaDescription = models.CharField(max_length=1000, null=True, blank=True)
	metaTags = models.CharField(max_length=1000, null=True, blank=True)
	metaFeaturedImage = models.ImageField(upload_to='images/documents', null=True, blank=True, validators=[FileExtensionValidator(['jpg','png','jpeg'])])
	metaKeywords = models.CharField(max_length=1000, null=True, blank=True)
	author = models.CharField(max_length=100, null=True, blank=True)
	publish = models.DateTimeField(default=timezone.now)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now_add=True)
	status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

	def __str__(self):
		return self.metaTitle or '--Name not provided' 

	class Meta:
		verbose_name_plural = 'Sell Your Startup Contact DM'

class sellYourStartupContactUsBanner(models.Model):
	bannerImage = models.ImageField(upload_to='images/documents', null=True, blank=True, validators=[FileExtensionValidator(['jpg','png','jpeg'])])
	bannerImage_alt_tag = models.CharField(max_length=1000, null=True, blank=True)
	author = models.CharField(max_length=100, null=True, blank=True)
	publish = models.DateTimeField(default=timezone.now)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now_add=True)
	status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

	def __str__(self):
		return "--Name not Provided"
	class Meta:
		verbose_name_plural = 'sell Your Startup Contact Us Banner'

class sellYourStartupContactUsKnowMore(models.Model):
	title = models.CharField(max_length=1000, null=True, blank=True)
	excerptContent = models.TextField(null=True, blank=True)
	author = models.CharField(max_length=100, null=True, blank=True)
	publish = models.DateTimeField(default=timezone.now)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now_add=True)
	status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

	def __str__(self):
		return "--Name not Provided"
	class Meta:
		verbose_name_plural = 'sell Your Startup Contact Us Know More'

class sellYourStartupContactUsKnowMoreFAQs(models.Model):
	heading = models.CharField(max_length=1000, null=True, blank=True)
	content = models.TextField(null=True, blank=True)
	author = models.CharField(max_length=100, null=True, blank=True)
	publish = models.DateTimeField(default=timezone.now)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now_add=True)
	status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

	def __str__(self):
		return "--Name not Provided"
	class Meta:
		verbose_name_plural = 'sell Your Startup Contact Us Know More FAQs'

class sellYourStartupContactUs(models.Model):
	contactPerson = models.CharField(max_length=1000, null=True, blank=True)
	email = models.EmailField(max_length=1000,null=True, blank=True)
	mobile = models.BigIntegerField(null=True, blank=True)
	city = models.ForeignKey(city, on_delete=models.CASCADE, null=True, blank=True)
	nameOfOrganization = models.CharField(max_length=1000,null=True, blank=True)
	presentRole = models.CharField(max_length=1000, null=True, blank=True)
	annualTurnover = models.BigIntegerField(null=True, blank=True)
	author = models.CharField(max_length=100, null=True, blank=True)
	publish = models.DateTimeField(default=timezone.now)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now_add=True)
	status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

	def __str__(self):
		return self.contactPerson or "--Name not Provided"
	class Meta:
		verbose_name_plural = 'Sell Your Startup Contact Us Form'

class seedFundingPackages(models.Model):
	duration = models.CharField(max_length=10, choices=DURATION_CHOICES, default='one_off') 
	pitchDeckImage = models.ImageField(upload_to='images/documents', null=True, blank=True, validators=[FileExtensionValidator(['jpg', 'png', 'jpeg'])])
	pitchDeckImage_alt_tag = models.CharField(max_length=256, null=True, blank=True)
	pitchDeckTitle = models.CharField(max_length=1000,null=True, blank=True)
	pitchDeckAmount = models.BigIntegerField(null=True, blank=True)

	investmentDeckImage = models.ImageField(upload_to='images/documents', null=True, blank=True, validators=[FileExtensionValidator(['jpg', 'png', 'jpeg'])])
	investmentDeckImage_alt_tag = models.CharField(max_length=256, null=True, blank=True)
	investmentDeckTitle = models.CharField(max_length=1000,null=True, blank=True)
	investmentDeckAmount = models.BigIntegerField(null=True, blank=True)

	equityResearchReportImage = models.ImageField(upload_to='images/documents', null=True, blank=True, validators=[FileExtensionValidator(['jpg', 'png', 'jpeg'])])
	equityResearchReportImage_alt_tag = models.CharField(max_length=256, null=True, blank=True)
	equityResearchReportTitle = models.CharField(max_length=1000,null=True, blank=True)
	equityResearchReportAmount = models.BigIntegerField(null=True, blank=True)

	valuationReportImage = models.ImageField(upload_to='images/documents', null=True, blank=True, validators=[FileExtensionValidator(['jpg', 'png', 'jpeg'])])
	valuationReportImage_alt_tag = models.CharField(max_length=256, null=True, blank=True)
	valuationReportTitle = models.CharField(max_length=1000,null=True, blank=True)
	valuationReportAmount = models.BigIntegerField(null=True, blank=True)

	projectionsImage = models.ImageField(upload_to='images/documents', null=True, blank=True, validators=[FileExtensionValidator(['jpg', 'png', 'jpeg'])])
	projectionsImage_alt_tag = models.CharField(max_length=256, null=True, blank=True)
	projectionsTitle = models.CharField(max_length=1000,null=True, blank=True)
	# projectionsAmount = models.BigIntegerField(null=True, blank=True)

	equityRestructuringImage = models.ImageField(upload_to='images/documents', null=True, blank=True, validators=[FileExtensionValidator(['jpg', 'png', 'jpeg'])])
	equityRestructuringImage_alt_tag = models.CharField(max_length=256, null=True, blank=True)
	equityRestructuringTitle = models.CharField(max_length=1000,null=True, blank=True)
	# equityRestructuringAmount = models.BigIntegerField(null=True, blank=True)

	total = models.BigIntegerField(null=True, blank=True)

	author = models.CharField(max_length=100, null=True, blank=True)
	publish = models.DateTimeField(default=timezone.now)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now_add=True)
	status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')


	def __str__(self):
		return '--Name not provided' 
		
	class Meta:
		verbose_name_plural = 'Seed Funding Packages'


