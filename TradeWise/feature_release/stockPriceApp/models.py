from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from stockApp.models import stockBasicDetail

STATUS_CHOICES = (
	('draft', 'Draft'),
	('published', 'Published'),
)

IS_SHARES_AVAILABLE = (
	('Available', 'Available'),
	('Not Available', 'Not Available')
)

#
class stockDailyUpdates(models.Model):
	stockProfile = models.ForeignKey(stockBasicDetail, on_delete=models.CASCADE, related_name='stockNameSDUp', null=True, blank=True)
	price =  models.DecimalField(max_digits=1000, decimal_places=2, null=True, blank=True)
	minLotSize = models.BigIntegerField(null=True,blank=True)
	ratings = models.CharField(max_length=1000,null=True,blank=True)
	available = models.CharField(max_length=1000,null=True,blank=True, choices=IS_SHARES_AVAILABLE, default='Available')
	author = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='authorSDUp', null=True, blank=True)
	publish = models.DateTimeField(default=timezone.now)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)

	def __str__(self):
		return f'Stock: {self.stockProfile.stockName} is having Price: {self.price} on {self.publish}'

	class Meta:
		verbose_name_plural = 'Pre IPO Stock Daily Updates Data'