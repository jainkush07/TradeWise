from django.db import models
from django.utils import timezone
from django.core.validators import FileExtensionValidator
from django.contrib.auth.models import User
# employeeApp import city, staate, country
from employeeApp.models import city, state, country

from investorApp.constants import SebiRegistrationTypes
from whatsappAuthApp.models import whatsappLeads
from django.db.models.signals import post_save
from django.dispatch import receiver
from cartApp.models import Transaction
from stockApp.models import stockBasicDetail, stockEventsDividend
from django.db.models import Q

STATUS_CHOICES = (
    ('draft', 'Draft'),
    ('published', 'Published'),
)

Gender_Choices = (
    ('male', 'Male'),
    ('female', 'Female'),
)
SHARE_DEMATERIALISED = (
    ('Yes', 'Yes'),
    ('No', 'No'),
)

ESOP_SHARE_DEMATERIALISED = (
    ('Yes,In demat', 'Yes, In demat'),
    ('Vested,Not In demat', 'Vested,Not In demat'),
    ('Not Fully Vested', 'Not Fully Vested'),
)
Transfer_Type_Choices = (
    (1, 'Physical DIS'),
    (2, 'Online EDIS'),
    (3, 'NSDL speed-e | CDSL easi')
)
TXN_MADE_BY = (
    ('Self', 'Self'),
    ('PaymentGateway', 'PaymentGateway'),
)

Portfolio_Range = (
    ('< ₹ 1 Lac', '< ₹ 1 Lac'),
    ('₹ 1 - 5 Lac', '₹ 1 - 5 Lac'),
    ('₹ 5 - 10 Lac', '₹ 5 - 10 Lac'),
    ('₹ 10 - 25 Lac', '₹ 10 - 25 Lac'),
    ('₹ 25 - 50 Lac', '₹ 25 - 50 La'),
    ('₹ 50 - 100 Lac', '₹ 50 - 100 Lac'),
    ('₹ 1 - 5 Crores', '₹ 1 - 5 Crores'),
    ('₹ 5 - 10 Crores', '₹ 5 - 10 Crores'),
    ('₹ 10 - 25 Crores', '₹ 10 - 25 Crores'),
    ('₹ 25 - 50 Crores', '₹ 25 - 50 Crores'),
    ('₹ 50 - 100 Crores', '₹ 50 - 100 Crores'),
    ('₹ 100 + Crores', '₹ 100 + Crores'),
)

TRANSACTION_FLAG = (
    ('Temprory', 'Temprory'),
    ('Acutal', 'Actual'),
)

COMPANY_SIGNED_CHOICES = (
    ('Individual', 'Individual'),
    ('Solo proprietorship firm', 'Solo proprietorship firm'),
    ('Partnership firm / LLP', 'Partnership firm / LLP'),
    ('Private limited company', 'Private limited company'),
    ('Public limited company', 'Public limited company'),
)
CHANNEL_PARTNER_COMPANY_REGISTERATION_CHOICES = (
    ('SEBI - stock market', 'SEBI - stock market'),
    ('AMFI - mutual funds', 'AMFI - mutual funds'),
    ('IRDA - insurace', 'IRDA - insurace'),
    ('None', 'None'),
)

COMPANY_REGISTERATION_CHOICES = (
    (SebiRegistrationTypes.AIF, 'Alternate Investment Fund'),
    (SebiRegistrationTypes.FPI, 'FPI/FII/QFI'),
    # (SebiRegistrationTypes.IA, 'Investment Advisor'),
    # (SebiRegistrationTypes.SYNDICATE_BANK, 'Syndicate Bank'),
    (SebiRegistrationTypes.STOCK_BROKER, 'Stock Broker'),
    (SebiRegistrationTypes.MUTUAL_FUND, 'Mutual Fund'),
    # (SebiRegistrationTypes.PORTFOLIO_MANAGER, 'Portfolio Managers'),
    (SebiRegistrationTypes.IVC, 'Indian Venture Capital Fund'),
    (SebiRegistrationTypes.FVC, 'Foreign Venture Capital Fund')
)

COMPANY_REGISTERED_WITH_CHOICES = (
    *CHANNEL_PARTNER_COMPANY_REGISTERATION_CHOICES,
    *COMPANY_REGISTERATION_CHOICES
)

Depository_Info = (
    ('NSDL', 'NSDL'),
    ('CDSL', 'CDSL'),
)

AccountType_Info = (
    ('Current', 'Current'),
    ('Saving', 'Saving'),
)

Boolean_Choice = (
    ('Yes', 'Yes'),
    ('No', 'No'),
)

ROFR_CHOICES = (
    ('Yes', 'Yes'),
    ('No', 'No'),
    ('No Idea', 'No Idea'),
)
DEALER_NETWORK_OPTIONS = (
    ('Unlisted Share Dealers', 'Unlisted Share Dealers'),
    ('Unlisted Pre Ipo Dealers', 'Unlisted Pre Ipo Dealers'),
    ('Others', 'Others'),
)
INFLUENCER_CHOICES = (
    ('Facebook', 'Facebook'),
    ('Whatsapp', 'Whatsapp'),
    ('Twitter', 'Twitter'),
    ('Youtube', 'Youtube'),
    ('LinkedIn', 'LinkedIn')
)


class BaseModel(models.Model):
    id = models.BigAutoField(primary_key=True, editable=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


#
class investorSource(models.Model):
    source = models.CharField(max_length=1000, null=True, blank=True)
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

    def __str__(self):
        return self.source or '--Name not provided--'

    class Meta:
        verbose_name_plural = 'Investor Source'


class investorPortfolioManagedBy(models.Model):
    managedBy = models.CharField(max_length=1000, null=True, blank=True)
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

    def __str__(self):
        return self.managedBy or '--Name not provided--'

    class Meta:
        verbose_name_plural = 'Investor Portfolio Managed By'


class channelPartnerList(models.Model):
    channelPartnerName = models.CharField(max_length=1000, null=True, blank=True)
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

    def __str__(self):
        return self.channelPartnerName or '--Name not provided--'

    class Meta:
        verbose_name_plural = 'Channel Partner List'


class dealerList(models.Model):
    dealerName = models.CharField(max_length=1000, null=True, blank=True)
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

    def __str__(self):
        return self.dealerName or '--Name not provided--'

    class Meta:
        verbose_name_plural = 'Dealer List'


def get_dealer_path(instance, filename):
    return 'dealer/{0}/documents/{1}'.format(instance.user_id, filename)


class DealerDetails(BaseModel):
    user_id = models.BigIntegerField(unique=True)
    dealer_name = models.CharField(max_length=1000, null=True, blank=True)
    network = models.CharField(max_length=30, choices=DEALER_NETWORK_OPTIONS, null=True, blank=True)
    asset_portfolio_managing = models.CharField(max_length=100, choices=Portfolio_Range, null=True, blank=True)
    num_of_investor = models.CharField(max_length=100,default='')
    signature = models.FileField(upload_to=get_dealer_path, null=True, blank=True,
                                 validators=[FileExtensionValidator(['pdf', 'jpeg', 'jpg', 'png', 'bmp'])])
    agreement_place = models.CharField(max_length=100, null=True, blank=True)
    agreement_signer = models.CharField(max_length=100, null=True, blank=True)
    agreement_date = models.DateTimeField(null=True)
    agreement_end_date = models.DateTimeField(null=True)
    consent = models.CharField(max_length=10, choices=Boolean_Choice, null=True, blank=True)
    agreement = models.FileField(upload_to=get_dealer_path, null=True, blank=True,
                                 validators=[FileExtensionValidator(['pdf', 'jpeg', 'jpg', 'png', 'bmp'])])
    verification_status = models.CharField(max_length=10, choices=Boolean_Choice, null=True, blank=True)

    @classmethod
    def fetch_obj(cls, user_id):
        obj = cls.objects.filter(user_id=user_id).last()
        if not obj:
            obj = cls(user_id=user_id)
            obj.save()
        return obj


class investorSourceDetails(models.Model):
    profileOwner = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profileOwnerISD', null=True,
                                        blank=True)
    sourceName = models.ForeignKey(investorSource, on_delete=models.CASCADE, related_name="investorSourceSSD",
                                   null=True, blank=True)
    portfolioManagedBy = models.ForeignKey(investorPortfolioManagedBy, on_delete=models.CASCADE,
                                           related_name="investorPortfolioISD", null=True, blank=True)
    channelPartner = models.ForeignKey(channelPartnerList, on_delete=models.CASCADE,
                                       related_name="investorPortfolioISD", null=True, blank=True)
    dealer = models.ForeignKey(dealerList, on_delete=models.CASCADE, related_name="investorPortfolioISD", null=True,
                               blank=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='authorISD', null=True, blank=True)
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

    def __str__(self):
        return str(self.profileOwner) or '--Name not provided--'

    class Meta:
        verbose_name_plural = 'Investor Source Details'


#
class investorPersonalDetails(models.Model):
    profileOwner = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profileOwnerIPD', null=True,
                                        blank=True)
    name = models.CharField(max_length=1000, null=True, blank=True)
    # totalProgress = models.BigIntegerField(null=Tr)
    # emailID = models.EmailField(max_length = 254, null=True, blank=True)
    mobileNumber = models.BigIntegerField(null=True, blank=True)
    emailVerified = models.BooleanField(default=False, null=True, blank=True)
    gender = models.CharField(max_length=50, choices=Gender_Choices, null=True, blank=True)
    panNumber = models.CharField(max_length=100, null=True, blank=True)
    uploadPan = models.FileField(upload_to='investor/documents/', null=True, blank=True,
                                 validators=[FileExtensionValidator(['pdf', 'jpeg', 'jpg', 'png', 'bmp'])])
    aadharNumber = models.CharField(max_length=100, null=True, blank=True)
    dob = models.DateField(null=True)
    uploadAadhar = models.FileField(upload_to='investor/documents/', null=True, blank=True,
                                    validators=[FileExtensionValidator(['pdf', 'jpeg', 'jpg', 'png', 'bmp'])])
    address = models.TextField(null=True, blank=True)
    city = models.ForeignKey(city, on_delete=models.SET_NULL, null=True, blank=True, related_name='cityIPD')
    pinCode = models.BigIntegerField(null=True, blank=True)
    state = models.ForeignKey(state, on_delete=models.SET_NULL, null=True, blank=True, related_name='stateIPD')
    country = models.ForeignKey(country, on_delete=models.SET_NULL, null=True, blank=True, related_name='countryIPD')
    aadharVerified = models.CharField(max_length=100, choices=Boolean_Choice, null=True, blank=True)
    panVerified = models.CharField(max_length=100, choices=Boolean_Choice, null=True, blank=True)
    personalDetailVerified = models.CharField(max_length=100, choices=Boolean_Choice, null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='authorIPD', null=True, blank=True)
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

    def save(self):
        try:
            whatsappLeadsInst = whatsappLeads.objects.get(profileOwner=self.profileOwner)
            self.mobileNumber = whatsappLeadsInst.phoneNumber
        except:
            pass
        try:
            verified_status, created = verificationStatus.objects.get_or_create(profileOwner=self.profileOwner)
        except:
            verified_status = None
        if self.uploadPan:
            if verified_status:
                verified_status.getPanStatus = 'Uploaded'
                verified_status.save()
        if self.uploadAadhar:
            if verified_status:
                verified_status.getAadharStatus = 'Uploaded'
                verified_status.save()
        super(investorPersonalDetails, self).save()

    def __str__(self):
        return self.name or '--Name not provided--'

    class Meta:
        verbose_name_plural = 'Investor Personal Details'

    @classmethod
    def fetch_obj(cls, user_id):
        obj = cls.objects.filter(profileOwner_id=user_id).last()
        if not obj:
            obj = cls(profileOwner_id=user_id)
            obj.save()
        return obj


#
class lookingToInvestDetails(models.Model):
    name = models.CharField(max_length=1000, null=True, blank=True)

    author = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='authorLTID', null=True, blank=True)
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

    def __str__(self):
        return self.name or '--Name not provided'

    class Meta:
        verbose_name = 'Looking To Invest Details'


class CompanyStages(BaseModel):
    name = models.CharField(max_length=1000, null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

    def __str__(self):
        return str(self.name)


#
class investmentDetails(models.Model):
    profileOwner = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profileOwnerID', null=True,
                                        blank=True)
    user_role = models.CharField(max_length=50, default='INVESTOR', null=True, blank=True)
    presentPortfolio = models.CharField(max_length=50, choices=Portfolio_Range, null=True, blank=True)
    investPorfolio = models.CharField(max_length=100, null=True, blank=True)
    assetPortfolioManaging = models.CharField(max_length=100, choices=Portfolio_Range, null=True, blank=True)
    secondaryMarket = models.BooleanField(null=True, blank=True)
    sectorToInvest = models.CharField(max_length=100, null=True, blank=True)
    primaryMarket = models.BooleanField(null=True, blank=True)
    companyStage = models.ManyToManyField(CompanyStages, blank=True)
    lookingToInvest = models.ManyToManyField(lookingToInvestDetails, blank=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='authorID', null=True, blank=True)
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

    def __str__(self):
        return str(self.presentPortfolio) or '--Name not provided--'

    class Meta:
        verbose_name_plural = 'Investment Details'


#
class investorBankDetails(models.Model):
    profileOwner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='profileOwnerIBD', null=True,
                                     blank=True)
    bankName = models.CharField(max_length=1000)
    accountHolder = models.CharField(max_length=256, null=True, blank=True)
    accountNumber = models.CharField(max_length=256, null=True, blank=True)
    accountType = models.CharField(max_length=10, choices=AccountType_Info, null=True, blank=True)
    is_default = models.BooleanField(default=True)
    ifsc_Code = models.CharField(max_length=1000, null=True, blank=True)
    cancelledCheque = models.FileField(upload_to='investor/documents/', null=True, blank=True,
                                       validators=[FileExtensionValidator(['pdf', 'jpeg', 'jpg', 'png', 'bmp'])])
    upiID = models.CharField(max_length=1000, null=True, blank=True)
    bankVerified = models.CharField(max_length=100, choices=Boolean_Choice, null=True, blank=True)

    author = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='authorIBD', null=True, blank=True)
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

    def __str__(self):
        return self.bankName or '--Name not provided--'

    class Meta:
        verbose_name_plural = 'Investor Bank Details'


#
@receiver(post_save, sender=investorBankDetails)
def update_verification_status_for_bank(sender, instance, **kwargs):
    bankInst = investorBankDetails.objects.filter(profileOwner=instance.profileOwner)
    verified_status, created = verificationStatus.objects.get_or_create(profileOwner=instance.profileOwner)
    bank_count = bankInst.count()
    yes_count = 0
    no_count = 0
    empty_count = 0
    if bankInst:
        for item in bankInst:
            if item.bankVerified == 'Yes':
                yes_count += 1
            elif item.bankVerified == 'No':
                no_count += 1
            else:
                empty_count += 1
        if bank_count == yes_count:
            verified_status.bankVerifiedStatus = 'Verified'
        elif bank_count == no_count:
            verified_status.bankVerifiedStatus = 'Failed'
        elif bank_count == empty_count:
            verified_status.bankVerifiedStatus = 'Uploaded'
        elif yes_count > 0:
            verified_status.bankVerifiedStatus = 'Partial Verified'
        else:
            verified_status.bankVerifiedStatus = 'Uploaded'
        verified_status.save()

    else:
        verified_status.bankVerifiedStatus = 'Uploaded'
        verified_status.save()


#
class stockBrokerDetails(models.Model):
    name = models.CharField(max_length=1000, null=True, blank=True)
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

    def __str__(self):
        return self.name or '--Name not provided--'

    class Meta:
        verbose_name_plural = 'Stock Broker Details'


class investorDMATDetails(models.Model):
    profileOwner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='profileOwnerIDD')
    stockBroker = models.ForeignKey('stockBrokerDetails', on_delete=models.SET_NULL, related_name="stockBrokerIDD",
                                    null=True, blank=True)
    depository = models.CharField(max_length=10, choices=Depository_Info, null=True, blank=True)
    dmatClientMasterReport = models.FileField(upload_to='investor/documents/', null=True, blank=True,
                                              validators=[FileExtensionValidator(['pdf', 'jpeg', 'jpg', 'png', 'bmp'])])
    dpID = models.CharField(max_length=1000, null=True, blank=True)
    clientID = models.CharField(max_length=1000, null=True, blank=True)  # field-type should be change
    is_default = models.BooleanField(default=True)
    dmatVerified = models.CharField(max_length=100, choices=Boolean_Choice, null=True, blank=True)

    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

    def __str__(self):
        return self.dpID or '--Name not provided--'

    class Meta:
        verbose_name_plural = 'Investor DMAT Details'


#
@receiver(post_save, sender=investorDMATDetails)
def update_verification_status_for_dmat(sender, instance, **kwargs):
    dmatInst = investorDMATDetails.objects.filter(profileOwner=instance.profileOwner)
    verified_status, created = verificationStatus.objects.get_or_create(profileOwner=instance.profileOwner)
    dmat_count = dmatInst.count()
    yes_count = 0
    no_count = 0
    empty_count = 0
    if dmatInst:
        for item in dmatInst:
            if item.dmatVerified == 'Yes':
                yes_count += 1
            elif item.dmatVerified == 'No':
                no_count += 1
            else:
                empty_count += 1
        print(
            f'dmat_count: {dmat_count} || yes_count: {yes_count} || no_count: {no_count} || empty_count: {empty_count}')
        if dmat_count == yes_count:
            verified_status.dmatVerifiedStatus = 'Verified'
        elif dmat_count == no_count:
            verified_status.dmatVerifiedStatus = 'Failed'
        elif dmat_count == empty_count:
            verified_status.dmatVerifiedStatus = 'Uploaded'
        elif yes_count > 0:
            verified_status.dmatVerifiedStatus = 'Partial Verified'
        else:
            verified_status.dmatVerifiedStatus = 'Uploaded'
        verified_status.save()

    else:
        verified_status.dmatVerifiedStatus = 'Uploaded'
        verified_status.save()


#
class linkedInModel(models.Model):
    profileOwner = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profileOwnerIIM', null=True,
                                        blank=True)
    profileOwnerMM = models.ManyToManyField(User, blank=True, related_name='profileOwnerMMIIM')
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

    class Meta:
        verbose_name_plural = 'Iinked In Model'

    def __str__(self):
        return f'Owner: {self.profileOwner.username}'


class verificationStatus(models.Model):
    profileOwner = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profileOwnerVSD')
    aadharVerifiedStatus = models.CharField(max_length=100, choices=Boolean_Choice, null=True, blank=True)
    panVerifiedStatus = models.CharField(max_length=100, choices=Boolean_Choice, null=True, blank=True)
    personalDetailVerifiedStatus = models.CharField(max_length=100, choices=Boolean_Choice, null=True, blank=True)
    bankVerifiedStatus = models.CharField(max_length=100, default='Empty', null=True, blank=True)
    dmatVerifiedStatus = models.CharField(max_length=100, default='Empty', null=True, blank=True)
    getVerifiedProgress = models.IntegerField(null=True, blank=True)

    getPersonalStatus = models.CharField(max_length=100, default='Filled', null=True, blank=True)
    getAadharStatus = models.CharField(max_length=100, default='Empty', null=True, blank=True)
    getPanStatus = models.CharField(max_length=100, default='Empty', null=True, blank=True)
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

    def save(self, *args, **kwargs):
        try:
            personalDetailInst = investorPersonalDetails.objects.get(profileOwner=self.profileOwner)
        except:
            personalDetailInst = None
        verification_progress = 0
        if self.personalDetailVerifiedStatus == 'Yes':
            self.getPersonalStatus = 'Verified'
            verification_progress += 20
        elif self.personalDetailVerifiedStatus == 'No':
            self.getPersonalStatus = 'Failed'
        else:
            self.getPersonalStatus = 'Filled'

        if personalDetailInst and personalDetailInst.uploadAadhar:
            if self.aadharVerifiedStatus == 'Yes':
                self.getAadharStatus = 'Verified'
                verification_progress += 20
            elif self.aadharVerifiedStatus == 'No':
                self.getAadharStatus = 'Failed'
            else:
                self.getAadharStatus = 'Uploaded'
        else:
            self.getAadharStatus = 'Empty'

        if personalDetailInst and personalDetailInst.uploadPan:
            if self.panVerifiedStatus == 'Yes':
                self.getPanStatus = 'Verified'
                verification_progress += 20
            elif self.panVerifiedStatus == 'No':
                self.getPanStatus = 'Failed'
            else:
                self.getPanStatus = 'Uploaded'
        else:
            self.getPanStatus = 'Empty'

        all_banks = investorBankDetails.objects.filter(profileOwner=self.profileOwner)
        all_banks_count = all_banks.count()
        verified_banks_count = all_banks.filter(bankVerified='Yes').count()
        try:
            per_bank_weight = 20 / all_banks_count
        except:
            per_bank_weight = 0
        verified_banks_percentage = per_bank_weight * verified_banks_count
        verification_progress += verified_banks_percentage

        all_dmats = investorDMATDetails.objects.filter(profileOwner=self.profileOwner)
        all_dmats_count = all_dmats.count()
        verified_dmats_count = all_dmats.filter(dmatVerified='Yes').count()
        try:
            per_dmat_weight = 20 / all_dmats_count
        except:
            per_dmat_weight = 0
        verified_dmats_percentage = per_dmat_weight * verified_dmats_count
        verification_progress += verified_dmats_percentage
        self.getVerifiedProgress = verification_progress
        super(verificationStatus, self).save()

    class Meta:
        verbose_name_plural = 'Investor Verification Status'


class investorPortfolio(models.Model):
    profileOwner = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profileOwnerIPLO')
    stock_name = models.ForeignKey(stockBasicDetail, on_delete=models.SET_NULL, related_name="investorPortfolioSTCK",
                                   null=True, blank=True)
    quantity = models.IntegerField(null=True, blank=True)
    transactionDate = models.DateTimeField(null=True, blank=True)
    investorStockPrice = models.IntegerField(null=True, blank=True)
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

    def __str__(self):
        return str(self.stock_name) or '--Name not provided--'

    class Meta:
        verbose_name_plural = 'Investor Portfolio'


### models for portfolio ###


class tempUser(models.Model):
    profileOwner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='profileOwnerTU')
    name = models.CharField(max_length=1000, null=True, blank=True)
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

    def __str__(self):
        return str(self.name) or '--Name not provided--'

    class Meta:
        verbose_name_plural = 'temp users'


class tempTransaction(models.Model):
    made_by = models.ForeignKey(tempUser, related_name='tempTransactionTT', on_delete=models.CASCADE)
    # made_on = models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(max_digits=1000, decimal_places=50, null=True, blank=True)
    # tempFlag = models.CharField(max_length=20, choices=TRANSACTION_FLAG, default='Temprory')
    selected_stock = models.ForeignKey(stockBasicDetail, on_delete=models.SET_NULL, related_name='transactionStockTT',
                                       null=True, blank=True)
    quantity = models.IntegerField(null=True, blank=True)
    investMentPrice = models.DecimalField(max_digits=1000, decimal_places=50, null=True, blank=True)
    txn_made_by = models.CharField(max_length=1000, choices=TXN_MADE_BY, default='Self')
    trxnDate = models.DateTimeField(null=True, blank=True)
    demat = models.ForeignKey(stockBrokerDetails, on_delete=models.SET_NULL, null=True, blank=True)
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
        # elif self.made_on:
        # 	dividendInst = stockEventsDividend.objects.filter(Q(exDateFrDividend__gte=self.made_on) & Q(stockProfileName=self.selected_stock))
        if dividendInst:
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

    # def save(self, *args, **kwargs):
    # 	if self.order_id is None and self.made_on and self.id:
    # 		self.order_id = self.made_on.strftime('PLANIFY%Y%m%dODR') + str(self.id)
    # 	return super().save(*args, **kwargs)

    def __str__(self):
        return f'User: {self.made_by} transacted for: {self.amount}' or '--Name not provided--'

    class Meta:
        verbose_name_plural = 'Temprory Order Transaction Details'


# Share Transfer Screen Models..

class shareBookTransactionsList(models.Model):
    related_investor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='shareBookTransactionSBTL',
                                         null=True, blank=True)
    sb_DpID = models.CharField(max_length=1000, null=True, blank=True)
    sb_clientID = models.CharField(max_length=1000, null=True, blank=True)
    sb_brokerName = models.CharField(max_length=1000, null=True, blank=True)
    sb_Quantity = models.CharField(max_length=1000, null=True, blank=True)
    sb_ISIN = models.CharField(max_length=1000, null=True, blank=True)
    sb_resonCode = models.CharField(max_length=1000, null=True, blank=True)
    sb_consideration = models.BigIntegerField(null=True, blank=True)
    sb_buyerName = models.CharField(max_length=1000, null=True, blank=True)
    sb_buyerBank = models.CharField(max_length=1000, null=True, blank=True)
    sb_accountNo = models.CharField(max_length=1000, null=True, blank=True)
    sb_paymentReference = models.CharField(max_length=1000, null=True, blank=True)
    sb_KYC = models.CharField(max_length=1000, null=True, blank=True)
    sb_stockName = models.CharField(max_length=1000, null=True, blank=True)
    sb_shareTransfer = models.CharField(max_length=100, null=True, blank=True)
    sb_executionDate = models.DateTimeField(null=True, blank=True)
    sb_uploadTransferRequest = models.FileField(upload_to='investor/documents/', null=True, blank=True, validators=[
        FileExtensionValidator(['pdf', 'jpeg', 'jpg', 'png', 'bmp'])])
    publish = models.DateTimeField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

    def __str__(self):
        return self.sb_buyerName or '--Name not provided--'

    class Meta:
        verbose_name_plural = 'Share Book Transaction List'


class shareBookStatusDetails(models.Model):
    tansaction = models.OneToOneField(shareBookTransactionsList, on_delete=models.CASCADE,
                                      related_name='shareBookTransactionSBT')
    sb_company = models.CharField(max_length=100, null=True, blank=True)
    sb_depository = models.CharField(max_length=100, null=True, blank=True)
    sb_shareTransferStatus = models.CharField(max_length=100, null=True, blank=True)
    sb_uploadFile = models.FileField(upload_to='investor/documents/', null=True, blank=True,
                                     validators=[FileExtensionValidator(['pdf', 'jpeg', 'jpg', 'png', 'bmp'])])
    publish = models.DateTimeField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

    def __str__(self):
        return self.sb_company or '--Name not provided--'

    class Meta:
        verbose_name_plural = 'Share Book Transaction Status List'


class UserTransferFacility(BaseModel):
    user_id = models.BigIntegerField(db_index=True)
    role = models.CharField(max_length=50, null=True, blank=True)
    transfer_type = models.SmallIntegerField(null=True, blank=True, choices=Transfer_Type_Choices)
    transfer_file_proof = models.FileField(upload_to='kyc/documents/transfer_facility/', null=True, blank=True,
                                           validators=[FileExtensionValidator(['pdf', 'jpeg', 'jpg', 'png', 'bmp'])])
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    verification_status = models.CharField(max_length=10, choices=Boolean_Choice, null=True, blank=True)

    class Meta:
        unique_together = ['user_id', 'role']

    @classmethod
    def fetch_obj(cls, user_id, role):
        obj = cls.objects.filter(user_id=user_id, role=role).last()
        if not obj:
            obj = cls(user_id=user_id, role=role)
            obj.save()
        return obj


class CompanySectors(models.Model):
    name = models.CharField(max_length=1000)
    analyst = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='analystCS', null=True, blank=True)
    verifiedBy = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='verifiedByCS', null=True, blank=True)
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

    def __str__(self):
        return str(self.name)


def get_company_upload_path(instance, filename):
    return 'company/{0}/documents/{1}'.format(instance.id, filename)


class CompanyDetails(BaseModel):
    user_id = models.BigIntegerField(db_index=True)
    address = models.TextField(null=True, blank=True)
    user_role = models.CharField(max_length=50, default='CHANNEL PARTNER')
    role_in_company = models.CharField(max_length=50, blank=True)
    city = models.ForeignKey(city, on_delete=models.SET_NULL, null=True, blank=True, related_name='cityCPD')
    pinCode = models.BigIntegerField(null=True, blank=True)
    company_url = models.URLField(max_length=1000, null=True, blank=True)
    registered_with = models.CharField(max_length=50, null=True, blank=True, choices=COMPANY_REGISTERED_WITH_CHOICES)
    license_number = models.CharField(max_length=100, null=True, blank=True)
    organisation_name = models.CharField(max_length=100, null=True, blank=True)
    signed_as = models.CharField(max_length=30, null=True, blank=True, choices=COMPANY_SIGNED_CHOICES)
    sector = models.CharField(max_length=100, null=True, blank=True)
    company_sector = models.ManyToManyField(CompanySectors)
    state = models.ForeignKey(state, on_delete=models.SET_NULL, null=True, blank=True, related_name='stateCPD')
    country = models.ForeignKey(country, on_delete=models.SET_NULL, null=True, blank=True, related_name='countryCPD')
    gst_applicable = models.CharField(max_length=10, choices=Boolean_Choice, null=True, blank=True)
    gst_number = models.CharField(max_length=100, null=True, blank=True)
    gst_proof = models.FileField(upload_to=get_company_upload_path, null=True, blank=True,
                                 validators=[FileExtensionValidator(['pdf', 'jpeg', 'jpg', 'png', 'bmp'])])
    license_proof = models.FileField(upload_to=get_company_upload_path, null=True, blank=True,
                                     validators=[FileExtensionValidator(['pdf', 'jpeg', 'jpg', 'png', 'bmp'])])
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    sebi_registeration = models.CharField(max_length=100, null=True, blank=True)
    pan_number = models.CharField(max_length=20, null=True, blank=True)
    upload_pan = models.FileField(upload_to=get_company_upload_path, null=True, blank=True,
                                  validators=[FileExtensionValidator(['pdf', 'jpeg', 'jpg', 'png', 'bmp'])])
    license_verified = models.CharField(max_length=10, choices=Boolean_Choice, null=True, blank=True)
    verification_status = models.CharField(max_length=10, choices=Boolean_Choice, null=True, blank=True)

    class Meta:
        unique_together = ['user_id', 'user_role']

    @classmethod
    def fetch_obj(cls, user_id, role):
        obj = cls.objects.filter(user_id=user_id, user_role=role).last()
        if not obj:
            obj = cls(user_id=user_id, user_role=role)
            obj.save()
        return obj


def get_company_business_upload_path(instance, filename):
    return 'company/{0}/business_documents/{1}'.format(instance.company_id, filename)


class CompanyBusinessDetails(BaseModel):
    company = models.OneToOneField(CompanyDetails, on_delete=models.CASCADE, null=True, blank=True)
    share_dematerialized = models.CharField(max_length=100, choices=Boolean_Choice, null=True, blank=True)
    valuation_status = models.CharField(max_length=10, choices=Boolean_Choice, null=True, blank=True)
    annual_turnover = models.FloatField(default=0)
    revenue_growth = models.FloatField(default=0)
    profit_growth = models.FloatField(default=0)
    valuation = models.FloatField(default=0)
    employees = models.BigIntegerField(default=0)
    pitch_deck = models.FileField(upload_to=get_company_business_upload_path, null=True, blank=True,
                                  validators=[FileExtensionValidator(['pdf', 'jpeg', 'jpg', 'png', 'bmp'])])
    verification_status = models.CharField(max_length=10, choices=Boolean_Choice, null=True, blank=True)

    @classmethod
    def fetch_obj(cls, company_id):
        obj = cls.objects.filter(company_id=company_id).last()
        if not obj:
            obj = cls(company_id=company_id)
            obj.save()
        return obj


def get_channel_partner_path(instance, filename):
    return 'cp/{0}/documents/{1}'.format(instance.user_id, filename)


class ChannelPartnerDetails(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='UserChannelPartnerDetail',
                             null=True, blank=True)
    signature = models.FileField(upload_to=get_channel_partner_path, null=True, blank=True,
                                 validators=[FileExtensionValidator(['pdf', 'jpeg', 'jpg', 'png', 'bmp'])])
    asset_portfolio_managing = models.CharField(max_length=100, choices=Portfolio_Range, null=True, blank=True)
    num_of_investor = models.CharField(max_length=100,default='')
    agreement_place = models.CharField(max_length=100, null=True, blank=True)
    agreement_signer = models.CharField(max_length=100, null=True, blank=True)
    agreement_date = models.DateTimeField(null=True)
    agreement_end_date = models.DateTimeField(null=True)
    consent = models.CharField(max_length=10, choices=Boolean_Choice, null=True, blank=True)
    agreement = models.FileField(upload_to=get_channel_partner_path, null=True, blank=True,
                                 validators=[FileExtensionValidator(['pdf', 'jpeg', 'jpg', 'png', 'bmp'])])
    verificationStatus = models.CharField(max_length=10, choices=Boolean_Choice, null=True, blank=True)

    @classmethod
    def fetch_obj(cls, user_id):
        obj = cls.objects.filter(user_id=user_id).last()
        if not obj:
            obj = cls(user_id=user_id)
            obj.save()
        return obj


class UserEsopDetails(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='UserEsopDetails',
                             null=True, blank=True)
    role_in_company = models.CharField(max_length=50, blank=True)
    organisation_name = models.CharField(max_length=100, null=True, blank=True)
    company_url = models.URLField(max_length=1000, null=True, blank=True)
    valuation = models.FloatField(default=0)
    share_dematerialized = models.CharField(max_length=100, choices=ESOP_SHARE_DEMATERIALISED, null=True, blank=True)
    valuation_status = models.CharField(max_length=10, choices=Boolean_Choice, null=True, blank=True)
    shares_owned = models.IntegerField(default=0)
    rofr = models.CharField(max_length=10, choices=ROFR_CHOICES, null=True, blank=True)
    verificationStatus = models.CharField(max_length=10, choices=Boolean_Choice, null=True, blank=True)

    class Meta:
        unique_together = ['user_id', 'organisation_name']

    @classmethod
    def fetch_obj(cls, user_id):
        obj = cls.objects.filter(user_id=user_id).last()
        if not obj:
            obj = cls(user_id=user_id)
            obj.save()
        return obj


class CompanySectorDetails(BaseModel):
    company = models.ForeignKey(CompanyDetails, on_delete=models.CASCADE)
    sector = models.ForeignKey(CompanySectors, on_delete=models.CASCADE)
    license_number = models.CharField(max_length=100, null=True, blank=True)
    license_proof = models.FileField(upload_to=get_company_upload_path, null=True, blank=True,
                                     validators=[FileExtensionValidator(['pdf', 'jpeg', 'jpg', 'png', 'bmp'])])
    license_verified = models.CharField(max_length=10, choices=Boolean_Choice, null=True, blank=True)
    verification_status = models.CharField(max_length=10, choices=Boolean_Choice, null=True, blank=True)

    class Meta:
        unique_together = ['company', 'sector']

    @classmethod
    def fetch_obj(cls, company_id, sector_id):
        obj = cls.objects.filter(company_id=company_id, sector_id=sector_id).last()
        if not obj:
            obj = cls(company_id=company_id, sector_id=sector_id)
            obj.save()
        return obj


class UserSocialDetails(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE,
                                null=True, blank=True)
    short_description = models.CharField(max_length=100, null=True, blank=True)
    is_fin_influencer = models.CharField(max_length=10, choices=Boolean_Choice, blank=True)
    description = models.CharField(max_length=1000, null=True, blank=True)
    linkedIn_handle = models.CharField(max_length=100, null=True, blank=True)
    facebook_handle = models.CharField(max_length=100, null=True, blank=True)
    youtube_handle = models.CharField(max_length=100, null=True, blank=True)
    instagram_handle = models.CharField(max_length=100, null=True, blank=True)
    twitter_handle = models.CharField(max_length=100, null=True, blank=True)
    telegram_handle = models.CharField(max_length=100, null=True, blank=True)
    moj_handle = models.CharField(max_length=100, null=True, blank=True)
    daily_hunt_handle = models.CharField(max_length=100, null=True, blank=True)
    pinterest_handle = models.CharField(max_length=100, null=True, blank=True)
    quora_handle = models.CharField(max_length=100, null=True, blank=True)
    josh_handle = models.CharField(max_length=100, null=True, blank=True)
    chingari_handle = models.CharField(max_length=100, null=True, blank=True)
    verification_status = models.CharField(max_length=10, choices=Boolean_Choice, null=True, blank=True)

    @classmethod
    def fetch_obj(cls, user_id):
        obj = cls.objects.filter(user_id=user_id).last()
        if not obj:
            obj = cls(user_id=user_id)
            obj.save()
        return obj


def get_company_financial_upload_path(instance, filename):
    return 'company/{0}/financial/{1}'.format(instance.company_id, filename)


class CompanyFinancialDetails(BaseModel):
    company = models.ForeignKey(CompanyDetails, on_delete=models.CASCADE, null=True, blank=True)
    financial_year = models.CharField(max_length=10, null=True, blank=True)
    financial_report = models.FileField(upload_to=get_company_financial_upload_path, null=True, blank=True,
                                        validators=[FileExtensionValidator(['pdf', 'jpeg', 'jpg', 'png', 'bmp'])])
    verification_status = models.CharField(max_length=10, choices=Boolean_Choice, null=True, blank=True)

    class Meta:
        unique_together = ['company', 'financial_year']

    @classmethod
    def fetch_obj(cls, company_id, year):
        obj, _ = cls.objects.get_or_create(company_id=company_id, financial_year=year)
        return obj
