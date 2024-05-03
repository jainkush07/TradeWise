from rest_framework import serializers

from productPagesApp.models import seedFundingContactUsSignup, growthFundingContactUsSignup, \
    earlyFundingContactUsSignup, sellESOPContactUs, privateBoutiqueContactUs, sellYourStartupContactUs


class seedFundingContactUsSignupSerializer(serializers.ModelSerializer):
    cityName = serializers.CharField(source='city.name', read_only=True)
    user_type = serializers.SerializerMethodField('get_user_type')
    class Meta:
        model = seedFundingContactUsSignup
        fields = ['contactPerson', 'email', 'mobile', 'cityName', 'nameOfOrganization', 'presentRole', 'annualTurnover', 'author', 'status', 'created', 'user_type']
    def get_user_type(self, obj):
        return "SEED_FUNDING"

class growthFundingContactUsSignupSerializer(serializers.ModelSerializer):
    cityName = serializers.CharField(source='city.name', read_only=True)
    user_type = serializers.SerializerMethodField('get_user_type')
    class Meta:
        model = growthFundingContactUsSignup
        fields = ['contactPerson', 'email', 'mobile', 'cityName', 'nameOfOrganization', 'presentRole', 'annualTurnover', 'author', 'status', 'created', 'user_type']
    def get_user_type(self, obj):
        return "GROWTH_FUNDING"

class earlyFundingContactUsSignupSerializer(serializers.ModelSerializer):
    cityName = serializers.CharField(source='city.name', read_only=True)
    user_type = serializers.SerializerMethodField('get_user_type')
    class Meta:
        model = earlyFundingContactUsSignup
        fields = ['contactPerson', 'email', 'mobile', 'cityName', 'nameOfOrganization', 'presentRole', 'annualTurnover', 'author', 'status', 'created', 'user_type']
    def get_user_type(self, obj):
        return "EARLY_FUNDING"

class sellESOPContactUsSerializer(serializers.ModelSerializer):
    user_type = serializers.SerializerMethodField('get_user_type')
    class Meta:
        model = sellESOPContactUs
        fields = ['contactPerson', 'email', 'mobile', 'nameOfOrganization', 'websiteURL', 'numberOfShares', 'author', 'status', 'created', 'user_type']
    def get_user_type(self, obj):
        return "SELL_ESOP"

class privateBoutiqueContactUsSerializer(serializers.ModelSerializer):
    cityName = serializers.CharField(source='city.name', read_only=True)
    stateName = serializers.CharField(source='state.name', read_only=True)
    countryName = serializers.CharField(source='countryCode.name', read_only=True)
    user_type = serializers.SerializerMethodField('get_user_type')
    class Meta:
        model = privateBoutiqueContactUs
        fields = ['contactPerson', 'email', 'mobile', 'countryName', 'cityName', 'author', 'stateName', 'created', 'user_type']
    def get_user_type(self, obj):
        return "PRIVATE_BOUTIQUE"

class sellYourStartupContactUsSerializer(serializers.ModelSerializer):
    cityName = serializers.CharField(source='city.name', read_only=True)
    user_type = serializers.SerializerMethodField('get_user_type')
    class Meta:
        model = sellYourStartupContactUs
        fields = ['contactPerson', 'email', 'mobile', 'cityName', 'nameOfOrganization', 'presentRole', 'annualTurnover', 'author', 'status', 'created', 'user_type']
    def get_user_type(self, obj):
        return "SELL_YOUR_STARTUP"
