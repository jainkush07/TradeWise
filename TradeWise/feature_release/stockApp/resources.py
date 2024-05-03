from import_export import resources
from stockApp.models import stockBalanceSheet, stockProfitAndLoss, stockCashFlow, stockBalanceSheetBankNBFC, stockProfitAndLossBankNBFC

#
class BalanceSheetResource(resources.ModelResource):
	class Meta:
		model = stockBalanceSheet
		exclude = ['publish', 'created', 'updated', 'status', 'analyst', 'verifiedBy']

#
class profitAndLossResource(resources.ModelResource):
	class Meta:
		model = stockProfitAndLoss
		exclude = ['publish', 'created', 'updated', 'status', 'analyst', 'verifiedBy']

#
class cashFlowResource(resources.ModelResource):
	class Meta:
		model = stockCashFlow
		exclude = ['publish', 'created', 'updated', 'status', 'analyst', 'verifiedBy']	

#
class BalanceSheetBankNBFCResource(resources.ModelResource):
	class Meta:
		model = stockBalanceSheetBankNBFC
		exclude = ['publish', 'created', 'updated', 'status', 'analyst', 'verifiedBy']

#
class profitAndLossBankNBFCResource(resources.ModelResource):
	class Meta:
		model = stockProfitAndLossBankNBFC
		exclude = ['publish', 'created', 'updated', 'status', 'analyst', 'verifiedBy']