from django.db import models
from django.contrib.auth.models import User
from stockApp.models import stockBasicDetail, stockEventsDividend
from django.utils import timezone
from websiteApp.models import buyPreIPOStockList
from decimal import Decimal
import uuid
from django.db.models import Q, F
from django.core.validators import FileExtensionValidator

STATUS_CHOICES = (
    ('draft', 'Draft'),
    ('published', 'Published'),
)

TXN_MADE_BY = (
    ('Self', 'Self'),
    ('PaymentGateway', 'PaymentGateway'),
    ('ShareBook', 'ShareBook'),
)

REASON_CODE = (
    ('Off Market Sales', 'Off Market Sales'),
    ('Return Of Shares', 'Return Of Shares'),
    ('Internal Transfer', 'Internal Transfer'),
)

SHARE_TRANSFER = (
    ('Initiated', 'Initiated'),
    ('Approved', 'Approved'),
    ('Transferred', 'Transferred')
)

COMPANY_CHOICE = (
    ('Planify Enterprises', 'Planify Enterprises'),
    ('Planify Capital', 'Planify Capital'),
)

DEPOSITORY_CHOICE = (
    ('NSDL', 'NSDL'),
    ('CDSL', 'CDSL')
)

PAYMENT_CONFIRMATION_CHOICE = (
    ('Payment Successful','Payment Successful'),
    ('Payment Failed','Payment Failed'),
    ('Payment Pending','Payment Pending')
)
# User = get_user_model()

class Transaction(models.Model):
    made_by = models.ForeignKey(User, related_name='transactions', on_delete=models.CASCADE)
    made_on = models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(max_digits=1000, decimal_places=50, null=True, blank=True)
    order_id = models.TextField(unique=True, null=True, blank=True)
    selected_stock = models.ForeignKey(stockBasicDetail, on_delete=models.SET_NULL, related_name='transactionStock',
                                       null=True, blank=True)
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
    quantity = models.DecimalField(max_digits=1000, decimal_places=2, default=0, null=True, blank=True)
    investMentPrice = models.DecimalField(max_digits=1000, decimal_places=50, default=0)
    txn_made_by = models.CharField(max_length=1000, choices=TXN_MADE_BY, default='PaymentGateway')
    payment_status = models.CharField(max_length=1000, choices=PAYMENT_CONFIRMATION_CHOICE, default='Payment Pending')
    trxnDate = models.DateTimeField(null=True, blank=True)
    sb_Depository = models.CharField(max_length=1000, choices=DEPOSITORY_CHOICE, null=True, blank=True)
    sb_Company = models.CharField(max_length=1000, choices=COMPANY_CHOICE, null=True, blank=True)
    sb_buyerIdentification = models.CharField(max_length=1000, null=True, blank=True)
    sb_buyerName = models.CharField(max_length=1000, null=True, blank=True)
    sb_ISIN = models.CharField(max_length=1000, null=True, blank=True)
    sb_resonCode = models.CharField(max_length=1000, choices=REASON_CODE, null=True, blank=True)
    transactionPrice = models.DecimalField(max_digits=1000, decimal_places=2, null=True, blank=True)
    sb_consideration = models.BigIntegerField(null=True, blank=True)
    sb_paymentReference = models.CharField(max_length=1000, null=True, blank=True)
    sb_KYC = models.CharField(max_length=1000, null=True, blank=True)
    sb_shareTransfer = models.CharField(max_length=100, choices=SHARE_TRANSFER, null=True, blank=True)
    sb_company = models.CharField(max_length=100, null=True, blank=True)
    sb_DpID = models.CharField(max_length=1000, null=True, blank=True)
    sb_clientID = models.CharField(max_length=1000, null=True, blank=True)
    sb_brokerName = models.CharField(max_length=1000, null=True, blank=True)
    sb_Quantity = models.CharField(max_length=1000, null=True, blank=True)
    sb_ISIN = models.CharField(max_length=1000, null=True, blank=True)
    demat = models.ForeignKey('investorApp.stockBrokerDetails', on_delete=models.SET_NULL, null=True, blank=True)

    sb_buyerBank = models.CharField(max_length=1000, null=True, blank=True)
    sb_accountNo = models.CharField(max_length=1000, null=True, blank=True)
    sb_uploadTransferRequest = models.FileField(upload_to='investor/documents/', null=True, blank=True, validators=[
        FileExtensionValidator(['pdf', 'jpeg', 'jpg', 'png', 'bmp'])])

    publish = models.DateTimeField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

    @property
    def total_dividend(self):
        sumDividend = []
        dividendInst = None
        if self.trxnDate:
            dividendInst = stockEventsDividend.objects.filter(
                Q(exDateFrDividend__gte=self.trxnDate) & Q(stockProfileName=self.selected_stock))
        elif self.made_on:
            dividendInst = stockEventsDividend.objects.filter(
                Q(exDateFrDividend__gte=self.made_on) & Q(stockProfileName=self.selected_stock))
        for item in dividendInst:
            sumDividend.append(item.dividendShare)

        return sum(sumDividend)

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


class UUIDModel(models.Model):
    id = models.BigAutoField(primary_key=True, editable=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    uid = models.UUIDField(default=uuid.uuid4, unique=True)

    class Meta:
        abstract = True


class UserCart(UUIDModel):
    CART_STATUS_CHOICES = (
        ('active', 'active'),
    )
    user_id = models.BigIntegerField(unique=True)
    status = models.CharField(max_length=20, choices=CART_STATUS_CHOICES, default='active')

    @classmethod
    def fetch_user_cart(cls, user_id):
        obj, _ = cls.objects.get_or_create(user_id=user_id)
        return obj


class CartItems(UUIDModel):
    ITEM_STATUS_CHOICES = (
        ('active', 'active'),
    )
    cart = models.ForeignKey(UserCart, on_delete=models.CASCADE, related_name='CartItem')
    pre_ipo_stock = models.ForeignKey(buyPreIPOStockList, on_delete=models.CASCADE)
    quantity = models.FloatField(default=0)
    status = models.CharField(max_length=20, choices=ITEM_STATUS_CHOICES, default='active')
    stock = models.ForeignKey(stockBasicDetail, on_delete=models.SET_NULL, related_name='cartStock', null=True,
                              blank=True)

    @classmethod
    def fetch_cart_items(cls, cart_id):
        return cls.objects.select_related('pre_ipo_stock').filter(cart_id=cart_id)

    @classmethod
    def fetch_obj(cls, uid, cart_id):
        return cls.objects.select_for_update().filter(uid=uid, cart_id=cart_id).last()

    @classmethod
    def fetch_stock_item(cls, cart_id, pre_ipo_id):
        obj, _ = cls.objects.select_for_update().get_or_create(pre_ipo_stock_id=pre_ipo_id, cart_id=cart_id)
        return obj

    @classmethod
    def fetch_item_count(cls, cart_id):
        return cls.objects.filter(cart_id=cart_id).count()

    def delete_item(self):
        self.delete()


class transactionDocs(models.Model):
    transacion_doc = models.FileField(upload_to='investor/documents/', null=True, blank=True,
                                      validators=[FileExtensionValidator(['pdf', 'jpeg', 'jpg', 'png', 'bmp'])])
    related_transaction = models.ForeignKey(Transaction, related_name='transactionsDoc', on_delete=models.CASCADE,
                                            null=True, blank=True)
    author = models.CharField(max_length=100, null=True, blank=True)
    publish = models.DateTimeField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated = models.DateTimeField(auto_now=True, null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft', null=True, blank=True)

    def __str__(self):
        return str(self.transacion_doc) or "----Name not provided-----"

    class Meta:
        verbose_name_plural = "Transaction Documents"
