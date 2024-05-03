from django.shortcuts import render, HttpResponse
from django.contrib.auth import authenticate, login as auth_login
from django.conf import settings
from .models import Transaction
from django.http import JsonResponse
from .paytm import generate_checksum, verify_checksum
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from stockApp.models import stockBasicDetail
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from cartApp.services.cart_service import CartService
from cartApp.services.transaction_service import TransactionServices
import requests
import json
from rest_framework import status
from cartApp.serializer import ItemUpdateSerializer, ItemAddSerializer
from . import PaytmChecksum
from rest_framework.views import APIView
from rest_framework.response import Response

from decimal import Decimal


#
@login_required
def process_to_pg_view(request):
    amount = request.POST.get('amount')
    quantity = request.POST.get('quantity')
    selected_stock = request.POST.get('stock')
    investmentPrice = request.POST.get('investMentPrice')
    try:
        stockInst = stockBasicDetail.objects.get(pk=selected_stock)
    except:
        stockInst = None
    transactionUser = User.objects.get(pk=request.user.pk)
    try:
        from investorApp.models import investorDMATDetails
        dmatInst = investorDMATDetails.objects.get(profileOwner=transactionUser, is_default=True)
        client_broker = dmatInst.stockBroker.name
        client_depository = dmatInst.depository
        client_dpID = dmatInst.dpID
        client_clientID = dmatInst.clientID
    except:
        client_broker = client_depository = client_dpID = client_clientID = None
    try:
        from investorApp.models import investorBankDetails
        bankInst = investorBankDetails.objects.get(profileOwner=transactionUser, is_default=True)
        client_bank = bankInst.bankName
        client_accNumber = bankInst.accountNumber
    except:
        client_bank = client_accNumber = None
    transaction = Transaction.objects.create(
        made_by=transactionUser,
        selected_stock=stockInst,
        amount=amount.replace(",", ""),
        quantity=quantity,
        investMentPrice=investmentPrice,
        sb_brokerName=client_broker,
        sb_Depository=client_depository,
        sb_DpID=client_dpID,
        sb_clientID=client_clientID,
        sb_buyerBank=client_bank,
        sb_accountNo=client_accNumber,
        sb_KYC='Done',
    )
    transaction.save()
    if stockInst.get_funds_in == 'Planify Enterprise':
        MKEY = settings.PAYTM_SECRET_KEY_ENTERPRISE
        MID = settings.PAYTM_MERCHANT_ID_ENTERPRISE
    else:
        MKEY = settings.PAYTM_SECRET_KEY_CAPITAL
        MID = settings.PAYTM_MERCHANT_ID_CAPITAL
    current_site = get_current_site(request)
    domain = current_site.domain
    callbackUrlPath = reverse('cartApp:callback')
    if domain == 'localhost:8000':
        domain = 'http://127.0.0.1:8000'
        callbackURL = str(domain) + callbackUrlPath
    elif domain == 'localhost:8001':
        domain = 'http://127.0.0.1:8001'
        callbackURL = str(domain) + callbackUrlPath
    else:
        callbackURL = 'https://' + str(domain) + callbackUrlPath
    # initiate
    paytmParams = dict()
    order_id = str(transaction.order_id)
    paytmParams["body"] = {
        "requestType": "Payment",
        "mid": MID,
        "websiteName": "WEBSTAGING",
        "orderId": order_id,
        "callbackUrl": str(callbackURL),
        "txnAmount": {
            "value": str(transaction.amount),
            "currency": "INR",
        },
        "userInfo": {
            "custId": str(transaction.made_by.email),
        },
        "enablePaymentMode": [
            {
                "mode": "UPI",
                "channels": ["UPI", "UPIPUSH", "UPIPUSHEXPRESS", ]
            },
        ],
    }
    checksum = PaytmChecksum.generateSignature(json.dumps(paytmParams["body"]), MKEY)
    amount = request.POST.get('amount')
    quantity = request.POST.get('quantity')
    selected_stock = request.POST.get('stock')
    investmentPrice = request.POST.get('investMentPrice')
    # selected_stock_from_shareBook = request.POST.get('selected_stock')
    # print(selected_stock)
    if amount and quantity:
        if not investmentPrice:
            investmentPrice = Decimal(amount) / Decimal(quantity)

    try:
        stockInst = stockBasicDetail.objects.get(pk=selected_stock)
    except:
        stockInst = None

    print(stockInst)
    transactionUser = User.objects.get(pk=request.user.pk)
    transaction = Transaction.objects.create(
        made_by=transactionUser,
        selected_stock=stockInst,
        amount=amount.replace(",", ""), quantity=quantity, investMentPrice=investmentPrice)
    transaction.save()

    if stockInst.get_funds_in == 'Planify Enterprise':
        MKEY = settings.PAYTM_SECRET_KEY_ENTERPRISE
        MID = settings.PAYTM_MERCHANT_ID_ENTERPRISE
    else:
        MKEY = settings.PAYTM_SECRET_KEY_CAPITAL
        MID = settings.PAYTM_MERCHANT_ID_CAPITAL
    current_site = get_current_site(request)
    domain = current_site.domain
    callbackUrlPath = reverse('cartApp:callback')
    if domain == 'localhost:8000':
        domain = 'http://127.0.0.1:8000'
        callbackURL = str(domain) + callbackUrlPath
    elif domain == 'localhost:8001':
        domain = 'http://127.0.0.1:8001'
        callbackURL = str(domain) + callbackUrlPath
    else:
        callbackURL = 'https://' + str(domain) + callbackUrlPath
    # initiate
    paytmParams = dict()
    order_id = str(transaction.order_id)
    paytmParams["body"] = {
        "requestType": "Payment",
        "mid": MID,
        "websiteName": "WEBSTAGING",
        "orderId": order_id,
        "callbackUrl": str(callbackURL),
        "txnAmount": {
            "value": str(transaction.amount),
            "currency": "INR",
        },
        "userInfo": {
            "custId": str(transaction.made_by.email),
        },
        "enablePaymentMode": [
            {
                "mode": "UPI",
                "channels": ["UPI", "UPIPUSH", "UPIPUSHEXPRESS", ]
            },
        ],
    }
    checksum = PaytmChecksum.generateSignature(json.dumps(paytmParams["body"]), MKEY)

    paytmParams["head"] = {
        "signature": checksum
    }

    post_data = json.dumps(paytmParams)

    # for Staging
    # url = "https://securegw-stage.paytm.in/theia/api/v1/initiateTransaction?mid="+str(MID)+"&orderId="+str(order_id)

    # for Production
    url = "https://securegw.paytm.in/theia/api/v1/initiateTransaction?mid=" + str(MID) + "&orderId=" + str(order_id)
    response = requests.post(url, data=post_data, headers={"Content-type": "application/json"}).json()
    # print(f'INITIATE: {response}')
    try:
        TxnToken = response['body']['txnToken']
    except:
        TxnToken = {'message': 'We are facing some issues with Paytm'}
    context = {
        'order_id': order_id,
        'MID': MID,
        'TxnToken': TxnToken,
    }
    return render(request, 'cart/proceed_to_pay.html', context)


#
@csrf_exempt
def callback(request):
    if request.method == 'POST':
        # print(f'request.POST: {request.POST}')
        received_data = dict(request.POST)
        # print(f'received_data: {received_data}')
        orderId = received_data['ORDERID'][0]
        transactionInst = Transaction.objects.get(order_id=orderId)
        try:
            transactionInst.pg_MID = received_data['MID'][0]
        except:
            pass
        try:
            transactionInst.pg_txnID = received_data['TXNID'][0]
        except:
            pass
        try:
            transactionInst.pg_txnAmount = received_data['TXNAMOUNT'][0]
        except:
            pass
        try:
            transactionInst.pg_paymentMode = received_data['PAYMENTMODE'][0]
        except:
            pass
        try:
            transactionInst.pg_currency = received_data['CURRENCY'][0]
        except:
            pass
        try:
            transactionInst.pg_txnDate = received_data['TXNDATE'][0]
        except:
            pass
        try:
            transactionInst.pg_status = received_data['STATUS'][0]
        except:
            pass
        try:
            transactionInst.pg_repsonseCode = received_data['RESPCODE'][0]
        except:
            pass
        try:
            transactionInst.pg_responseMsg = received_data['RESPMSG'][0]
        except:
            pass
        try:
            transactionInst.pg_gatewayName = received_data['GATEWAYNAME'][0]
        except:
            pass
        try:
            transactionInst.pg_bankTxnID = received_data['BANKTXNID'][0]
        except:
            pass
        try:
            transactionInst.pg_bankName = received_data['BANKNAME'][0]
        except:
            pass
        try:
            transactionInst.pg_checkSubHash = received_data['CHECKSUMHASH'][0]
        except:
            pass

        transactionInst.save()
        paytm_params = {}
        paytm_checksum = received_data['CHECKSUMHASH'][0]
        for key, value in received_data.items():
            if key == 'CHECKSUMHASH':
                paytm_checksum = value[0]
            else:
                paytm_params[key] = str(value[0])
        # Verify checksum
        if transactionInst.selected_stock.get_funds_in == 'Planify Capital':
            secret_key = settings.PAYTM_SECRET_KEY_CAPITAL
        else:
            secret_key = settings.PAYTM_SECRET_KEY_ENTERPRISE
        is_valid_checksum = verify_checksum(paytm_params, secret_key, str(paytm_checksum))
        if is_valid_checksum:
            received_data['message'] = "Checksum Matched"
        else:
            received_data['message'] = "Checksum Mismatched"
            return render(request, 'cart/callback.html', context=received_data)
        return render(request, 'cart/callback.html', context=received_data)


#
# def process_to_pg_view(request):
@login_required()
def process_to_pg_new_flow_view(request):
    if request.method == 'POST':
        amount = request.POST.get('amount')
        quantity = request.POST.get('quantity')
        selected_stock = request.POST.get('stock')
        investmentPrice = request.POST.get('investMentPrice')

        stockInst = stockBasicDetail.objects.get(pk=selected_stock)
        transactionUser = User.objects.get(pk=request.user.pk)
        transaction = Transaction.objects.create(made_by=transactionUser, selected_stock=stockInst,
                                                 amount=amount.replace(",", ""), quantity=quantity,
                                                 investMentPrice=investmentPrice)
        transaction.save()
        if stockInst.get_funds_in == 'Planify Enterprise':
            merchant_key = settings.PAYTM_SECRET_KEY_ENTERPRISE
            merchant_id = settings.PAYTM_MERCHANT_ID_ENTERPRISE
        else:
            merchant_key = settings.PAYTM_SECRET_KEY_CAPITAL
            merchant_id = settings.PAYTM_MERCHANT_ID_CAPITAL
        current_site = get_current_site(request)
        domain = current_site.domain
        callbackUrlPath = reverse('cartApp:callback')
        if domain == 'localhost:8000':
            domain = 'http://127.0.0.1:8000'
            callbackURL = str(domain) + callbackUrlPath
        else:
            callbackURL = 'https://' + str(domain) + callbackUrlPath
        params = (
            ('MID', merchant_id),
            ('ORDER_ID', str(transaction.order_id)),
            ('CUST_ID', str(transaction.made_by.email)),
            ('TXN_AMOUNT', str(transaction.amount)),
            ('CHANNEL_ID', settings.PAYTM_CHANNEL_ID),
            ('WEBSITE', settings.PAYTM_WEBSITE),
            # ('EMAIL', request.user.email),
            # ('MOBILE_N0', '9911223388'),
            ('INDUSTRY_TYPE_ID', settings.PAYTM_INDUSTRY_TYPE_ID),
            ('CALLBACK_URL', callbackURL),
            # ('PAYMENT_MODES', '["UPIPUSH","UPI", "UPIPUSHEXPRESS"]'),
            # ('PAYMENT_MODES', '{"mode":"UPI","channels":["UPIPUSH","UPI", "UPIPUSHEXPRESS"]}'),
            # ('PAYMENT_MODE_ONLY', 'NO'),
        )

        paytm_params = dict(params)
        checksum = generate_checksum(paytm_params, merchant_key)

        transaction.checksum = checksum
        transaction.save()
        paytm_params['CHECKSUMHASH'] = checksum
        return render(request, 'cart/redirect.html', context=paytm_params)
    return render(request, 'cart/redirect.html')


#
def initiate_payment(request):
    if request.method == "GET":
        return render(request, 'cart/pay.html')
    try:
        username = request.POST['username']
        password = request.POST['password']
        amount = int(request.POST['amount'])
        user = authenticate(request, username=username, password=password)
        if user is None:
            raise ValueError
        auth_login(request=request, user=user)
    except:
        return render(request, 'cart/pay.html', context={'error': 'Wrong Accound Details or amount'})

    transaction = Transaction.objects.create(made_by=user, amount=amount)
    transaction.save()
    merchant_key = settings.PAYTM_SECRET_KEY

    params = (
        ('MID', settings.PAYTM_MERCHANT_ID),
        ('ORDER_ID', str(transaction.order_id)),
        ('CUST_ID', str(transaction.made_by.email)),
        ('TXN_AMOUNT', str(transaction.amount)),
        ('CHANNEL_ID', settings.PAYTM_CHANNEL_ID),
        ('WEBSITE', settings.PAYTM_WEBSITE),
        # ('EMAIL', request.user.email),
        # ('MOBILE_N0', '9911223388'),
        ('INDUSTRY_TYPE_ID', settings.PAYTM_INDUSTRY_TYPE_ID),
        ('CALLBACK_URL', 'http://127.0.0.1:8000/callback/'),
        # ('PAYMENT_MODE_ONLY', 'NO'),
    )

    paytm_params = dict(params)
    checksum = generate_checksum(paytm_params, merchant_key)

    transaction.checksum = checksum
    transaction.save()

    paytm_params['CHECKSUMHASH'] = checksum
    # print('SENT: ', checksum)
    return render(request, 'cart/redirect.html', context=paytm_params)


#
@csrf_exempt
def callback_old(request):
    if request.method == 'POST':
        received_data = dict(request.POST)
        orderId = received_data['ORDERID'][0]
        transactionInst = Transaction.objects.get(order_id=orderId)
        try:
            transactionInst.pg_MID = received_data['MID'][0]
        except:
            pass
        try:
            transactionInst.pg_txnID = received_data['TXNID'][0]
        except:
            pass
        try:
            transactionInst.pg_txnAmount = received_data['TXNAMOUNT'][0]
        except:
            pass
        try:
            transactionInst.pg_paymentMode = received_data['PAYMENTMODE'][0]
        except:
            pass
        try:
            transactionInst.pg_currency = received_data['CURRENCY'][0]
        except:
            pass
        try:
            transactionInst.pg_txnDate = received_data['TXNDATE'][0]
        except:
            pass
        try:
            transactionInst.pg_status = received_data['STATUS'][0]
        except:
            pass
        try:
            transactionInst.pg_repsonseCode = received_data['RESPCODE'][0]
        except:
            pass
        try:
            transactionInst.pg_responseMsg = received_data['RESPMSG'][0]
        except:
            pass
        try:
            transactionInst.pg_gatewayName = received_data['GATEWAYNAME'][0]
        except:
            pass
        try:
            transactionInst.pg_bankTxnID = received_data['BANKTXNID'][0]
        except:
            pass
        try:
            transactionInst.pg_bankName = received_data['BANKNAME'][0]
        except:
            pass
        try:
            transactionInst.pg_checkSubHash = received_data['CHECKSUMHASH'][0]
        except:
            pass

        transactionInst.save()
        paytm_params = {}
        paytm_checksum = received_data['CHECKSUMHASH'][0]
        for key, value in received_data.items():
            if key == 'CHECKSUMHASH':
                paytm_checksum = value[0]
            else:
                paytm_params[key] = str(value[0])
        # Verify checksum
        if transactionInst.selected_stock.get_funds_in == 'Planify Capital':
            secret_key = settings.PAYTM_SECRET_KEY_CAPITAL
        else:
            secret_key = settings.PAYTM_SECRET_KEY_ENTERPRISE
        is_valid_checksum = verify_checksum(paytm_params, secret_key, str(paytm_checksum))
        if is_valid_checksum:
            received_data['message'] = "Checksum Matched"
        else:
            received_data['message'] = "Checksum Mismatched"
            return render(request, 'cart/callback.html', context=received_data)
        return render(request, 'cart/callback.html', context=received_data)


class CartDetailsView(APIView):

    def get(self, request):
        resp = CartService(user=request.user).get_cart_details()
        status_code = status.HTTP_200_OK
        if resp.get('status') is False:
            status_code = status.HTTP_400_BAD_REQUEST
        return Response(resp, status=status_code)

    def delete(self, request):
        resp = CartService(user=request.user).clear_cart()
        status_code = status.HTTP_200_OK
        if resp.get('status') is False:
            status_code = status.HTTP_400_BAD_REQUEST
        return Response(resp, status=status_code)


def cart_detail_view(request):
    resp = {}
    if request.method == 'GET':
        resp = CartService(user=request.user).get_cart_details()
    elif request.method == 'DELETE':
        resp = CartService(user=request.user).clear_cart()
    status_code = status.HTTP_200_OK
    if resp.get('status') is False:
        status_code = status.HTTP_400_BAD_REQUEST
    return JsonResponse(resp, status=status_code)


class CartItemView(APIView):

    def put(self, request, uid):
        data = request.data
        validate = ItemUpdateSerializer(data=data)
        if validate.is_valid():
            resp = CartService(user=request.user).update_item(uid, data=data)
        else:
            resp = {'status': False, "message": str(list(validate.errors.values())[0][0])}
        status_code = status.HTTP_200_OK
        if resp.get('status') is False:
            status_code = status.HTTP_400_BAD_REQUEST
        return Response(resp, status=status_code)

    def delete(self, request, uid):
        resp = CartService(user=request.user).delete_item(uid)
        status_code = status.HTTP_200_OK
        if resp.get('status') is False:
            status_code = status.HTTP_400_BAD_REQUEST
        return Response(resp, status=status_code)


def cart_items_view(request, uid):
    resp = {}
    if request.method == 'PUT':
        data = request.data
        validate = ItemUpdateSerializer(data=data)
        if validate.is_valid():
            resp = CartService(user=request.user).update_item(uid, data=data)
        else:
            resp = {'status': False, "message": str(list(validate.errors.values())[0][0])}
    elif request.method == 'DELETE':
        resp = CartService(user=request.user).delete_item(uid)
    status_code = status.HTTP_200_OK
    if resp.get('status') is False:
        status_code = status.HTTP_400_BAD_REQUEST
    return JsonResponse(resp, status=status_code)


class CartAddItemView(APIView):
    def post(self, request):
        data = request.data
        validate = ItemAddSerializer(data=data)
        if validate.is_valid():
            resp = CartService(user=request.user).add_item(data)
        else:
            resp = {'status': False, "message": str(list(validate.errors.values())[0][0])}
        status_code = status.HTTP_200_OK
        if resp.get('status') is False:
            status_code = status.HTTP_400_BAD_REQUEST
        return Response(resp, status=status_code)


def cart_add_item_view(request):
    resp = {}
    if request.method == 'POST':
        data = request.data
        validate = ItemAddSerializer(data=data)
        if validate.is_valid():
            resp = CartService(user=request.user).add_item(data)
        else:
            resp = {'status': False, "message": str(list(validate.errors.values())[0][0])}
    status_code = status.HTTP_200_OK
    if resp.get('status') is False:
        status_code = status.HTTP_400_BAD_REQUEST
    return JsonResponse(resp, status=status_code)

class TradebookGetAPIview(APIView):

	def get(self, request):
		resp = TransactionServices(user=request.user).get_tradebook_details()
		status_code = status.HTTP_200_OK
		if resp.get('status') is False:
			status_code = status.HTTP_400_BAD_REQUEST
		return Response(resp, status=status_code)

# below is the temp code..
# ....................................

# ....................................
class sampleInvoiceView(APIView):

	def get(self, request):
		resp = TransactionServices(user=request.user).tempInvoice()
		status_code = status.HTTP_200_OK
		if resp.get('status') is False:
			status_code = status.HTTP_400_BAD_REQUEST
		return Response(resp, status=status_code)

class InvoiceGenerationView(APIView):

    def get(self, request):
        data = request.data
        resp = TransactionServices(user=request.user).fetch_tran_invoice(data)
        status_code = status.HTTP_200_OK
        if resp.get('status') is False:
            status_code = status.HTTP_400_BAD_REQUEST
        return Response(resp, status=status_code)

