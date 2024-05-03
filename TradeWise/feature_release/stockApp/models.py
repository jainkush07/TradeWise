from secrets import choice
from django.db import models
from django.utils import timezone
from django.core.validators import FileExtensionValidator, MinLengthValidator
import re
import datetime
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
import requests
from django.urls import reverse
from bs4 import BeautifulSoup
from django.core.exceptions import ValidationError
from django.contrib import messages
from authApp.models import roles
from django.utils.timezone import now
import os 


alphanumeric = RegexValidator(r'^[0-9a-zA-Z]*$', 'Only alphanumeric characters are allowed.')


SHARE_CHOICES = (
    ('financial_year', 'financial_year'),
    ('convertible_equity', 'convertible_equity'),
)




STATUS_CHOICES = (
    ('draft', 'Draft'),
    ('published', 'Published'),
)

DATA_IN = (
    ('K', 'K'),
    ('L', 'L'),
    ('Cr', 'Cr'),
    ('M', 'M'),
)

BEN_OR_DCF = (
    ("Ben Graham Value", "Ben Graham's Value"),
    ("DCF", "DCF")
)

NEWS_TYPE = (
    ('Articles-Only', 'Articles Only'),
    ('Articles-Videos', 'Articles & Videos'),
    ('Videos-Only', 'Videos Only'),
)

ICON_CHOICES = (
    (1, 'Increasing'),
    (2, 'Stable'),
    (3, 'Decreasing'),
)

RATING_OPTIONS = (
    (0, 'No Rating'),
    (1, '1'),
    (2, '2'),
    (3, '3'),
    (4, '4'),
    (5, '5'),
)

GENDER_CHOICES = (
    ('male', 'Male'),
    ('female', 'Female'),
)

VISIBILITY_CHOICES = (
    ('visible', 'visible'),
    ('hidden', 'hidden'),
)

TTM_CHOICES = (
    ('Quarter', 'Quarter'),
    ('Half Yearly', 'Half Yearly'),
    ('9 Monthly', '9 Monthly'),
    ('Annual', 'Annual'),
)


PRIORITY = (
    ('ShortForm', 'ShortForm'),
    ('FullForm', 'FullForm'),
)


SHARE_DEMATERIALISED = (
    ('Yes', 'Yes'),
    ('No', 'No'),
)

PLANIFY_CERTIFIED = (
    ('Yes', 'Yes'),
    ('No', 'No'),
)

TYPE_OF_SHARES = (
    ('Equity','Equity'),
    ('CCPS', 'CCPS'),
    ('CCD', 'CCD'),
    ('NCD', 'NCD'),
    ('CSOP', 'CSOP'),
)

STATUS_COMPLETE = (
    ('Completed','Completed'),
    ('Not Completed', 'Not Completed'),
)

IS_LAUNCHING_SOON =(
    ('Yes', 'Yes'),
    ('No', 'No'),
)

LAUNCHING_SOON_TYPE = (
    ('Prebook','Prebook'),
    ('Waitlist','Waitlist'),
)

YEAR_CHOICES = [(r,r) for r in range(1800, datetime.date.today().year+2)]

CURRENT_YEAR = datetime.datetime.now().year


class loginReminderPopup(models.Model):
    titleOne = models.CharField(max_length=1000, null=True, blank=True)
    contentOne = models.CharField(max_length=1000, null=True, blank=True)
    titleOneImg = models.ImageField(upload_to='login/images', null=True, blank=True)
    titleOneImg_AltTag = models.CharField(max_length=100, null=True, blank=True)


    titleTwo = models.CharField(max_length=1000, null=True, blank=True)
    contentTwo = models.CharField(max_length=1000, null=True, blank=True)
    titleTwoImg = models.ImageField(upload_to='login/images', null=True, blank=True)
    titleTwoImg_AltTag = models.CharField(max_length=100, null=True, blank=True)

    titleThree = models.CharField(max_length=1000, null=True, blank=True)
    contentThree = models.CharField(max_length=1000, null=True, blank=True)
    titleThreeImg = models.ImageField(upload_to='login/images', null=True, blank=True)
    titleThreeImg_AltTag = models.CharField(max_length=100, null=True, blank=True)

    titleFour = models.CharField(max_length=1000, null=True, blank=True)
    contentFour = models.CharField(max_length=1000, null=True, blank=True)
    titleFourImg = models.ImageField(upload_to='login/images', null=True, blank=True)
    titleFourImg_AltTag = models.CharField(max_length=100, null=True, blank=True)

    titleFive = models.CharField(max_length=1000, null=True, blank=True)
    contentFive = models.CharField(max_length=1000, null=True, blank=True)
    titleFiveImg = models.ImageField(upload_to='login/images', null=True, blank=True)
    titleFiveImg_AltTag = models.CharField(max_length=100, null=True, blank=True)

    titleSix = models.CharField(max_length=1000, null=True, blank=True)
    contentSix = models.CharField(max_length=1000, null=True, blank=True)
    titleSixImg = models.ImageField(upload_to='login/images', null=True, blank=True)
    titleSixImg_AltTag = models.CharField(max_length=100, null=True, blank=True)

    bannerImg = models.ImageField(upload_to='login/images', null=True, blank=True)
    bannerImg_AltTag = models.CharField(max_length=100, null=True, blank=True)

    videoID = models.CharField(max_length=1000, null=True, blank=True)
    videoTitle = models.CharField(max_length=1000, null=True, blank=True)
    videoContent = models.CharField(max_length=1000, null=True, blank=True)
    
    author = models.CharField(max_length=1000, null=True, blank=True)
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

    def __str__(self):
        return '--Login Reminder Popup--'

    class Meta:
        verbose_name_plural = 'Login Reminder Popup Data'



class welcomeLoginPopup(models.Model):
    # relatedTo = models.OneToOneField(roles, on_delete=models.CASCADE, related_name='letsBeginPP')
    heading = models.CharField(max_length=1000, null=True, blank=True)
    letsBeginImage = models.ImageField(upload_to='stock/images/logo', null=True, blank=True)
    letsBeginContent = models.TextField(null=True, blank=True)
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=VISIBILITY_CHOICES, default='visible')

    class Meta:
        verbose_name_plural = 'Lets begin Popup Content'

    def __str__(self):
        return '--Name not provided--'


class fundingDetailsVisibility(models.Model):
    stockProfileName = models.OneToOneField('stockBasicDetail', on_delete=models.CASCADE, related_name='stockProfileNameFDVI')
    fundedBy = models.CharField(max_length=10, choices=VISIBILITY_CHOICES, default='visible')
    fundingAmount = models.CharField(max_length=10, choices=VISIBILITY_CHOICES, default='visible')
    dateOfInvestment = models.CharField(max_length=10, choices=VISIBILITY_CHOICES, default='visible')
    fundingRound = models.CharField(max_length=10, choices=VISIBILITY_CHOICES, default='visible')
    fundName = models.CharField(max_length=10, choices=VISIBILITY_CHOICES, default='visible')
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=VISIBILITY_CHOICES, default='visible')

    def __str__(self):
        return '--Name not provided--'

class stockListDM(models.Model):
    metaTitleResearchReportListing = models.CharField(max_length=1000,null=True, blank=True)
    metaDescriptionResearchReportListing = models.TextField(null=True, blank=True)
    metaKeywordsResearchReportListing = models.TextField(null=True, blank=True)
    tagsResearchReportListing = models.CharField(max_length=1000, null=True, blank=True)
    metaFeaturedImage = models.ImageField(upload_to='stock/images/featured', null=True, blank=True)
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=VISIBILITY_CHOICES, default='visible')

    class Meta:
        verbose_name_plural = 'Stock Listing DM Information'

    def __str__(self):
        return self.metaTitleResearchReportListing or '--Name not provided--'


class stockAppSpecific(models.Model):
    schema = models.TextField(null=True, blank=True)
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

    class Meta:
        verbose_name_plural = 'For Analyst - Stock App Specific Data'


class currentRateOfbondYield(models.Model):
    value = models.DecimalField(max_digits=1000, decimal_places=2, null=True, blank=True)
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

    def __str__(self):
        return str(self.value) or '--Name not provided--'

    class Meta:
        verbose_name_plural = 'For Analyst - Current Rate of Bond Yield'

class stockListHeading(models.Model):
    headingForstocklisting = models.CharField(max_length=70, null=True, blank=True)
    contentForstocklisting = models.TextField(null=True, blank=True)
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

    def __str__(self):
        return str(self.value) or '--Name not provided--'

    class Meta:
        verbose_name_plural = 'headingforstocklist' 


class stockTransferDepositoryOptions(models.Model):
    name = models.CharField(max_length=1000)
    analyst = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='analystSTDO', null=True, blank=True)
    verifiedBy = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='verifiedBySTDO', null=True, blank=True)
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

    def __str__(self):
        return self.name or '--Name not provided--'

    class Meta:
        verbose_name_plural = 'For Analyst - Stock Basic Details Depository' 


class saleTypeOptions(models.Model):
    name = models.CharField(max_length=1000)
    analyst = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='analystSTO', null=True, blank=True)
    verifiedBy = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='verifiedBySTO', null=True, blank=True)
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

    def __str__(self):
        return self.name or '--Name not provided--'

    class Meta:
        verbose_name_plural = 'For Analyst - Stock Basic Details Investment'




class keyratioUrlsForSitemap(models.Model):
    stockProfileName = models.OneToOneField('stockBasicDetail', on_delete=models.CASCADE, related_name='stockProfileNameKRUrl')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

    def get_absolute_url(self):
        return reverse('stockApp:keyRatioURL', args=[self.stockProfileName.slug])

    class Meta:
        verbose_name_plural = 'DO NOT TOUCH- FOR SITEMAP-KEYRATIO'


class peersUrlsForSitemap(models.Model):
    stockProfileName = models.OneToOneField('stockBasicDetail', on_delete=models.CASCADE, related_name='stockProfileNamePeersUrl')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

    def get_absolute_url(self):
        return reverse('stockApp:peersURL', args=[self.stockProfileName.slug])

    class Meta:
        verbose_name_plural = 'DO NOT TOUCH- FOR SITEMAP-PEERS'


class financialUrlsForSitemap(models.Model):
    stockProfileName = models.OneToOneField('stockBasicDetail', on_delete=models.CASCADE, related_name='stockProfileNameFinancialUrl')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

    def get_absolute_url(self):
        return reverse('stockApp:financialURL', args=[self.stockProfileName.slug])

    class Meta:
        verbose_name_plural = 'DO NOT TOUCH- FOR SITEMAP-FINANCIAL'


class ownershipUrlsForSitemap(models.Model):
    stockProfileName = models.OneToOneField('stockBasicDetail', on_delete=models.CASCADE, related_name='stockProfileNameOwnershipUrl')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

    def get_absolute_url(self):
        return reverse('stockApp:ownershipURL', args=[self.stockProfileName.slug])

    class Meta:
        verbose_name_plural = 'DO NOT TOUCH- FOR SITEMAP-OWNERSHIP'


class newsUrlsForSitemap(models.Model):
    stockProfileName = models.OneToOneField('stockBasicDetail', on_delete=models.CASCADE, related_name='stockProfileNameNewsUrl')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

    def get_absolute_url(self):
        return reverse('stockApp:newsURL', args=[self.stockProfileName.slug])

    class Meta:
        verbose_name_plural = 'DO NOT TOUCH- FOR SITEMAP-NEWS'


class eventsUrlsForSitemap(models.Model):
    stockProfileName = models.OneToOneField('stockBasicDetail', on_delete=models.CASCADE, related_name='stockProfileNameEventsUrl')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

    def get_absolute_url(self):
        return reverse('stockApp:eventsURL', args=[self.stockProfileName.slug])

    class Meta:
        verbose_name_plural = 'DO NOT TOUCH- FOR SITEMAP-EVENTS'

class startupCategoryOptions(models.Model):
    categoryName = models.CharField(max_length=100, null=True, blank=True)
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

    def __str__(self):
        return self.categoryName or '--Name not provided--'

    class Meta:
        verbose_name_plural = 'Startups Category Options'


class stockBasicDetail(models.Model):
    Account_Choice_For_Fund = (
        ('Planify Enterprise', 'Planify Enterprise'),
        ('Planify Capital', 'Planify Capital'),
    )
    stockName = models.CharField(max_length=1000)
    logo = models.ImageField(upload_to='stock/images/logo', null=True, blank=True)
    logoAlt = models.CharField(max_length=256, null=True, blank=True)
    seoTitle = models.CharField(max_length=256, null=True, blank=True)
    slug = models.SlugField(max_length=256, unique=True, null=True, blank=True)
    analyst = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='analystSBD', null=True, blank=True)
    verifiedBy = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='verifiedBySBD', null=True, blank=True)
    showOnPrivateBoutique = models.BooleanField(default=False)
    showOnHomePage = models.BooleanField(default=False)
    showOnPitchPage = models.BooleanField(default=False)
    content = models.TextField(null=True, blank=True)
    headingForStartup = models.CharField(max_length=70, null=True, blank=True)
    # startupCategory = models.ForeignKey(startupCategoryOptions, on_delete=models.SET_NULL, related_name='startupCategorySC', null=True, blank=True)
    bgImageForStartup = models.ImageField(upload_to='stock/images/logo', null=True, blank=True)
    bgImageForStartupAlt = models.CharField(max_length=256, null=True, blank=True)
    ticker = models.CharField(max_length=15, validators=[MinLengthValidator(2)])
    ROFRRequired = models.BooleanField(null=True, blank=True)
    stockTransferDepository = models.ManyToManyField(stockTransferDepositoryOptions, related_name='stockTransferDepositorySBD',blank=True)
    saleType = models.ManyToManyField(saleTypeOptions, related_name='saleTypeSBD',blank=True)
    shareDematerialized = models.CharField(max_length=100, choices=SHARE_DEMATERIALISED, null=True, blank=True)
    isLaunchSoon = models.CharField(max_length=100, choices=IS_LAUNCHING_SOON, default='No')
    launching_Soon_Type = models.CharField(max_length=100, choices=LAUNCHING_SOON_TYPE, null=True, blank=True)
    type_Of_Shares = models.CharField(max_length=100, choices=TYPE_OF_SHARES, null=True, blank=True)
    amount_To_Raise = models.BigIntegerField(null=True, blank=True, default=0)
    get_funds_in = models.CharField(max_length=256, choices=Account_Choice_For_Fund, default='Planify Capital', null=True, blank=True)
    launch_Date = models.DateField(null=True, blank=True)
    end_Date = models.DateField(null=True, blank=True)
    jump_Start = models.BigIntegerField(null=True, blank=True, default=0)
    min_invest = models.IntegerField(null=True, blank=True)
    investment_Raised = models.BigIntegerField(null=True, blank=True, default=0)
    isStatusComp = models.CharField(max_length=100, choices=STATUS_COMPLETE, default='Not Completed')
    planifyCertified = models.CharField(max_length=100, choices=PLANIFY_CERTIFIED, null=True, blank=True)
    investRaisedPercent = models.DecimalField(max_digits=100, decimal_places=2, null=True, blank=True)
    daysLeft = models.BigIntegerField(null=True, blank=True)
    # totalDividend = models.DecimalField(max_digits=1000, decimal_places=50, null=True, blank=True)
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

    @property
    def days_left(self):
        if self.end_Date:
            return (self.end_Date - now().date()).days+1

    def save(self):
        if self.investment_Raised and self.amount_To_Raise:
            try:
                self.investRaisedPercent = (self.investment_Raised/self.amount_To_Raise)*100
            except:
                pass

        if self.end_Date and self.launch_Date:
            delta = self.end_Date - self.launch_Date
            self.daysLeft = delta.days
        super(stockBasicDetail, self).save()

    def __str__(self):
        return self.stockName or '--Name not provided--'

    def get_absolute_url(self):
        return reverse('stockApp:snapshotURL', args=[self.slug])
    
    class Meta:
        verbose_name_plural = 'Stock Basic Details - Profile'

#
class benGrahamOrDCF(models.Model):
    stockProfileName = models.OneToOneField(stockBasicDetail, on_delete=models.CASCADE, related_name='stockProfileNameBGOD')
    intrinsicValueType = models.CharField(max_length=100,choices=BEN_OR_DCF, default="Ben Graham Value")
    DCFValue = models.DecimalField(max_digits=1000, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return 'Stock Name: %s, Intrinsic Type: %s' % (self.stockProfileName.stockName, self.intrinsicValueType) or '--Name not provided--'

    class Meta:
        verbose_name_plural = 'Ben Graham Value Or DCF'

class sectorOptions(models.Model):
    name = models.CharField(max_length=1000)
    analyst = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='analystSO', null=True, blank=True)
    verifiedBy = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='verifiedBySO', null=True, blank=True)
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

    def __str__(self):
        return self.name or '--Name not provided--'

    class Meta:
        verbose_name_plural = 'For Analyst - Stock Essentials Sector'


class subSectorOptions(models.Model):
    name = models.CharField(max_length=1000)
    analyst = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='analystSSO', null=True, blank=True)
    verifiedBy = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='verifiedBySSO', null=True, blank=True)
    sector = models.ForeignKey(sectorOptions, on_delete=models.SET_NULL, related_name='sectorSSO', null=True, blank=True)
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

    def __str__(self):
        return self.name or '--Name not provided--'

    class Meta:
        verbose_name_plural = 'For Analyst - Stock Essentials Sub-Sector'

class categoryOptions(models.Model):
    name = models.CharField(max_length=1000)
    fetchScreenerPrice = models.BooleanField(default=False)
    shortForm = models.CharField(max_length=1000, null=True, blank=True)
    fullForm = models.CharField(max_length=1000, null=True, blank=True)
    priority = models.CharField(max_length=100, choices=PRIORITY, default='ShortForm')
    analyst = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='analystCaO', null=True, blank=True)
    verifiedBy = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='verifiedByCaO', null=True, blank=True)
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

    def __str__(self):
        return self.name or '--Name not provided--'

    class Meta:
        verbose_name_plural = 'For Analyst - Stock Essentials Category'

class typeOfCompanyOptions(models.Model):
    name = models.CharField(max_length=1000)
    analyst = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='analystTCO', null=True, blank=True)
    verifiedBy = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='verifiedByTCO', null=True, blank=True)
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

    def __str__(self):
        return self.name or '--Name not provided--'

    class Meta:
        verbose_name_plural = 'For Analyst - Stock Essentials Company Type'

class countryOptions(models.Model):
    name = models.CharField(max_length=1000)
    analyst = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='analystCO', null=True, blank=True)
    verifiedBy = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='verifiedByCO', null=True, blank=True)
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

    def __str__(self):
        return self.name or 'India'

    class Meta:
        verbose_name_plural = 'For Analyst - Stock Essentials Country'

class bookValueData(models.Model):
    stockProfileName = models.ForeignKey(stockBasicDetail, on_delete=models.CASCADE, related_name='stockProfileNameBVAnn')
    analyst = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='analystBVAnn', null=True, blank=True)
    verifiedBy = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='verifiedByBVAnn', null=True, blank=True)
    year = models.PositiveIntegerField(choices=YEAR_CHOICES, default=CURRENT_YEAR)
    bookValue = models.DecimalField(max_digits=1000, decimal_places=2, null=True, blank=True)
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

    def __str__(self):
        return 'Stock Name: %s, Year: %s, Value: %s' % (self.stockProfileName.stockName, self.year, self.bookValue) or '--Name not provided--'

    class Meta:
        verbose_name_plural = 'Key Ratio - Book Value Annual Data'


class financialFigureUnits(models.Model):
    stockProfileName = models.OneToOneField(stockBasicDetail, on_delete=models.CASCADE, related_name='stockProfileNameFFU')
    analyst = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='analystFFU', null=True, blank=True)
    verifiedBy = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='verifiedByFFU', null=True, blank=True)
    shareOutstandingNumber = models.CharField(max_length=10, choices=DATA_IN, default='Crores', null=True,blank=True)
    financialNumbers = models.CharField(max_length=10, choices=DATA_IN, default='Crores', null=True,blank=True)
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

    def __str__(self):
        return 'Stock Name: %s' % (self.stockProfileName.stockName) or '--Name not provided--'

    class Meta:
        verbose_name_plural = 'Financial - Data Units(cr/lakh.. etc)'


class stockEssentials(models.Model):
    stockProfileName = models.OneToOneField(stockBasicDetail, on_delete=models.CASCADE, related_name='stockProfileNameSE')
    analyst = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='analystSE', null=True, blank=True)
    verifiedBy = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='verifiedBySE', null=True, blank=True)
    essentialsDescription = models.TextField(null=True, blank=True)
    salesGrowthRateOfXYear = models.DecimalField(max_digits=1000, decimal_places=2, null=True, blank=True)
    ISIN = models.CharField(max_length=50, null=True, blank=True, validators=[alphanumeric])
    faceValue = models.DecimalField(max_digits=1000, decimal_places=2, null=True, blank=True)
    totalShares = models.BigIntegerField(null=True, blank=True)
    sector = models.ForeignKey(sectorOptions, on_delete=models.SET_NULL, null=True, blank=True, related_name='sectorSE')
    subSector = models.ForeignKey(subSectorOptions,blank=True, on_delete=models.SET_NULL,null=True, related_name='subSectorSE')
    category = models.ForeignKey(categoryOptions,blank=True, on_delete=models.SET_NULL,null=True, related_name='categorySE')
    screenerLink = models.URLField(max_length=1000,null=True,blank=True, help_text='Will work only when Category is "Listed".')
    enterpriseValue = models.DecimalField(max_digits=1000, decimal_places=2, null=True, blank=True) #not in use, calculated using formula
    balance_with_RBI = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)
    preference_equity = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)
    typeOfCompany = models.ForeignKey(typeOfCompanyOptions,blank=True, on_delete=models.SET_NULL,null=True, related_name='typeOfCompanySE')
    countryRegisteredIn = models.ForeignKey(countryOptions,blank=True, on_delete=models.SET_NULL,null=True, related_name='countryRegisteredInSE')
    registeredDate  = models.DateField(null=True, blank=True)
    researchLastUpdatedOn = models.DateField(null=True, blank=True)
    listingDate  = models.DateField(null=True, blank=True)
    stockExchangeReferenceSymbol = models.CharField(max_length=1000, null=True, blank=True)
    regOffice = models.CharField(max_length=1000, null=True, blank=True)
    shares_on_offer = models.BigIntegerField(null=True, blank=True)
    equityPercent = models.DecimalField(max_digits=1000, decimal_places=2, null=True, blank=True)
    website = models.URLField(max_length=1000,null=True,blank=True)
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

    @property
    def total_dividend(self):
        sumDividend = 0 
        dividendInst = stockEventsDividend.objects.filter(stockProfileName=self.stockProfileName)
        for item in dividendInst:
            sumDividend+=item.dividendShare
        return sumDividend


    def save(self):
        if self.totalShares and self.shares_on_offer:
            self.equityPercent = (self.shares_on_offer/(self.totalShares+self.shares_on_offer))*100
        super(stockEssentials, self).save()

    def __str__(self):
        return self.stockProfileName.stockName or '--Name not provided--'

    class Meta:
        verbose_name_plural = 'Stock Essentials - Profile'

class managementOptions(models.Model):
    name = models.CharField(max_length=1000)
    analyst = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='analystMO', null=True, blank=True)
    verifiedBy = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='verifiedByMO', null=True, blank=True)
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

    def __str__(self):
        return self.name or '--Name not provided--'

    class Meta:
        verbose_name_plural = 'For Analyst - Stock Investment Checklist Management'


class accountingPracticeOptions(models.Model):
    name = models.CharField(max_length=1000)
    analyst = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='analystAPO', null=True, blank=True)
    verifiedBy = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='verifiedByAPO', null=True, blank=True)
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

    def __str__(self):
        return self.name or '--Name not provided--'

    class Meta:
        verbose_name_plural = 'For Analyst - Stock Investment Checklist Accounting'


class profitabilityOptions(models.Model):
    name = models.CharField(max_length=1000)
    analyst = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='analystPO', null=True, blank=True)
    verifiedBy = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='verifiedByPO', null=True, blank=True)
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

    def __str__(self):
        return self.name or '--Name not provided--'

    class Meta:
        verbose_name_plural = 'For Analyst - Stock Investment Checklist Profitability'


class solvencyOptions(models.Model):
    name = models.CharField(max_length=1000)
    analyst = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='analystSolO', null=True, blank=True)
    verifiedBy = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='verifiedBySolO', null=True, blank=True)
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

    def __str__(self):
        return self.name or '--Name not provided--'

    class Meta:
        verbose_name_plural = 'For Analyst - Stock Investment Checklist Solvency'


class growthOptions(models.Model):
    name = models.CharField(max_length=1000)
    analyst = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='analystGO', null=True, blank=True)
    verifiedBy = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='verifiedByGO', null=True, blank=True)
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

    def __str__(self):
        return self.name or '--Name not provided--'

    class Meta:
        verbose_name_plural = 'For Analyst - Stock Investment Checklist Growth'

class valuationOptions(models.Model):
    name = models.CharField(max_length=1000)
    analyst = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='analystVO', null=True, blank=True)
    verifiedBy = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='verifiedByVO', null=True, blank=True)
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

    def __str__(self):
        return self.name or '--Name not provided--'

    class Meta:
        verbose_name_plural = 'For Analyst - Stock Investment Checklist Valuation'

class businessTypeOptions(models.Model):
    name = models.CharField(max_length=1000)
    analyst = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='analystBTO', null=True, blank=True)
    verifiedBy = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='verifiedByBTO', null=True, blank=True)
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

    def __str__(self):
        return self.name or '--Name not provided--'

    class Meta:
        verbose_name_plural = 'For Analyst - Stock Investment Checklist Business Type'

class recommendationOptions(models.Model):
    name = models.CharField(max_length=1000)
    analyst = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='analystRO', null=True, blank=True)
    verifiedBy = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='verifiedByRO', null=True, blank=True)
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

    def __str__(self):
        return self.name or '--Name not provided--'

    class Meta:
        verbose_name_plural = 'For Analyst - Stock Investment Checklist Recommendation'


class stockInvestmentChecklist(models.Model):
    stockProfileName = models.OneToOneField(stockBasicDetail, on_delete=models.CASCADE, related_name='stockProfileNameSIC')
    analyst = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='analystSIC', null=True, blank=True)
    verifiedBy = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='verifiedBySIC', null=True, blank=True)
    management = models.ForeignKey(managementOptions, on_delete=models.SET_NULL, null=True, blank=True, related_name='managementSIC')
    acountingPratice = models.ForeignKey(accountingPracticeOptions, on_delete=models.SET_NULL, null=True, blank=True, related_name='acountingPraticeSIC')
    profitability = models.ForeignKey(profitabilityOptions, on_delete=models.SET_NULL, null=True, blank=True, related_name='profitabilitySIC')
    solvency = models.ForeignKey(solvencyOptions, on_delete=models.SET_NULL, null=True, blank=True, related_name='solvencySIC')
    growth = models.ForeignKey(growthOptions, on_delete=models.SET_NULL, null=True, blank=True, related_name='growthSIC')
    valuation = models.ForeignKey(valuationOptions, on_delete=models.SET_NULL, null=True, blank=True, related_name='valuationSIC')
    businessType = models.ForeignKey(businessTypeOptions, on_delete=models.SET_NULL, null=True, blank=True, related_name='businessTypeSIC')
    rating = models.PositiveIntegerField(choices=RATING_OPTIONS, null=True, blank=True, default=0)
    recommendation = models.ForeignKey(recommendationOptions, on_delete=models.SET_NULL, null=True, blank=True, related_name='recommendationSIC')
    accumulationRangeDescriptionFrom = models.BigIntegerField(null=True, blank=True)
    accumulationRangeDescriptionTo = models.BigIntegerField(null=True, blank=True)
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

    def __str__(self):
        return self.stockProfileName.stockName or '--Name not provided--'

    class Meta:
        verbose_name_plural = 'Stock Investment Checklist - Profile'


class deck(models.Model):
    stockProfileName = models.ForeignKey(stockBasicDetail, on_delete=models.CASCADE,
                                            related_name='stockProfileNamedeck')
    dec_description = models.TextField(null=True, blank=True)
    dec_ppt = models.FileField(upload_to='stock/images/deck', null=True, blank=True)

    class Meta:
        verbose_name_plural = "deck"

    def __str__(self):
        return str(self.id) or '--Name not provided--'


class deck_images(models.Model):
    deckname = models.ForeignKey(deck, on_delete=models.CASCADE, related_name='deckimages', null=True, blank=True)
    page_description = models.TextField(null=True, blank=True)
    tag = models.TextField(null=True)
    page_image = models.FileField(upload_to='stock/images/image', null=True, blank=True)

    class Meta:
        verbose_name_plural = "deck_images"

    def __str__(self):
        return str(self.deckname.stockProfileName) or '--Name not provided--'


class pitchDocs(models.Model):
    stockProfileName = models.ForeignKey(stockBasicDetail, on_delete=models.CASCADE,
                                            related_name='stockProfileNamedocs')
    doc_description = models.TextField(null=True, blank=True)
    doc_pdf = models.FileField(upload_to='stock/images/docs', null=True, blank=True)

    class Meta:
        verbose_name_plural = "docs"

    def __str__(self):
        return str(self.id) or '--Name not provided--'


class pitchDocs_images(models.Model):
    docname = models.ForeignKey(pitchDocs, on_delete=models.CASCADE, related_name='docimages', null=True, blank=True)
    page_description = models.TextField(null=True, blank=True)
    tag = models.TextField(null=True)
    page_image = models.FileField(upload_to='stock/images/image', null=True, blank=True)

    class Meta:
        verbose_name_plural = "doc_images"

    def __str__(self):
        return str(self.docname.stockProfileName) or '--Name not provided--'


class highLights(models.Model):
    stockProfileName = models.ForeignKey(stockBasicDetail, on_delete=models.CASCADE,
                                            related_name='stockProfileNameHL')
    description = models.TextField(null=True, blank=True)
    icon = models.ImageField(upload_to='stock/images/highLightsicon', null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Highlights'

class pitchupperimage(models.Model):
    stockProfileName = models.ForeignKey(stockBasicDetail, on_delete=models.CASCADE,
                                            related_name='stockProfileNamepitchimages', null=True, blank=True)
    upperimage = models.ImageField(upload_to='stock/images/image', null=True, blank=True)
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

    class Meta:
        verbose_name_plural = 'upperimage'


class stockAdmin(models.Model):
    stockProfileName = models.OneToOneField(stockBasicDetail, on_delete=models.CASCADE, related_name='stockProfileNameSA')
    analyst = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='analystSA', null=True, blank=True)
    verifiedBy = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='verifiedBySA', null=True, blank=True)
    verifiedDetails = models.BooleanField(null=True, blank=True)
    verifiedByAdmin = models.CharField(max_length=1000, null=True, blank=True)
    reportLive = models.BooleanField(null=True, blank=True)
    researchReport = models.BooleanField(null=True, blank=True)
    metaTitle = models.CharField(max_length=1000,null=True, blank=True)
    metaDescription = models.TextField(null=True, blank=True)
    metaKeywords = models.TextField(null=True, blank=True)
    tags = models.CharField(max_length=1000, null=True, blank=True)
    metaTitlekeyRatio = models.CharField(max_length=1000,null=True, blank=True)
    metaDescriptionkeyRatio = models.TextField(null=True, blank=True)
    metaKeywordskeyRatio = models.TextField(null=True, blank=True)
    tagskeyRatio = models.CharField(max_length=1000, null=True, blank=True)
    metaTitlePeers = models.CharField(max_length=1000,null=True, blank=True)
    metaDescriptionPeers = models.TextField(null=True, blank=True)
    metaKeywordsPeers = models.TextField(null=True, blank=True)
    tagsPeers = models.CharField(max_length=1000, null=True, blank=True)
    metaTitleFinancialBalanceSheet = models.CharField(max_length=1000,null=True, blank=True)
    metaDescriptionFinancialBalanceSheet = models.TextField(null=True, blank=True)
    metaKeywordsFinancialBalanceSheet = models.TextField(null=True, blank=True)
    tagsFinancialBalanceSheet = models.CharField(max_length=1000, null=True, blank=True)
    metaTitleFinancialProfitLoss = models.CharField(max_length=1000,null=True, blank=True)
    metaDescriptionFinancialProfitLoss = models.TextField(null=True, blank=True)
    metaKeywordsFinancialProfitLoss = models.TextField(null=True, blank=True)
    tagsFinancialProfitLoss = models.CharField(max_length=1000, null=True, blank=True)
    metaTitleFinancialCashFlow = models.CharField(max_length=1000,null=True, blank=True)
    metaDescriptionFinancialCashFlow = models.TextField(null=True, blank=True)
    metaKeywordsFinancialCashFlow = models.TextField(null=True, blank=True)
    tagsFinancialCashFlow = models.CharField(max_length=1000, null=True, blank=True)
    metaTitleOnwership = models.CharField(max_length=1000,null=True, blank=True)
    metaDescriptionOnwership = models.TextField(null=True, blank=True)
    metaKeywordsOnwership = models.TextField(null=True, blank=True)
    tagsOnwership = models.CharField(max_length=1000, null=True, blank=True)
    metaTitleNews = models.CharField(max_length=1000,null=True, blank=True)
    metaDescriptionNews = models.TextField(null=True, blank=True)
    metaKeywordsNews = models.TextField(null=True, blank=True)
    tagsNews = models.CharField(max_length=1000, null=True, blank=True)
    metaTitleEvents = models.CharField(max_length=1000,null=True, blank=True)
    metaDescriptionEvents = models.TextField(null=True, blank=True)
    metaKeywordsEvents = models.TextField(null=True, blank=True)
    tagsEvents = models.CharField(max_length=1000, null=True, blank=True)
    featuredImage = models.ImageField(upload_to='stock/images/featuredImage', null=True, blank=True)
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

    def __str__(self):
        return self.stockProfileName.stockName or '--Name not provided--'
        # return 'Stock Name: %s, Verified By: %s' % (self.stockProfileName.stockName, self.verifiedBy) or '--Name not provided--'

    class Meta:
        verbose_name_plural = 'Stock Admin - Profile'

class stockIPO(models.Model):
    stockProfileName = models.OneToOneField(stockBasicDetail, on_delete=models.CASCADE, related_name='stockProfileNameSI')
    analyst = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='analystSIPO', null=True, blank=True)
    verifiedBy = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='verifiedBySIPO', null=True, blank=True)
    IPODescription = models.TextField(null=True, blank=True)
    openDate = models.DateField(null=True, blank=True)
    openTime = models.TimeField(null=True, blank=True)
    closedDate = models.DateField(null=True, blank=True)
    closedTime = models.TimeField(null=True, blank=True)
    listingDateBox = models.DateField(null=True, blank=True)
    listingTime = models.TimeField(null=True, blank=True)
    offerForSale = models.DecimalField(max_digits=1000, decimal_places=2, null=True, blank=True)
    freshIssue = models.DecimalField(max_digits=1000, decimal_places=2, null=True, blank=True)
    totalIPOSize = models.DecimalField(max_digits=1000, decimal_places=2, null=True, blank=True)
    offerForSaleNoOfShares = models.DecimalField(max_digits=100, decimal_places=20, null=True, blank=True)
    freshIssueNoOfShares = models.DecimalField(max_digits=100, decimal_places=20, null=True, blank=True)
    totalIpoNoOfShares = models.DecimalField(max_digits=100, decimal_places=20, null=True, blank=True)
    priceBandFrom = models.BigIntegerField(null=True, blank=True)
    priceBandTo = models.BigIntegerField(null=True, blank=True)
    minOrderQuantity = models.PositiveIntegerField(null=True, blank=True)
    greyMarketPremiumFrom = models.BigIntegerField(null=True, blank=True)
    greyMarketPremiumTo = models.BigIntegerField(null=True, blank=True)
    retailSubscription = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)
    retailSubscriptionPercentage = models.DecimalField(max_digits=1000, decimal_places=2, null=True, blank=True)
    QIBSubscription = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)
    QIBSubscriptionPercentage = models.DecimalField(max_digits=1000, decimal_places=2, null=True, blank=True)
    NonInstitutionalSubscription = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)
    NonInstitutionalSubscriptionPercentage = models.DecimalField(max_digits=1000, decimal_places=2, null=True, blank=True)
    employeeQuota = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)
    employeeQuotaPercentage = models.DecimalField(max_digits=1000, decimal_places=2, null=True, blank=True)
    NII = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)
    NIIPercentage = models.DecimalField(max_digits=1000, decimal_places=2, null=True, blank=True)
    specialQuota = models.CharField(max_length=256, null=True, blank=True, default='Special Quota')
    specialQuotaValue = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)
    specialQuotaValuePercentage = models.DecimalField(max_digits=1000, decimal_places=2, null=True, blank=True)
    totalSubscription = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

    def save(self):
        if self.offerForSale:
            offerFrSale = self.offerForSale
        else:
            offerFrSale = 0
        if self.freshIssue:
            frshIssue = self.freshIssue
        else:
            frshIssue = 0
        self.totalIPOSize = offerFrSale + frshIssue
        if self.totalIPOSize:
            try:
                a1 = self.retailSubscription * (self.retailSubscriptionPercentage / 100) * self.totalIPOSize
            except:
                a1 = 0
            try:
                a2 = self.QIBSubscription * (self.QIBSubscriptionPercentage / 100) * self.totalIPOSize
            except:
                a2 = 0
            try:
                a3 = self.NonInstitutionalSubscription * (self.NonInstitutionalSubscriptionPercentage / 100) * self.totalIPOSize
            except:
                a3 = 0
            try:
                a4 = self.employeeQuota * (self.employeeQuotaPercentage / 100) * self.totalIPOSize
            except:
                a4 = 0
            try:
                a5 = self.NII * (self.NIIPercentage / 100) * self.totalIPOSize
            except:
                a5 = 0
            try:
                a6 = self.specialQuotaValue * (self.specialQuotaValuePercentage / 100) * self.totalIPOSize
            except:
                a6 = 0
            self.totalSubscription = (a1 + a2 + a3 + a4 + a5 + a6) / self.totalIPOSize
        super(stockIPO, self).save()

    def __str__(self):
        return self.stockProfileName.stockName or '--Name not provided--'

    class Meta:
        verbose_name_plural = 'Stock IPO - Profile'


class stageOptions(models.Model):
    name = models.CharField(max_length=1000)
    analyst = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='analystStageO', null=True, blank=True)
    verifiedBy = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='verifiedByStageO', null=True, blank=True)
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

    def __str__(self):
        return self.name or '--Name not provided--'

    class Meta:
        verbose_name_plural = 'For Analyst - Stock Funding Stage'

class lookingForOptions(models.Model):
    name = models.CharField(max_length=1000)
    analyst = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='analystLFO', null=True, blank=True)
    verifiedBy = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='verifiedByLFO', null=True, blank=True)
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

    def __str__(self):
        return self.name or '--Name not provided--'

    class Meta:
        verbose_name_plural = 'For Analyst - Stock Funding Looking For'


class currencySymbolOptions(models.Model):
    name = models.CharField(max_length=1000)
    uniqueCode = models.CharField(max_length=1000, null=True,blank=True)
    analyst = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='analystCSO', null=True, blank=True)
    verifiedBy = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='verifiedByCSO', null=True, blank=True)
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

    def __str__(self):
        return self.name or '--Name not provided--'

    class Meta:
        verbose_name_plural = 'For Analyst - Stock Funding Currency Symbol'

class stockFunding(models.Model):
    stockProfileName = models.OneToOneField(stockBasicDetail, on_delete=models.CASCADE, related_name='stockProfileNameSF')
    analyst = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='analystSF', null=True, blank=True)
    verifiedBy = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='verifiedBySF', null=True, blank=True)
    stage = models.ForeignKey(stageOptions, related_name='stageSF', on_delete=models.SET_NULL, null=True, blank=True)
    lookingFor = models.ForeignKey(lookingForOptions, related_name='lookingForSF', on_delete=models.SET_NULL, null=True, blank=True)
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

    def __str__(self):
        return self.stockProfileName.stockName or '--Name not provided--'
        # return 'Stock Name: %s, Stage:%s' % (self.stockProfileName.stockName, self.stage.name) or '--Name not provided--'

    class Meta:
        verbose_name_plural = 'Stock Funding - Profile'

    
class stockFundingRounds(models.Model):
    stockProfileName = models.ForeignKey(stockBasicDetail, on_delete=models.CASCADE, related_name='stockProfileNameSFR')
    analyst = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='analystSFR', null=True, blank=True)
    verifiedBy = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='verifiedBySFR', null=True, blank=True)
    fundingRound = models.CharField(max_length=10, null=True, blank=True)
    dateOfInvestment = models.DateField(null=True, blank=True)
    date_available = models.BooleanField(default=True)
    fundedBy = models.CharField(max_length=1000)
    fundName = models.CharField(max_length=1000, null=True, blank=True)
    fundingAmount = models.DecimalField(max_digits=1000, decimal_places=2, null=True, blank=True)
    currencySymbol = models.ForeignKey(currencySymbolOptions, related_name='currencySymbolSFR', on_delete=models.SET_NULL, null=True, blank=True)
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

    def __str__(self):
        return self.fundedBy or '--Name not provided--'

    class Meta:
        verbose_name_plural = 'Stock Funding - Round Details'



class stockDetails(models.Model):
    stockProfileName = models.OneToOneField(stockBasicDetail, on_delete=models.CASCADE, related_name='stockProfileNameSD')
    analyst = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='analystSD', null=True, blank=True)
    verifiedBy = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='verifiedBySD', null=True, blank=True)
    companyDescription = models.TextField(null=True, blank=True)
    mergerDescription = models.TextField(null=True, blank=True)
    aquistionsDescription = models.TextField(null=True, blank=True)
    investmentsDescription = models.TextField(null=True, blank=True)
    subsidiaryDescription = models.TextField(null=True, blank=True)
    businessModelDescription = models.TextField(null=True, blank=True)
    productsAndServicesDescription = models.TextField(null=True, blank=True)
    assestsDescription =  models.TextField(null=True, blank=True)
    industryStatisticsDescription =  models.TextField(null=True, blank=True)
    futureProspectsDescription =  models.TextField(null=True, blank=True)
    governmentInitiativesDescription =  models.TextField(null=True, blank=True)
    awardsDescription =  models.TextField(null=True, blank=True)
    strengthsDescription =  models.TextField(null=True, blank=True)
    shortcomingsDescription =  models.TextField(null=True, blank=True)
    opportunitiesDescription =  models.TextField(null=True, blank=True)
    threatsDescription =  models.TextField(null=True, blank=True)
    planifyViewDescription = models.TextField(null=True, blank=True)	
    ratingDescription = models.TextField(null=True, blank=True)
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

    def __str__(self):
        return self.stockProfileName.stockName or '--Name not provided--'

    class Meta:
        verbose_name_plural = 'Stock Details - Description'


class stockRevenueBreakUp(models.Model):
    stockProfileName = models.ForeignKey(stockBasicDetail, on_delete=models.CASCADE, related_name='stockProfileNameSRB')
    analyst = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='analystSRB', null=True, blank=True)
    verifiedBy = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='verifiedBySRB', null=True, blank=True)
    items = models.CharField(max_length=1000,null=True, blank=True)
    value = models.DecimalField(max_digits=1000, decimal_places=2, null=True, blank=True)
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

    def __str__(self):
        return self.stockProfileName.stockName or '--Name not provided--'

    class Meta:
        verbose_name_plural = 'Stock Details - Revenue BreakUp'



class stockOwnership(models.Model):
    stockProfileName = models.OneToOneField(stockBasicDetail, on_delete=models.CASCADE, related_name='stockProfileNameSOwner')
    analyst = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='analystSOwner', null=True, blank=True)
    verifiedBy = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='verifiedBySOwner', null=True, blank=True)
    ownershipDescription = models.TextField(null=True, blank=True)
    totalPromoterHoldingName = models.CharField(null=True, blank=True, max_length=1000)
    totalPromoterHoldingDescription = models.TextField(null=True, blank=True)
    pledgePromoterHoldingName = models.CharField(null=True, blank=True, max_length=1000)
    pledgePromoterHoldingDescription = models.TextField(null=True, blank=True)
    mutualFundInstitutionalHoldingName = models.CharField(null=True, blank=True , max_length=1000)
    mutualFundInstitutionalHoldingDescription = models.TextField(null=True, blank=True)
    foreignInstitutionalHoldingName = models.CharField(null=True, blank=True , max_length=1000)
    foreignInstitutionalHoldingDescription = models.TextField(null=True, blank=True)
    domesticInstitutionalHoldingName = models.CharField(null=True, blank=True , max_length=1000)
    domesticInstitutionalHoldingDescription = models.TextField(null=True, blank=True)
    promoterImage = models.ImageField(upload_to='stock/images/promoterImage', null=True, blank=True)
    genderFrImage = models.CharField(max_length=25, choices=GENDER_CHOICES, default='male')
    promoterImageAlt = models.CharField(max_length=256, null=True, blank=True)
    promoterName = models.CharField(null=True, blank=True, max_length=1000)
    promoterTitle = models.CharField(null=True, blank=True, max_length=1000)
    description = models.TextField(null=True, blank=True)
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

    def __str__(self):
        return self.stockProfileName.stockName or '--Name not provided--'

    class Meta:
        verbose_name_plural = 'Stock Ownership - Share Holding Trend'


class stockOwnershipDirector(models.Model):
    stockProfileName = models.ForeignKey(stockBasicDetail, on_delete=models.CASCADE, related_name='stockProfileNameSOD')
    analyst = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='analystSOD', null=True, blank=True)
    verifiedBy = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='verifiedBySOD', null=True, blank=True)
    directorName = models.CharField(max_length=1000)
    gender = models.CharField(max_length=25, choices=GENDER_CHOICES, default='male')
    directorTitle = models.CharField(null=True, blank=True, max_length=1000)
    delta = models.TextField(null=True)
    directorImage = models.ImageField(upload_to='stock/images/directorImage', null=True, blank=True)
    directorImageAlt = models.CharField(max_length=256, null=True, blank=True)
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

    def __str__(self):
        return self.directorName or '--Name not provided--'

    class Meta:
        verbose_name_plural = 'Stock Ownership - Director Details'

class stockOwnershipInstitutional(models.Model):
    stockProfileName = models.ForeignKey(stockBasicDetail, on_delete=models.CASCADE, related_name='stockProfileNameSOI')
    analyst = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='analystSOI', null=True, blank=True)
    verifiedBy = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='verifiedBySOI', null=True, blank=True)
    institutionName = models.CharField(max_length=1000)
    fundName = models.CharField(null=True, blank=True, max_length=1000)
    institutionImage = models.ImageField(upload_to='stock/images/institutionImage', null=True, blank=True)
    institutionImageAlt = models.CharField(max_length=256, null=True, blank=True)
    noOfShares = models.BigIntegerField(null=True, blank=True)
    percentageHolding = models.DecimalField(max_digits=1000, decimal_places=2, null=True, blank=True)
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

    def __str__(self):
        return self.institutionName or '--Name not provided--'

    class Meta:
        verbose_name_plural = 'Stock Ownership - Key Institutional Details'


class stockOwnershipPattern(models.Model):
    stockProfileName = models.ForeignKey(stockBasicDetail, on_delete=models.CASCADE, related_name='stockProfileNameSOP')
    analyst = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='analystSOP', null=True, blank=True)
    verifiedBy = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='verifiedBySOP', null=True, blank=True)
    year = models.PositiveIntegerField(choices=YEAR_CHOICES, default=CURRENT_YEAR)
    totalPromoterholdingValue = models.DecimalField(max_digits=1000, decimal_places=2, null=True, blank=True)
    mutualFundHoldingValue = models.DecimalField(max_digits=1000, decimal_places=2, null=True, blank=True)
    domesticInstitutionalHoldingsValue = models.DecimalField(max_digits=1000, decimal_places=2, null=True, blank=True)
    foreignInstitutionalHoldingsValue = models.DecimalField(max_digits=1000, decimal_places=2, null=True, blank=True)
    #new fields added starts 
    institutionalHolding = models.DecimalField(max_digits=1000, decimal_places=2, null=True, blank=True)
    publicInstitutionalHoldings = models.DecimalField(max_digits=1000, decimal_places=2, null=True, blank=True)
    nonPublicInstitutionalHoldings = models.DecimalField(max_digits=1000, decimal_places=2, null=True, blank=True)
    retail = models.DecimalField(max_digits=1000, decimal_places=2, null=True, blank=True)
    employees = models.DecimalField(max_digits=1000, decimal_places=2, null=True, blank=True)
    custodians = models.DecimalField(max_digits=1000, decimal_places=2, null=True, blank=True)
    promoters = models.DecimalField(max_digits=1000, decimal_places=2, null=True, blank=True)
    privatePublicInvestmenFirmVCs = models.DecimalField(max_digits=1000, decimal_places=2, null=True, blank=True)
    #new fields added ends. 
    others = models.DecimalField(max_digits=1000, decimal_places=2, null=True, blank=True)
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

    def save(self):
        if self.totalPromoterholdingValue:
            totalPromoterholdingVal = self.totalPromoterholdingValue
        else:
            totalPromoterholdingVal = 0

        if self.mutualFundHoldingValue:
            mutualFundHoldingVal = self.mutualFundHoldingValue
        else:
            mutualFundHoldingVal = 0

        if self.domesticInstitutionalHoldingsValue:
            domesticInstitutionalHoldingsVal = self.domesticInstitutionalHoldingsValue
        else:
            domesticInstitutionalHoldingsVal = 0

        if self.foreignInstitutionalHoldingsValue:
            foreignInstitutionalHoldingsVal = self.foreignInstitutionalHoldingsValue
        else:
            foreignInstitutionalHoldingsVal = 0

        if self.institutionalHolding:
            institutionalHoldingVal = self.institutionalHolding
        else:
            institutionalHoldingVal = 0

        if self.publicInstitutionalHoldings:
            publicInstitutionalHoldingsVal = self.publicInstitutionalHoldings
        else:
            publicInstitutionalHoldingsVal = 0

        if self.nonPublicInstitutionalHoldings:
            nonPublicInstitutionalHoldingsVal = self.nonPublicInstitutionalHoldings
        else:
            nonPublicInstitutionalHoldingsVal = 0

        if self.retail:
            retailVal = self.retail
        else:
            retailVal = 0

        if self.employees:
            employeesVal = self.employees
        else:
            employeesVal = 0

        if self.custodians:
            custodiansVal = self.custodians
        else:
            custodiansVal = 0

        if self.promoters:
            promotersVal = self.promoters
        else:
            promotersVal = 0

        if self.privatePublicInvestmenFirmVCs:
            privatePublicInvestmenFirmVCsVal = self.privatePublicInvestmenFirmVCs
        else:
            privatePublicInvestmenFirmVCsVal = 0

        if self.others:
            othersVal = self.others
        else:
            othersVal = 0
        totalValue = totalPromoterholdingVal + mutualFundHoldingVal + domesticInstitutionalHoldingsVal + foreignInstitutionalHoldingsVal + institutionalHoldingVal + publicInstitutionalHoldingsVal + nonPublicInstitutionalHoldingsVal + retailVal + employeesVal + custodiansVal + promotersVal + privatePublicInvestmenFirmVCsVal + othersVal
        if totalValue == 100:
            super(stockOwnershipPattern, self).save()
        
    def __str__(self):
        return self.stockProfileName.stockName or '--Name not provided--'

    class Meta:
        verbose_name_plural = 'Stock Ownership - Share Holding Pattern'




class stockNews(models.Model):
    stockProfileName = models.ForeignKey(stockBasicDetail, on_delete=models.CASCADE, related_name='stockProfileNameSN')
    analyst = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='analystSN', null=True, blank=True)
    verifiedBy = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='verifiedBySN', null=True, blank=True)
    newsType = models.CharField(max_length=25, choices=NEWS_TYPE, null=True, blank=True)
    websiteLink = models.URLField(max_length=1000,null=True,blank=True)
    websiteThumbnail = models.TextField(null=True, blank=True)
    thumbnail = models.ImageField(upload_to='stock/images/thumbnailImage', null=True, blank=True)
    thumbnailAlt = models.CharField(max_length=256, null=True, blank=True)
    title = models.CharField(max_length=100)
    referalWebsiteName = models.CharField(max_length=100, null=True, blank=True)
    newsPublishDate = models.DateField(null=True, blank=True)
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')


    def __str__(self):
        return self.title or '--Name not provided--'

    class Meta:
        verbose_name_plural = 'Stock News - Details'

    def get_absolute_url(self):
        if self.websiteLink:
            return self.websiteLink
        else:
            return 'javascript:void(0);'

    def model_name(self):
        return 'stockNews'

    def save(self):
        if self.websiteLink:
            try:
                page = requests.get(self.websiteLink)
                soup = BeautifulSoup(page.text, 'html.parser')
                img = soup.find('meta',  property="og:image")
                self.websiteThumbnail = img["content"] if img else ""
            except:
                pass
        super(stockNews, self).save()

    def releaseDate_self(self):
        if self.newsPublishDate:
            return self.newsPublishDate
        elif self.updated:
            return self.updated
        else:
            return 'No Date'

    def get_current_image(self):
        if self.thumbnail:
            return self.thumbnail.url
        elif self.websiteThumbnail:
            return self.websiteThumbnail
        else:
            return 'https://inwoin-for-ec2.s3.amazonaws.com/static/stocks/imgs/icons/Planify-logo1.png'

    def source_self(self):
        try:
            return self.referalWebsiteName
        except:
            return 'Not Available'


class websiteMaster(models.Model):
    stockProfileName = models.ForeignKey(stockBasicDetail, on_delete=models.CASCADE, related_name='stockProfileNameWM')
    analyst = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='analystWM', null=True, blank=True)
    verifiedBy = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='verifiedByWM', null=True, blank=True)
    title = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')


    def __str__(self):
        return self.title or '--Name not provided--'

    class Meta:
        verbose_name_plural = 'Stock News - Disclaimer Details'

#As of now not using starts.
class stockEventsTypeOptions(models.Model):
    stockProfileName = models.ForeignKey(stockBasicDetail, on_delete=models.CASCADE, related_name='stockProfileNameSETO')
    analyst = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='analystSETO', null=True, blank=True)
    verifiedBy = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='verifiedBySETO', null=True, blank=True)
    stockEventType = models.CharField(null=True, blank=True, max_length=1000)
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')


    def __str__(self):
        return self.stockEventType or '--Name not provided--'

    class Meta:
        verbose_name_plural = 'For Analyst - Stock Events Event Type Options'
#As of now not using ends.


class dividendTypeOptions(models.Model):
    name = models.CharField(max_length=1000)
    analyst = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='analystDTO', null=True, blank=True)
    verifiedBy = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='verifiedByDTO', null=True, blank=True)
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

    def __str__(self):
        return self.name or '--Name not provided--'

    class Meta:
        verbose_name_plural = 'For Analyst- Stock Events Dividend Type'



class stockEventsDividend(models.Model):
    stockProfileName = models.ForeignKey(stockBasicDetail, on_delete=models.CASCADE, related_name='stockProfileNameSED')
    analyst = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='analystSED', null=True, blank=True)
    verifiedBy = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='verifiedBySED', null=True, blank=True)
    dividendType = models.ForeignKey(dividendTypeOptions, on_delete=models.SET_NULL, null=True, blank=True, related_name='dividendTypeSED')
    dividendShare = models.DecimalField(max_digits=1000, decimal_places=2, null=True, blank=True)
    exDateFrDividend = models.DateField(null=True, blank=True)
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

    def __str__(self):
        return self.stockProfileName.stockName or '--Name not provided--'

    class Meta:
        verbose_name_plural = 'Stock Events - Dividend Type Details'


class corpActionsOptions(models.Model):
    name = models.CharField(max_length=1000)
    analyst = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='analystCAO', null=True, blank=True)
    verifiedBy = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='verifiedByCAO', null=True, blank=True)
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

    def __str__(self):
        return self.name or '--Name not provided--'

    class Meta:
        verbose_name_plural = 'For Analyst - Stock Events Corporate Actions'

class stockEventsCorpActions(models.Model):
    stockProfileName = models.ForeignKey(stockBasicDetail, on_delete=models.CASCADE, related_name='stockProfileNameSEC')
    analyst = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='analystSECA', null=True, blank=True)
    verifiedBy = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='verifiedBySECA', null=True, blank=True)
    corporateActionsName = models.ForeignKey(corpActionsOptions, on_delete=models.SET_NULL, null=True, blank=True, related_name='pastCorporateActionsSEC')
    corporateActionsDescription = models.TextField(null=True, blank=True)
    ratio = models.CharField(max_length=50, null=True, blank=True)
    exDateFrCorporate = models.DateField(null=True, blank=True)
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

    def __str__(self):
        return self.stockProfileName.stockName or '--Name not provided--'

    class Meta:
        verbose_name_plural = 'Stock Events - Corporate Actions Details'

class announcementTypeOptions(models.Model):
    name = models.CharField(max_length=1000)
    analyst = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='analystATO', null=True, blank=True)
    verifiedBy = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='verifiedByATO', null=True, blank=True)
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

    def __str__(self):
        return self.name or '--Name not provided--'

    class Meta:
        verbose_name_plural = 'For Analyst - Stock Events Announcement Type'

class stockEventsAnnouncements(models.Model):
    stockProfileName = models.ForeignKey(stockBasicDetail, on_delete=models.CASCADE, related_name='stockProfileNameSEA')
    analyst = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='analystSEA', null=True, blank=True)
    verifiedBy = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='verifiedBySEA', null=True, blank=True)
    announcementTitle = models.ForeignKey(announcementTypeOptions, on_delete=models.SET_NULL, null=True, blank=True, related_name='announcementTitleSEA')
    announcementBrief = models.TextField(null=True, blank=True)
    linkUrlFrAnnouncement = models.URLField(null=True, blank=True)
    linkFrAnnouncement = models.FileField(upload_to ='stock/document/linkFrAnnouncement',null=True, blank=True, validators=[FileExtensionValidator(['pdf'])])
    dateFrAnnouncement = models.DateField(null=True, blank=True)
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

    def __str__(self):
        return self.stockProfileName.stockName or '--Name not provided--'

    class Meta:
        verbose_name_plural = 'Stock Events - Announcement Type Details'
    
# class legalOrdersOptions(models.Model):
# 	name = models.CharField(max_length=1000)
# 	analyst = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='analystLOO', null=True, blank=True)
# 	verifiedBy = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='verifiedByLOO', null=True, blank=True)
# 	publish = models.DateTimeField(default=timezone.now)
# 	created = models.DateTimeField(auto_now_add=True)
# 	updated = models.DateTimeField(auto_now=True)
# 	status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

# 	def __str__(self):
# 		return self.name or '--Name not provided--'

# 	class Meta:
# 		verbose_name_plural = 'For Analyst - Stock Events Legal Orders Options'

class stockEventsLegalOrders(models.Model):
    stockProfileName = models.ForeignKey(stockBasicDetail, on_delete=models.CASCADE, related_name='stockProfileNameSELO')
    analyst = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='analystSELO', null=True, blank=True)
    verifiedBy = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='verifiedBySELO', null=True, blank=True)
    caseTitle = models.CharField(max_length=1000, null=True, blank=True)
    caseNumber = models.CharField(max_length=1000, null=True, blank=True)
    linkUrlFrLegalOrders = models.URLField(null=True, blank=True)
    linkFrLegalOrders = models.FileField(upload_to ='stock/document/linkFrLegalOrders',null=True, blank=True, validators=[FileExtensionValidator(['pdf'])])
    exDateFrLegalOrders = models.DateField(null=True, blank=True)
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

    def __str__(self):
        return self.stockProfileName.stockName or '--Name not provided--'

    class Meta:
        verbose_name_plural = 'Stock Events - Legal Orders Details'



class financialStatementsFrBalanceSheet(models.Model):
    stockProfileName = models.ForeignKey(stockBasicDetail, on_delete=models.CASCADE, related_name='stockProfileNameFS')
    analyst = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='analystFS', null=True, blank=True)
    verifiedBy = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='verifiedByFS', null=True, blank=True)
    statementIcon = models.PositiveIntegerField(choices=ICON_CHOICES, default=1)
    title = models.CharField(max_length=1000)
    description = models.TextField(null=True, blank=True)	
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

    def __str__(self):
        return self.title or '--Name not provided--'

    class Meta:
        verbose_name_plural = 'Stock Financial - Balance Sheet Details'

class financialStatementsFrProfitAndLoss(models.Model):
    stockProfileName = models.ForeignKey(stockBasicDetail, on_delete=models.CASCADE, related_name='stockProfileNameFSPL')
    analyst = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='analystFSPL', null=True, blank=True)
    verifiedBy = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='verifiedByFSPL', null=True, blank=True)
    statementIcon = models.PositiveIntegerField(choices=ICON_CHOICES, default=1)
    title = models.CharField(max_length=1000)
    description = models.TextField(null=True, blank=True)
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

    def __str__(self):
        return self.title or '--Name not provided--'

    class Meta:
        verbose_name_plural = 'Stock Financial - Profit And Loss Details'

class financialStatementsFrCashFlow(models.Model):
    stockProfileName = models.ForeignKey(stockBasicDetail, on_delete=models.CASCADE, related_name='stockProfileNameFSCF')
    analyst = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='analystFSCF', null=True, blank=True)
    verifiedBy = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='verifiedByFSCF', null=True, blank=True)
    statementIcon = models.PositiveIntegerField(choices=ICON_CHOICES, default=1)
    title = models.CharField(max_length=1000)
    description = models.TextField(null=True, blank=True)
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

    def __str__(self):
        return self.title or '--Name not provided--'

    class Meta:
        verbose_name_plural = 'Stock Financial - CashFlow Details'

class financialCompanyUpdates(models.Model):
    stockProfileName = models.ForeignKey(stockBasicDetail, on_delete=models.CASCADE, related_name='stockProfileNameFCU')
    analyst = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='analystFCU', null=True, blank=True)
    verifiedBy = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='verifiedByFCU', null=True, blank=True)
    title = models.PositiveIntegerField(choices=YEAR_CHOICES, default=CURRENT_YEAR)
    description = models.TextField(null=True, blank=True)
    linkFrReport = models.FileField(upload_to ='stock/document/linkFrReport',null=True, blank=True, validators=[FileExtensionValidator(['pdf'])])
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

    def __str__(self):
        return self.title or '--Name not provided--'

    class Meta:
        verbose_name_plural = 'Stock Financial - Company Financial Reports'


class annualReportsDHRPImage(models.Model):
    stockProfileName = models.ForeignKey(stockBasicDetail, on_delete=models.CASCADE, related_name='stockProfileNameARDHRPImage')
    DRHPimage_heading = models.CharField(max_length=500, null=True, blank=True)
    DRHPimage_uploadReport = models.FileField(upload_to ='stock/document/imageReport',null=True, blank=True)
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

    def __str__(self):
        return self.DRHPimage_heading or '--Name not provided--'

    class Meta:
        verbose_name_plural = 'Stock Financial -DRHP-Image'


class annualReportsDHRP(models.Model):
    stockProfileName = models.OneToOneField(stockBasicDetail, on_delete=models.CASCADE, related_name='stockProfileNameARDHRP')
    DRHP_heading = models.CharField(max_length=500, null=True, blank=True)
    DRHP_uploadReport = models.FileField(upload_to ='stock/document/uploadReport',null=True, blank=True, validators=[FileExtensionValidator(['pdf'])])
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

    def __str__(self):
        return self.DRHP_heading or '--Name not provided--'

    class Meta:
        verbose_name_plural = 'Stock Financial - Annual Reports - DRHP'

class stockDeckAndDocs(models.Model):
    stockProfileName = models.ForeignKey(stockBasicDetail, on_delete=models.CASCADE, related_name='stockProfileNameARDD')
    titleOrYear = models.CharField(max_length=1000, null=True, blank=True)
    description = models.CharField(max_length=2000, null=True, blank=True)
    uploadPDFOrPPT = models.FileField(upload_to ='stock/document/uploadReport',null=True, blank=True, validators=[FileExtensionValidator(['pdf','ppt','pptm','pptx','jpeg','jpg', 'png'])])
    # uploadPpt = models.FileField(upload_to ='stock/document/uploadReport',null=True, blank=True, validators=[FileExtensionValidator(['ppt'])])
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')


    def extension(self):
        name, extension = os.path.splitext(self.uploadPDFOrPPT.name)
        return extension

    def __str__(self):
        return self.titleOrYear or '--Name not provided--'

    class Meta:
        verbose_name_plural = 'Stock Financial - Deck and Documents'



class stockBalanceSheet(models.Model):
    stockProfileName = models.ForeignKey(stockBasicDetail, on_delete=models.CASCADE, related_name='stockProfileNameSBS')
    analyst = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='analystSBS', null=True, blank=True)
    verifiedBy = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='verifiedBySBS', null=True, blank=True)
    year = models.PositiveIntegerField(choices=YEAR_CHOICES, default=CURRENT_YEAR)
    cashAndCashEquivalents = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)
    marketableSecurities = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)
    bankBalanceOtherThanCashEquivalents = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True) 
    cashAndShortTermInvestments = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True) #cashAndShortTermInvestments = cashAndCashEquivalents + marketableSecurities + bankBalanceOtherThanCashEquivalents
    totalReceivables = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)
    totalInventory = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)
    prepaidExpenses = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)
    currentInvestments = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)
    otherCurrentFinancialAssets = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)
    loanAndAdvances = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)
    deferredTaxAssest = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)
    currentAssets =  models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True) # currentAssets = cashAndShortTermInvestments + totalReceivables + totalInventory + prepaidExpenses + currentInvestments + otherCurrentFinancialAssets + loanAndAdvances + deferredTaxAssest
    netPropertyORPlantOREquipment = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)
    goodWill = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)
    otherIntangibleAssests = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)
    intangibleAssestsUnderDevelopment = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)
    longTermInvestments = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)
    deferredTaxAssetsNet = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)
    otherNonCurrentAssets = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)
    nonCurrentAssets = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)#nonCurrentAssets = netPropertyORPlantOREquipment + goodwill + otherIntangibleAssests + intangibleAssestsUnderDevelopment + longTermInvestments + deferredTaxAssetsNet + otherNonCurrentAssets
    totalAssets = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)
    accountPayable = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)
    totalDeposits = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)
    currentPortionOfLongTermDebt = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)
    unearnedRevenue = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)
    currentPortionOfLeases = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)
    otherCurrentLiabilities = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)
    currentLiabilities = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)#currentLiabilities =  accountPayable+ totalDeposits+ currentPortionOfLongTermDebt+ UnearnedRevenue+ currentPortionOfLeases+ otherCurrentLiabilities
    totalLongTermDebt = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)
    longTermPortionOfLeases = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)
    deferredTaxLiabilities = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)
    otherNonCurrentLiabilities = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)
    nonCurrentLiabilities = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True) #nonCurrentLiabilities = totalLongTermDebt + longTermPortionOfLeases + deferredTaxLiabilities + otherNonCurrentLiabilities
    totalLiabilities = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)
    commonStock = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)
    otherEquity = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)
    reservesAndSurplus = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)
    additionalPaidInCapital = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)
    retainedEarnings =  models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)
    minorityInterest = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)
    treasureStock =  models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)
    comprehensiveIncAndOther =  models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)
    totalEquity = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True) #totalEquity = commonStock + otherEquity + reservesAndSurplus + additionalPaidInCapital + retainedEarnings + minorityInterest + treasureStock + comprehensiveIncAndOther
    totalCommonSharesOutstanding = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)
    totalLiabilitiesShareHolderHistory = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)#totalLiabilitiesShareHolderHistory = totalEquity + currentLiabilities + nonCurrentLiabilities
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

    def save(self):
        if not self.cashAndShortTermInvestments:
            if self.cashAndCashEquivalents:
                cashCashEquiv = self.cashAndCashEquivalents
            else:
                cashCashEquiv = 0
            if self.marketableSecurities:
                marketableSec = self.marketableSecurities
            else:
                marketableSec = 0
            if self.bankBalanceOtherThanCashEquivalents:
                bankBalOthrThnCashEquiv = self.bankBalanceOtherThanCashEquivalents
            else:
                bankBalOthrThnCashEquiv = 0
            self.cashAndShortTermInvestments = cashCashEquiv + marketableSec + bankBalOthrThnCashEquiv
            cashShortTermInvest = self.cashAndShortTermInvestments
        else :
            cashShortTermInvest = self.cashAndShortTermInvestments
            
        if self.totalReceivables:
            totalRecv = self.totalReceivables
        else:
            totalRecv = 0
        if self.totalInventory:
            totalInv = self.totalInventory
        else:
            totalInv = 0
        if self.prepaidExpenses:
            prepaidExp = self.prepaidExpenses
        else:
            prepaidExp = 0
        if self.currentInvestments:
            currentInvst = self.currentInvestments
        else:
            currentInvst = 0
        if self.otherCurrentFinancialAssets:
            otherCrrFinAssets = self.otherCurrentFinancialAssets
        else:
            otherCrrFinAssets = 0
        if self.loanAndAdvances:
            loanAdv = self.loanAndAdvances
        else:
            loanAdv = 0
        if self.deferredTaxAssest:
            defTaxeAssest = self.deferredTaxAssest
        else:
            defTaxeAssest = 0
        self.currentAssets = cashShortTermInvest + totalRecv + totalInv + prepaidExp + currentInvst + otherCrrFinAssets + loanAdv + defTaxeAssest

        if self.netPropertyORPlantOREquipment:
            netPropPlantEquip = self.netPropertyORPlantOREquipment
        else:
            netPropPlantEquip = 0
        if self.goodWill:
            goodwill = self.goodWill
        else:
            goodwill = 0
        if self.otherIntangibleAssests:
            otherIntangAssest = self.otherIntangibleAssests
        else:
            otherIntangAssest = 0
        if self.intangibleAssestsUnderDevelopment:
            intangAssestsUnderDevelop = self.intangibleAssestsUnderDevelopment
        else:
            intangAssestsUnderDevelop = 0
        if self.longTermInvestments:
            longTermInv = self.longTermInvestments
        else:
            longTermInv = 0
        if self.deferredTaxAssetsNet:
            defTaxAssetsNet = self.deferredTaxAssetsNet
        else:
            defTaxAssetsNet = 0
        if self.otherNonCurrentAssets:
            otherNonCurrAssets = self.otherNonCurrentAssets
        else:
            otherNonCurrAssets = 0
        self.nonCurrentAssets = netPropPlantEquip + goodwill + otherIntangAssest + intangAssestsUnderDevelop + longTermInv + defTaxAssetsNet + otherNonCurrAssets

        self.totalAssets = self.currentAssets + self.nonCurrentAssets

        if self.accountPayable:
            accPayable = self.accountPayable
        else:
            accPayable = 0
        if self.totalDeposits:
            totDeposits = self.totalDeposits
        else:
            totDeposits = 0
        if self.currentPortionOfLongTermDebt:
            crrPortLongTermDebt = self.currentPortionOfLongTermDebt
        else:
            crrPortLongTermDebt = 0
        if self.unearnedRevenue:
            unearnedRev = self.unearnedRevenue
        else:
            unearnedRev = 0
        if self.currentPortionOfLeases:
            currentPortLeases = self.currentPortionOfLeases
        else:
            currentPortLeases = 0
        if self.otherCurrentLiabilities:
            otherCurrLiabilities = self.otherCurrentLiabilities
        else:
            otherCurrLiabilities = 0
        self.currentLiabilities = accPayable + totDeposits + crrPortLongTermDebt + unearnedRev + currentPortLeases + otherCurrLiabilities

        if self.totalLongTermDebt:
            totLongTermDebt = self.totalLongTermDebt
        else:
            totLongTermDebt = 0
        if self.longTermPortionOfLeases:
            longTermPortLeases = self.longTermPortionOfLeases
        else:
            longTermPortLeases = 0
        if self.deferredTaxLiabilities:
            defTaxLiabilities = self.deferredTaxLiabilities
        else:
            defTaxLiabilities = 0
        if self.otherNonCurrentLiabilities:
            otherNonCurrLiabilities = self.otherNonCurrentLiabilities
        else:
            otherNonCurrLiabilities = 0
        self.nonCurrentLiabilities = totLongTermDebt + longTermPortLeases + defTaxLiabilities + otherNonCurrLiabilities

        self.totalLiabilities = self.currentLiabilities + self.nonCurrentLiabilities

        if self.commonStock:
            commStock = self.commonStock
        else:
            commStock = 0
        if self.otherEquity:
            othrEquity = self.otherEquity
        else:
            othrEquity = 0
        if self.reservesAndSurplus:
            reservesSurplus = self.reservesAndSurplus
        else:
            reservesSurplus = 0
        if self.additionalPaidInCapital:
            addtnlPaidCapital = self.additionalPaidInCapital
        else:
            addtnlPaidCapital = 0
        if self.retainedEarnings:
            retainedEarn = self.retainedEarnings
        else:
            retainedEarn = 0
        if self.minorityInterest:
            minInterest = self.minorityInterest
        else:
            minInterest = 0
        if self.treasureStock:
            treasStock = self.treasureStock
        else:
            treasStock = 0
        if self.comprehensiveIncAndOther:
            comprehensiveIncOther = self.comprehensiveIncAndOther
        else:
            comprehensiveIncOther = 0
        self.totalEquity = commStock + othrEquity + reservesSurplus + addtnlPaidCapital + retainedEarn + minInterest + treasStock + comprehensiveIncOther

        if self.totalCommonSharesOutstanding:
            totCommonSharesOutstand = self.totalCommonSharesOutstanding
        else:
            totCommonSharesOutstand = 0

        self.totalLiabilitiesShareHolderHistory =  self.totalEquity + self.currentLiabilities + self.nonCurrentLiabilities
        # print('------------MODEL PRINT self.totalAssets - self.totalLiabilitiesShareHolderHistory-----------')
        # print(self.totalAssets - self.totalLiabilitiesShareHolderHistory == 0)
        # print('------------// MODEL PRINT self.totalAssets - self.totalLiabilitiesShareHolderHistory //-----------')
        # if (self.totalAssets - self.totalLiabilitiesShareHolderHistory) == 0:
        super(stockBalanceSheet, self).save()
        # else:
        # 	raise ValueError('Total Liabilities and Sharehold’s Equity - Total Asset should be Zero')

    def __str__(self):
        return 'Stock Name: %s, Year: %s' % (self.stockProfileName.stockName, self.year) or '--Name not provided--'

    class Meta:
        verbose_name_plural = 'Stock Financial - Balance Sheet'

#------Quarter starts For Balance Sheet -------
class stockBalanceSheetTTM(models.Model):
    stockProfileName = models.OneToOneField(stockBasicDetail, on_delete=models.CASCADE, related_name='stockProfileNameSBSTTM')
    analyst = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='analystSBSTTM', null=True, blank=True)
    verifiedBy = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='verifiedBySBSTTM', null=True, blank=True)
    year = models.PositiveIntegerField(choices=YEAR_CHOICES, default=CURRENT_YEAR)
    TTMDataFor = models.CharField(max_length=25, choices=TTM_CHOICES, default='quarter')
    cashAndCashEquivalents = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)
    marketableSecurities = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)
    bankBalanceOtherThanCashEquivalents = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True) 
    cashAndShortTermInvestments = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True) #cashAndShortTermInvestments = cashAndCashEquivalents + marketableSecurities + bankBalanceOtherThanCashEquivalents
    totalReceivables = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)
    totalInventory = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)
    prepaidExpenses = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)
    currentInvestments = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)
    otherCurrentFinancialAssets = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)
    loanAndAdvances = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)
    deferredTaxAssest = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)
    currentAssets =  models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True) # currentAssets = cashAndShortTermInvestments + totalReceivables + totalInventory + prepaidExpenses + currentInvestments + otherCurrentFinancialAssets + loanAndAdvances + deferredTaxAssest
    netPropertyORPlantOREquipment = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)
    goodWill = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)
    otherIntangibleAssests = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)
    intangibleAssestsUnderDevelopment = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)
    longTermInvestments = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)
    deferredTaxAssetsNet = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)
    otherNonCurrentAssets = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)
    nonCurrentAssets = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)#nonCurrentAssets = netPropertyORPlantOREquipment + goodwill + otherIntangibleAssests + intangibleAssestsUnderDevelopment + longTermInvestments + deferredTaxAssetsNet + otherNonCurrentAssets
    totalAssets = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)
    accountPayable = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)
    totalDeposits = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)
    currentPortionOfLongTermDebt = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)
    unearnedRevenue = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)
    currentPortionOfLeases = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)
    otherCurrentLiabilities = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)
    currentLiabilities = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)#currentLiabilities =  accountPayable+ totalDeposits+ currentPortionOfLongTermDebt+ UnearnedRevenue+ currentPortionOfLeases+ otherCurrentLiabilities
    totalLongTermDebt = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)
    longTermPortionOfLeases = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)
    deferredTaxLiabilities = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)
    otherNonCurrentLiabilities = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)
    nonCurrentLiabilities = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True) #nonCurrentLiabilities = totalLongTermDebt + longTermPortionOfLeases + deferredTaxLiabilities + otherNonCurrentLiabilities
    totalLiabilities = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)
    commonStock = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)
    otherEquity = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)
    reservesAndSurplus = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)
    additionalPaidInCapital = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)
    retainedEarnings =  models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)
    minorityInterest = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)
    treasureStock =  models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)
    comprehensiveIncAndOther =  models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)
    totalEquity = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True) #totalEquity = commonStock + otherEquity + reservesAndSurplus + additionalPaidInCapital + retainedEarnings + minorityInterest + treasureStock + comprehensiveIncAndOther
    totalCommonSharesOutstanding = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)
    totalLiabilitiesShareHolderHistory = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)#totalLiabilitiesShareHolderHistory = totalEquity + currentLiabilities + nonCurrentLiabilities
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

    def save(self):
        if not self.cashAndShortTermInvestments:
            if self.cashAndCashEquivalents:
                cashCashEquiv = self.cashAndCashEquivalents
            else:
                cashCashEquiv = 0
            if self.marketableSecurities:
                marketableSec = self.marketableSecurities
            else:
                marketableSec = 0
            if self.bankBalanceOtherThanCashEquivalents:
                bankBalOthrThnCashEquiv = self.bankBalanceOtherThanCashEquivalents
            else:
                bankBalOthrThnCashEquiv = 0
            self.cashAndShortTermInvestments = cashCashEquiv + marketableSec + bankBalOthrThnCashEquiv
            cashShortTermInvest = self.cashAndShortTermInvestments
        else :
            cashShortTermInvest = self.cashAndShortTermInvestments
            
        if self.totalReceivables:
            totalRecv = self.totalReceivables
        else:
            totalRecv = 0
        if self.totalInventory:
            totalInv = self.totalInventory
        else:
            totalInv = 0
        if self.prepaidExpenses:
            prepaidExp = self.prepaidExpenses
        else:
            prepaidExp = 0
        if self.currentInvestments:
            currentInvst = self.currentInvestments
        else:
            currentInvst = 0
        if self.otherCurrentFinancialAssets:
            otherCrrFinAssets = self.otherCurrentFinancialAssets
        else:
            otherCrrFinAssets = 0
        if self.loanAndAdvances:
            loanAdv = self.loanAndAdvances
        else:
            loanAdv = 0
        if self.deferredTaxAssest:
            defTaxeAssest = self.deferredTaxAssest
        else:
            defTaxeAssest = 0
        self.currentAssets = cashShortTermInvest + totalRecv + totalInv + prepaidExp + currentInvst + otherCrrFinAssets + loanAdv + defTaxeAssest

        if self.netPropertyORPlantOREquipment:
            netPropPlantEquip = self.netPropertyORPlantOREquipment
        else:
            netPropPlantEquip = 0
        if self.goodWill:
            goodwill = self.goodWill
        else:
            goodwill = 0
        if self.otherIntangibleAssests:
            otherIntangAssest = self.otherIntangibleAssests
        else:
            otherIntangAssest = 0
        if self.intangibleAssestsUnderDevelopment:
            intangAssestsUnderDevelop = self.intangibleAssestsUnderDevelopment
        else:
            intangAssestsUnderDevelop = 0
        if self.longTermInvestments:
            longTermInv = self.longTermInvestments
        else:
            longTermInv = 0
        if self.deferredTaxAssetsNet:
            defTaxAssetsNet = self.deferredTaxAssetsNet
        else:
            defTaxAssetsNet = 0
        if self.otherNonCurrentAssets:
            otherNonCurrAssets = self.otherNonCurrentAssets
        else:
            otherNonCurrAssets = 0
        self.nonCurrentAssets = netPropPlantEquip + goodwill + otherIntangAssest + intangAssestsUnderDevelop + longTermInv + defTaxAssetsNet + otherNonCurrAssets

        self.totalAssets = self.currentAssets + self.nonCurrentAssets

        if self.accountPayable:
            accPayable = self.accountPayable
        else:
            accPayable = 0
        if self.totalDeposits:
            totDeposits = self.totalDeposits
        else:
            totDeposits = 0
        if self.currentPortionOfLongTermDebt:
            crrPortLongTermDebt = self.currentPortionOfLongTermDebt
        else:
            crrPortLongTermDebt = 0
        if self.unearnedRevenue:
            unearnedRev = self.unearnedRevenue
        else:
            unearnedRev = 0
        if self.currentPortionOfLeases:
            currentPortLeases = self.currentPortionOfLeases
        else:
            currentPortLeases = 0
        if self.otherCurrentLiabilities:
            otherCurrLiabilities = self.otherCurrentLiabilities
        else:
            otherCurrLiabilities = 0
        self.currentLiabilities = accPayable + totDeposits + crrPortLongTermDebt + unearnedRev + currentPortLeases + otherCurrLiabilities

        if self.totalLongTermDebt:
            totLongTermDebt = self.totalLongTermDebt
        else:
            totLongTermDebt = 0
        if self.longTermPortionOfLeases:
            longTermPortLeases = self.longTermPortionOfLeases
        else:
            longTermPortLeases = 0
        if self.deferredTaxLiabilities:
            defTaxLiabilities = self.deferredTaxLiabilities
        else:
            defTaxLiabilities = 0
        if self.otherNonCurrentLiabilities:
            otherNonCurrLiabilities = self.otherNonCurrentLiabilities
        else:
            otherNonCurrLiabilities = 0
        self.nonCurrentLiabilities = totLongTermDebt + longTermPortLeases + defTaxLiabilities + otherNonCurrLiabilities

        self.totalLiabilities = self.currentLiabilities + self.nonCurrentLiabilities

        if self.commonStock:
            commStock = self.commonStock
        else:
            commStock = 0
        if self.otherEquity:
            othrEquity = self.otherEquity
        else:
            othrEquity = 0
        if self.reservesAndSurplus:
            reservesSurplus = self.reservesAndSurplus
        else:
            reservesSurplus = 0
        if self.additionalPaidInCapital:
            addtnlPaidCapital = self.additionalPaidInCapital
        else:
            addtnlPaidCapital = 0
        if self.retainedEarnings:
            retainedEarn = self.retainedEarnings
        else:
            retainedEarn = 0
        if self.minorityInterest:
            minInterest = self.minorityInterest
        else:
            minInterest = 0
        if self.treasureStock:
            treasStock = self.treasureStock
        else:
            treasStock = 0
        if self.comprehensiveIncAndOther:
            comprehensiveIncOther = self.comprehensiveIncAndOther
        else:
            comprehensiveIncOther = 0
        self.totalEquity = commStock + othrEquity + reservesSurplus + addtnlPaidCapital + retainedEarn + minInterest + treasStock + comprehensiveIncOther

        if self.totalCommonSharesOutstanding:
            totCommonSharesOutstand = self.totalCommonSharesOutstanding
        else:
            totCommonSharesOutstand = 0

        self.totalLiabilitiesShareHolderHistory =  self.totalEquity + self.currentLiabilities + self.nonCurrentLiabilities
        # if (self.totalAssets - self.totalLiabilitiesShareHolderHistory) == 0:
        super(stockBalanceSheetTTM, self).save()
        # else:
        # 	raise ValueError('Total Liabilities and Sharehold’s Equity - Total Asset should be Zero')
        # super(stockBalanceSheetTTM, self).save()

    def __str__(self):
        return 'Stock Name: %s, TTM: %s' % (self.stockProfileName.stockName, self.TTMDataFor) or '--Name not provided--'

    class Meta:
        verbose_name_plural = 'Stock Financial - Balance Sheet TTM'


#------Quarter ends For Balance Sheet -------

class stockProfitAndLoss(models.Model):
    stockProfileName = models.ForeignKey(stockBasicDetail, on_delete=models.CASCADE, related_name='stockProfileNameSPAL')
    analyst = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='analystSPAL', null=True, blank=True)
    verifiedBy = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='verifiedBySPAL', null=True, blank=True)
    year = models.PositiveIntegerField(choices=YEAR_CHOICES, default=CURRENT_YEAR)
    revenue = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)
    otherRevenue = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)
    totalRevenue = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True) #totalRevenue= revenue + otherRevenue
    costOfGoodsSold = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)
    grossProfit = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True) #grossProfit = totalRevenue - costOfGoodsSold
    rawMaterials = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)
    powerAndFuelCost = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)
    employeeCost = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)
    sellingAndAdministrativeExpenses = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)
    operatingAndOtherExpenses = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)
    ebidta = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True) #ebidta = totalRevenue - rawMaterials - powerAndFuelCost - employeeCost - sellingAndAdministrativeExpenses - operatingAndOtherExpenses
    depreciationAndAmortization = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)
    pbit = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True) #pbit = ebidta - depreciationAndAmortization
    interestIncome = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)
    interestExpense = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)
    otherItems = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)
    pbt = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True) #pbt = pbit - (interestIncome-interestExpense) 
    taxesAndOtherItems = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)
    netIncome = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True) #netIncome = pbt - taxesAndOtherItems
    dilutedEPS = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)
    basicEPS = 	models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)
    DPS = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)
    payoutRatio = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

    def save(self):
        if self.revenue:
            rev = self.revenue
        else:
            rev = 0
        if self.otherRevenue:
            otherRev = self.otherRevenue
        else:
            otherRev = 0
        self.totalRevenue = rev + otherRev

        if self.costOfGoodsSold:
            cogs = self.costOfGoodsSold
        else:
            cogs = 0
        self.grossProfit = self.totalRevenue - cogs

        if self.rawMaterials:
            rawMat = self.rawMaterials
        else:
            rawMat = 0
        if self.powerAndFuelCost:
            powFuelCost = self.powerAndFuelCost
        else:
            powFuelCost = 0
        if self.employeeCost:
            empCost = self.employeeCost
        else:
            empCost = 0
        if self.sellingAndAdministrativeExpenses:
            sellingAdminExp = self.sellingAndAdministrativeExpenses
        else:
            sellingAdminExp = 0
        if self.operatingAndOtherExpenses:
            operatingOtherExp = self.operatingAndOtherExpenses
        else:
            operatingOtherExp = 0
        self.ebidta = self.grossProfit - rawMat - powFuelCost - empCost - sellingAdminExp - operatingOtherExp
        
        if self.depreciationAndAmortization:
            depAmort = self.depreciationAndAmortization
        else:
            depAmort = 0
        self.pbit = self.ebidta - depAmort 

        if self.interestIncome:
            intInc = self.interestIncome
        else:
            intInc = 0
        if self.interestExpense:
            intExp = self.interestExpense
        else:
            intExp = 0
        if self.otherItems:
            otherItems = self.otherItems
        else:
            otherItems = 0
        self.pbt = self.pbit  + intInc - intExp - otherItems

        if self.taxesAndOtherItems:
            taxesOthrItems = self.taxesAndOtherItems
        else:
            taxesOthrItems = 0
        self.netIncome = self.pbt - taxesOthrItems
        super(stockProfitAndLoss, self).save()


    def __str__(self):
        return self.stockProfileName.stockName or '--Name not provided--'

    class Meta:
        verbose_name_plural = 'Stock Financial - Profit And Loss'


# # 
# #Quarter starts for Profit and loss starts
class stockProfitAndLossTTM(models.Model):
    stockProfileName = models.ForeignKey(stockBasicDetail, on_delete=models.CASCADE, related_name='stockProfileNameSPALTTM')
    analyst = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='analystSPALTTM', null=True, blank=True)
    verifiedBy = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='verifiedBySPALTTM', null=True, blank=True)
    year = models.PositiveIntegerField(choices=YEAR_CHOICES, default=CURRENT_YEAR)
    TTMDataFor = models.CharField(max_length=25, choices=TTM_CHOICES, default='quarter')
    revenue = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)
    otherRevenue = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)
    totalRevenue = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True) #totalRevenue= revenue + otherRevenue
    costOfGoodsSold = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)
    grossProfit = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True) #grossProfit = totalRevenue - costOfGoodsSold
    rawMaterials = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)
    powerAndFuelCost = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)
    employeeCost = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)
    sellingAndAdministrativeExpenses = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)
    operatingAndOtherExpenses = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)
    ebidta = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True) #ebidta = totalRevenue - rawMaterials - powerAndFuelCost - employeeCost - sellingAndAdministrativeExpenses - operatingAndOtherExpenses
    depreciationAndAmortization = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)
    pbit = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True) #pbit = ebidta - depreciationAndAmortization
    interestIncome = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)
    interestExpense = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)
    otherItems = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)
    pbt = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True) #pbt = pbit - (interestIncome-interestExpense) 
    taxesAndOtherItems = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)
    netIncome = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True) #netIncome = pbt - taxesAndOtherItems
    dilutedEPS = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)
    basicEPS = 	models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)
    DPS = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)
    payoutRatio = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

    def save(self):
        if self.revenue:
            rev = self.revenue
        else:
            rev = 0
        if self.otherRevenue:
            otherRev = self.otherRevenue
        else:
            otherRev = 0
        self.totalRevenue = rev + otherRev

        if self.costOfGoodsSold:
            cogs = self.costOfGoodsSold
        else:
            cogs = 0
        self.grossProfit = self.totalRevenue - cogs

        if self.rawMaterials:
            rawMat = self.rawMaterials
        else:
            rawMat = 0
        if self.powerAndFuelCost:
            powFuelCost = self.powerAndFuelCost
        else:
            powFuelCost = 0
        if self.employeeCost:
            empCost = self.employeeCost
        else:
            empCost = 0
        if self.sellingAndAdministrativeExpenses:
            sellingAdminExp = self.sellingAndAdministrativeExpenses
        else:
            sellingAdminExp = 0
        if self.operatingAndOtherExpenses:
            operatingOtherExp = self.operatingAndOtherExpenses
        else:
            operatingOtherExp = 0
        self.ebidta = self.grossProfit - rawMat - powFuelCost - empCost - sellingAdminExp - operatingOtherExp
        
        if self.depreciationAndAmortization:
            depAmort = self.depreciationAndAmortization
        else:
            depAmort = 0
        self.pbit = self.ebidta - depAmort 

        if self.interestIncome:
            intInc = self.interestIncome
        else:
            intInc = 0
        if self.interestExpense:
            intExp = self.interestExpense
        else:
            intExp = 0
        if self.otherItems:
            otherItems = self.otherItems
        else:
            otherItems = 0
        self.pbt = self.pbit  + intInc - intExp - otherItems

        if self.taxesAndOtherItems:
            taxesOthrItems = self.taxesAndOtherItems
        else:
            taxesOthrItems = 0
        self.netIncome = self.pbt - taxesOthrItems
        super(stockProfitAndLossTTM, self).save()


    def __str__(self):
        return self.stockProfileName.stockName or '--Name not provided--'

    class Meta:
        verbose_name_plural = 'Stock Financial - Profit And Loss TTM'
# #Quarter ends for Profit and loss ends

class stockCashFlow(models.Model):
    stockProfileName = models.ForeignKey(stockBasicDetail, on_delete=models.CASCADE, related_name='stockProfileNameSCF')
    analyst = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='analystSCF', null=True, blank=True)
    verifiedBy = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='verifiedBySCF', null=True, blank=True)
    year = models.PositiveIntegerField(choices=YEAR_CHOICES, default=CURRENT_YEAR)
    cashFromOperatingActivities= models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)
    cashFromInvestingActivities = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)
    cashFromFinancingActivities = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)
    netChangeInCash =  models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True) #netChangeInCash = cashFromOperatingActivities + cashFromInvestingActivities + cashFromFinancingActivities
    changesInWorkingCapital= models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)
    capitalExpenditures = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)
    freeCashFlow = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    
    def save(self):
        if self.cashFromOperatingActivities:
            cashFromOperatingAct = self.cashFromOperatingActivities
        else:
            cashFromOperatingAct = 0
        if self.cashFromInvestingActivities:
            cashFromInvestingAct = self.cashFromInvestingActivities
        else:
            cashFromInvestingAct = 0
        if self.cashFromFinancingActivities:
            cashFromFinancingAct = self.cashFromFinancingActivities
        else:
            cashFromFinancingAct = 0
        self.netChangeInCash = cashFromOperatingAct + cashFromInvestingAct + cashFromFinancingAct
        super(stockCashFlow, self).save()

    def __str__(self):
        return self.stockProfileName.stockName or '--Name not provided--'

    class Meta:
        verbose_name_plural = 'Stock Financial - Cashflow'


#Quarter starts for Cash Flow starts
class stockCashFlowTTM(models.Model):
    stockProfileName = models.ForeignKey(stockBasicDetail, on_delete=models.CASCADE, related_name='stockProfileNameSCFTTM')
    analyst = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='analystSCFTTM', null=True, blank=True)
    verifiedBy = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='verifiedBySCFTTM', null=True, blank=True)
    # year = models.PositiveIntegerField(choices=YEAR_CHOICES, default=CURRENT_YEAR)
    TTMDataFor = models.CharField(max_length=25, choices=TTM_CHOICES, default='quarter')
    cashFromOperatingActivities= models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)
    cashFromInvestingActivities = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)
    cashFromFinancingActivities = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)
    netChangeInCash =  models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True) #netChangeInCash = cashFromOperatingActivities + cashFromInvestingActivities + cashFromFinancingActivities
    changesInWorkingCapital= models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)
    capitalExpenditures = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)
    freeCashFlow = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    
    def save(self):
        if self.cashFromOperatingActivities:
            cashFromOperatingAct = self.cashFromOperatingActivities
        else:
            cashFromOperatingAct = 0
        if self.cashFromInvestingActivities:
            cashFromInvestingAct = self.cashFromInvestingActivities
        else:
            cashFromInvestingAct = 0
        if self.cashFromFinancingActivities:
            cashFromFinancingAct = self.cashFromFinancingActivities
        else:
            cashFromFinancingAct = 0
        self.netChangeInCash = cashFromOperatingAct + cashFromInvestingAct + cashFromFinancingAct
        super(stockCashFlowTTM, self).save()

    def __str__(self):
        return self.stockProfileName.stockName or '--Name not provided--'

    class Meta:
        verbose_name_plural = 'Stock Financial - Cashflow TTM'
# Quarter starts for Cash Flow ends 


class stockGrowth(models.Model):
    stockProfileName = models.OneToOneField(stockBasicDetail, on_delete=models.CASCADE, related_name='stockProfileNameSGrow')
    analyst = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='analystSGrow', null=True, blank=True)
    verifiedBy = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='verifiedBySGrow', null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    revenueGrowthDescription = models.TextField(null=True, blank=True)
    netProfitGrowthPATDescription = models.TextField(null=True, blank=True)
    EPSGrowthDescription = models.TextField(null=True, blank=True)
    bookValueGrowthDescription = models.TextField(null=True, blank=True)
    EBIDTAGrowthDescription = models.TextField(null=True, blank=True)
    operatingProfitGrowthDescription = models.TextField(null=True, blank=True)
    cashFlowFromOperationsDescription = models.TextField(null=True, blank=True)
    assestsGrowthDescription = models.TextField(null=True, blank=True)
    cashFlowFromFinancingDescription = models.TextField(null=True, blank=True)
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

    def __str__(self):
        return self.stockProfileName.stockName or '--Name not provided--'

    class Meta:
        verbose_name_plural = 'Stock Growth - Details'


class stockSolvency(models.Model):
    stockProfileName = models.OneToOneField(stockBasicDetail, on_delete=models.CASCADE, related_name='stockProfileNameSSol')
    analyst = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='analystSSol', null=True, blank=True)
    verifiedBy = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='verifiedBySSol', null=True, blank=True)
    solvencyDescription = models.TextField(null=True, blank=True)
    DERatioDescription = models.TextField(null=True, blank=True)
    currentRatioDescription = models.TextField(null=True, blank=True)
    quickRatioDescription = models.TextField(null=True, blank=True)
    interestCoverageRatioDescription = models.TextField(null=True, blank=True)
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')


    def __str__(self):
        return self.stockProfileName.stockName or '--Name not provided--'

    class Meta:
        verbose_name_plural = 'Stock Solvency - Details'


class stockOperatingEfficiency(models.Model):
    stockProfileName = models.OneToOneField(stockBasicDetail, on_delete=models.CASCADE, related_name='stockProfileNameSOEff')
    analyst = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='analystSOEff', null=True, blank=True)
    verifiedBy = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='verifiedBySOEff', null=True, blank=True)
    operatingEfficiencyDescription = models.TextField(null=True, blank=True)
    operatingProfitEBITMarginDescription = models.TextField(null=True, blank=True)
    PBTMarginDescription = models.TextField(null=True, blank=True)
    PATMarginDescription = models.TextField(null=True, blank=True)
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

    def __str__(self):
        return self.stockProfileName.stockName or '--Name not provided--'

    class Meta:
        verbose_name_plural = 'Stock Operating Effeciency - Details'


class stockRatios(models.Model):
    stockProfileName = models.OneToOneField(stockBasicDetail, on_delete=models.CASCADE, related_name='stockProfileNameSRatios')
    analyst = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='analystSRatios', null=True, blank=True)
    verifiedBy = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='verifiedBySRatios', null=True, blank=True)
    profitiabilityDescription = models.TextField(null=True, blank=True) 
    returnOnEquityDescription = models.TextField(null=True, blank=True)
    ROCEDescription = models.TextField(null=True, blank=True)
    returnOnAssestsDescription = models.TextField(null=True, blank=True)
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

    def __str__(self):
        return self.stockProfileName.stockName or '--Name not provided--'

    class Meta:
        verbose_name_plural = 'Stock Ratios - Details'

#
class stockPeers(models.Model):
    stockProfileName = models.OneToOneField(stockBasicDetail, on_delete=models.CASCADE, related_name='stockProfileNameSPeer')
    analyst = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='analystSPeer', null=True, blank=True)
    verifiedBy = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='verifiedBySPeer', null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    marketCapDescription = models.TextField(null=True, blank=True)
    revenueDescription = models.TextField(null=True, blank=True)
    pbDescription = models.TextField(null=True, blank=True)
    peDescription = models.TextField(null=True, blank=True)
    netProfitMarginDescription = models.TextField(null=True, blank=True)
    evByEbitdaDescription = models.TextField(null=True, blank=True)
    marketCapBySalesDescription = models.TextField(null=True, blank=True)
    assestTurnOverRatioDescription = models.TextField(null=True, blank=True)
    fixedAssetTurnoverRatioDescription = models.TextField(null=True, blank=True)
    ROEDescription = models.TextField(null=True, blank=True)
    ROCEDescription = models.TextField(null=True, blank=True)
    DebtToEquityDescription = models.TextField(null=True, blank=True)
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

    def __str__(self):
        return self.stockProfileName.stockName or '--Name not provided--'

    class Meta:
        verbose_name_plural = 'Stock Peers - Graph Descriptions'

#
class stockPeersDescriptionForBankNBFC(models.Model):
    stockProfileName = models.OneToOneField(stockBasicDetail, on_delete=models.CASCADE, related_name='stockProfileNameSPDForBNBFCPeer')
    analyst = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='analystSPDForBNBFCPeer', null=True, blank=True)
    verifiedBy = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='verifiedBySPDForBNBFCPeer', null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    carDescriptionDescription = models.TextField(null=True, blank=True)
    netNPADescription = models.TextField(null=True, blank=True)
    grossNPADescription = models.TextField(null=True, blank=True)
    CASADescription = models.TextField(null=True, blank=True)
    tier1Description = models.TextField(null=True, blank=True)
    tier2Description = models.TextField(null=True, blank=True)
    totalAMUDescription = models.TextField(null=True, blank=True)
    RORWADescription = models.TextField(null=True, blank=True)
    netInterestIncomeDescription = models.TextField(null=True, blank=True)
    revenueDescription = models.TextField(null=True, blank=True)
    roaDescription = models.TextField(null=True, blank=True)
    netProfitMarginDescription = models.TextField(null=True, blank=True)
    assetTurnOverRatioDescription = models.TextField(null=True, blank=True)
    roeDescription = models.TextField(null=True, blank=True)
    PEDescription = models.TextField(null=True, blank=True)
    PBDescription = models.TextField(null=True, blank=True)
    nimDescription = models.TextField(null=True, blank=True)
    debtToEquityRatioDescription = models.TextField(null=True, blank=True)
    pByTBDescription = models.TextField(null=True, blank=True)
    marketCapDescription = models.TextField(null=True, blank=True)
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

    def __str__(self):
        return self.stockProfileName.stockName or '--Name not provided--'

    class Meta:
        verbose_name_plural = 'Stock Peers - Bank NBFC Graph Descriptions'


class leadGenerationDetails(models.Model):
    IAM_OPTIONS = (
        ('Investor', 'Investor'),
        ('Partner', 'Partner'),
        ('Shareholder', 'Shareholder'),
        ('Institution', 'Institution'),
        ('Employee', 'Employee'),
    )
    IWANT_OPTIONS = (
        ('Buy-Share', 'Buy Share'),
        ('Sell-Share', 'Sell Share'),
        ('Others', 'Others'),
    )
    stockProfileName = models.ForeignKey(stockBasicDetail, on_delete=models.SET_NULL, related_name='stockProfileNameLGD',null=True, blank=True)
    name = models.CharField(max_length=1000, null=True, blank=True)
    emailID = models.EmailField(max_length=200, null=True, blank=True)
    phoneNo = models.BigIntegerField()
    location = models.CharField(max_length=1000, null=True, blank=True)
    iAm = models.CharField(max_length=15, choices=IAM_OPTIONS, null=True, blank=True)
    iWant = models.CharField(max_length=15, choices=IWANT_OPTIONS, null=True, blank=True)
    message = models.TextField(null=True, blank=True)
    agreedToTC = models.BooleanField(null=True, blank=True)
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    
    def __str__(self):
        return self.name or '--Name not provided--'
    
    class Meta:
        verbose_name_plural = 'Lead Generation - Details' 


class peersCompanyLinking(models.Model):
    STOCK_STATUS = (
        ('Listed', 'Listed'),
        ('Unlisted', 'Unlisted'),
    )
    stockProfileName = models.ForeignKey(stockBasicDetail, on_delete=models.CASCADE, related_name='stockProfileNamePCL')
    screenerLink = models.URLField(max_length=256, null=True, blank=True)
    stockStatus = models.CharField(max_length=10, choices=STOCK_STATUS, default='Unlisted')
    stockName = models.CharField(max_length=256, null=True, blank=True)
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

    def __str__(self):
        return f'{self.stockName} for {self.stockProfileName.stockName}' or '--Name not provided--'

    class Meta:
        verbose_name_plural = 'Peer - Company Linking'


class peersCompanyLinkingForBankNBFC(models.Model):
    STOCK_STATUS = (
        ('Listed', 'Listed'),
        ('Unlisted', 'Unlisted'),
    )
    stockProfileName = models.ForeignKey(stockBasicDetail, on_delete=models.CASCADE, related_name='stockProfileNamePCLFNBFC')
    screenerLink = models.URLField(max_length=256, null=True, blank=True)
    stockStatus = models.CharField(max_length=10, choices=STOCK_STATUS, default='Unlisted')
    stockName = models.CharField(max_length=256, null=True, blank=True)
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

    def __str__(self):
        return f'{self.stockName} for {self.stockProfileName.stockName}' or '--Name not provided--'

    class Meta:
        verbose_name_plural = 'Peer - Company Linking For Bank NBFC'


#
class peerLinkingYearlyData(models.Model):
    screenerCompany = models.ForeignKey(peersCompanyLinking, on_delete=models.CASCADE, related_name='stockProfileNamePLYD')
    year = models.PositiveIntegerField(choices=YEAR_CHOICES, default=CURRENT_YEAR)
    cashAndShortTermEquivalents = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)
    PreferenceEquity = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True, help_text='To be taken from "Value Research".')
    totalMinorityInterest = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True, help_text='To be taken from "Value Research".')
    longTermMarketableSecurities = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)
    bookValue = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)
    currentPrice = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)
    revenue = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True, help_text="for Unlisted Stock")
    netProfitMargin = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True, help_text="for Unlisted Stock")
    assetTurnoverRation = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True, help_text="for Unlisted Stock")
    totalFixedAssetTurnoverRatio = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True, help_text="for Unlisted Stock")
    ROE = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True, help_text="for Unlisted Stock")
    ROCE = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True, help_text="for Unlisted Stock")
    deptToEquity = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True, help_text="for Unlisted Stock")
    peRatio = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True, help_text="for Unlisted Stock")
    pbRatio = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True, help_text="for Unlisted Stock")
    marketCap = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True, help_text="for Unlisted Stock")
    marketCapBySales = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True, help_text="for Unlisted Stock")
    enterpriseValue = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True, help_text="for Unlisted Stock")
    evByEbitda = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True, help_text="for Unlisted Stock")
    cashAndShortTermCashEquivalents = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True, help_text="for Unlisted Stock")
    analyst = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='analystPLYD', null=True, blank=True)
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

    def __str__(self):
        return f'{self.screenerCompany.stockName} for Year: {self.year} and Company: {self.screenerCompany.stockProfileName.stockName}' or '--Name not provided--'

    class Meta:
        verbose_name_plural = 'Peer - Company Linking Year Wise Data'

#
class peerLinkingYearlyDataForBankNBFC(models.Model):
    screenerCompany = models.ForeignKey(peersCompanyLinkingForBankNBFC, on_delete=models.CASCADE, related_name='stockProfileNamePLYDFNBFC')
    year = models.PositiveIntegerField(choices=YEAR_CHOICES, default=CURRENT_YEAR)
    CAR = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)
    netNPA = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)
    grossNPA = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)
    CASA = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)
    tier1CapitalRatio = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)
    tier2CapitalRatio = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)
    totalAMU = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)
    RORWA = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)
    numberOfShares = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)
    intangibleAssests = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)
    goodwill = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)
    loanLossProvision = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)
    netInterestIncome = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True, help_text="for Unlisted Stock")
    revenue = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True, help_text="for Unlisted Stock")
    roa = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True, help_text="for Unlisted Stock")
    netProfitMargin = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True, help_text="for Unlisted Stock")
    assetTurnOverRatio = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True, help_text="for Unlisted Stock")
    ROE = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True, help_text="for Unlisted Stock")
    peRatio = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True, help_text="for Unlisted Stock")
    pbRatio = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True, help_text="for Unlisted Stock")
    marketCap = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True, help_text="for Unlisted Stock")
    NIM = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True, help_text="for Unlisted Stock")
    DERatio = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True, help_text="for Unlisted Stock")
    priceByTangibleBookRatio = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True, help_text="for Unlisted Stock")
    analyst = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='analystPLYDFNBFC', null=True, blank=True)
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

    def __str__(self):
        return f'{self.screenerCompany.stockName} for Year: {self.year} and Company: {self.screenerCompany.stockProfileName.stockName}' or '--Name not provided--'

    class Meta:
        verbose_name_plural = 'Peer - Company Linking Year Wise Data for Bank NBFC'


#
class sectorSpecificRatios(models.Model):
    stockProfileName = models.OneToOneField(stockBasicDetail, on_delete=models.CASCADE, related_name='stockProfileNameSSRJ')
    analyst = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='analystSSRJ', null=True, blank=True)
    verifiedBy = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='verifiedBySSRJ', null=True, blank=True)
    sectorSpecificRatiosDescription = models.TextField(null=True, blank=True)
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

    def __str__(self):
        return self.stockProfileName.stockName or '--Name not provided--'

    class Meta:
        verbose_name_plural = 'Stock Sector Specific Ratios - Details'

#
class iDescriptionForKeyRatios(models.Model):
    revenue = models.CharField(max_length=256,null=True, blank=True)
    net_profit_growth = models.CharField(max_length=256,null=True, blank=True)
    eps_growth = models.CharField(max_length=256,null=True, blank=True)
    book_value_growth = models.CharField(max_length=256,null=True, blank=True)
    EBITDA_growth = models.CharField(max_length=256,null=True, blank=True)
    operating_profit_growth = models.CharField(max_length=256,null=True, blank=True)
    asset_growth = models.CharField(max_length=256,null=True, blank=True)
    cash_flow_from_financing = models.CharField(max_length=256,null=True, blank=True)
    cash_flow_from_operations = models.CharField(max_length=256,null=True, blank=True)
    de_ratio = models.CharField(max_length=256,null=True, blank=True)
    current_ratio = models.CharField(max_length=256,null=True, blank=True)
    quick_ratio = models.CharField(max_length=256,null=True, blank=True)
    interest_coverage_ratio = models.CharField(max_length=256,null=True, blank=True)
    operating_profit_EBIT_margin = models.CharField(max_length=256,null=True, blank=True)
    profit_before_tax_margin = models.CharField(max_length=256,null=True, blank=True)
    profit_after_tax_margin = models.CharField(max_length=256,null=True, blank=True)
    return_on_equity = models.CharField(max_length=256,null=True, blank=True)
    return_on_capital_employed = models.CharField(max_length=256,null=True, blank=True)
    return_to_assets = models.CharField(max_length=256,null=True, blank=True)
    dividend_yield = models.CharField(max_length=256,null=True, blank=True)
    earning_yield = models.CharField(max_length=256,null=True, blank=True)
    tier_1_capital_ratio = models.CharField(max_length=256,null=True, blank=True)
    tier_2_capital_ratio = models.CharField(max_length=256,null=True, blank=True)
    tangible_book_value = models.CharField(max_length=256,null=True, blank=True)
    AUM = models.CharField(max_length=256,null=True, blank=True)
    AUM_growth = models.CharField(max_length=256,null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    analyst = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='analystIDFKR', null=True, blank=True)
    verifiedBy = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='verifiedByIDFKR', null=True, blank=True)

    def __str__(self):
        return f'Created by: {str(self.analyst)} on {self.created}' or '--Name not provided--'

    class Meta:
        verbose_name_plural = 'Key Ratio - i Description for Graphs'

#
class industrySpecificGraphs(models.Model):
    GRAPH_TYPE = (
        ('Value', 'Value'),
        ('Percentage', 'Percentage'),
    )
    stockProfileName = models.ForeignKey(stockBasicDetail, on_delete=models.CASCADE, related_name='stockProfileNameISG')
    graphFor = models.CharField(max_length=256)
    graphType = models.CharField(max_length=12, choices=GRAPH_TYPE, default='Value')
    graphDescription = models.TextField(null=True, blank=True)
    iDescription = models.CharField(max_length=256,null=True, blank=True)
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    analyst = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='analystISG', null=True, blank=True)
    verifiedBy = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='verifiedByISG', null=True, blank=True)

    def __str__(self):
        return 'Stock Name: %s, Graph: %s' % (self.stockProfileName.stockName, self.graphFor) or '--Name not provided--'

    class Meta:
        verbose_name_plural = 'Key Ratio - Industry Specific Graph'


class industrySpecificGraphsValues(models.Model):
    valuesFor = models.ForeignKey(industrySpecificGraphs, on_delete=models.CASCADE, related_name='valuesForISGV')
    year = models.PositiveIntegerField(choices=YEAR_CHOICES, default=CURRENT_YEAR)
    value = models.DecimalField(max_digits=1000, decimal_places=2)
    analyst = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='analystISGV', null=True, blank=True)

    def __str__(self):
        return 'Graph: %s, Year: %s' % (self.valuesFor.graphFor, self.year) or '--Name not provided--'

    class Meta:
        verbose_name_plural = 'Key Ratio - Industry Specific Graph Values'



class foundingRoundsFigureUnits(models.Model):
    stockProfileName = models.OneToOneField(stockBasicDetail, on_delete=models.CASCADE, related_name='JstockProfileNameFFU')
    analyst = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='JanalystFFU', null=True, blank=True)
    verifiedBy = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='JverifiedByFFU', null=True, blank=True)
    fundingUnitNumbers = models.CharField(max_length=10, choices=DATA_IN, default='Cr', null=True,blank=True)
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

    def __str__(self):
        return 'Stock Name: %s' % (self.stockProfileName.stockName) or '--Name not provided--'

    class Meta:
        verbose_name_plural = 'Funding Units Numbers - Data Units(cr/lakh.. etc)'


#description field for SEO - starts 

class stockFinBalanceSheetSEO(models.Model):
    stockProfileName = models.OneToOneField(stockBasicDetail, on_delete=models.CASCADE, related_name='stockProfileNameSFinancialsSEO')
    analyst = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='analystFinancialsSEO', null=True, blank=True)
    verifiedBy = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='verifiedByFinancialsSEO', null=True, blank=True)
    balanceSheetDescriptionSEO = models.TextField(null=True, blank=True)
    profitAndLossDescriptionSEO = models.TextField(null=True, blank=True)
    cashFlowDescriptionSEO = models.TextField(null=True, blank=True)
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

    def __str__(self):
        return self.stockProfileName.stockName or '--Name not provided--'

    class Meta:
        verbose_name_plural = 'Stock Financial SEO - Description'

class stockNewsSEO(models.Model):
    stockProfileName = models.OneToOneField(stockBasicDetail, on_delete=models.CASCADE, related_name='stockProfileNameStockNewsSEO')
    analyst = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='analystStockNewsSEO', null=True, blank=True)
    verifiedBy = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='verifiedByStockNewsSEO', null=True, blank=True)
    newsDescriptionSEO = models.TextField(null=True, blank=True)
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

    def __str__(self):
        return self.stockProfileName.stockName or '--Name not provided--'

    class Meta:
        verbose_name_plural = 'Stock News SEO - Description'

class stockEventsSEO(models.Model):
    stockProfileName = models.OneToOneField(stockBasicDetail, on_delete=models.CASCADE, related_name='stockProfileNameStockEventsSEO')
    analyst = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='analystStockEventsSEO', null=True, blank=True)
    verifiedBy = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='verifiedByStockEventsSEO', null=True, blank=True)
    eventsDescriptionSEO = models.TextField(null=True, blank=True)
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

    def __str__(self):
        return self.stockProfileName.stockName or '--Name not provided--'

    class Meta:
        verbose_name_plural = 'Stock Events SEO - Description'

#description field for SEO -  ends 

class stockBalanceSheetBankNBFC(models.Model):
    stockProfileName = models.ForeignKey(stockBasicDetail, on_delete=models.CASCADE, related_name='stockProfileNameSBSBank')
    analyst = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='analystSBSBank', null=True, blank=True)
    verifiedBy = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='verifiedBySBSBank', null=True, blank=True)
    year = models.PositiveIntegerField(choices=YEAR_CHOICES, default=CURRENT_YEAR)
    cashAndCashEquivalents = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)
    longTermInvestments = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)
    loans = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)
    otherReceivables = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)
    otherCurrentAssets = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)
    totalInventory = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)
    financialAssets = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)
    fixedAssests = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)
    rightOfUseAsset = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)
    goodWillOnConsolidation = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)
    nonCurrentInvestments = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)
    deferredCharges = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)
    deferredTaxAssets = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)
    otherNonCurrentAssets = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)
    nonFinancialAssets = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)
    totalAssets = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)
    equityShareCapital = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)
    reservesAndSurplus = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)
    minorityInterest = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)
    shareApplicationMoneyPendingAllotment = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)
    otherEquity = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)
    totalEquity = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)
    deposits = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)
    longTermBorrowings = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)
    deferredTaxLiabilities = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)
    otherFinancialLiabilities = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)
    otherNonFinancialLiabilities = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)
    shortTermProvisions = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)
    longTermProvisions = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)
    shortTermBorrowings = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)
    tradePayable = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)
    leaseLiability = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)
    otherNonCurrentLiabilities = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)
    otherCurrentLiabilities = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)
    currentPortionOfLongTermDebt = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)
    totalLiabilities = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)
    totalLiabilitiesAndShareHoldingEquity = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)
    totalCommonSharesOutstanding = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)
    tier1CapitalRatio = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)
    tier2CapitalRatio = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)
    tangibleBookValue = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)
    aum = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)
    aumGrowth = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

    def save(self):
        if self.cashAndCashEquivalents:
            cashAndCashEq = self.cashAndCashEquivalents
        else:
            cashAndCashEq = 0
        if self.longTermInvestments:
            longTermInv = self.longTermInvestments
        else:
            longTermInv = 0
        if self.loans:
            loan = self.loans
        else:
            loan = 0
        if self.otherReceivables:
            totalRecv = self.otherReceivables
        else:
            totalRecv = 0
        if self.otherCurrentAssets:
            otherCurrAssets = self.otherCurrentAssets
        else:
            otherCurrAssets = 0

        if self.totalInventory:
            totInventory = self.totalInventory
        else:
            totInventory = 0

        self.financialAssets = cashAndCashEq + longTermInv + loan + totalRecv + otherCurrAssets + totInventory

        if self.fixedAssests:
            fixAssests = self.fixedAssests
        else:
            fixAssests = 0
        if self.rightOfUseAsset:
            rightUseAsset = self.rightOfUseAsset
        else:
            rightUseAsset = 0
        if self.goodWillOnConsolidation:
            goodWillOnCons = self.goodWillOnConsolidation
        else:
            goodWillOnCons = 0
        if self.nonCurrentInvestments:
            nonCurrInvestments = self.nonCurrentInvestments
        else:
            nonCurrInvestments = 0
        if self.deferredCharges:
            defCharges = self.deferredCharges
        else:
            defCharges = 0
        if self.deferredTaxAssets:
            defTaxAssets = self.deferredTaxAssets
        else:
            defTaxAssets = 0
        if self.otherNonCurrentAssets:
            otherNonCurrAssets = self.otherNonCurrentAssets
        else:
            otherNonCurrAssets = 0
        self.nonFinancialAssets = fixAssests + rightUseAsset + goodWillOnCons + nonCurrInvestments + defCharges + defTaxAssets + otherNonCurrAssets

        self.totalAssets = self.financialAssets + self.nonFinancialAssets


        if self.equityShareCapital:
            equityShareCap = self.equityShareCapital
        else:
            equityShareCap = 0
        if self.reservesAndSurplus:
            reservAndSurpl = self.reservesAndSurplus
        else:
            reservAndSurpl = 0
        if self.minorityInterest:
            minorityInt = self.minorityInterest
        else:
            minorityInt = 0
        if self.shareApplicationMoneyPendingAllotment:
            shareAppMoneyPendgAll = self.shareApplicationMoneyPendingAllotment
        else:
            shareAppMoneyPendgAll = 0
        if self.otherEquity:
            othrEquity = self.otherEquity
        else:
            othrEquity = 0
        
        self.totalEquity = equityShareCap + reservAndSurpl + minorityInt + shareAppMoneyPendgAll + othrEquity

        if self.deposits:
            deposit = self.deposits
        else:
            deposit = 0

        if self.longTermBorrowings:
            longTermBor = self.longTermBorrowings
        else:
            longTermBor = 0

        if self.deferredTaxLiabilities:
            defTaxLiab = self.deferredTaxLiabilities
        else:
            defTaxLiab = 0
        if self.otherFinancialLiabilities:
            otherFinLiab = self.otherFinancialLiabilities
        else:
            otherFinLiab = 0
        if self.otherNonFinancialLiabilities:
            otherNonFinLiab = self.otherNonFinancialLiabilities
        else:
            otherNonFinLiab = 0
        if self.shortTermProvisions:
            shortTermProv = self.shortTermProvisions
        else:
            shortTermProv = 0
        if self.longTermProvisions:
            longTermProv = self.longTermProvisions
        else:
            longTermProv = 0
        if self.shortTermBorrowings:
            shortTermBorrwngs = self.shortTermBorrowings
        else:
            shortTermBorrwngs = 0
        if self.tradePayable:
            tradePay = self.tradePayable
        else:
            tradePay = 0
        if self.leaseLiability:
            leaseLiab = self.leaseLiability
        else:
            leaseLiab = 0
        if self.otherNonCurrentLiabilities:
            otherNonCurrentLiab = self.otherNonCurrentLiabilities
        else:
            otherNonCurrentLiab = 0
        if self.otherCurrentLiabilities:
            otherCurrentLiab = self.otherCurrentLiabilities
        else:
            otherCurrentLiab = 0
        if self.currentPortionOfLongTermDebt:
            currentPortnOfLngTrmDebt = self.currentPortionOfLongTermDebt
        else:
            currentPortnOfLngTrmDebt = 0

        self.totalLiabilities = deposit + longTermBor + defTaxLiab + otherFinLiab + otherNonFinLiab + shortTermProv + longTermProv + shortTermBorrwngs + tradePay + leaseLiab + otherNonCurrentLiab + otherCurrentLiab + currentPortnOfLngTrmDebt

        # if self.totalLiabilitiesAndShareHoldingEquity:
        # 	totLiabAndShareHoldingEqty = self.totalLiabilitiesAndShareHoldingEquity
        # else:
        # 	totLiabAndShareHoldingEqty = 0
        self.totalLiabilitiesAndShareHoldingEquity = self.totalLiabilities + self.totalEquity

        if self.totalCommonSharesOutstanding:
            totCommonSharesOuts = self.totalCommonSharesOutstanding
        else:
            totCommonSharesOuts = 0
        # if (self.totalAssets - self.totalLiabilitiesAndShareHoldingEquity) == 0:
        super(stockBalanceSheetBankNBFC, self).save()
        # else:
        # 	raise ValueError('Total Liabilities and Sharehold’s Equity - Total Asset should be Zero')

    def __str__(self):
        return 'Stock Name: %s, Year: %s' % (self.stockProfileName.stockName, self.year) or '--Name not provided--'

    class Meta:
        verbose_name_plural = 'Stock Financial - Balance Sheet For Bank & NBFCs'


class stockProfitAndLossBankNBFC(models.Model):
    stockProfileName = models.ForeignKey(stockBasicDetail, on_delete=models.CASCADE, related_name='stockProfileNameSBSProfitLoss')
    analyst = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='analystProfitAndLoss', null=True, blank=True)
    verifiedBy = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='verifiedProfitAndLoss', null=True, blank=True)
    year = models.PositiveIntegerField(choices=YEAR_CHOICES, default=CURRENT_YEAR)
    netInterestIncome = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)
    totalRevenue = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)
    cogsMinusRepairsMaintenance = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)
    grossProfit = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)
    salariesAndEmpBenefits = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)
    cospMinusAdvertisingPlusRent = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)
    otherOperatingExp = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)
    ebidta = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)
    depreciationAndAmortization = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)
    pbit = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)
    otherItems = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)
    shareOfProfitLossOfJoinVentures = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)
    pbt = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)
    taxesAndOtherItems = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)
    netIncome = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)
    dilutedEPS = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)
    basicEPS = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)
    DPS = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True) 
    payoutRatio = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')


    def save(self):

        if self.netInterestIncome:
            netIntIncome = self.netInterestIncome
        else:
            netIntIncome = 0

        if self.totalRevenue:
            totRevenue = self.totalRevenue
        else:
            totRevenue = 0
        if self.cogsMinusRepairsMaintenance:
            cogsMinusRepairsMaint = self.cogsMinusRepairsMaintenance
        else:
            cogsMinusRepairsMaint = 0
        self.grossProfit = totRevenue - cogsMinusRepairsMaint

        if self.salariesAndEmpBenefits:
            salariesEmpBenefits = self.salariesAndEmpBenefits
        else:
            salariesEmpBenefits = 0
        if self.cospMinusAdvertisingPlusRent:
            cospMinusAdvrtsngPlusRent = self.cospMinusAdvertisingPlusRent
        else:
            cospMinusAdvrtsngPlusRent = 0
        if self.otherOperatingExp:
            otherOpertgExp = self.otherOperatingExp
        else:
            otherOpertgExp = 0

        self.ebidta = self.grossProfit - salariesEmpBenefits - cospMinusAdvrtsngPlusRent - otherOpertgExp

        if self.depreciationAndAmortization:
            depreciationAndAmor = self.depreciationAndAmortization
        else:
            depreciationAndAmor = 0

        self.pbit = self.ebidta - depreciationAndAmor

        if self.otherItems:
            otherItem = self.otherItems
        else:
            otherItem = 0
        if self.shareOfProfitLossOfJoinVentures:
            shareOfPLOfJoinVentures = self.shareOfProfitLossOfJoinVentures
        else:
            shareOfPLOfJoinVentures = 0

        self.pbt = self.pbit + otherItem - shareOfPLOfJoinVentures

        if self.taxesAndOtherItems:
            taxesOtherItems = self.taxesAndOtherItems
        else:
            taxesOtherItems = 0
        
        self.netIncome = self.pbt - taxesOtherItems

        if self.dilutedEPS:
            dilEPS = self.dilutedEPS
        else:
            dilEPS = 0

        if self.basicEPS:
            bascEPS = self.basicEPS
        else:
            bascEPS = 1

        if self.DPS:
            dPs = self.DPS
        else:
            dPs = 0
            
        # if self.payoutRatio:
        # 	payoutRtio = self.payoutRatio
        # else:
        # 	payoutRtio = 0

        self.payoutRatio = dPs / bascEPS

        super(stockProfitAndLossBankNBFC, self).save()

    def __str__(self):
        return 'Stock Name: %s, Year: %s' % (self.stockProfileName.stockName, self.year) or '--Name not provided--'

    class Meta:
        verbose_name_plural = 'Stock Financial - Profit And Loss For Bank & NBFCs'


class valuationRatio(models.Model):
    stockProfileName = models.OneToOneField(stockBasicDetail, on_delete=models.CASCADE, related_name='stockProfileNameVR')
    valuationRatioDescription = models.TextField(null=True, blank=True)
    valuationRatioDividendYield = models.TextField(null=True, blank=True)
    valuationRatioEarningYield = models.TextField(null=True, blank=True)
    author = models.CharField(max_length=100, null=True, blank=True)
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    

    def __str__(self):
        return '--Name not provided'

    class Meta:
        verbose_name_plural = 'Valuation Ratio'



class bankNBFCRatioDescription(models.Model):
    stockProfileName = models.OneToOneField(stockBasicDetail, on_delete=models.CASCADE, related_name='stockProfileNameBNBFCD')
    tier1CapitalRatio = models.TextField(null=True, blank=True)
    tier2CapitalRatio = models.TextField(null=True, blank=True)
    tangibleBookValue = models.TextField(null=True, blank=True)
    aum = models.TextField(null=True, blank=True)
    aumGrowth = models.TextField(null=True, blank=True)

    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    

    def __str__(self):
        return '--Name not provided'

    class Meta:
        verbose_name_plural = 'Valuation Ratio'



class stockBalanceSheetBankNBFCTTM(models.Model):
    stockProfileName = models.OneToOneField(stockBasicDetail, on_delete=models.CASCADE, related_name='stockProfileNameSBSBankTTM')
    analyst = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='analystSBSBankTTM', null=True, blank=True)
    verifiedBy = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='verifiedBySBSBankTTM', null=True, blank=True)
    TTMDataFor = models.CharField(max_length=25, choices=TTM_CHOICES, default='quarter')
    year = models.PositiveIntegerField(choices=YEAR_CHOICES, default=CURRENT_YEAR)
    cashAndCashEquivalents = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)
    longTermInvestments = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)
    loans = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)
    otherReceivables = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)
    otherCurrentAssets = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)
    totalInventory = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)
    financialAssets = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)
    fixedAssests = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)
    rightOfUseAsset = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)
    goodWillOnConsolidation = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)
    nonCurrentInvestments = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)
    deferredCharges = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)
    deferredTaxAssets = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)
    otherNonCurrentAssets = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)
    nonFinancialAssets = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)
    totalAssets = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)
    equityShareCapital = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)
    reservesAndSurplus = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)
    minorityInterest = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)
    shareApplicationMoneyPendingAllotment = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)
    otherEquity = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)
    totalEquity = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)
    deposits = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)
    longTermBorrowings = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)
    deferredTaxLiabilities = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)
    otherFinancialLiabilities = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)
    otherNonFinancialLiabilities = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)
    shortTermProvisions = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)
    longTermProvisions = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)
    shortTermBorrowings = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)
    tradePayable = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)
    leaseLiability = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)
    otherNonCurrentLiabilities = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)
    otherCurrentLiabilities = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)
    currentPortionOfLongTermDebt = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)
    totalLiabilities = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)
    totalLiabilitiesAndShareHoldingEquity = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)
    totalCommonSharesOutstanding = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)
    tier1CapitalRatio = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)
    tier2CapitalRatio = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)
    tangibleBookValue = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)
    aum = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)
    aumGrowth = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

    def save(self):
        if self.cashAndCashEquivalents:
            cashAndCashEq = self.cashAndCashEquivalents
        else:
            cashAndCashEq = 0
        if self.longTermInvestments:
            longTermInv = self.longTermInvestments
        else:
            longTermInv = 0
        if self.loans:
            loan = self.loans
        else:
            loan = 0
        if self.otherReceivables:
            totalRecv = self.otherReceivables
        else:
            totalRecv = 0
        if self.otherCurrentAssets:
            otherCurrAssets = self.otherCurrentAssets
        else:
            otherCurrAssets = 0

        if self.totalInventory:
            totInventory = self.totalInventory
        else:
            totInventory = 0

        self.financialAssets = cashAndCashEq + longTermInv + loan + totalRecv + otherCurrAssets + totInventory

        if self.fixedAssests:
            fixAssests = self.fixedAssests
        else:
            fixAssests = 0
        if self.rightOfUseAsset:
            rightUseAsset = self.rightOfUseAsset
        else:
            rightUseAsset = 0
        if self.goodWillOnConsolidation:
            goodWillOnCons = self.goodWillOnConsolidation
        else:
            goodWillOnCons = 0
        if self.nonCurrentInvestments:
            nonCurrInvestments = self.nonCurrentInvestments
        else:
            nonCurrInvestments = 0
        if self.deferredCharges:
            defCharges = self.deferredCharges
        else:
            defCharges = 0
        if self.deferredTaxAssets:
            defTaxAssets = self.deferredTaxAssets
        else:
            defTaxAssets = 0
        if self.otherNonCurrentAssets:
            otherNonCurrAssets = self.otherNonCurrentAssets
        else:
            otherNonCurrAssets = 0
        self.nonFinancialAssets = fixAssests + rightUseAsset + goodWillOnCons + nonCurrInvestments + defCharges + defTaxAssets + otherNonCurrAssets

        self.totalAssets = self.financialAssets + self.nonFinancialAssets


        if self.equityShareCapital:
            equityShareCap = self.equityShareCapital
        else:
            equityShareCap = 0
        if self.reservesAndSurplus:
            reservAndSurpl = self.reservesAndSurplus
        else:
            reservAndSurpl = 0
        if self.minorityInterest:
            minorityInt = self.minorityInterest
        else:
            minorityInt = 0
        if self.shareApplicationMoneyPendingAllotment:
            shareAppMoneyPendgAll = self.shareApplicationMoneyPendingAllotment
        else:
            shareAppMoneyPendgAll = 0
        if self.otherEquity:
            othrEquity = self.otherEquity
        else:
            othrEquity = 0
        
        self.totalEquity = equityShareCap + reservAndSurpl + minorityInt + shareAppMoneyPendgAll + othrEquity

        if self.deposits:
            deposit = self.deposits
        else:
            deposit = 0

        if self.longTermBorrowings:
            longTermBor = self.longTermBorrowings
        else:
            longTermBor = 0

        if self.deferredTaxLiabilities:
            defTaxLiab = self.deferredTaxLiabilities
        else:
            defTaxLiab = 0
        if self.otherFinancialLiabilities:
            otherFinLiab = self.otherFinancialLiabilities
        else:
            otherFinLiab = 0
        if self.otherNonFinancialLiabilities:
            otherNonFinLiab = self.otherNonFinancialLiabilities
        else:
            otherNonFinLiab = 0
        if self.shortTermProvisions:
            shortTermProv = self.shortTermProvisions
        else:
            shortTermProv = 0
        if self.longTermProvisions:
            longTermProv = self.longTermProvisions
        else:
            longTermProv = 0
        if self.shortTermBorrowings:
            shortTermBorrwngs = self.shortTermBorrowings
        else:
            shortTermBorrwngs = 0
        if self.tradePayable:
            tradePay = self.tradePayable
        else:
            tradePay = 0
        if self.leaseLiability:
            leaseLiab = self.leaseLiability
        else:
            leaseLiab = 0
        if self.otherNonCurrentLiabilities:
            otherNonCurrentLiab = self.otherNonCurrentLiabilities
        else:
            otherNonCurrentLiab = 0
        if self.otherCurrentLiabilities:
            otherCurrentLiab = self.otherCurrentLiabilities
        else:
            otherCurrentLiab = 0
        if self.currentPortionOfLongTermDebt:
            currentPortnOfLngTrmDebt = self.currentPortionOfLongTermDebt
        else:
            currentPortnOfLngTrmDebt = 0

        self.totalLiabilities = deposit + longTermBor + defTaxLiab + otherFinLiab + otherNonFinLiab + shortTermProv + longTermProv + shortTermBorrwngs + tradePay + leaseLiab + otherNonCurrentLiab + otherCurrentLiab + currentPortnOfLngTrmDebt

        # if self.totalLiabilitiesAndShareHoldingEquity:
        # 	totLiabAndShareHoldingEqty = self.totalLiabilitiesAndShareHoldingEquity
        # else:
        # 	totLiabAndShareHoldingEqty = 0
        self.totalLiabilitiesAndShareHoldingEquity = self.totalLiabilities + self.totalEquity

        if self.totalCommonSharesOutstanding:
            totCommonSharesOuts = self.totalCommonSharesOutstanding
        else:
            totCommonSharesOuts = 0
        # if (self.totalAssets - self.totalLiabilitiesAndShareHoldingEquity) == 0:
        super(stockBalanceSheetBankNBFCTTM, self).save()
        # else:
        # 	raise ValueError('Total Liabilities and Sharehold’s Equity - Total Asset should be Zero')

    def __str__(self):
        return 'Stock Name: %s, Year: %s' % (self.stockProfileName.stockName, self.year) or '--Name not provided--'

    class Meta:
        verbose_name_plural = 'Stock Financial - Balance Sheet For Bank & NBFCs TTM'


class stockProfitAndLossBankNBFCTTM(models.Model):
    stockProfileName = models.OneToOneField(stockBasicDetail, on_delete=models.CASCADE, related_name='stockProfileNameSBSProfitLossTTM')
    analyst = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='analystProfitAndLossTTM', null=True, blank=True)
    verifiedBy = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='verifiedProfitAndLossTTM', null=True, blank=True)
    TTMDataFor = models.CharField(max_length=25, choices=TTM_CHOICES, default='quarter')
    year = models.PositiveIntegerField(choices=YEAR_CHOICES, default=CURRENT_YEAR)
    netInterestIncome = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)
    totalRevenue = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)
    cogsMinusRepairsMaintenance = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)
    grossProfit = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)
    salariesAndEmpBenefits = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)
    cospMinusAdvertisingPlusRent = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)
    otherOperatingExp = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)
    ebidta = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)
    depreciationAndAmortization = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)
    pbit = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)
    otherItems = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)
    shareOfProfitLossOfJoinVentures = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)
    pbt = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)
    taxesAndOtherItems = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)
    netIncome = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)
    dilutedEPS = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)
    basicEPS = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)
    DPS = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True) 
    payoutRatio = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')


    def save(self):

        if self.netInterestIncome:
            netIntIncome = self.netInterestIncome
        else:
            netIntIncome = 0

        if self.totalRevenue:
            totRevenue = self.totalRevenue
        else:
            totRevenue = 0
        if self.cogsMinusRepairsMaintenance:
            cogsMinusRepairsMaint = self.cogsMinusRepairsMaintenance
        else:
            cogsMinusRepairsMaint = 0
        self.grossProfit = totRevenue - cogsMinusRepairsMaint

        if self.salariesAndEmpBenefits:
            salariesEmpBenefits = self.salariesAndEmpBenefits
        else:
            salariesEmpBenefits = 0
        if self.cospMinusAdvertisingPlusRent:
            cospMinusAdvrtsngPlusRent = self.cospMinusAdvertisingPlusRent
        else:
            cospMinusAdvrtsngPlusRent = 0
        if self.otherOperatingExp:
            otherOpertgExp = self.otherOperatingExp
        else:
            otherOpertgExp = 0

        self.ebidta = self.grossProfit - salariesEmpBenefits - cospMinusAdvrtsngPlusRent - otherOpertgExp

        if self.depreciationAndAmortization:
            depreciationAndAmor = self.depreciationAndAmortization
        else:
            depreciationAndAmor = 0

        self.pbit = self.ebidta - depreciationAndAmor

        if self.otherItems:
            otherItem = self.otherItems
        else:
            otherItem = 0
        if self.shareOfProfitLossOfJoinVentures:
            shareOfPLOfJoinVentures = self.shareOfProfitLossOfJoinVentures
        else:
            shareOfPLOfJoinVentures = 0

        self.pbt = self.pbit + otherItem - shareOfPLOfJoinVentures

        if self.taxesAndOtherItems:
            taxesOtherItems = self.taxesAndOtherItems
        else:
            taxesOtherItems = 0
        
        self.netIncome = self.pbt - taxesOtherItems

        if self.dilutedEPS:
            dilEPS = self.dilutedEPS
        else:
            dilEPS = 0

        if self.basicEPS:
            bascEPS = self.basicEPS
        else:
            bascEPS = 1

        if self.DPS:
            dPs = self.DPS
        else:
            dPs = 0
            
        # if self.payoutRatio:
        # 	payoutRtio = self.payoutRatio
        # else:
        # 	payoutRtio = 0

        self.payoutRatio = dPs / bascEPS

        super(stockProfitAndLossBankNBFCTTM, self).save()

    def __str__(self):
        return 'Stock Name: %s, Year: %s' % (self.stockProfileName.stockName, self.year) or '--Name not provided--'

    class Meta:
        verbose_name_plural = 'Stock Financial - Profit And Loss For Bank & NBFCs TTM'


#
class researchReportFAQs(models.Model):
    stockProfileName = models.ForeignKey(stockBasicDetail, on_delete=models.CASCADE, related_name='stockProfileNameRRF')
    questions = models.TextField(null=True, blank=True, help_text="Add 'stock_name_auto' to automatically add the Research Report name.")
    answers = models.TextField(null=True, blank=True, help_text="Add 'stock_name_auto' to automatically add the Research Report name.")
    author = models.CharField(max_length=1000, null=True, blank=True)
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

    def __str__(self):
        return f'Question: {self.questions} for Stock {self.stockProfileName.stockName}' 

    class Meta:
        verbose_name_plural = 'Research Report Specific FAQs'

#
class commonFAQ(models.Model):
    questions = models.TextField(null=True, blank=True, help_text="Add 'stock_name_auto' to automatically add the Research Report name.")
    answers = models.TextField(null=True, blank=True, help_text="Add 'stock_name_auto' to automatically add the Research Report name.")
    author = models.CharField(max_length=100, null=True, blank=True)
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    
    def __str__(self):
        return '--Name not provided'

    class Meta:
            verbose_name_plural = 'Common FAQ'


#
class valuesRBIStandards(models.Model):
    year = models.PositiveIntegerField(choices=YEAR_CHOICES, default=CURRENT_YEAR)
    RBI_CARValue = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)
    RBI_tier1Value = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)
    RBI_tier2Value = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)
    RBI_maintenanceMarginRequirement = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    
    def __str__(self):
        return f'RBI Values for Year: {self.year}' or '--Name not provided'

    class Meta:
        verbose_name_plural = 'Company Values RBI Standards'

#
class companyRatios(models.Model):
    stockProfileName = models.ForeignKey(stockBasicDetail, on_delete=models.CASCADE, related_name='stockProfileNameCR')
    year = models.PositiveIntegerField(choices=YEAR_CHOICES, default=CURRENT_YEAR)
    carValue = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)
    tier1Value = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)
    tier2Value = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)
    maintenanceMarginRequirement = models.DecimalField(max_digits=1000, decimal_places=20, null=True, blank=True)
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    

    def __str__(self):
        return f'For Stock: {self.stockProfileName.stockName}, Year: {self.year}' or '--Name not provided'

    class Meta:
        verbose_name_plural = 'Company Values Self With RBI Standards'

#
class totalShareYearlyData(models.Model):
    stockProfileName = models.ForeignKey(stockBasicDetail, on_delete=models.CASCADE, related_name='stockProfileNameTSYD')
    shareType = models.CharField(max_length=100, choices=SHARE_CHOICES, default='financial_year')
    year = models.IntegerField(null=True, blank=True)
    totalShares = models.DecimalField(max_digits=100, decimal_places=20, null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

    def __str__(self):
        return f'Stock: {self.stockProfileName.stockName}, Year: {self.year}, Shares: {self.totalShares}' or '---name not provided----'

    class Meta:
        verbose_name_plural = 'Total Share Yearly Data(for snapshot)'


#
class regulatoryRatios(models.Model):
    stockProfileName = models.OneToOneField('stockBasicDetail', on_delete=models.CASCADE, related_name='regulatoryRatiosTitle')
    mainDescription = models.TextField(null=True, blank=True)
    carDescription = models.TextField(null=True, blank=True)
    tier1Description = models.TextField(null=True, blank=True)
    tier2Description = models.TextField(null=True, blank=True)
    maintainanceMarginRequirementDescription = models.TextField(null=True, blank=True)
    author = models.CharField(max_length=100, null=True, blank=True)
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

    def __str__(self):
        return self.metaTitle or '--Name not provided' 

    class Meta:
        verbose_name_plural = 'Regulatory Ratios'



class campaign(models.Model):
    stockProfileName = models.ForeignKey(stockBasicDetail, on_delete=models.CASCADE,
                                            related_name='stockProfileNameCampaign')
    campaign_description = models.TextField(null=True, blank=True, default="")
    updatedAt = models.DateTimeField(auto_now=True)
    startDate = models.DateTimeField(editable=True)
    endDate = models.DateTimeField(editable=True)
    isActive = models.BooleanField(default=True)
    

    class Meta:
        verbose_name_plural = "campaign"

    def __str__(self):
        return self.stockProfileName.stockName or '--Name not provided--'








