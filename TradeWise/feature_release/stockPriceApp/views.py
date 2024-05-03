from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.utils import timezone
from .models import *
from stockApp.models import stockBasicDetail
import datetime

DATE_TODAY = datetime.date.today()
ONE_DAY_BACK = DATE_TODAY - datetime.timedelta(days=1)
ONE_WEEK_BACK = DATE_TODAY - datetime.timedelta(days=7)
ONE_MONTH_BACK = DATE_TODAY - datetime.timedelta(days=30)

#
def marketDashboardView(request):
	allPublishedStocks = stockBasicDetail.objects.filter(status='published')
	comparisonDate = request.GET.get('date')
	comparisonType = request.GET.get('type')
	context = {}
	for item in allPublishedStocks:
		try:
			latestStockObj = stockDailyUpdates.objects.filter(stockProfile = item).latest('publish')
		except:
			latestStockObj = None
		# if comparisonType == 'topgainer':
		if comparisonDate == '1day':
			try:
				secondObj = stockDailyUpdates.objects.get(stockProfile = item, publish__date = ONE_DAY_BACK)
			except:
				secondObj = None
		if latestStockObj and secondObj:
			priceToday = latestStockObj.price
			pricePrevious = secondObj.price
			priceDiff = priceToday - pricePrevious
			if priceDiff < 0:
				priceDiffType = 'negetive'
			elif priceDiff == 0:
				priceDiffType = 'nothing'
			else:
				priceDiffType = 'positive'
			priceChangePercentage = (priceDiff / pricePrevious) * 100
			subContext = {
				'price': priceToday,
				'priceDiff': priceDiff,
				'diffPrecentage': priceChangePercentage,
				'differenceType': priceDiffType,
			}
			context[item] = subContext
	return HttpResponse(str(context))
