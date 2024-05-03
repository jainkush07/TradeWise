from django import forms
from django.db import models
from decimal import Decimal
from . models import *


class annualReportsDHRPImageForm(forms.ModelForm):
    class Meta:
        model = annualReportsDHRPImage
        exclude = ['stockProfileName', 'publish', 'created', 'updated', 'status', 'DRHPimage_heading']


class deck_imagesForm(forms.ModelForm):
    class Meta:
        model = deck_images
        exclude = ['page_image']


class deckForm(forms.ModelForm):
    class Meta:
        model = deck
        exclude = ['stockProfileName']


class highLightsForm(forms.ModelForm):
    class Meta:
        model = highLights
        exclude = ['stockProfileName']

class pitchupperimageForm(forms.ModelForm):
    class Meta:
        model = pitchupperimage
        exclude = ['publish', 'created', 'updated', 'status', 'stockProfileName']



class DateInput(forms.DateInput):
    input_type = 'date'

def round_decimal(value, places):
    if value is not None:
        return value.quantize(Decimal(10) ** -places)
    return value

class RoundingDecimalFormField(forms.DecimalField):
    def to_python(self, value):
        value = super(RoundingDecimalFormField, self).to_python(value)
        return round_decimal(value, self.decimal_places)

class RoundingDecimalModelField(models.DecimalField):
    def to_python(self, value):
        value = super(RoundingDecimalModelField, self).to_python(value)
        return round_decimal(value, self.decimal_places)

    def formfield(self, **kwargs):
        defaults = { 'form_class': RoundingDecimalFormField }
        defaults.update(kwargs)
        return super(RoundingDecimalModelField, self).formfield(**kwargs)

#
class financialCompanyUpdatesForm(forms.ModelForm):
    linkFrReport = forms.FileField(label='Upload Report File', widget=forms.FileInput(attrs={'class': "pdfInput"}))

    class Meta:
        model = financialCompanyUpdates
        exclude = ['stockProfileName', 'publish', 'created', 'updated', 'status', 'analyst', 'verifiedBy']

#
class annualReportsDHRPForm(forms.ModelForm):
    class Meta:
        model = annualReportsDHRP
        exclude = ['stockProfileName', 'publish', 'created', 'updated', 'status',]

#
class stockBalanceSheetForm(forms.ModelForm):
    cashAndCashEquivalents = RoundingDecimalFormField(max_digits = 19, decimal_places = 2, required=False)
    marketableSecurities = RoundingDecimalFormField(max_digits = 19, decimal_places = 2, required=False)
    bankBalanceOtherThanCashEquivalents = RoundingDecimalFormField(max_digits = 19, decimal_places = 2, required=False)
    cashAndShortTermInvestments = RoundingDecimalFormField(max_digits = 19, decimal_places = 2, required=False, help_text='Either enter a sum of these - (cashAndCashEquivalents, marketableSecurities, bankBalanceOtherThanCashEquivalents) or direct value - cashAndShortTermInvestments')
    totalReceivables = RoundingDecimalFormField(max_digits = 19, decimal_places = 2, required=False)
    totalInventory = RoundingDecimalFormField(max_digits = 19, decimal_places = 2, required=False)
    prepaidExpenses = RoundingDecimalFormField(max_digits = 19, decimal_places = 2, required=False)
    currentInvestments = RoundingDecimalFormField(max_digits = 19, decimal_places = 2, required=False)
    otherCurrentFinancialAssets = RoundingDecimalFormField(max_digits = 19, decimal_places = 2, required=False)
    loanAndAdvances = RoundingDecimalFormField(max_digits = 19, decimal_places = 2, required=False)
    deferredTaxAssest = RoundingDecimalFormField(max_digits = 19, decimal_places = 2, required=False)
    netPropertyORPlantOREquipment = RoundingDecimalFormField(max_digits = 19, decimal_places = 2, required=False)
    goodWill = RoundingDecimalFormField(max_digits = 19, decimal_places = 2, required=False)
    otherIntangibleAssests = RoundingDecimalFormField(max_digits = 19, decimal_places = 2, required=False)
    intangibleAssestsUnderDevelopment = RoundingDecimalFormField(max_digits = 19, decimal_places = 2, required=False)
    longTermInvestments = RoundingDecimalFormField(max_digits = 19, decimal_places = 2, required=False)
    deferredTaxAssetsNet = RoundingDecimalFormField(max_digits = 19, decimal_places = 2, required=False)
    otherNonCurrentAssets = RoundingDecimalFormField(max_digits = 19, decimal_places = 2, required=False)
    accountPayable = RoundingDecimalFormField(max_digits = 19, decimal_places = 2, required=False)
    totalDeposits = RoundingDecimalFormField(max_digits = 19, decimal_places = 2, required=False)
    currentPortionOfLongTermDebt = RoundingDecimalFormField(max_digits = 19, decimal_places = 2, required=False)
    unearnedRevenue = RoundingDecimalFormField(max_digits = 19, decimal_places = 2, required=False)
    currentPortionOfLeases = RoundingDecimalFormField(max_digits = 19, decimal_places = 2, required=False)
    otherCurrentLiabilities = RoundingDecimalFormField(max_digits = 19, decimal_places = 2, required=False)
    totalLongTermDebt = RoundingDecimalFormField(max_digits = 19, decimal_places = 2, required=False)
    longTermPortionOfLeases = RoundingDecimalFormField(max_digits = 19, decimal_places = 2, required=False)
    deferredTaxLiabilities = RoundingDecimalFormField(max_digits = 19, decimal_places = 2, required=False)
    otherNonCurrentLiabilities = RoundingDecimalFormField(max_digits = 19, decimal_places = 2, required=False)
    commonStock = RoundingDecimalFormField(max_digits = 19, decimal_places = 2, required=False)
    otherEquity = RoundingDecimalFormField(max_digits = 19, decimal_places = 2, required=False)
    reservesAndSurplus = RoundingDecimalFormField(max_digits = 19, decimal_places = 2, required=False)
    additionalPaidInCapital = RoundingDecimalFormField(max_digits = 19, decimal_places = 2, required=False)
    retainedEarnings  = RoundingDecimalFormField(max_digits = 19, decimal_places = 2, required=False)
    minorityInterest = RoundingDecimalFormField(max_digits = 19, decimal_places = 2, required=False)
    treasureStock = RoundingDecimalFormField(max_digits = 19, decimal_places = 2, required=False)
    comprehensiveIncAndOther = RoundingDecimalFormField(max_digits = 19, decimal_places = 2, required=False)
    totalCommonSharesOutstanding = RoundingDecimalFormField(max_digits = 19, decimal_places = 2, required=False)
    class Meta:
        model = stockBalanceSheet
        exclude = ['currentAssets','nonCurrentAssets','totalAssets', 'currentLiabilities', 'nonCurrentLiabilities', 'totalLiabilities', 'totalEquity','totalLiabilitiesShareHolderHistory', 'stockProfileName', 'publish', 'created', 'updated', 'status', 'analyst', 'verifiedBy']


#
class stockBalanceSheetTTMForm(forms.ModelForm):
    class Meta:
        model = stockBalanceSheetTTM
        exclude = ['currentAssets','nonCurrentAssets','totalAssets', 'currentLiabilities', 'nonCurrentLiabilities', 'totalLiabilities', 'totalEquity','totalLiabilitiesShareHolderHistory', 'stockProfileName', 'publish', 'created', 'updated', 'status', 'analyst', 'verifiedBy', 'year']



#
class recommendationOptionsForm(forms.ModelForm):
    class Meta:
        model = recommendationOptions
        exclude = ['publish', 'created', 'updated', 'status', 'analyst', 'verifiedBy']


# 2
class stockInvestmentChecklistForm(forms.ModelForm):
    class Meta:
        model = stockInvestmentChecklist
        exclude = ['stockProfileName', 'publish', 'created', 'updated', 'status', 'analyst', 'verifiedBy']


# 3
class stockAdminForm(forms.ModelForm):
    class Meta:
        model = stockAdmin
        fields = ['verifiedDetails','verifiedByAdmin','reportLive','researchReport']
# 4
class stockAdminSnapshotForm(forms.ModelForm):
    class Meta:
        model = stockAdmin
        fields = ['featuredImage','metaTitle','metaDescription','metaKeywords','tags']
#
class stockAdminKeyRatioForm(forms.ModelForm):
    class Meta:
        model = stockAdmin
        fields = ['metaTitlekeyRatio','metaDescriptionkeyRatio','metaKeywordskeyRatio','tagskeyRatio']

#5
class stockAdminPeersForm(forms.ModelForm):
    class Meta:
        model = stockAdmin
        fields = ['metaTitlePeers','metaDescriptionPeers','metaKeywordsPeers','tagsPeers']
#6
class stockAdminFinancialBalanceSheetForm(forms.ModelForm):
    class Meta:
        model = stockAdmin
        fields = ['metaTitleFinancialBalanceSheet','metaDescriptionFinancialBalanceSheet','metaKeywordsFinancialBalanceSheet','tagsFinancialBalanceSheet']

#
class stockAdminFinancialProfitLossForm(forms.ModelForm):
    class Meta:
        model = stockAdmin
        fields = ['metaTitleFinancialProfitLoss','metaDescriptionFinancialProfitLoss','metaKeywordsFinancialProfitLoss','tagsFinancialProfitLoss']

#
class stockAdminFinancialCashFlowForm(forms.ModelForm):
    class Meta:
        model = stockAdmin
        fields = ['metaTitleFinancialCashFlow','metaDescriptionFinancialCashFlow','metaKeywordsFinancialCashFlow','tagsFinancialCashFlow']

#6
class stockAdminOwnershipForm(forms.ModelForm):
    class Meta:
        model = stockAdmin
        fields = ['metaTitleOnwership','metaDescriptionOnwership','metaKeywordsOnwership','tagsOnwership']

#8
class stockAdminNewsForm(forms.ModelForm):
    class Meta:
        model = stockAdmin
        fields = ['metaTitleNews','metaDescriptionNews','metaKeywordsNews','tagsNews']
#9
class stockAdminEventsForm(forms.ModelForm):
    class Meta:
        model = stockAdmin
        fields = ['metaTitleEvents','metaDescriptionEvents','metaKeywordsEvents','tagsEvents']

#10
class stockIPOForm(forms.ModelForm):
    offerForSale = RoundingDecimalFormField(max_digits= 1000, decimal_places= 2, required=False)
    freshIssue = RoundingDecimalFormField(max_digits= 1000, decimal_places= 2, required=False)
    retailSubscription = RoundingDecimalFormField(max_digits= 1000, decimal_places= 20, required=False)
    QIBSubscription = RoundingDecimalFormField(max_digits= 1000, decimal_places= 20, required=False)
    NonInstitutionalSubscription = RoundingDecimalFormField(max_digits= 1000, decimal_places= 20, required=False)
    employeeQuota = RoundingDecimalFormField(max_digits= 1000, decimal_places= 20, required=False)
    NII = RoundingDecimalFormField(max_digits= 1000, decimal_places= 20, required=False)
    specialQuotaValue = RoundingDecimalFormField(max_digits= 1000, decimal_places= 20, required=False)
    totalSubscription = RoundingDecimalFormField(max_digits= 1000, decimal_places= 20, required=False)
    offerForSaleNoOfShares = RoundingDecimalFormField(max_digits= 1000, decimal_places= 2, required=False)
    freshIssueNoOfShares = RoundingDecimalFormField(max_digits= 1000, decimal_places= 2, required=False)
    totalIpoNoOfShares = RoundingDecimalFormField(max_digits= 1000, decimal_places= 2, required=False)
    class Meta:
        model = stockIPO
        exclude = ['stockProfileName', 'publish', 'created', 'updated', 'status', 'analyst', 'verifiedBy']
        widgets = {
            'listingDate': DateInput(),
            'openDate': DateInput(),
            'closedDate': DateInput(),
            'listingDateBox': DateInput(),
            'openTime': forms.TimeInput(attrs={'type': 'time'}),
            'closedTime': forms.TimeInput(attrs={'type': 'time'}),
            'listingTime': forms.TimeInput(attrs={'type': 'time'}),
        }

# 5
class stageOptionsForm(forms.ModelForm):
    class Meta:
        model = stageOptions
        exclude = ['publish', 'created', 'updated', 'status', 'analyst', 'verifiedBy']


# 6
class lookingForOptionsForm(forms.ModelForm):
    class Meta:
        model = lookingForOptions
        exclude = ['publish', 'created', 'updated', 'status', 'analyst', 'verifiedBy']


# 7
class currencySymbolOptionsForm(forms.ModelForm):
    class Meta:
        model = currencySymbolOptions
        exclude = ['publish', 'created', 'updated', 'status', 'analyst', 'verifiedBy']


# 8
class stockFundingForm(forms.ModelForm):
    class Meta:
        model = stockFunding
        exclude = ['stockProfileName', 'publish', 'created', 'updated', 'status', 'analyst', 'verifiedBy']


# 9
class stockFundingRoundsForm(forms.ModelForm):
    fundingAmount = RoundingDecimalFormField(max_digits = 19, decimal_places = 2, required=False)
    class Meta:
        model = stockFundingRounds
        exclude = ['stockProfileName', 'publish', 'created', 'updated', 'status', 'analyst', 'verifiedBy']
        widgets = {
            'dateOfInvestment': DateInput()
        }

# 10
class stockDetailsFormMergerAcquistion(forms.ModelForm):
    class Meta:
        model = stockDetails
        fields = ['mergerDescription', 'aquistionsDescription', 'investmentsDescription']

#
class stockDetailsSubsidiariesBusModelForm(forms.ModelForm):
    class Meta:
        model = stockDetails
        fields = ['subsidiaryDescription', 'businessModelDescription']

#
class stockDetailsProductForm(forms.ModelForm):
    class Meta:
        model = stockDetails
        fields = ['productsAndServicesDescription']

#
class stockDetailsAssestForm(forms.ModelForm):
    class Meta:
        model = stockDetails
        fields = ['assestsDescription']

#
class stockDetailsIndustryOverviewForm(forms.ModelForm):
    class Meta:
        model = stockDetails
        fields = ['industryStatisticsDescription', 'futureProspectsDescription','governmentInitiativesDescription']

#
class stockDetailsAwardForm(forms.ModelForm):
    class Meta:
        model = stockDetails
        fields = ['awardsDescription',]

#
class stockDetailsSSOTForm(forms.ModelForm):
    class Meta:
        model = stockDetails
        fields = ['strengthsDescription', 'shortcomingsDescription', 'opportunitiesDescription', 'threatsDescription']

#
class stockDetailsAboutForm(forms.ModelForm):
    class Meta:
        model = stockDetails
        fields = ['companyDescription',]

# 11
class stockRevenueBreakUpForm(forms.ModelForm):
    value = RoundingDecimalFormField(max_digits = 19, decimal_places = 2, required=False)
    class Meta:
        model = stockRevenueBreakUp
        exclude = ['stockProfileName', 'publish', 'created', 'updated', 'status', 'analyst', 'verifiedBy']


# 12
class profitabilityOptionsForm(forms.ModelForm):
    class Meta:
        model = profitabilityOptions
        exclude = ['publish', 'created', 'updated', 'status', 'analyst', 'verifiedBy']


# 13
class solvencyOptionsForm(forms.ModelForm):
    class Meta:
        model = solvencyOptions
        exclude = ['publish', 'created', 'updated', 'status', 'analyst', 'verifiedBy']


# 14
class growthOptionsForm(forms.ModelForm):
    class Meta:
        model = growthOptions
        exclude = ['publish', 'created', 'updated', 'status', 'analyst', 'verifiedBy']


# 15
class valuationOptionsForm(forms.ModelForm):
    class Meta:
        model = valuationOptions
        exclude = ['publish', 'created', 'updated', 'status', 'analyst', 'verifiedBy']


# 16
class businessTypeOptionsForm(forms.ModelForm):
    class Meta:
        model = businessTypeOptions
        exclude = ['publish', 'created', 'updated', 'status', 'analyst', 'verifiedBy']


# 17
class stockOwnershipForm(forms.ModelForm):
    class Meta:
        model = stockOwnership
        exclude = ['stockProfileName','publish', 'created', 'updated', 'status', 'analyst', 'verifiedBy']

# 18
class stockOwnershipDirectorForm(forms.ModelForm):
    class Meta:
        model = stockOwnershipDirector
        exclude = ['stockProfileName', 'publish', 'created', 'updated', 'status', 'analyst', 'verifiedBy']


# 19
class stockOwnershipInstitutionalForm(forms.ModelForm):
    percentageHolding = RoundingDecimalFormField(max_digits = 19, decimal_places = 2, required=False)
    class Meta:
        model = stockOwnershipInstitutional
        exclude = ['stockProfileName', 'publish', 'created', 'updated', 'status', 'analyst', 'verifiedBy']


# 20
class stockEventsCorpActionsForm(forms.ModelForm):
    class Meta:
        model = stockEventsCorpActions
        exclude = ['stockProfileName', 'publish', 'created', 'updated', 'status', 'analyst', 'verifiedBy']
        widgets = {
            'exDateFrCorporate': DateInput()
        }


# 21
class announcementTypeOptionsForm(forms.ModelForm):
    class Meta:
        model = announcementTypeOptions
        exclude = ['publish', 'created', 'updated', 'status', 'analyst', 'verifiedBy']



# 22
class stockEventsAnnouncementsForm(forms.ModelForm):
    class Meta:
        model = stockEventsAnnouncements
        exclude = [ 'stockProfileName', 'publish', 'created', 'updated', 'status', 'analyst', 'verifiedBy']
        widgets = {
            'dateFrAnnouncement': DateInput()
        }

# 23
# class legalOrdersOptionsForm(forms.ModelForm):
# 	class Meta:
# 		model = legalOrdersOptions
# 		exclude = ['publish', 'created', 'updated', 'status', 'analyst', 'verifiedBy']



# 24
class stockEventsLegalOrdersForm(forms.ModelForm):
    class Meta:
        model = stockEventsLegalOrders
        exclude = ['stockProfileName', 'publish', 'created', 'updated', 'status', 'analyst', 'verifiedBy']
        widgets = {
            'exDateFrLegalOrders': DateInput()
        }


##
class stockProfitAndLossTTMForm(forms.ModelForm):
    class Meta:
        model = stockProfitAndLossTTM
        exclude = ['year','totalRevenue','ebidta', 'pbit', 'pbt', 'netIncome', 'stockProfileName','publish', 'created', 'updated', 'status', 'analyst', 'verifiedBy']

##
class stockProfitAndLossForm(forms.ModelForm):
    revenue = RoundingDecimalFormField(max_digits = 19, decimal_places = 2, required=False)
    otherRevenue = RoundingDecimalFormField(max_digits = 19, decimal_places = 2, required=False)
    rawMaterials = RoundingDecimalFormField(max_digits = 19, decimal_places = 2, required=False)
    costOfGoodsSold = RoundingDecimalFormField(max_digits = 19, decimal_places = 2, required=False)
    powerAndFuelCost = RoundingDecimalFormField(max_digits = 19, decimal_places = 2, required=False)
    employeeCost = RoundingDecimalFormField(max_digits = 19, decimal_places = 2, required=False)
    sellingAndAdministrativeExpenses = RoundingDecimalFormField(max_digits = 19, decimal_places = 2, required=False)
    operatingAndOtherExpenses = RoundingDecimalFormField(max_digits = 19, decimal_places = 2, required=False)
    depreciationAndAmortization = RoundingDecimalFormField(max_digits = 19, decimal_places = 2, required=False)
    interestIncome = RoundingDecimalFormField(max_digits = 19, decimal_places = 2, required=False)
    interestExpense = RoundingDecimalFormField(max_digits = 19, decimal_places = 2, required=False)
    taxesAndOtherItems = RoundingDecimalFormField(max_digits = 19, decimal_places = 2, required=False)
    dilutedEPS = RoundingDecimalFormField(max_digits = 19, decimal_places = 2, required=False)
    basicEPS = RoundingDecimalFormField(max_digits = 19, decimal_places = 2, required=False)
    DPS = RoundingDecimalFormField(max_digits = 19, decimal_places = 2, required=False)
    payoutRatio = RoundingDecimalFormField(max_digits = 19, decimal_places = 2, required=False)
    class Meta:
        model = stockProfitAndLoss
        exclude = ['totalRevenue','ebidta', 'pbit', 'pbt', 'netIncome', 'stockProfileName','publish', 'created', 'updated', 'status', 'analyst', 'verifiedBy']

#
class stockCashFlowForm(forms.ModelForm):
    cashFromOperatingActivities = RoundingDecimalFormField(max_digits = 19, decimal_places = 2, required=False)
    cashFromInvestingActivities = RoundingDecimalFormField(max_digits = 19, decimal_places = 2, required=False)
    cashFromFinancingActivities = RoundingDecimalFormField(max_digits = 19, decimal_places = 2, required=False)
    changesInWorkingCapital = RoundingDecimalFormField(max_digits = 19, decimal_places = 2, required=False)
    capitalExpenditures = RoundingDecimalFormField(max_digits = 19, decimal_places = 2, required=False)
    freeCashFlow = RoundingDecimalFormField(max_digits = 19, decimal_places = 2, required=False)
    class Meta:
        model = stockCashFlow
        exclude = ['netChangeInCash', 'stockProfileName','publish', 'created', 'updated', 'status', 'analyst', 'verifiedBy']

#
class stockCashFlowTTMForm(forms.ModelForm):
    class Meta:
        model = stockCashFlowTTM
        exclude = ['netChangeInCash', 'stockProfileName','publish', 'created', 'updated', 'status', 'analyst', 'verifiedBy']


# old

class stockTransferDepositoryOptionsForm(forms.ModelForm):
    class Meta:
        model = stockTransferDepositoryOptions
        exclude = ['publish', 'created', 'updated', 'status', 'analyst', 'verifiedBy']

#
class saleTypeOptionsForm(forms.ModelForm):
    class Meta:
        model = saleTypeOptions
        exclude = ['publish', 'created', 'updated', 'status', 'analyst', 'verifiedBy']

#
class stockBasicDetailForm(forms.ModelForm):
    class Meta:
        model = stockBasicDetail
        exclude = ['publish', 'created', 'updated', 'status', 'analyst', 'verifiedBy', 'investRaisedPercent','daysLeft', 'bgImageForStartup']
        required = (
            'stockName', 'ticker',
        )
        widgets = {
            'launch_Date': DateInput(),
            'end_Date': DateInput(),
            'stockTransferDepository': forms.CheckboxSelectMultiple(),
            'saleType': forms.CheckboxSelectMultiple(),
        }

#
class sectorOptionsForm(forms.ModelForm):
    class Meta:
        model = sectorOptions
        exclude = ['publish', 'created', 'updated', 'status', 'analyst', 'verifiedBy']

#
class subSectorOptionsForm(forms.ModelForm):
    class Meta:
        model = subSectorOptions
        exclude = ['publish', 'created', 'updated', 'status', 'analyst', 'verifiedBy']

#
class categoryOptionsForm(forms.ModelForm):
    class Meta:
        model = categoryOptions
        exclude = ['fetchScreenerPrice', 'publish', 'created', 'updated', 'status', 'analyst', 'verifiedBy']

#
class typeOfCompanyOptionsForm(forms.ModelForm):
    class Meta:
        model = typeOfCompanyOptions
        exclude = ['publish', 'created', 'updated', 'status', 'analyst', 'verifiedBy']

#
class countryOptionsForm(forms.ModelForm):
    class Meta:
        model = countryOptions
        exclude = ['publish', 'created', 'updated', 'status', 'analyst','verifiedBy']

#
class stockEssentialsForm(forms.ModelForm):
    salesGrowthRateOfXYear = RoundingDecimalFormField(max_digits = 19, decimal_places = 2, required=False, help_text='SalesGrowthRateOfXYear - This value is used for calculating Intrinsic Value.')
    faceValue = RoundingDecimalFormField(max_digits = 19, decimal_places = 2, required=False)
    balance_with_RBI = RoundingDecimalFormField(max_digits=1000, decimal_places=20, required=False)
    preference_equity = RoundingDecimalFormField(max_digits=1000, decimal_places=20, required=False)
    class Meta:
        model = stockEssentials
        exclude = ['enterpriseValue', 'listingDate', 'researchLastUpdatedOn', 'stockProfileName','publish', 'created', 'updated', 'status', 'analyst', 'verifiedBy', 'typeOfCompany','countryRegisteredIn','registeredDate','stockExchangeReferenceSymbol','regOffice','website']
        widgets = {
            'registeredDate': DateInput()
        }

#
class stockEssentialsBottomForm(forms.ModelForm):
    class Meta:
        model = stockEssentials
        fields = ['typeOfCompany','countryRegisteredIn','registeredDate','researchLastUpdatedOn','listingDate', 'stockExchangeReferenceSymbol','regOffice','website']
        widgets = {
            'registeredDate': DateInput(),
            'researchLastUpdatedOn': DateInput(),
            'listingDate': DateInput()
        }

#
class bookValueDataForm(forms.ModelForm):
    bookValue = RoundingDecimalFormField(max_digits = 19, decimal_places = 2, required=False)
    class Meta:
        model = bookValueData
        exclude = ['stockProfileName','publish', 'created', 'updated', 'status', 'analyst', 'verifiedBy']

#
class managementOptionsForm(forms.ModelForm):
    class Meta:
        model = managementOptions
        exclude = ['publish', 'created', 'updated', 'status', 'analyst', 'verifiedBy']

#
class accountingPracticeOptionsForm(forms.ModelForm):
    class Meta:
        model = accountingPracticeOptions
        exclude = ['publish', 'created', 'updated', 'status', 'analyst', 'verifiedBy']


#
class stockOwnershipPatternForm(forms.ModelForm):
    totalPromoterholdingValue = RoundingDecimalFormField(max_digits = 19, decimal_places = 2, required=False)
    mutualFundHoldingValue = RoundingDecimalFormField(max_digits = 19, decimal_places = 2, required=False)
    domesticInstitutionalHoldingsValue = RoundingDecimalFormField(max_digits = 19, decimal_places = 2, required=False)
    foreignInstitutionalHoldingsValue = RoundingDecimalFormField(max_digits = 19, decimal_places = 2, required=False)
    institutionalHolding = RoundingDecimalFormField(max_digits = 19, decimal_places = 2, required=False)
    publicInstitutionalHoldings = RoundingDecimalFormField(max_digits = 19, decimal_places = 2, required=False)
    nonPublicInstitutionalHoldings = RoundingDecimalFormField(max_digits = 19, decimal_places = 2, required=False)
    retail = RoundingDecimalFormField(max_digits = 19, decimal_places = 2, required=False)
    employees = RoundingDecimalFormField(max_digits = 19, decimal_places = 2, required=False)
    custodians = RoundingDecimalFormField(max_digits = 19, decimal_places = 2, required=False)
    promoters = RoundingDecimalFormField(max_digits = 19, decimal_places = 2, required=False)
    privatePublicInvestmenFirmVCs = RoundingDecimalFormField(max_digits = 19, decimal_places = 2, required=False)
    others = RoundingDecimalFormField(max_digits = 19, decimal_places = 2, required=False)

    class Meta:
        model = stockOwnershipPattern
        exclude = ['stockProfileName','publish', 'created', 'updated', 'status', 'analyst', 'verifiedBy']

#
class stockNewsForm(forms.ModelForm):
    class Meta:
        model = stockNews
        exclude = ['websiteThumbnail','stockProfileName','publish', 'created', 'updated', 'status', 'analyst', 'verifiedBy']
        widgets = {
            'newsPublishDate': DateInput()
        }
#

#
class websiteMasterForm(forms.ModelForm):
    class Meta:
        model = websiteMaster
        exclude = ['stockProfileName', 'publish', 'created', 'updated', 'status', 'analyst', 'verifiedBy']

#
class stockEventsTypeOptionsForm(forms.ModelForm):
    class Meta:
        model = stockEventsTypeOptions
        exclude = ['stockProfileName','publish', 'created', 'updated', 'status', 'analyst', 'verifiedBy']

#
class dividendTypeOptionsForm(forms.ModelForm):
    class Meta:
        model = dividendTypeOptions
        exclude = ['publish', 'created', 'updated', 'status', 'analyst', 'verifiedBy']

#
class stockEventsDividendForm(forms.ModelForm):
    dividendShare = RoundingDecimalFormField(max_digits = 19, decimal_places = 2, required=False)
    class Meta:
        model = stockEventsDividend
        exclude = ['stockProfileName', 'publish', 'created', 'updated', 'status', 'analyst', 'verifiedBy']
        widgets = {
            'exDateFrDividend': DateInput()
        }
#
class corpActionsOptionsForm(forms.ModelForm):
    class Meta:
        model = corpActionsOptions
        exclude = ['publish', 'created', 'updated', 'status', 'analyst', 'verifiedBy']

#
class stockSolvencyForm(forms.ModelForm):
    class Meta:
        model = stockSolvency
        exclude = ['stockProfileName', 'publish', 'created', 'updated', 'status', 'analyst', 'verifiedBy']

#
class stockOperatingEfficiencyForm(forms.ModelForm):
    class Meta:
        model = stockOperatingEfficiency
        exclude = ['stockProfileName', 'publish', 'created', 'updated', 'status', 'analyst', 'verifiedBy']

#
class stockRatiosForm(forms.ModelForm):
    class Meta:
        model = stockRatios
        exclude = ['stockProfileName', 'publish', 'created', 'updated', 'status', 'analyst', 'verifiedBy']


#
class stockPeersForm(forms.ModelForm):
    class Meta:
        model = stockPeers
        exclude = ['stockProfileName', 'publish', 'created', 'updated', 'status', 'analyst', 'verifiedBy']


#
class financialStatementsFrBalanceSheetForm(forms.ModelForm):
    class Meta:
        model = financialStatementsFrBalanceSheet
        exclude = ['stockProfileName','publish', 'created', 'updated', 'status', 'analyst', 'verifiedBy']

#
class financialFigureUnitsForm(forms.ModelForm):
    class Meta:
        model = financialFigureUnits
        exclude = ['stockProfileName','analyst', 'verifiedBy', 'publish', 'created', 'updated', 'status']

#
class financialStatementsFrProfitAndLossForm(forms.ModelForm):
    class Meta:
        model = financialStatementsFrProfitAndLoss
        exclude = ['stockProfileName', 'publish', 'created', 'updated', 'status', 'analyst', 'verifiedBy']

#
class financialStatementsFrCashFlowForm(forms.ModelForm):
    class Meta:
        model = financialStatementsFrCashFlow
        exclude = ['stockProfileName', 'publish', 'created', 'updated', 'status', 'analyst', 'verifiedBy']

#
class stockGrowthForm(forms.ModelForm):
    class Meta:
        model = stockGrowth
        exclude = ['stockProfileName', 'publish', 'created', 'updated', 'status', 'analyst', 'verifiedBy']

#
class sectorSpecificRatiosForm(forms.ModelForm):
    class Meta:
        model = sectorSpecificRatios
        exclude = ['stockProfileName', 'publish', 'created', 'updated', 'status', 'analyst', 'verifiedBy']

#
class leadGenerationDetailsForm(forms.ModelForm):
    class Meta:
        model = leadGenerationDetails
        exclude = ['stockProfileName', 'publish', 'created', 'updated', 'status']
        required = (
            'phoneNo', 'agreedToTC',
        )


#
class peersCompanyLinkingForm(forms.ModelForm):
    class Meta:
        model = peersCompanyLinking
        exclude = ['stockProfileName', 'publish', 'created', 'updated', 'status']

#
class peersCompanyLinkingForBankNBFCForm(forms.ModelForm):
    class Meta:
        model = peersCompanyLinkingForBankNBFC
        exclude = ['stockProfileName', 'publish', 'created', 'updated', 'status']

#
class industrySpecificGraphForm(forms.ModelForm):
    class Meta:
        model = industrySpecificGraphs
        exclude = ['stockProfileName', 'publish', 'created', 'updated', 'status', 'analyst', 'verifiedBy']


#
class industrySpecificGraphValsForm(forms.ModelForm):
    class Meta:
        model = industrySpecificGraphsValues
        exclude = ['valuesFor', 'analyst',]


#
class currentRateOfbondYieldForm(forms.ModelForm):
    value = RoundingDecimalFormField(max_digits = 19, decimal_places = 2, required=True)
    class Meta:
        model = currentRateOfbondYield
        exclude = ['publish', 'updated', 'status', 'analyst', 'verifiedBy']

class stockListHeadingForm(forms.ModelForm):
    class Meta:
        model = stockListHeading
        exclude = ['publish', 'updated', 'created', 'status',]

#
class stockAppSpecificForm(forms.ModelForm):
    class Meta:
        model = stockAppSpecific
        exclude = ['publish', 'created', 'updated', 'status',]

#
class pubDraftStockForm(forms.ModelForm):
    class Meta:
        model = stockBasicDetail
        fields = ['status',]

#
class foundingRoundsFigureUnitsForm(forms.ModelForm):
    class Meta:
        model = foundingRoundsFigureUnits
        exclude = ['stockProfileName','analyst', 'verifiedBy', 'publish', 'created', 'updated', 'status']

#
class fundingDetailsVisibilityForm(forms.ModelForm):
    class Meta:
        model = fundingDetailsVisibility
        exclude = ['stockProfileName','publish', 'created', 'updated', 'status']

#
class benGrahamOrDCFForm(forms.ModelForm):
    class Meta:
        model = benGrahamOrDCF
        exclude = ['stockProfileName',]

#
class stockListDMForm(forms.ModelForm):
    class Meta:
        model = stockListDM
        exclude = ['publish', 'created', 'updated', 'status']


# #
#description field for SEO - starts 
class stockFinBalanceSheetSEOForm(forms.ModelForm):
    class Meta:
        model = stockFinBalanceSheetSEO
        exclude = ['stockProfileName', 'publish', 'created', 'updated', 'status', 'analyst', 'verifiedBy']


class stockNewsSEOForm(forms.ModelForm):
    class Meta:
        model = stockNewsSEO
        exclude = ['stockProfileName', 'publish', 'created', 'updated', 'status', 'analyst', 'verifiedBy']


class stockEventsSEOForm(forms.ModelForm):
    class Meta:
        model = stockEventsSEO
        exclude = ['stockProfileName', 'publish', 'created', 'updated', 'status', 'analyst', 'verifiedBy']

#description field for SEO - ends


#bank - nbfc's 


##
class stockProfitAndLossBankNBFCForm(forms.ModelForm):
    netInterestIncome = RoundingDecimalFormField(max_digits = 19, decimal_places = 2, required=False)
    totalRevenue = RoundingDecimalFormField(max_digits = 19, decimal_places = 2, required=False)
    cogsMinusRepairsMaintenance = RoundingDecimalFormField(max_digits = 19, decimal_places = 2, required=False)
    salariesAndEmpBenefits = RoundingDecimalFormField(max_digits = 19, decimal_places = 2, required=False)
    cospMinusAdvertisingPlusRent = RoundingDecimalFormField(max_digits = 19, decimal_places = 2, required=False)
    otherOperatingExp = RoundingDecimalFormField(max_digits = 19, decimal_places = 2, required=False)
    depreciationAndAmortization = RoundingDecimalFormField(max_digits = 19, decimal_places = 2, required=False)
    otherItems = RoundingDecimalFormField(max_digits = 19, decimal_places = 2, required=False)
    shareOfProfitLossOfJoinVentures = RoundingDecimalFormField(max_digits = 19, decimal_places = 2, required=False)
    taxesAndOtherItems = RoundingDecimalFormField(max_digits = 19, decimal_places = 2, required=False)
    dilutedEPS = RoundingDecimalFormField(max_digits = 19, decimal_places = 2, required=False)
    basicEPS = RoundingDecimalFormField(max_digits = 19, decimal_places = 2, required=False)
    DPS = RoundingDecimalFormField(max_digits = 19, decimal_places = 2, required=False)
    class Meta:
        model = stockProfitAndLossBankNBFC
        exclude = ['grossProfit','ebidta', 'pbit', 'pbt', 'netIncome', 'payoutRatio', 'stockProfileName','publish', 'created', 'updated', 'status', 'analyst', 'verifiedBy']


#
class stockBalanceSheetBankNBFCForm(forms.ModelForm):
    cashAndCashEquivalents = RoundingDecimalFormField(max_digits = 19, decimal_places = 2, required=False)
    longTermInvestments = RoundingDecimalFormField(max_digits = 19, decimal_places = 2, required=False)
    loans = RoundingDecimalFormField(max_digits = 19, decimal_places = 2, required=False)
    otherReceivables = RoundingDecimalFormField(max_digits = 19, decimal_places = 2, required=False, help_text='Either enter a sum of these - (cashAndCashEquivalents, marketableSecurities, bankBalanceOtherThanCashEquivalents) or direct value - cashAndShortTermInvestments')
    otherCurrentAssets = RoundingDecimalFormField(max_digits = 19, decimal_places = 2, required=False)
    fixedAssests = RoundingDecimalFormField(max_digits = 19, decimal_places = 2, required=False)
    rightOfUseAsset = RoundingDecimalFormField(max_digits = 19, decimal_places = 2, required=False)
    goodWillOnConsolidation = RoundingDecimalFormField(max_digits = 19, decimal_places = 2, required=False)
    nonCurrentInvestments = RoundingDecimalFormField(max_digits = 19, decimal_places = 2, required=False)
    deferredCharges = RoundingDecimalFormField(max_digits = 19, decimal_places = 2, required=False)
    deferredTaxAssets = RoundingDecimalFormField(max_digits = 19, decimal_places = 2, required=False)
    otherNonCurrentAssets = RoundingDecimalFormField(max_digits = 19, decimal_places = 2, required=False)
    equityShareCapital = RoundingDecimalFormField(max_digits = 19, decimal_places = 2, required=False)
    reservesAndSurplus = RoundingDecimalFormField(max_digits = 19, decimal_places = 2, required=False)
    minorityInterest = RoundingDecimalFormField(max_digits = 19, decimal_places = 2, required=False)
    shareApplicationMoneyPendingAllotment = RoundingDecimalFormField(max_digits = 19, decimal_places = 2, required=False)
    otherEquity = RoundingDecimalFormField(max_digits = 19, decimal_places = 2, required=False)
    longTermBorrowings = RoundingDecimalFormField(max_digits = 19, decimal_places = 2, required=False)
    deferredTaxLiabilities = RoundingDecimalFormField(max_digits = 19, decimal_places = 2, required=False)
    otherFinancialLiabilities = RoundingDecimalFormField(max_digits = 19, decimal_places = 2, required=False)
    otherNonFinancialLiabilities = RoundingDecimalFormField(max_digits = 19, decimal_places = 2, required=False)
    shortTermProvisions = RoundingDecimalFormField(max_digits = 19, decimal_places = 2, required=False)
    longTermProvisions = RoundingDecimalFormField(max_digits = 19, decimal_places = 2, required=False)
    shortTermBorrowings = RoundingDecimalFormField(max_digits = 19, decimal_places = 2, required=False)
    tradePayable = RoundingDecimalFormField(max_digits = 19, decimal_places = 2, required=False)
    leaseLiability = RoundingDecimalFormField(max_digits = 19, decimal_places = 2, required=False)
    otherNonCurrentLiabilities = RoundingDecimalFormField(max_digits = 19, decimal_places = 2, required=False)
    otherCurrentLiabilities = RoundingDecimalFormField(max_digits = 19, decimal_places = 2, required=False)
    currentPortionOfLongTermDebt = RoundingDecimalFormField(max_digits = 19, decimal_places = 2, required=False)
    totalCommonSharesOutstanding = RoundingDecimalFormField(max_digits = 19, decimal_places = 2, required=False)

    class Meta:
        model = stockBalanceSheetBankNBFC
        exclude = ['financialAssets','nonFinancialAssets','totalAssets', 'totalEquity', 'totalLiabilities', 'totalLiabilitiesAndShareHoldingEquity', 'stockProfileName', 'publish', 'created', 'updated', 'status', 'analyst', 'verifiedBy']


#
class valuationRatioForm(forms.ModelForm):
    class Meta:
        model = valuationRatio
        exclude = ('stockProfileName','author', 'publish' ,'created','updated','status')

#
class peerLinkingYearlyDataForm(forms.ModelForm):
    cashAndShortTermEquivalents = RoundingDecimalFormField(max_digits=1000, decimal_places=20, required=False)
    PreferenceEquity = RoundingDecimalFormField(max_digits=1000, decimal_places=20, required=False)
    totalMinorityInterest = RoundingDecimalFormField(max_digits=1000, decimal_places=20, required=False)
    longTermMarketableSecurities = RoundingDecimalFormField(max_digits=1000, decimal_places=20, required=False)
    bookValue = RoundingDecimalFormField(max_digits=1000, decimal_places=20, required=False)
    currentPrice = RoundingDecimalFormField(max_digits=1000, decimal_places=20, required=False)
    revenue = RoundingDecimalFormField(max_digits=1000, decimal_places=20, required=False)
    netProfitMargin = RoundingDecimalFormField(max_digits=1000, decimal_places=20, required=False)
    assetTurnoverRation = RoundingDecimalFormField(max_digits=1000, decimal_places=20, required=False)
    totalFixedAssetTurnoverRatio = RoundingDecimalFormField(max_digits=1000, decimal_places=20, required=False)
    ROE = RoundingDecimalFormField(max_digits=1000, decimal_places=20, required=False)
    ROCE = RoundingDecimalFormField(max_digits=1000, decimal_places=20, required=False)
    deptToEquity = RoundingDecimalFormField(max_digits=1000, decimal_places=20, required=False)
    peRatio = RoundingDecimalFormField(max_digits=1000, decimal_places=20, required=False)
    pbRatio = RoundingDecimalFormField(max_digits=1000, decimal_places=20, required=False)
    marketCap = RoundingDecimalFormField(max_digits=1000, decimal_places=20, required=False)
    marketCapBySales = RoundingDecimalFormField(max_digits=1000, decimal_places=20, required=False)
    enterpriseValue = RoundingDecimalFormField(max_digits=1000, decimal_places=20, required=False)
    evByEbitda = RoundingDecimalFormField(max_digits=1000, decimal_places=20, required=False)
    cashAndShortTermCashEquivalents = RoundingDecimalFormField(max_digits=1000, decimal_places=20, required=False)
    class Meta:
        model = peerLinkingYearlyData
        exclude = ('screenerCompany','analyst', 'author', 'publish' ,'created','updated','status')


#
class peerLinkingYearlyDataForBankNBFCForm(forms.ModelForm):
    tier1CapitalRatio = RoundingDecimalFormField(max_digits=1000, decimal_places=20, required=False)
    CAR = RoundingDecimalFormField(max_digits=1000, decimal_places=20, required=False)
    netNPA = RoundingDecimalFormField(max_digits=1000, decimal_places=20, required=False)
    grossNPA = RoundingDecimalFormField(max_digits=1000, decimal_places=20, required=False)
    CASA = RoundingDecimalFormField(max_digits=1000, decimal_places=20, required=False)
    tier1CapitalRatio = RoundingDecimalFormField(max_digits=1000, decimal_places=20, required=False)
    tier2CapitalRatio = RoundingDecimalFormField(max_digits=1000, decimal_places=20, required=False)
    totalAMU = RoundingDecimalFormField(max_digits=1000, decimal_places=20, required=False)
    RORWA = RoundingDecimalFormField(max_digits=1000, decimal_places=20, required=False)
    # numberOfShares = RoundingDecimalFormField(max_digits=1000, decimal_places=20, required=False)
    intangibleAssests = RoundingDecimalFormField(max_digits=1000, decimal_places=20, required=False)
    goodwill = RoundingDecimalFormField(max_digits=1000, decimal_places=20, required=False)
    loanLossProvision = RoundingDecimalFormField(max_digits=1000, decimal_places=20, required=False)
    netInterestIncome = RoundingDecimalFormField(max_digits=1000, decimal_places=20, required=False)
    revenue = RoundingDecimalFormField(max_digits=1000, decimal_places=20, required=False)
    roa = RoundingDecimalFormField(max_digits=1000, decimal_places=20, required=False)
    netProfitMargin = RoundingDecimalFormField(max_digits=1000, decimal_places=20, required=False)
    assetTurnOverRatio = RoundingDecimalFormField(max_digits=1000, decimal_places=20, required=False)
    ROE = RoundingDecimalFormField(max_digits=1000, decimal_places=20, required=False)
    peRatio = RoundingDecimalFormField(max_digits=1000, decimal_places=20, required=False)
    pbRatio = RoundingDecimalFormField(max_digits=1000, decimal_places=20, required=False)
    marketCap = RoundingDecimalFormField(max_digits=1000, decimal_places=20, required=False)
    NIM = RoundingDecimalFormField(max_digits=1000, decimal_places=20, required=False)
    DERatio = RoundingDecimalFormField(max_digits=1000, decimal_places=20, required=False)
    priceByTangibleBookRatio = RoundingDecimalFormField(max_digits=1000, decimal_places=20, required=False)
    class Meta:
        model = peerLinkingYearlyDataForBankNBFC
        exclude = ('screenerCompany','analyst', 'author', 'publish' ,'created','updated','status')

#
class iDescriptionForKeyRatiosForm(forms.ModelForm):
    class Meta:
        model = iDescriptionForKeyRatios
        exclude = ('created','updated', 'status', 'analyst' ,'verifiedBy',)

#
class bankNBFCRatioDescriptionForm(forms.ModelForm):
    class Meta:
        model = bankNBFCRatioDescription
        exclude = ('stockProfileName','author', 'publish' ,'created','updated','status')

#
class researchReportFAQsForm(forms.ModelForm):
    class Meta:
        model = researchReportFAQs
        exclude = ('stockProfileName','author', 'publish' ,'created','updated','status')

#
class totalShareYearlyDataForm(forms.ModelForm):
    class Meta:
        model = totalShareYearlyData
        exclude = ('stockProfileName', 'author', 'publish', 'created', 'updated', 'status')

#
class valuesRBIStandardsForm(forms.ModelForm):
    RBI_CARValue = RoundingDecimalFormField(max_digits = 1000, decimal_places = 20, required=False)
    RBI_tier1Value = RoundingDecimalFormField(max_digits = 1000, decimal_places = 20, required=False)
    RBI_tier2Value = RoundingDecimalFormField(max_digits = 1000, decimal_places = 20, required=False)
    RBI_maintenanceMarginRequirement = RoundingDecimalFormField(max_digits = 1000, decimal_places = 20, required=False)

    class Meta:
        model = valuesRBIStandards
        exclude = ['publish', 'created', 'updated', 'status',]

#
class companyRatiosForm(forms.ModelForm):
    carValue = RoundingDecimalFormField(max_digits = 1000, decimal_places = 20, required=False)
    tier1Value = RoundingDecimalFormField(max_digits = 1000, decimal_places = 20, required=False)
    tier2Value = RoundingDecimalFormField(max_digits = 1000, decimal_places = 20, required=False)
    maintenanceMarginRequirement = RoundingDecimalFormField(max_digits = 1000, decimal_places = 20, required=False)

    class Meta:
        model = companyRatios
        exclude = ['stockProfileName','publish', 'created', 'updated', 'status',]

#
class regulatoryRatiosForm(forms.ModelForm):
    class Meta:
        model = regulatoryRatios
        exclude = ('author', 'publish' ,'created','updated','status','stockProfileName')


#
class stockPeersDescriptionForBankNBFCForm(forms.ModelForm):
    class Meta:
        model = stockPeersDescriptionForBankNBFC
        exclude = ('analyst', 'verifiedBy', 'publish' ,'created','updated','status','stockProfileName')


#
class commonFAQForm(forms.ModelForm):
    class Meta:
        model = commonFAQ
        exclude = ('author', 'publish' ,'created','updated','status')



class stockBalanceSheetBankNBFCTTMForm(forms.ModelForm):
    class Meta:
        model = stockBalanceSheetBankNBFCTTM
        exclude = ('analyst', 'verifiedBy', 'author', 'publish' ,'created','updated','status','stockProfileName', 'year', )


class stockProfitAndLossBankNBFCTTMForm(forms.ModelForm):
    class Meta:
        model = stockProfitAndLossBankNBFCTTM
        exclude = ('analyst', 'verifiedBy', 'author', 'publish' ,'created','updated','status','stockProfileName', 'year', )



class welcomeLoginPopupForm(forms.ModelForm):
    class Meta:
        model = welcomeLoginPopup
        exclude = ('author','publish','created','updated','status')


class stockDeckAndDocsForm(forms.ModelForm):
    class Meta:
        model = stockDeckAndDocs
        exclude = ('stockProfileName','author','publish','created','updated','status')



