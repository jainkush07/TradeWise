from django.shortcuts import render, get_object_or_404, redirect, HttpResponse, reverse
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib import messages
from authApp.serializers import UserSerializer
from employeeApp.models import city, state, country
from .forms import *
from .models import *
from authApp.models import userRoles
from cartApp.models import Transaction
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Q
from whatsappAuthApp.models import whatsappLeads
import datetime
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from authApp.models import userRoles, roles
from authApp.views import checkUserAndProfiles, checkUserAndProfilesSec
from whatsappAuthApp.models import whatsappLeads
from cartApp.models import Transaction
from stockApp.models import stockEventsDividend, stockEssentials
from websiteApp.models import buyPreIPOStockList
from django.contrib.auth.decorators import login_required
from decimal import Decimal
from datetime import date, datetime
from dateutil.relativedelta import relativedelta
import dateutil, datetime, pytz
from calendar import isleap
from authNewApp.views import check_email_whatsapp_verification_status, otp_authentication
from django.conf import settings
from django.core.paginator import Paginator
from rest_framework.decorators import api_view
from .serializers import *
from rest_framework.response import Response
from investorApp.services.kyc.kyc_orchestrator import KycOrchestrator
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response


#

def shareBookStatusDetailsSubmitView(request):
    if request.method == 'POST':
        methodType = request.POST.get('submitType')
        redirectTo = request.POST.get('requestFrom')
        userInst = request.POST.get('profileOwner')
        stockInst = request.POST.get('selected_stock')
        getAmount = request.POST.get('amount')
        investor = request.POST.get('investor')
        doc = request.POST.get('transacion_doc')
        fileMethodType = request.POST.get('fileSubmitType')
        userInst = User.objects.get(username=investor)
        # print(f'this is docuemt uploaded by --- {doc}')
        if methodType == 'new':
            objlnst = None
        else:
            pkID = request.POST.get('dataID')
            objlnst = get_object_or_404(Transaction, pk=pkID)

        if fileMethodType == 'new':
            docObjInst = None
        else:
            pkIDForDoc = request.POST.get('docDataID')
            docObjInst = get_object_or_404(transactionDocs, pk=pkIDForDoc)
        objForm = shareBookStatusDetailsForm(request.POST, instance=objlnst)
        transactionDocumentForm = transactionDocsForm(request.POST, request.FILES, instance=docObjInst)

        if objForm.is_valid():
            cd = objForm.save(commit=False)
            cd.made_by = userInst
            cd.author = request.user
            cd.save()
            cd.refresh_from_db()
            objForm.save_m2m()

            if doc and transactionDocumentForm.is_valid():
                cd2 = transactionDocumentForm.save(commit=False)
                cd2.transacion_doc = doc
                cd2.related_transaction = objlnst
                cd2.author = request.user
                cd2.save()
                cd2.refresh_from_db()
                transactionDocumentForm.save_m2m()
            messages.success(request, 'Details Updated Successfully')
        else:
            messages.error(request, objForm.errors)
        return redirect('investorApp:sharebookUrl')
    return HttpResponse('Invalid Entry')


#### share book transactions submit view ######
def shareBookTransactionSubmitView(request):
    if request.method == 'POST':
        methodType = request.POST.get('submitType')
        redirectTo = request.POST.get('requestFrom')
        userInst = request.POST.get('profileOwner')
        stockInst = request.POST.get('selected_stock')
        getAmount = request.POST.get('amount')
        investor = request.POST.get('investor')
        doc = request.POST.get('transacion_doc')
        fileMethodType = request.POST.get('fileSubmitType')
        userInst = User.objects.get(username=investor)
        # print(f'this doc is uploaded bysdfsdf --- {doc}')
        if methodType == 'new':
            objlnst = None
        else:
            pkID = request.POST.get('dataID')
            objlnst = get_object_or_404(Transaction, pk=pkID)
        if fileMethodType == 'new':
            docObjInst = None
        else:
            pkIDForDoc = request.POST.get('docDataID')
            docObjInst = get_object_or_404(transactionDocs, pk=pkIDForDoc)
        objForm = shareBookTransactionsListForm(request.POST, instance=objlnst)
        transactionDocumentForm = transactionDocsForm(request.POST, request.FILES, instance=docObjInst)
        if objForm.is_valid():
            cd = objForm.save(commit=False)
            cd.made_by = userInst
            cd.author = request.user
            cd.save()
            cd.refresh_from_db()
            objForm.save_m2m()
            if doc and transactionDocumentForm.is_valid():
                cd2 = transactionDocumentForm.save(commit=False)
                cd2.transacion_doc = doc
                cd2.related_transaction = objlnst
                cd2.author = request.user
                cd2.save()
                cd2.refresh_from_db()
                transactionDocumentForm.save_m2m()
                messages.success(request, 'Details Updated Successfully')
            messages.success(request, 'Details Updated Successfully')
        else:
            messages.error(request, objForm.errors)
        return redirect('investorApp:sharebookUrl')
    return HttpResponse('Invalid Entry')


def investorPortfolioSubmitView(request):
    if request.method == 'POST':
        methodType = request.POST.get('submitType')
        redirectTo = request.POST.get('requestFrom')

        userInst = request.POST.get('profileOwner')
        stockInst = request.POST.get('selected_stock')
        getAmount = request.POST.get('amount')

        # stockBasicDetailInst = stockBasicDetail.objects.get(pk=stockInst)

        # Transaction.objects.create(selected_stock=stockBasicDetailInst)

        if methodType == 'new':
            objlnst = None
        else:
            pkID = request.POST.get('dataID')

            objlnst = get_object_or_404(Transaction, pk=pkID)
        objForm = investorPortfolioForm(request.POST, instance=objlnst)

        if objForm.is_valid():
            # print("running")
            cd = objForm.save(commit=False)
            cd.profileOwner = request.user
            cd.author = request.user
            cd.made_by = request.user
            cd.amount = getAmount
            # cd.made_by=request.user.id
            cd.save()
            cd.refresh_from_db()
            objForm.save_m2m()
            messages.success(request, 'Details Updated Successfully')
        else:
            messages.error(request, objForm.errors)
        return redirect(redirectTo)
    return HttpResponse('Invalid Entry')


def childInvestorPersonalDetailSubmitView(request):
    if request.method == 'POST':
        methodType = request.POST.get('submitType')
        redirectTo = request.POST.get('requestFrom')
        redirectSuccess = request.POST.get('redirecting')
        if methodType == 'new':
            objlnst = None
        else:
            pkID = request.POST.get('dataID')
            objlnst = get_object_or_404(tempUser, pk=pkID)
        objForm = tempUserForm(request.POST, instance=objlnst)
        if objForm.is_valid():
            cd = objForm.save(commit=False)
            cd.parentProfileOwner = request.user
            cd.author = request.user
            cd.profileOwner = request.user
            cd.save()
            cd.refresh_from_db()
            objForm.save_m2m()
            messages.success(request, 'Details Updated Successfully')
        else:
            messages.error(request, 'Please check an error occured!')
        return redirect(redirectTo)
    return HttpResponse('Invalid Entry')

@api_view(["POST"])
def childInvestorPersonalDetailSubmitViewAPI(request):
    if request.method == 'POST':
        methodType = request.data.get('submitType')
        redirectTo = request.get_full_path
        redirectSuccess = request.data.get('redirecting')
        if methodType == 'new':
            objlnst = None
        else:
            pkID = request.data.get('dataID')
            objlnst = get_object_or_404(tempUser, pk=pkID)
        objForm = tempUserForm(request.data, instance=objlnst)
        if objForm.is_valid():
            cd = objForm.save(commit=False)
            cd.parentProfileOwner = request.user
            cd.author = request.user
            cd.profileOwner = request.user
            cd.save()
            cd.refresh_from_db()
            objForm.save_m2m()
            messages.success(request, 'Details Updated Successfully')
            return Response({'status': True})
        else:
            messages.error(request, 'Please check an error occured!')
            return Response({'status': False})
        #return redirect(redirectTo)
        
    return HttpResponse('Invalid Entry')


@api_view(["POST"])
def childInvestorPersonalDetailSubmitViewAPI(request):
    if request.method == 'POST':
        methodType = request.data.get('submitType')
        redirectTo = request.get_full_path
        redirectSuccess = request.data.get('redirecting')
        if methodType == 'new':
            objlnst = None
        else:
            pkID = request.data.get('dataID')
            objlnst = get_object_or_404(tempUser, pk=pkID)
        objForm = tempUserForm(request.data, instance=objlnst)
        if objForm.is_valid():
            cd = objForm.save(commit=False)
            cd.parentProfileOwner = request.user
            cd.author = request.user
            cd.profileOwner = request.user
            cd.save()
            cd.refresh_from_db()
            objForm.save_m2m()
            messages.success(request, 'Details Updated Successfully')
            return Response({'status': True})
        else:
            messages.error(request, 'Please check an error occured!')
            return Response({'status': False})
        #return redirect(redirectTo)
        
    return HttpResponse('Invalid Entry')


def childInvestorTempTransactionView(request):
    if request.method == 'POST':
        # print("running temp transactions view")
        methodType = request.POST.get('submitType')
        redirectTo = request.POST.get('requestFrom')
        redirectSuccess = request.POST.get('redirecting')
        tempUserInst = request.POST.get('made_by')
        if methodType == 'new':
            objlnst = None
        # print("new")
        else:
            pkID = request.POST.get('tempDataID')
            print(f'this is pk id --- {pkID}')
            objlnst = get_object_or_404(tempTransaction, pk=pkID)
        objForm = tempTransactionForm(request.POST, instance=objlnst)
        # print(objForm)
        if objForm.is_valid():
            # print('this is runnig valid')
            cd = objForm.save(commit=False)
            # cd.parentProfileOwner = request.user
            cd.author = request.user
            # cd.made_by=tempUserInst
            cd.save()
            cd.refresh_from_db()
            objForm.save_m2m()
            messages.success(request, 'Details Updated Successfully')
        else:
            messages.error(request, 'Please check an error occured!')
        return redirect(redirectTo)
    return HttpResponse('Invalid Entry')

@api_view(['POST'])
def childInvestorTempTransactionViewAPI(request):
    if request.method == 'POST':
        # print("running temp transactions view")
        methodType = request.data.get('submitType')
        # redirectTo = request.POST.get_full_path
        redirectSuccess = request.data.get('redirecting')
        name = request.data.get('name')
        userInstID = request.data.get('userInstID')
        tempUserInst = request.data.get('made_by')
        userInst = User.objects.get(id=userInstID)
        if name == userInst.profileOwnerIPD.name:
            if methodType == 'new':

                objlnst = None
            else:
                pkID = request.data.get('tempDataID')
                objlnst = get_object_or_404(Transaction, pk=pkID)
            objForm = investorPortfolioForm(request.data, instance=objlnst)

            if objForm.is_valid():
                # print("running")
                cd = objForm.save(commit=False)
                cd.profileOwner = request.user
                cd.author = request.user
                cd.made_by = request.user
                #cd.amount = getAmount
                #cd.made_by=request.user.id
                cd.save()
                cd.refresh_from_db()
                objForm.save_m2m()
                messages.success(request, 'Details Updated Successfully')
                return Response({'status': True})
            else:
                return Response({"status": False, 'message': objForm.errors})
        # print("user found")
        # print("user : ", user)
        else:
            # print("enter if block")
            if methodType == 'new':
                    #print("getting if")
                objlnst = None
                # print("new")
            else:
                    #print("getting else")
                pkID = request.data.get('tempDataID')
                # print(f'this is pk id --- {pkID}')
                objlnst = get_object_or_404(tempTransaction, pk=pkID)
            objForm = tempTransactionForm(request.data, instance=objlnst)
                # print(objForm)
            if objForm.is_valid():
                    # print('this is runnig valid')
                cd = objForm.save(commit=False)
                    # cd.parentProfileOwner = request.user
                cd.author = request.user
                    # cd.made_by=tempUserInst
                cd.save()
                cd.refresh_from_db()
                objForm.save_m2m()
                messages.success(request, 'Details Updated Successfully')
                return Response({'status': True})
            else:
                messages.error(request, 'Please check an error occured!')
                return Response({"status": False, 'message': objForm.errors})
                # return redirect(redirectTo)
    return HttpResponse('Invalid Entry')

def slugBasedInvestorSourceSubmitView(request):
    if request.method == 'POST':
        methodType = request.POST.get('submitType')
        redirectTo = request.POST.get('requestFrom')
        redirectSuccess = request.POST.get('redirecting')
        PersonalInst = request.POST.get('peraonalInstance')
        if methodType == 'new':
            objlnst = None
        else:
            pkID = request.POST.get('dataID')
            objlnst = get_object_or_404(investorSourceDetails, pk=pkID)
        objForm = investorSourceDetailsForm(request.POST, instance=objlnst)
        if objForm.is_valid():
            cd = objForm.save(commit=False)
            # cd.profileOwner = request.user
            # cd.author=request.user
            cd.save()
            cd.refresh_from_db()
            objForm.save_m2m()
            messages.success(request, 'Source Details Updated Successfully')
        else:
            messages.error(request, 'Please check an error occured!')
        return redirect(redirectTo)
    return HttpResponse('Invalid Entry')


#
def createInvestorView(request):
    if request.method == 'POST':
        getEmail = request.POST.get('email')
        getPhoneNumber = request.POST.get('phoneNumber')
        # getPassword = request.POST.get('password')
        loginType = request.POST.get('loginType')
        redirectTo = request.POST.get('requestFrom')
        countryCode = request.POST.get('countryCode')

        # userList = User.objects.all()
        # if getEmail not in userList:
        userProfile = checkUserAndProfiles(getEmail)

        user = None

        if not userProfile:
            user = User.objects.create(
                username=getPhoneNumber,
                email=getEmail,
                is_active=False
            )
            user.set_unusable_password()
            user.save()

            try:
                createInvestorPersonalDetails = investorPersonalDetails(profileOwner=user)
                createInvestorPersonalDetails.save()
            except:
                pass

            try:
                createVerificationStatus = verificationStatus(profileOwner=user)
                createVerificationStatus.save()
            except:
                pass

            try:
                createWhatsappLeads = whatsappLeads(profileOwner=user)
                createWhatsappLeads.save()
            except:
                pass

            try:
                createWhatsappLeadsInst = whatsappLeads.objects.get(profileOwner=user)
            except:
                createWhatsappLeadsInst = None

            createWhatsappLeadsInst.phoneNumber = user.username
            createWhatsappLeadsInst.countryCode = countryCode
            createWhatsappLeadsInst.save()
            try:
                roleForUser = roles.objects.get(name=loginType)
            except:
                roleForUser = None
            roleOfUser = userRoles(profile_owner=user)
            roleOfUser.save()
            roleOfUser.profile_roles.add(roleForUser)
            try:
                objInst = investorPersonalDetails.objects.get(profileOwner=user)
            except:
                objInst = None
            objInst.mobileNumber = user.username
            objInst.save()

            messages.success(request, 'Investor Added Successfully')

        else:
            messages.error(request, 'This email is already exists')
        return redirect(redirectTo)
    return HttpResponse('Invalid Entry Point!')


#
def apply_mods_view(request):
    tried = 0
    triedSuccess = 0
    failed = 0
    try:
        tried += 1
        objInsts = investorPersonalDetails.objects.all()
        for item in objInsts:
            if item.profileOwner:
                item.mobileNumber = item.profileOwner.username
                item.save()
        triedSuccess += 1
    except:
        failed += 1
    return HttpResponse(f'tried: {tried} | triedSuccess: {triedSuccess} | failed: {failed} | failed: {failed}')


def getAllMobile():
    personalInst = investorPersonalDetails.objects.all()

    for item in personalInst:
        try:
            whatsappLeadsInst = whatsappLeads.objects.get(profileOwner=item.profileOwner)
            item.mobileNumber = whatsappLeadsInst.phoneNumber
        except:
            pass
        item.save()


#### new combined view

def personalVerificationStatusView(request):
    if request.method == 'POST':
        methodType = request.POST.get('submitType')
        redirectTo = request.POST.get('requestFrom')
        submitDetailType = request.POST.get('detailType')
        profileOwner = request.POST.get('profileOwner')
        pkID = request.POST.get('dataID')
        if submitDetailType == 'personal':
            if methodType == 'new':
                objlnst = None
            else:
                objlnst = get_object_or_404(verificationStatus, profileOwner=profileOwner)
            objForm = personalVerificationStatusForm(request.POST, request.FILES, instance=objlnst)
            if objForm.is_valid():
                cd = objForm.save(commit=False)
                cd.save()
                cd.refresh_from_db()
                messages.success(request, 'Personal Data sent for verification')
            else:
                messages.error(request, objForm.errors)
            return redirect(redirectTo)

    return HttpResponse('Invalid Entry')


#####


def getBankStatusCheckView(request):
    if request.method == 'POST':
        methodType = request.POST.get('submitType')
        redirectTo = request.POST.get('requestFrom')
        pkID = request.POST.get('dataID')
        if methodType == 'new':
            objlnst = None
        else:
            objlnst = get_object_or_404(investorBankDetails, pk=pkID)
        objForm = investorBankVerifyStausForm(request.POST, instance=objlnst)
        if objForm.is_valid():
            cd = objForm.save(commit=False)
            cd.save()
            cd.refresh_from_db()
            messages.success(request, 'Data sent for verification')
        else:
            messages.error(request, objForm.errors)
        return redirect(redirectTo)
    # investorUser = User.objects.all()
    # for item in investorUser:
    # 	alreadyObj = 0
    # 	createdObjs = 0
    # 	try:
    # 		cd = verificationStatus(profileOwner=item)
    # 		cd.save()
    # 		createdObjs += 1
    # 	except:
    # 		alreadyObj += 1
    # return HttpResponse(f'Success Created: {createdObjs} || already present: {alreadyObj}')
    return HttpResponse('Invalid Entry')


def getDmatStatusCheckView(request):
    if request.method == 'POST':
        methodType = request.POST.get('submitType')
        redirectTo = request.POST.get('requestFrom')
        pkID = request.POST.get('dataID')
        if methodType == 'new':
            objlnst = None
        else:
            objlnst = get_object_or_404(investorDMATDetails, pk=pkID)
        objForm = investorDmatVerifyStausForm(request.POST, request.FILES, instance=objlnst)
        if objForm.is_valid():
            cd = objForm.save(commit=False)
            cd.save()
            cd.refresh_from_db()
            messages.success(request, 'Data sent for verification')
        else:
            messages.error(request, objForm.errors)
        return redirect(redirectTo)
    return HttpResponse('Invalid Entry')


#
def getProfileCounterView(instProfilOwner):
    field_weight = 100 / 17.9
    total_weight = 0.0
    try:
        objInst = investorDMATDetails.objects.filter(profileOwner=instProfilOwner).count()
    except:
        objInst = 0
    if objInst > 0:
        total_weight += field_weight
    try:
        objInst = investorBankDetails.objects.filter(profileOwner=instProfilOwner).count()
    except:
        objInst = 0
    if objInst > 0:
        total_weight += field_weight
    try:
        objInst = investmentDetails.objects.get(profileOwner=instProfilOwner)
        if objInst.presentPortfolio != None:
            total_weight += field_weight
        if objInst.secondaryMarket != None:
            total_weight += field_weight
        if objInst.primaryMarket != None:
            total_weight += field_weight
        if objInst.lookingToInvest != None:
            total_weight += field_weight
        if objInst.secondaryMarket != None:
            total_weight += field_weight
        if objInst.investPorfolio != None:
            total_weight += field_weight
    except:
        objInst = None
    try:
        objInst = investorPersonalDetails.objects.get(profileOwner=instProfilOwner)
        if objInst.name:
            total_weight += field_weight
        if objInst.gender != None:
            total_weight += field_weight
        if objInst.panNumber != None:
            total_weight += field_weight
        if objInst.aadharNumber != None:
            total_weight += field_weight
        if objInst.uploadAadhar != None:
            total_weight += field_weight
        if objInst.address != None:
            total_weight += field_weight
        if objInst.city != None:
            total_weight += field_weight
        if objInst.pinCode != None:
            total_weight += field_weight
        if objInst.country != None:
            total_weight += field_weight
        if objInst.uploadPan != None:
            total_weight += field_weight
    except:
        objInst = None

    roundTotal = int(total_weight)
    return roundTotal


#
def getUserProfile(user, profileRequest):
    userInst = get_object_or_404(User, username=user)
    if profileRequest == 'personal':
        profile = investorPersonalDetails.objects.get(profileOwner=userInst)
    elif profileRequest == 'investment':
        profile = investmentDetails.objects.get(profileOwner=userInst)
    elif profileRequest == 'bank':
        profile = bankForSlug.objects.get(profileOwner=userInst)
    elif profileRequest == 'dmat':
        profile = dematForSlug.objects.get(profileOwner=userInst)
    return profile


#
def getConnectedUsers(user, requestFor):
    connectedProfile = connectedInvestors.objects.filter(user=user)
    userList = []
    for item in connectedProfile:
        connectedUser = getUserProfile(item, requestFor)
        userList.append(connectedUser)
    return userList


# def totalCalculatedProgress(request):
# 	if request.user.is_authenticated:
# 		investorBankInsts = investorBankDetails.objects.filter(profileOwner=request.user.pk).order_by('-is_default','bankName')
# 		try:
# 			inst = get_object_or_404(User, pk=request.user.pk)
# 			investorPersonalInst = get_object_or_404(investorPersonalDetails, profileOwner=inst)
# 			investmentInst = get_object_or_404(investmentDetails, profileOwner=inst)
# 			objInst1 = investorPersonalDetails.objects.get(profileOwner=inst)
# 			objInst2 = investmentDetails.objects.get(profileOwner=inst)

# 		except:
# 			investorPersonalInst = None
# 			investmentInst = None
# 			objInst1 = None
# 			objInst2 = None
# 		objInst3 = investorBankDetails.objects.filter(profileOwner=inst).count()
# 		objInst4 = investorDMATDetails.objects.filter(profileOwner=inst).count()
# 	calculatedProgress = 0
# 	if objInst1 :
# 		calculatedProgress = objInst1.totalProgress
# 		if objInst2:
# 			calculatedProgress += objInst2.totalProgress
# 			if objInst3:
# 				calculatedProgress += 1
# 				if objInst4:
# 					calculatedProgress += 1

# 	return calculatedProgress

#

def deleteFKdataView(request):
    if request.method == 'POST':
        deletePK = request.POST.get('deleteDataID')
        print(f'this is delete pk {deletePK}')
        deleteFrom = request.POST.get('deleteFlag')
        requestedPage = request.POST.get('redirectTo')
        if deleteFrom == 'investorBankDetails':
            try:
                objInst = investorBankDetails.objects.get(pk=deletePK)
                objInst.delete()
                messages.success(request, 'Data Deleted')
            except:
                messages.error(request, "error occured")
        elif deleteFrom == 'investorDMATDetails':
            try:
                objInst = investorDMATDetails.objects.get(pk=deletePK)
                objInst.delete()
                messages.success(request, 'Data Deleted')
            except:
                messages.error(request, "error occured")
        elif deleteFrom == 'Transaction':
            print('transaction running')
            try:
                objInst = Transaction.objects.get(pk=deletePK)
                objInst.delete()
                messages.success(request, 'Data Deleted')
            except:
                messages.error(request, "error occured")

        elif deleteFrom == 'tempUser':
            print("temp user view runnign")
            try:
                objInst = tempUser.objects.get(pk=deletePK)
                objInst.delete()
                messages.success(request, 'Data Deleted')
            except:
                messages.error(request, "error occured")

        elif deleteFrom == 'tempTransaction':
            print('temp transaction running ')
            # try:
            objInst = tempTransaction.objects.get(pk=deletePK)
            objInst.delete()
            messages.success(request, 'Data Deleted')
        # except:
        # 	messages.error(request,"error occured")

        return redirect(requestedPage)
    return HttpResponse('Invalid Entry Point')


@api_view(["POST"])
def deleteFKdataViewAPI(request):
    if request.method == 'POST':
        deletePK = request.data.get('deleteDataID')
        name = request.data.get('name')
        userInstID = request.data.get('userInstID')
        print(f'this is delete pk {deletePK}')
        deleteFrom = request.data.get('deleteFlag')
        #requestedPage = request.POST.get('redirectTo')
        if deleteFrom == 'investorBankDetails':
            try:
                objInst = investorBankDetails.objects.get(pk=deletePK)
                objInst.delete()
                messages.success(request, 'Data Deleted')
            except:
                messages.error(request, "error occured")
        elif deleteFrom == 'investorDMATDetails':
            try:
                objInst = investorDMATDetails.objects.get(pk=deletePK)
                objInst.delete()
                messages.success(request, 'Data Deleted')
            except:
                messages.error(request, "error occured")
        elif deleteFrom == 'Transaction':
            print('transaction running')
            try:
                objInst = Transaction.objects.get(pk=deletePK)
                objInst.delete()
                messages.success(request, 'Data Deleted')
            except:
                messages.error(request, "error occured")

        elif deleteFrom == 'tempUser':
            print("temp user view runnign")
            try:
                objInst = tempUser.objects.get(pk=deletePK)
                objInst.delete()
                messages.success(request, 'Data Deleted')
            except:
                messages.error(request, "error occured")

        elif deleteFrom == 'tempTransaction':
            userInst = User.objects.get(id=userInstID)
            if name == userInst.profileOwnerIPD.name:
                try:
                    objInst = Transaction.objects.get(pk=deletePK)
                    objInst.delete()
                    messages.success(request, 'Data Deleted')
                except:
                    messages.error(request, "error occured")
            else:
            #print('temp transaction running ')
                try:
                    objInst = tempTransaction.objects.get(pk=deletePK)
                    objInst.delete()
                    messages.success(request, 'Data Deleted')
                except:
                    messages.error(request,"error occured")
        else:
            return Response({'status': False})
        return Response({'status': True})
    return HttpResponse('Invalid Entry Point')


#
def personalDetailView(request):
    pageFlag = {}
    global profileCounter
    profileCounter = 0.0
    if request.user.is_authenticated:
        loggedInUserInst = User.objects.get(pk=request.user.pk)
        whatsappVerified, emailVerified, passAvailable, loginPinAvailable = check_email_whatsapp_verification_status(
            loggedInUserInst)
        request.session['loginType'] = 'INVESTOR'
        if not whatsappVerified or not emailVerified or not passAvailable or not loginPinAvailable:
            if whatsappVerified and not emailVerified:
                return redirect(settings.UPDATE_EMAIL_TO_ACCOUNT_URL)
            elif emailVerified and not whatsappVerified:
                return redirect(settings.UPDATE_WHATSAPP_TO_ACCOUNT_URL)
            elif whatsappVerified and emailVerified and not passAvailable:
                return redirect(settings.CHANGE_PASSWORD_URL)
            elif whatsappVerified and emailVerified and not loginPinAvailable:
                return redirect(settings.LOGIN_PIN_URL)

        # whatsappLeadsInst = whatsappLeads.objects.filter(profileOwner=loggedInUserInst).exists()
        # if whatsappLeadsInst:
        # 	try:
        # 		if not request.user.profileOwnerWL.verified:
        # 			messages.warning(request, 'Whatsapp Number Verification Pending.')
        # 			request.session['loginType'] = 'INVESTOR'
        # 			return redirect('whatsappAuthApp:getVerifiedUrl')
        # 	except:
        # 		pass
        # else:
        # 	messages.warning(request, 'Whatsapp Number Verification Pending.')
        # 	request.session['loginType'] = 'INVESTOR'
        # 	return redirect('whatsappAuthApp:getVerifiedUrl')

        try:
            inst = User.objects.get(pk=request.user.pk)
            otpInst = otp_authentication.objects.get(userProfile=inst)
            # print(otpInst.country_code)
            if inst:
                profileCounter = getProfileCounterView(inst)
        except:
            inst = None
        try:
            investorPersonalInst = get_object_or_404(investorPersonalDetails, profileOwner=inst)
        except:
            investorPersonalInst = None

        try:
            verificationStatusInst = verificationStatus.get_object_or_404(profileOwner=inst)
        except:
            verificationStatusInst = None

    else:
        inst = None
        investorPersonalInst = None

    if not request.user.is_authenticated:
        return redirect('authApp:loginUsernameHandlerUrl')
    elif request.user.is_authenticated:
        inverstorProfile = False
        try:
            userRoleObj = userRoles.objects.get(profile_owner=inst)
            for item in userRoleObj.profile_roles.all():
                if 'INVESTOR' == item.name:
                    inverstorProfile = True
        except:
            userRoleObj = None
        if not inverstorProfile:
            logout(request)
            return redirect('authApp:loginUsernameHandlerUrl')

    try:
        userList = getConnectedUsers(request.user, requestFor='personal')
    except:
        userList = None
    pageFlag['Main'] = 'Personal'
    cities = city.objects.all()
    states = state.objects.all()
    countryInst = country.objects.all()
    try:
        investorPersonalInstName = get_object_or_404(investorPersonalDetails, profileOwner=request.user.pk)
    except:
        investorPersonalInstName = None

    context = {
        'inst': inst,
        'otpInst': otpInst,
        'profileCounter': profileCounter,
        'pageFlag': pageFlag,
        'userList': userList,
        'investorPersonalInst': investorPersonalInst,
        'investorPersonalInstName': investorPersonalInstName,
        'cities': cities,
        'states': states,
        'countryInst': countryInst,
        'countryInst': countryInst,
        'verificationStatusInst': verificationStatusInst,
        # 'calculatedProgress':calculatedProgress,

    }
    return render(request, 'investor/personalDetail.html', context)


#
def slugBasedPersonalDetailView(request, slug):
    pageFlag = {}
    action = 'Personal'
    profileCounter = 0.0
    otpInst = None
    if request.user.is_authenticated:
        try:
            # print(slug)
            PersonalInst = investorPersonalDetails.objects.get(profileOwner__username=slug)
        # print(PersonalInst)
        except:
            PersonalInst = None

        investorPersonalInst = get_object_or_404(investorPersonalDetails, profileOwner=PersonalInst.profileOwner)
        # print(investorPersonalInst)

        try:
            otpInst = otp_authentication.objects.get(userProfile=PersonalInst.profileOwner.pk)
        except:
            otpInst = None

        try:
            createInvestorInvestmentDetails = investmentDetails(profileOwner=PersonalInst.profileOwner)
        except:
            pass

    try:
        profileCounter = getProfileCounterView(PersonalInst.profileOwner.pk)
    except:
        profileCounter = None

    verificationSelectForm = investorAdharVerificationForm()

    try:
        verificationStatusInst = verificationStatus.objects.get(profileOwner=PersonalInst.profileOwner)
    except:
        verificationStatusInst = None

    try:
        userList = getConnectedUsers(request.user, requestFor='personal')
    except:
        userList = None

    investorPersonalInstName = get_object_or_404(investorPersonalDetails, profileOwner__username=slug)
    cities = city.objects.all()
    states = state.objects.all()
    countryInst = country.objects.all()
    context = {
        'pageFlag': pageFlag,
        'PersonalInst': PersonalInst,
        'action': action,
        'userList': userList,
        'investorPersonalInst': investorPersonalInst,
        'investorPersonalInstName': investorPersonalInstName,
        'cities': cities,
        'states': states,
        'countryInst': countryInst,
        'profileCounter': profileCounter,
        'verificationSelectForm': verificationSelectForm,
        'verificationStatusInst': verificationStatusInst,
        'otpInst': otpInst,
    }
    return render(request, 'investor/personalDetail.html', context)


#
def investmentView(request):
    pageFlag = {}
    lookingToInvest = lookingToInvestDetails.objects.filter(status='published')
    if request.user.is_authenticated:
        # investorBankInsts = investorBankDetails.objects.filter(profileOwner=request.user.pk).order_by('-is_default','bankName')
        try:
            inst = get_object_or_404(User, pk=request.user.pk)
            investmentInst = get_object_or_404(investmentDetails, profileOwner=inst)
        except:
            investmentInst = None
    else:
        inst = None
        investmentInst = None

    if not request.user.is_authenticated:
        return redirect('authApp:loginUsernameHandlerUrl')
    elif request.user.is_authenticated:
        inverstorProfile = False
        try:
            userRoleObj = userRoles.objects.get(profile_owner=inst)
            for item in userRoleObj.profile_roles.all():
                if 'INVESTOR' == item.name:
                    inverstorProfile = True
        except:
            userRoleObj = None

    if not inverstorProfile:
        logout(request)
        return redirect('authApp:loginUsernameHandlerUrl')
    investmentForm = investmentDetailsForm(instance=investmentInst)
    try:
        userList = getConnectedUsers(request.user, requestFor='investment')
    except:
        userList = None
    try:
        investorPersonalInstName = get_object_or_404(investorPersonalDetails, profileOwner=request.user.pk)
    except:
        investorPersonalInstName = None
    pageFlag['Main'] = 'Investment'

    if inst:
        profileCounter = getProfileCounterView(inst)

    # calculatedProgress = totalCalculatedProgress(request)
    context = {
        'profileCounter': profileCounter,
        'pageFlag': pageFlag,
        'userList': userList,
        'investorPersonalInstName': investorPersonalInstName,
        'lookingToInvest': lookingToInvest,
        'investmentInst': investmentInst,
        'investmentForm': investmentForm,
        # 'calculatedProgress':calculatedProgress,
    }
    return render(request, 'investor/investmentDetail.html', context)


#
def slugBasedInvestmentView(request, slug):
    pageFlag = {}
    action = 'Investment'
    lookingToInvest = lookingToInvestDetails.objects.filter(status='published')
    profileCounter = 0.0

    PersonalInst = None
    investmentInst = None

    if request.user.is_authenticated:
        # investorBankInsts = investorBankDetails.objects.filter(profileOwner=request.user.pk).order_by('-is_default','bankName')
        try:
            PersonalInst = investorPersonalDetails.objects.get(profileOwner__username=slug)

            investmentInst = get_object_or_404(investmentDetails, profileOwner=PersonalInst)
        except:
            investmentInst = None

    else:
        PersonalInst = None
        investmentInst = None

    try:
        userList = getConnectedUsers(request.user, requestFor='investment')
    except:
        userList = None

    # print(PersonalInst)
    profileCounter = getProfileCounterView(PersonalInst.profileOwner)

    # profileCounter = None
    # pageFlag[personalInst.slug] = 'Investment'
    # investorPersonalInstName = get_object_or_404(investorPersonalDetails, profileOwner=request.user.pk)
    # print(f'this is {investorPersonalInstName}')
    context = {
        'pageFlag': pageFlag,
        'action': action,
        'userList': userList,
        'lookingToInvest': lookingToInvest,
        'investmentInst': investmentInst,
        'profileCounter': profileCounter,
        'PersonalInst': PersonalInst,
        # 'investorPersonalInstName':investorPersonalInstName,
    }
    return render(request, 'investor/investmentDetail.html', context)


#
def bankView(request):
    pageFlag = {}
    if request.user.is_authenticated:
        investorBankInsts = investorBankDetails.objects.filter(profileOwner=request.user.pk).order_by('-is_default',
                                                                                                      'bankName')
        try:
            inst = get_object_or_404(User, pk=request.user.pk)
        # investorPersonalInst = get_object_or_404(investorPersonalDetails, profileOwner=inst)
        # investmentInst = get_object_or_404(investmentDetails, profileOwner=inst)
        except:
            # investorPersonalInst = None
            inst = None
    else:
        inst = None

    if not request.user.is_authenticated:
        return redirect('authApp:loginUsernameHandlerUrl')
    elif request.user.is_authenticated:
        inverstorProfile = False
        try:
            userRoleObj = userRoles.objects.get(profile_owner=inst)
            for item in userRoleObj.profile_roles.all():
                if 'INVESTOR' == item.name:
                    inverstorProfile = True
        except:
            userRoleObj = None
    if not inverstorProfile:
        logout(request)
        return redirect('authApp:loginUsernameHandlerUrl')

    try:
        userList = getConnectedUsers(request.user, requestFor='bank')
    except:
        userList = None
    pageFlag['Main'] = 'Bank'
    try:
        investorPersonalInstName = get_object_or_404(investorPersonalDetails, profileOwner=request.user.pk)
    except:
        investorPersonalInstName = None

    # calculatedProgress = totalCalculatedProgress(request)

    if inst:
        profileCounter = getProfileCounterView(inst)

    context = {
        'profileCounter': profileCounter,
        'pageFlag': pageFlag,
        'userList': userList,
        'investorBankInsts': investorBankInsts,
        'investorPersonalInstName': investorPersonalInstName,
        # 'calculatedProgress':calculatedProgress
        # 'investorPersonalInst':investorPersonalInst,
    }
    return render(request, 'investor/bank.html', context)


#
def slugBasedBankView(request, slug):
    pageFlag = {}
    action = 'Bank'
    profileCounter = 0.0
    bankInst = None
    PersonalInst = None
    if request.user.is_authenticated:
        # try:
        PersonalInst = investorPersonalDetails.objects.get(profileOwner__username=slug)
        # bankForSlugInst = bankForSlug.objects.get(profileOwner=personalInst.profileOwner)
        investorBankInsts = investorBankDetails.objects.filter(profileOwner=PersonalInst.profileOwner.pk).order_by(
            '-is_default', 'bankName')
    # except:
    # bankInst = None
    # PersonalInst = None
    try:
        userList = getConnectedUsers(request.user, requestFor='bank')
    except:
        userList = None

    profileCounter = getProfileCounterView(PersonalInst.profileOwner.pk)

    context = {
        'pageFlag': pageFlag,
        'action': action,
        'userList': userList,
        # 'bankForSlugInst':bankForSlugInst,
        'investorBankInsts': investorBankInsts,
        # 'investorPersonalInstName':investorPersonalInstName,
        'profileCounter': profileCounter,
        'PersonalInst': PersonalInst,

    }
    return render(request, 'investor/bank.html', context)


#
def dmatView(request):
    pageFlag = {}
    stockBrokerInst = stockBrokerDetails.objects.filter(status='published')
    if request.user.is_authenticated:
        investorDMATInsts = investorDMATDetails.objects.filter(profileOwner=request.user.pk).order_by('-is_default',
                                                                                                      'stockBroker')
        try:
            inst = get_object_or_404(User, pk=request.user.pk)
        # investorPersonalInst = get_object_or_404(investorPersonalDetails, profileOwner=inst)
        except:
            # investorPersonalInst = None
            inst = None
    else:
        inst = None

    if not request.user.is_authenticated:
        return redirect('authApp:loginUsernameHandlerUrl')
    elif request.user.is_authenticated:
        inverstorProfile = False
        try:
            userRoleObj = userRoles.objects.get(profile_owner=inst)
            for item in userRoleObj.profile_roles.all():
                if 'INVESTOR' == item.name:
                    inverstorProfile = True
        except:
            userRoleObj = None
    if not inverstorProfile:
        logout(request)
        return redirect('authApp:loginUsernameHandlerUrl')

    try:
        userList = getConnectedUsers(request.user, requestFor='dmat')
    except:
        userList = None
    try:
        investorPersonalInstName = get_object_or_404(investorPersonalDetails, profileOwner=request.user.pk)
    except:
        investorPersonalInstName = None
    pageFlag['Main'] = 'DMAT'

    if inst:
        profileCounter = getProfileCounterView(inst)

    context = {
        'profileCounter': profileCounter,
        'pageFlag': pageFlag,
        'userList': userList,
        'investorDMATInsts': investorDMATInsts,
        'stockBrokerInst': stockBrokerInst,
        'investorPersonalInstName': investorPersonalInstName,
    }
    return render(request, 'investor/dmat.html', context)


#
def slugBasedDmatView(request, slug):
    pageFlag = {}
    action = 'Dmat'
    profileCounter = 0.0
    stockBrokerInst = stockBrokerDetails.objects.filter(status='published')
    if request.user.is_authenticated:
        try:
            PersonalInst = investorPersonalDetails.objects.get(profileOwner__username=slug)
            # dematForSlugInst = dematForSlug.objects.get(profileOwner=PersonalInst.profileOwner)
            investorDMATInsts = investorDMATDetails.objects.filter(profileOwner=PersonalInst.profileOwner)
        except:
            investorDMATInsts = None
            PersonalInst = None
            dematForSlugInst = None
    try:
        userList = getConnectedUsers(request.user, requestFor='dmat')
    except:
        userList = None
    # investorPersonalInstName = get_object_or_404(investorPersonalDetails, profileOwner=request.user.pk)
    # pageFlag[PersonalInst.slug] = 'DMAT'
    profileCounter = getProfileCounterView(PersonalInst.profileOwner.pk)
    context = {
        'pageFlag': pageFlag,
        'action': action,
        'userList': userList,
        # 'dematForSlugInst':dematForSlugInst,
        'investorDMATInsts': investorDMATInsts,
        'stockBrokerInst': stockBrokerInst,
        # 'investorPersonalInstName':investorPersonalInstName,
        'profileCounter': profileCounter,
        'PersonalInst': PersonalInst,
    }
    return render(request, 'investor/dmat.html', context)


# Form Submitted#
def investorPersonalDetailsView(request):
    if request.method == 'POST':
        methodType = request.POST.get('submitType')
        redirectTo = request.POST.get('requestFrom')
        # investorEmail = request.user.email
        redirectSuccess = request.POST.get('redirecting')
        # print(f'this is email id {investorEmail}')
        if methodType == 'new':
            objlnst = None
        else:
            pkID = request.POST.get('dataID')
            # shubham start
            objlnst = get_object_or_404(investorPersonalDetails, id=pkID)  # change model name
        objForm = investorPersonalDetailsForm(request.POST, request.FILES, instance=objlnst)  # change form name
        # shubham ends
        if objForm.is_valid():
            cd = objForm.save(commit=False)
            if methodType == 'new':
                cd.profileOwner = request.user
                cd.author = request.user
            # cd.emailID = investorEmail

            # print(cd.emailID)
            cd.save()
            cd.refresh_from_db()
            messages.success(request, f'Personal Details Updated Successfully')
        # return JsonResponse({'error': False, 'message': 'Updated Successfully'})
        else:
            messages.error(request, 'Please check an error occured!')
        # print(objForm.errors)
        return redirect(redirectTo)
    return HttpResponse('Invalid Entry')


#
def slugBasedPersonalDetailSubmitView(request):
    if request.method == 'POST':
        methodType = request.POST.get('submitType')
        redirectTo = request.POST.get('requestFrom')
        mobileNumber = request.POST.get('mobileNumber')
        # print(f'this is mobile number from personal detail {mobileNumber}')
        # investorEmail = request.user.email
        redirectSuccess = request.POST.get('redirecting')
        # print(f'this is email id {investorEmail}')
        if methodType == 'new':
            objlnst = None
        else:
            pkID = request.POST.get('dataID')
            # shubham start
            objlnst = get_object_or_404(investorPersonalDetails, id=pkID)  # change model name
        objForm = investorPersonalDetailsForm(request.POST, request.FILES, instance=objlnst)  # change form name
        # shubham ends
        # print(objForm)
        if objForm.is_valid():
            cd = objForm.save(commit=False)
            if methodType == 'new':
                cd.profileOwner = request.user
                cd.author = request.user
            # cd.emailID = investorEmail

            # print(cd.emailID)
            cd.save()
            cd.refresh_from_db()
            messages.success(request, f'Personal Details Updated Successfully')
        else:
            messages.error(request, f'Please check an error occured!: {objForm.errors}')
        return redirect(redirectTo)
    return HttpResponse('Invalid Entry')


#
def connectedInvestorsSubmitView(request):
    if request.method == 'POST':
        methodType = request.POST.get('submitType')
        redirectTo = request.POST.get('requestFrom')
        redirectSuccess = request.POST.get('redirecting')
        userFormInst = userForm(request.POST)
        if userFormInst.is_valid():
            cd_1 = userFormInst.save(commit=False)
            cd_1.save()
            cd_1.refresh_from_db()
        if methodType == 'new':
            objlnst = None
        else:
            pkID = request.POST.get('dataID')
            objlnst = get_object_or_404(investorPersonalDetails, id=pkID)
        objForm = investorPersonalDetailsForm(request.POST, request.FILES, instance=objlnst)
        if objForm.is_valid():
            cd = objForm.save(commit=False)
            cd.profileOwner = cd_1
            cd.createdBy = request.user
            cd.save()
            cd.refresh_from_db()
            connectedProfiles = connectedInvestors(user=request.user, connectedProfile=cd_1, createdBy=request.user)
            connectedProfiles.save()
            connectedProfiles.refresh_from_db()
            investmentProfile = investmentDetails(profileOwner=cd_1)
            investmentProfile.save()
            investmentProfile.refresh_from_db()
            bankProfile = bankForSlug(profileOwner=cd_1)
            bankProfile.save()
            bankProfile.refresh_from_db()
            dematProfile = dematForSlug(profileOwner=cd_1)
            dematProfile.save()
            dematProfile.refresh_from_db()
            messages.success(request, 'Updated Successfully')
        else:
            messages.error(request, 'False')
        return redirect(redirectTo)
    return HttpResponse('Invalid Entry')


# start writing code by shubham
def investmentDetailsView(request):
    if request.method == 'POST':
        methodType = request.POST.get('submitType')
        redirectTo = request.POST.get('requestFrom')
        redirectSuccess = request.POST.get('redirecting')
        if methodType == 'new':
            objlnst = None
        else:
            pkID = request.POST.get('dataID')
            objlnst = get_object_or_404(investmentDetails, pk=pkID)
        objForm = investmentDetailsForm(request.POST, instance=objlnst)
        if objForm.is_valid():
            cd = objForm.save(commit=False)
            cd.profileOwner = request.user
            cd.author = request.user
            cd.save()
            cd.refresh_from_db()
            objForm.save_m2m()
            messages.success(request, 'Investment Details Updated Successfully')
        else:
            messages.error(request, objForm.errors)
        # print(objForm.errors)
        return redirect('investorApp:bankUrl')
    # return redirect('investorApp:bankUrl')
    return HttpResponse('Invalid Entry')


#
def slugBasedInvestorDetailSubmitView(request):
    if request.method == 'POST':
        methodType = request.POST.get('submitType')
        redirectTo = request.POST.get('requestFrom')
        redirectSuccess = request.POST.get('redirecting')
        PersonalInst = request.POST.get('peraonalInstance')
        if methodType == 'new':
            objlnst = None
        else:
            pkID = request.POST.get('dataID')
            objlnst = get_object_or_404(investmentDetails, pk=pkID)
        objForm = investmentDetailsForm(request.POST, instance=objlnst)
        if objForm.is_valid():
            cd = objForm.save(commit=False)
            # cd.profileOwner = request.user
            # cd.author=request.user
            cd.save()
            cd.refresh_from_db()
            objForm.save_m2m()
            messages.success(request, 'Investment Details Updated Successfully')
        else:
            messages.error(request, 'Please check an error occured!')
        # print(objForm.errors)
        return redirect('investorApp:slugBasedBankUrl', PersonalInst)
    # return redirect('investorApp:bankUrl')
    return HttpResponse('Invalid Entry')


# def set_default(request):
# 	investorBanks = investorBankDetails.objects.filter(profileOwner=request.user)


def investorBankDetailsView(request):
    if request.method == 'POST':
        # print("bank non slug view is running")
        methodType = request.POST.get('submitType')
        redirectTo = request.POST.get('requestFrom')
        redirectSuccess = request.POST.get('redirecting')
        # print(methodType)
        if methodType == 'new':
            objlnst = None
        elif methodType == 'update':
            pkID = request.POST.get('dataID')
            # print(pkID)
            objlnst = get_object_or_404(investorBankDetails, pk=pkID)
        objForm = investorBankDetailsForm(request.POST, request.FILES, instance=objlnst)
        # print(objForm)
        # print(objForm.is_valid())
        if objForm.is_valid():
            cd = objForm.save(commit=False)
            cd.author = request.user
            cd.profileOwner = request.user
            profileOwner = User.objects.get(pk=request.user.pk)
            investorBanks = investorBankDetails.objects.filter(profileOwner=profileOwner, is_default=True)
            if cd.is_default == True:
                for item in investorBanks:
                    item.is_default = False
                    item.save()
            cd.save()
            objForm.save_m2m()
            cd.refresh_from_db()
            if methodType == 'new':
                messages.success(request, 'Bank Details Added Successfully')
            else:
                messages.success(request, 'Bank Details Updated Successfully')
        else:
            messages.error(request, 'False')
        # print(objForm.errors)
        return redirect(redirectTo)
    return HttpResponse('Invalid Entry')


#
def slugBasedinvestorBankDetailSubmitView(request):
    if request.method == 'POST':
        methodType = request.POST.get('submitType')
        redirectTo = request.POST.get('requestFrom')
        redirectSuccess = request.POST.get('redirecting')
        slugInst = request.POST.get('slug')
        personalInst = request.POST.get('personalInstance')
        userInst = User.objects.get(username=personalInst)

        if methodType == 'new':
            objlnst = None
        elif methodType == 'update':
            pkID = request.POST.get('dataID')
            # print(pkID)
            objlnst = get_object_or_404(investorBankDetails, pk=pkID)
        objForm = investorBankDetailsForm(request.POST, request.FILES, instance=objlnst)
        # print(objForm)
        # print(objForm.is_valid())
        if objForm.is_valid():
            cd = objForm.save(commit=False)
            cd.author = userInst
            cd.profileOwner = userInst

            # profileOwnerPk = User.objects.get(pk=userInst.pk)
            investorBanks = investorBankDetails.objects.filter(profileOwner=userInst, is_default=True)
            if cd.is_default == True:
                for item in investorBanks:
                    item.is_default = False
                    item.save()
            cd.save()
            objForm.save_m2m()
            cd.refresh_from_db()
            if methodType == 'new':
                messages.success(request, 'Bank Details Added Successfully')
            else:
                messages.success(request, 'Bank Details Updated Successfully')
        else:
            messages.error(request, 'False')
        # print(objForm.errors)
        return redirect(redirectTo)
    return HttpResponse('Invalid Entry')


#

def investorDMATDetailsView(request):
    if request.method == 'POST':
        methodType = request.POST.get('submitType')
        redirectTo = request.POST.get('requestFrom')
        redirectSuccess = request.POST.get('redirecting')
        if methodType == 'new':
            objlnst = None
        else:
            pkID = request.POST.get('dataID')
            objlnst = get_object_or_404(investorDMATDetails, pk=pkID)

        objForm = investorDMATDetailsForm(request.POST, request.FILES, instance=objlnst)
        if objForm.is_valid():
            cd = objForm.save(commit=False)
            cd.author = request.user
            cd.profileOwner = request.user
            profileOwner = User.objects.get(pk=request.user.pk)
            if cd.is_default == True:
                investorDMATS = investorDMATDetails.objects.filter(profileOwner=profileOwner, is_default=True)
                for item in investorDMATS:
                    item.is_default = False
                    item.save()
            cd.save()
            objForm.save_m2m()
            cd.refresh_from_db()
            if methodType == 'new':
                messages.success(request, 'DMAT Details Added Successfully')
            else:
                messages.success(request, 'DMAT Details Updated Successfully')
        else:
            messages.error(request, 'False')
        # print(objForm.errors)
        return redirect(redirectTo)
    return HttpResponse('Invalid Entry')


#
def slugBasedDmatDetailSubmitView(request):
    if request.method == 'POST':
        methodType = request.POST.get('submitType')
        redirectTo = request.POST.get('requestFrom')
        redirectSuccess = request.POST.get('redirecting')
        slugInst = request.POST.get('slug')
        personalInst = request.POST.get('personalInstance')

        userInst = User.objects.get(username=personalInst)

        if methodType == 'new':
            objlnst = None
        else:
            pkID = request.POST.get('dataID')
            objlnst = get_object_or_404(investorDMATDetails, pk=pkID)
        objForm = investorDMATDetailsForm(request.POST, request.FILES, instance=objlnst)
        if objForm.is_valid():
            cd = objForm.save(commit=False)
            cd.author = userInst
            cd.profileOwner = userInst
            profileOwner = userInst
            investorDMATS = investorDMATDetails.objects.filter(profileOwner=profileOwner, is_default=True)
            if cd.is_default == True:
                for item in investorDMATS:
                    item.is_default = False
                    item.save()
            cd.save()
            objForm.save_m2m()
            cd.refresh_from_db()
            if methodType == 'new':
                messages.success(request, 'DMAT Details Added Successfully')
            else:
                messages.success(request, 'DMAT Details Updated Successfully')
        else:
            messages.error(request, 'False')
        # print(objForm.errors)
        return redirect(redirectTo)
    return HttpResponse('Invalid Entry')


def stockBrokerDetailsView(request):
    if request.method == 'POST':
        methodType = request.POST.get('submitType')
        redirectTo = request.POST.get('requestFrom')
        redirectSuccess = request.POST.get('redirecting')
        if methodType == 'new':
            objlnst = None
        else:
            pkID = request.POST.get('dataID')
            objlnst = get_object_or_404(stockBrokerDetails, pk=pkID)
        objForm = stockBrokerDetailsForm(request.POST, request.FILES, instance=objlnst)
        if objForm.is_valid():
            cd = objForm.save(commit=False)
            cd.createdBy = request.user
            cd.profileOwner = request.user
            cd.save()
            cd.refresh_from_db()
            messages.success(request, 'Updated Successfully')
        else:
            messages.error(request, 'False')
    return HttpResponse('Invalid Entry')


def lookingToInvestDetailsView(request):
    if request.method == 'POST':
        methodType = request.POST.get('submitType')
        redirectTo = request.POST.get('requestFrom')
        redirectSuccess = request.POST.get('redirecting')
        if methodType == 'new':
            objlnst = None
        else:
            pkID = request.post.get('dataID')
            objlnst = get_object_or_404(lookingToInvestDetails, pk=pkID)
        objForm = lookingToInvestDetailsForm(request.POST, request.FILES, instance=objlnst)
        if objForm.is_valid():
            cd = objForm.save(commit=False)
            cd.createdBy = request.user
            cd.profileOwner = request.user
            cd.save()
            cd.refresh_from_db()
            messages.success(request, 'Updates Successfully')
        else:
            messages.error(request, 'False')
    return HttpResponse('Invalid Entry')


# ends the code by shuham


# Gaurav Code
def load_states(request):
    try:
        countryId = request.GET.get('country')
    except:
        countryId = None
    states = state.objects.filter(stateCountry=countryId).order_by('name')
    context = {
        'states': states,
    }
    return render(request, 'investor/stateoptions.html', context)


def load_cities(request):
    try:
        cityId = request.GET.get('state')
    except:
        cityId = None
    cities = city.objects.filter(cityState=cityId)
    context = {
        'cities': cities,
    }
    return render(request, 'investor/cityoptions.html', context)


def load_statesClick(request):
    try:
        stateId = request.GET.get('stateId')
    except:
        stateId = None

    try:
        stateInst = state.objects.get(pk=stateId)
        countryId = country.objects.get(pk=stateInst.stateCountry.pk)
    except:
        countryId = None
    states = state.objects.filter(stateCountry=countryId).order_by('name')
    context = {
        'states': states,
    }
    return render(request, 'investor/stateoptions.html', context)


def load_citiesClick(request):
    try:
        cityId = request.GET.get('cityId')
    except:
        cityId = None
    # print(cityId)
    try:
        cityInst = city.objects.get(pk=cityId)
        stateId = state.objects.get(pk=cityInst.cityState.pk)
    except:
        stateId = None
    # print(cityInst)
    # print(stateId)
    cities = city.objects.filter(cityState=stateId).order_by('name')
    # print(cities)
    context = {
        'cities': cities,
    }
    return render(request, 'investor/cityoptions.html', context)


@staff_member_required
def investorKycView(request):
    getAllMobile()

    allInvestors = investorPersonalDetails.objects.all().order_by('id')
    nameSearch = request.GET.get('name') or None
    emailSearch = request.GET.get('email') or None
    mobileSearch = request.GET.get('mobile') or None
    bankSearch = request.GET.get('bankStatusSearch') or None
    dmatSearch = request.GET.get('dmatStatusSearch') or None
    panSearch = request.GET.get('panStatusSearch') or None
    aadharSearch = request.GET.get('aadharStatusSearch') or None
    personalSearch = request.GET.get('personalStatusSearch') or None
    progressSearch = request.GET.get('progress') or None
    starDate = request.GET.get('startDateSearch') or None
    endDate = request.GET.get('endDateSearch') or None

    try:
        ed = datetime.datetime.strptime(endDate, "%Y-%m-%d").date() + datetime.timedelta(days=1)
    except:
        ed = ""

    ed = str(ed)

    if nameSearch:
        allInvestors = allInvestors.exclude(profileOwner=None).filter(name__icontains=nameSearch)
    if mobileSearch:
        allInvestors = allInvestors.exclude(profileOwner=None).filter(mobileNumber__icontains=mobileSearch)
    if emailSearch:
        allInvestors = allInvestors.exclude(profileOwner=None).filter(profileOwner__email=emailSearch)
    if personalSearch:
        allInvestors = allInvestors.exclude(profileOwner=None).filter(
            profileOwner__profileOwnerVSD__getPersonalStatus__icontains=personalSearch)
    if aadharSearch:
        allInvestors = allInvestors.exclude(profileOwner=None).filter(
            profileOwner__profileOwnerVSD__getAadharStatus__icontains=aadharSearch)
    if panSearch:
        allInvestors = allInvestors.exclude(profileOwner=None).filter(
            profileOwner__profileOwnerVSD__getPanStatus__icontains=panSearch)
    if bankSearch:
        allInvestors = allInvestors.exclude(profileOwner=None).filter(
            profileOwner__profileOwnerVSD__bankVerifiedStatus__icontains=bankSearch)
    if dmatSearch:
        allInvestors = allInvestors.exclude(profileOwner=None).filter(
            profileOwner__profileOwnerVSD__dmatVerifiedStatus__icontains=dmatSearch)
    if progressSearch:
        if progressSearch:
            allInvestors = allInvestors.exclude(profileOwner=None).filter(
                profileOwner__profileOwnerVSD__getVerifiedProgress__gte=progressSearch)
    if starDate and endDate:
        allInvestors = allInvestors.exclude(profileOwner=None).filter(created__gte=starDate, created__lte=ed)
    elif starDate:
        allInvestors = allInvestors.exclude(profileOwner=None).filter(created__icontains=starDate)
    elif endDate:
        allInvestors = allInvestors.exclude(profileOwner=None).filter(created__icontains=endDate)

    countryList = country.objects.all()
    context = {
        'allInvestors': allInvestors,
        'countryList': countryList,
    }
    return render(request, 'investor/investorKyc.html', context)


def createSource():
    userInst = investorPersonalDetails.objects.all()
    for item in userInst:
        try:
            sourceInst = investorSourceDetails.objects.create(profileOwner=item.profileOwner)
        except:
            pass

    return True


@staff_member_required
def investorsourceView(request, slug):
    action = 'action'

    PersonalInst = None
    sourceInst = None

    if request.user.is_authenticated:
        try:
            PersonalInst = investorPersonalDetails.objects.get(profileOwner__username=slug)

            sourceInst = get_object_or_404(investorSourceDetails, profileOwner=PersonalInst.profileOwner)

        except:
            sourceInst = None

    else:
        PersonalInst = None
        sourceInst = None

    # try:
    # 	userList = getConnectedUsers(request.user, requestFor='investment')
    # except:
    # 	userList = None

    sourceNameInst = investorSource.objects.all()

    investorPortfolioManagedByInst = investorPortfolioManagedBy.objects.all()

    channelPartnerListInst = channelPartnerList.objects.all()

    dealerListInst = dealerList.objects.all()

    createSource()
    # print(PersonalInst)

    context = {
        'action': action,
        'PersonalInst': PersonalInst,
        'sourceInst': sourceInst,
        'sourceNameInst': sourceNameInst,
        'investorPortfolioManagedByInst': investorPortfolioManagedByInst,
        'channelPartnerListInst': channelPartnerListInst,
        'dealerListInst': dealerListInst,
    }
    return render(request, 'investor/sourceDetails.html', context)


#### code by shubham starts here #######

def countYears(investmentDate):
    start_date = investmentDate.date()
    end_date = datetime.datetime.now().date()
    # print(start_date)
    # print(end_date)
    diffyears = end_date.year - start_date.year
    difference = end_date - start_date.replace(end_date.year)
    days_in_year = isleap(end_date.year) and 366 or 365
    difference_in_years = diffyears + (difference.days) / days_in_year

    # print(f'this is difference year --- {difference_in_years}')

    return difference_in_years


@login_required(login_url='authApp:loginUsernameHandlerUrl')
def investorpotfolioView(request):
    investorInst = investorPersonalDetails.objects.all().order_by('id')
    try:
        userInst = User.objects.get(pk=request.user.pk)
    except:
        userInst = None
    print(request.user.pk)
    # messages.error(request, message= request.user.pk)
    try:
        investorInst = investorPersonalDetails.objects.get(profileOwner=userInst)
    except:
        investorInst = None

    allTransactionsOfUserInst = Transaction.objects.filter(made_by=userInst).order_by('-made_on').order_by('-trxnDate')
    stockBasicDetailInst = stockBasicDetail.objects.all()

    ######## Total Values ################
    # portfolioInvestoTotals={}
    totalAmountWeight = 0
    totalInvestmentValue = 0
    totalCurrentValue = 0
    totalPL = 0
    totalAbsReturn = 0
    totalDiv = 0

    portfolioDict = {}
    portfolioUserDataDict = {}
    transactionSubDict = {}
    transactionDict = {}

    #### to find allocation for userInst  ###
    totalPresentValue = totalDiv = totalInvestmentPrice = weightAverageReturn = 0
    totalDivident = 0

    for item in allTransactionsOfUserInst:
        try:
            priceInst = buyPreIPOStockList.objects.filter(stockName=item.selected_stock).latest('publish')
        except:
            priceInst = None
        try:
            dividendInst = stockEssentials.objects.filter(stockProfileName=item.selected_stock).latest('publish')
        except:
            dividendInst = None

        if item.pg_status == 'TXN_SUCCESS' or item.txn_made_by == 'Self':

            try:
                totalDiv = totalDiv + (item.total_dividend * item.quantity)
            except:
                totalDiv = 0

            if priceInst:
                try:
                    totalPresentValue += item.quantity * priceInst.investorPrice
                except:
                    totalPresentValue = 0
            else:
                totalPresentValue = 0

            totalInvestmentPrice += item.investMentPrice

    transactioCount = currentVal = totalAmountWeight = investmentVal = totalInvestmentValue = totalCurrentValue = transactionProfitLoss = profitLossPercent = 0

    ##### values for particular stock #########################
    for item in allTransactionsOfUserInst:

        # print(f'this is list of dividends {item.total_dividend}')
        try:
            priceInst = buyPreIPOStockList.objects.filter(stockName=item.selected_stock).latest('publish')
        except:
            priceInst = None
        try:
            dividendInst = stockEssentials.objects.filter(stockProfileName=item.selected_stock).latest('publish')
        except:
            dividendInst = None

        if item.pg_status == 'TXN_SUCCESS' or item.txn_made_by == 'Self':

            totalAmountWeight += item.amount
            investmentVal = item.quantity * item.investMentPrice
            totalInvestmentValue += investmentVal

            if priceInst:
                try:
                    currentVal = item.quantity * priceInst.investorPrice
                except:
                    currentVal = 0
            else:
                currentVal = 0
            totalCurrentValue += currentVal
            transactionProfitLoss = currentVal - investmentVal
            # print(f'this is profit {transactionProfitLoss}')
            if priceInst:
                try:
                    profitLossPercent = (priceInst.investorPrice - item.investMentPrice) * 100
                except:
                    profitLossPercent = 0
            else:
                profitLossPercent = 0

            if priceInst:
                try:
                    weightAverageReturn += (item.investMentPrice / totalInvestmentPrice) * (
                                ((priceInst.investorPrice - item.investMentPrice) / item.investMentPrice) * 100)
                except:
                    weightAverageReturn = 0
            else:
                weightAverageReturn = 0

            transactionSubDict['paymentType'] = item.txn_made_by
            transactionSubDict['investment_value'] = investmentVal
            transactionSubDict['current_value'] = currentVal
            transactionSubDict['amount'] = item.amount
            # transactionSubDict['profileLoss'] = transactionProfitLoss
            transactionSubDict['id'] = item.id
            transactionSubDict['selected_stock'] = item.selected_stock
            transactionSubDict['quantity'] = item.quantity
            transactionSubDict['made_on'] = item.made_on
            transactionSubDict['trxnDate'] = item.trxnDate
            transactionSubDict['investMentPrice'] = item.investMentPrice
            if priceInst:
                transactionSubDict['stockPrice'] = priceInst.investorPrice
            else:
                transactionSubDict['stockPrice'] = 0
            transactionSubDict['dividend'] = item.total_dividend * item.quantity

            if priceInst:
                transactionSubDict['stockRating'] = priceInst.ratings
            else:
                transactionSubDict['stockRating'] = 0

            if priceInst:
                try:
                    transactionSubDict['profitLoss'] = (item.quantity * priceInst.investorPrice) - (
                                item.quantity * item.investMentPrice) + (item.total_dividend * item.quantity)
                except:
                    transactionSubDict['profitLoss'] = 0
            else:
                transactionSubDict['profitLoss'] = 0

            if priceInst:
                try:
                    # transactionSubDict['absoluteReturn']=(((item.investMentPrice)+(item.quantity * priceInst.investorPrice)-(item.quantity * item.investMentPrice)+item.total_dividend)/item.investMentPrice)*100
                    transactionSubDict['absoluteReturn'] = (priceInst.investorPrice + item.total_dividend) / (
                        item.investMentPrice) * 100
                except:
                    transactionSubDict['absoluteReturn'] = 0
            else:
                transactionSubDict['absoluteReturn'] = 0

            if priceInst:
                try:
                    transactionSubDict['allocation'] = ((
                                                                    item.quantity * priceInst.investorPrice) / totalPresentValue) * 100
                except:
                    transactionSubDict['allocation'] = 0
            else:
                transactionSubDict['allocation'] = 0

            if item.trxnDate and priceInst:
                try:
                    transactionSubDict['returnPerYear'] = ((float(
                        (priceInst.investorPrice) / (item.investMentPrice)) ** (
                                                                        1 / countYears(item.trxnDate))) - 1) * 100
                except:
                    transactionSubDict['returnPerYear'] = 0
            elif item.made_on and priceInst:
                try:
                    transactionSubDict['returnPerYear'] = ((float(
                        (priceInst.investorPrice) / (item.investMentPrice)) ** (
                                                                        1 / countYears(item.made_on))) - 1) * 100
                except:
                    transactionSubDict['returnPerYear'] = 0
            else:
                transactionSubDict['returnPerYear'] = 0

            transactionDict[item] = transactionSubDict
            transactionSubDict = {}

    # print(weightAverageReturn)
    totalPL = totalCurrentValue - totalInvestmentValue
    try:
        totalAbsReturn = (totalCurrentValue / totalAmountWeight) * 100
    except:
        totalAbsReturn = 0
    portfolioUserDataDict['total_amount'] = totalAmountWeight
    portfolioUserDataDict['investment_value'] = totalInvestmentValue
    portfolioUserDataDict['current_value'] = totalCurrentValue
    portfolioUserDataDict['profile_or_loss'] = totalPL
    portfolioUserDataDict['absolute_return'] = totalAbsReturn
    portfolioUserDataDict['weightAverageReturnPerYear'] = weightAverageReturn
    portfolioUserDataDict['transactions'] = transactionDict

    transactionDict = {}
    try:
        portfolioDict[userInst.profileOwnerIPD.name] = portfolioUserDataDict
    except:
        portfolioDict['None'] = portfolioUserDataDict

    #########################################################################
    ############ dicts for new add investor #################################

    #### to find allocation for userInst s ###
    totalPresentValueTemp = 0
    totalDivTemp = 0

    ##### to find allocation ######

    allTempUsers = tempUser.objects.filter(profileOwner=userInst)
    for item in allTempUsers:

        totalAmountWeight = totalInvestmentValue = totalCurrentValue = totalPL = totalAbsReturn = totalDiv = totalInvestmentPrice = weightAverageReturn = 0

        portfolioUserDataDict = {}
        tempUserTransaction = tempTransaction.objects.filter(made_by=item).order_by('-trxnDate')
        transactionDict = {}
        transactionSubDict = {}

        for subItem in tempUserTransaction:
            try:
                priceInst = buyPreIPOStockList.objects.filter(stockName=subItem.selected_stock).latest('publish')
            except:
                priceInst = None

            try:
                dividendInst = stockEssentials.objects.filter(stockProfileName=subItem.selected_stock).latest('publish')
            except:
                dividendInst = None

            if dividendInst:
                try:
                    totalDivTemp = totalDivTemp + (dividendInst.total_dividend * subItem.quantity)
                except:
                    totalDivTemp = 0

            if priceInst:
                try:
                    totalPresentValueTemp += subItem.quantity * priceInst.investorPrice
                except:
                    totalPresentValueTemp = 0
            else:
                totalPresentValueTemp = 0

            totalInvestmentPrice += subItem.investMentPrice

        for subItem in tempUserTransaction:

            try:
                priceInst = buyPreIPOStockList.objects.filter(stockName=subItem.selected_stock).latest('publish')
            except:
                priceInst = None

            try:
                dividendInst = stockEssentials.objects.filter(stockProfileName=subItem.selected_stock).latest('publish')
            except:
                dividendInst = None

            totalAmountWeight += subItem.amount
            investmentVal = subItem.quantity * subItem.investMentPrice
            if priceInst:
                try:
                    currentVal = subItem.quantity * priceInst.investorPrice
                except:
                    currentVal = 0
            else:
                currentVal = 0

            transactionProfitLoss = currentVal - investmentVal
            absoluteReturn = (currentVal / subItem.amount) * 100
            totalInvestmentValue += investmentVal
            totalCurrentValue += currentVal

            if priceInst:
                try:
                    profitLossPercent = (priceInst.investorPrice - subItem.investMentPrice) * 100
                except:
                    profitLossPercent = 0
            else:
                profitLossPercent = 0

            if priceInst:
                try:
                    weightAverageReturn += (subItem.investMentPrice / totalInvestmentPrice) * (
                                ((priceInst.investorPrice - subItem.investMentPrice) / subItem.investMentPrice) * 100)
                except:
                    weightAverageReturn = 0
            else:
                weightAverageReturn = 0

            transactionSubDict['paymentType'] = subItem.txn_made_by
            transactionSubDict['tempUserID'] = subItem.made_by.pk
            transactionSubDict['investment_value'] = investmentVal
            transactionSubDict['current_value'] = currentVal
            # transactionSubDict['profile_or_loss'] = transactionProfitLoss
            transactionSubDict['selected_stock'] = subItem.selected_stock
            transactionSubDict['quantity'] = subItem.quantity
            transactionSubDict['amount'] = subItem.amount
            try:
                transactionSubDict['made_on'] = subItem.made_on
            except:
                transactionSubDict['made_on'] = None
            transactionSubDict['trxnDate'] = subItem.trxnDate
            transactionSubDict['investMentPrice'] = subItem.investMentPrice
            if priceInst:
                transactionSubDict['stockPrice'] = priceInst.investorPrice
            else:
                transactionSubDict['stockPrice'] = 0

            transactionSubDict['dividend'] = subItem.total_dividend * subItem.quantity

            if priceInst:
                transactionSubDict['stockRating'] = priceInst.ratings
            else:
                transactionSubDict['stockPrice'] = 0

            if priceInst:
                try:
                    transactionSubDict['profitLoss'] = (subItem.quantity * priceInst.investorPrice) - (
                                subItem.quantity * subItem.investMentPrice) + (
                                                                   subItem.total_dividend * subItem.quantity)
                except:
                    transactionSubDict['profitLoss'] = 0
            else:
                transactionSubDict['profitLoss'] = 0

            if priceInst:
                try:
                    # transactionSubDict['absoluteReturn']=(((subItem.investMentPrice)+(subItem.quantity * priceInst.investorPrice)-(subItem.quantity * subItem.investMentPrice)+subItem.total_dividend)/subItem.investMentPrice)*100
                    transactionSubDict['absoluteReturn'] = (priceInst.investorPrice + subItem.total_dividend) / (
                        subItem.investMentPrice) * 100
                except:
                    transactionSubDict['absoluteReturn'] = 0
            else:
                transactionSubDict['absoluteReturn'] = 0

            if priceInst:
                try:
                    transactionSubDict['allocation'] = ((
                                                                    subItem.quantity * priceInst.investorPrice) / totalPresentValueTemp) * 100
                except:
                    transactionSubDict['allocation'] = 0
            else:
                transactionSubDict['allocation'] = 0

            if subItem.trxnDate and priceInst:
                try:
                    transactionSubDict['returnPerYear'] = ((float(
                        (priceInst.investorPrice) / (subItem.investMentPrice)) ** (
                                                                        1 / countYears(subItem.trxnDate))) - 1) * 100
                except:
                    transactionSubDict['returnPerYear'] = 0
            else:
                transactionSubDict['returnPerYear'] = 0

            transactionDict[subItem] = transactionSubDict
            transactionSubDict = {}

        totalPL = totalCurrentValue - totalInvestmentValue
        try:
            totalAbsReturn = (totalCurrentValue / totalAmountWeight) * 100
        except:
            totalAbsReturn = 0
        portfolioUserDataDict['total_amount'] = totalAmountWeight
        portfolioUserDataDict['investment_value'] = totalInvestmentValue
        portfolioUserDataDict['current_value'] = totalCurrentValue
        portfolioUserDataDict['profile_or_loss'] = totalPL
        portfolioUserDataDict['absolute_return'] = totalAbsReturn
        portfolioUserDataDict['weightAverageReturnPerYear'] = weightAverageReturn

        try:
            portfolioUserDataDict['totalReturnPerYear'] = ((
                                                                       totalCurrentValue - totalInvestmentValue / currentValue) ** (
                                                                       1 / 1)) - 1
        except:
            portfolioUserDataDict['totalReturnPerYear'] = 0

        portfolioUserDataDict['transactions'] = transactionDict
        transactionDict = {}
        portfolioDict[item] = portfolioUserDataDict

    ####### all Totals ########
    numberOfusers = len(portfolioDict.keys())
    summationInvestedAmount = summationCurrentValue = summationProfitLoss = summationAbsoluteReturn = summationReturnPerYear = 0
    summationInvestedAmount = sum(d['investment_value'] for d in portfolioDict.values() if d)
    summationCurrentValue = sum(d['current_value'] for d in portfolioDict.values() if d)
    summationProfitLoss = sum(d['profile_or_loss'] for d in portfolioDict.values() if d)
    try:
        summationAbsoluteReturn = summationCurrentValue / summationInvestedAmount * 100
    except:
        summationAbsoluteReturn = 0
    try:
        summationReturnPerYear = sum(
            d['weightAverageReturnPerYear'] for d in portfolioDict.values() if d) / numberOfusers
    except:
        summationReturnPerYear = 0

    print(f'this is the count of all transaction {numberOfusers}')
    # print(f'this is sum of current value {summationCurrentValue}')

    context = {
        'userInst': userInst,
        'portfolioDict': portfolioDict,
        'investorInst': investorInst,
        'allTransactionsOfUserInst': allTransactionsOfUserInst,
        'stockBasicDetailInst': stockBasicDetailInst,
        'summationInvestedAmount': summationInvestedAmount,
        'summationCurrentValue': summationCurrentValue,
        'summationProfitLoss': summationProfitLoss,
        'summationAbsoluteReturn': summationAbsoluteReturn,
        'summationReturnPerYear': summationReturnPerYear
    }

    return render(request, 'investor/investorPortfolioNew.html', context)


@staff_member_required
def sharebookView(request):
    status = ''
    investorInst = request.GET.get('investorIdentity')
    shareBookDictMain = {}
    shareBookDict = {}
    stock_and_price = {}
    stockBasicDetailInst = stockBasicDetail.objects.all().order_by('stockName')
    for stock in stockBasicDetailInst:
        try:
            stockPrice = buyPreIPOStockList.objects.filter(stockName=stock).latest('id')
            stock_and_price[stock] = stockPrice.investorPrice
        except:
            stock_and_price[stock] = 0
    investorDetailInst = None

    if investorInst:
        try:
            investorDetailInst = investorPersonalDetails.objects.get(profileOwner__username=investorInst)
            status = 'success'
        except:
            status = 'fail'
        if not investorDetailInst:
            try:
                investorDetailInst = investorPersonalDetails.objects.get(profileOwner__email=investorInst)
                status = 'success'
            except:
                status = 'fail'
        if not investorDetailInst:
            try:
                investorDetailInst = investorPersonalDetails.objects.get(panNumber=investorInst)
                status = 'success'
            except:
                status = 'fail'
    investorPersonalInst = None
    bankInst = None
    dmatInst = None
    stockInst = None
    allTransactionInsts = None
    if investorDetailInst:
        bankInst = investorBankDetails.objects.filter(
            Q(profileOwner=investorDetailInst.profileOwner) & Q(is_default=True)).last()
        dmatInst = investorDMATDetails.objects.filter(
            Q(profileOwner=investorDetailInst.profileOwner) & Q(is_default=True)).last()
        allTransactionInsts = Transaction.objects.filter(made_by=investorDetailInst.profileOwner).order_by('trxnDate')

    allTransactionInstsOfCart = Transaction.objects.all().exclude(made_by=None).order_by('made_on')
    ########### filters code #######################
    dateFilterSearchq = request.GET.get('dateFilterSearchq') or None
    executionDateSearchq = request.GET.get('searchDate') or None
    buyerNameSearchq = request.GET.get('buyerNameSearch') or None
    stockNameSearch = request.GET.get('stockNameSearch') or None
    searchShareTransfer = request.GET.get('searchShareTransfer') or None
    searchKyc = request.GET.get('searchKyc') or None
    searchQuantity = request.GET.get('searchQuantity') or None
    searchConsideration = request.GET.get('searchConsideration') or None
    if dateFilterSearchq:
        allTransactionInstsOfCart = allTransactionInstsOfCart.filter(
            trxnDate=dateFilterSearchq)
    if buyerNameSearchq:
        allTransactionInstsOfCart = allTransactionInstsOfCart.filter(
            made_by__profileOwnerIPD__name__icontains=buyerNameSearchq)       
    if executionDateSearchq:
        allTransactionInstsOfCart = allTransactionInstsOfCart.filter(
            trxnDate=executionDateSearchq)
    if stockNameSearch:
        allTransactionInstsOfCart = allTransactionInstsOfCart.filter(
            selected_stock__id=stockNameSearch)
    if searchShareTransfer:
        allTransactionInstsOfCart = allTransactionInstsOfCart.filter(
            sb_shareTransfer=searchShareTransfer)
    if searchKyc:
        allTransactionInstsOfCart = allTransactionInstsOfCart.filter(sb_KYC=searchKyc)
    if searchConsideration:
        allTransactionInstsOfCart = allTransactionInstsOfCart.filter(
            amount=int(searchConsideration))
    if searchQuantity:
        allTransactionInstsOfCart = allTransactionInstsOfCart.filter(
            quantity=int(searchQuantity))

    paginator = Paginator(allTransactionInstsOfCart, 100)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    for item in page_obj:
        try:
            investorPersonalInst = investorPersonalDetails.objects.filter(profileOwner=item.made_by).latest('id')
        except:
            investorPersonalInst = None
        try:
            stockInst = stockEssentials.objects.filter(stockProfileName=item.selected_stock).latest('id')
        except:
            stockInst = None

        try:
            transDocInst = transactionDocs.objects.filter(related_transaction=item).latest('id')
        except:
            transDocInst = None

        try:
            alltransDocInst = transactionDocs.objects.filter(related_transaction=item)
        except:
            alltransDocInst = None

        if item.pg_status == 'TXN_SUCCESS':
            if item.txn_made_by == 'PaymentGateway' or item.txn_made_by == 'ShareBook':
                shareBookDict['transactionInst'] = item

                shareBookDict['documentList'] = alltransDocInst

                if transDocInst:
                    shareBookDict['transactionDocID'] = transDocInst.id
                shareBookDict['transactionID'] = item.id
                shareBookDict['executionDate'] = item.trxnDate if item.trxnDate else item.made_on

                if investorPersonalInst:
                    shareBookDict['buyerName'] = investorPersonalInst.name
                else:
                    shareBookDict['buyerName'] = item.made_by

                shareBookDict['made_by'] = item.made_by
                shareBookDict['buyerIdentification'] = item.sb_buyerIdentification
                shareBookDict['company'] = item.sb_Company
                shareBookDict['depository'] = item.sb_Depository
                shareBookDict['purchasedStockName'] = item.selected_stock
                shareBookDict['shareQuantity'] = item.quantity
                shareBookDict['consideration'] = item.amount
                if bankInst:
                    shareBookDict['iskyc'] = 'Yes' if bankInst.cancelledCheque else 'No'
                else:
                    shareBookDict['iskyc'] = item.sb_KYC

                shareBookDict['isShareTransfer'] = item.sb_shareTransfer

                if dmatInst:
                    shareBookDict['dpID'] = dmatInst.dpID
                else:
                    shareBookDict['dpID'] = item.sb_DpID
                if dmatInst:
                    shareBookDict['clientID'] = dmatInst.clientID
                else:
                    shareBookDict['clientID'] = item.sb_clientID
                if dmatInst:
                    shareBookDict['stockBrokerName'] = dmatInst.stockBroker
                else:
                    shareBookDict['stockBrokerName'] = item.sb_brokerName

                if bankInst:
                    shareBookDict['buyerBankName'] = bankInst.bankName
                else:
                    shareBookDict['buyerBankName'] = item.sb_buyerBank

                if bankInst:
                    shareBookDict['buyerBankAccNo'] = bankInst.accountNumber
                else:
                    shareBookDict['sb_accountNo'] = item.sb_accountNo

                shareBookDict[
                    'paymentRefrenceNum'] = item.sb_paymentReference if item.sb_paymentReference else item.order_id

                if stockInst:
                    shareBookDict['isinNumber'] = stockInst.ISIN
                else:
                    shareBookDict['isinNumber'] = item.sb_ISIN

                if dmatInst:
                    shareBookDict['brokerName'] = dmatInst.stockBroker
                else:
                    shareBookDict['brokerName'] = item.sb_brokerName

                shareBookDict['made_by'] = item.made_by
                shareBookDict['reasonCode'] = item.sb_resonCode
                shareBookDict['investMentPrice'] = item.investMentPrice
                shareBookDict['uploadDocs'] = item.sb_uploadTransferRequest
                shareBookDictMain[item] = shareBookDict
                shareBookDict = {}
    shareBrokers = stockBrokerDetails.objects.all().order_by('name')
    context = {
        'shareBookDictMain': shareBookDictMain,
        'status': status,
        'investorDetailInst': investorDetailInst,
        'bankInst': bankInst,
        'dmatInst': dmatInst,
        'stockBasicDetailInst': stockBasicDetailInst,
        'stock_and_price': stock_and_price,
        'investorInst': investorInst,
        'allTransactionInsts': allTransactionInsts,
        'shareBrokers': shareBrokers,
        'page_obj': page_obj,
    }
    return render(request, 'investor/shareBookNew.html', context)


#
@api_view(['GET'])
def getinvestorpotfolioView(request):
    try:
        userInst = User.objects.get(pk=request.user.id)  # 658
    except:
        userInst = None

    userInst_detail = ""
    if userInst:
        userInst_detail = UserSerializer(userInst).data

    try:
        investorInst = investorPersonalDetails.objects.get(profileOwner=userInst)
    except:
        investorInst = None

    investorInst_detail = ""
    if investorInst:
        investorInst_detail = investorPersonalDetailsSerializer(investorInst).data

    allTransactionsOfUserInst = Transaction.objects.filter(made_by=userInst).order_by('-made_on').order_by('-trxnDate')

    allTransactionsOfUserInst_list = []
    if allTransactionsOfUserInst:
        allTransactionsOfUserInst_list = TransactionSerializer(allTransactionsOfUserInst, many=True).data

    stockBasicDetailInst = stockBasicDetail.objects.all()

    stockBasicDetailInst_list = []
    if stockBasicDetailInst:
        stockBasicDetailInst_list = stockBasicDetailSerializer(stockBasicDetailInst, many=True).data

    ######## Total Values ################
    totalAmountWeight = 0
    totalInvestmentValue = 0
    totalCurrentValue = 0
    totalPL = 0
    totalAbsReturn = 0
    totalDiv = 0

    portfolioDict = []
    portfolioUserDataDict = {}
    transactionSubDict = {}
    transactionList = []

    #### to find allocation for userInst  ###
    totalPresentValue = totalDiv = totalInvestmentPrice = weightAverageReturn = 0
    totalDivident = 0

    for item in allTransactionsOfUserInst:
        try:
            priceInst = buyPreIPOStockList.objects.filter(stockName=item.selected_stock).latest('publish')
        except:
            priceInst = None
        try:
            dividendInst = stockEssentials.objects.filter(stockProfileName=item.selected_stock).latest('publish')
        except:
            dividendInst = None

        if item.pg_status == 'TXN_SUCCESS' or item.txn_made_by == 'Self':

            try:
                totalDiv = totalDiv + (item.total_dividend * item.quantity)
            except:
                totalDiv = 0

            if priceInst:
                try:
                    totalPresentValue += item.quantity * priceInst.investorPrice
                except:
                    totalPresentValue = 0
            else:
                totalPresentValue = 0

            totalInvestmentPrice += item.investMentPrice

    transactioCount = currentVal = totalAmountWeight = investmentVal = totalInvestmentValue = totalCurrentValue = transactionProfitLoss = profitLossPercent = 0

    ##### values for particular stock #########################
    for item in allTransactionsOfUserInst:

        try:
            priceInst = buyPreIPOStockList.objects.filter(stockName=item.selected_stock).latest('publish')
        except:
            priceInst = None
        try:
            dividendInst = stockEssentials.objects.filter(stockProfileName=item.selected_stock).latest('publish')
        except:
            dividendInst = None

        if item.pg_status == 'TXN_SUCCESS' or item.txn_made_by == 'Self':

            totalAmountWeight += item.amount
            investmentVal = item.quantity * item.investMentPrice
            totalInvestmentValue += investmentVal

            if priceInst:
                try:
                    currentVal = item.quantity * priceInst.investorPrice
                except:
                    currentVal = 0
            else:
                currentVal = 0
            totalCurrentValue += currentVal
            transactionProfitLoss = currentVal - investmentVal
            if priceInst:
                try:
                    profitLossPercent = (priceInst.investorPrice - item.investMentPrice) * 100
                except:
                    profitLossPercent = 0
            else:
                profitLossPercent = 0

            if priceInst:
                try:
                    weightAverageReturn += (item.investMentPrice / totalInvestmentPrice) * (
                                ((priceInst.investorPrice - item.investMentPrice) / item.investMentPrice) * 100)
                except:
                    weightAverageReturn = 0
            else:
                weightAverageReturn = 0

            transactionSubDict['paymentType'] = item.txn_made_by
            transactionSubDict['investment_value'] = investmentVal
            transactionSubDict['current_value'] = currentVal
            transactionSubDict['amount'] = item.amount
            # transactionSubDict['profileLoss'] = transactionProfitLoss
            transactionSubDict['id'] = item.id
            transactionSubDict['selected_stock'] = stockBasicDetailSerializer(item.selected_stock).data
            transactionSubDict['quantity'] = item.quantity
            transactionSubDict['made_on'] = item.made_on
            transactionSubDict['trxnDate'] = item.trxnDate
            transactionSubDict['investMentPrice'] = item.investMentPrice
            if item.demat:
                transactionSubDict['demat'] = stockBrokerDetailSerializer(item.demat).data
            else:
                transactionSubDict['demat'] = None
            if priceInst:
                transactionSubDict['stockPrice'] = priceInst.investorPrice
            else:
                transactionSubDict['stockPrice'] = 0
            transactionSubDict['dividend'] = item.total_dividend * item.quantity

            if priceInst:
                transactionSubDict['stockRating'] = priceInst.ratings
            else:
                transactionSubDict['stockRating'] = 0

            if priceInst:
                try:
                    transactionSubDict['profitLoss'] = (item.quantity * priceInst.investorPrice) - (
                                item.quantity * item.investMentPrice) + (item.total_dividend * item.quantity)
                except:
                    transactionSubDict['profitLoss'] = 0
            else:
                transactionSubDict['profitLoss'] = 0

            if priceInst:
                try:
                    # transactionSubDict['absoluteReturn']=(((item.investMentPrice)+(item.quantity * priceInst.investorPrice)-(item.quantity * item.investMentPrice)+item.total_dividend)/item.investMentPrice)*100
                    transactionSubDict['absoluteReturn'] = (priceInst.investorPrice + item.total_dividend) / (
                        item.investMentPrice) * 100
                except:
                    transactionSubDict['absoluteReturn'] = 0
            else:
                transactionSubDict['absoluteReturn'] = 0

            if priceInst:
                try:
                    transactionSubDict['allocation'] = ((
                                                                    item.quantity * priceInst.investorPrice) / totalPresentValue) * 100
                except:
                    transactionSubDict['allocation'] = 0
            else:
                transactionSubDict['allocation'] = 0

            if item.trxnDate and priceInst:
                try:
                    transactionSubDict['returnPerYear'] = ((float(
                        (priceInst.investorPrice) / (item.investMentPrice)) ** (
                                                                        1 / countYears(item.trxnDate))) - 1) * 100
                except:
                    transactionSubDict['returnPerYear'] = 0
            elif item.made_on and priceInst:
                try:
                    transactionSubDict['returnPerYear'] = ((float(
                        (priceInst.investorPrice) / (item.investMentPrice)) ** (
                                                                        1 / countYears(item.made_on))) - 1) * 100
                except:
                    transactionSubDict['returnPerYear'] = 0
            else:
                transactionSubDict['returnPerYear'] = 0

            transactionList.append(transactionSubDict)
            transactionSubDict = {}

    # print(weightAverageReturn)
    totalPL = totalCurrentValue - totalInvestmentValue
    try:
        totalAbsReturn = (totalCurrentValue / totalAmountWeight) * 100
    except:
        totalAbsReturn = 0
    portfolioUserDataDict['total_amount'] = totalAmountWeight
    portfolioUserDataDict['investment_value'] = totalInvestmentValue
    portfolioUserDataDict['current_value'] = totalCurrentValue
    portfolioUserDataDict['profile_or_loss'] = totalPL
    portfolioUserDataDict['absolute_return'] = totalAbsReturn
    portfolioUserDataDict['weightAverageReturnPerYear'] = weightAverageReturn
    portfolioUserDataDict['transactions'] = transactionList

    transactionList = []
    try:
        if userInst.profileOwnerIPD.name:
            portfolioUserDataDict["username"] = userInst.profileOwnerIPD.name
        elif userInst.first_name and userInst.last_name:
            portfolioUserDataDict["username"] = userInst.first_name+ " "+ userInst.last_name
        else:
            portfolioUserDataDict["username"] = None
        portfolioUserDataDict["id"] = userInst.profileOwnerIPD.id
        portfolioDict.append(portfolioUserDataDict)
    except:
        portfolioDict['None'] = portfolioUserDataDict

    #########################################################################
    ############ dicts for new add investor #################################

    #### to find allocation for userInst s ###
    totalPresentValueTemp = 0
    totalDivTemp = 0

    ##### to find allocation ######

    allTempUsers = tempUser.objects.filter(profileOwner=userInst)
    for item in allTempUsers:

        totalAmountWeight = totalInvestmentValue = totalCurrentValue = totalPL = totalAbsReturn = totalDiv = totalInvestmentPrice = weightAverageReturn = 0

        portfolioUserDataDict = {}
        tempUserTransaction = tempTransaction.objects.filter(made_by=item).order_by('-trxnDate')
        transactionList = []
        transactionSubDict = {}

        for subItem in tempUserTransaction:
            try:
                priceInst = buyPreIPOStockList.objects.filter(stockName=subItem.selected_stock).latest('publish')
            except:
                priceInst = None

            try:
                dividendInst = stockEssentials.objects.filter(stockProfileName=subItem.selected_stock).latest('publish')
            except:
                dividendInst = None

            if dividendInst:
                try:
                    totalDivTemp = totalDivTemp + (dividendInst.total_dividend * subItem.quantity)
                except:
                    totalDivTemp = 0

            if priceInst:
                try:
                    totalPresentValueTemp += subItem.quantity * priceInst.investorPrice
                except:
                    totalPresentValueTemp = 0
            else:
                totalPresentValueTemp = 0

            totalInvestmentPrice += subItem.investMentPrice

        for subItem in tempUserTransaction:

            try:
                priceInst = buyPreIPOStockList.objects.filter(stockName=subItem.selected_stock).latest('publish')
            except:
                priceInst = None

            try:
                dividendInst = stockEssentials.objects.filter(stockProfileName=subItem.selected_stock).latest('publish')
            except:
                dividendInst = None

            totalAmountWeight += subItem.amount
            investmentVal = subItem.quantity * subItem.investMentPrice
            if priceInst:
                try:
                    currentVal = subItem.quantity * priceInst.investorPrice
                except:
                    currentVal = 0
            else:
                currentVal = 0

            transactionProfitLoss = currentVal - investmentVal
            absoluteReturn = (currentVal / subItem.amount) * 100
            totalInvestmentValue += investmentVal
            totalCurrentValue += currentVal

            if priceInst:
                try:
                    profitLossPercent = (priceInst.investorPrice - subItem.investMentPrice) * 100
                except:
                    profitLossPercent = 0
            else:
                profitLossPercent = 0

            if priceInst:
                try:
                    weightAverageReturn += (subItem.investMentPrice / totalInvestmentPrice) * (
                                ((priceInst.investorPrice - subItem.investMentPrice) / subItem.investMentPrice) * 100)
                except:
                    weightAverageReturn = 0
            else:
                weightAverageReturn = 0

            transactionSubDict['paymentType'] = subItem.txn_made_by
            transactionSubDict['tempUserID'] = subItem.made_by.pk
            transactionSubDict['tempDataID'] = subItem.pk
            transactionSubDict['investment_value'] = investmentVal
            transactionSubDict['current_value'] = currentVal
            # transactionSubDict['profile_or_loss'] = transactionProfitLoss
            transactionSubDict['selected_stock'] = stockBasicDetailSerializer(subItem.selected_stock).data
            transactionSubDict['quantity'] = subItem.quantity
            transactionSubDict['amount'] = subItem.amount
            if subItem.demat:
                transactionSubDict['demat'] = stockBrokerDetailSerializer(subItem.demat).data
            else:
                transactionSubDict['demat'] = None
            try:
                transactionSubDict['made_on'] = subItem.made_on
            except:
                transactionSubDict['made_on'] = None
            transactionSubDict['trxnDate'] = subItem.trxnDate
            transactionSubDict['investMentPrice'] = subItem.investMentPrice
            if priceInst:
                transactionSubDict['stockPrice'] = priceInst.investorPrice
            else:
                transactionSubDict['stockPrice'] = 0

            transactionSubDict['dividend'] = subItem.total_dividend * subItem.quantity

            if priceInst:
                transactionSubDict['stockRating'] = priceInst.ratings
            else:
                transactionSubDict['stockRating'] = 0

            if priceInst:
                try:
                    transactionSubDict['profitLoss'] = (subItem.quantity * priceInst.investorPrice) - (
                                subItem.quantity * subItem.investMentPrice) + (
                                                                   subItem.total_dividend * subItem.quantity)
                except:
                    transactionSubDict['profitLoss'] = 0
            else:
                transactionSubDict['profitLoss'] = 0

            if priceInst:
                try:
                    # transactionSubDict['absoluteReturn']=(((subItem.investMentPrice)+(subItem.quantity * priceInst.investorPrice)-(subItem.quantity * subItem.investMentPrice)+subItem.total_dividend)/subItem.investMentPrice)*100
                    transactionSubDict['absoluteReturn'] = (priceInst.investorPrice + subItem.total_dividend) / (
                        subItem.investMentPrice) * 100
                except:
                    transactionSubDict['absoluteReturn'] = 0
            else:
                transactionSubDict['absoluteReturn'] = 0

            if priceInst:
                try:
                    transactionSubDict['allocation'] = ((
                                                                    subItem.quantity * priceInst.investorPrice) / totalPresentValueTemp) * 100
                except:
                    transactionSubDict['allocation'] = 0
            else:
                transactionSubDict['allocation'] = 0

            if subItem.trxnDate and priceInst:
                try:
                    transactionSubDict['returnPerYear'] = ((float(
                        (priceInst.investorPrice) / (subItem.investMentPrice)) ** (
                                                                        1 / countYears(subItem.trxnDate))) - 1) * 100
                except:
                    transactionSubDict['returnPerYear'] = 0
            else:
                transactionSubDict['returnPerYear'] = 0

            # transactionSubDict['made_by'] = subItem.made_by.name
            transactionList.append(transactionSubDict)
            transactionSubDict = {}

        totalPL = totalCurrentValue - totalInvestmentValue
        try:
            totalAbsReturn = (totalCurrentValue / totalAmountWeight) * 100
        except:
            totalAbsReturn = 0
        portfolioUserDataDict['total_amount'] = totalAmountWeight
        portfolioUserDataDict['investment_value'] = totalInvestmentValue
        portfolioUserDataDict['current_value'] = totalCurrentValue
        portfolioUserDataDict['profile_or_loss'] = totalPL
        portfolioUserDataDict['absolute_return'] = totalAbsReturn
        portfolioUserDataDict['weightAverageReturnPerYear'] = weightAverageReturn

        try:
            portfolioUserDataDict['totalReturnPerYear'] = ((
                                                                       totalCurrentValue - totalInvestmentValue / currentValue) ** (
                                                                       1 / 1)) - 1
        except:
            portfolioUserDataDict['totalReturnPerYear'] = 0

        portfolioUserDataDict['transactions'] = transactionList
        # portfolioUserDataDict['made_by'] = item.name
        transactionList = []
        portfolioUserDataDict['username'] = item.name
        portfolioUserDataDict['id'] = item.id
        portfolioDict.append(portfolioUserDataDict)

    ####### all Totals ########
    numberOfusers = len(portfolioDict)
    summationInvestedAmount = summationCurrentValue = summationProfitLoss = summationAbsoluteReturn = summationReturnPerYear = 0
    summationInvestedAmount = sum(d['investment_value'] for d in portfolioDict if d)
    summationCurrentValue = sum(d['current_value'] for d in portfolioDict if d)
    summationProfitLoss = sum(d['profile_or_loss'] for d in portfolioDict if d)
    try:
        summationAbsoluteReturn = summationCurrentValue / summationInvestedAmount * 100
    except:
        summationAbsoluteReturn = 0
    try:
        summationReturnPerYear = sum(
            d['weightAverageReturnPerYear'] for d in portfolioDict if d) / numberOfusers
    except:
        summationReturnPerYear = 0

    print(f'this is the count of all transaction {numberOfusers}')
    # print(f'this is sum of current value {summationCurrentValue}')
    # print(portfolioDict)
    context = {
        'userInst': userInst_detail,
        'portfolioDict': portfolioDict,
        'investorInst': investorInst_detail,
        'allTransactionsOfUserInst': allTransactionsOfUserInst_list,
        'stockBasicDetailInst': stockBasicDetailInst_list,
        'summationInvestedAmount': summationInvestedAmount,
        'summationCurrentValue': summationCurrentValue,
        'summationProfitLoss': summationProfitLoss,
        'summationAbsoluteReturn': summationAbsoluteReturn,
        'summationReturnPerYear': summationReturnPerYear
    }

    return Response(context)

@api_view(["GET"])
def getinvestorpotfolioUserStockView(request):
    try:
        userID = request.GET.get('userID')
    except:    
        userID = None
    try:
        userInst = User.objects.get(pk=request.user.id)  # 658
    except:
        userInst = None
    if userID == None:

        allTransactionsOfUserInst = Transaction.objects.filter(made_by=userInst).order_by('-made_on').order_by('-trxnDate')

        ######## Total Values ################
        totalAmountWeight = 0
        totalInvestmentValue = 0
        totalCurrentValue = 0
        totalPL = 0
        totalAbsReturn = 0
        totalDiv = 0

        portfolioDict = []
        portfolioUserDataDict = {}
        transactionSubDict = {}
        transactionList = []
        finalTransactionList = []

        #### to find allocation for userInst  ###
        totalPresentValue = totalDiv = totalInvestmentPrice = weightAverageReturn = 0
        totalDivident = 0

        for item in allTransactionsOfUserInst:
            try:
                priceInst = buyPreIPOStockList.objects.filter(stockName=item.selected_stock).latest('publish')
            except:
                priceInst = None
            try:
                dividendInst = stockEssentials.objects.filter(stockProfileName=item.selected_stock).latest('publish')
            except:
                dividendInst = None

            if item.pg_status == 'TXN_SUCCESS' or item.txn_made_by == 'Self':

                try:
                    totalDiv = totalDiv + (item.total_dividend * item.quantity)
                except:
                    totalDiv = 0

                if priceInst:
                    try:
                        totalPresentValue += item.quantity * priceInst.investorPrice
                    except:
                        totalPresentValue = 0
                else:
                    totalPresentValue = 0

                totalInvestmentPrice += item.investMentPrice

        transactioCount = currentVal = totalAmountWeight = investmentVal = totalInvestmentValue = totalCurrentValue = transactionProfitLoss = profitLossPercent = 0

        ##### values for particular stock #########################
        for item in allTransactionsOfUserInst:

            try:
                priceInst = buyPreIPOStockList.objects.filter(stockName=item.selected_stock).latest('publish')
            except:
                priceInst = None
            try:
                dividendInst = stockEssentials.objects.filter(stockProfileName=item.selected_stock).latest('publish')
            except:
                dividendInst = None

            if item.pg_status == 'TXN_SUCCESS' or item.txn_made_by == 'Self':

                totalAmountWeight += item.amount
                investmentVal = item.quantity * item.investMentPrice
                totalInvestmentValue += investmentVal

                if priceInst:
                    try:
                        currentVal = item.quantity * priceInst.investorPrice
                    except:
                        currentVal = 0
                else:
                    currentVal = 0
                totalCurrentValue += currentVal
                transactionProfitLoss = currentVal - investmentVal
                if priceInst:
                    try:
                        profitLossPercent = (priceInst.investorPrice - item.investMentPrice) * 100
                    except:
                        profitLossPercent = 0
                else:
                    profitLossPercent = 0

                if priceInst:
                    try:
                        weightAverageReturn += (item.investMentPrice / totalInvestmentPrice) * (
                                    ((priceInst.investorPrice - item.investMentPrice) / item.investMentPrice) * 100)
                    except:
                        weightAverageReturn = 0
                else:
                    weightAverageReturn = 0

                transactionSubDict['paymentType'] = item.txn_made_by
                transactionSubDict['investment_value'] = investmentVal
                transactionSubDict['current_value'] = currentVal
                transactionSubDict['amount'] = item.amount
                # transactionSubDict['profileLoss'] = transactionProfitLoss
                transactionSubDict['id'] = item.id
                transactionSubDict['selected_stock'] = stockBasicDetailSerializer(item.selected_stock).data
                transactionSubDict['quantity'] = item.quantity
                transactionSubDict['made_on'] = item.made_on
                transactionSubDict['trxnDate'] = item.trxnDate
                transactionSubDict['investMentPrice'] = item.investMentPrice
                if item.demat:
                    transactionSubDict['demat'] = stockBrokerDetailSerializer(item.demat).data
                else:
                    transactionSubDict['demat'] = None
                if priceInst:
                    transactionSubDict['stockPrice'] = priceInst.investorPrice
                else:
                    transactionSubDict['stockPrice'] = 0
                transactionSubDict['dividend'] = item.total_dividend * item.quantity

                if priceInst:
                    transactionSubDict['stockRating'] = priceInst.ratings
                else:
                    transactionSubDict['stockRating'] = 0

                if priceInst:
                    try:
                        transactionSubDict['profitLoss'] = (item.quantity * priceInst.investorPrice) - (
                                    item.quantity * item.investMentPrice) + (item.total_dividend * item.quantity)
                    except:
                        transactionSubDict['profitLoss'] = 0
                else:
                    transactionSubDict['profitLoss'] = 0

                if priceInst:
                    try:
                        # transactionSubDict['absoluteReturn']=(((item.investMentPrice)+(item.quantity * priceInst.investorPrice)-(item.quantity * item.investMentPrice)+item.total_dividend)/item.investMentPrice)*100
                        transactionSubDict['absoluteReturn'] = (priceInst.investorPrice + item.total_dividend) / (
                            item.investMentPrice) * 100
                    except:
                        transactionSubDict['absoluteReturn'] = 0
                else:
                    transactionSubDict['absoluteReturn'] = 0

                if priceInst:
                    try:
                        transactionSubDict['allocation'] = ((
                                                                        item.quantity * priceInst.investorPrice) / totalPresentValue) * 100
                    except:
                        transactionSubDict['allocation'] = 0
                else:
                    transactionSubDict['allocation'] = 0

                if item.trxnDate and priceInst:
                    try:
                        transactionSubDict['returnPerYear'] = ((float(
                            (priceInst.investorPrice) / (item.investMentPrice)) ** (
                                                                            1 / countYears(item.trxnDate))) - 1) * 100
                    except:
                        transactionSubDict['returnPerYear'] = 0
                elif item.made_on and priceInst:
                    try:
                        transactionSubDict['returnPerYear'] = ((float(
                            (priceInst.investorPrice) / (item.investMentPrice)) ** (
                                                                            1 / countYears(item.made_on))) - 1) * 100
                    except:
                        transactionSubDict['returnPerYear'] = 0
                else:
                    transactionSubDict['returnPerYear'] = 0

                transactionList.append(transactionSubDict)
                transactionSubDict = {}

        # print(weightAverageReturn)
        totalPL = totalCurrentValue - totalInvestmentValue
        try:
            totalAbsReturn = (totalCurrentValue / totalAmountWeight) * 100
        except:
            totalAbsReturn = 0
        try:
            if userInst.profileOwnerIPD.name:
                portfolioUserDataDict["username"] = userInst.profileOwnerIPD.name
            elif userInst.first_name and userInst.last_name:
                portfolioUserDataDict["username"] = userInst.first_name+ " "+ userInst.last_name
            else:
                portfolioUserDataDict["username"] = None
            portfolioUserDataDict["id"] = userInst.profileOwnerIPD.id
            portfolioDict.append(portfolioUserDataDict)
        except:
            portfolioDict['None'] = portfolioUserDataDict
        portfolioUserDataDict['transactions'] = transactionList
        finalTransactionList.append(transactionList)


        return Response(portfolioUserDataDict)
    elif userID != None:

        # transactionList = []

        #########################################################################
        ############ dicts for new add investor #################################

        #### to find allocation for userInst s ###
        totalPresentValueTemp = 0
        totalDivTemp = 0

        ##### to find allocation ######

        allTempUsers = tempUser.objects.filter(profileOwner=userInst)
        for item in allTempUsers:
            temp_portfolioUserDataDict = {}

            totalAmountWeight = totalInvestmentValue = totalCurrentValue = totalPL = totalAbsReturn = totalDiv = totalInvestmentPrice = weightAverageReturn = 0

            portfolioUserDataDict = {}
            tempUserTransaction = tempTransaction.objects.filter(made_by=item).order_by('-trxnDate')
            transactionList = []
            transactionSubDict = {}

            for subItem in tempUserTransaction:
                try:
                    priceInst = buyPreIPOStockList.objects.filter(stockName=subItem.selected_stock).latest('publish')
                except:
                    priceInst = None

                try:
                    dividendInst = stockEssentials.objects.filter(stockProfileName=subItem.selected_stock).latest('publish')
                except:
                    dividendInst = None

                if dividendInst:
                    try:
                        totalDivTemp = totalDivTemp + (dividendInst.total_dividend * subItem.quantity)
                    except:
                        totalDivTemp = 0

                if priceInst:
                    try:
                        totalPresentValueTemp += subItem.quantity * priceInst.investorPrice
                    except:
                        totalPresentValueTemp = 0
                else:
                    totalPresentValueTemp = 0

                totalInvestmentPrice += subItem.investMentPrice

            for subItem in tempUserTransaction:

                try:
                    priceInst = buyPreIPOStockList.objects.filter(stockName=subItem.selected_stock).latest('publish')
                except:
                    priceInst = None

                try:
                    dividendInst = stockEssentials.objects.filter(stockProfileName=subItem.selected_stock).latest('publish')
                except:
                    dividendInst = None

                totalAmountWeight += subItem.amount
                investmentVal = subItem.quantity * subItem.investMentPrice
                if priceInst:
                    try:
                        currentVal = subItem.quantity * priceInst.investorPrice
                    except:
                        currentVal = 0
                else:
                    currentVal = 0

                transactionProfitLoss = currentVal - investmentVal
                absoluteReturn = (currentVal / subItem.amount) * 100
                totalInvestmentValue += investmentVal
                totalCurrentValue += currentVal

                if priceInst:
                    try:
                        profitLossPercent = (priceInst.investorPrice - subItem.investMentPrice) * 100
                    except:
                        profitLossPercent = 0
                else:
                    profitLossPercent = 0

                if priceInst:
                    try:
                        weightAverageReturn += (subItem.investMentPrice / totalInvestmentPrice) * (
                                    ((priceInst.investorPrice - subItem.investMentPrice) / subItem.investMentPrice) * 100)
                    except:
                        weightAverageReturn = 0
                else:
                    weightAverageReturn = 0

                transactionSubDict['paymentType'] = subItem.txn_made_by
                transactionSubDict['tempUserID'] = subItem.made_by.pk
                transactionSubDict['tempDataID'] = subItem.pk
                transactionSubDict['investment_value'] = investmentVal
                transactionSubDict['current_value'] = currentVal
                # transactionSubDict['profile_or_loss'] = transactionProfitLoss
                transactionSubDict['selected_stock'] = stockBasicDetailSerializer(subItem.selected_stock).data
                transactionSubDict['quantity'] = subItem.quantity
                transactionSubDict['amount'] = subItem.amount
                if subItem.demat:
                    transactionSubDict['demat'] = stockBrokerDetailSerializer(subItem.demat).data
                else:
                    transactionSubDict['demat'] = None
                try:
                    transactionSubDict['made_on'] = subItem.made_on
                except:
                    transactionSubDict['made_on'] = None
                transactionSubDict['trxnDate'] = subItem.trxnDate
                transactionSubDict['investMentPrice'] = subItem.investMentPrice
                if priceInst:
                    transactionSubDict['stockPrice'] = priceInst.investorPrice
                else:
                    transactionSubDict['stockPrice'] = 0

                transactionSubDict['dividend'] = subItem.total_dividend * subItem.quantity

                if priceInst:
                    transactionSubDict['stockRating'] = priceInst.ratings
                else:
                    transactionSubDict['stockRating'] = 0

                if priceInst:
                    try:
                        transactionSubDict['profitLoss'] = (subItem.quantity * priceInst.investorPrice) - (
                                    subItem.quantity * subItem.investMentPrice) + (
                                                                    subItem.total_dividend * subItem.quantity)
                    except:
                        transactionSubDict['profitLoss'] = 0
                else:
                    transactionSubDict['profitLoss'] = 0

                if priceInst:
                    try:
                        # transactionSubDict['absoluteReturn']=(((subItem.investMentPrice)+(subItem.quantity * priceInst.investorPrice)-(subItem.quantity * subItem.investMentPrice)+subItem.total_dividend)/subItem.investMentPrice)*100
                        transactionSubDict['absoluteReturn'] = (priceInst.investorPrice + subItem.total_dividend) / (
                            subItem.investMentPrice) * 100
                    except:
                        transactionSubDict['absoluteReturn'] = 0
                else:
                    transactionSubDict['absoluteReturn'] = 0

                if priceInst:
                    try:
                        transactionSubDict['allocation'] = ((
                                                                        subItem.quantity * priceInst.investorPrice) / totalPresentValueTemp) * 100
                    except:
                        transactionSubDict['allocation'] = 0
                else:
                    transactionSubDict['allocation'] = 0

                if subItem.trxnDate and priceInst:
                    try:
                        transactionSubDict['returnPerYear'] = ((float(
                            (priceInst.investorPrice) / (subItem.investMentPrice)) ** (
                                                                            1 / countYears(subItem.trxnDate))) - 1) * 100
                    except:
                        transactionSubDict['returnPerYear'] = 0
                else:
                    transactionSubDict['returnPerYear'] = 0

                # transactionSubDict['made_by'] = subItem.made_by.name
                transactionList.append(transactionSubDict)
                transactionSubDict = {}

            totalPL = totalCurrentValue - totalInvestmentValue
            try:
                totalAbsReturn = (totalCurrentValue / totalAmountWeight) * 100
            except:
                totalAbsReturn = 0
            portfolioUserDataDict['total_amount'] = totalAmountWeight
            portfolioUserDataDict['investment_value'] = totalInvestmentValue
            portfolioUserDataDict['current_value'] = totalCurrentValue
            portfolioUserDataDict['profile_or_loss'] = totalPL
            portfolioUserDataDict['absolute_return'] = totalAbsReturn
            portfolioUserDataDict['weightAverageReturnPerYear'] = weightAverageReturn
            if int(userID) == item.id:
                temp_portfolioUserDataDict['total_amount'] = totalAmountWeight
                temp_portfolioUserDataDict['investment_value'] = totalInvestmentValue
                temp_portfolioUserDataDict['current_value'] = totalCurrentValue
                temp_portfolioUserDataDict['profile_or_loss'] = totalPL
                temp_portfolioUserDataDict['absolute_return'] = totalAbsReturn
                temp_portfolioUserDataDict['weightAverageReturnPerYear'] = weightAverageReturn      

            try:
                portfolioUserDataDict['totalReturnPerYear'] = ((
                                                                        totalCurrentValue - totalInvestmentValue / currentValue) ** (
                                                                        1 / 1)) - 1
                if int(userID) == item.id:
                    temp_portfolioUserDataDict['totalReturnPerYear'] = ((
                                                                        totalCurrentValue - totalInvestmentValue / currentValue) ** (
                                                                        1 / 1)) - 1      

            except:
                portfolioUserDataDict['totalReturnPerYear'] = 0
                if int(userID) == item.id:
                    temp_portfolioUserDataDict['totalReturnPerYear'] = 0
            # print(f"this is the userID{userID}")
            # print(f"this is the userID{item.id}")
            # print(int(userID) == item.id)
            if int(userID) == item.id:
                # print("statement is run now!!")
                temp_portfolioUserDataDict['username'] = item.name
                temp_portfolioUserDataDict['id'] = item.id
                temp_portfolioUserDataDict['transactions'] = transactionList
                # return Response({
                #     'portfolioDict': temp_portfolioUserDataDict,
                # })
                return Response(temp_portfolioUserDataDict)
            else:
                pass
        return Response({"msg": "Please send the correct user Id"})      
    return Response({"msg": "Please send the correct user Id or the request Type !"})    



class UserKycConfigAPIView(APIView):

    def get(self, request):
        resp = KycOrchestrator(request.user, request.user_role).fetch_kyc_config()
        status_code = status.HTTP_200_OK
        if resp.get('status') is False:
            status_code = status.HTTP_400_BAD_REQUEST
        return Response(resp, status=status_code)


class UserKycPageConfigAPIView(APIView):

    def get(self, request):
        step = request.GET.get('step')
        resp = KycOrchestrator(request.user, request.user_role).fetch_kyc_page_config(step)
        status_code = status.HTTP_200_OK
        if resp.get('status') is False:
            status_code = status.HTTP_400_BAD_REQUEST
        return Response(resp, status=status_code)


class UserKycUpdateAPIView(APIView):

    def post(self, request):
        step = request.GET.get('step')
        resp = KycOrchestrator(request.user, request.user_role).update_kyc_details(step, request.data)
        status_code = status.HTTP_200_OK
        if resp.get('status') is False:
            status_code = status.HTTP_400_BAD_REQUEST
        return Response(resp, status=status_code)

class UserKycDeleteAPIView(APIView):
    def delete(self, request, step, pk):
        resp = KycOrchestrator(request.user, request.user_role).delete_kyc_details(step, pk)
        status_code = status.HTTP_200_OK
        if resp.get('status') is False:
            status_code = status.HTTP_400_BAD_REQUEST
        return Response(resp, status=status_code)


class UserKycDocumentAPIView(APIView):

    def post(self, request):
        step = request.GET.get('step')
        resp = KycOrchestrator(request.user, request.user_role).upload_kyc_docs(step, request.FILES, request.data)
        status_code = status.HTTP_200_OK
        if resp.get('status') is False:
            status_code = status.HTTP_400_BAD_REQUEST
        return Response(resp, status=status_code)


class UserKycAPIView(APIView):

    def post(self, request):
        resp = KycOrchestrator(request.user, request.user_role).complete_kyc()
        status_code = status.HTTP_200_OK
        if resp.get('status') is False:
            status_code = status.HTTP_400_BAD_REQUEST
        return Response(resp, status=status_code)


class UserKycFieldOptionsAPIView(APIView):

    def get(self, request, field):
        data = request.GET
        resp = KycOrchestrator(request.user, request.user_role).fetch_field_options(field, data)
        status_code = status.HTTP_200_OK
        if resp.get('status') is False:
            status_code = status.HTTP_400_BAD_REQUEST
        return Response(resp, status=status_code)

@api_view(['GET'])
def getAllStockBrokerDetails(request):
    if request.method == "GET":
        stockBrokerDetailList = stockBrokerDetails.objects.all()
        serializedData = stockBrokerDetailSerializer(stockBrokerDetailList, many=True).data
        serializedData = list(serializedData)
        return Response(serializedData)
