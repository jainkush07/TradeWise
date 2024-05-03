from rest_framework import serializers
from cartApp.models import CartItems


class ItemUpdateSerializer(serializers.Serializer):
    quantity = serializers.FloatField(min_value=0, max_value=100000000, required=True,
                                      error_messages={'invalid': "Please input valid quantity", 'required': 'please add qunatity'})


class ItemAddSerializer(serializers.Serializer):
    quantity = serializers.FloatField(min_value=0, max_value=100000000,required=False,
                                      error_messages={'invalid': "Please input valid quantity"})
    amount = serializers.FloatField(min_value=0, max_value=10000000000, required=False,
                                    error_messages={'invalid': "Please input valid amount"})
    stock_id = serializers.CharField(required=True,
                                     error_messages={'invalid': "Please select a valid stock",
                                                     'required': 'Please select a¬ valid stock'}
                                     )
