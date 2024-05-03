from django.urls import path, re_path
from . import views

app_name = 'authNewApp'

urlpatterns = [
	path('social-login-verify/', views.social_login_view, name='social_login_url'),
	path('resend-otp/', views.resent_otp_ajax_view, name='resent_otp_ajax_url'),
	path('login/authenticate/', views.existing_user_login_view, name="existing_user_login_url"),
	path('login/existing-authenticate/', views.existing_user_submit_view, name="existing_user_submit_url"),
	path('otp-verification/', views.otp_submit_and_activate_view, name="otp_submit_and_activate_url"),
	path('user-password/', views.create_or_update_user_password_view, name="create_or_update_user_password_url"),
	path('user-password/<slug:slug>', views.password_reset_view, name="password_reset_url"),
	# path('user-PIN/', views.create_or_update_user_login_PIN_view, name="create_or_update_user_login_PIN_url"),
	path('2-step-auth/', views.user_create_update_or_verify_pin_view, name="try_login_by_pin_url"),
	path('2-step-auth/<slug:slug>/', views.user_create_update_or_verify_pin_view, name="user_create_update_or_verify_pin_url"),
	path('update-whatsapp/', views.user_whatsapp_update_view, name="user_whatsapp_update_url"),
	path('update-email/', views.user_email_update_view, name="user_email_update_url"),
	path('login-checkpoint/', views.otp_authentication_submit_view, name="otp_authentication_submit_url"),
	path('login/', views.login_signup_first_view, name="login_signup_first_url"),
	path('logout/', views.logout_view, name="logout_url"),
]
