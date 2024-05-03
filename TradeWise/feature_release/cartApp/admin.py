from django.contrib import admin
from .models import Transaction
from import_export.widgets import ForeignKeyWidget, ManyToManyWidget
from import_export.admin import ImportExportModelAdmin
from import_export import resources
from import_export import fields, resources
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User


class TransactionResource(resources.ModelResource):
	made_by = fields.Field(column_name = 'made_by', attribute='made_by', widget=ForeignKeyWidget(User, 'username'))

	class Meta:
		model = Transaction
		fields = ('made_by', 'made_on', 'amount', 'order_id', 'selected_stock', 'checksum', 'pg_MID', 'pg_txnID', 'pg_txnAmount', 'pg_paymentMode', 'pg_currency', 'pg_txnDate', 'pg_status', 'pg_repsonseCode', 'pg_responseMsg', 'pg_gatewayName', 'pg_bankTxnID', 'pg_bankName', 'pg_checkSubHash', 'quantity', 'investMentPrice', 'txn_made_by', 'trxnDate', 'publish', 'created', 'updated', 'status')


class TransactionImport(ImportExportModelAdmin):
	resource_class = TransactionResource

admin.site.register(Transaction, TransactionImport)




