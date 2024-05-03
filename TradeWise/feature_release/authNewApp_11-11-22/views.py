from django.shortcuts import render, redirect, reverse, HttpResponse
from django.template.loader import render_to_string
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from investorApp.models import investorPersonalDetails, verificationStatus
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils import six
from django.contrib import messages
from django.conf import settings
from django.core.mail import send_mail
from django.http import JsonResponse
from whatsappAuthApp.models import whatsappLeads
from employeeApp.models import country
from planifyMain import whatsappTemp
from authApp.models import *
from .models import *
from .forms import *
import random
import track
import requests

#
class TokenGenerator(PasswordResetTokenGenerator):
	def _make_hash_value(self, user, timestamp):
		return (
			six.text_type(user.pk) + six.text_type(timestamp) +
			six.text_type(user.is_active)
		)
account_activation_token = TokenGenerator()

#
def logout_view(request):
	logout(request)
	messages.info(request, "Logged out successfully!")
	return redirect("websiteApp:homePageUrl")

#
def generate_otp_view():
	otp = str(random.randint(1000, 9999))
	return otp

#
def logged_in_user_redirect(request, callingFunction=None):
	redirect_required = False
	if request.user.is_authenticated:
		userInst = User.objects.get(pk=request.user.pk)
		try:
			if not userInst.userProfile_otp_authentication_authV2.email_verified:
				redirect_required = ('authNewApp:user_email_update_url')
			elif not userInst.userProfile_otp_authentication_authV2.phone_verified:
				redirect_required = ('authNewApp:user_whatsapp_update_url')
			elif not userInst.has_usable_password():
				redirect_required = ('authNewApp:create_or_update_user_password_url')
			else:
				redirect_required = (settings.LOGIN_REDIRECT_URL)
		except:
			pass
	return redirect_required

#
def login_signup_first_view(request):
	redirect_required = logged_in_user_redirect(request)
	if redirect_required:
		return redirect(redirect_required)
	countryList = country.objects.all()
	errorCode = request.session.get('error', None)
	errorType = request.session.get('error_type', None)
	authType = request.session.get('type', None)
	sent_otp_on = request.session.get('sent_otp_on', None)
	having_details = request.session.get('having_details', None)
	country_code = request.session.get('country_code', None)
	if not authType:
		authType = request.GET.get('type', None)
	if authType:
		request.session['type'] = authType
	errors = {
		'errorType': errorType,
		'sent_otp_on': sent_otp_on,
		'having_details': having_details,
		'country_code': country_code,
	}
	context = {
		'countryList': countryList,
		'errors': errors,
		'authType': authType,
		'noUniversalLoginPop': True,
	}
	if errorCode:
		del request.session['error']
	if errorType:
		del request.session['error_type']
	if sent_otp_on:
		del request.session['sent_otp_on']
	if having_details:
		del request.session['having_details']
	if country_code:
		del request.session['country_code']
	return render(request, 'auth_v2/auth_1.html', context)

#
def existing_user_login_view(request):

	context = {
		'noUniversalLoginPop': True,
	}
	return render(request, 'auth_v2/auth_2.html', context)

#
def existing_user_submit_view(request):
	if request.method == 'POST':
		username = request.session.get('user', None)
		login_method = request.session.get('type', None)
		password = request.POST.get('password')
		user = authenticate(request, username=username, password=password)

		if user is None:
			User = get_user_model()
			user_queryset = User.objects.filter(email__iexact=username)
			if user_queryset:
				username = user_queryset[0].username
				user = authenticate(username=username, password=password)

		if user is not None:
			if user.is_active:
				request.session['user_id'] = user.pk
				# return redirect(settings.LOGIN_REDIRECT_URL)
				return redirect(settings.LOGIN_PIN_URL)
			else:
				request.session['error_type'] = 'inactive'
		else:
			messages.error(request, f'Invalid Credentials! Kindly Retry with Valid Password.')
			return redirect('authNewApp:existing_user_login_url')
	return redirect(settings.LOGIN_URL)

#
def user_create_update_or_verify_pin_view(request, slug=None):
	errors = None
	request.session['type'] = 'pin'
	if request.user.is_authenticated:
		user_id = request.user.pk
	else:
		user_id = request.session.get('user_id', None)
	try:
		user = User.objects.get(pk=user_id)
	except:
		user = None

	if slug:
		page_flag = slug # can be submit, reset or update
	else:
		if user is not None and user.userProfile_otp_authentication_authV2.login_pin:
			page_flag = 'login'
		else:
			page_flag = 'create'
	# print(f'page_flag: {page_flag} || user: {user} || user_id: {user_id}')
	if user:
		if page_flag == 'reset':
			if request.GET.get('token') or request.POST.get('token'):
				if request.session.get('pin_action'):
					del request.session['pin_action']
			else:
				otpInst, otpCreated = otp_authentication.objects.get_or_create(userProfile=user)
				otp = generate_otp_view()
				otpInst.otp = otp
				otpInst.save()
				errorsCount = 0
				try:
					sendto = otpInst.mobile
					countryCode = otpInst.country_code
					status = send_otp_over_whatsapp_view(sendto, otp, countryCode)
				except:
					errorsCount += 1 
				try:
					sendto = otpInst.email
					status = send_otp_over_mail_view(sendto, otp)
				except:
					errorsCount += 1 
				if errorsCount == 2:
					messages.error(request, 'We are not able to sent communication to your email or phone number, Kindly contact Support.')
				else:
					errors = {
						'errorType': 'reset-pin',
					}
				request.session['pin_action'] = 'reset'

		if request.method == 'POST':
			verify_user_token = request.POST.get('token', None)
			token_based_pin_update = None
			if verify_user_token:
				if account_activation_token.check_token(user, verify_user_token):
					token_based_pin_update = True
				else:
					token_based_pin_update = False
			otpInst, otpCreated = otp_authentication.objects.get_or_create(userProfile=user)
			if page_flag == 'login':
				new_pin = request.POST.get('login_pin', None)
				if new_pin and str(otpInst.login_pin) == str(new_pin):
					login(request, user, backend='django.contrib.auth.backends.ModelBackend')
					return redirect(settings.LOGIN_REDIRECT_URL)
				else:
					messages.error(request, 'Kindly Enter a Valid PIN.')
			elif page_flag == 'create':
				new_pin = request.POST.get('login_pin', None)
				if new_pin:
					otpInst.login_pin = new_pin
					otpInst.save()
					messages.success(request, 'Login PIN Created Successfully.')
					login(request, user, backend='django.contrib.auth.backends.ModelBackend')
					return redirect(settings.LOGIN_REDIRECT_URL)
				else:
					messages.error(request, 'Kindly Enter New PIN.')
			elif page_flag == 'update':
				crr_pin = request.POST.get('current_pin')
				if crr_pin:
					if str(otpInst.login_pin) == str(crr_pin):
						new_pin = request.POST.get('login_pin', None)
						if new_pin:
							otpInst.login_pin = new_pin
							otpInst.save()
							messages.success(request, 'Login PIN Updated Successfully.')
							return redirect(settings.LOGIN_REDIRECT_URL)
						else:
							messages.error(request, 'Kindly Enter New PIN.')
					else:
						messages.error(request, 'Entered Current Pin is Invalid.')
				else:
					messages.error(request, 'Kindly Enter Current PIN.')
			elif page_flag == 'reset':
				if token_based_pin_update:
					new_pin = request.POST.get('login_pin', None)
					if new_pin:
						otpInst.login_pin = new_pin
						otpInst.save()
						messages.success(request, 'Login PIN Reset Successful.')
						login(request, user, backend='django.contrib.auth.backends.ModelBackend')
						return redirect(settings.LOGIN_REDIRECT_URL)
					else:
						messages.error(request, 'Kindly Enter New PIN.')
				elif token_based_pin_update == False:
					messages.error(request, 'User Authentication Failed.')
				else:
					messages.error(request, 'Error Verifying your Account. Kindly Retry.')
	context = {
		'noUniversalLoginPop': True,
		'page_flag': page_flag,
		'errors': errors,
	}
	return render(request, 'auth_v2/auth_3.html', context)

#
def check_user_by_email_view(email):
	user = gotUserBy = None
	if User.objects.filter(username = email).exists():
		user = User.objects.get(username = email)
	elif User.objects.filter(email = email).exists():
		user = User.objects.get(email = email)
	return user, gotUserBy

#
def check_user_by_phone_view(phone):
	user = None
	if User.objects.filter(username = phone).exists():
		user = User.objects.get(username = phone)
	return user

#
def add_new_user_to_intract_view(sendto, countryCode):
	flag = False
	payload = {"phoneNumber": str(sendto), "countryCode": str(countryCode), "tags": ["new users"]}
	r = requests.post(
		'https://api.interakt.ai/v1/public/track/users/',
		headers=
			{
				'Accept': 'application/json',
				'Content-Type': 'application/json',
				'Authorization': 'Basic UXlhZXpxLThCYkU5RnhGMVNqTmRLWEktRm1qallxeWo1R1ZqYm9iUVFuUTo='
			},
		json=payload
	)
	flag = r.status_code
	return flag

#
def send_otp_over_whatsapp_view(sendto, otp, countryCode='+91'):
	flag = add_new_user_to_intract_view(sendto, countryCode)
	otp_sent_flag = False
	if (flag == 202 or flag == 200 or flag == 201):
		template_var = whatsappTemp.WHATSAPP_OTP
		payload = {
			"countryCode": str(countryCode),
			"phoneNumber": str(sendto),
			"type": "Template",
			"template": {
				"name": template_var,
				"languageCode": "en",
				"bodyValues": [str(otp)],
				}
			}
		response = requests.post(
			'https://api.interakt.ai/v1/public/message/',
			headers={
				'Accept': 'application/json',
				'Content-Type': 'application/json',
				'Authorization': 'Basic UXlhZXpxLThCYkU5RnhGMVNqTmRLWEktRm1qallxeWo1R1ZqYm9iUVFuUTo='
				},
			json=payload
		)
		otp_sent_flag = response.status_code
	return otp_sent_flag

#
def send_otp_over_mail_view(sendto, otp):
	flag = False
	context = {
		'otp': otp,
	}
	message = render_to_string('auth_v2/otp_mail.html', context)
	email = send_mail(
		subject='Verify Your Planify Account',
		message='',
		from_email='reports@planify.in',
		recipient_list=[sendto],
		html_message=message,
	)
	flag = email
	return flag

#
def resent_otp_ajax_view(request):
	if request.method == 'POST':
		sent_on = request.POST.get('send_on')
		sent_to = request.POST.get('address')
		country_code = request.POST.get('country_code')
		if sent_on == 'Email':
			user, gotUserBy = check_user_by_email_view(sent_to)
			if user:
				user = user
			elif request.user.is_authenticated:
				user = User.objects.get(pk=request.user.pk)
			else:
				message = 'Authentication Issue. Kindly Refresh the page and Try Again.'
			if user:
				otp = generate_otp_view()
				sent_status = send_otp_over_mail_view(sent_to, otp)
				if sent_status:
					otpInst, otpCreated = otp_authentication.objects.get_or_create(userProfile=user)
					otpInst.otp = otp
					otpInst.save()
					message = 'We have resent a 4 digit code (OTP) to your Email: '+sent_to+'.'
				else:
					message = 'Unable to resent OTP, Kindly Try Again Later.'
			else:
				message = 'Authentication Issue. Kindly Refresh the page and Try Again.'
		elif sent_on == 'Mobile':
			user = check_user_by_phone_view(sent_to)
			if user:
				user = user
			elif request.user.is_authenticated:
				user = User.objects.get(pk=request.user.pk)
			else:
				message = 'Authentication Issue. Kindly Refresh the page and Try Again.'
			if user:
				otp = generate_otp_view()
				sent_status = send_otp_over_whatsapp_view(sent_to, otp, country_code)
				if sent_status:
					otpInst, otpCreated = otp_authentication.objects.get_or_create(userProfile=user)
					otpInst.otp = otp
					otpInst.save()
					message = 'We have resent a 4 digit code (OTP) to your Whatsapp number: '+sent_to+' '
				else:
					message = 'Unable to resent OTP, Kindly Try Again Later.'
		elif sent_on == 'Both':
			# try:
			user_id = request.session.get('user_id')
			user = User.objects.get(pk=user_id)
			if user:
				otp = generate_otp_view()
				try:
					username = int(user.username)
				except:
					username = user.username
				if type(username) is int:
					try:
						country_code = user.userProfile_otp_authentication_authV2.country_code
					except:
						username = user.username
					if type(username) is int:
						try:
							country_code = user.userProfile_otp_authentication_authV2.country_code
						except:
							country_code = '+91'
						sent_status_whatsapp = send_otp_over_whatsapp_view(username, otp, country_code)
					else:
						sent_status_whatsapp = False
					if user.email:
						sent_status_email = send_otp_over_mail_view(user.email, otp)
					else:
						sent_status_email = False
					otpInst, otpCreated = otp_authentication.objects.get_or_create(userProfile=user)
					otpInst.otp = otp
					otpInst.save()
					if sent_status_email and sent_status_whatsapp in [202, 200, 201,]:
						message = 'We have resent a 4 digit code (OTP) to your '+str(user.email)+' and '+str(user.username)+' '
					elif not sent_status_email and sent_status_whatsapp in [202, 200, 201,]:
						message = 'We have resent a 4 digit code (OTP) to your Whatsapp number '+str(user.username)+' '
					elif sent_status_email and not sent_status_whatsapp in [202, 200, 201,]:
						message = 'We have resent a 4 digit code (OTP) to your Email '+str(user.email)+' '
					else:
						message = 'We are unable to verify your account, Kindly refresh page and Try Again.'
			else:
				message = 'Authentication Issue. Kindly Refresh the page and Try Again.'
		context = {
			'message': message,
		}
		return JsonResponse(context)
	return HttpResponse('Invalid Entry!')

#
def otp_authentication_submit_view(request):
	if request.method == 'POST':
		gotUserBy = None
		email = request.POST.get('email')
		phone = request.POST.get('phone')
		countryCode = request.POST.get('countryCode')
		profile_type = request.POST.get('profile_type' or 'INVESTOR')
		requested_on = request.POST.get('requested_on') # mobile or email
		requested_for = request.POST.get('requested_for') # login or signup
		otp = generate_otp_view()
		request.session['type'] = requested_on
		request.session['profile_type'] = profile_type
		if requested_on == 'Mobile':
			userInst = check_user_by_phone_view(phone)
			request.session['sent_otp_on'] = 'Mobile'
			request.session['having_details'] = phone
			request.session['country_code'] = countryCode
		elif requested_on == 'Email':
			userInst, gotUserBy = check_user_by_email_view(email)
			request.session['sent_otp_on'] = 'Email'
			request.session['having_details'] = email
		if userInst:
			request.session['user_id'] = userInst.pk
			if requested_on == 'Mobile':
				request.session['user'] = phone
			elif requested_on == 'Email':
				request.session['user'] = email
			if userInst.is_active and userInst.has_usable_password():
				return redirect('authNewApp:existing_user_login_url')
			elif not userInst.is_active:
				request.session['error_type'] = 'inactive'
			elif not userInst.has_usable_password():
				request.session['error_type'] = 'no_password'
			if request.session.get('error_type') in ['inactive', 'no_password',]:
				otpInst, otpInst_created = otp_authentication.objects.get_or_create(userProfile=userInst)
				otpInst.save()
		else:
			request.session['error_type'] = 'no_account'
			try:
				if requested_on == 'Email':
					userInst = User.objects.create(
						username=email,
						email=email,
						is_active=False
					)
				elif requested_on == 'Mobile':
					userInst = User.objects.create(
						username=phone,
						is_active=False
					)
				userInst.set_unusable_password()
			except:
				messages.error(request, 'Error while creating User')
				return redirect('authNewApp:login_signup_first_url')
			roleForUser = roles.objects.get(name=profile_type)
			roleOfUser = userRoles(profile_owner=userInst)
			userInst.save()
			roleOfUser.save()
			roleOfUser.profile_roles.add(roleForUser)
			objForm = otp_authentication_form(request.POST)
			
			if objForm.is_valid():
				cd = objForm.save(commit=False)
				cd.userProfile = userInst
				cd.otp = otp
				cd.save()
			else:
				messages.error(request, f'Please check for the Below Errors: {objForm.errors}')
		if request.session.get('error_type') in ['inactive', 'no_password', 'no_account',]:
			otpInst, otpCreated = otp_authentication.objects.get_or_create(userProfile=userInst)
			otpInst.country_code = countryCode
			if requested_on == 'Mobile':
				request.session['user'] = phone
				otpInst.mobile = phone
				sent_status = send_otp_over_whatsapp_view(phone, otp, countryCode)
			elif requested_on == 'Email':
				request.session['user'] = email
				otpInst.email = email
				sent_status = send_otp_over_mail_view(email, otp)
			otpInst.otp = otp
			otpInst.save()
	return redirect('authNewApp:login_signup_first_url')

#
def otp_submit_and_activate_view(request):
	username = request.session.get('user', None)
	authType = request.session.get('type', None)
	profile_type = request.session.get('profile_type', None)
	try:
		crr_user = User.objects.get(username=username)
	except:
		crr_user = None
	if not crr_user:
		try:
			crr_user = User.objects.get(email=username)
		except:
			crr_user = None
	if crr_user and request.method == 'POST':
		otpInst, otpCreated = otp_authentication.objects.get_or_create(userProfile=crr_user)
		if str(otpInst.otp) == str(request.POST.get('otp')):
			crr_user.is_active = True
			if authType == 'Mobile':
				otpInst.phone_verified = True
				if crr_user.username != otpInst.mobile:
					if User.objects.exclude(pk=crr_user.pk).filter(username=otpInst.mobile).exists():
						messages.error(request, 'Verified Mobile Already Linked with Some Other Account.')
					else:
						crr_user.username = otpInst.mobile
			elif authType == 'Email':
				otpInst.email_verified = True
				crr_user.email = otpInst.email
			elif authType == 'pin':
				pin_action = request.session.get('pin_action', None)
				if pin_action == 'reset':
					verify_user_token = account_activation_token.make_token(crr_user)
					user_redirect = reverse('authNewApp:user_create_update_or_verify_pin_url', kwargs={'slug': 'reset'})
					user_redirect += '?token='+verify_user_token
					return redirect(user_redirect)
			elif authType == 'password':
				pass_action = request.session.get('pass_action', None)
				if pass_action == 'reset':
					verify_user_token = account_activation_token.make_token(crr_user)
					user_redirect = reverse('authNewApp:password_reset_url', kwargs={'slug': 'reset'})
					user_redirect += '?token='+verify_user_token
					return redirect(user_redirect)
			crr_user.save()
			otpInst.save()
			login(request, crr_user, backend='django.contrib.auth.backends.ModelBackend')
			request.session['profile_type'] = profile_type
			request.session['user_onboarding'] = True
			user_have_pass = crr_user.has_usable_password()
			user_last_login = crr_user.last_login
			request.session['user_id'] = crr_user.pk
			if crr_user.username == crr_user.email:
				return redirect('authNewApp:user_whatsapp_update_url')
			elif not crr_user.email:
				return redirect('authNewApp:user_email_update_url')
			elif not user_have_pass and not request.session.get('social_auth_last_login_backend', None):
				return redirect('authNewApp:create_or_update_user_password_url')
			elif not otpInst.login_pin:
				return redirect('authNewApp:user_create_update_or_verify_pin_url', 'create')
			if request.session.get('social_login'):
				return redirect(settings.LOGIN_REDIRECT_URL)
			else:
				if request.session.get('error_type') == 'no_account' or not user_have_pass:
					return redirect('authNewApp:create_or_update_user_password_url')
				else:
					return redirect('authNewApp:existing_user_login_url')
		else:
			request.session['error_type'] = 'invalid_otp'
		return redirect('authNewApp:login_signup_first_url')
	else:
		messages.error(request, 'Invalid Entry!')
	return redirect('authNewApp:existing_user_login_url')

#
def check_email_whatsapp_verification_status(userInst):
	whatsappVerified = emailVerified = passAvailable =  loginPinAvailable = False
	try:
		if userInst.userProfile_otp_authentication_authV2.phone_verified == True:
			whatsappVerified = True
	except:
		pass
	try:
		if userInst.userProfile_otp_authentication_authV2.email_verified == True:
			emailVerified = True
	except:
		pass
	try:
		if userInst.has_usable_password():
			passAvailable = True
	except:
		pass
	try:
		if userInst.userProfile_otp_authentication_authV2.login_pin:
			loginPinAvailable = True
	except:
		pass
	return whatsappVerified, emailVerified, passAvailable, loginPinAvailable

# def check_email_whatsapp_verification_status(userInst):
# 	whatsappVerified = emailVerified = loginPinAvailable = False
# 	try:
# 		if userInst.userProfile_otp_authentication_authV2.phone_verified == True:
# 			whatsappVerified = True
# 	except:
# 		pass
# 	try:
# 		if userInst.userProfile_otp_authentication_authV2.email_verified == True:
# 			emailVerified = True
# 	except:
# 		pass
# 	try:
# 		if userInst.userProfile_otp_authentication_authV2.login_pin:
# 			loginPinAvailable = True
# 	except:
# 		pass
# 	return whatsappVerified, emailVerified, loginPinAvailable

#
def create_password_and_valid_redirect(request, userInst, pass1, pass_msg, referredID=None):
	userInst.set_password(pass1)
	userInst.is_active = True
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
	request.session['message'] = pass_msg
	messages.warning(request, pass_msg)
	login(request, userInst, backend='django.contrib.auth.backends.ModelBackend')
	request.session['user_id'] = userInst.pk
	whatsappVerified, emailVerified, passAvailable, loginPinAvailable = check_email_whatsapp_verification_status(userInst)
	if not whatsappVerified and emailVerified:
		return redirect('authNewApp:user_whatsapp_update_url')
	elif whatsappVerified and not emailVerified:
		return redirect('authNewApp:user_email_update_url')
	elif whatsappVerified and emailVerified and not passAvailable:
		return redirect(settings.CHANGE_PASSWORD_URL)
	elif whatsappVerified and emailVerified and not loginPinAvailable:
		return redirect('authNewApp:user_create_update_or_verify_pin_url', 'create')
	elif whatsappVerified and emailVerified and loginPinAvailable:
		return redirect(settings.LOGIN_REDIRECT_URL)
	return False

#
def password_reset_view(request, slug=None):
	errors = None
	request.session['type'] = 'password'
	if slug:
		page_flag = slug
	else:
		page_flag = 'login'
	request.session['send_on'] = sent_otp_on = 'Both'
	if page_flag == 'reset':
		if request.GET.get('token') or request.POST.get('token'):
			if request.session.get('pass_action'):
				del request.session['pass_action']
		else:
			user_id = request.session.get('user_id')
			user = User.objects.get(pk=user_id)
			otpInst, otpCreated = otp_authentication.objects.get_or_create(userProfile=user)
			otp = generate_otp_view()
			otpInst.otp = otp
			otpInst.save()
			errorsCount = 0
			try:
				sendto = otpInst.mobile
				countryCode = otpInst.country_code
				status = send_otp_over_whatsapp_view(sendto, otp, countryCode)
			except:
				errorsCount += 1 
			try:
				sendto = otpInst.email
				status = send_otp_over_mail_view(sendto, otp)
			except:
				errorsCount += 1 
			if errorsCount == 2:
				messages.error(request, 'We are not able to sent communication to your email or phone number, Kindly contact Support.')
			else:
				errors = {
					'errorType': 'reset-password',
					'sent_otp_on': sent_otp_on,
				}
			request.session['pass_action'] = 'reset'

	if request.method == 'POST':
		user_id = request.session.get('user_id')
		user = User.objects.get(pk=user_id)
		sent_otp_on = request.session.get('sent_otp_on', None)
		# having_details = request.session.get('having_details', None)
		verify_user_token = request.POST.get('token', None)
		token_based_pass_update = None
		if verify_user_token:
			if account_activation_token.check_token(user, verify_user_token):
				token_based_pass_update = True
			else:
				token_based_pass_update = False
		otpInst, otpCreated = otp_authentication.objects.get_or_create(userProfile=user)
		if page_flag == 'reset':
			if token_based_pass_update:
				new_pass1 = request.POST.get('password', None)
				new_pass2 = request.POST.get('confirm_password', None)
				if (new_pass1 and new_pass2) and (new_pass1 == new_pass2):
					user.set_password(new_pass1)
					user.save()
					messages.success(request, 'Password Reset Successful.')
					login(request, user, backend='django.contrib.auth.backends.ModelBackend')
					return redirect(settings.LOGIN_REDIRECT_URL)
				else:
					messages.error(request, 'Both Entered Password are Different. Kindly enter same password.')
			elif token_based_pass_update == False:
				messages.error(request, 'User Authentication Failed.')
			else:
				messages.error(request, 'Error Verifying your Account. Kindly Retry.')
	context = {
		'noUniversalLoginPop': True,
		'page_flag': page_flag,
		'errors': errors,
	}
	return render(request, 'auth_v2/update_password.html', context)


#
@login_required
def create_or_update_user_password_view(request):
	userInst = User.objects.get(pk=request.user.pk)
	if userInst.has_usable_password():
		pass_msg = "Password Updated Successfully."
		password_update = True
	else:
		pass_msg = "Password Created Successfully."
		password_update = False
	if request.method == 'POST':
		crr_pass = request.POST.get('current_password', None)
		pass1 = request.POST.get('password')
		pass2 = request.POST.get('confirm_password')
		referredID = request.POST.get('referralID', None)
		if pass1 != pass2:
			messages.error(request, 'Password Mismatched. Kindly Enter same password both times.')
			entered_pass_updatable = False
		else:
			entered_pass_updatable = True
		if entered_pass_updatable:
			if crr_pass:
				user = authenticate(request, username=userInst.username, password=crr_pass)
				if user is not None:
					create_pass_flag = create_password_and_valid_redirect(request, userInst, pass1, pass_msg, referredID)
					if create_pass_flag:
						return create_pass_flag
					else:
						messages.error(request, 'System Error While Updating your Password. Kindly retry after sometime or contact support.')
				else:
					messages.error(request, 'Invalid Current Password. Kindly Enter Valid Password you used for Login.')
			else:
				create_pass_flag = create_password_and_valid_redirect(request, userInst, pass1, pass_msg, referredID)
				if create_pass_flag:
					return create_pass_flag
				else:
					messages.error(request, 'System Error While Updating your Password. Kindly retry after sometime or contact support.')
	try:
		sideMenuObj = loginBannerObjects.objects.get(relatedTo__name=loginType)
	except:
		sideMenuObj = None
	context = {
		'sideMenuObj': sideMenuObj,
		'noUniversalLoginPop': True,
		'password_update': password_update,
	}
	return render(request, 'auth_v2/update_password.html', context)

#
def create_or_update_user_login_PIN_view(request):
	try:
		otpInst, otpCreated = otp_authentication.objects.get_or_create(userProfile_pk=request.user.pk)
	except:
		otpInst = None
	if otpInst:
		if otpInst.login_pin:
			pin_action = 'change'
		else:
			pin_action = 'create'
	else:
		pin_action = 'reset'


	context = {
		'noUniversalLoginPop': True,
		'pin_action': pin_action,
	}
	return render(request, 'auth_v2/auth_3.html', context)

#
@login_required
def user_whatsapp_update_view(request):
	sent_otp_on = 'Mobile'
	having_details = request.session.get('having_details', None)
	country_code = request.session.get('country_code', None)
	errors = None
	if request.method == 'POST':
		request.session['user'] = request.user.username
		request.session['type'] = 'Mobile'
		sendto = request.POST.get('phone')
		countryCode = request.POST.get('countryCode')
		request.session['sent_otp_on'] = sent_otp_on = 'Mobile'
		request.session['having_details'] = having_details = sendto
		request.session['country_code'] = country_code = countryCode
		userInst = User.objects.get(pk=request.user.pk)
		if otp_authentication.objects.exclude(userProfile=userInst).filter(mobile=sendto, country_code=countryCode).exists():
			messages.error(request, 'Mobile Number you entered is already linked with Some Account. Kindly Provide a Different Number or Contact Support.')
		else:
			otp = generate_otp_view()
			status = send_otp_over_whatsapp_view(sendto, otp, countryCode)
			otpInst, created = otp_authentication.objects.get_or_create(userProfile=userInst)
			otpInst.otp = otp
			otpInst.mobile = sendto
			otpInst.country_code = countryCode
			otpInst.save()
			errorType = 'verify'
			errors = {
				'errorType': errorType,
				'sent_otp_on': sent_otp_on,
				'having_details': having_details,
				'country_code': country_code,
			}
	if not request.session.get('error_type') == 'invalid_otp':
		if request.session.get('sent_otp_on'):
			del request.session['sent_otp_on']
		if request.session.get('having_details'):
			del request.session['having_details']
		if request.session.get('country_code'):
			del request.session['country_code']
	else:
		errorType = request.session.get('error_type', None)
		if having_details and country_code:
			errors = {
				'errorType': errorType,
				'sent_otp_on': sent_otp_on,
				'having_details': having_details,
				'country_code': country_code,
			}
		else:
			errors = {
				'errorType': errorType,
			}
		if errorType:
			del request.session['error_type']
	countryList = country.objects.all()
	context = {
		'errors': errors,
		'countryList': countryList,
		'authType': 'Mobile',
	}
	return render(request, 'auth_v2/add_whatsapp_to_profile.html', context)

#
@login_required
def user_email_update_view(request):
	errors = None
	if request.method == 'POST':
		request.session['user'] = request.user.username
		request.session['type'] = 'Email'
		sendto = request.POST.get('email')
		# countryCode = request.POST.get('countryCode')
		userInst = User.objects.get(pk=request.user.pk)
		if otp_authentication.objects.exclude(userProfile=userInst).filter(email=sendto).exists():
			messages.error(request, 'Email Address you entered is already linked with Some Account. Kindly Provide a Different Email ID or Contact Support.')
		else:
			otp = generate_otp_view()
			status = send_otp_over_mail_view(sendto, otp)
			otpInst, otpCreated = otp_authentication.objects.get_or_create(userProfile=userInst)
			otpInst.otp = otp
			otpInst.email = sendto
			otpInst.save()
			errorType = 'verify'
			request.session['sent_otp_on'] = sent_otp_on = 'Email'
			request.session['having_details'] = having_details = sendto
			errors = {
				'errorType': errorType,
				'sent_otp_on': sent_otp_on,
				'having_details': having_details,
			}			
			if sent_otp_on:
				del request.session['sent_otp_on']
			if having_details:
				del request.session['having_details']
	context = {
		'errors': errors,
		'authType': 'Email',
	}
	return render(request, 'auth_v2/add_email_to_profile.html', context)

#
def social_login_view(request):
	loginType = request.GET.get('type') or request.session['type']
	try:
		userInst = User.objects.get(pk=request.user.pk)
		uname = userInst.username
		request.session['user_id'] = userInst.pk
	except:
		userInst = None
	if userInst:
		used_social_auth = request.session.get('social_auth_last_login_backend')
		empLogin = False
		try:
			user_mail_domain = uname.split('@')[1]
			if user_mail_domain == 'planify.in':
				print(f'User with email: {uname} have domain: {user_mail_domain} and Hence not allowed to signin')
				messages.error(request, 'You can not use Planify ID to Signup.')
				redirectUrl = reverse(settings.LOGIN_URL)
				redirectUrl += '?type=' + loginType
				userInst.delete()
				return redirect(redirectUrl)
		except:
			pass
		otpInst, otpInst_created = otp_authentication.objects.get_or_create(userProfile=userInst)
		if used_social_auth == 'google-oauth2':
			otpInst.email_verified = True
			otpInst.google_verified = True
		elif used_social_auth == 'linkedin-oauth2':
			# otpInst.email_verified = True
			otpInst.linkedin_verified = True
		otpInst.save()
		if userInst.userProfile_otp_authentication_authV2.login_pin:
			request.session['user_id'] = userInst.pk
			redirectUrl = reverse('authNewApp:user_create_update_or_verify_pin_url', kwargs={'slug': 'login'})
		else:
			redirectUrl = reverse(settings.LOGIN_PIN_URL)
		roleForUser = roles.objects.get(name=loginType)
		roleOfUser, created = userRoles.objects.get_or_create(profile_owner=userInst)
		if created:
			roleOfUser.save()
			roleOfUser.profile_roles.add(roleForUser)
			request.session['onboarding'] = True
		if not otpInst.phone_verified:
			redirectUrl = reverse(settings.UPDATE_WHATSAPP_TO_ACCOUNT_URL)
			redirectUrl += "?onboarding=true"
			redirectUrl += "&type=" + loginType
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
		request.session['social_login'] = True
		return redirect(redirectUrl)
	else:
		return HttpResponse(
			f'No Response from your Google Account, This triggered System Failure. Kindly Go Back & Try Again Later or Signup Manually.')
	return HttpResponse(f'Hello {loginType}, An error occured. Kindly Try Again.')