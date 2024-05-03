import copy
import datetime
from investorApp.services.kyc.constants import UserRoleTypes
from investorApp.services.kyc.base import KycBase
from investorApp.models import (investorBankDetails, investorDMATDetails,
                                UserTransferFacility, investmentDetails, CompanyDetails, investorPersonalDetails)
from investorApp.services.kyc.config import FOKycConfig, StepName, KycFeConfig
from investorApp.services.kyc.screen_configs.family_office_config import COMPANY_DETAIL_SECTION, COMPANY_DETAIL_PAGE_CONF
from investorApp.services.kyc.util import (fill_template_config, fetch_screen_options)
from investorApp.services.kyc.common_kyc import CommonKycConfig


class FamilyOfficeKyc(KycBase):
    role = UserRoleTypes.FO.value
    _instance = None

    def __init__(self, user):
        self.user = user
        self.steps = FOKycConfig
        self.common_kyc = CommonKycConfig(self.user, self.role)
        self.investor_obj = investorPersonalDetails.fetch_obj(user.id)
        self.investment_detail_obj, _ = investmentDetails.objects.get_or_create(profileOwner=user,
                                                                                defaults={'user_role': self.role})
        super(FamilyOfficeKyc, self).__init__(user)

    def get_role_name(self):
        return self.role

    def is_user_pd_step_done(self):
        data = self.investor_obj.__dict__
        if type(data.get('contact_person')) in [str, None, datetime.datetime, int, float] and data.get(
                'contact_person') in [None, '']:
            return False
        return True

    def is_company_detail_step_done(self):
        data = CommonKycConfig(self.user, self.role).__dict__
        if type(data.get('city')) in [str, None, datetime.datetime, int, float] and data.get(
                'city') in [None, '']:
            return False
        return True

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
            elif step == StepName.COMPANY_DETAILS and not self.is_company_detail_step_done():
                pending_steps.append(step)
            elif step == StepName.D_MAT_DETAILS and not self.is_user_dmat_step_done():
                pending_steps.append(step)
            elif step == StepName.TRANSFER_FACILITY and not self.is_user_facility_step_done():
                pending_steps.append(step)
        return pending_steps

    def _fetch_personal_detail_conf(self):
        screen_conf = self.common_kyc.fetch_user_personal_detail_conf(self.investor_obj)
        return screen_conf

    def _fetch_investment_detail_conf(self):
        screen_conf = self.common_kyc.fetch_investment_detail_conf(self.investment_detail_obj)
        return screen_conf

    def _fetch_company_detail_conf(self):
        step = StepName.COMPANY_DETAILS
        screen_conf = copy.deepcopy(COMPANY_DETAIL_PAGE_CONF)
        section = copy.deepcopy(COMPANY_DETAIL_SECTION)
        obj = CompanyDetails.fetch_obj(self.user.id, self.role)
        data = obj.__dict__
        data['company_sector'] = list(obj.company_sector.values_list('id', flat=True))
        data["license_proof_url"] = obj.license_proof.url if obj.license_proof else ''
        data["gst_proof_url"] = obj.gst_proof.url if obj.gst_proof else ''
        data["upload_pan_url"] = obj.upload_pan.url if obj.upload_pan else ''
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
            StepName.COMPANY_DETAILS: self._fetch_company_detail_conf,
            StepName.BANK_DETAILS: self._fetch_bank_detail_conf,
            StepName.D_MAT_DETAILS: self._fetch_dmat_conf,
            StepName.TRANSFER_FACILITY: self._fetch_facility_conf,
            StepName.INVESTMENT_DETAILS: self._fetch_investment_detail_conf
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
            "heading": "Family Office Kyc",
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
        if step == StepName.INVESTMENT_DETAILS:
            instance = self.investment_detail_obj
        elif step == StepName.PERSONAL_DETAILS:
            instance = self.investor_obj
        return self.common_kyc.update_kyc_details(step, data, instance)

    def upload_kyc_docs(self, step, files, data):
        instance = None
        if step == StepName.INVESTMENT_DETAILS:
            instance = self.investment_detail_obj
        elif step == StepName.PERSONAL_DETAILS:
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
        return self.common_kyc.fetch_field_options(self.investor_obj, field, query_params)

    def delete_kyc_details(self, step, pk: str):
        return self.common_kyc.delete_kyc_details(step, pk)
