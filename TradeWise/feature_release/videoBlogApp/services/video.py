from videoBlogApp.models import categoryOptions, subCategoryOptions
from stockApp.models import categoryOptions as stockCategoryOptions


class VideoService:

    @staticmethod
    def get_video_filters():
        priority_order = {'startups': 0, 'pre ipo': 1, 'upcoming ipo': 2, 'seed funding': 3, 'unicorns': 4, 'ideas': 5,
                          'market news & economy': 6, 'interviews - young entrepreneurs': 7, 'stock recommendations': 8,
                          'beginner guide - funding': 9, 'beginner guide - preipo': 10,
                          'employee stock options - esop': 11, 'large cap': 12, 'mid cap': 13, 'small cap': 14,
                          'micro cap': 15, 'delisted stock': 16,
                          'listed on small exchange - suspended/liquidation phase - lse': 17, 'listed stocks': 18,
                          'diversified stocks': 19, 'channel partner videos': 20, 'financial planning': 21,
                          'investment strategy': 22}
        categories = categoryOptions.objects.all().values('name', 'slug', 'id')
        category_id_list = [i['id'] for i in categories]
        # sub_categories = subCategoryOptions.objects.filter(category_id__in=category_id_list).values(
        #     'name', 'slug', 'category', 'id')
        data_list = []
        for category in categories:
            category["filter_type"] = "category"
            category['filter'] = {'category': category['id']}
            del category['id']
            data_list.append(category)
        # for category in sub_categories:
        #     category["filter_type"] = "sub_category"
        #     category['filter'] = {'subCategory': category['id']}
        #     del category['id']
        #     data_list.append(category)
        categoryList = [
            'Micro Cap',
            'Small Cap',
            'Mid Cap',
            'Large Cap',
            'Unicorns',
            'Growth Stocks',
            'Stock Market',
            'Freezed Stocks',
            'Listed Stocks',
            'Financial Planning',
            'IPO',
            'Upcoming IPO',
            'Pre IPO',
            'Delisted Stocks',
            'Diversified Stocks',
            'Liquidation/Suspended Phase',
            'Listed on Small Exchange']
        stocks_category = stockCategoryOptions.objects.filter(name__in=categoryList).values('name', 'id')
        for category in stocks_category:
            category["filter_type"] = "stocks_category"
            category['filter'] = {'stockCategory': category['id']}
            del category['id']
            data_list.append(category)
        data_list = sorted(data_list, key=lambda x: priority_order.get(x['name'].lower().strip(), 100))
        return data_list
