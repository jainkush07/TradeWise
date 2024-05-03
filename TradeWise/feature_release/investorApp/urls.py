from django.urls import path
from . import views

app_name = 'investorApp'

urlpatterns = [
    # render view
    path('shareBookStatusDetailsSubmitView/', views.shareBookStatusDetailsSubmitView,
         name="shareBookStatusDetailsSubmitUrl"),
    path('shareBookTransaction', views.shareBookTransactionSubmitView, name="shareBookTransactionSubmitUrl"),
    path('investorPortfolioSubmit/', views.investorPortfolioSubmitView, name="investorPortfolioSubmitUrl"),
    path('childInvestorTempTransaction/', views.childInvestorTempTransactionView,
         name="childInvestorTempTransactionUrl"),
    path('childInvestorTempTransactionViewAPI/', views.childInvestorTempTransactionViewAPI,
         name="childInvestorTempTransactionViewAPI"),
    path('childInvestorPersonalDetailSubmit/', views.childInvestorPersonalDetailSubmitView,
         name="childInvestorPersonalDetailSubmitUrl"),
    path('childInvestorPersonalDetailSubmitViewAPI/', views.childInvestorPersonalDetailSubmitViewAPI,
         name="childInvestorPersonalDetailSubmitViewAPI"),
    path('', views.personalDetailView, name='personalDetailUrl'),
    path('investment/', views.investmentView, name='investmentUrl'),
    path('investor-kyc/', views.investorKycView, name="investorKycUrl"),
    path('investor-portfolio/', views.investorpotfolioView, name="investorpotfolioUrl"),
    path('investor-sharebook/', views.sharebookView, name="sharebookUrl"),

    path('bank/', views.bankView, name='bankUrl'),
    path('DMAT/', views.dmatView, name='DMATUrl'),
    path('deleteFKdata/', views.deleteFKdataView, name="deleteFKdataUrl"),
    path('deleteFKdataAPI/', views.deleteFKdataViewAPI, name="deleteFKdataAPI"),
    path('apply-mods/', views.apply_mods_view, name="apply_mods_url"),
    # Submit path('', views.employeeListView, name="employeeListUrl"),
    path('getDmatStatusCheck/', views.getDmatStatusCheckView, name="getDmatStatusCheckUrl"),
    path('getBankStatusCheck/', views.getBankStatusCheckView, name="getBankStatusCheckUrl"),

    path('personal-info', views.investorPersonalDetailsView, name='investorPersonalDetailsUrl'),
    path('investment-info', views.investmentDetailsView, name='investmentDetailsUrl'),
    path('bank-info', views.investorBankDetailsView, name='investorBankDetailsUrl'),
    path('DMAT-info', views.investorDMATDetailsView, name='investorDMATDetailsUrl'),
    path('invest-info', views.lookingToInvestDetailsView, name='investmentINDetailsUrl'),
    path('getVerify/', views.personalVerificationStatusView, name='personalVerificationStatusUrl'),
    # slug based submit path
    path('slug-based-personal-info-submit', views.slugBasedPersonalDetailSubmitView,
         name='slugBasedPersonalDetailSubmitUrl'),
    path('slug-based-investor-info-submit', views.slugBasedInvestorDetailSubmitView,
         name='slugBasedInvestorDetailSubmitUrl'),
    path('slug-based-investor-bank-info-submit', views.slugBasedinvestorBankDetailSubmitView,
         name='slugBasedinvestorBankDetailSubmitUrl'),
    path('slug-based-dmat-info-submit', views.slugBasedDmatDetailSubmitView, name='slugBasedDmatDetailSubmitUrl'),
    path('slug-based-source-info-submit', views.slugBasedInvestorSourceSubmitView,
         name='slugBasedInvestorSourceSubmitUrl'),

    # connected Investors submit
    path('connected-investors-submit-info', views.connectedInvestorsSubmitView, name='connectedInvestorsSubmitUrl'),
    path('createInvestor/', views.createInvestorView, name="createInvestorUrl"),

    # gaurav code
    path('load-states/', views.load_states, name='load_states_url'),
    path('load-cities/', views.load_cities, name='load_cities_url'),
    path('states/', views.load_statesClick, name='load_statesClick_url'),
    path('cities/', views.load_citiesClick, name='load_citiesClick_url'),

    # slug based render view
    path('<slug>/source/', views.investorsourceView, name="investorsourceUrl"),

    path('<slug>/personal/', views.slugBasedPersonalDetailView, name='slugBasedPersonalDetailUrl'),
    path('<slug>/investment/', views.slugBasedInvestmentView, name='slugBasedInvestmentUrl'),
    path('<slug>/bank/', views.slugBasedBankView, name='slugBasedBankUrl'),
    path('<slug>/DMAT/', views.slugBasedDmatView, name='slugBasedDmatUrl'),
    path('investor-portfolio-api/', views.getinvestorpotfolioView, name="investorportfolioApi"),
    path('investor-portfolio-user-stock/', views.getinvestorpotfolioUserStockView, name="getinvestorpotfolioUserStockView"),
    path('kyc/config/', views.UserKycConfigAPIView.as_view(), name='fetch_kyc_config'),
    path('kyc/step/config/', views.UserKycPageConfigAPIView.as_view(), name='fetch_kyc_step_config'),
    path('kyc/user/', views.UserKycUpdateAPIView.as_view(), name='kyc_user_data'),
    path('kyc/user/<str:step>/<str:pk>/', views.UserKycDeleteAPIView.as_view(), name='kyc_user_step_clean'),
    path('kyc/field/<str:field>/options/', views.UserKycFieldOptionsAPIView.as_view(), name='kyc_field_options'),
    path('kyc/document/', views.UserKycDocumentAPIView.as_view(), name='kyc_docs'),
    path('kyc/', views.UserKycDocumentAPIView.as_view(), name='kyc_docs'),
    path('stockBrokerDetails/', views.getAllStockBrokerDetails),

]
