import copy
import datetime
from whatsappAuthApp.models import whatsappLeads
from investorApp.services.kyc.base import KycBase
from investorApp.models import (investorPersonalDetails, investorBankDetails, investmentDetails, investorDMATDetails,
                                )
from investorApp.services.kyc.config import InvestorKycConfig, StepName, KycFeConfig
from investorApp.forms import (investorPersonalDetailsForm, investmentDetailsForm, investorBankDetailsForm,
                               investorDMATDetailsForm)
from investorApp.services.kyc.screen_configs.investor_page_config import (PERSONAL_DETAIL_PAGE_CONF,
                                                                          PERSONAL_DETAIL_SECTION,
                                                                          BANK_DETAIL_PAGE_CONF, BANK_DETAIL_SECTION,
                                                                          DMAT_SECTION, DMAT_PAGE_CONF)
from investorApp.services.kyc.screen_configs.common_config import INVESTMENT_DETAIL_SECTION, \
    PRIMARY_INVESTMENT_SUB_COMPONENT, \
    INVESTMENT_DETAIL_PAGE_CONF
from investorApp.services.kyc.util import (fill_template_config,
                                           fetch_fields_option,
                                           fetch_screen_options, format_kyc_data)
from investorApp.services.kyc.constants import InvestmentMarket
from investorApp.services.kyc.validators import validate_step_data
from investorApp.services.kyc.common_kyc import CommonKycConfig


class InvestorKyc(KycBase):
    role = 'INVESTOR'
    _instance = None

    def __init__(self, user):
        self.user = user
        self.steps = InvestorKycConfig
        self.common_kyc = CommonKycConfig(self.user, self.role)
        self.investor_obj = investorPersonalDetails.fetch_obj(user.id)
        self.investment_detail_obj, _ = investmentDetails.objects.get_or_create(profileOwner=user)
        super(InvestorKyc, self).__init__(user)

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

    def is_user_invest_detail_step_done(self):
        if not self.investment_detail_obj:
            return False
        data = self.investment_detail_obj.__dict__
        for key, val in data.items():
            if type(val) in [str, None, datetime.datetime, int, float] and val in [None, '']:
                return False
        return True

    def is_user_bank_step_done(self):
        return investorBankDetails.objects.filter(profileOwner_id=self.user.id, ifsc_Code__isnull=False).exists()

    def is_user_dmat_step_done(self):
        return investorDMATDetails.objects.filter(profileOwner_id=self.user.id, dpID__isnull=False).exists()

    def get_pending_steps(self):
        pending_steps = []
        for step in self.steps:
            if step == StepName.PERSONAL_DETAILS and not self.is_user_pd_step_done():
                pending_steps.append(step)
            elif step == StepName.BANK_DETAILS and not self.is_user_bank_step_done():
                pending_steps.append(step)
            elif step == StepName.INVESTMENT_DETAILS and not self.is_user_invest_detail_step_done():
                pending_steps.append(step)
            elif step == StepName.D_MAT_DETAILS and not self.is_user_dmat_step_done():
                pending_steps.append(step)
        return pending_steps

    def _get_screen_options(self, step, data):
        return fetch_screen_options(step, self.role, data)

    def _is_data_validate(self, step, data):
        return validate_step_data(step, self.role, data)

    def _format_step_data(self, step, data):
        data = format_kyc_data(data, self.role, step)
        return data

    def _fetch_personal_detail_conf(self):
        step = StepName.PERSONAL_DETAILS
        screen_conf = copy.deepcopy(PERSONAL_DETAIL_PAGE_CONF)
        section = copy.deepcopy(PERSONAL_DETAIL_SECTION)
        data = self.investor_obj.__dict__
        data['city'] = self.investor_obj.city.name if self.investor_obj.city else ''
        data['state'] = self.investor_obj.state.name if self.investor_obj.state else ''
        data["upload_pan_url"] = self.investor_obj.uploadPan.url if self.investor_obj.uploadPan else ''
        data["upload_aadhaar_url"] = self.investor_obj.uploadAadhar.url if self.investor_obj.uploadAadhar else ''
        data['country'] = self.investor_obj.country.name if self.investor_obj.country else ''
        cory = whatsappLeads.objects.filter(profileOwner_id=self.user).values('countryCode', 'phoneNumber').last()
        if cory:
            data['countryCode'] = cory.get('countryCode')
            if not data.get('mobileNumber'):
                data['mobileNumber'] = cory.get('phoneNumber')
        data.update(self._get_screen_options(step=step, data=data))
        if not data.get('email'):
            data['email'] = self.user.email
        section = fill_template_config(section, data, step)
        screen_conf['sections'] = [section]
        return screen_conf

    def _fetch_investment_detail_conf(self):
        step = StepName.INVESTMENT_DETAILS
        screen_conf = copy.deepcopy(INVESTMENT_DETAIL_PAGE_CONF)
        section = copy.deepcopy(INVESTMENT_DETAIL_SECTION)
        data = self.investment_detail_obj.__dict__
        investment_market = []
        if self.investment_detail_obj.primaryMarket:
            investment_market.append(InvestmentMarket.PRIMARY.value)
        if self.investment_detail_obj.secondaryMarket:
            investment_market.append(InvestmentMarket.SECONDARY.value)
        data[
            'investment_market'] = investment_market
        if InvestmentMarket.PRIMARY.value in investment_market:
            section['components'].append(copy.deepcopy(PRIMARY_INVESTMENT_SUB_COMPONENT))
        data['lookingToInvest'] = list(self.investment_detail_obj.lookingToInvest.values_list('id', flat=True))
        data.update(self._get_screen_options(step=step, data=data))
        section = fill_template_config(section, data, step)
        screen_conf['sections'] = [section]
        return screen_conf

    def _fetch_bank_detail_conf(self):
        return self.common_kyc.fetch_bank_config()

    def _fetch_dmat_conf(self):
        return self.common_kyc.fetch_dmat_config()

    def fetch_kyc_page_config(self, step):
        step_map = {
            StepName.PERSONAL_DETAILS: self._fetch_personal_detail_conf,
            StepName.INVESTMENT_DETAILS: self._fetch_investment_detail_conf,
            StepName.BANK_DETAILS: self._fetch_bank_detail_conf,
            StepName.D_MAT_DETAILS: self._fetch_dmat_conf
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
            "heading": "Investor Kyc",
            "subHeading": "",
            "progress": {
                "percentage": ((total_steps - pending_steps_count) / total_steps) * 100
            },
            "steps": steps,
            'current_step': current_step
        }
        return config

    def update_kyc_details(self, step, data: dict):
        resp = {'status': False, "message": ""}
        objForm = None
        data = self._format_step_data(step, data)
        validation_resp = self._is_data_validate(step, data)
        if not validation_resp['status']:
            return validation_resp
        if step == StepName.PERSONAL_DETAILS:
            objForm = investorPersonalDetailsForm(data, instance=self.investor_obj)
        elif step == StepName.BANK_DETAILS:
            instance = investorBankDetails.objects.filter(id=data.get('pk'),
                                                          profileOwner_id=self.user.id).last() if data.get(
                'pk') else None
            objForm = investorBankDetailsForm(data, instance=instance)
            if data.get('is_default'):
                investorBankDetails.objects.filter(profileOwner=self.user, is_default=True).update(
                    is_default=False)
        elif step == StepName.INVESTMENT_DETAILS:
            instance = self.investment_detail_obj
            objForm = investmentDetailsForm(data, instance=instance)
        elif step == StepName.D_MAT_DETAILS:
            instance = investorDMATDetails.objects.filter(id=data.get('pk'),
                                                          profileOwner_id=self.user.id).last() if data.get(
                'pk') else None
            objForm = investorDMATDetailsForm(data, instance=instance)
            if data.get('is_default'):
                investorDMATDetails.objects.filter(profileOwner=self.user, is_default=True).update(
                    is_default=False)
        if objForm and objForm.is_valid():
            cd = objForm.save(commit=False)
            cd.profileOwner = self.user
            cd.author = self.user
            cd.save()
            cd.refresh_from_db()
            objForm.save_m2m()
            resp["status"] = True
        elif not objForm:
            resp['message'] = 'Invalid Step'
        else:
            resp['message'] = 'Invalid data'
        return resp

    def upload_kyc_docs(self, step, files, data):
        resp = {'status': False, "message": ""}
        objForm = None
        if step == StepName.PERSONAL_DETAILS:
            if data.get('name'):
                self.common_kyc.update_user_details(data)
            objForm = investorPersonalDetailsForm(data, files, instance=self.investor_obj)
        elif step == StepName.BANK_DETAILS:
            instance = investorBankDetails.objects.filter(id=data.get('pk'),
                                                          profileOwner_id=self.user.id).last() if data.get(
                'pk') else None
            objForm = investorBankDetailsForm(data, files, instance=instance)
        elif step == StepName.D_MAT_DETAILS:
            instance = investorDMATDetails.objects.filter(id=data.get('pk'),
                                                          profileOwner_id=self.user.id).last() if data.get(
                'pk') else None
            objForm = investorDMATDetailsForm(data, files, instance=instance)
        if objForm and objForm.is_valid():
            cd = objForm.save(commit=False)
            cd.profileOwner = self.user
            cd.author = self.user
            cd.save()
            doc_data = {
                'pk': cd.id
            }
            for doc in files.keys():
                try:
                    doc_data[doc] = getattr(cd, doc).url
                except Exception as e:
                    pass
            cd.refresh_from_db()
            objForm.save_m2m()
            resp["status"] = True
            resp['data'] = doc_data
        elif not objForm:
            resp['message'] = 'Invalid Step'
        else:
            resp['message'] = 'Invalid data'
        return resp

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
        resp = {'status': False, "message": "Invalid"}
        instance = None
        if step == StepName.BANK_DETAILS:
            instance = investorBankDetails.objects.filter(id=pk,
                                                          profileOwner_id=self.user.id).last() if pk else None
        elif step == StepName.D_MAT_DETAILS:
            instance = investorDMATDetails.objects.filter(id=pk,
                                                          profileOwner_id=self.user.id).last() if pk else None

        if instance:
            instance.delete()
            resp['status'] = True
            resp["message"] = ''
        return resp
