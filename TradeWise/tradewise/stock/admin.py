
from django.contrib import admin
from . models import *

admin.site.register(User)
admin.site.register(SentimentAnalysis)
admin.site.register(FundamentalAnalysis)
admin.site.register(Stock)
admin.site.register(TechnicalAnalysis)
admin.site.register(Trade)
admin.site.register(Portfolio)
admin.site.register(PortfolioStock)