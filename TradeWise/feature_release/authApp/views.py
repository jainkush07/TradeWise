from django.shortcuts import render, redirect, reverse, get_object_or_404, HttpResponse
from django.contrib.auth.models import User
from .models import *
from django.contrib import messages
from authApp.services.data_orchestrator import DataOrchestrator
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str
from django.http import JsonResponse
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.admin.views.decorators import staff_member_required
from authApp.services.dashboard_service import DashboardService
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.core.mail import EmailMessage
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.utils.safestring import mark_safe
from .forms import *
from planifyMain import whatsappTemp
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from authApp.services.otp_service import OtpOrchestrator
from django.conf import settings
from rest_framework.permissions import AllowAny
from authApp.services.user_service import UserService, SocialAuth
from rest_framework.views import APIView
from rest_framework.decorators import permission_classes
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework.authentication import TokenAuthentication
from rest_framework import generics
from .serializers import *
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from rest_framework.decorators import api_view
from authApp.decorators import staff_internal_login_required

# import pywhatkit
import requests
from whatsappAuthApp.models import whatsappLeads
from investorApp.models import verificationStatus, investorPersonalDetails
from employeeApp.models import country
from authApp.services.notification_service import NotificationMaster


#
def demo_view(request):
    ask_whatsapp_url = reverse('whatsappAuthApp:getNotificationUrl')
    # print(f'ask_whatsapp_url: {ask_whatsapp_url}')
    return HttpResponse('Success')


#
def loginInUserRedirect(request):
    if request.user.is_authenticated:
        return redirect('websiteApp:buypreIPOUrl')
    else:
        return redirect('authApp:loginUsernameHandlerUrl')


#
def loginTypeValidView(loginType):
    loginTypeValid = False
    allRolesList = []
    allRoles = roles.objects.all()
    for item in allRoles:
        if str(item.name) == str(loginType):
            loginTypeValid = True
    return loginTypeValid


#
def logoutView(request):
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect("websiteApp:homePageUrl")


# root auth URL
def loginAsView(request):
    if request.user.is_authenticated:
        return loginInUserRedirect(request)
    context = {}
    return render(request, 'authApp/UI/chooseLogin.html', context)


#
def loginUsernameHandlerView(request):
    if request.user.is_authenticated:
        return loginInUserRedirect(request)
    loginType = request.GET.get('type')
    loginTypeValid = loginTypeValidView(loginType)
    if not loginType or not loginTypeValid:
        messages.error(request, 'Invalid Login Request. Kindly Select a valid Profile Type to Login.')
        return redirect('authApp:loginAsUrl')
    else:
        request.session['loginType'] = loginType
        try:
            sideMenuObj = loginBannerObjects.objects.get(relatedTo__name=loginType)
        except:
            sideMenuObj = None
        loginBannerObjectsInstForm = loginBannerObjectsForm(instance=sideMenuObj)

    countryList = country.objects.all()
    context = {
        'sideMenuObj': sideMenuObj,
        'loginBannerObjectsInstForm': loginBannerObjectsInstForm,
        'countryList': countryList,
    }
    return render(request, 'authApp/UI/login1.html', context)


#
def checkUserAndProfiles(emailID):
    userProfile = None
    if emailID:
        if User.objects.filter(email=emailID).exists():
            userProfile = User.objects.get(email=emailID)
        elif User.objects.filter(username=emailID).exists():
            userProfile = User.objects.get(username=emailID)
    return userProfile


#
def activationMailGeneratorView(request, user, to_email, userAction=None, loginType=None):
    try:
        current_site = get_current_site(request)
        if loginType:
            mail_subject = f'Activate your Planify {loginType} account.'
        else:
            mail_subject = f'Activate your Planify Account.'
        message = render_to_string('authApp/mails/activateAccountEmail.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
            'type': loginType,
            'action': userAction,

        })
        # to_email = request.POST.get('enteredEmail')
        email = EmailMessage(
            subject=mail_subject,
            body=message,
            from_email='reports@planify.in',
            to=[to_email]
        )
        email.send()
        function_completed = True
    except:
        function_completed = False
    return function_completed


#
def loginSignUpSubmitHandlerView(request):
    if request.method == 'POST':
        empLogin = False
        redirectTo = request.POST.get('requestFrom')
        loginType = request.POST.get('loginType')
        emailID = request.POST.get('enteredEmail')
        # loginType = request.POST.get('action')
        domain = emailID.split('@')[1]
        domain_list = ["planify.in", ]
        if domain in domain_list:
            empLogin = True
        if not empLogin and loginType == 'EMPLOYEE':
            messages.error(request, 'Restricted Access for Planify Employees Only!')
            return redirect(redirectTo)
        elif loginType != 'EMPLOYEE' and empLogin:
            messages.error(request, 'It is not allowed for an Planify Employee to Register as some Different Profile!')
            return redirect(redirectTo)
        profileInst = checkUserAndProfiles(emailID)
        if profileInst:
            profile_active = profileInst.is_active
            profile_has_pass = profileInst.has_usable_password
        else:
            profile_active = None
            profile_has_pass = None
        if profileInst and profile_active and profile_has_pass:
            returnURL = reverse('authApp:loginPasswordHandlerUrl')
            returnURL += '?profile=' + emailID
            if empLogin:
                returnURL += '&type=EMPLOYEE'
            else:
                returnURL += '&type=' + loginType
            return redirect(returnURL)
        elif profileInst and not profileInst.is_active and empLogin == False:
            link = reverse("authApp:emailVerifyTokenRegeneratorUrl")
            link += '?type=' + loginType
            redirectTo += '&popup=error'
        # messages.warning(request, mark_safe(
        # 	f'Account Disabled, Not Activated or password Yet. Contact Support or Regenerate Activation Mail by <a href="{link}">Clicking Here</a>.'))
        else:
            if empLogin:
                messages.error(request,
                               'Please contact HR or Internal Support Team if facing any error while logging in.')
            else:
                try:
                    user = User.objects.create(
                        username=request.POST.get('enteredEmail'),
                        email=request.POST.get('enteredEmail'),
                        is_active=False
                    )
                    user.set_unusable_password()
                except:
                    messages.error(request, 'Error while creating User')
                    return redirect(redirectTo)
                function_completed = activationMailGeneratorView(request, user, emailID, loginType=loginType)
                roleForUser = roles.objects.get(name=loginType)
                roleOfUser = userRoles(profile_owner=user)
                user.save()
                roleOfUser.save()
                roleOfUser.profile_roles.add(roleForUser)
                if function_completed:
                    redirectTo += '&popup=success'
                # messages.warning(request,
                # f"To verify your email, we've sent a verification link to {emailID}. Please check your updates Promotions/Spam folder in case you don’t find our email in your inbox.")
                else:
                    redirectTo += '&popup=error'
                # messages.error(request,
                # 			   f"Your account got created but we are not able to generate Account Activation Email right now. Kindly try resetting and creating new password for your Account!")
        return redirect(redirectTo)
    return HttpResponse('Invalid Entry Point!')


def check_email_whatsapp_verification_status(userInst):
    whatsappVerified = emailVerified = False
    try:
        if userInst.profileOwnerWL.verified == True:
            whatsappVerified = True
    except:
        pass
    try:
        if userInst.profileOwnerIPD.emailVerified == True:
            emailVerified = True
    except:
        pass
    return whatsappVerified, emailVerified


#
@login_required
def createUsablePasswordView(request):
    loginType = request.POST.get('loginType') or request.GET.get('type') or request.session['loginType']
    if request.method == 'POST':
        userInst = User.objects.get(pk=request.user.pk)
        pass1 = request.POST.get('password')
        pass2 = request.POST.get('confirm_password')

        referredID = request.POST.get('referralID')
        if pass1 != pass2:
            messages.error(request, 'Password Mismatched. Kindly Enter same password both times.')
        else:
            userInst.set_password(pass1)
            # userInst.is_active = True
            userInst.save()
            if referredID:
                profileUser = userRoles.objects.get(profile_owner=userInst)
                profileUser.referred_by_id = referredID
                try:
                    referrer_profile = userRoles.objects.get(profile_username=referredID)
                    profileUser.referred_by_user = referrer_profile.profile_owner
                except:
                    pass
                profileUser.save()
            passwordCreateMsg = "Password Created Successfully."
            passwordUpdateMsg = "Password Updated Successfully."
            messages.success(request, passwordCreateMsg)
            login(request, userInst, backend='django.contrib.auth.backends.ModelBackend')
            whatsappVerified, emailVerified = check_email_whatsapp_verification_status(userInst)
            if not whatsappVerified and emailVerified:
                ask_whatsapp_url = reverse('whatsappAuthApp:getNotificationUrl')
                if loginType:
                    ask_whatsapp_url += "?type=" + str(loginType)
                return redirect(ask_whatsapp_url)
            elif whatsappVerified and not emailVerified:
                ask_email_url = reverse('authApp:get_email_verified_url')
                if loginType:
                    ask_email_url += "?type=" + str(loginType)
                return redirect(ask_email_url)
            elif whatsappVerified and emailVerified:
                return redirect('websiteApp:startupPageUrl')

    try:
        sideMenuObj = loginBannerObjects.objects.get(relatedTo__name=loginType)
    except:
        sideMenuObj = None
    context = {
        'sideMenuObj': sideMenuObj
    }
    return render(request, 'authApp/UI/resetOrCreatePassword.html', context)


#
def get_email_verified_view(request):
    get_verified_page = True
    unverified_mail = None
    try:
        if not request.user.profileOwnerIPD.emailVerified:
            unverified_mail = request.user.email
    except:
        pass
    try:
        sideMenuObj = loginBannerObjects.objects.get(relatedTo__name=request.session['loginType'])
    except:
        sideMenuObj = None
    userRolesInst = userRoles.objects.get(profile_owner=request.user)
    staticLoginType = None
    for item in userRolesInst.profile_roles.all():
        staticLoginType = item
        break

    loginType = request.GET.get('type')
    # userType = request.POST.get('profile')
    # username = request.POST.get('username')
    # print(loginType)
    request.session['loginType'] = loginType
    try:
        sideMenuObj = loginBannerObjects.objects.get(relatedTo__name=loginType)
    except:
        sideMenuObj = None
    loginBannerObjectsInstForm = loginBannerObjectsForm(instance=sideMenuObj)

    context = {
        'get_verified_page': get_verified_page,
        'unverified_mail': unverified_mail,
        'sideMenuObj': sideMenuObj,
        'staticLoginType': staticLoginType,
        'sideMenuObj': sideMenuObj,
    }
    return render(request, 'authApp/UI/get_email_verified.html', context)


#
def get_email_verified_submit_view(request):
    if request.POST:
        # redirectTo = request.POST.get('redirectTo')
        loginType = request.POST.get('loginType')
        actionType = request.POST.get('action')
        emailID = request.POST.get('emailID')
        staticType = request.POST.get('staticType')
        if not loginType:
            loginType = staticType
        if User.objects.filter(email=emailID).exists() or User.objects.filter(username=emailID).exists():
            messages.error(request, 'Email Address Linked with Some Other Account!')
            ask_email_url = reverse('authApp:get_email_verified_url')
            if loginType:
                ask_email_url += "?type=" + str(loginType)
            return redirect(ask_email_url)
        else:
            # try:
            userInst = User.objects.get(pk=request.user.pk)
            userInst.email = emailID
            userInst.save()
            # except:
            # messages.error(request, 'Error Occured while saving your mail id, Kindly Retry!')
            # try:
            function_completed = activationMailGeneratorView(request, userInst, emailID, userAction='everify',
                                                             loginType=loginType)
            if function_completed:
                messages.warning(request,
                                 f"To verify your email, we've sent a verification link to {emailID}. Please check your updates Promotions/Spam folder in case you don’t find our email in your inbox.")
            else:
                messages.error(request,
                               f"Your account got created but we are not able to generate Account Activation Email right now. Kindly try resetting and creating new password for your Account!")
        return redirect("websiteApp:buypreIPOUrl")
    return HttpResponse('Invalid Entry Point!')


#
def accountActivationView(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    userType = request.GET.get('type')
    userAction = request.GET.get('action')
    createUsablePassLink = reverse('authApp:createUsablePasswordUrl')
    createUsablePassLink += '?type=' + userType
    # print(f'userType: {userType}')
    # print(f'userAction: {userAction}')
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        # print('User Activated')
        try:
            createInvestorPersonalDetails = investorPersonalDetails(profileOwner=user)
            if user.username == user.email or userAction == 'app_login_email_verify':
                createInvestorPersonalDetails.emailVerified = True
            createInvestorPersonalDetails.save()
            createVerificationStatus = verificationStatus(profileOwner=user)
            createVerificationStatus.save()
        # print('createInvestorPersonalDetails & createVerificationStatus DONE')
        except:
            # print('createInvestorPersonalDetails & createVerificationStatus NOT DONE')
            pass
        if userAction not in ['app_login_email_verify', 'app_login_whatsapp_verify']:
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        try:
            username_user = int(user.username)
        except:
            username_user = user.username
        # print(f'username_user: {username_user}')
        #########
        if userAction in ['noverify', 'app_login_whatsapp_verify', ]:
            whatsApp_inst = whatsappLeads.objects.get(profileOwner=user)
            whatsApp_inst.verified = True
            whatsApp_inst.save()
            messages.success(request, 'Your Whatsapp Number has been Verfied and is enabled for Notifications.')
            if userAction == 'app_login_whatsapp_verify':
                return render(request, 'authApp/UI/device_app_wa_verification.html', {})
            # print(f'WhatsApp Verified in noverify!')
            return redirect('websiteApp:startupPageUrl')
        elif userAction in ['everify', 'app_login_email_verify', ]:
            personalInst = investorPersonalDetails.objects.get(profileOwner=user)
            personalInst.emailVerified = True
            personalInst.save()
            messages.success(request, 'Your Email Address has been Verified Successfully.')
            if userAction == 'app_login_email_verify':
                return render(request, 'authApp/UI/device_app_email_verification.html', {})
            # print(f'Email Verified in everify!')
            return redirect('websiteApp:startupPageUrl')
        elif not user.has_usable_password() and (not user.email and type(username_user) == int):
            whatsApp_inst = whatsappLeads.objects.get(profileOwner=user)
            whatsApp_inst.verified = True
            whatsApp_inst.save()
            messages.success(request,
                             'Your Whatsapp Number has been Verfied and is enabled for Notifications. Kindly Create password for future Login.')
            # print(f'WhatsApp Verified & Create Password Prompted!')
            return redirect(createUsablePassLink)
        # elif user.has_usable_password() and userAction == 'everify':
        # 	personalInst = investorPersonalDetails.objects.get(profileOwner=user)
        # 	personalInst.emailVerified = True
        # 	personalInst.save()
        # 	messages.success(request, 'Your Email Address has been verified successfully.')
        # 	return redirect('websiteApp:startupPageUrl')
        # elif userAction == 'app_login_email_verify':
        # 	return render(request, 'authApp/UI/device_app_email_verification.html', {})
        elif user.has_usable_password() and not userAction == 'reset':
            return redirect('websiteApp:startupPageUrl')
        else:
            # print(f'Every Condition Failed!')
            return redirect(createUsablePassLink)
    #########

    # if not user.has_usable_password() and (not user.email and type(username_user) == int):
    # 	whatsApp_inst = whatsappLeads.objects.get(profileOwner=user)
    # 	whatsApp_inst.verified = True
    # 	whatsApp_inst.save()
    # 	messages.success(request, 'Your no. has been verified successfully.')
    # 	return redirect(createUsablePassLink)
    # elif user.has_usable_password() and userAction in ['noverify', 'app_login_whatsapp_verify']:
    # 	whatsApp_inst = whatsappLeads.objects.get(profileOwner=user)
    # 	whatsApp_inst.verified = True
    # 	whatsApp_inst.save()
    # 	messages.success(request, 'Your no. has been verified successfully.')
    # 	if userAction == 'app_login_email_verify':
    # 		return render(request, 'authApp/UI/device_app_wa_verification.html', {})
    # 	return redirect('websiteApp:startupPageUrl')
    # elif user.has_usable_password() and userAction == 'everify':
    # 	personalInst = investorPersonalDetails.objects.get(profileOwner=user)
    # 	# whatsApp_inst = whatsappLeads.objects.get(profileOwner=user)
    # 	personalInst.emailVerified = True
    # 	personalInst.save()
    # 	messages.success(request, 'Your Email Address has been verified successfully.')
    # 	return redirect('websiteApp:startupPageUrl')
    # elif userAction == 'app_login_email_verify':
    # 	return render(request, 'authApp/UI/device_app_email_verification.html', {})
    # elif user.has_usable_password() and not userAction == 'reset':
    # 	return redirect('websiteApp:startupPageUrl')
    # else:
    # 	return redirect(createUsablePassLink)

    elif request.user.is_authenticated and not request.user.has_usable_password():
        messages.warning(request, 'Activation link is invalid! Either it Expired or Already used.')
        return redirect(createUsablePassLink)
    else:
        return HttpResponse('Activation link is invalid! Either it Expired or Already used.')


#
def social_login_view(request):
    loginType = request.GET.get('loginType') or request.session['loginType']
    try:
        userInst = User.objects.get(pk=request.user.pk)
        uname = userInst.username
    except:
        userInst = None
    if userInst:
        empLogin = False
        try:
            user_mail_domain = uname.split('@')[1]
            if user_mail_domain == 'planify.in':
                messages.error(request, 'You can not use Planify ID to Signup.')
                redirectUrl = reverse('authApp:loginUsernameHandlerUrl')
                redirectUrl += '?type=' + loginType
                userInst.delete()
                if "loginType" in request.session:
                    del request.session['loginType']
                return redirect(redirectUrl)
        except:
            pass
        redirectUrl = reverse('websiteApp:startupPageUrl')
        roleForUser = roles.objects.get(name=loginType)
        roleOfUser, created = userRoles.objects.get_or_create(profile_owner=userInst)
        if created:
            roleOfUser.save()
            roleOfUser.profile_roles.add(roleForUser)
            redirectUrl = reverse('whatsappAuthApp:getNotificationUrl')
            redirectUrl += "?onboarding=true"
            redirectUrl += "&type=" + loginType
            request.session['onboarding'] = 'true'
        try:
            if loginType == 'INVESTOR':
                createInvestorPersonalDetails = investorPersonalDetails(profileOwner=userInst)
                createInvestorPersonalDetails.emailVerified = True
                createInvestorPersonalDetails.save()
                createVerificationStatus = verificationStatus(profileOwner=userInst)
                createVerificationStatus.save()
        except:
            pass
        request.session['loginType'] = loginType
        # if userInst and created:
        # 	return redirect('authApp:createUsablePasswordUrl')
        # else:
        return redirect(redirectUrl)
    else:
        return HttpResponse(
            f'No Response from your Google Account, This triggered System Failure. Kindly Go Back & Try Again Later or Signup Manually.')
    return HttpResponse(f'Hello {loginType}, An error occured. Kindly Try Again.')


#
def loginBannerObjectsView(request):
    if request.method == 'POST':
        methodType = request.POST.get('submitType')
        redirectTo = request.POST.get('requestFrom')
        pkID = request.POST.get('dataID')
        if methodType == 'new':
            objlnst = None
        else:
            objlnst = get_object_or_404(loginBannerObjects, pk=pkID)
        objForm = loginBannerObjectsForm(request.POST, request.FILES, instance=objlnst)
        if objForm.is_valid():
            cd = objForm.save(commit=False)
            cd.save()
            cd.refresh_from_db()
            messages.success(request, 'Data sent for verification')
        else:
            messages.error(request, f'Please check following errors: {objForm.errors}')
        return redirect(redirectTo)
    return HttpResponse('Invalid Entry')


def checkUserAndProfilesSec(phoneNumber):
    userProfile = None
    if phoneNumber:
        if User.objects.filter(username=phoneNumber).exists():
            userProfile = User.objects.get(username=phoneNumber)
    return userProfile


#
@login_required
def profileRoutingView(request):
    return render(request, 'authApp/UI/profileRouting.html')


def whatsappRedirect(request, loggedInType):
    try:
        userInstLoggedIn = User.objects.get(pk=request.user.pk)
        userInst = whatsappLeads.objects.get(profileOwner=userInstLoggedIn)
    except:
        userInst = None

    if userInst:
        if userInst.phoneNumber:
            return redirect('websiteApp:buypreIPOUrl')
        else:
            whatsappLink = reverse('whatsappAuthApp:getNotificationUrl')
            whatsappLink += '?profile=' + str(loggedInType)

            whatsappLink += '&type=' + str(loggedInType)
            return redirect(whatsappLink)
    else:
        whatsappLink = reverse('whatsappAuthApp:getNotificationUrl')
        whatsappLink += '?profile=' + str(loggedInType)
        whatsappLink += '&type=' + str(loggedInType)
        return redirect(whatsappLink)


#
def userLoginHandleView(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        loginType = request.POST.get('profile')
        loggedInType = request.POST.get('loginType')

        user = authenticate(request, username=username, password=password)

        if user is None:
            User = get_user_model()
            user_queryset = User.objects.all().filter(email__iexact=username)
            if user_queryset:
                username = user_queryset[0].username
                user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
            else:
                link = reverse("authApp:emailVerifyTokenRegeneratorUrl")
                link += '?type=' + loginType
                return HttpResponse(mark_safe(
                    f'Account Disabled or Not Activated Yet. Contact Support or Regenerate Activation Mail by <a href="{link}">Clicking Here</a>.'))
            # print('hello')
            # if not loggedInType == 'EMPLOYEE':
            if not request.user.email:
                if not loggedInType == 'EMPLOYEE':
                    # print("this is running")
                    emailLink = reverse("authApp:getEmailUrl")
                    emailLink += '?profile=' + loginType + '&type=' + loggedInType
                    return redirect(emailLink)
                else:
                    return redirect('websiteApp:buypreIPOUrl')
            else:
                if not loggedInType == 'EMPLOYEE':
                    return whatsappRedirect(request, loggedInType)
                else:
                    return redirect('websiteApp:buypreIPOUrl')
        # return redirect('authApp:loginUsernameHandlerUrl')
        else:
            messages.error(request, 'Invalid Login Credentials, Please Try Again or Contact Support if error persists.')
            errorRedirect = reverse('authApp:loginUsernameHandlerUrl')
            errorRedirect += '?type=' + loggedInType
            return redirect(errorRedirect)
    return HttpResponse('Invalid Entry Points!')


def userLoginHandleWhatsappView(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        loginType = request.POST.get('profile')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
            else:
                link = reverse("authApp:emailVerifyTokenRegeneratorUrl")
                link += '?type=' + loginType
                return HttpResponse(mark_safe(
                    f'Account Disabled or Not Activated Yet. Contact Support or Regenerate Activation Mail by <a href="{link}">Clicking Here</a>.'))

            return redirect('websiteApp:buypreIPOUrl')
        else:
            messages.error(request, 'Invalid Login Credentials, Please Try Again or Contact Support.')
            errorRedirect = reverse('authApp:loginUsernameHandlerUrl')
            errorRedirect += '?type=' + loginType
            return redirect(errorRedirect)
    return HttpResponse('Invalid Entry Point!')


def whatsAppApiView(request, phoneNumber):
    payload = {"phoneNumber": str(phoneNumber), "countryCode": "+91", "tags": ["new users"]}
    r = requests.post('https://api.interakt.ai/v1/public/track/users/',
                      headers={'Accept': 'application/json', 'Content-Type': 'application/json',
                               'Authorization': 'Basic UXlhZXpxLThCYkU5RnhGMVNqTmRLWEktRm1qallxeWo1R1ZqYm9iUVFuUTo='},
                      json=payload)
    # print(r.status_code)
    return r.status_code


#
def activationMessageGeneratorView(request, user, phoneNumber, userAction=None, loginType=None, countryCode=None):
    current_site = get_current_site(request)
    # reset = reverse('authApp:createUsablePasswordUrl')
    # action = createUsablePasswordView
    # print(f'this is country code {countryCode}')
    convCountryCode = "+" + str(countryCode)
    # print(f'this is string converted countryCode {convCountryCode}')
    if loginType:
        mail_subject = f'Activate your Planify {loginType} account.'
    else:
        mail_subject = f'Activate your Planify Account.'

    status_code = whatsAppApiView(request, phoneNumber)

    message = {
        'user': user,
        'domain': current_site.domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
        'type': loginType,
        'action': userAction,
    }

    template_var = ""
    if not settings.SERVER_NAME_FOR_EMAIL == 'Testing Server Website ':
        template_var = whatsappTemp.WHATSAPP_RESET_PASSWORD_PROD
    else:
        template_var = whatsappTemp.WHATSAPP_RESET_PASSWORD

    # print(message['uid'])
    # print(message['token'])
    # print(message['type'])
    # print(message['action'])
    if (status_code == 202 or status == 200 or status == 201):
        authUrl = 'auth/activate/' + message['uid'] + '/' + message['token'] + '/?type=' + message['type']
        # print(type(message['action']))
        if message['action']:
            authUrl += '&action=' + message['action']
        else:
            authUrl = authUrl
        payload = {
            "countryCode": convCountryCode,
            "phoneNumber": str(phoneNumber),
            "type": "Template",
            "template": {
                "name": template_var,
                "languageCode": "en",
                "bodyValues": [
                    str(loginType)
                ],
                "buttonValues": {
                    "0": [authUrl]
                }
            }
        }
        res = requests.post('https://api.interakt.ai/v1/public/message/',
                            headers={'Accept': 'application/json', 'Content-Type': 'application/json',
                                     'Authorization': 'Basic UXlhZXpxLThCYkU5RnhGMVNqTmRLWEktRm1qallxeWo1R1ZqYm9iUVFuUTo='},
                            json=payload)
    else:
        messages.error(request, 'please check an error occurred.')

    # print("status_code")
    # print(res.status_code)

    return True


#
def emailVerifyTokenRegeneratorView(request):
    if request.method == 'POST':
        emailID = request.POST.get('username')
        userType = request.POST.get('profile')
        actionType = request.POST.get('action')
        user = checkUserAndProfiles(emailID)
        if user:
            activationMailGeneratorView(request, user, emailID, actionType, userType)
            messages.success(request, "We have sent you Email to Proceed Further.")
        else:
            link = reverse("authApp:loginUsernameHandlerUrl")
            messages.error(request, mark_safe(
                f'No account exists with the provided email Address. Please recheck or Signup by <a href="{link}">Clicking Here</a>.'))
    context = {}
    return render(request, 'authApp/UI/resetPassword.html', context)


def whatsappVerifyTokenRegeneratorView(request):
    if request.method == 'POST':
        phoneNumber = request.POST.get('username')
        userType = request.POST.get('profile')
        actionType = request.POST.get('action')
        # print(actionType)
        user = checkUserAndProfilesSec(phoneNumber)
        if user:
            activationMessageGeneratorView(request, user, phoneNumber, actionType, userType)
            messages.success(request, "We have sent you message to Proceed Further.")
        else:
            link = reverse("authApp:loginUsernameHandlerUrl")
            messages.error(request, mark_safe(
                f'No account exists with the provided whatsapp number. Please recheck or Signup by <a href="{link}">Clicking Here</a>.'))
    context = {}
    return render(request, 'authApp/UI/whatsappResetPassword.html', context)


#
def getEmailSubmitView(request):
    if request.method == 'POST':
        empLogin = False
        redirectTo = request.POST.get('requestFrom')
        loginType = request.POST.get('loginType')
        emailID = request.POST.get('enteredEmail')
        domain = emailID.split('@')[1]
        domain_list = ["planify.in", ]
        # print(f'logintype{loginType}')
        if domain in domain_list:
            empLogin = True
        if not empLogin and loginType == 'EMPLOYEE':
            messages.error(request, 'Restricted Access for Planify Employees Only!')
            return redirect('authApp:loginUsernameHandlerUrl')
        elif loginType != 'EMPLOYEE' and empLogin:
            messages.error(request, 'It is not allowed for an Planify Employee to Register as some Different Profile!')
            return redirect('authApp:loginUsernameHandlerUrl')
        profileInst = checkUserAndProfiles(emailID)
        if User.objects.filter(email=emailID).exists():
            messages.error(request, 'Email Id is Already exists')
            return redirect(redirectTo)
        else:
            userInst = User.objects.get(pk=request.user.pk)
            userInst.email = emailID
            userInst.save()
            # emailVerifyTokenRegeneratorView()
            activationMailGeneratorView(request, userInst, emailID, loginType)
            return redirect("websiteApp:buypreIPOUrl")
    # print(f'this is userInst emailID {userInst}')

    # loggedInUserInst = User.objects.get(username=request.user.username)
    # loggedInUserInst.email = emailID
    # loggedInUserInst.save()

    return HttpResponse('Invalid Entry')


# for whatsapp
def loginSignUpSubmitHandlerWhatsappView(request):
    if request.method == 'POST':
        empLogin = False
        redirectTo = request.POST.get('requestFrom')
        loginType = request.POST.get('loginType')
        # emailID = request.POST.get('enteredEmail')
        phoneNumber = request.POST.get('phoneNumber')
        countryCode = request.POST.get('countryCode')
        # print(f'this is country code ------ {countryCode}')
        # domain = emailID.split('@')[1]
        # domain_list = ["planify.in",]
        # print("hello")
        # if domain in domain_list:
        #   empLogin = True
        # loginUsing = request.POST.get('loginUsing')
        # print(loginAstype)
        if not empLogin and loginType == 'EMPLOYEE':
            messages.error(request, 'Restricted Access for Planify Employees Only!')
            return redirect('authApp:loginUsernameHandlerUrl')
        elif loginType != 'EMPLOYEE' and empLogin:
            messages.error(request, 'It is not allowed for an Planify Employee to Register as some Different Profile!')
            return redirect('authApp:loginUsernameHandlerUrl')
        profileInst = checkUserAndProfilesSec(phoneNumber)
        # print(profileInst)
        if profileInst:
            profile_active = profileInst.is_active
            profile_has_pass = profileInst.has_usable_password
        else:
            profile_active = None
            profile_has_pass = None
        # print('pass',profile_has_pass)
        # print(profile_active)
        if profileInst and profile_active and profile_has_pass:
            returnURL = reverse('authApp:loginPasswordHandlerUrl')
            returnURL += '?profile=' + phoneNumber
            if empLogin:
                returnURL += '&type=EMPLOYEE'
            else:
                returnURL += '&type=' + loginType

            return redirect(returnURL)
        elif profileInst and not profileInst.is_active:
            link = reverse("authApp:whatsappVerifyTokenRegeneratorUrl")
            link += '?type=' + loginType

            redirectTo += '?popup=whatsappError'
        # messages.warning(request, mark_safe(
        # 	f'Account Disabled, Not Activated or password Yet. Contact Support or Regenerate Activation Message by <a href="{link}">Clicking Here</a>.'))
        else:
            if empLogin:
                messages.error(request,
                               'Please contact HR or Internal Support Team if facing any error while logging in.')
            else:
                try:
                    user = User.objects.create(
                        username=request.POST.get('phoneNumber'),
                        # email=request.POST.get('enteredEmail'),
                        is_active=False
                    )
                    user.set_unusable_password()
                except:
                    messages.error(request, 'Error while creating User')
                    return redirect('authApp:loginUsernameHandlerUrl')
            function_completed = activationMessageGeneratorView(request, user, phoneNumber, loginType=loginType,
                                                                countryCode=countryCode)
            roleForUser = roles.objects.get(name=loginType)
            roleOfUser = userRoles(profile_owner=user)
            whatsAppUser = whatsappLeads.objects.create(profileOwner=user, phoneNumber=phoneNumber, countryCode='+91')
            user.save()
            roleOfUser.save()
            whatsAppUser.save()
            roleOfUser.profile_roles.add(roleForUser)
            if function_completed:
                redirectTo += '&popup=whatsappSuccess'
            else:
                redirectTo += '&popup=whatsappError'
        # messages.warning(request, f"To verify your WhatsApp, we've sent a verification link to {phoneNumber}.")
        return redirect(redirectTo)
    return HttpResponse('Invalid Entry Point!')


#
def getEmailView(request):
    loginType = request.GET.get('loginType')
    # userType = request.POST.get('profile')
    # username = request.POST.get('username')

    try:
        sideMenuObj = loginBannerObjects.objects.get(relatedTo__name=loginType)
    except:
        sideMenuObj = None
    loginBannerObjectsInstForm = loginBannerObjectsForm(instance=sideMenuObj)

    loginType = request.GET.get('type')
    # userType = request.POST.get('profile')
    # username = request.POST.get('username')
    # print(loginType)
    request.session['loginType'] = loginType
    try:
        sideMenuObj = loginBannerObjects.objects.get(relatedTo__name=loginType)
    except:
        sideMenuObj = None
    loginBannerObjectsInstForm = loginBannerObjectsForm(instance=sideMenuObj)

    context = {
        'sideMenuObj': sideMenuObj,
    }

    return render(request, 'authApp/UI/getEmail.html', context)


class LoginAPIView(APIView):
    serializer = LoginSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        # try:
        serializer = self.serializer(data=request.data)
        login_type = request.GET.get('loginType')
        if serializer.is_valid(raise_exception=True):
            email = serializer.data.get('email')
            mobile_num = serializer.data.get('phoneNumber')
            if email:
                user_data = User.objects.filter(email=email).values('username').last()
                user_name = user_data.get('username') if user_data else None
            else:
                user_name = mobile_num
            password = serializer.data.get('password')

            if user_name:
                user = authenticate(username=user_name, password=password)
                if user and user.id:
                    user_service = UserService()
                    role_validation = user_service.validate_role(user, login_type)
                    if role_validation == 2 or not login_type:
                        return Response({"status": False, "message": "You are not allowed to login with this role"},
                                        status=status.HTTP_400_BAD_REQUEST)
                    elif role_validation == 0:
                        user_service.add_user_role(user, login_type)
                    data = user_service.get_login_creds(user, login_type)
                    return Response({'data': data, 'status': True})

        return Response({"status": False, "message": "please check your credentials"},
                        status=status.HTTP_400_BAD_REQUEST)


class LogoutApiView(APIView):
    def post(self, request):
        try:
            if request.user and request.user.id:
                UserLogoutHistory.logout(user_id=request.user.id, platform='NA',
                                         all_mobile_devices=True)
                UserDeviceTokens.clean_tokens(request.user.id)
        except:
            pass
        return Response({"status": True, "message": "You have been logged out "},
                        status=status.HTTP_200_OK)


class UserStateCheckView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        login_type = request.GET.get('loginType')
        poll = request.GET.get('poll')
        current_site = get_current_site(request)
        site_domain = current_site.domain
        if not login_type:
            return Response({'status': False, 'message': 'Please pick the role'}, status=status.HTTP_400_BAD_REQUEST)
        resp = UserService().user_login_state(data=request.data, login_type=login_type, domain=site_domain, poll=poll)
        status_code = status.HTTP_200_OK
        if resp.get('status') is False:
            status_code = status.HTTP_400_BAD_REQUEST
        return Response(resp, status=status_code)


#
def loginPasswordHandlerView(request):
    if request.user.is_authenticated:
        return loginInUserRedirect(request)
    emailID = request.GET.get('profile')
    loginType = request.GET.get('type')
    loginTypeValid = loginTypeValidView(loginType)
    if not loginType or loginTypeValid == False:
        messages.error(request, 'Bad Request!')
        return redirect('authApp:loginUsernameHandlerUrl')
    secondUserCheck = checkUserAndProfiles(emailID)
    if not secondUserCheck:
        messages.error(request, 'Bad Login ID.')
        returnPath = reverse('authApp:loginUsernameHandlerUrl')
        returnPath += '?type=' + loginType
        return redirect(returnPath)

    try:
        profileInst = int(emailID)
    except:
        profileInst = emailID

    if type(profileInst) == int:
        profileInst = "integerType"
    else:
        profileInst = "strType"

    try:
        sideMenuObj = loginBannerObjects.objects.get(relatedTo__name=loginType)
    except:
        sideMenuObj = None
    loginBannerObjectsInstForm = loginBannerObjectsForm(instance=sideMenuObj)

    context = {
        "sideMenuObj": sideMenuObj,
        "profileInst": profileInst,
        'loginType': loginType
    }
    return render(request, 'authApp/UI/login2.html', context)


class resetOrCreatePasswordAPIView(APIView):
    serializer_class = resetOrCreatePasswordSerializer

    def post(self, request, pk):
        loginType = request.POST.get('loginType')
        if request.method == 'POST':
            pass1 = request.data.get('password')
            pass2 = request.data.get('confirm_password')
            userInst = User.objects.get(id=pk)

            referred_id = request.POST.get('referralID')
            if pass1 != pass2:
                return Response('Password Mismatched. Kindly Enter same password both times.')
            else:
                UserService().set_user_password(userInst, pass1)
                if referred_id:
                    UserService().apply_referral(userInst, referred_id)
                passwordCreateMsg = "Password Created Successfully."
                passwordUpdateMsg = "Password Updated Successfully."
                messages.success(request, passwordCreateMsg)
                login(request, userInst, backend='django.contrib.auth.backends.ModelBackend')
                return Response('password changed successfully')

        else:
            return Response("Invalid Method")


class RegisterAPIView(APIView):

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class UserBasic(APIView):

    def get(self, request):
        user = request.user
        user_role = request.user_role
        data = UserService().get_user_basic_info(user.id, user, user_role)
        resp = {'status': True, 'data': data}
        return Response(resp)


class UserRole(APIView):

    def post(self, request):
        user = request.user
        current_user_role = request.user_role
        data = request.data
        user_role = data.get('role')
        resp = UserService().change_user_role(user, current_user_role, user_role)
        return Response(resp)

    def get(self, request):
        user = request.user
        current_user_role = request.user_role
        data = UserService().fetch_user_roles(user)
        data['current_user_role'] = current_user_role
        return Response({'status': True, 'data': data})


class UserSocialAuth(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        vendor = request.GET.get('vendor')
        login_type = request.GET.get('loginType')
        redirect_uri = request.GET.get('redirectUri')
        current_site = get_current_site(request)
        site_domain = current_site.domain
        code = request.data.get('code')
        headers = request.headers
        resp = SocialAuth(vendor).process_auth(code, login_type, site_domain, redirect_uri, headers=headers)
        status_code = status.HTTP_200_OK
        if resp.get('status') is False:
            status_code = status.HTTP_400_BAD_REQUEST
        return Response(resp, status=status_code)


class UserPasswordCreateAPIView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        pass1 = request.data.get('password')
        pass2 = request.data.get('confirm_password')
        email = request.data.get('email')
        mobile_num = request.data.get('phoneNumber')
        login_type = request.GET.get('loginType')
        userInst = None
        if request.user and request.user.id:
            userInst = request.user
        else:
            if email:
                userInst = User.objects.filter(email=request.data.get('email')).last()
            elif mobile_num:
                userInst = User.objects.filter(username=mobile_num).last()
        if not userInst:
            return Response({'status': False, 'message': 'User does not exist.'},
                            status=status.HTTP_400_BAD_REQUEST)
        if not userInst.is_active:
            return Response({'status': False, 'message': 'user is in active.'},
                            status=status.HTTP_400_BAD_REQUEST)
        if userInst.password and userInst.has_usable_password() and not request.data.get('otp'):
            return Response({'status': False, 'message': 'Your password is already set. Please reset the password.'},
                            status=status.HTTP_400_BAD_REQUEST)
        if request.data.get('otp'):
            is_otp_validated, requested = OtpOrchestrator().validate_otp(userInst, request.data)
            if not is_otp_validated:
                return Response(
                    {'status': False, 'message': 'Invalid otp.'},
                    status=status.HTTP_400_BAD_REQUEST)
        referred_id = request.POST.get('referral_id')
        if pass1 != pass2:
            return Response({'status': False, 'message': 'Password Mismatched. Kindly Enter same password both times.'},
                            status=status.HTTP_400_BAD_REQUEST)
        else:
            UserService().set_user_password(userInst, pass1)
            if referred_id:
                UserService().apply_referral(userInst, referred_id)
            data = UserService().get_login_creds(userInst, login_type)
            return Response({'status': True, 'message': 'password created successfully', 'data': data})


class UserPasswordResetAPIView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        login_type = request.GET.get('loginType')
        current_site = get_current_site(request)
        site_domain = current_site.domain
        resp = UserService().reset_user_password(request.data, site_domain, login_type)
        status_code = status.HTTP_200_OK
        if resp.get('status') is False:
            status_code = status.HTTP_400_BAD_REQUEST
        return Response(resp, status=status_code)


class UserEmailRegisterAPIView(APIView):

    def post(self, request):
        login_type = request.GET.get('loginType')
        current_site = get_current_site(request)
        email = request.data.get('email')
        send_otp = request.data.get('sendOtp', None)
        site_domain = current_site.domain
        user = request.user
        resp = UserService().add_user_email(email, site_domain, login_type, user, send_otp)
        status_code = status.HTTP_200_OK
        if resp.get('status') is False:
            status_code = status.HTTP_400_BAD_REQUEST
        return Response(resp, status=status_code)


class UserVerifyOtpAPIView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        user = request.user if request.user and request.user.id else None
        user_role = request.user_role if request.user_role else request.GET.get('loginType')
        resp = UserService().validate_user(request.data, user, user_role)
        status_code = status.HTTP_200_OK
        if resp.get('status') is False:
            status_code = status.HTTP_400_BAD_REQUEST
        return Response(resp, status=status_code)


class UserDeviceTokenApiView(APIView):
    def post(self, request):
        user = request.user
        platform = request.headers.get('platform', '')
        UserService().update_user_device_token(user, platform, request.data)
        status_code = status.HTTP_200_OK
        return Response({'status': True}, status=status_code)


class NotificationTriggerApiView(APIView):
    def post(self, request):
        platform = request.headers.get('platform', '')
        data = request.data
        resp = NotificationMaster().send_push_notification(user_id=data["user_id"], template_name=data['template_name'],
                                                           payload=data['payload'], platform=platform)
        status_code = status.HTTP_200_OK
        if not resp:
            status_code = status.HTTP_400_BAD_REQUEST
        return Response({'status': resp}, status=status_code)


class UserGetOtpView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        # try:
        login_type = request.GET.get('loginType')
        current_site = get_current_site(request)
        site_domain = current_site.domain
        if not login_type:
            return Response({'status': False, 'message': 'Please pick the role'}, status=status.HTTP_400_BAD_REQUEST)
        data = request.data
        data["sendOtp"] = True
        headers = request.headers
        resp = UserService().user_login_state(data=data, login_type=login_type, domain=site_domain, headers=headers)
        status_code = status.HTTP_200_OK
        if resp.get('status') is False:
            status_code = status.HTTP_400_BAD_REQUEST
        return Response(resp, status=status_code)


class RolesView(APIView):
    permission_classes = (AllowAny,)

    @method_decorator(cache_page(15 * 60))
    def get(self, request):
        # try:
        resp = UserService.fetch_roles()
        return Response(resp)


@api_view(['GET'])
@permission_classes([AllowAny])
@cache_page(15 * 60)
def get_slug_info(request, slug_type, slug):
    resp = DataOrchestrator().fetch_slug_info(slug_type, slug)
    return Response(resp)


class UserPinSetAPIView(APIView):

    def post(self, request):
        data = request.data

        resp = UserService().set_pin(user=request.user, data=data)
        status_code = status.HTTP_200_OK
        if resp.get('status') is False:
            status_code = status.HTTP_400_BAD_REQUEST
        return Response(resp, status=status_code)


class UserPinValidateAPIView(APIView):

    def post(self, request):
        data = request.data

        resp = UserService().validate_pin(user=request.user, data=data)
        status_code = status.HTTP_200_OK
        if resp.get('status') is False:
            status_code = status.HTTP_400_BAD_REQUEST
        return Response(resp, status=status_code)


class UserPinUpdateAPIView(APIView):

    def post(self, request):
        data = request.data
        resp = UserService().set_pin(user=request.user, data=data)
        status_code = status.HTTP_200_OK
        if resp.get('status') is False:
            status_code = status.HTTP_400_BAD_REQUEST
        return Response(resp, status=status_code)


class UserPinResetAPIView(APIView):

    def get(self, request):
        current_site = get_current_site(request)
        site_domain = current_site.domain
        resp = UserService().send_mpin_reset_otp(user=request.user, domain=site_domain)
        status_code = status.HTTP_200_OK
        if resp.get('status') is False:
            status_code = status.HTTP_400_BAD_REQUEST
        return Response(resp, status=status_code)

    def post(self, request):
        resp = UserService().validate_reset_mpin(user=request.user, data=request.data)
        status_code = status.HTTP_200_OK
        if resp.get('status') is False:
            status_code = status.HTTP_400_BAD_REQUEST
        return Response(resp, status=status_code)


@api_view(['GET'])
def getDeviceToken(request, userId):
    try:
        platform = request.headers.get('platform')
        data = None
        if userId != 0:
            data = UserDeviceTokens.objects.filter(user_id=userId).order_by('updated').first()
            data = UserDeviceTokensSerializer(data).data
            del data['id']
        else:
            data = UserDeviceTokens.objects.all()
            data = UserDeviceTokensSerializer(data, many=True).data
        status_code = status.HTTP_200_OK
        return Response({'data': data}, status=status_code)
    except Exception as e:
        status_code = status.HTTP_400_BAD_REQUEST
        return Response({'message': str(e)}, status=status_code)


@staff_internal_login_required
def fetch_dashboard_users(request):
    filters = {}
    limit = int(request.GET.get('limit', 5000))
    fetch_type = request.GET.get('fetch_type', 'advisor')
    if request.GET.get('q'):
        filters['q'] = request.GET.get('q')
    elif request.GET.get('user_role'):
        filters['user_role'] = request.GET.get('user_role')
    elif request.GET.get('employee_user_id'):
        filters['employee_user_id'] = request.GET.get('employee_user_id')
    page = int(request.GET.get('page', 1))
    page_size = int(request.GET.get('page_size', 50))
    resp = DashboardService(request.user).fetch_users_data(filters, limit, fetch_type, page, page_size)
    status_code = status.HTTP_200_OK
    if resp.get('status') is False:
        status_code = status.HTTP_400_BAD_REQUEST
    return JsonResponse(resp, status=status_code)


@staff_internal_login_required
def user_advisor(request):
    if request.method == 'POST':
        resp = DashboardService(request.user).update_user_advisor_data(data=request.POST)
        status_code = status.HTTP_200_OK
        if resp.get('status') is False:
            status_code = status.HTTP_400_BAD_REQUEST
        return JsonResponse(resp, status=status_code)
    else:
        return JsonResponse({}, status=status.HTTP_400_BAD_REQUEST)


@staff_internal_login_required
def userRoleUpdateAPI(request):
    if request.method == 'POST':
        resp = DashboardService(request.user).update_user_role_new(data=request.POST)
        status_code = status.HTTP_200_OK
        if resp.get('status') is False:
            status_code = status.HTTP_400_BAD_REQUEST
        return JsonResponse(resp, status=status_code)
    else:
        return JsonResponse({}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def getUserDetails(request, userId):
    try:
        data = None
        if userId:
            data = User.objects.filter(id=userId).first()
            data = UserSerializer(data).data
        status_code = status.HTTP_200_OK
        return Response({'data': data}, status=status_code)
    except Exception as e:
        status_code = status.HTTP_400_BAD_REQUEST
        return Response({'message': str(e)}, status=status_code)


@api_view(['GET'])
def authenicateUserToken(request):
    try:
        if request.user:
            return Response({"status": "Success",
                             "data": UserSerializer(request.user).data,
                             "is_staff": request.user.is_staff,
                             "is_active": request.user.is_active,
                             "is_authenticated": request.user.is_authenticated
                             })
    except Exception as e:
        return Response({"status": "Failed", "message": str(e)})
