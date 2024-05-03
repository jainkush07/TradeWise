from cartApp.models import UserCart, CartItems, Transaction
from websiteApp.models import buyPreIPOStockList
import pdfkit
from django.core.files.base import ContentFile
from django.template import Template, Context
import base64
from django.contrib.auth.models import User
from employeeApp.models import employeePersonalDetails
from investorApp.models import investorPersonalDetails

class TransactionServices:

    def __init__(self, user):
        self.user_id = user.id
        self.user = user
    
    def _fetch_stock_details(self, item):
        stock_name = item.selected_stock
        # stock_price_inst = stockDailyUpdates.objects.get(stockProfile = stock_name)
        return {
                'id': stock_name.id,
                'name': stock_name.stockName,
                'slug': stock_name.slug,
                'ticker': stock_name.ticker,
                # "value": stock_val,
                # 'stock_pricce': stock_price_inst.price,
                'logo': stock_name.logo.url if stock_name.logo else '',
        }

    def _fetch_trade_data(self, item):
        stock_details = self._fetch_stock_details(item)
        stock_price = item.amount / item.quantity
        
        return {
            "transaction_id": item.id,
            "order_id" : item.order_id,
            "stock_details" : stock_details,
            "txn_made_by" : item.txn_made_by,
            "quantity" : item.quantity,
            "Amount" : round(item.amount,2),
            "buy_price" : round(stock_price,2),
            "investMentPrice" : round(item.investMentPrice,2),
            "payment_status" : item.payment_status,
            "transaction_date" : item.trxnDate,
            "sb_Depository" : item.sb_Depository,
            "sb_Company" : item.sb_Company,
            "sb_shareTransfer" : item.sb_shareTransfer
        }
    
    def get_tradebook_details(self):
        user_id = self.user_id
        user_trade_inst = Transaction.objects.filter(made_by = user_id).order_by('-trxnDate')
        user_trade_list = []
        for item in user_trade_inst:
            if item.payment_status == "Payment Successful":
                user_trade_list.append(
                    self._fetch_trade_data(item)
                )
        return {
            'user_id': user_id,
            'user_trade_list': user_trade_list
        }

    def _generate_user_agreement_html(self, data):
        agreement = open('cartApp/templates/cart/invoiceGen.html', 'r', encoding="utf8").read().replace('\n', '')
        # agreement = open('cartApp/templates/cart/sampleInvoice.html', 'r', encoding="utf8").read().replace('\n', '')
        return Template(agreement).render(Context(data))

    def tempInvoice(self):
        data = {"msg": "Planify_Sample_Invoice"}
        html = self._generate_user_agreement_html(data)
        pdf = self._generate_html_pdf(html)
        pdf_data = base64.b64encode(pdf)
        files = {'agreement': pdf_data}
        data = files
        return files

    def _generate_html_pdf(self, html):
        options = {
            'page-height': "1040px",
            'page-width': "800px",
            'margin-top': '20px',
            'margin-right': '5px',
            'margin-bottom': '20px',
            'margin-left': '5px',
            'encoding': "UTF-8",
            'disable-smart-shrinking': '',
            'no-outline': None,
            '--enable-javascript': '',
            'enable-local-file-access': None
        }
        pdf = pdfkit.from_string(html, False, options=options)
        return pdf    

    def fetch_tran_invoice(self, data):
        try:
            order_db = Transaction.objects.get(id = data.get('pk'), made_by = self.user, payment_status = 'Payment Successful')     
        except Exception as e:
            # print(e)
            return {'msg': '505 object is not found !', 'status': False}
        buyerInst = self._fetch_user_details()
        sellerDetail = self._fetch_seler_details(order_db)
        data = {
            'order': order_db.id,
            'order_id': order_db.order_id,
            'name': order_db.made_by.username,
            'user_email': order_db.made_by.email,
            'stockName': order_db.selected_stock.stockName,
            'trxnDate': order_db.trxnDate.strftime("%d-%b-%y"),
            'quantity': round(order_db.quantity),
            'investMentPrice': round(order_db.investMentPrice,2),
            'amount': round(order_db.amount, 2),
            'sb_shareTransfer': order_db.sb_shareTransfer,
            'buyerInst':buyerInst,
            'sellerDetail': sellerDetail,
        }
        # print(data)
        html = self._generate_user_agreement_html(data)
        # print(html)
        pdf = self._generate_html_pdf(html)
        # pdf_data = ContentFile(base64.b64decode(pdf), name=f'{data["msg"]}_invoice.pdf')
        pdf_data = base64.b64encode(pdf)
        # print(pdf_data)
        files = {'agreement': pdf_data}
        return files

    def _fetch_user_details(self):
        user =  self.user
        # print(user)
        try:
            user_obj = investorPersonalDetails.objects.get(profileOwner = user)
            return {
                "name": user_obj.name,
                "personalEmail": user_obj.emailVerified,
                "mobileNumber": user_obj.mobileNumber,
                "aadharNumber": user_obj.aadharNumber,
                "panNumber": user_obj.panNumber,
            }
        except:
            pass
        return {
                "name": "------",
                "personalEmail": "------",
                "mobileNumber": "------",
                "aadharNumber": "------",
                "panNumber": "------",
            }
        
    def _fetch_seler_details(self, order_db):
        if order_db:
            if order_db.sb_Company == "Planify Enterprises":
                return { "seller_company": "Planify Enterprises", "pan_number": "AALCP8636R" , "email": "demat@planify.in", "contact_no": "8882410001", "dp_id": "IN302822 - 10472040"}
            elif order_db.sb_Company == "Planify Capital":
                return { "seller_company": "Planify Capital", "pan_number": "AALCP8636R" , "email": "demat@planify.in", "contact_no": "+91 8882410001", "dp_id": "IN302822 - 10472040"}
        return {}
    
