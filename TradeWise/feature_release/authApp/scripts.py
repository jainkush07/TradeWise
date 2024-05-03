from django.contrib.auth.models import User
from authApp.services.user_service import UserService
from whatsappAuthApp.models import whatsappLeads
from authNewApp.models import otp_authentication


def register_users(data_list):
    user_service = UserService()
    for data in data_list:
        user = None
        email = data.get('email') if data.get('email') and str(data.get('email')) != 'nan' else None
        phone = data.get('phoneNumber') if data.get('phoneNumber') and str(data.get('phoneNumber')) != 'nan' else None
        if email or phone:
            if email:
                user = User.objects.filter(email=data.get('email')).last()
            elif phone:
                user = User.objects.filter(username=data.get('phoneNumber')).last()
            if not user:
                if email:
                    verified = True
                else:
                    verified = False
                resp = user_service.register_user(email, 'INVESTOR', verified=verified, mobile_num=phone)
                if resp and resp.get('user'):
                    user = resp.get('user')
                    user.is_active = True
                    user.set_unusable_password()
                    user.save()
                    if phone:
                        wa_obj = whatsappLeads.objects.filter(phoneNumber=phone).last()
                        if not wa_obj:
                            wa_obj = whatsappLeads(phoneNumber=phone, countryCode="+91")
                            wa_obj.profileOwner = user
                            wa_obj.verified = True
                            wa_obj.save()
                    otpInst, otpInst_created = otp_authentication.objects.get_or_create(userProfile=user)
                    if otpInst:
                        otpInst.email_verified = True
                        otpInst.phone_verified = True
                    otpInst.save()
