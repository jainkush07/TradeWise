from django.db import models
from django.contrib.auth.models import User
from stockApp.models import stockBasicDetail
from django.utils import timezone


STATUS_CHOICES = (
	('draft', 'Draft'),
	('published', 'Published'),
)

TXN_MADE_BY = (
	('Self', 'Self'),
	('PaymentGateway', 'PaymentGateway'),
)
# User = get_user_model()

class Transaction(models.Model):
	made_by = models.ForeignKey(User, related_name='transactions', on_delete=models.CASCADE)
	made_on = models.DateTimeField(auto_now_add=True)
	amount = models.DecimalField(max_digits=1000, decimal_places=50, null=True, blank=True)
	order_id = models.TextField(unique=True, null=True, blank=True)
	selected_stock = models.ForeignKey(stockBasicDetail, on_delete=models.SET_NULL, related_name='transactionStock', null=True, blank=True)
	checksum = models.CharField(max_length=1000, null=True, blank=True)
	pg_MID = models.CharField(max_length=1000, null=True, blank=True)
	pg_txnID = models.CharField(max_length=1000, null=True, blank=True)
	pg_txnAmount = models.CharField(max_length=1000, null=True, blank=True)
	pg_paymentMode = models.CharField(max_length=1000, null=True, blank=True)
	pg_currency = models.CharField(max_length=1000, null=True, blank=True)
	pg_txnDate = models.CharField(max_length=1000, null=True, blank=True)
	pg_status = models.CharField(max_length=1000, null=True, blank=True)
	pg_repsonseCode = models.CharField(max_length=1000, null=True, blank=True)
	pg_responseMsg = models.CharField(max_length=1000, null=True, blank=True)
	pg_gatewayName = models.CharField(max_length=1000, null=True, blank=True)
	pg_bankTxnID = models.CharField(max_length=1000, null=True, blank=True)
	pg_bankName = models.CharField(max_length=1000, null=True, blank=True)
	pg_checkSubHash = models.CharField(max_length=1000, null=True, blank=True)
	quantity = models.IntegerField(null=True, blank=True)
	investMentPrice = models.DecimalField(max_digits=1000, decimal_places=50, null=True, blank=True)
	txn_made_by = models.CharField(max_length=1000,choices=TXN_MADE_BY, default='PaymentGateway')
	trxnDate = models.DateTimeField(null=True, blank=True)
	publish = models.DateTimeField(null=True, blank=True)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')


	# def ger_user(self, request):
	# 	currentUserInst = request.user
	# 	retur currentUserInst

	
	def total_invested_amount(self, user):
		# totalInvestedAmount = 0
		transactionInst = Transaction.objects.filter(made_by=user)
		totalAmount = 0
		for item in transactionInst:
			totalAmount = item.amount
			
		return totalAmount


	def save(self, *args, **kwargs):
		if self.order_id is None and self.made_on and self.id:
			self.order_id = self.made_on.strftime('PLANIFY%Y%m%dODR') + str(self.id)
		return super().save(*args, **kwargs)

	def __str__(self):
		return f'User: {self.made_by} transacted for: {self.amount} with Order ID: {self.order_id}' or '--Name not provided--'

	class Meta:
		verbose_name_plural = 'Order Transaction Details'