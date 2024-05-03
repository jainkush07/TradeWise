import requests
from django.conf import settings
from authApp.models import UserDeviceTokens, NotificationTemplates
from django.core.mail import EmailMessage
from django.core.mail import send_mail
from django.template import Template, Context


class NotificationMaster:

    @staticmethod
    def send_email(mail_subject, message, to_email, html=False):
        try:
            if html:
                send_mail(
                    subject=mail_subject,
                    message='',
                    from_email='reports@planify.in',
                    recipient_list=[to_email],
                    html_message=message,
                )
            else:
                email = EmailMessage(
                    subject=mail_subject,
                    body=message,
                    from_email='reports@planify.in',
                    to=[to_email]
                )
                email.send()
        except:
            return False
        return True

    def send_push_notification(self, user_id, template_name: str, payload: dict = {}, platform: str = None):
        try:
            token_data = UserDeviceTokens.get_user_device_token(user_id, platform)
            notif_obj = NotificationTemplates.fetch_obj(template_name)
            if token_data and notif_obj:
                token = token_data.get('token')
                title = notif_obj.title
                body = notif_obj.body
                if payload:
                    title = Template(title).render(Context(payload))
                    body = Template(body).render(Context(payload))
                return self._push_device_notification(token, title, body)
        except:
            pass
        return False

    def _push_device_notification(self, token, title, body):
        # https://stackoverflow.com/questions/37490629/firebase-send-notification-with-rest-api
        # https://medium.com/@mail2ashislaha/rich-push-notification-with-firebase-cloud-messaging-fcm-and-pusher-in-ios-platform-8b4e9922120
        url = f'https://fcm.googleapis.com/fcm/send'
        push_payload = {
            "to": token,
            "notification": {
                "title": title,
                "body": body
            },
            'data': {}
        }
        headers = {
            'Authorization': settings.FCM_SECRET_KEY
        }
        resp = requests.post(url, json=push_payload, timeout=10, headers=headers)
        if resp.ok:
            jsn_resp = resp.json()
            if jsn_resp and jsn_resp.get('success'):
                return True
        return False
