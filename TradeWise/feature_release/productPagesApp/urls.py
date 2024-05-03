from . import views
from django.urls import path

import stockApp

app_name = 'productPagesApp'

urlpatterns = [
    path('deleteFKdata/', views.deleteFKdataView, name="deleteFKdataUrl"),  
    path('seedFundingBanner/', views.seedFundingBannerView, name="seedFundingBannerUrl"),
    path('seedFundRaisingJourney/', views.seedFundRaisingJourneyView, name="seedFundRaisingJourneyUrl"),
    path('seedFundingAppFeature/', views.seedFundingAppFeatureView, name="seedFundingAppFeatureUrl"),
    path('seedFundingFAQMain/', views.seedFundingFAQMainView, name="seedFundingFAQMainUrl"),
    path('seedFundingFAQs/', views.seedFundingFAQsView, name="seedFundingFAQsUrl"),
    path('seedFundingPricingPlan/', views.seedFundingPricingPlanView, name="seedFundingPricingPlanUrl"),
    path('seedFundingPackages/', views.seedFundingPackagesView, name="seedFundingPackagesUrl"),  
    path('seed-funding/', views.seedFundingView, name="seedFundingUrl"),  
    path('growthFundingBanner/', views.growthFundingBannerView, name="growthFundingBannerUrl"),
    path('growthFundRaisingJourney/', views.growthFundRaisingJourneyView, name="growthFundRaisingJourneyUrl"),
    path('growthFundingAppFeature/', views.growthFundingAppFeatureView, name="growthFundingAppFeatureUrl"),
    path('growthFundingFAQMain/', views.growthFundingFAQMainView, name="growthFundingFAQMainUrl"),
    path('growthFundingFAQs/', views.growthFundingFAQsView, name="growthFundingFAQsUrl"),
    path('growthFundingPricingPlan/', views.growthFundingPricingPlanView, name="growthFundingPricingPlanUrl"),
    path('growthFundingPackages/', views.growthFundingPackagesView, name="growthFundingPackagesUrl"),
    path('growth-funding/', views.growthFundingView, name="growthFundingUrl"),
    # path('deleteFKdata/', views.deleteFKdataView, name="deleteFKdataUrl"),
    path('earlyFundingBanner/', views.earlyFundingBannerView, name="earlyFundingBannerUrl"),
    path('earlyFundRaisingJourney/', views.earlyFundRaisingJourneyView, name="earlyFundRaisingJourneyUrl"),
    path('earlyFundingAppFeature/', views.earlyFundingAppFeatureView, name="earlyFundingAppFeatureUrl"),
    path('earlyFundingFAQMain/', views.earlyFundingFAQMainView, name="earlyFundingFAQMainUrl"),
    path('earlyFundingFAQs/', views.earlyFundingFAQsView, name="earlyFundingFAQsUrl"),
    path('earlyFundingPricingPlan/', views.earlyFundingPricingPlanView, name="earlyFundingPricingPlanUrl"),
    path('earlyFundingPackages/', views.earlyFundingPackagesView, name="earlyFundingPackagesUrl"),   
    path('startup-funding/', views.earlyFundingView, name="earlyFundingUrl"),
    path('earlyFundingDM/', views.earlyFundingDMView, name="earlyFundingDMUrl"),
    path('earlyFundingContactDM/', views.earlyFundingContactDMView, name="earlyFundingContactDMUrl"),   
    path('seedFundingDM/', views.seedFundingDMView, name="seedFundingDMUrl"),
    path('seedFundingContactDM/', views.seedFundingContactDMView, name="seedFundingContactDMUrl"),    
    path('growthFundingDM/', views.growthFundingDMView, name="growthFundingDMUrl"),
    path('growthFundingContactDM/', views.growthFundingContactDMView, name="growthFundingContactDMUrl"),
    path('seedFundingContactUsBanner/', views.seedFundingContactUsBannerView, name="seedFundingContactUsBannerUrl"),
    path('seedFundingContactUsKnowMore/', views.seedFundingContactUsKnowMoreView, name="seedFundingContactUsKnowMoreUrl"),
    path('seedFundingContactUsKnowMoreFAQs/', views.seedFundingContactUsKnowMoreFAQsView, name="seedFundingContactUsKnowMoreFAQsUrl"),
    path('earlyFundingContactUsBanner/', views.earlyFundingContactUsBannerView, name="earlyFundingContactUsBannerUrl"),
    path('earlyFundingContactUsKnowMore/', views.earlyFundingContactUsKnowMoreView, name="earlyFundingContactUsKnowMoreUrl"),
    path('earlyFundingContactUsKnowMoreFAQs/', views.earlyFundingContactUsKnowMoreFAQsView, name="earlyFundingContactUsKnowMoreFAQsUrl"),
    path('growthFundingContactUsBanner/', views.growthFundingContactUsBannerView, name="growthFundingContactUsBannerUrl"),
    path('growthFundingContactUsKnowMore/', views.growthFundingContactUsKnowMoreView, name="growthFundingContactUsKnowMoreUrl"),
    path('growthFundingContactUsKnowMoreFAQs/', views.growthFundingContactUsKnowMoreFAQsView, name="growthFundingContactUsKnowMoreFAQsUrl"),
    path('seedFundingContactUsForm/', views.seedFundingContactView, name="seedFundingContactViewUrl"),
    path('seedFundingContact/', views.seedFundingContactSignupView, name="seedFundingContactUrl"),
    path('earlyFundingContactUsForm/', views.earlyFundingContactView, name="earlyFundingContactViewUrl"),
    path('startupFundingContact/', views.earlyFundingContactSignupView, name="earlyFundingContactUrl"),
    path('growthFundingContactUsForm/', views.growthFundingContactView, name="growthFundingContactViewUrl"),
    path('growthFundingContact/', views.growthFundingContactSignupView, name="growthFundingContactUrl"),

    # path('deleteFKdata/', views.deleteFKdataView, name="deleteFKdataUrl"), 
    path('sellESOPBanner/', views.sellESOPBannerView, name = "sellESOPBannerUrl"),
    path('sellESOPAboutUs/', views.sellESOPAboutUsView, name = "sellESOPAboutUsUrl"),
    path('sellESOPFineWordsAboutUs/', views.sellESOPFineWordsAboutUsView, name = "sellESOPFineWordsAboutUsUrl"),
    path('sellESOPVideo/', views.sellESOPVideoView, name = "sellESOPVideoUrl"),
    path('sellESOPJourney/', views.sellESOPJourneyView, name = "sellESOPJourneyUrl"),
    path('sellESOPAppFeatures/', views.sellESOPAppFeaturesView, name = "sellESOPAppFeaturesUrl"),
    path('sellESOPCards/', views.sellESOPCardsView, name = "sellESOPCardsUrl"),
    path('sellESOPRunningNumbers/', views.sellESOPRunningNumbersView, name = "sellESOPRunningNumbersUrl"),
    path('sellESOPFAQMain/', views.sellESOPFAQMainView, name = "sellESOPFAQMainUrl"),
    path('sellESOPFAQs/', views.sellESOPFAQsView, name = "sellESOPFAQsUrl"),
    path('sell-esop/', views.sellESOPView, name="sellESOPUrl"),
    path('sellESOPDM/', views.sellESOPDMView, name="sellESOPDMUrl"),
    path('sellESOPContactDM/', views.sellESOPContactDMView, name="sellESOPContactDMUrl"),
    path('sellESOPContactUsBanner/', views.sellESOPContactUsBannerView, name="sellESOPContactUsBannerUrl"),
    path('sellESOPContactUsKnowMore/', views.sellESOPContactUsKnowMoreView, name="sellESOPContactUsKnowMoreUrl"),
    path('sellESOPContactUsKnowMoreFAQs/', views.sellESOPContactUsKnowMoreFAQsView, name="sellESOPContactUsKnowMoreFAQsUrl"),
    path('sellESOPContact', views.sellESOPContactView, name="sellESOPContactViewUrl"),
    path('sellESOPContactForm', views.sellESOPContactSignupView, name="sellESOPContactUrl"),

    #private-boutique
    path('privateBoutiqueFAQLegality/', views.privateBoutiqueFAQLegalityView, name='privateBoutiqueFAQLegalityUrl'),
    path('privateBoutiqueFAQNRI/',views.privateBoutiqueFAQNRIView, name="privateBoutiqueFAQNRIUrl"),
    path('privateBoutiqueSuccessStories/', views.privateBoutiqueSuccessStoriesView, name='privateBoutiqueSuccessStoriesUrl'),
    path('privateBoutiqueCategory/',views.privateBoutiqueCategoryView, name="privateBoutiqueCategoryUrl"),
    path('privateBoutiqueBanner/',views.privateBoutiqueBannerView, name="privateBoutiqueBannerUrl"),
    path('privateBoutiqueRunningCards/',views.privateBoutiqueRunningCardsView, name="privateBoutiqueRunningCardsUrl"),
    path('privateBoutiqueInvestingProcessImage/',views.privateBoutiqueInvestingProcessImageView, name="privateBoutiqueInvestingProcessImageUrl"),
    path('privateBoutiqueInvestingProcessCards/',views.privateBoutiqueInvestingProcessCardsView, name="privateBoutiqueInvestingProcessCardsUrl"),
    path('privateBoutiqueSellingProcessCards/',views.privateBoutiqueSellingProcessCardsView, name="privateBoutiqueSellingProcessCardsUrl"),
    path('privateBoutiqueSellingProcessImage/',views.privateBoutiqueSellingProcessImageView, name="privateBoutiqueSellingProcessImageUrl"),
    path('privateBoutiqueWhyToInvestCards/',views.privateBoutiqueWhyToInvestCardsView, name="privateBoutiqueWhyToInvestCardsUrl"),
    path('privateBoutiqueWhyToInvestContent/',views.privateBoutiqueWhyToInvestContentView, name="privateBoutiqueWhyToInvestContentUrl"),
    path('privateBoutiqueFAQInvestment/',views.privateBoutiqueFAQInvestmentView, name="privateBoutiqueFAQInvestmentUrl"),
    path('privateBoutiqueFAQTaxImplications/', views.privateBoutiqueFAQTaxImplicationsView, name="privateBoutiqueFAQTaxImplicationsUrl"),
    path('privateBoutiqueContactUs/', views.privateBoutiqueContactUsView, name="privateBoutiqueContactUsUrl"),
    path('privateBoutiqueContactUsBanner/', views.privateBoutiqueContactUsBannerView, name="privateBoutiqueContactUsBannerUrl"),
    path('privateBoutiqueContactUsKnowMore/', views.privateBoutiqueContactUsKnowMoreView, name="privateBoutiqueContactUsKnowMoreUrl"),
    path('privateBoutiqueContactUsKnowMoreFAQs/', views.privateBoutiqueContactUsKnowMoreFAQsView, name="privateBoutiqueContactUsKnowMoreFAQsUrl"),
    path('privateBoutiqueContactDM/', views.privateBoutiqueContactDMView, name="privateBoutiqueContactDMUrl"),
    path('privateBoutiqueDM/',views.privateBoutiqueDMView, name="privateBoutiqueDMUrl"),
    path('privateBoutiqueContactUsSignup/', views.privateBoutiqueContactUsSignupView, name="privateBoutiqueContactUsSignupUrl"),
    path('privateBoutique/', views.privateBoutiqueView, name="privateBoutiqueUrl"),
    
    # 
    path('sellYourStartupBanner',views.sellYourStartupBannerView , name="sellYourStartupBannerUrl"),
    path('sellYourStartupExposure',views.sellYourStartupExposureView , name="sellYourStartupExposureUrl"),
    path('sellYourUnparalleledExposure',views.sellYourStartupUnparalleledExposureView , name="sellYourStartupUnparalleledExposureUrl"),   
    path('sellYourBusinessList',views.sellYourStartupBusinessListView , name="sellYourStartupBusinessListUrl"),
    path('sellYourStartupBusinessWorth',views.sellYourStartupBusinessWorthView , name="sellYourStartupBusinessWorthUrl"),
    path('sellYourStartupFAQMain',views.sellYourStartupFAQMainView , name="sellYourStartupFAQMainUrl"),
    path('sellYourStartupFAQs',views.sellYourStartupFAQsView , name="sellYourStartupFAQsUrl"),
    path('sellYourStartupDM/', views.sellYourStartupDMView, name="sellYourStartupDMUrl"),
    #render View
    path('sell-startup-business/',views.sellYourStartupView , name="sellYourStartupUrl"),
    path('sellYourStartupContactUsBanner/', views.sellYourStartupContactUsBannerView, name="sellYourStartupContactUsBannerUrl"),
    path('sellYourStartupContactUsKnowMore/', views.sellYourStartupContactUsKnowMoreView, name="sellYourStartupContactUsKnowMoreUrl"),
    path('sellYourStartupContactUsKnowMoreFAQs/', views.sellYourStartupContactUsKnowMoreFAQsView, name="sellYourStartupContactUsKnowMoreFAQsUrl"),
    path('sellYourStartupContact/', views.sellYourStartupContactUsView, name="sellYourStartupContactViewUrl"),
    path('sellYourStartupContactDM/', views.sellYourStartupContactDMView, name="sellYourStartupContactDMUrl"),
    path('sellYourStartupContactForm/', views.sellYourStartupContactSignupView, name="sellYourStartupContactUrl"),
    path('getAllEntityData/', stockApp.views.getFormEntityObject, name='getSeedfundingObject'),

]