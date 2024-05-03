from rest_framework import serializers
from articleBlogApp.models import blogArticles


class BlogArticleListSerializer(serializers.ModelSerializer):
    class Meta:
        model = blogArticles
        fields = ['author', 'title', 'slug', 'subTitle', 'articleImage', 'publish', 'id', 'dateForListing', 'excerptContent', 'article_views']


class BlogArticleSerializer(serializers.ModelSerializer):
    subCategory = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()
    tags = serializers.SerializerMethodField()

    def get_subCategory(self, obj):
        subCategory = []
        for item in obj.subCategory.all():
            subCategory.append(item.name)
        return subCategory

    def get_category(self, obj):
        getCategory = []
        for item in obj.category.all():
            getCategory.append(item.name)
        return getCategory

    def get_tags(self, obj):
        tagsList = []
        for item in obj.tags.all():
            tagsList.append(item.name)
        return tagsList

    class Meta:
        model = blogArticles
        fields = ['author', 'title', 'slug', 'subTitle', 'articleImage', 'publish', 'id', 'content1', 'content2',
                  'content3', 'content4', 'content5', 'article_views', 'articleVideo', 'dateForListing', 'excerptContent', 'category', 'subCategory', 'tags']
                 
class newBlogArticleSerializer(serializers.ModelSerializer):
    weburl = serializers.URLField(source='get_absolute_url_newForAPI', read_only=True)

    subCategory = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()
    tags = serializers.SerializerMethodField()

    def get_subCategory(self, obj):
        subCategory = []
        for item in obj.subCategory.all():
            subCategory.append(item.name)
        return subCategory

    def get_category(self, obj):
        getCategory = []
        for item in obj.category.all():
            getCategory.append(item.name)
        return getCategory

    def get_tags(self, obj):
        tagsList = []
        for item in obj.tags.all():
            tagsList.append(item.name)
        return tagsList
        
    class Meta:
        model = blogArticles
        # exclude = ('author', 'created', 'updated', 'status','content1', 'content2', 'content3', 'content4', 'content5')
        fields = '__all__'       
