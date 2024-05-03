from django.shortcuts import HttpResponse
from bs4 import BeautifulSoup
import requests
from decimal import Decimal
from datetime import datetime
from dateutil.relativedelta import relativedelta
from .models import peerLinkingYearlyData, financialFigureUnits, peerLinkingYearlyDataForBankNBFC
from screenerStoreApp.models import stockPriceScreener, PeersCrawledValuesScreener
from stockApp.serializers import *

date = datetime.datetime.now()
financialYear = date + relativedelta(months=+3)

#
def return_val_or_0(value):
	try:
		value = Decimal(value)	
		return value
	except:
		value = 0
		return value

#
def return_val_or_1(value):
	if value:
		return value
	else:
		value = 1
		return value

#
def numberConversion(value, currentSystem, convertTo):
	convertedVal = value
	if currentSystem == 'Cr':
		if convertTo == 'K':
			convertedVal = value * 10000
		elif convertTo == 'L':
			convertedVal = value * 100
		elif convertTo == 'M':
			convertedVal = value * 10
	elif currentSystem == 'L':
		if convertTo == 'K':
			convertedVal = value * 100
		elif convertTo == 'M':
			convertedVal = value / 10
		elif convertTo == 'Cr':
			convertedVal = value / 100
	elif currentSystem == 'M':
		if convertTo == 'K':
			convertedVal = value * 1000
		elif convertTo == 'L':
			convertedVal = value * 10
		elif convertTo == 'Cr':
			convertedVal = value / 10
	elif currentSystem == 'K':
		if convertTo == 'L':
			convertedVal = value / 100
		elif convertTo == 'M':
			convertedVal = value / 1000
		elif convertTo == 'Cr':
			convertedVal = value / 10000
	return convertedVal

#
def getScreenerPriceForStock(company):
	urlToCrawl= company.screenerLink
	stockInst = company.stockProfileName
	currentPrice = None
	try:
		source = requests.get(str(urlToCrawl)).text
		soup = BeautifulSoup(source, 'lxml')
		for item in soup.find(id="top-ratios").find_all('li'):
			fetchedValDiv = item.find('span', class_='name').renderContents().strip().decode("utf-8")
			fetchedValVal = (item.find('span', class_='number').renderContents().strip().decode("utf-8").replace(',', ''))
			try:
				fetchedValVal = Decimal(fetchedValVal)
			except:
				fetchedValVal = Decimal(0)
			if fetchedValDiv == 'Current Price':
				currentPrice = fetchedValVal
		saver = stockPriceScreener(stock= stockInst,price=currentPrice, crawledUrl=urlToCrawl)
		saver.save()
	except:
		pass
	return currentPrice

#
def getScreenerPriceForStockByUrl(urlToCrawl):
	currentPrice = None
	try:
		source = requests.get(str(urlToCrawl)).text
		soup = BeautifulSoup(source, 'lxml')
		for item in soup.find(id="top-ratios").find_all('li'):
			fetchedValDiv = item.find('span', class_='name').renderContents().strip().decode("utf-8")
			fetchedValVal = (item.find('span', class_='number').renderContents().strip().decode("utf-8").replace(',', ''))
			try:
				fetchedValVal = Decimal(fetchedValVal)
			except:
				fetchedValVal = Decimal(0)
			if fetchedValDiv == 'Current Price':
				currentPrice = fetchedValVal
	except:
		pass
	return currentPrice

#
def crawlScreenerView(company, fetchForYear):
	urlToCrawl= company.screenerLink
	stockID= company.id
	stockType= company.stockStatus
	try:		
		source = requests.get(str(urlToCrawl)).text
		soup = BeautifulSoup(source, 'lxml')
		# financial Figure units are in
		try:
			stockFinancialSystemInst = financialFigureUnits.objects.get(stockProfileName=company.stockProfileName)
			stockFinancialSystem = stockFinancialSystemInst.financialNumbers
		except:
			stockFinancialSystem = None
		# to extract fields
		sales = interest = otherIncome = netProfit = eps = operatingProfit = depreciation = None
		# extraction Profit & Loss
		# noOfcolToExtract = 1
		forCount = 0
		yearFound = noOfcolToExtract = False
		yearNotAvailable = []
		for item in soup.find(id="profit-loss").find('table', class_='data-table responsive-text-nowrap').find('thead').find_all('th'):
			thVal = item.renderContents().strip().decode("utf-8")
			if yearFound:
				if not 'TTM' in thVal:
					yearNotAvailable.append(thVal)
			if str(fetchForYear) in thVal:
				noOfcolToExtract = forCount
				yearFound = True
			forCount += 1
		if not noOfcolToExtract:
			noOfcolToExtract = forCount - 1
		forCount = 0
		for item in soup.find(id="profit-loss").find('table', class_='data-table responsive-text-nowrap').find('tbody').find_all('tr'):
			extdPLItem = item.findAll('td')
			if forCount == 0:
				sales = extdPLItem[noOfcolToExtract].renderContents().strip().decode("utf-8").replace(',', '')
				try:
					sales = Decimal(sales)
				except:
					sales = Decimal(0)
			if forCount == 2:
				operatingProfit = (extdPLItem[noOfcolToExtract].renderContents().strip().decode("utf-8").replace(',', ''))
				try:
					operatingProfit = Decimal(operatingProfit)
				except:
					operatingProfit = Decimal(0)
			elif forCount == 4:
				otherIncome = (extdPLItem[noOfcolToExtract].renderContents().strip().decode("utf-8").replace(',', ''))
				try:
					otherIncome = Decimal(otherIncome)
				except:
					otherIncome = Decimal(0)
			elif forCount == 5:
				interest = (extdPLItem[noOfcolToExtract].renderContents().strip().decode("utf-8").replace(',', ''))
				try:
					interest = Decimal(interest)
				except:
					interest = Decimal(0)
			elif forCount == 6:
				depreciation = (extdPLItem[noOfcolToExtract].renderContents().strip().decode("utf-8").replace(',', ''))
				try:
					depreciation = Decimal(depreciation)
				except:
					depreciation = Decimal(0)
			elif forCount == 9:
				netProfit = (extdPLItem[noOfcolToExtract].renderContents().strip().decode("utf-8").replace(',', ''))
				try:
					netProfit = Decimal(netProfit)
				except:
					netProfit = Decimal(0)
			elif forCount == 10:
				eps = (extdPLItem[noOfcolToExtract].renderContents().strip().decode("utf-8").replace(',', ''))
				try:
					eps = Decimal(eps)
				except:
					eps = Decimal(0)
			forCount += 1
		# extraction balance sheet
		forCount = 0
		averageTotalAsset = borrowingsCY = borrowings = shareCapitalAvg = reservesAvg = totalEquityCY = totalEquityPY = None
		shareCapitalCY = reservesCY = shareCapitalPY = reservesPY = None
		for item in soup.find(id="balance-sheet").find('table', class_='data-table responsive-text-nowrap').find('tbody').find_all('tr'):
			extdBSItem = item.findAll('td')
			if forCount == 0:
				shareCapitalCY = (extdBSItem[noOfcolToExtract].renderContents().strip().decode("utf-8").replace(',', ''))
				try:
					shareCapitalCY = Decimal(shareCapitalCY)
				except:
					shareCapitalCY = Decimal(0)
				shareCapitalPY = (extdBSItem[noOfcolToExtract-1].renderContents().strip().decode("utf-8").replace(',', ''))
				try:
					shareCapitalPY = Decimal(shareCapitalPY)
				except:
					shareCapitalPY = Decimal(0)
				shareCapitalAvg = (shareCapitalCY + shareCapitalPY) / 2
			elif forCount == 1:
				reservesCY = (extdBSItem[noOfcolToExtract].renderContents().strip().decode("utf-8").replace(',', ''))
				try:
					reservesCY = Decimal(reservesCY)
				except:
					reservesCY = Decimal(0)
				reservesPY = (extdBSItem[noOfcolToExtract-1].renderContents().strip().decode("utf-8").replace(',', ''))
				try:
					reservesPY = Decimal(reservesPY)
				except:
					reservesPY = Decimal(0)
				reservesAvg = (reservesCY + reservesPY) / 2
			elif forCount == 2:
				borrowingsCY = (extdBSItem[noOfcolToExtract].renderContents().strip().decode("utf-8").replace(',', ''))
				try:
					borrowingsCY = Decimal(borrowingsCY)
				except:
					borrowingsCY = Decimal(0)
				borrowingsPY = (extdBSItem[noOfcolToExtract-1].renderContents().strip().decode("utf-8").replace(',', ''))
				try:
					borrowingsPY = Decimal(borrowingsPY)
				except:
					borrowingsPY = Decimal(0)
				borrowings = (borrowingsCY + borrowingsPY) / 2
			elif forCount == 9:
				totalAssetCY = (extdBSItem[noOfcolToExtract].renderContents().strip().decode("utf-8").replace(',', ''))
				try:
					totalAssetCY = Decimal(totalAssetCY)
				except:
					totalAssetCY = Decimal(0)
				totalAssetPY = (extdBSItem[noOfcolToExtract-1].renderContents().strip().decode("utf-8").replace(',', ''))
				try:
					totalAssetPY = Decimal(totalAssetPY)
				except:
					totalAssetPY = Decimal(0)
				averageTotalAsset = (totalAssetCY + totalAssetPY) / 2
			if shareCapitalCY and reservesCY:
				totalEquityCY = shareCapitalCY + reservesCY
			if shareCapitalPY and reservesPY:
				totalEquityPY = shareCapitalPY + reservesPY
			forCount += 1
		# top ratios section
		forCount = 0
		roce = roe = bookValue = currentPrice = marketCap = None
		for item in soup.find(id="top-ratios").find_all('li'):
			fetchedValDiv = item.find('span', class_='name').renderContents().strip().decode("utf-8")
			fetchedValVal = (item.find('span', class_='number').renderContents().strip().decode("utf-8").replace(',', ''))
			try:
				fetchedValVal = Decimal(fetchedValVal)
			except:
				fetchedValVal = Decimal(0)
			if fetchedValDiv == 'ROCE':
				roce = fetchedValVal
			elif fetchedValDiv == 'ROE':
				roe = fetchedValVal
			elif fetchedValDiv == 'Book Value':
				bookValue = fetchedValVal
			elif fetchedValDiv == 'Current Price':
				currentPrice = fetchedValVal
			elif fetchedValDiv == 'Market Cap':
				marketCap = fetchedValVal
			forCount += 1
		# ratios section
		forCount = 0		
		for item in soup.find(id="ratios").find('table', class_='data-table responsive-text-nowrap').find('tbody').find_all('tr'):
			extdBSItem = item.findAll('td')
			if forCount == 5:
				roceRatio = (extdBSItem[noOfcolToExtract].renderContents().strip().decode("utf-8").replace(',', '').replace('%', ''))
				try:
					roce = Decimal(roceRatio)
				except:
					roce = Decimal(0)
			forCount += 1
		# divident section
		if sales == 0:
			saleDivident = 1
		else:
			saleDivident = sales
		if averageTotalAsset == 0:
			averageTotalAssetDivident = 1
		else:
			averageTotalAssetDivident = averageTotalAsset
		debtToEquityDivi = shareCapitalAvg + reservesAvg
		if debtToEquityDivi == 0:
			debtToEquityDivident = 1
		else:
			debtToEquityDivident = debtToEquityDivi
		if eps == 0:
			epsDivident = 1
		else:
			epsDivident = eps
		if bookValue == 0:
			bookValueDivident = 1
		else:
			bookValueDivident = bookValue
		# company querylist
		yearlyData = peerLinkingYearlyData.objects.filter(screenerCompany=company)
		yearlyData_list =[]
		if yearlyData:
			for each in yearlyData:
				yearlyData_serial = peerLinkingYearlyDataSerializer(each)
				yearlyData_list.append(yearlyData_serial.data)

		try:
			stockYearData = yearlyData.get(year=fetchForYear)
		except:
			stockYearData = None
		cashAndShortTerm = preferenceEquity = minorityInterest = longTermSecurities = None
		marketCapVal = bookValueVal = currentPriceVal = 0
		if stockYearData:
			cashAndShortTerm = stockYearData.cashAndShortTermEquivalents
			preferenceEquity = stockYearData.PreferenceEquity
			minorityInterest = stockYearData.totalMinorityInterest
			longTermSecurities = stockYearData.longTermMarketableSecurities
		# # formulas
		revenue = marketCapBySales = npm = totalAssetTurnoverRatio = debtToEquity = peGraph = pbGraph = enterpriseVal = evByEbitda = None
		# if sales and otherIncome:
		revenue = round(return_val_or_0(sales) + return_val_or_0(otherIncome),2)
		# if sales and netProfit:
		npm = round(((return_val_or_0(netProfit) / return_val_or_0(saleDivident))*100),2)
		# if sales and averageTotalAsset:
		totalAssetTurnoverRatio = round(return_val_or_0(sales) / return_val_or_0(averageTotalAssetDivident),2)
		# if borrowings and shareCapitalAvg and reservesAvg:
		debtToEquity = round(return_val_or_0(borrowings) / return_val_or_0(debtToEquityDivident),2)
		# if currentPrice and eps:
		peGraph = round(return_val_or_0(currentPrice) / return_val_or_0(epsDivident),2)
		# if currentPrice and bookValue:
		pbGraph = round(return_val_or_0(currentPrice) / return_val_or_0(bookValueDivident),2)


		# if marketCap and cashAndShortTerm and borrowingsCY and preferenceEquity and minorityInterest and longTermSecurities:
		enterpriseVal = round(return_val_or_0(marketCap) - return_val_or_0(cashAndShortTerm) + return_val_or_0(borrowingsCY) + return_val_or_0(preferenceEquity) + return_val_or_0(minorityInterest) - return_val_or_0(longTermSecurities),2)
		# if marketCap and sales:
		marketCapBySales = round(return_val_or_0(marketCap) / return_val_or_0(saleDivident),2)
		# if operatingProfit and otherIncome and depreciation and enterpriseVal:
		ebitda = return_val_or_0(operatingProfit) + return_val_or_0(otherIncome) + return_val_or_0(depreciation)
		# if ebitda == 0:
		# 	ebitda = 1
		evByEbitda = round(enterpriseVal / return_val_or_1(ebitda),2)
		
		# if netProfit and totalEquityCY and totalEquityPY:
		avgTotalEquity = (return_val_or_0(totalEquityCY) + return_val_or_0(totalEquityPY)) / Decimal(2)
		# roe = netProfit / avgTotalEquity
		roe = return_val_or_0(netProfit) / return_val_or_1(avgTotalEquity)
		roe = round(roe * 100,2)
		
		if stockFinancialSystem:
			if marketCap:
				marketCap = numberConversion(marketCap, 'Cr', stockFinancialSystem)
			if revenue:
				revenue = numberConversion(revenue, 'Cr', stockFinancialSystem)
		context = {
			'id':stockID,
			'type':stockType,
			'fetchedUrl': urlToCrawl,
			'revenue': revenue,
			'netProfitMargin': npm,
			'assetTurnoverRation': totalAssetTurnoverRatio,
			'ROE': roe,
			'ROCE': roce,
			'deptToEquity': debtToEquity,
			'peGraph': peGraph,
			'pbGraph': pbGraph,
			'marketCap': marketCap,
			'marketCapBySales': marketCapBySales,
			'enterpriseVal': enterpriseVal,
			'evByEbitda': evByEbitda,
			'cashAndShortTermEquivalents': cashAndShortTerm,
			'PreferenceEquity': preferenceEquity,
			'totalMinorityInterest': minorityInterest,
			'longTermMarketableSecurities': longTermSecurities,
			'yearNotAvailable': yearNotAvailable,
			'yearlyData': yearlyData_list,
		}
		return context
	except:
		context = {
			'id':stockID,
			'type':stockType,
			'fetchedUrl': urlToCrawl,
			}
		return context

#
def crawlScreenerForBankNBFCView(company, fetchForYear):
	urlToCrawl= company.screenerLink
	stockID= company.id
	stockType= company.stockStatus
	try:
		source = requests.get(str(urlToCrawl)).text
		soup = BeautifulSoup(source, 'lxml')
		# financial Figure units are in
		try:
			stockFinancialSystemInst = financialFigureUnits.objects.get(stockProfileName=company.stockProfileName)
			stockFinancialSystem = stockFinancialSystemInst.financialNumbers
		except:
			stockFinancialSystem = None
		forCount = 0
		yearFound = noOfcolToExtract = False
		yearNotAvailable = []
		for item in soup.find(id="profit-loss").find('table', class_='data-table responsive-text-nowrap').find('thead').find_all('th'):
			thVal = item.renderContents().strip().decode("utf-8")
			if yearFound:
				if not 'TTM' in thVal:
					yearNotAvailable.append(thVal)
			if str(fetchForYear) in thVal:
				noOfcolToExtract = forCount
				yearFound = True
			forCount += 1
		if not noOfcolToExtract:
			noOfcolToExtract = forCount - 1
		forCount = 0
		revenue = interest = otherIncome = netProfit = 0
		for item in soup.find(id="profit-loss").find('table', class_='data-table responsive-text-nowrap').find('tbody').find_all('tr'):
			extdPLItem = item.findAll('td')
			if forCount == 0:
				revenue = extdPLItem[noOfcolToExtract].renderContents().strip().decode("utf-8").replace(',', '')
				try:
					revenue = Decimal(revenue)
				except:
					revenue = Decimal(0)
			elif forCount == 1:
				interest = extdPLItem[noOfcolToExtract].renderContents().strip().decode("utf-8").replace(',', '')
				try:
					interest = Decimal(interest)
				except:
					interest = Decimal(0)
			elif forCount == 5:
				otherIncome = extdPLItem[noOfcolToExtract].renderContents().strip().decode("utf-8").replace(',', '')
				try:
					otherIncome = Decimal(otherIncome)
				except:
					otherIncome = Decimal(0)
			elif forCount == 9:
				netProfit = extdPLItem[noOfcolToExtract].renderContents().strip().decode("utf-8").replace(',', '')
				try:
					netProfit = Decimal(netProfit)
				except:
					netProfit = Decimal(0)
			forCount += 1
		forCount = 0
		avgTotalAsset = shareCapitalCY = shareCapitalPY = reservesCY = reservesPY = avgBorrowings = 0
		for item in soup.find(id="balance-sheet").find('table', class_='data-table responsive-text-nowrap').find('tbody').find_all('tr'):
			extdPLItem = item.findAll('td')
			if forCount == 0:
				shareCapitalCY = extdPLItem[noOfcolToExtract].renderContents().strip().decode("utf-8").replace(',', '')
				shareCapitalPY = extdPLItem[noOfcolToExtract-1].renderContents().strip().decode("utf-8").replace(',', '')
				try:
					shareCapitalCY = Decimal(shareCapitalCY)
				except:
					shareCapitalCY = Decimal(0)
				try:
					shareCapitalPY = Decimal(shareCapitalPY)
				except:
					shareCapitalPY = Decimal(0)
			elif forCount == 1:
				reservesCY = extdPLItem[noOfcolToExtract].renderContents().strip().decode("utf-8").replace(',', '')
				reservesPY = extdPLItem[noOfcolToExtract-1].renderContents().strip().decode("utf-8").replace(',', '')
				try:
					reservesCY = Decimal(reservesCY)
				except:
					reservesCY = Decimal(0)
				try:
					reservesPY = Decimal(reservesPY)
				except:
					reservesPY = Decimal(0)
			elif forCount == 2:
				borrowingsCY = extdPLItem[noOfcolToExtract].renderContents().strip().decode("utf-8").replace(',', '')
				borrowingsPY = extdPLItem[noOfcolToExtract-1].renderContents().strip().decode("utf-8").replace(',', '')
				try:
					borrowingsCY = Decimal(borrowingsCY)
				except:
					borrowingsCY = Decimal(0)
				try:
					borrowingsPY = Decimal(borrowingsPY)
				except:
					borrowingsPY = Decimal(0)
				avgBorrowings = (borrowingsCY + borrowingsPY) / 2
			elif forCount == 9:
				totalAssetCY = extdPLItem[noOfcolToExtract].renderContents().strip().decode("utf-8").replace(',', '')
				totalAssetPY = extdPLItem[noOfcolToExtract-1].renderContents().strip().decode("utf-8").replace(',', '')
				try:
					totalAssetCY = Decimal(totalAssetCY)
				except:
					totalAssetCY = Decimal(0)
				try:
					totalAssetPY = Decimal(totalAssetPY)
				except:
					totalAssetPY = Decimal(0)
				avgTotalAsset = (totalAssetCY + totalAssetPY) / 2
			forCount += 1
		forCount = 0
		roe = 0
		for item in soup.find(id="ratios").find('table', class_='data-table responsive-text-nowrap').find('tbody').find_all('tr'):
			extdPLItem = item.findAll('td')
			if forCount == 0:
				roe = extdPLItem[noOfcolToExtract].renderContents().strip().decode("utf-8").replace('%', '')
				try:
					roe = Decimal(roe)
				except:
					roe = Decimal(0)
			forCount += 1
		forCount = 0
		stockPE = marketCap = 0
		for item in soup.find(id="top-ratios").find_all('li'):
			fetchedValDiv = item.find('span', class_='name').renderContents().strip().decode("utf-8")
			fetchedValVal = (item.find('span', class_='number').renderContents().strip().decode("utf-8").replace(',', ''))
			try:
				fetchedValVal = Decimal(fetchedValVal)
			except:
				fetchedValVal = Decimal(0)
			if fetchedValDiv == 'Current Price':
				currentPrice = fetchedValVal
			elif fetchedValDiv == 'Book Value':
				bookValue = fetchedValVal
			elif fetchedValDiv == 'Stock P/E':
				stockPE = fetchedValVal
			elif fetchedValDiv == 'Market Cap':
				marketCap = fetchedValVal

		# formulas
		netInterestIncome = return_val_or_0(revenue) - return_val_or_0(interest)
		totalRevenue = return_val_or_0(revenue) + return_val_or_0(otherIncome) - return_val_or_0(interest)
		roa = return_val_or_0(netProfit) / return_val_or_1(avgTotalAsset)
		netProfitMargin = return_val_or_0(netProfit) / return_val_or_1(netInterestIncome)
		assetTurnOverRatio = return_val_or_0(netInterestIncome) / return_val_or_0(avgTotalAsset)
		roe = roe
		stockPE = stockPE
		if bookValue == 0:
			bookValue = 1
		stockPB = return_val_or_0(currentPrice) / return_val_or_1(bookValue)
		shareCapPlusReserveCY = return_val_or_0(shareCapitalCY) + return_val_or_0(reservesCY)
		shareCapPlusReservePY = return_val_or_0(shareCapitalPY) + return_val_or_0(reservesPY)
		avgShareCapPlusReserve = (return_val_or_0(shareCapPlusReserveCY) + return_val_or_0(shareCapPlusReservePY)) / 2
		debtToEquityRatio = return_val_or_0(avgBorrowings) / return_val_or_1(avgShareCapPlusReserve)
		nim = return_val_or_0(netInterestIncome) / return_val_or_1(avgTotalAsset)
		# manual Entries
		yearlyData = peerLinkingYearlyDataForBankNBFC.objects.filter(screenerCompany=company)
		try:
			stockYearData = yearlyData.get(year=fetchForYear)
		except:
			stockYearData = None
		try:
			stockYearDataPY = yearlyData.get(year=int(fetchForYear) - 1)
		except:
			stockYearDataPY = None
		car = netNPA = grossNPA = CASA = tier1CapitalRatio = tier2CapitalRatio = totalAMU = RORWA = intangibleAssets = 0
		goodwillCY = loanLossProvisionCY = 0
		numberOfShares = 1
		screenerHaveGrossNPA = screenerHaveNetNPA = False
		marchIsOn = None
		for item in soup.find(id="quarters").find('table', class_='data-table responsive-text-nowrap').find('thead').find_all('tr'):
			quarterFetch = 'Mar '+str(fetchForYear)
			extdPLItem = item.findAll('th')
			counterForFor = 0
			for item in extdPLItem:
				if quarterFetch == item.renderContents().strip().decode("utf-8"):
					marchIsOn = counterForFor
					break;
				counterForFor += 1
			# return HttpResponse(str(marchIsOn))
		netNPAScreener = grossNPAScreener = None
		forCount = 0
		if marchIsOn:
			for item in soup.find(id="quarters").find('table', class_='data-table responsive-text-nowrap').find('tbody').find_all('tr'):
				extdPLItem = item.findAll('td')
				if forCount == 11:
					grossNPA = extdPLItem[marchIsOn].renderContents().strip().decode("utf-8").replace('%', '')
					try:
						grossNPAScreener = Decimal(grossNPA)
					except:
						grossNPAScreener = Decimal(0)
				elif forCount == 12:
					netNPA = extdPLItem[marchIsOn].renderContents().strip().decode("utf-8").replace('%', '')
					try:
						netNPAScreener = Decimal(netNPA)
					except:
						netNPAScreener = Decimal(0)
				forCount += 1
		if stockYearData:
			car = stockYearData.CAR
			if netNPAScreener:
				netNPA = netNPAScreener
			else:
				netNPA = stockYearData.netNPA
			if grossNPAScreener:
				grossNPA = grossNPAScreener
			else:
				grossNPA = stockYearData.grossNPA
			
			CASA = stockYearData.CASA
			tier1CapitalRatio = stockYearData.tier1CapitalRatio
			tier2CapitalRatio = stockYearData.tier2CapitalRatio
			totalAMU = stockYearData.totalAMU
			RORWA = stockYearData.RORWA
			numberOfShares = stockYearData.numberOfShares
			intangibleAssets = stockYearData.intangibleAssests
			goodwillCY = stockYearData.goodwill
			loanLossProvisionCY = stockYearData.loanLossProvision
		intangibleAssestsPY = goodwillPY =  0
		if stockYearDataPY:
			intangibleAssestsPY = stockYearDataPY.intangibleAssests
			goodwillPY = stockYearDataPY.goodwill
		forAvg1 = return_val_or_0(shareCapitalCY) + return_val_or_0(reservesCY) - return_val_or_0(intangibleAssets) - return_val_or_0(goodwillCY)
		forAvg2 = return_val_or_0(shareCapitalPY) + return_val_or_0(reservesPY) - return_val_or_0(intangibleAssestsPY) - return_val_or_0(goodwillPY)
		avgForTByTB = (return_val_or_0(forAvg1) + return_val_or_0(forAvg2)) / 2
		tByTBDivisor = return_val_or_0(avgForTByTB) / return_val_or_1(numberOfShares)
		tByTB = return_val_or_0(currentPrice) / return_val_or_1(tByTBDivisor)
		totalRevenue = totalRevenue - return_val_or_0(loanLossProvisionCY)
		if stockFinancialSystem:
			if netInterestIncome:
				netInterestIncome = numberConversion(netInterestIncome, 'Cr', stockFinancialSystem)
			if totalRevenue:
				totalRevenue = numberConversion(totalRevenue, 'Cr', stockFinancialSystem)
			if marketCap:
				marketCap = numberConversion(marketCap, 'Cr', stockFinancialSystem)
		context = {
			'id':stockID,
			'type':stockType,
			'fetchedUrl': urlToCrawl,
			'revenue': round(return_val_or_0(totalRevenue),2),
			'netInterestIncome': round(return_val_or_0(netInterestIncome),2),
			'roa': round(return_val_or_0(roa * 100 ),2),
			'netProfitMarginPercentage': round(return_val_or_0(netProfitMargin * 100 ),2),
			'assetTurnOverRatio': round(return_val_or_0(assetTurnOverRatio),2),
			'roe': round(return_val_or_0(roe),2),
			'stockPE': round(return_val_or_0(stockPE),2),
			'stockPB': round(return_val_or_0(stockPB),2),
			'debtToEquityRatio': round(return_val_or_0(debtToEquityRatio),2),
			'nim': round(return_val_or_0(nim * 100),2),
			'car': round(return_val_or_0(car),2),
			'netNPA': round(return_val_or_0(netNPA),2),
			'grossNPA': round(return_val_or_0(grossNPA),2),
			'CASA': round(return_val_or_0(CASA),2),
			'tier1': round(return_val_or_0(tier1CapitalRatio),2),
			'tier2': round(return_val_or_0(tier2CapitalRatio),2),
			'totalAMU': round(return_val_or_0(totalAMU),2),
			'RORWA': round(return_val_or_0(RORWA),2),
			'numberOfShares': round(return_val_or_0(numberOfShares),2),
			'intangibleAssests': round(return_val_or_0(intangibleAssets),2),
			'pByTB': round(return_val_or_0(tByTB),2),
			'marketCap': round(return_val_or_0(marketCap),2),
			'yearlyData': yearlyData,
			}
		return context
	except:
		context = {
			'id':stockID,
			'type':stockType,
			'fetchedUrl': urlToCrawl,
			}
		return context

#
# def crawlScreenerForBankNBFCView(company, fetchForYear):
# 	urlToCrawl= company.screenerLink
# 	stockID= company.id
# 	stockType= company.stockStatus
# 	try:		
# 		source = requests.get(str(urlToCrawl)).text
# 		soup = BeautifulSoup(source, 'lxml')
# 		# financial Figure units are in
# 		try:
# 			stockFinancialSystemInst = financialFigureUnits.objects.get(stockProfileName=company.stockProfileName)
# 			stockFinancialSystem = stockFinancialSystemInst.financialNumbers
# 		except:
# 			stockFinancialSystem = None
# 		forCount = 0
# 		yearFound = False
# 		yearNotAvailable = []
# 		for item in soup.find(id="profit-loss").find('table', class_='data-table responsive-text-nowrap').find('thead').find_all('th'):
# 			thVal = item.renderContents().strip().decode("utf-8")
# 			if yearFound:
# 				if not 'TTM' in thVal:
# 					yearNotAvailable.append(thVal)
# 			if str(fetchForYear) in thVal:
# 				noOfcolToExtract = forCount
# 				yearFound = True
# 			forCount += 1
# 		forCount = 0
# 		revenue = interest = otherIncome = netProfit = 0
# 		for item in soup.find(id="profit-loss").find('table', class_='data-table responsive-text-nowrap').find('tbody').find_all('tr'):
# 			extdPLItem = item.findAll('td')
# 			if forCount == 0:
# 				revenue = extdPLItem[noOfcolToExtract].renderContents().strip().decode("utf-8").replace(',', '')
# 				try:
# 					revenue = Decimal(revenue)
# 				except:
# 					revenue = Decimal(0)
# 			elif forCount == 1:
# 				interest = extdPLItem[noOfcolToExtract].renderContents().strip().decode("utf-8").replace(',', '')
# 				try:
# 					interest = Decimal(interest)
# 				except:
# 					interest = Decimal(0)
# 			elif forCount == 5:
# 				otherIncome = extdPLItem[noOfcolToExtract].renderContents().strip().decode("utf-8").replace(',', '')
# 				try:
# 					otherIncome = Decimal(otherIncome)
# 				except:
# 					otherIncome = Decimal(0)
# 			elif forCount == 9:
# 				netProfit = extdPLItem[noOfcolToExtract].renderContents().strip().decode("utf-8").replace(',', '')
# 				try:
# 					netProfit = Decimal(netProfit)
# 				except:
# 					netProfit = Decimal(0)
# 			forCount += 1
# 		forCount = 0
# 		avgTotalAsset = shareCapitalCY = shareCapitalPY = reservesCY = reservesPY = avgBorrowings = 0
# 		for item in soup.find(id="balance-sheet").find('table', class_='data-table responsive-text-nowrap').find('tbody').find_all('tr'):
# 			extdPLItem = item.findAll('td')
# 			if forCount == 0:
# 				shareCapitalCY = extdPLItem[noOfcolToExtract].renderContents().strip().decode("utf-8").replace(',', '')
# 				shareCapitalPY = extdPLItem[noOfcolToExtract-1].renderContents().strip().decode("utf-8").replace(',', '')
# 				try:
# 					shareCapitalCY = Decimal(shareCapitalCY)
# 				except:
# 					shareCapitalCY = Decimal(0)
# 				try:
# 					shareCapitalPY = Decimal(shareCapitalPY)
# 				except:
# 					shareCapitalPY = Decimal(0)
# 			elif forCount == 1:
# 				reservesCY = extdPLItem[noOfcolToExtract].renderContents().strip().decode("utf-8").replace(',', '')
# 				reservesPY = extdPLItem[noOfcolToExtract-1].renderContents().strip().decode("utf-8").replace(',', '')
# 				try:
# 					reservesCY = Decimal(reservesCY)
# 				except:
# 					reservesCY = Decimal(0)
# 				try:
# 					reservesPY = Decimal(reservesPY)
# 				except:
# 					reservesPY = Decimal(0)
# 			elif forCount == 2:
# 				borrowingsCY = extdPLItem[noOfcolToExtract].renderContents().strip().decode("utf-8").replace(',', '')
# 				borrowingsPY = extdPLItem[noOfcolToExtract-1].renderContents().strip().decode("utf-8").replace(',', '')
# 				try:
# 					borrowingsCY = Decimal(borrowingsCY)
# 				except:
# 					borrowingsCY = Decimal(0)
# 				try:
# 					borrowingsPY = Decimal(borrowingsPY)
# 				except:
# 					borrowingsPY = Decimal(0)
# 				avgBorrowings = (borrowingsCY + borrowingsPY) / 2
# 			elif forCount == 9:
# 				totalAssetCY = extdPLItem[noOfcolToExtract].renderContents().strip().decode("utf-8").replace(',', '')
# 				totalAssetPY = extdPLItem[noOfcolToExtract-1].renderContents().strip().decode("utf-8").replace(',', '')
# 				try:
# 					totalAssetCY = Decimal(totalAssetCY)
# 				except:
# 					totalAssetCY = Decimal(0)
# 				try:
# 					totalAssetPY = Decimal(totalAssetPY)
# 				except:
# 					totalAssetPY = Decimal(0)
# 				avgTotalAsset = (totalAssetCY + totalAssetPY) / 2
# 			forCount += 1
# 		forCount = 0
# 		roe = 0
# 		for item in soup.find(id="ratios").find('table', class_='data-table responsive-text-nowrap').find('tbody').find_all('tr'):
# 			extdPLItem = item.findAll('td')
# 			if forCount == 0:
# 				roe = extdPLItem[noOfcolToExtract].renderContents().strip().decode("utf-8").replace('%', '')
# 				try:
# 					roe = Decimal(roe)
# 				except:
# 					roe = Decimal(0)
# 			forCount += 1
# 		forCount = 0
# 		stockPE = 0
# 		for item in soup.find(id="top-ratios").find_all('li'):
# 			fetchedValDiv = item.find('span', class_='name').renderContents().strip().decode("utf-8")
# 			fetchedValVal = (item.find('span', class_='number').renderContents().strip().decode("utf-8").replace(',', ''))
# 			try:
# 				fetchedValVal = Decimal(fetchedValVal)
# 			except:
# 				fetchedValVal = Decimal(0)
# 			if fetchedValDiv == 'Current Price':
# 				currentPrice = fetchedValVal
# 			elif fetchedValDiv == 'Book Value':
# 				bookValue = fetchedValVal
# 			elif fetchedValDiv == 'Stock P/E':
# 				stockPE = fetchedValVal

# 		# formulas
# 		netInterestIncome = return_val_or_0(revenue) - return_val_or_0(interest)
# 		totalRevenue = return_val_or_0(revenue) + return_val_or_0(otherIncome) - return_val_or_0(interest)
# 		roa = return_val_or_0(netProfit) / return_val_or_1(avgTotalAsset)
# 		netProfitMargin = return_val_or_0(netProfit) / return_val_or_1(netInterestIncome)
# 		assetTurnOverRatio = return_val_or_0(netInterestIncome) / return_val_or_0(avgTotalAsset)
# 		roe = roe
# 		stockPE = stockPE
# 		if bookValue == 0:
# 			bookValue = 1
# 		stockPB = return_val_or_0(currentPrice) / return_val_or_1(bookValue)
# 		shareCapPlusReserveCY = return_val_or_0(shareCapitalCY) + return_val_or_0(reservesCY)
# 		shareCapPlusReservePY = return_val_or_0(shareCapitalPY) + return_val_or_0(reservesPY)
# 		avgShareCapPlusReserve = (return_val_or_0(shareCapPlusReserveCY) + return_val_or_0(shareCapPlusReservePY)) / 2
# 		debtToEquityRatio = return_val_or_0(avgBorrowings) / return_val_or_1(avgShareCapPlusReserve)
# 		nim = return_val_or_0(netInterestIncome) / return_val_or_1(avgTotalAsset)
# 		# manual Entries
# 		yearlyData = peerLinkingYearlyDataForBankNBFC.objects.filter(screenerCompany=company)
# 		try:
# 			stockYearData = yearlyData.get(year=fetchForYear)
# 		except:
# 			stockYearData = None
# 		try:
# 			stockYearDataPY = yearlyData.get(year=int(fetchForYear) - 1)
# 		except:
# 			stockYearDataPY = None
# 		car = netNPA = grossNPA = CASA = tier1CapitalRatio = tier2CapitalRatio = totalAMU = RORWA = intangibleAssets = 0
# 		goodwillCY = loanLossProvisionCY = 0
# 		numberOfShares = 1
# 		screenerHaveGrossNPA = screenerHaveNetNPA = False
# 		marchIsOn = None
# 		for item in soup.find(id="quarters").find('table', class_='data-table responsive-text-nowrap').find('thead').find_all('tr'):
# 			quarterFetch = 'Mar '+str(fetchForYear)
# 			extdPLItem = item.findAll('th')
# 			counterForFor = 0
# 			for item in extdPLItem:
# 				if quarterFetch == item.renderContents().strip().decode("utf-8"):
# 					marchIsOn = counterForFor
# 					break;
# 				counterForFor += 1
# 			# return HttpResponse(str(marchIsOn))
# 		netNPAScreener = grossNPAScreener = None
# 		forCount = 0
# 		if marchIsOn:
# 			for item in soup.find(id="quarters").find('table', class_='data-table responsive-text-nowrap').find('tbody').find_all('tr'):
# 				extdPLItem = item.findAll('td')
# 				if forCount == 11:
# 					grossNPA = extdPLItem[marchIsOn].renderContents().strip().decode("utf-8").replace('%', '')
# 					try:
# 						grossNPAScreener = Decimal(grossNPA)
# 					except:
# 						grossNPAScreener = Decimal(0)
# 				elif forCount == 12:
# 					netNPA = extdPLItem[marchIsOn].renderContents().strip().decode("utf-8").replace('%', '')
# 					try:
# 						netNPAScreener = Decimal(netNPA)
# 					except:
# 						netNPAScreener = Decimal(0)
# 				forCount += 1
# 		if stockYearData:
# 			car = stockYearData.CAR
# 			if netNPAScreener:
# 				netNPA = netNPAScreener
# 			else:
# 				netNPA = stockYearData.netNPA
# 			if grossNPAScreener:
# 				grossNPA = grossNPAScreener
# 			else:
# 				grossNPA = stockYearData.grossNPA
			
# 			CASA = stockYearData.CASA
# 			tier1CapitalRatio = stockYearData.tier1CapitalRatio
# 			tier2CapitalRatio = stockYearData.tier2CapitalRatio
# 			totalAMU = stockYearData.totalAMU
# 			RORWA = stockYearData.RORWA
# 			numberOfShares = stockYearData.numberOfShares
# 			intangibleAssets = stockYearData.intangibleAssests
# 			goodwillCY = stockYearData.goodwill
# 			loanLossProvisionCY = stockYearData.loanLossProvision
# 		intangibleAssestsPY = goodwillPY =  0
# 		if stockYearDataPY:
# 			intangibleAssestsPY = stockYearDataPY.intangibleAssests
# 			goodwillPY = stockYearDataPY.goodwill
# 		forAvg1 = return_val_or_0(shareCapitalCY) + return_val_or_0(reservesCY) - return_val_or_0(intangibleAssets) - return_val_or_0(goodwillCY)
# 		forAvg2 = return_val_or_0(shareCapitalPY) + return_val_or_0(reservesPY) - return_val_or_0(intangibleAssestsPY) - return_val_or_0(goodwillPY)
# 		avgForTByTB = (return_val_or_0(forAvg1) + return_val_or_0(forAvg2)) / 2
# 		tByTBDivisor = return_val_or_0(avgForTByTB) / return_val_or_1(numberOfShares)
# 		tByTB = return_val_or_0(currentPrice) / return_val_or_1(tByTBDivisor)
# 		totalRevenue = totalRevenue - return_val_or_0(loanLossProvisionCY)
# 		if stockFinancialSystem:
# 			if netInterestIncome:
# 				netInterestIncome = numberConversion(netInterestIncome, 'Cr', stockFinancialSystem)
# 			if totalRevenue:
# 				totalRevenue = numberConversion(totalRevenue, 'Cr', stockFinancialSystem)
# 		context = {
# 			'id':stockID,
# 			'type':stockType,
# 			'fetchedUrl': urlToCrawl,
# 			'revenue': round(return_val_or_0(totalRevenue),2),
# 			'netInterestIncome': round(return_val_or_0(netInterestIncome),2),
# 			'roa': round(return_val_or_0(roa * 100 ),2),
# 			'netProfitMarginPercentage': round(return_val_or_0(netProfitMargin * 100 ),2),
# 			'assetTurnOverRatio': round(return_val_or_0(assetTurnOverRatio),2),
# 			'roe': round(return_val_or_0(roe),2),
# 			'stockPE': round(return_val_or_0(stockPE),2),
# 			'stockPB': round(return_val_or_0(stockPB),2),
# 			'debtToEquityRatio': round(return_val_or_0(debtToEquityRatio),2),
# 			'nim': round(return_val_or_0(nim * 100),2),
# 			'car': round(return_val_or_0(car),2),
# 			'netNPA': round(return_val_or_0(netNPA),2),
# 			'grossNPA': round(return_val_or_0(grossNPA),2),
# 			'CASA': round(return_val_or_0(CASA),2),
# 			'tier1': round(return_val_or_0(tier1CapitalRatio),2),
# 			'tier2': round(return_val_or_0(tier2CapitalRatio),2),
# 			'totalAMU': round(return_val_or_0(totalAMU),2),
# 			'RORWA': round(return_val_or_0(RORWA),2),
# 			'numberOfShares': round(return_val_or_0(numberOfShares),2),
# 			'intangibleAssests': round(return_val_or_0(intangibleAssets),2),
# 			'pByTB': round(return_val_or_0(tByTB),2),
# 			'yearlyData': yearlyData,
# 			}
# 		return context
# 	except:
# 		context = {
# 			'id':stockID,
# 			'type':stockType,
# 			'fetchedUrl': urlToCrawl,
# 			}
# 		return context