import requests
from django.conf import settings


class LinkedInAuth:

    @classmethod
    def fetch_access_token(cls, code: str, domain: str, redirect_uri: str = None):
        resp_data = None
        url = "https://www.linkedin.com/oauth/v2/accessToken"
        data = {
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': redirect_uri if redirect_uri else f'{domain}/social-login-verify/',
            'client_id': settings.LINKED_IN_APP_AUTH_KEY,
            'client_secret': settings.LINKED_IN_APP_AUTH_SECRET,
        }
        resp = requests.post(url, json=data)
        if resp.ok:
            resp_data = resp.json()
        return resp_data

    def fetch_profile_detail(self, code: str, domain: str, redirect_uri: str = None):
        resp_data = None
        data = self.fetch_access_token(code, domain, redirect_uri)
        if data and data.get('accessToken'):
            url = "https://api.linkedin.com/v2/me"
            headers = {'Authorization': f'Bearer {data.get("accessToken")}'}
            resp = requests.get(url, headers=headers)
            if resp.ok:
                resp_data = resp.json()
        return resp_data


class GoogleAuth:
    def fetch_profile_detail(self, code: str, domain: str):
        return self.fetch_token_info(code)

    def fetch_token_info(self, token: str):
        try:
            url = f'https://oauth2.googleapis.com/tokeninfo?id_token={token}'
            resp = requests.get(url)
            if resp.ok:
                data = resp.json()
                # if data['aud'] != settings.SOCIAL_AUTH_GOOGLE_OAUTH2_KEY:
                #     return None
                return data
        except:
            pass
        return None
