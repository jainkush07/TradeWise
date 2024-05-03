from rest_framework import  serializers
from stockApp.models import *
from newsBlogApp.models import blogNews
from videoShortsApp.models import blogVideosShorts
from videoBlogApp.models import blogVideos
from articleBlogApp.models import blogArticles


class annualReportsDHRPImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = annualReportsDHRPImage
        fields = '__all__'


class typeOfCompanyOptionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = typeOfCompanyOptions
        fields = '__all__'


class deck_imagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = deck_images
        fields = '__all__'


class deckSerializer(serializers.ModelSerializer):
    class Meta:
        model = deck
        fields = '__all__'


class stockInvestmentChecklistSerializer(serializers.ModelSerializer):
    class Meta:
        model = stockInvestmentChecklist
        fields = '__all__'


class highLightsSerializer(serializers.ModelSerializer):
    class Meta:
        model = highLights
        fields = '__all__'


class peerLinkingYearlyDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = peerLinkingYearlyData
        fields = '__all__'


class peersCompanyLinkingSerializer(serializers.ModelSerializer):
    class Meta:
        model = peersCompanyLinking
        fields = '__all__'


class stockPeersSerializer(serializers.ModelSerializer):
    class Meta:
        model = stockPeers
        fields = '__all__'


class stockFinBalanceSheetSEOSerializer(serializers.ModelSerializer):
    class Meta:
        model = stockFinBalanceSheetSEO
        fields = '__all__'


class stockCashFlowTTMSerializer(serializers.ModelSerializer):
    class Meta:
        model = stockCashFlowTTM
        fields = '__all__'


class stockProfitAndLossTTMSerializer(serializers.ModelSerializer):
    class Meta:
        model = stockProfitAndLossTTM
        fields = '__all__'


class stockBalanceSheetTTMSerializer(serializers.ModelSerializer):
    class Meta:
        model = stockBalanceSheetTTM
        fields = '__all__'


class annualReportsDHRPSerializer(serializers.ModelSerializer):
    class Meta:
        model = annualReportsDHRP
        fields = '__all__'


class financialFigureUnitsSerializer(serializers.ModelSerializer):
    class Meta:
        model = financialFigureUnits
        fields = '__all__'


class stockDeckAndDocsSerializer(serializers.ModelSerializer):
    class Meta:
        model = stockDeckAndDocs
        fields = '__all__'


class stockCashFlowSerializer(serializers.ModelSerializer):
    class Meta:
        model = stockCashFlow
        fields = '__all__'


class stockBalanceSheetSerializer(serializers.ModelSerializer):
    class Meta:
        model = stockBalanceSheet
        fields = '__all__'


class financialStatementsFrCashFlowSerializer(serializers.ModelSerializer):
    class Meta:
        model = financialStatementsFrCashFlow
        fields = '__all__'


class financialStatementsFrBalanceSheetSerializer(serializers.ModelSerializer):
    class Meta:
        model = financialStatementsFrBalanceSheet
        fields = '__all__'


class financialStatementsFrProfitAndLossSerializer(serializers.ModelSerializer):
    class Meta:
        model = financialStatementsFrProfitAndLoss
        fields = '__all__'


class stockEventsLegalOrdersSerializer(serializers.ModelSerializer):
    class Meta:
        model = stockEventsLegalOrders
        fields = '__all__'

class stockEventsSEOSerializer(serializers.ModelSerializer):
    class Meta:
        model = stockEventsSEO
        fields = '__all__'


class stockOwnershipInstitutionalSerializer(serializers.ModelSerializer):
    class Meta:
        model = stockOwnershipInstitutional
        fields = '__all__'


class stockOwnershipPatternSerializer(serializers.ModelSerializer):
    class Meta:
        model = stockOwnershipPattern
        fields = '__all__'


class stockOwnershipDirectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = stockOwnershipDirector
        fields = '__all__'


class stockOwnershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = stockOwnership
        fields = '__all__'


class blogArticlesSerializer(serializers.ModelSerializer):
    class Meta:
        model = blogArticles
        fields = '__all__'


class stockNewsSEOSerializer(serializers.ModelSerializer):
    class Meta:
        model = stockNewsSEO
        fields = '__all__'


class blogVideosSerializer(serializers.ModelSerializer):
    class Meta:
        model = blogVideos
        fields = '__all__'


class blogVideosShortsSerializer(serializers.ModelSerializer):
    class Meta:
        model = blogVideosShorts
        fields = '__all__'


class blogNewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = blogNews
        fields = '__all__'


class stockNewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = stockNews
        fields = '__all__'


class websiteMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = websiteMaster
        fields = '__all__'


class fundingDetailsVisibilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = fundingDetailsVisibility
        fields = '__all__'


class foundingRoundsFigureUnitsSerializer(serializers.ModelSerializer):
    class Meta:
        model = foundingRoundsFigureUnits
        fields = '__all__'

class bookValueDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = bookValueData
        fields = '__all__'

class benGrahamOrDCFSerializer(serializers.ModelSerializer):
    class Meta:
        model = benGrahamOrDCF
        fields = '__all__'

class stockRevenueBreakUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = stockRevenueBreakUp
        fields = '__all__'

class stockFundingRoundsSerializer(serializers.ModelSerializer):
    class Meta:
        model = stockFundingRounds
        fields = '__all__'


class stockFundingSerializer(serializers.ModelSerializer):
    class Meta:
        model = stockFunding
        fields = '__all__'


class stockDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = stockDetails
        fields = '__all__'


class stockEssentialsSerializer(serializers.ModelSerializer):
    class Meta:
        model = stockEssentials
        fields = '__all__'


class stockAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = stockAdmin
        fields = '__all__'


class stockIPOSerializer(serializers.ModelSerializer):
    class Meta:
        model = stockIPO
        fields = '__all__'


class stockInvestmentChecklistSerializer(serializers.ModelSerializer):
    class Meta:
        model = stockInvestmentChecklist
        fields = '__all__'


class commonFAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = commonFAQ
        fields = '__all__'


class totalShareYearlyDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = totalShareYearlyData
        fields = '__all__'


class researchReportFAQsSerializer(serializers.ModelSerializer):
    class Meta:
        model = researchReportFAQs
        fields = '__all__'


class saleTypeOptionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = saleTypeOptions
        fields = '__all__'


class stockTransferDepositoryOptionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = stockTransferDepositoryOptions
        fields = '__all__'


class stockProfitAndLossSerializer(serializers.ModelSerializer):
    class Meta:
        model = stockProfitAndLoss
        fields = '__all__'


class subSectorOptionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = subSectorOptions
        fields = '__all__'

class sectorOptionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = sectorOptions
        fields = '__all__'


class categoryOptionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = categoryOptions
        fields = '__all__'


class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = stockBasicDetail
        fields = '__all__'


class StockAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = stockAdmin
        fields = ['verifiedDetails', 'verifiedByAdmin', 'reportLive', 'researchReport','featuredImage','metaTitle','metaDescription','metaKeywords','tags']


class stockGrowthSerializer(serializers.ModelSerializer):
    class Meta:
        model = stockGrowth
        fields = '__all__'


class stockSolvencySerializer(serializers.ModelSerializer):
    class Meta:
        model = stockSolvency
        fields = '__all__'
        

class stockOperatingEfficiencySerializer(serializers.ModelSerializer):
    class Meta:
        model = stockOperatingEfficiency
        fields = '__all__'
        

class sectorSpecificRatiosSerializer(serializers.ModelSerializer):
    class Meta:
        model = sectorSpecificRatios
        fields = '__all__'


class stockRatiosSerializer(serializers.ModelSerializer):
    class Meta:
        model = stockRatios
        fields = '__all__'


class stockBalanceSheetSerializer(serializers.ModelSerializer):
    class Meta:
        model = stockBalanceSheet
        fields = '__all__'


class stockCashFlowSerializer(serializers.ModelSerializer):
    class Meta:
        model = stockCashFlow
        fields = '__all__'


class valuationRatioSerializer(serializers.ModelSerializer):
    class Meta:
        model = valuationRatio
        fields = '__all__'


class iDescriptionForKeyRatiosSerializer(serializers.ModelSerializer):
    class Meta:
        model = iDescriptionForKeyRatios
        fields = '__all__'


class bankNBFCRatioDescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = bankNBFCRatioDescription
        fields = '__all__'


class valuesRBIStandardsSerializer(serializers.ModelSerializer):
    class Meta:
        model = valuesRBIStandards
        fields = '__all__'


class companyRatiosSerializer(serializers.ModelSerializer):
    class Meta:
        model = companyRatios
        fields = '__all__'


class regulatoryRatiosSerializer(serializers.ModelSerializer):
    class Meta:
        model = regulatoryRatios
        fields = '__all__'


class stockProfitAndLossBankNBFCSerializer(serializers.ModelSerializer):
    class Meta:
        model = stockProfitAndLossBankNBFC
        fields = '__all__'

        
class stockBalanceSheetBankNBFCSerializer(serializers.ModelSerializer):
    class Meta:
        model = stockBalanceSheetBankNBFC
        fields = '__all__'


class stockBalanceSheetBankNBFCTTMSerializer(serializers.ModelSerializer):
    class Meta:
        model = stockBalanceSheetBankNBFCTTM
        fields = '__all__'

class stockProfitAndLossBankNBFCTTMSerializer(serializers.ModelSerializer):
    class Meta:
        model = stockProfitAndLossBankNBFCTTM
        fields = '__all__'

class stockPeersDescriptionForBankNBFCSerializer(serializers.ModelSerializer):
    class Meta:
        model = stockPeersDescriptionForBankNBFC
        fields = '__all__'

class peersCompanyLinkingForBankNBFCSerializer(serializers.ModelSerializer):
    class Meta:
        model = peersCompanyLinkingForBankNBFC
        fields = '__all__'

class peerLinkingYearlyDataForBankNBFCSerializer(serializers.ModelSerializer):
    class Meta:
        model = peerLinkingYearlyDataForBankNBFC
        fields = '__all__'


class campaignSerializer(serializers.ModelSerializer):
    class Meta:
        model = campaign
        fields = '__all__'

class financialCompanyUpdatesSerializer(serializers.ModelSerializer):
    class Meta:
        model = financialCompanyUpdates
        fields = '__all__'


class pitchDocs_imagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = pitchDocs_images
        fields = '__all__'


class pitchDocsSerializer(serializers.ModelSerializer):
    class Meta:
        model = pitchDocs
        fields = '__all__'
