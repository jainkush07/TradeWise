from django import forms
from .models import *



class seedFundingBannerForm(forms.ModelForm):
	class Meta:
		model = seedFundingBanner
		exclude = ('author', 'publish' ,'created','updated','status', 'button_1_ActionUrl', 'button_2_ActionUrl', 'backgroundImage', 'backgroundImage_alt_tag')
class seedFundRaisingJourneyForm(forms.ModelForm):
	class Meta:
		model = seedFundRaisingJourney
		exclude = ('author', 'publish' ,'created','updated','status')
class seedFundingFAQMainForm(forms.ModelForm):
	class Meta:
		model = seedFundingFAQMain
		exclude = ('author', 'publish', 'created', 'updated', 'status')
class seedFundingPricingPlanForm(forms.ModelForm):
	class Meta:
		model = seedFundingPricingPlan
		exclude = ('author', 'publish', 'created', 'updated', 'status')
class seedFundingAppFeatureForm(forms.ModelForm):
	class Meta:
		model = seedFundingAppFeature
		exclude = ('author', 'publish', 'created', 'updated', 'status')
class seedFundingFAQsForm(forms.ModelForm):
	class Meta:
		model = seedFundingFAQs
		exclude = ('author', 'publish', 'created', 'updated', 'status', 'FAQ')
class seedFundingPackagesForm(forms.ModelForm):
	class Meta:
		model = seedFundingPackages
		exclude = ('author', 'publish', 'created', 'updated', 'status','button_ActionUrl')
class growthFundingBannerForm(forms.ModelForm):
	class Meta:
		model = growthFundingBanner
		exclude = ('author', 'publish' ,'created','updated','status', 'button_2_ActionUrl','button_1_ActionUrl')
class growthFundRaisingJourneyForm(forms.ModelForm):
	class Meta:
		model = growthFundRaisingJourney
		exclude = ('author', 'publish' ,'created','updated','status')
class growthFundingFAQMainForm(forms.ModelForm):
	class Meta:
		model = growthFundingFAQMain
		exclude = ('author', 'publish', 'created', 'updated', 'status')
class growthFundingPricingPlanForm(forms.ModelForm):
	class Meta:
		model = growthFundingPricingPlan
		exclude = ('author', 'publish', 'created', 'updated', 'status')
class growthFundingAppFeatureForm(forms.ModelForm):
	class Meta:
		model = growthFundingAppFeature
		exclude = ('author', 'publish', 'created', 'updated', 'status')
class growthFundingFAQsForm(forms.ModelForm):
	class Meta:
		model = growthFundingFAQs
		exclude = ('author', 'publish', 'created', 'updated', 'status','FAQ')
class growthFundingPackagesForm(forms.ModelForm):
	class Meta:
		model = growthFundingPackages
		exclude = ('author', 'publish', 'created', 'updated', 'status')
class earlyFundingBannerForm(forms.ModelForm):
	class Meta:
		model = earlyFundingBanner
		exclude = ('author', 'publish' ,'created','updated','status', 'button_1_ActionUrl', 'button_2_ActionUrl', 'backgroundImage')
class earlyFundRaisingJourneyForm(forms.ModelForm):
	class Meta:
		model = earlyFundRaisingJourney
		exclude = ('author', 'publish' ,'created','updated','status')


class earlyFundingFAQMainForm(forms.ModelForm):
	class Meta:
		model = earlyFundingFAQMain
		exclude = ('author', 'publish', 'created', 'updated', 'status')
class earlyFundingPricingPlanForm(forms.ModelForm):
	class Meta:
		model = earlyFundingPricingPlan
		exclude = ('author', 'publish', 'created', 'updated', 'status')
class earlyFundingAppFeatureForm(forms.ModelForm):
	class Meta:
		model = earlyFundingAppFeature
		exclude = ('author', 'publish', 'created', 'updated', 'status')
class earlyFundingFAQsForm(forms.ModelForm):
	class Meta:
		model = earlyFundingFAQs
		exclude = ('author', 'publish', 'created', 'updated', 'status','faq')
class earlyFundingPackagesForm(forms.ModelForm):
	class Meta:
		model = earlyFundingPackages
		exclude = ('author', 'publish', 'created', 'updated', 'status')
class growthFundingContactUsSignupForm(forms.ModelForm):
	class Meta:
		model = growthFundingContactUsSignup
		exclude = ('author', 'publish', 'created', 'updated', 'status')


class growthFundingContactUsBannerForm(forms.ModelForm):
	class Meta:
		model = growthFundingContactUsBanner
		exclude = ('author', 'publish', 'created', 'updated', 'status')

class growthFundingContactUsKnowMoreForm(forms.ModelForm):
	class Meta:
		model = growthFundingContactUsKnowMore
		exclude = ('author', 'publish', 'created', 'updated', 'status')

class growthFundingContactUsKnowMoreFAQsForm(forms.ModelForm):
	class Meta:
		model = growthFundingContactUsKnowMoreFAQs
		exclude = ('author', 'publish', 'created', 'updated', 'status')

class seedFundingDMForm(forms.ModelForm):
	class Meta:
		model = seedFundingDM
		exclude = ('author', 'publish', 'created', 'updated', 'status')

class seedFundingContactDMForm(forms.ModelForm):
	class Meta:
		model = seedFundingContactDM
		exclude = ('author', 'publish', 'created', 'updated', 'status')

class growthFundingDMForm(forms.ModelForm):
	class Meta:
		model = growthFundingDM
		exclude = ('author', 'publish', 'created', 'updated', 'status')

class growthFundingContactDMForm(forms.ModelForm):
	class Meta:
		model = growthFundingContactDM
		exclude = ('author', 'publish', 'created', 'updated', 'status')

class earlyFundingDMForm(forms.ModelForm):
	class Meta:
		model = earlyFundingDM
		exclude = ('author', 'publish', 'created', 'updated', 'status')

class earlyFundingContactDMForm(forms.ModelForm):
	class Meta:
		model = earlyFundingContactDM
		exclude = ('author', 'publish', 'created', 'updated', 'status')


class seedFundingContactUsSignupForm(forms.ModelForm):
	class Meta:
		model = seedFundingContactUsSignup
		exclude = ('author', 'publish', 'created', 'updated', 'status')


class seedFundingContactUsBannerForm(forms.ModelForm):
	class Meta:
		model = seedFundingContactUsBanner
		exclude = ('author', 'publish', 'created', 'updated', 'status')

class seedFundingContactUsKnowMoreForm(forms.ModelForm):
	class Meta:
		model = seedFundingContactUsKnowMore
		exclude = ('author', 'publish', 'created', 'updated', 'status')

class seedFundingContactUsKnowMoreFAQsForm(forms.ModelForm):
	class Meta:
		model = seedFundingContactUsKnowMoreFAQs
		exclude = ('author', 'publish', 'created', 'updated', 'status')


class earlyFundingContactUsSignupForm(forms.ModelForm):
	class Meta:
		model = earlyFundingContactUsSignup
		exclude = ('author', 'publish', 'created', 'updated', 'status')

class earlyFundingContactUsBannerForm(forms.ModelForm):
	class Meta:
		model = earlyFundingContactUsBanner
		exclude = ('author', 'publish', 'created', 'updated', 'status')

class earlyFundingContactUsKnowMoreForm(forms.ModelForm):
	class Meta:
		model = earlyFundingContactUsKnowMore
		exclude = ('author', 'publish', 'created', 'updated', 'status')

class earlyFundingContactUsKnowMoreFAQsForm(forms.ModelForm):
	class Meta:
		model = earlyFundingContactUsKnowMoreFAQs
		exclude = ('author', 'publish', 'created', 'updated', 'status')

# private-boutique


class privateBoutiqueFAQNRIForm(forms.ModelForm):
	class Meta:
		model = privateBoutiqueFAQNRI
		exclude = ('author', 'publish', 'created', 'updated', 'status')


class privateBoutiqueFAQLegalityForm(forms.ModelForm):
	class Meta:
		model = privateBoutiqueFAQLegality
		exclude = ('author', 'publish' ,'created','updated','status')


class privateBoutiqueSuccessStoriesForm(forms.ModelForm):
	class Meta:
		model = privateBoutiqueSuccessStories
		exclude = ('author', 'publish', 'created', 'updated', 'status')


class privateBoutiqueCategoryForm(forms.ModelForm):
	class Meta:
		model = privateBoutiqueCategory
		exclude = ('author', 'publish' ,'created','updated','status')

class privateBoutiqueBannerForm(forms.ModelForm):
	class Meta:
		model = privateBoutiqueBanner
		exclude = ('author', 'publish' ,'created','updated','status')

class privateBoutiqueRunningCardsForm(forms.ModelForm):
	class Meta:
		model = privateBoutiqueRunningCards
		exclude = ('author', 'publish' ,'created','updated','status')

class privateBoutiqueInvestingProcessImageForm(forms.ModelForm):
	class Meta:
		model = privateBoutiqueInvestingProcessImage
		exclude = ('author', 'publish' ,'created','updated','status')

class privateBoutiqueInvestingProcessCardsForm(forms.ModelForm):
	class Meta:
		model = privateBoutiqueInvestingProcessCards
		exclude = ('author', 'publish' ,'created','updated','status')

class privateBoutiqueSellingProcessCardsForm(forms.ModelForm):
	class Meta:
		model = privateBoutiqueSellingProcessCards
		exclude = ('author', 'publish' ,'created','updated','status')

class privateBoutiqueSellingProcessImageForm(forms.ModelForm):
	class Meta:
		model = privateBoutiqueSellingProcessImage
		exclude = ('author', 'publish' ,'created','updated','status')

class privateBoutiqueWhyToInvestCardsForm(forms.ModelForm):
	class Meta:
		model = privateBoutiqueWhyToInvestCards
		exclude = ('author', 'publish' ,'created','updated','status')

class privateBoutiqueWhyToInvestContentForm(forms.ModelForm):
	class Meta:
		model = privateBoutiqueWhyToInvestContent
		exclude = ('author', 'publish' ,'created','updated','status')

class privateBoutiqueFAQInvestmentForm(forms.ModelForm):
	class Meta:
		model = privateBoutiqueFAQInvestment
		exclude = ('author', 'publish' ,'created','updated','status')

class privateBoutiqueFAQTaxImplicationsForm(forms.ModelForm):
	class Meta:
		model = privateBoutiqueFAQTaxImplications
		exclude = ('author', 'publish' ,'created','updated','status')

class privateBoutiqueDMForm(forms.ModelForm):
	class Meta:
		model = privateBoutiqueDM
		exclude = ('author', 'publish' ,'created','updated','status')


class privateBoutiqueContactUsForm(forms.ModelForm):
	class Meta:
		model = privateBoutiqueContactUs
		exclude = ('author', 'publish' ,'created','updated','status')

class privateBoutiqueContactUsBannerForm(forms.ModelForm):
	class Meta:
		model = privateBoutiqueContactUsBanner
		exclude = ('author', 'publish' ,'created','updated','status')

class privateBoutiqueContactUsKnowMoreForm(forms.ModelForm):
	class Meta:
		model = privateBoutiqueContactUsKnowMore
		exclude = ('author', 'publish' ,'created','updated','status')

class privateBoutiqueContactUsKnowMoreFAQsForm(forms.ModelForm):
	class Meta:
		model = privateBoutiqueContactUsKnowMoreFAQs
		exclude = ('author', 'publish' ,'created','updated','status')

class privateBoutiqueContactDMForm(forms.ModelForm):
	class Meta:
		model = privateBoutiqueContactDM
		exclude = ('author', 'publish' ,'created','updated','status')
		

#
class sellESOPBannerForm(forms.ModelForm):
	class Meta:
		model = sellESOPBanner
		exclude = ('author', 'publish' ,'created','updated','status', 'button_ActionUrl')

class sellESOPAboutUsForm(forms.ModelForm):
	class Meta:
		model = sellESOPAboutUs
		exclude = ('author', 'publish' ,'created','updated','status')

class sellESOPFineWordsAboutUsForm(forms.ModelForm):
	class Meta:
		model = sellESOPFineWordsAboutUs
		exclude = ('author', 'publish', 'created', 'updated', 'status')

class sellESOPVideoForm(forms.ModelForm):
	class Meta:
		model = sellESOPVideo
		exclude = ('author', 'publish', 'created', 'updated', 'status')

class sellESOPJourneyForm(forms.ModelForm):
	class Meta:
		model = sellESOPJourney
		exclude = ('author', 'publish', 'created', 'updated', 'status')


class sellESOPAppFeaturesForm(forms.ModelForm):
	class Meta:
		model = sellESOPAppFeatures
		exclude = ('author', 'publish', 'created', 'updated', 'status')


class sellESOPFAQMainForm(forms.ModelForm):
	class Meta:
		model = sellESOPFAQMain
		exclude = ('author', 'publish', 'created', 'updated', 'status')



class sellESOPRunningNumbersForm(forms.ModelForm):
	class Meta:
		model = sellESOPRunningNumbers
		exclude = ('author', 'publish', 'created', 'updated', 'status')

class sellESOPCardsForm(forms.ModelForm):
	class Meta:
		model = sellESOPCards
		exclude = ('author', 'publish', 'created', 'updated', 'status')

class sellESOPFAQsForm(forms.ModelForm):
	class Meta:
		model = sellESOPFAQs
		exclude = ('author', 'publish', 'created', 'updated', 'status', 'faq')

class sellESOPDMForm(forms.ModelForm):
	class Meta:
		model = sellESOPDM
		exclude = ('author', 'publish', 'created', 'updated', 'status')

class sellESOPContactDMForm(forms.ModelForm):
	class Meta:
		model = sellESOPContactDM
		exclude = ('author', 'publish', 'created', 'updated', 'status')

class sellESOPContactUsForm(forms.ModelForm):
	class Meta:
		model = sellESOPContactUs
		exclude = ('author', 'publish', 'created', 'updated', 'status')


class sellESOPContactUsBannerForm(forms.ModelForm):
	class Meta:
		model = sellESOPContactUsBanner
		exclude = ('author', 'publish', 'created', 'updated', 'status')

class sellESOPContactUsKnowMoreForm(forms.ModelForm):
	class Meta:
		model = sellESOPContactUsKnowMore
		exclude = ('author', 'publish', 'created', 'updated', 'status')

class sellESOPContactUsKnowMoreFAQsForm(forms.ModelForm):
	class Meta:
		model = sellESOPContactUsKnowMoreFAQs
		exclude = ('author', 'publish', 'created', 'updated', 'status')

#private-boutique



#
class sellYourStartupBannerForm(forms.ModelForm):
	class Meta:
		model = sellYourStartupBanner
		exclude = ('author', 'publish' ,'created','updated','status','button_ActionUrl')

class sellYourStartupExposureForm(forms.ModelForm):
	class Meta:
		model = sellYourStartupExposure
		exclude = ('author', 'publish' ,'created','updated','status', 'buttonOnHover_ActionUrl')

class sellYourStartupUnparalleledExposureForm(forms.ModelForm):
	class Meta:
		model = sellYourStartupUnparalleledExposure
		exclude = ('author', 'publish' ,'created','updated','status')

class sellYourStartupBusinessListForm(forms.ModelForm):
	class Meta:
		model = sellYourStartupBusinessList
		exclude = ('author', 'publish' ,'created','updated','status', 'button_ActionUrl')

class sellYourStartupBusinessWorthForm(forms.ModelForm):
	class Meta:
		model = sellYourStartupBusinessWorth
		exclude = ('author', 'publish' ,'created','updated','status','button_ActionUrl')

class sellYourStartupFAQMainForm(forms.ModelForm):
	class Meta:
		model = sellYourStartupFAQMain
		exclude = ('author', 'publish' ,'created','updated','status')

class sellYourStartupFAQsForm(forms.ModelForm):
	class Meta:
		model = sellYourStartupFAQs
		exclude = ('author', 'publish' ,'created','updated','status','faqMain')

class sellYourStartupDMForm(forms.ModelForm):
	class Meta:
		model = sellYourStartupDM
		exclude = ('author', 'publish' ,'created','updated','status','faqMain')

class sellYourStartupContactDMForm(forms.ModelForm):
	class Meta:
		model = sellYourStartupContactDM
		exclude = ('author', 'publish' ,'created','updated','status','faqMain')

class sellYourStartupContactUsBannerForm(forms.ModelForm):
	class Meta:
		model = sellYourStartupContactUsBanner
		exclude = ('author', 'publish', 'created', 'updated', 'status')

class sellYourStartupContactUsKnowMoreForm(forms.ModelForm):
	class Meta:
		model = sellYourStartupContactUsKnowMore
		exclude = ('author', 'publish', 'created', 'updated', 'status')

class sellYourStartupContactUsKnowMoreFAQsForm(forms.ModelForm):
	class Meta:
		model = sellYourStartupContactUsKnowMoreFAQs
		exclude = ('author', 'publish', 'created', 'updated', 'status')

class sellYourStartupContactUsForm(forms.ModelForm):
	class Meta:
		model = sellYourStartupContactUs
		exclude = ('author', 'publish', 'created', 'updated', 'status')