from videoBlogApp.models import blogVideos
from articleBlogApp.models import blogArticles
from stockApp.models import stockBasicDetail
from newsBlogApp.models import blogNews


class DataOrchestrator:

    @staticmethod
    def fetch_slug_info(slug_type, slug):
        data = {}
        if slug_type in ['video']:
            data = blogVideos.objects.filter(slug=slug).values('id').last()
        elif slug_type in ['research-report']:
            data = stockBasicDetail.objects.filter(slug=slug).values('id').last()
        elif slug_type in ['article-detail', 'article-blog']:
            data = blogArticles.objects.filter(slug=slug).values('id').last()
        elif slug_type in ['planify-feed']:
            data = blogNews.objects.filter(slug=slug).values('id').last()
        return data
