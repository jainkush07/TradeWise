from rest_framework import serializers
from .models import investorPersonalDetails, stockBrokerDetails
from cartApp.models import Transaction
from stockApp.models import stockBasicDetail



class investorPersonalDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = investorPersonalDetails
        fields = '__all__'


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'

class stockBasicDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = stockBasicDetail
        fields = '__all__'

class stockBrokerDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = stockBrokerDetails
        fields = ('id', 'name', 'status')