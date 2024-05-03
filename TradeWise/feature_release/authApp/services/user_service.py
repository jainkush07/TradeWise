import uuid
from django.db.models import Q
from authNewApp.models import otp_authentication
from django.core.cache import cache
from authApp.services.notification_service import NotificationMaster
from django.contrib.auth.models import User
from whatsappAuthApp.services.whatsapp_lead import WhatsappLead
from whatsappAuthApp.services.whatsapp_sms import send_whatsapp_verification
from rest_framework_simplejwt.tokens import RefreshToken
from authApp.services.otp_service import OtpOrchestrator
from django.utils.encoding import force_bytes, force_str
from whatsappAuthApp.models import whatsappLeads
from investorApp.models import verificationStatus, investorPersonalDetails
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from investorApp.services.kyc.constants import UserRoleTypes
from authApp.tokens import account_activation_token
from authApp.constants import UserTypes
from authApp.integrations.social_auth import LinkedInAuth, GoogleAuth
from authApp.models import userRoles, roles, UserDeviceTokens, UserAdvisors


def check_email_whatsapp_verification_status(userInst):
    # need to improve logic todo
    whatsappVerified = emailVerified = False
    try:
        if userInst.profileOwnerWL.verified:
            whatsappVerified = True
    except:
        pass
    try:
        if userInst.profileOwnerIPD.emailVerified:
            emailVerified = True
    except:
        pass
    return whatsappVerified, emailVerified


class UserService:

    def validate_role(self, user, role, user_roles=None):
        if not user_roles:
            user_roles = self._get_user_roles(user)
        if role == UserRoleTypes.INSTITUTIONAL.value:
            role = UserRoleTypes.VC.value
        if role in user_roles:
            return 1
        role_block = {
            UserRoleTypes.INVESTOR.value: [UserRoleTypes.INSTITUTIONAL.value, UserRoleTypes.VC.value,
                                           UserRoleTypes.FO.value,
                                           UserRoleTypes.PRIVATE_BANKS.value, UserRoleTypes.EMPLOYEE.value],
            UserRoleTypes.INSTITUTIONAL.value: [UserRoleTypes.INVESTOR.value, UserRoleTypes.CHANNEL_PARTNER.value,
                                                UserRoleTypes.ESOP.value, UserRoleTypes.FOUNDER.value,
                                                UserRoleTypes.FO.value,
                                                UserRoleTypes.PRIVATE_BANKS.value],
            UserRoleTypes.VC.value: [UserRoleTypes.INVESTOR.value, UserRoleTypes.CHANNEL_PARTNER.value,
                                     UserRoleTypes.ESOP.value, UserRoleTypes.FOUNDER.value,
                                     UserRoleTypes.FO.value,
                                     UserRoleTypes.PRIVATE_BANKS.value],
            UserRoleTypes.FO.value: [UserRoleTypes.INVESTOR.value, UserRoleTypes.CHANNEL_PARTNER.value,
                                     UserRoleTypes.INSTITUTIONAL.value, UserRoleTypes.VC.value,
                                     UserRoleTypes.PRIVATE_BANKS.value],
            UserRoleTypes.EMPLOYEE.value: [UserRoleTypes.INSTITUTIONAL.value, UserRoleTypes.VC.value,
                                           UserRoleTypes.DEALER.value,
                                           UserRoleTypes.ESOP.value, UserRoleTypes.FOUNDER.value,
                                           UserRoleTypes.FO.value,
                                           UserRoleTypes.CHANNEL_PARTNER.value, UserRoleTypes.PRIVATE_BANKS.value,
                                           UserRoleTypes.INVESTOR.value],
            UserRoleTypes.DEALER.value: [UserRoleTypes.INSTITUTIONAL.value, UserRoleTypes.VC.value,
                                         UserRoleTypes.EMPLOYEE.value,
                                         UserRoleTypes.AUTHORE.value, UserRoleTypes.ESOP.value, UserRoleTypes.FO.value,
                                         UserRoleTypes.CHANNEL_PARTNER.value, UserRoleTypes.PRIVATE_BANKS.value],
            UserRoleTypes.CHANNEL_PARTNER.value: [UserRoleTypes.INSTITUTIONAL.value, UserRoleTypes.EMPLOYEE.value,
                                                  UserRoleTypes.ESOP.value, UserRoleTypes.VC.value,
                                                  UserRoleTypes.FO.value, UserRoleTypes.DEALER.value,
                                                  UserRoleTypes.PRIVATE_BANKS.value
                                                  ],
            UserRoleTypes.AUTHORE.value: [],
            UserRoleTypes.ESOP.value: [UserRoleTypes.CHANNEL_PARTNER.value, UserRoleTypes.INSTITUTIONAL.value,
                                       UserRoleTypes.VC.value],
            UserRoleTypes.FOUNDER.value: [UserRoleTypes.INSTITUTIONAL.value, UserRoleTypes.VC.value],
            UserRoleTypes.PRIVATE_BANKS.value: [UserRoleTypes.INSTITUTIONAL.value, UserRoleTypes.EMPLOYEE.value,
                                                UserRoleTypes.FO.value, UserRoleTypes.CHANNEL_PARTNER.value,
                                                UserRoleTypes.INVESTOR.value, UserRoleTypes.VC.value],
        }
        blocked_roles = role_block.get(role, [])
        for _role in blocked_roles:
            if _role in user_roles:
                return 2
        role_combination_na = {
            UserRoleTypes.FOUNDER.value: [[UserRoleTypes.INVESTOR.value, UserRoleTypes.DEALER.value],
                                          [UserRoleTypes.INVESTOR.value, UserRoleTypes.CHANNEL_PARTNER.value],
                                          [UserRoleTypes.ESOP.value, UserRoleTypes.PRIVATE_BANKS.value]],
            UserRoleTypes.DEALER.value: [[UserRoleTypes.INVESTOR.value, UserRoleTypes.FOUNDER.value],
                                         [UserRoleTypes.INVESTOR.value, UserRoleTypes.CHANNEL_PARTNER.value],
                                         [UserRoleTypes.ESOP.value, UserRoleTypes.INVESTOR.value]],
            UserRoleTypes.INVESTOR.value: [[UserRoleTypes.FOUNDER.value, UserRoleTypes.DEALER.value],
                                           [UserRoleTypes.FOUNDER.value, UserRoleTypes.CHANNEL_PARTNER.value],
                                           [UserRoleTypes.CHANNEL_PARTNER.value, UserRoleTypes.DEALER.value],
                                           [UserRoleTypes.ESOP.value, UserRoleTypes.DEALER.value]
                                           ],
            UserRoleTypes.CHANNEL_PARTNER.value: [[UserRoleTypes.INVESTOR.value, UserRoleTypes.FOUNDER.value],
                                                  [UserRoleTypes.INVESTOR.value, UserRoleTypes.DEALER.value]],
            UserRoleTypes.PRIVATE_BANKS.value: [[UserRoleTypes.ESOP.value, UserRoleTypes.FOUNDER.value]],
            UserRoleTypes.ESOP.value: [[UserRoleTypes.PRIVATE_BANKS.value, UserRoleTypes.FOUNDER.value], [UserRoleTypes.INVESTOR.value, UserRoleTypes.DEALER.value]],
        }
        combination_blocks = role_combination_na.get(role, [])
        for combination in combination_blocks:
            if all(x in user_roles for x in combination):
                return 2
        return 0

    @staticmethod
    def fetch_user_obj(data):
        email = data.get('email')
        mobile_num = data.get('phoneNumber')
        if email:
            user = User.objects.filter(email=email).last()
        else:
            user = User.objects.filter(username=mobile_num).last()
        return user

    @staticmethod
    def set_user_password(user_obj, password):
        user_obj.set_password(password)
        user_obj.save()

    @staticmethod
    def apply_referral(user_obj, referred_id):
        profileUser = userRoles.objects.get(profile_owner=user_obj)
        profileUser.referred_by_id = referred_id
        try:
            referrer_profile = userRoles.objects.get(profile_username=referred_id)
            profileUser.referred_by_user = referrer_profile.profile_owner
        except:
            pass
        profileUser.save()

    @staticmethod
    def fetch_roles():
        login_roles = list(roles.objects.all().values_list('name', flat=True))
        return {'login_roles': login_roles}

    def get_user_basic_info(self, user_id, user_obj, user_role):
        email = user_obj.email
        user_type = UserTypes.LIVE
        onb_conf = self.user_onboarded(user_obj)
        if email and onb_conf.get('email_verified') and (
                email.split('@')[-1] == 'uixlabs.in' or email.split('+')[0] == 'vishalpandey317'):
            user_type = UserTypes.INTERNAL
        return {
            'current_user_role': user_role,
            'username': user_obj.username,
            'admin_access': user_obj.is_staff or user_obj.is_superuser,
            'email': email,
            'user_id': user_id,
            'user_type': user_type,
            'onboarding_config': onb_conf
        }

    def get_login_creds(self, user, user_role):
        if user_role == UserRoleTypes.INSTITUTIONAL.value:
            user_role = UserRoleTypes.VC.value
        token = self.generate_user_token(user, user_role)
        data = {
            'refresh': str(token),
            'access_token': str(token.access_token),
        }
        data.update(**self.get_user_basic_info(user_id=user.id, user_obj=user, user_role=user_role))
        return data

    def _get_user_roles(self, user):
        user_roles = list(
            userRoles.objects.filter(profile_owner=user).values_list('profile_roles__name', flat=True))
        return user_roles

    def fetch_user_roles(self, user):
        user_roles = self._get_user_roles(user)
        return {
            'user_roles': user_roles
        }

    def change_user_role(self, user, current_role, user_role):
        user_roles = self._get_user_roles(user)
        if user_role not in user_roles or user_role == current_role:
            return {'status': False, 'message': "invalid role"}
        data = self.get_login_creds(user, user_role)
        return {'status': True, 'data': data}

    def user_onboarded(self, user_obj):
        onboarding_status = False
        wa_verified, email_verified = check_email_whatsapp_verification_status(user_obj)
        password_generated = True if user_obj.password and user_obj.has_usable_password() else False
        pin_set = False
        otp_data = otp_authentication.objects.filter(userProfile=user_obj).values('login_pin', 'email_verified',
                                                                                  'phone_verified').last()
        if otp_data:
            if otp_data.get('login_pin'):
                pin_set = True
            if otp_data.get('email_verified'):
                email_verified = True
            if otp_data.get('phone_verified'):
                wa_verified = True
        if password_generated and wa_verified and email_verified and user_obj.is_active:
            onboarding_status = True
        return {
            'wa_verified': wa_verified,
            'email_verified': email_verified,
            'is_active': user_obj.is_active,
            'password_generated': password_generated,
            'onboarding_status': onboarding_status,
            'pin_set': pin_set,
        }

    @staticmethod
    def get_user_roles(user):
        user_types = list(
            userRoles.objects.filter(profile_owner=user).values_list('profile_roles__name', flat=True))
        return user_types

    def user_login_state(self, data, login_type, domain, poll=None, version='v1', headers={}):
        email = data.get('email')
        mobile_num = data.get('phoneNumber')
        country_code = data.get('countryCode')
        send_otp = data.get('sendOtp')
        email_sent, user_registered, wa_sent, status = None, False, None, True
        onboard = {}
        msg = ''
        user_types = []
        if email or (mobile_num and country_code):
            if email:
                user = User.objects.filter(email=email).last()
                if not user:
                    resp = self.register_user(email, login_type, headers=headers)
                    user = resp.get('user')
            else:
                user = User.objects.filter(username=mobile_num).last()
                if not user:
                    resp = self.register_user(None, login_type, mobile_num=mobile_num, headers=headers)
                    user = resp.get('user')
            if user:
                onboard = self.user_onboarded(user)
                if onboard.get('password_generated') and (onboard.get('email_verified') or onboard.get('wa_verified')):
                    user_registered = True
                user_types = self._get_user_roles(user)
                user_low_types = [i.lower() for i in user_types]
                if user_low_types and login_type.lower() not in user_low_types:
                    if onboard and onboard.get('onboarding_status') and self.validate_role(user, login_type,
                                                                                           user_types) != 2:
                        #  not block users for changing profile
                        pass
                    else:
                        status = False
                        msg = f'User is already registered with types - {user_low_types[0]}'
                else:
                    if email and (not onboard.get('email_verified') or (
                            not onboard.get('password_generated') and not poll)):
                        onboard['email_verified'] = False
                        otp = None
                        if send_otp:
                            otp = OtpOrchestrator().fetch_otp(user, data)
                        email_sent = self.send_email_verification_mail(user, email, domain,
                                                                       user_action="app_login_email_verify",
                                                                       login_type=login_type, otp=otp)
                        if email_sent:
                            msg = f"To verify your email, we've sent a verification link to {email}. Please check your updates Promotions/Spam folder in case you don’t find our email in your inbox."
                            if send_otp:
                                msg = f"To verify your email, we've sent an otp to {email}. Please check your updates Promotions/Spam folder in case you don’t find our email in your inbox."
                        elif email_sent is False:
                            msg = 'We are facing some issues at the moment , please try again later'
                            status = False
                    elif mobile_num and (not onboard.get('wa_verified') or (
                            not onboard.get('password_generated') and not poll)):
                        onboard['wa_verified'] = False
                        resp = WhatsappLead(mobile_num, country_code).add_user_number(user, domain=domain,
                                                                                      action_type='app_login_whatsapp_verify',
                                                                                      login_type=login_type,
                                                                                      bypass_verif_check=True,
                                                                                      send_otp=send_otp)

                        msg = resp.get('message')
                        if not resp.get('status'):
                            status = False
                        wa_sent = status

            else:
                status = False
                msg = 'Something Went wrong, try again later'
        else:
            status = False
            msg = 'Enter a valid data points'
        data = {
            'user_registered': user_registered,
            'validation_email_sent': email_sent,
            'validation_wa_sent': wa_sent,
            'validation_sent': email_sent or wa_sent,
            'onboarding_config': onboard,
            'user_types': user_types}
        return {'status': status, 'message': msg, 'data': data}

    @staticmethod
    def set_user_pass(user):
        user.password = uuid.uuid4().hex
        user.save()

    @staticmethod
    def add_user_role(user, role, platform=''):
        if role == UserRoleTypes.INSTITUTIONAL.value:
            role = UserRoleTypes.VC.value
        roleForUser = roles.objects.get(name=role)
        roleOfUser, created = userRoles.objects.get_or_create(profile_owner=user, defaults={'platform': platform})
        roleOfUser.profile_roles.add(roleForUser)
        roleOfUser.save()

    def register_user(self, email, login_type, verified=False, mobile_num=None, headers={}):
        email_sent = False
        user = None
        try:
            username = email if email else mobile_num
            user = User.objects.create(
                username=username,
                email=email or '',
                is_active=False
            )
            if verified:
                self.set_user_pass(user)
            else:
                user.set_unusable_password()
            platform = headers.get('platform', 'app')
            self.add_user_role(user, login_type, platform)
            if login_type == UserRoleTypes.INVESTOR.value:
                if verified:
                    self.verify_email(user)
                else:
                    self.register_investor(user)
            user.save()
            user_registered = True
        except Exception as e:
            user_registered = False
        return {'email_sent': email_sent, 'user_registered': user_registered, 'user': user}

    def reset_user_password(self, data, domain, login_type):
        status = False
        email = data.get('email')
        mobile_num = data.get('phoneNumber')
        country_code = data.get('countryCode')
        send_otp = data.get('sendOtp', None)
        user = self.fetch_user_obj(data)
        if user:
            otp = None
            if send_otp:
                otp = OtpOrchestrator().fetch_otp(user, data)
            if email:
                status = self.send_password_reset_email(user, email, domain, login_type, otp)
            else:
                statusCode = send_whatsapp_verification(domain, user, mobile_num, country_code, login_type, "reset",
                                                        otp=otp)
                if statusCode == 202 or statusCode == 200 or statusCode == 201:
                    status = True
            msg = f"To reset your password, we've sent {'a verification link' if not send_otp else 'an otp'} to {email or mobile_num}" if status else 'We are facing some issues at the moment , please try again later'
        else:
            msg = 'Email is not registered ,Please check your email again.'
        return {'status': status, 'message': msg}

    def add_user_email(self, email, domain, login_type, user, send_otp=None):
        status = False
        if user and user.id:
            if User.objects.filter(email=email).exclude(id=user.id).exists():
                msg = 'Email is already linked with some other account'
                return {'status': status, 'message': msg}
            onb_config = self.user_onboarded(user)
            if not onb_config.get('email_verified'):
                user.email = email
                user.save()
                otp = None
                if send_otp:
                    otp = OtpOrchestrator().fetch_otp(user, {'email': email})
                status = self.send_email_verification_mail(user, email, domain,
                                                           user_action="app_login_email_verify",
                                                           login_type=login_type, otp=otp)
                if status:
                    msg = f"To verify your email, we've sent a verification link to {email}. Please check your updates Promotions/Spam folder in case you don’t find our email in your inbox."
                else:
                    msg = 'We are facing some issues at the moment , please try again later'
            else:
                msg = 'Email is already verified ,Please check your email again.'
        else:
            msg = 'User is not registered ,Please check your email again.'
        return {'status': status, 'message': msg}

    def send_email_verification_mail(self, user, email, domain, user_action=None, login_type=None, otp=None):
        if login_type:
            mail_subject = f'Activate your Planify {login_type} account.'
        else:
            mail_subject = f'Activate your Planify Account.'
        if otp:
            context = {
                'otp': otp,
            }
            message = render_to_string('authApp/mails/otp_mail.html', context)
            html = True
        else:
            html = False
            message = render_to_string('authApp/mails/activateAccountEmail.html', {
                'user': user,
                'domain': domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
                'type': login_type,
                'action': user_action,

            })
        return NotificationMaster.send_email(mail_subject, message, email, html=html)

    def send_password_reset_email(self, user, email, domain, login_type=None, otp=None):
        if login_type:
            mail_subject = f'Reset your Planify {login_type} account.'
        else:
            mail_subject = f'Reset your Planify Account.'
        if otp:
            context = {
                'otp': otp,
            }
            message = render_to_string('authApp/mails/otp_mail.html', context)
            html = True
        else:
            html = False
            message = render_to_string('authApp/mails/activateAccountEmail.html', {
                'user': user,
                'domain': domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
                'type': login_type,
                'action': "reset",

            })
        return NotificationMaster.send_email(mail_subject, message, email, html=html)

    def generate_user_token(self, user, user_role=None):
        if user_role == UserRoleTypes.INSTITUTIONAL.value:
            user_role = UserRoleTypes.VC.value
        token = RefreshToken.for_user(user)
        token['user_role'] = user_role
        return token

    @classmethod
    def set_pin(cls, user, data, otp_obj=None):
        resp = {'status': False, 'message': 'Invalid Request.'}
        old_pin = data.get('old_pin')
        if not user or not user.id:
            return resp
        otpInst = otp_obj if otp_obj else otp_authentication.objects.filter(userProfile=user).last()
        if not otpInst:
            otpInst = otp_authentication(userProfile=user)
            otpInst.save()
        if not otpInst or not data.get('pin') or (otpInst.login_pin and not old_pin):
            return resp
        if old_pin and otpInst.login_pin != old_pin:
            resp['message'] = 'Invalid Pin'
            return resp
        otpInst.login_pin = data.get('pin')
        otpInst.save()
        resp["status"] = True
        resp['message'] = 'Success'
        return resp

    def send_mpin_reset_otp(self, user, domain):
        resp = {'status': False, 'message': 'We are facing some issues at the moment , please try again later'}
        data = {'email': user.email}
        otp = OtpOrchestrator().fetch_otp(user, data)
        em_status = self.send_password_reset_email(user, user.email, domain, None, otp)
        wa_status = send_whatsapp_verification(domain, user, user.profileOwnerWL.phoneNumber,
                                               user.profileOwnerWL.countryCode, None,
                                               "reset",
                                               otp=otp)
        if wa_status in [202, 200, 201] or em_status:
            resp["status"] = True
            msg = f"we've sent an otp to {user.email if em_status else user.username}"
            if em_status and wa_status in [202, 200, 201]:
                msg += f' and your whatsapp {user.username}'
            resp['message'] = msg
        return resp

    def validate_reset_mpin(self, user, data):
        resp = {'status': False, 'message': "invalid otp"}
        data["email"] = user.email
        data["phoneNumber"] = user.username
        otp_obj, _ = otp_authentication.objects.get_or_create(userProfile=user)
        data["old_pin"] = otp_obj.login_pin
        validation_status, requested = OtpOrchestrator().validate_otp(user, data, otp_obj)
        if not validation_status:
            return resp
        return self.set_pin(user, data, otp_obj)

    @classmethod
    def validate_pin(cls, user, data):
        resp = {'status': False, 'message': 'Invalid Request.'}
        if not user or not user.id:
            return resp
        otpInst = otp_authentication.objects.filter(userProfile=user).last()
        if not otpInst or not data.get('pin') or not otpInst.login_pin:
            return resp
        if otpInst.login_pin != data.get('pin'):
            resp['message'] = 'Invalid Pin'
            return resp
        resp["status"] = True
        resp['message'] = 'Success'
        return resp

    @classmethod
    def update_user_device_token(cls, user, platform, data):
        if data.get('token'):
            UserDeviceTokens.upsert_token(user.id, platform, data.get('token'))

    @classmethod
    def verify_email(cls, user):
        try:
            createInvestorPersonalDetails = investorPersonalDetails(profileOwner=user)
            createInvestorPersonalDetails.emailVerified = True
            createInvestorPersonalDetails.save()
            createVerificationStatus = verificationStatus(profileOwner=user)
            createVerificationStatus.save()
        except:
            pass

    @classmethod
    def register_investor(cls, user):
        try:
            createInvestorPersonalDetails = investorPersonalDetails(profileOwner=user)
            createInvestorPersonalDetails.save()
            createVerificationStatus = verificationStatus(profileOwner=user)
            createVerificationStatus.save()
        except:
            pass

    @classmethod
    def verify_whatsapp(cls, user):
        whatsApp_inst = whatsappLeads.objects.get(profileOwner=user)
        whatsApp_inst.verified = True
        whatsApp_inst.save()

    @classmethod
    def activate_user(cls, user):
        user.is_active = True
        user.save()

    def validate_user(self, data, user=None, user_role=None):
        if not user:
            user = self.fetch_user_obj(data)
        if user:
            is_otp_validated, requested = OtpOrchestrator().validate_otp(user, data)
            if is_otp_validated:
                if not user.is_active:
                    self.activate_user(user)
                if requested == 'Email':
                    self.verify_email(user)
                else:
                    self.verify_whatsapp(user)
                resp_data = self.get_login_creds(user, user_role)
                return {'status': True, 'message': 'Verified', 'data': resp_data}
            else:
                return {'status': False, 'message': 'Invalid otp'}
        return {'status': False, 'message': 'invalid request'}


class SocialAuth:

    def __init__(self, vendor):
        self.vendor = vendor

    def process_auth(self, code, login_type, domain, redirect_uri=None, headers={}):
        _resp = {
            'status': 0, 'message': 'unable to connect to the auth'
        }
        profile_data = None

        if self.vendor == 'linkedin':
            profile_data = LinkedInAuth().fetch_profile_detail(code, domain, redirect_uri)
        elif self.vendor == 'google':
            profile_data = GoogleAuth().fetch_profile_detail(code, domain)
        if profile_data and profile_data.get('email') and profile_data.get('email_verified'):
            user_service = UserService()
            user = User.objects.filter(email=profile_data.get('email')).last()
            if not user:
                resp = user_service.register_user(profile_data.get('email'), login_type, verified=True, headers=headers)
                if resp and resp.get('user'):
                    user = resp.get('user')
            if user:
                otpInst, otpInst_created = otp_authentication.objects.get_or_create(userProfile=user)
                if otpInst:
                    if not otpInst.email_verified:
                        user_service.verify_email(user)
                    otpInst.email_verified = True
                    if self.vendor == 'google':
                        otpInst.google_verified = True
                    elif self.vendor == 'linkedin':
                        otpInst.linkedin_verified = True
                    otpInst.save()
                _resp["status"] = 1
                if not user.has_usable_password() or not user.password:
                    user_service.set_user_pass(user)
                if not user.is_active:
                    user.is_active = True
                    user.save()
                data = user_service.get_login_creds(user, login_type)
                _resp["data"] = data
                _resp["message"] = "success"
        return _resp
