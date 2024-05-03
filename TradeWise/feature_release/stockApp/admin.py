from django.contrib import admin
from . models import *
from django_summernote.admin import SummernoteModelAdmin
from import_export.admin import ImportExportModelAdmin

admin.site.site_header = "Planify PreIPO"
admin.site.site_title = "Planify PreIPO"
admin.site.index_title = "Welcome to Planify PreIPO(Powered by Inwoin)"

def approvePost(modeladmin, request, queryset):
	for post in queryset:
		post.status = 'published'
		post.save()
approvePost.short_description = 'Approve Selected'


def draftPost(modeladmin, request, queryset):
	for post in queryset:
		post.status = 'draft'
		post.save()
draftPost.short_description = 'Draft Selected'



# 2 finacialCompanyUpdates      ////
@admin.register(financialCompanyUpdates)
class finacialCompanyUpdatesImport(ImportExportModelAdmin):
	actions = [approvePost, draftPost,]
	def save_model(self, request, obj, form, change):
		obj.analyst = request.user
		super().save_model(request, obj, form, change)

# 3 stockBalanceSheet
@admin.register(stockBalanceSheet)
class stockBalanceSheetImport(ImportExportModelAdmin, SummernoteModelAdmin):
	actions = [approvePost, draftPost,]
	def save_model(self, request, obj, form, change):
		obj.analyst = request.user
		super().save_model(request, obj, form, change)

# 1     recommendationOptions
@admin.register(recommendationOptions)
class recommendationOptionsImport(ImportExportModelAdmin, SummernoteModelAdmin):
	actions = [approvePost, draftPost,]
	def save_model(self, request, obj, form, change):
		obj.analyst = request.user
		super().save_model(request, obj, form, change)

# 2       stockInvestmentChecklist
@admin.register(stockInvestmentChecklist)
class stockInvestmentChecklistImport(ImportExportModelAdmin, SummernoteModelAdmin):
	actions = [approvePost, draftPost,]
	def save_model(self, request, obj, form, change):
		obj.analyst = request.user
		super().save_model(request, obj, form, change)

# 3  stockAdmin     ////
@admin.register(stockAdmin)
class stockAdminImport(ImportExportModelAdmin, SummernoteModelAdmin):
	summernote_fields = ('metaDescription', 'metaKeywords')
	actions = [approvePost, draftPost,]
	def save_model(self, request, obj, form, change):
		obj.analyst = request.user
		super().save_model(request, obj, form, change)

# 4  stockIPO    ////
@admin.register(stockIPO)
class stockIPOImport(ImportExportModelAdmin, SummernoteModelAdmin):
	summernote_fields = ('IPODescription',)
	actions = [approvePost, draftPost,]
	def save_model(self, request, obj, form, change):
		obj.analyst = request.user
		super().save_model(request, obj, form, change)

# 5   stageOptions
@admin.register(stageOptions)
class stageOptionsImport(ImportExportModelAdmin, SummernoteModelAdmin):
	actions = [approvePost, draftPost,]
	def save_model(self, request, obj, form, change):
		obj.analyst = request.user
		super().save_model(request, obj, form, change)

# 6  lookingForOptions
@admin.register(lookingForOptions)
class lookingForOptionsImport(ImportExportModelAdmin, SummernoteModelAdmin):
	actions = [approvePost, draftPost,]
	def save_model(self, request, obj, form, change):
		obj.analyst = request.user
		super().save_model(request, obj, form, change)

# 7    currencySymbolOptions
@admin.register(currencySymbolOptions)
class currencySymbolOptionsImport(ImportExportModelAdmin, SummernoteModelAdmin):
	actions = [approvePost, draftPost,]
	def save_model(self, request, obj, form, change):
		obj.analyst = request.user
		super().save_model(request, obj, form, change)

# 8  stockFunding
@admin.register(stockFunding)
class stockFundingImport(ImportExportModelAdmin, SummernoteModelAdmin):
	actions = [approvePost, draftPost,]
	def save_model(self, request, obj, form, change):
		obj.analyst = request.user
		super().save_model(request, obj, form, change)

# 9    stockFundingRounds
@admin.register(stockFundingRounds)
class stockFundingRoundsImport(ImportExportModelAdmin, SummernoteModelAdmin):
	actions = [approvePost, draftPost,]
	def save_model(self, request, obj, form, change):
		obj.analyst = request.user
		super().save_model(request, obj, form, change)

# 10  stockDetails          ////
@admin.register(stockDetails)
class stockDetailsImport(ImportExportModelAdmin, SummernoteModelAdmin):
	summernote_fields = ('companyDescription',
		'mergerDescription',
		'aquistionsDescription',
		'investmentsDescription',
		'subsidiaryDescription',
		'businessModelDescription',
		'productsAndServicesDescription',
		'assestsDescription',
		'industryStatisticsDescription',
		'futureProspectsDescription',
		'governmentInitiativesDescription',
		'awardsDescription',
		'strengthsDescription',
		'shortcommingsDescription',
		'opportunitiesDescription',
		'threatsDescription',
		'planifyViewDescription',
		'ratingDescription',                                            
		)

	actions = [approvePost, draftPost,]
	def save_model(self, request, obj, form, change):
		obj.analyst = request.user
		super().save_model(request, obj, form, change)

# 11   stockRevenueBreakUp
@admin.register(stockRevenueBreakUp)
class stockRevenueBreakUpImport(ImportExportModelAdmin, SummernoteModelAdmin):
	actions = [approvePost, draftPost,]
	def save_model(self, request, obj, form, change):
		obj.analyst = request.user
		super().save_model(request, obj, form, change)

# 12        profitabilityOptions
@admin.register(profitabilityOptions)
class profitabilityOptionsImport(ImportExportModelAdmin, SummernoteModelAdmin):
	actions = [approvePost, draftPost,]
	def save_model(self, request, obj, form, change):
		obj.analyst = request.user
		super().save_model(request, obj, form, change)

# 13   solvencyOptions
@admin.register(solvencyOptions)
class solvencyOptionsImport(ImportExportModelAdmin, SummernoteModelAdmin):
	actions = [approvePost, draftPost,]
	def save_model(self, request, obj, form, change):
		obj.analyst = request.user
		super().save_model(request, obj, form, change)

# 14   growthOptions
@admin.register(growthOptions)
class growthOptionsImport(ImportExportModelAdmin, SummernoteModelAdmin):
	actions = [approvePost, draftPost,]
	def save_model(self, request, obj, form, change):
		obj.analyst = request.user
		super().save_model(request, obj, form, change)

# 15  valuationOptions
@admin.register(valuationOptions)
class valuationOptionsImport(ImportExportModelAdmin, SummernoteModelAdmin):
	actions = [approvePost, draftPost,]
	def save_model(self, request, obj, form, change):
		obj.analyst = request.user
		super().save_model(request, obj, form, change)

# 16   businessTypeOptions
@admin.register(businessTypeOptions)
class businessTypeOptionsImport(ImportExportModelAdmin, SummernoteModelAdmin):
	actions = [approvePost, draftPost,]
	def save_model(self, request, obj, form, change):
		obj.analyst = request.user
		super().save_model(request, obj, form, change)

# 17 stockOwnership           ////
@admin.register(stockOwnership)
class stockOwnershipImport(ImportExportModelAdmin, SummernoteModelAdmin):
	summernote_fields = (
		'ownershipDescription',
		'totalPromoterHoldingDescription',
		'pledgePromoterHoldingDescription',
		'mutualFundIntitutionalHoldingDescription',
		'foreignInstutionalHoldingDescription',
		'domesticInstutionalHoldingDescription',
		'description',                            
		)
	actions = [approvePost, draftPost,]
	def save_model(self, request, obj, form, change):
		obj.analyst = request.user
		super().save_model(request, obj, form, change)

# 18  stockOwnershipDirector      ////
@admin.register(stockOwnershipDirector)
class stockOwnershipDirectorImport(ImportExportModelAdmin, SummernoteModelAdmin):
	summernote_fields = ('totalPromoterHoldingDescription', 
		'pledgePromoterHoldingDescription', 
		'mutualFundInstitutionalHoldingDescription',
		'foreignInstitutionalHoldingDescription',
		'domesticInstitutionalHoldingDescription',
		'description',
		)
	actions = [approvePost, draftPost,]
	def save_model(self, request, obj, form, change):
		obj.analyst = request.user
		super().save_model(request, obj, form, change)

# 19  stockOwnershipInstitutional
@admin.register(stockOwnershipInstitutional)
class stockOwnershipInstitutionalImport(ImportExportModelAdmin, SummernoteModelAdmin):
	actions = [approvePost, draftPost,]
	def save_model(self, request, obj, form, change):
		obj.analyst = request.user
		super().save_model(request, obj, form, change)

# 20 stockEventsCorpActions        ///
@admin.register(stockEventsCorpActions)
class stockEventsCorpActionsImport(ImportExportModelAdmin, SummernoteModelAdmin):
	summernote_fields = ('corporateActionsDescription',)
	actions = [approvePost, draftPost,]
	def save_model(self, request, obj, form, change):
		obj.analyst = request.user
		super().save_model(request, obj, form, change)

# 21  announcementTypeOptions
@admin.register(announcementTypeOptions)
class announcementTypeOptionsImport(ImportExportModelAdmin, SummernoteModelAdmin):
	actions = [approvePost, draftPost,]
	def save_model(self, request, obj, form, change):
		obj.analyst = request.user
		super().save_model(request, obj, form, change)

# 22 stockEventsAnnouncements        ///
@admin.register(stockEventsAnnouncements)
class stockEventsAnnouncementsImport(ImportExportModelAdmin, SummernoteModelAdmin):
	summernote_fields = ('announcementBrief',)
	actions = [approvePost, draftPost,]
	def save_model(self, request, obj, form, change):
		obj.analyst = request.user
		super().save_model(request, obj, form, change)

# 23 legalOrdersOptions
# @admin.register(legalOrdersOptions)
# class legalOrdersOptionsImport(ImportExportModelAdmin, SummernoteModelAdmin):
# 	actions = [approvePost, draftPost,]
# 	def save_model(self, request, obj, form, change):
# 		obj.analyst = request.user
# 		super().save_model(request, obj, form, change)

# 24 stockEventsLegalOrders
@admin.register(stockEventsLegalOrders)
class stockEventsLegalOrdersImport(ImportExportModelAdmin, SummernoteModelAdmin):
	actions = [approvePost, draftPost,]
	def save_model(self, request, obj, form, change):
		obj.analyst = request.user
		super().save_model(request, obj, form, change)


#
@admin.register(stockProfitAndLoss)
class stockProfitAndLossImport(ImportExportModelAdmin, SummernoteModelAdmin):
	actions = [approvePost, draftPost,]
	def save_model(self, request, obj, form, change):
		obj.analyst = request.user
		super().save_model(request, obj, form, change)

#
@admin.register(stockCashFlow)
class stockCashFlowImport(ImportExportModelAdmin, SummernoteModelAdmin):
	actions = [approvePost, draftPost,]
	def save_model(self, request, obj, form, change):
		obj.analyst = request.user
		super().save_model(request, obj, form, change)
#
@admin.register(stockTransferDepositoryOptions)
class stockTransferDepositoryOptionsImport(ImportExportModelAdmin, SummernoteModelAdmin):
	actions = [approvePost, draftPost,]
	def save_model(self, request, obj, form, change):
		obj.analyst = request.user
		super().save_model(request, obj, form, change)

#
@admin.register(saleTypeOptions)
class saleTypeOptionsImport(ImportExportModelAdmin, SummernoteModelAdmin):
	actions = [approvePost, draftPost,]
	def save_model(self, request, obj, form, change):
		obj.analyst = request.user
		super().save_model(request, obj, form, change)

#
@admin.register(stockBasicDetail)
class stockBasicDetailImport(ImportExportModelAdmin, SummernoteModelAdmin):
	prepopulated_fields = {'slug': ('stockName',)}
	summernote_fields = ('content',)
	actions = [approvePost, draftPost,]
	def save_model(self, request, obj, form, change):
		obj.analyst = request.user
		super().save_model(request, obj, form, change)

	
#
@admin.register(sectorOptions)
class sectorOptionImport(ImportExportModelAdmin, SummernoteModelAdmin):
	actions = [approvePost, draftPost,]
	def save_model(self, request, obj, form, change):
		obj.analyst = request.user
		super().save_model(request, obj, form, change)


#
@admin.register(subSectorOptions)
class subSectorOptionsImport(ImportExportModelAdmin, SummernoteModelAdmin):
	actions = [approvePost, draftPost,]
	def save_model(self, request, obj, form, change):
		obj.analyst = request.user
		super().save_model(request, obj, form, change)


#
@admin.register(categoryOptions)
class categoryOptionsImport(ImportExportModelAdmin, SummernoteModelAdmin):
	actions = [approvePost, draftPost,]
	def save_model(self, request, obj, form, change):
		obj.analyst = request.user
		super().save_model(request, obj, form, change)


#
@admin.register(typeOfCompanyOptions)
class typeOfCompanyOptionsImport(ImportExportModelAdmin, SummernoteModelAdmin):
	actions = [approvePost, draftPost,]
	def save_model(self, request, obj, form, change):
		obj.analyst = request.user
		super().save_model(request, obj, form, change)


#
@admin.register(countryOptions)
class countryOptionsImport(ImportExportModelAdmin, SummernoteModelAdmin):
	actions = [approvePost, draftPost,]
	def save_model(self, request, obj, form, change):
		obj.analyst = request.user
		super().save_model(request, obj, form, change)


#
@admin.register(stockEssentials)
class stockEssentialsImport(ImportExportModelAdmin, SummernoteModelAdmin):
	actions = [approvePost, draftPost,]
	def save_model(self, request, obj, form, change):
		obj.analyst = request.user
		super().save_model(request, obj, form, change)

#
@admin.register(managementOptions)
class managementOptionsImport(ImportExportModelAdmin, SummernoteModelAdmin):
	actions = [approvePost, draftPost,]
	def save_model(self, request, obj, form, change):
		obj.analyst = request.user
		super().save_model(request, obj, form, change)


#
@admin.register(accountingPracticeOptions)
class accountingPracticeOptionsImport(ImportExportModelAdmin, SummernoteModelAdmin):
	actions = [approvePost, draftPost,]
	def save_model(self, request, obj, form, change):
		obj.analyst = request.user
		super().save_model(request, obj, form, change)


#
@admin.register(stockOwnershipPattern)
class stockOwnershipPatternImport(ImportExportModelAdmin, SummernoteModelAdmin):
	actions = [approvePost, draftPost,]
	def save_model(self, request, obj, form, change):
		obj.analyst = request.user
		super().save_model(request, obj, form, change)


#
@admin.register(stockNews)
class stockNewsImport(ImportExportModelAdmin):
	actions = [approvePost, draftPost,]
	def save_model(self, request, obj, form, change):
		obj.analyst = request.user
		super().save_model(request, obj, form, change)


#
@admin.register(websiteMaster)
class websiteMasterImport(ImportExportModelAdmin, SummernoteModelAdmin):
	summernote_fields = ('description',)
	actions = [approvePost, draftPost,]
	def save_model(self, request, obj, form, change):
		obj.analyst = request.user
		super().save_model(request, obj, form, change)

#
@admin.register(stockEventsTypeOptions)
class stockEventsTypeOptionsImport(ImportExportModelAdmin, SummernoteModelAdmin):
	actions = [approvePost, draftPost,]
	def save_model(self, request, obj, form, change):
		obj.analyst = request.user
		super().save_model(request, obj, form, change)

#
@admin.register(dividendTypeOptions)
class dividendTypeOptionsImport(ImportExportModelAdmin, SummernoteModelAdmin):
	actions = [approvePost, draftPost,]
	def save_model(self, request, obj, form, change):
		obj.analyst = request.user
		super().save_model(request, obj, form, change)

#
@admin.register(stockEventsDividend)
class stockEventsDividendImport(ImportExportModelAdmin, SummernoteModelAdmin):
	actions = [approvePost, draftPost,]
	def save_model(self, request, obj, form, change):
		obj.analyst = request.user
		super().save_model(request, obj, form, change)


#
@admin.register(corpActionsOptions)
class corpActionsOptionsImport(ImportExportModelAdmin, SummernoteModelAdmin):
	actions = [approvePost, draftPost,]
	def save_model(self, request, obj, form, change):
		obj.analyst = request.user
		super().save_model(request, obj, form, change)


#
@admin.register(stockSolvency)
class stockSolvencyImport(ImportExportModelAdmin, SummernoteModelAdmin):
	summernote_fields = ('solvencyDescription',
		'DERatioDescription', 
		'currentRatioDescription',
		'quickRatioDescription',
		'interestCoverageRatioDescription',
		'capitalAdequateRatioDescription',
		'availableSolvencyMarginRatioDescription',
		'ratioOfPolicyHoldersLiabilitiesDescription',
		)
	actions = [approvePost, draftPost,]
	def save_model(self, request, obj, form, change):
		obj.analyst = request.user
		super().save_model(request, obj, form, change)

#
@admin.register(stockOperatingEfficiency)
class stockOperatingEfficiencyImport(ImportExportModelAdmin, SummernoteModelAdmin):
	summernote_fields = ('operatingEfficiencyDescription',
		'operatingProfitEBITMarginDescription',
		'PBTMarginDescription',
		'PATMarginDescription',
		'netInterestMarginDescription',
		'grossNPADescription',
		'netNPADescription',
		'GNPADescription',
		)
	actions = [approvePost, draftPost,]
	def save_model(self, request, obj, form, change):
		obj.analyst = request.user
		super().save_model(request, obj, form, change)
#
@admin.register(stockRatios)
class stockRatiosImport(ImportExportModelAdmin, SummernoteModelAdmin):
	summernote_fields = ('profitiabilityDescription',
		'returnOnEquityDescription',
		'ROCEDescription',
		'returnOnAssestsDescription',
		'riskWeightedAssestsRatioDescription',
		'RORWADescription',
		)
	actions = [approvePost, draftPost,]
	def save_model(self, request, obj, form, change):
		obj.analyst = request.user
		super().save_model(request, obj, form, change)
#
@admin.register(stockPeers)
class stockPeersImport(ImportExportModelAdmin, SummernoteModelAdmin):
	summernote_fields =  ('description',
		'revenueDescription',
		'netProfitMarginDescription',
		'assestTurnOverRatioDescription',
		'ROEDescription',
		'ROCEDescription',
		'DebtToEquityDescription',
		)
	actions = [approvePost, draftPost,]
	def save_model(self, request, obj, form, change):
		obj.analyst = request.user
		super().save_model(request, obj, form, change)

@admin.register(financialStatementsFrBalanceSheet)
class financialStatementsFrBalanceSheetImport(ImportExportModelAdmin, SummernoteModelAdmin):
	summernote_fields = ('description ',)
	actions = [approvePost, draftPost,]
	def save_model(self, request, obj, form, change):
		obj.analyst = request.user
		super().save_model(request, obj, form, change)

#
@admin.register(financialStatementsFrProfitAndLoss)
class financialStatementsFrProfitAndLossImport(ImportExportModelAdmin, SummernoteModelAdmin):
	summernote_fileds = ('description ',)
	actions = [approvePost, draftPost,]
	def save_model(self, request, obj, form, change):
		obj.analyst = request.user
		super().save_model(request, obj, form, change)
#
@admin.register(financialStatementsFrCashFlow)
class financialStatementsFrCashFlowImport(ImportExportModelAdmin, SummernoteModelAdmin):
	summernote_fields = ('description ',)
	actions = [approvePost, draftPost,]
	def save_model(self, request, obj, form, change):
		obj.analyst = request.user
		super().save_model(request, obj, form, change)

#
@admin.register(stockGrowth)
class stockGrowthImport(ImportExportModelAdmin, SummernoteModelAdmin):
	summernote_fields = (
		'description ', 
		'revenueGrowthDescription ', 
		'netProfitGrowthPATDescription ',
		'EPSGrowthDescription ', 
		'bookValueGrowthDescription ',
		'EBIDTAGrowthDescription ', 
		'operatingProfitGrowthDescription ',
		'cashFlowFromOperationsDescription ',
		'assestsGrowthDescription ', 
		'cashFlowFromFinancingDescription ', 
		'grossDirectPremiumGrowthDescription ',
		'AUMGrowthDescription ', 
		)
	actions = [approvePost, draftPost,]
	def save_model(self, request, obj, form, change):
		obj.analyst = request.user
		super().save_model(request, obj, form, change)

admin.site.register(leadGenerationDetails)
admin.site.register(peersCompanyLinking)
admin.site.register(industrySpecificGraphs)
admin.site.register(industrySpecificGraphsValues)
admin.site.register(currentRateOfbondYield)
admin.site.register(bookValueData)
admin.site.register(financialFigureUnits)
admin.site.register(stockAppSpecific)
admin.site.register(keyratioUrlsForSitemap)
admin.site.register(peersUrlsForSitemap)
admin.site.register(financialUrlsForSitemap)
admin.site.register(ownershipUrlsForSitemap)
admin.site.register(newsUrlsForSitemap)
admin.site.register(eventsUrlsForSitemap)
admin.site.register(foundingRoundsFigureUnits)
admin.site.register(fundingDetailsVisibility)
admin.site.register(benGrahamOrDCF)
admin.site.register(stockListDM)
admin.site.register(annualReportsDHRP)
admin.site.register(stockBalanceSheetTTM)
admin.site.register(stockProfitAndLossTTM)
admin.site.register(stockCashFlowTTM)


##description field for SEO - starts 
@admin.register(stockFinBalanceSheetSEO)
class stockFinBalanceSheetSEOImport(ImportExportModelAdmin, SummernoteModelAdmin):
	summernote_fields = (
		'balanceSheetDescriptionSEO ',  
		'profitAndLossDescriptionSEO ',  
		'cashFlowDescriptionSEO ',  
		)
	actions = [approvePost, draftPost,]
	def save_model(self, request, obj, form, change):
		obj.analyst = request.user
		super().save_model(request, obj, form, change)


@admin.register(stockNewsSEO)
class stockNewsSEOImport(ImportExportModelAdmin, SummernoteModelAdmin):
	summernote_fields = (
		'newsDescriptionSEO ',  
		)
	actions = [approvePost, draftPost,]
	def save_model(self, request, obj, form, change):
		obj.analyst = request.user
		super().save_model(request, obj, form, change)


@admin.register(stockEventsSEO)
class stockEventsSEOImport(ImportExportModelAdmin, SummernoteModelAdmin):
	summernote_fields = (
		'eventsDescriptionSEO ',    
		)
	actions = [approvePost, draftPost,]
	def save_model(self, request, obj, form, change):
		obj.analyst = request.user
		super().save_model(request, obj, form, change)

#description field for SEO - ends 

@admin.register(peerLinkingYearlyData)
class peerLinkingYearlyDataImport(ImportExportModelAdmin):
	actions = [approvePost, draftPost,]
	def save_model(self, request, obj, form, change):
		obj.analyst = request.user
		super().save_model(request, obj, form, change)


@admin.register(iDescriptionForKeyRatios)
class iDescriptionForKeyRatiosImport(ImportExportModelAdmin):
	actions = [approvePost, draftPost,]
	def save_model(self, request, obj, form, change):
		obj.analyst = request.user
		super().save_model(request, obj, form, change)


admin.site.register(stockBalanceSheetBankNBFC)
admin.site.register(stockProfitAndLossBankNBFC)
admin.site.register(valuationRatio)
admin.site.register(bankNBFCRatioDescription)
admin.site.register(researchReportFAQs)
admin.site.register(totalShareYearlyData)
admin.site.register(companyRatios)
admin.site.register(valuesRBIStandards)
admin.site.register(peersCompanyLinkingForBankNBFC)
admin.site.register(peerLinkingYearlyDataForBankNBFC)
admin.site.register(regulatoryRatios)
admin.site.register(commonFAQ)
admin.site.register(stockBalanceSheetBankNBFCTTM)
admin.site.register(stockProfitAndLossBankNBFCTTM)
admin.site.register(startupCategoryOptions)
admin.site.register(loginReminderPopup)
admin.site.register(stockPeersDescriptionForBankNBFC)

class welcomeLoginPopupAdmin(SummernoteModelAdmin):
    summernote_fields = ('letsBeginContent',)

admin.site.register(welcomeLoginPopup, welcomeLoginPopupAdmin)
# admin.site.register(welcomeLoginPopup)

admin.site.register(deck_images)
admin.site.register(deck)
admin.site.register(annualReportsDHRPImage)
admin.site.register(highLights)
admin.site.register(campaign)
admin.site.register(pitchupperimage)