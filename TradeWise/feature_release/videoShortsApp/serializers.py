from rest_framework import serializers
from .models import *


class blogShortsListingDMSerializer(serializers.ModelSerializer):
    class Meta:
        model = blogShortsListingDM
        exclude = ('publish', 'created', 'updated', 'status',)

class shortsListSerializer(serializers.ModelSerializer):
    class Meta:
        model = blogVideosShorts
        fields = '__all__'


class shortsHeadingDMSerializer(serializers.ModelSerializer):
	class Meta:
		model = shortsHeadingDM
		exclude = ('videoShorts', 'publish', 'created', 'updated', 'status')

#=====================================================================      

class PaginationblogVideosShortsSerializer(serializers.ModelSerializer):
    class Meta:
        model = blogVideosShorts
        fields = '__all__'





