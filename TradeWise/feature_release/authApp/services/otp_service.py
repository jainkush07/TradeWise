import random
from authNewApp.models import otp_authentication


class OtpOrchestrator:

    @staticmethod
    def generate_otp():
        otp = str(random.randint(1000, 9999))
        return otp

    def fetch_otp(self, user, data: dict):
        otpInst, otpInst_created = otp_authentication.objects.get_or_create(userProfile=user)
        if data.get('email'):
            otpInst.email = data.get('email')
            otpInst.requested_on = 'Email'
        else:
            otpInst.mobile = data.get('phoneNumber')
            otpInst.country_code = data.get('countryCode')
            otpInst.requested_on = 'Mobile'
        otp = self.generate_otp()
        otpInst.otp = otp
        otpInst.save()
        return otp

    def validate_otp(self, user, data, otp_obj=None):
        otpInst = otp_obj if otp_obj else otp_authentication.objects.get(userProfile=user)
        status = False
        if str(otpInst.otp) == str(data.get('otp')):
            if otpInst.requested_on == 'Email':
                otpInst.email_verified = True
                status = True
                otpInst.save()
            elif otpInst.requested_on == 'Mobile':
                otpInst.phone_verified = True
                status = True
                otpInst.save()
        return status, otpInst.requested_on
