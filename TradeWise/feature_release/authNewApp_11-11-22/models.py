from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


STATUS_CHOICES = (
	('draft', 'Draft'),
	('published', 'Published'),
)


#
class otp_authentication(models.Model):
	userProfile = models.OneToOneField(User, on_delete=models.CASCADE, related_name="userProfile_otp_authentication_authV2")
	mobile = models.CharField(max_length=256, null=True, blank=True)
	country_code = models.CharField(max_length=5, null=True, blank=True)
	email = models.CharField(max_length=256, null=True, blank=True)
	otp = models.CharField(max_length=256, null=True, blank=True)
	login_pin = models.CharField(max_length=256, null=True, blank=True)
	requested_on = models.CharField(max_length=10, choices=(('Mobile','Mobile'),('Email', 'Email'),), default='Email')
	requested_for = models.CharField(max_length=10, choices=(('Login','Login'),('Signup', 'Signup'),('Verify', 'Verify'),), default='Signup')
	email_verified = models.BooleanField(default=False)
	phone_verified = models.BooleanField(default=False)
	google_verified = models.BooleanField(default=False)
	linkedin_verified = models.BooleanField(default=False)
	onboarding_popup = models.BooleanField(default=False)
	author = models.CharField(max_length=1000, null=True, blank=True)
	publish = models.DateTimeField(default=timezone.now)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now_add=True)
	status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

	def __str__(self):
		return f'User: {self.userProfile.username} request OTP on: {self.requested_on} have OTP: {self.otp}' or '--name not provided--'

	class Meta:
		verbose_name_plural = 'OTP Authentication'