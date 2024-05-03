import copy
import datetime
from investorApp.services.kyc.constants import UserRoleTypes
from investorApp.services.kyc.base import KycBase
from investorApp.models import (investorPersonalDetails, UserSocialDetails)
from investorApp.services.kyc.config import AuthorKycConfig, StepName, KycFeConfig
from investorApp.services.kyc.util import (fill_template_config,
                                           fetch_screen_options, fetch_fields_option)
from investorApp.services.kyc.common_kyc import CommonKycConfig


class AuthoreKyc(KycBase):
    role = UserRoleTypes.AUTHORE.value
    _instance = None

    def __init__(self, user):
        self.user = user
        self.steps = AuthorKycConfig
        self.common_kyc = CommonKycConfig(self.user, self.role)
        self.investor_obj = investorPersonalDetails.fetch_obj(user.id)
        super(AuthoreKyc, self).__init__(user)

    def get_role_name(self):
        return self.role

    def is_user_pd_step_done(self):
        data = self.investor_obj.__dict__
        for key, val in data.items():
            if type(val) in [str, None, datetime.datetime, int, float] and val in [None, '']:
                return False
        return True

    def is_social_info_done(self):
        return UserSocialDetails.objects.filter(user_id=self.user.id).exclude(is_fin_influencer='').exists()

    def get_pending_steps(self):
        pending_steps = []
        for step in self.steps:
            if step == StepName.PERSONAL_DETAILS and not self.is_user_pd_step_done():
                pending_steps.append(step)
            elif step == StepName.SOCIAL_INFORMATION and not self.is_social_info_done():
                pending_steps.append(step)
        return pending_steps

    def _fetch_personal_detail_conf(self):
        return self.common_kyc.fetch_user_personal_detail_conf(self.investor_obj)

    def _fetch_user_description_conf(self):
        return self.common_kyc.fetch_user_description_conf()

    def fetch_kyc_page_config(self, step):
        step_map = {
            StepName.PERSONAL_DETAILS: self._fetch_personal_detail_conf,
            StepName.SOCIAL_INFORMATION: self._fetch_user_description_conf
        }
        if step not in step_map.keys():
            return {"status": False, "message": "Invalid screen"}
        screen = step_map[step]()
        return {"status": True, "data": screen}

    def fetch_kyc_config(self, step=None):
        pending_steps = self.get_pending_steps()
        current_step = None
        if step and step in self.steps:
            current_step = step
        elif pending_steps:
            current_step = pending_steps[0]
        elif self.steps:
            current_step = self.steps[-1]
        total_steps = len(self.steps)
        pending_steps_count = len(pending_steps)
        steps = []
        for step in self.steps:
            conf = KycFeConfig.get(step)
            conf['state'] = 'pending' if step in pending_steps else 'completed'
            steps.append(conf)
        config = {
            "page": "",
            "type": "kyc",
            "heading": "Authore Kyc",
            "subHeading": "",
            "progress": {
                "percentage": int(((total_steps - pending_steps_count) / total_steps) * 100)
            },
            "steps": steps,
            'current_step': current_step
        }
        return config

    def update_kyc_details(self, step, data: dict):
        instance = None
        if step == StepName.PERSONAL_DETAILS:
            instance = self.investor_obj
        return self.common_kyc.update_kyc_details(step, data, instance)

    def upload_kyc_docs(self, step, files, data):
        instance = None
        if step == StepName.PERSONAL_DETAILS:
            instance = self.investor_obj
        return self.common_kyc.upload_kyc_docs(step, data, files, instance)

    def complete_kyc(self):
        resp = {'status': False, "message": ""}
        pending_steps = self.get_pending_steps()
        if pending_steps:
            resp["message"] = 'Steps are pending, please complete'
            resp["pending_steps"] = pending_steps
        else:
            resp["status"] = True
        return resp

    def fetch_field_options(self, field, query_params):
        data = self.investor_obj.__dict__
        return fetch_fields_option(self.role, field, query_params, data)

    def delete_kyc_details(self, step, pk: str):
        return self.common_kyc.delete_kyc_details(step, pk)
