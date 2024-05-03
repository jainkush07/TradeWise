import copy
import datetime
from investorApp.services.kyc.base import KycBase
from investorApp.models import (investorPersonalDetails, investorBankDetails, investorDMATDetails, UserTransferFacility,
                                UserEsopDetails)
from investorApp.services.kyc.constants import UserRoleTypes
from investorApp.services.kyc.config import EsopKycConfig, StepName, KycFeConfig
from investorApp.services.kyc.screen_configs.esop_config import ESOP_DETAIL_SECTION, ESOP_DETAIL_PAGE_CONF, \
    VALUATION_SUB_COMPONENT
from investorApp.services.kyc.util import (fill_template_config,
                                           fetch_screen_options)
from investorApp.services.kyc.common_kyc import CommonKycConfig


class ESOPKyc(KycBase):
    role = UserRoleTypes.ESOP.value
    _instance = None

    def __init__(self, user):
        self.user = user
        self.steps = EsopKycConfig
        self.common_kyc = CommonKycConfig(self.user, self.role)
        self.investor_obj = investorPersonalDetails.fetch_obj(user.id)
        super(ESOPKyc, self).__init__(user)

    def get_role_name(self):
        return self.role

    def is_user_pd_step_done(self):
        if not self.investor_obj:
            return False
        data = self.investor_obj.__dict__
        for key, val in data.items():
            if type(val) in [str, None, datetime.datetime, int, float] and val in [None, '']:
                return False
        return True

    def is_company_detail_step_done(self):
        return UserEsopDetails.objects.filter(user_id=self.user.id).exists()

    def is_user_bank_step_done(self):
        return investorBankDetails.objects.filter(profileOwner_id=self.user.id, ifsc_Code__isnull=False).exists()

    def is_user_dmat_step_done(self):
        return investorDMATDetails.objects.filter(profileOwner_id=self.user.id, dpID__isnull=False).exists()

    def is_user_facility_step_done(self):
        return UserTransferFacility.objects.filter(user_id=self.user.id, role=self.role,
                                                   transfer_type__isnull=False).exists()

    def get_pending_steps(self):
        pending_steps = []
        for step in self.steps:
            if step == StepName.PERSONAL_DETAILS and not self.is_user_pd_step_done():
                pending_steps.append(step)
            elif step == StepName.BANK_DETAILS and not self.is_user_bank_step_done():
                pending_steps.append(step)
            elif step == StepName.ESOP_COMPANY_DETAILS and not self.is_company_detail_step_done():
                pending_steps.append(step)
            elif step == StepName.D_MAT_DETAILS and not self.is_user_dmat_step_done():
                pending_steps.append(step)
            elif step == StepName.TRANSFER_FACILITY and not self.is_user_facility_step_done():
                pending_steps.append(step)
        return pending_steps

    def _fetch_user_description_conf(self):
        return self.common_kyc.fetch_user_description_conf()

    def _fetch_personal_detail_conf(self):
        return self.common_kyc.fetch_user_personal_detail_conf(self.investor_obj)

    def _fetch_esop_detail_conf(self):
        step = StepName.ESOP_COMPANY_DETAILS
        screen_conf = copy.deepcopy(ESOP_DETAIL_PAGE_CONF)
        section = copy.deepcopy(ESOP_DETAIL_SECTION)
        obj = UserEsopDetails.fetch_obj(self.user.id)
        data = obj.__dict__
        data['valuation'] = data['valuation'] or ''
        data['shares_owned'] = data['shares_owned'] or ''
        if data and data['valuation_status'] == 'Yes':
            section['components'].insert(-1, copy.deepcopy(VALUATION_SUB_COMPONENT))
        data.update(fetch_screen_options(step, self.role, data))
        section = fill_template_config(section, data, step)
        screen_conf['sections'] = [section]
        return screen_conf

    def _fetch_facility_conf(self):
        screen_conf = self.common_kyc.fetch_facility_conf()
        return screen_conf

    def _fetch_bank_detail_conf(self):
        screen_conf = self.common_kyc.fetch_bank_config()
        return screen_conf

    def _fetch_dmat_conf(self):
        screen_conf = self.common_kyc.fetch_dmat_config()
        return screen_conf

    def fetch_kyc_page_config(self, step):
        step_map = {
            StepName.PERSONAL_DETAILS: self._fetch_personal_detail_conf,
            StepName.ESOP_COMPANY_DETAILS: self._fetch_esop_detail_conf,
            StepName.BANK_DETAILS: self._fetch_bank_detail_conf,
            StepName.D_MAT_DETAILS: self._fetch_dmat_conf,
            StepName.TRANSFER_FACILITY: self._fetch_facility_conf
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
            "heading": "Esop Registeration",
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
        elif step == StepName.ESOP_COMPANY_DETAILS:
            instance = UserEsopDetails.fetch_obj(self.user.id)
        return self.common_kyc.update_kyc_details(step, data, instance)

    def upload_kyc_docs(self, step, files, data):
        instance = None
        if step == StepName.PERSONAL_DETAILS:
            instance = self.investor_obj
        elif step == StepName.ESOP_COMPANY_DETAILS:
            instance = UserEsopDetails.fetch_obj(self.user.id)
        return self.common_kyc.upload_kyc_docs(step, files, data, instance)

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
        return self.common_kyc.fetch_field_options(self.investor_obj, field, query_params)

    def delete_kyc_details(self, step, pk: str):
        return self.common_kyc.delete_kyc_details(step, pk)
