from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import datetime
from stockApp.models import stockBasicDetail

#
STATUS_CHOICES = (
	('Draft', 'Draft'),
	('Published', 'Published'),
)

#
class excel_utility(models.Model):
	mobile = models.BigIntegerField(null=True, blank=True)
	email = models.EmailField(max_length=256, null=True, blank=True)
	pan = models.CharField(max_length=10, null=True, blank=True)
	adv_date = models.DateField(default=datetime.date.today, null=True, blank=True)
	full_payment_date = models.DateField(default=datetime.date.today, null=True, blank=True)
	trf_date = models.DateField(default=datetime.date.today, null=True, blank=True)
	pre_ipo_stock = models.ForeignKey(stockBasicDetail, on_delete=models.CASCADE, related_name='pre_ipo_stockEU', null=True, blank=True)
	quantity = models.DecimalField(max_digits=1000, decimal_places=2, null=True, blank=True)
	price = models.DecimalField(max_digits=1000, decimal_places=2, null=True, blank=True)
	final_amount = models.DecimalField(max_digits=1000, decimal_places=2, null=True, blank=True)
	tds = models.DecimalField(max_digits=1000, decimal_places=2, null=True, blank=True)
	amount_in_bank = models.DecimalField(max_digits=1000, decimal_places=2, null=True, blank=True)
	acc_no = models.CharField(max_length=50, null=True, blank=True)
	bank_name = models.CharField(max_length=256, null=True, blank=True)
	reference_number = models.CharField(max_length=256, null=True, blank=True)
	owned_by = models.CharField(max_length=256, null=True, blank=True)
	source = models.CharField(max_length=256, null=True, blank=True)
	channel_partner = models.CharField(max_length=256, null=True, blank=True)
	parent_cp = models.CharField(max_length=256, null=True, blank=True)
	total_incentive = models.DecimalField(max_digits=1000, decimal_places=2, null=True, blank=True)
	incentive_tds = models.DecimalField(max_digits=1000, decimal_places=2, null=True, blank=True)
	net_incentive_paid = models.DecimalField(max_digits=1000, decimal_places=2, null=True, blank=True) 
	author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='author_authApp_otp_for_account')
	publish = models.DateTimeField(default=timezone.now, null=True, blank=True)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Draft', null=True, blank=True)

	def __str__(self):
		return str(self.pk) or '--Name not provided--'

	class Meta:
		verbose_name_plural = 'Excel Utility Data'

