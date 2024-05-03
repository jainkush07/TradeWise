import copy
import json
import datetime
from whatsappAuthApp.models import whatsappLeads
from investorApp.services.kyc.constants import UserRoleTypes
from investorApp.services.kyc.base import KycBase
from investorApp.forms import CompanyDetailForm, CompanyBusinessDetailForm, CompanyFinancailDetailForm
from investorApp.models import (investorBankDetails, investorDMATDetails,
                                UserTransferFacility, CompanyDetails, CompanyBusinessDetails, CompanyFinancialDetails)
from investorApp.services.kyc.config import FounderKycConfig, StepName, KycFeConfig
from investorApp.services.kyc.screen_configs.founder_config import (PERSONAL_DETAIL_PAGE_CONF,
                                                                    PERSONAL_DETAIL_SECTION,
                                                                    COMPANY_DETAIL_SECTION,
                                                                    COMPANY_DETAIL_PAGE_CONF,
                                                                    COMPANY_FINANCIAL_UPLOAD_COMPONENT,
                                                                    COMPANY_FINANCIAL_UPLOAD_SUB_COMPONENT
                                                                    )

from investorApp.services.kyc.util import (fill_template_config,
                                           fetch_screen_options, fetch_fields_option)
from investorApp.services.kyc.common_kyc import CommonKycConfig


class FounderKyc(KycBase):
    role = UserRoleTypes.FOUNDER.value
    _instance = None

    def __init__(self, user):
        self.user = user
        self.steps = FounderKycConfig
        self.common_kyc = CommonKycConfig(self.user, self.role)
        self.company_obj = CompanyDetails.fetch_obj(user.id, self.role)
        super(FounderKyc, self).__init__(user)

    def get_role_name(self):
        return self.role

    def is_user_pd_step_done(self):
        data = self.company_obj.__dict__
        if type(data.get('role_in_company')) in [str, None, datetime.datetime, int, float] and data.get(
                'role_in_company') in [None, '']:
            return False
        return True

    def is_company_detail_step_done(self):
        data = self.company_obj.__dict__
        if type(data.get('valuation')) in [str, None, datetime.datetime, int, float] and data.get(
                'valuation') in [None, '']:
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
            if step == StepName.INS_PERSONAL_DETAILS and not self.is_user_pd_step_done():
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
        step = StepName.INS_PERSONAL_DETAILS
        screen_conf = copy.deepcopy(PERSONAL_DETAIL_PAGE_CONF)
        section = copy.deepcopy(PERSONAL_DETAIL_SECTION)
        data = self.company_obj.__dict__
        data['name'] = self.user.first_name + f' {self.user.last_name}' if self.user.last_name else ''
        cory = whatsappLeads.objects.filter(profileOwner_id=self.user).values('countryCode', 'phoneNumber').last()
        if cory:
            data['countryCode'] = cory.get('countryCode')
            if not data.get('mobileNumber'):
                data['mobileNumber'] = cory.get('phoneNumber')
        data.update(fetch_screen_options(step, self.role, data))
        if not data.get('email'):
            data['email'] = self.user.email
        section = fill_template_config(section, data, step)
        screen_conf['sections'] = [section]
        return screen_conf

    def _fetch_company_detail_conf(self):
        step = StepName.COMPANY_DETAILS
        screen_conf = copy.deepcopy(COMPANY_DETAIL_PAGE_CONF)
        section = copy.deepcopy(COMPANY_DETAIL_SECTION)
        data = self.company_obj.__dict__
        annual_financial_component = copy.deepcopy(COMPANY_FINANCIAL_UPLOAD_COMPONENT)
        company_financials = CompanyFinancialDetails.objects.filter(company_id=self.company_obj.id).all()
        if not company_financials:
            year = datetime.datetime.now().year
            financial_obj = CompanyFinancialDetails.fetch_obj(company_id=self.company_obj.id, year=year)
            company_financials = [financial_obj]
        data_list = []
        sub_component = copy.deepcopy(COMPANY_FINANCIAL_UPLOAD_SUB_COMPONENT)
        for company_financial in company_financials:
            company_financial_data = company_financial.__dict__
            company_financial_data[
                'financial_report_url'] = company_financial.financial_report.url if company_financial.financial_report else ''
            company_financial_data.update(fetch_screen_options(None, self.role, data))
            data_list.append(fill_template_config(sub_component, company_financial_data))
        if len(company_financials) >= 5:
            annual_financial_component['componentProperties']['config'] = {}
        annual_financial_component['componentProperties']['list'] = data_list
        business_obj = CompanyBusinessDetails.fetch_obj(self.company_obj.id)
        if business_obj:
            data.update(business_obj.__dict__)
            data["pitch_deck_url"] = business_obj.pitch_deck.url if business_obj.pitch_deck else ''
        section['components'].append(annual_financial_component)
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

    def _handle_company_financial_data(self, instance, data, files=None):
        if not files and data.get('annual_financial_doc'):
            year = datetime.datetime.now().year
            new_financial_year = ''
            company_financial_years = CompanyFinancialDetails.objects.filter(
                company_id=self.company_obj.id).values_list('financial_year', flat=True)
            if len(company_financial_years) < 5:
                for i in range(year, year - 6, -1):
                    if str(i) not in company_financial_years:
                        new_financial_year = i
                        break
                if new_financial_year:
                    CompanyFinancialDetails.fetch_obj(self.company_obj.id, new_financial_year)
            return {}
        sub_files = {}
        doc_data = {}
        sub_sector_data = {}
        for key, val in data.items():
            if 'financial_report__' in key:
                sub_keys = key.split('__')
                if not sub_sector_data.get(sub_keys[1]):
                    sub_sector_data[sub_keys[1]] = {}
                sub_sector_data[sub_keys[1]][sub_keys[0]] = val
        if files:
            for key, val in files.items():
                if 'financial_report__' in key:
                    sub_keys = key.split('__')
                    sub_files[sub_keys[1]] = {
                        'financial_report': val,
                    }
        for key, val in sub_sector_data.items():
            files = sub_files.get(key)
            sub_instance = CompanyFinancialDetails.fetch_obj(instance.id, key)
            objForm = CompanyFinancailDetailForm(val, files, instance=sub_instance)
            if objForm.is_valid():
                cd = objForm.save(commit=False)
                cd.save()
                if files:
                    for doc in files.keys():
                        try:
                            doc_data[f"{doc}__{key}"] = getattr(cd, doc).url
                        except Exception as e:
                            pass
                cd.refresh_from_db()
                objForm.save_m2m()
        return doc_data

    def fetch_kyc_page_config(self, step):
        step_map = {
            StepName.INS_PERSONAL_DETAILS: self._fetch_personal_detail_conf,
            StepName.COMPANY_DETAILS: self._fetch_company_detail_conf,
            StepName.BANK_DETAILS: self._fetch_bank_detail_conf,
            StepName.D_MAT_DETAILS: self._fetch_dmat_conf,
            StepName.TRANSFER_FACILITY: self._fetch_facility_conf,
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
            if step == StepName.INS_PERSONAL_DETAILS:
                conf['label'] = 'Personal Details'
            conf['state'] = 'pending' if step in pending_steps else 'completed'
            steps.append(conf)
        config = {
            "page": "",
            "type": "kyc",
            "heading": "Founder Registeration",
            "subHeading": "",
            "progress": {
                "percentage": ((total_steps - pending_steps_count) / total_steps) * 100
            },
            "steps": steps,
            'current_step': current_step
        }
        return config

    def update_kyc_details(self, step, data: dict):
        instance = None
        if step not in [StepName.INS_PERSONAL_DETAILS, StepName.COMPANY_DETAILS, StepName.COMPANY_FINANCIALS]:
            return self.common_kyc.update_kyc_details(step, data, instance)
        elif step == StepName.COMPANY_FINANCIALS:

            self._handle_company_financial_data(self.company_obj, data, None)
            return {'status': True, "message": ""}
        else:
            resp = {'status': False, "message": ""}
            objForm = None
            if step == StepName.INS_PERSONAL_DETAILS:
                self.common_kyc.update_user_details(data)
                objForm = CompanyDetailForm(data, instance=self.company_obj)
            elif step == StepName.COMPANY_DETAILS:
                objForm = CompanyDetailForm(data, instance=self.company_obj)
                if objForm.is_valid():
                    objForm.save()
                objForm = CompanyBusinessDetailForm(data,
                                                    instance=CompanyBusinessDetails.fetch_obj(self.company_obj.id))
            if objForm and objForm.is_valid():
                cd = objForm.save(commit=False)
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
        resp = {'status': False, "message": "invalid data"}
        instance = None
        if step not in [StepName.INS_PERSONAL_DETAILS, StepName.COMPANY_DETAILS, StepName.COMPANY_FINANCIALS]:
            return self.common_kyc.upload_kyc_docs(step, data, files, instance)
        elif step == StepName.COMPANY_FINANCIALS:
            doc_data = self._handle_company_financial_data(self.company_obj, data, files)
            if doc_data:
                resp['status'] = True
                resp['message'] = 'Success'
                resp['data'] = doc_data
            return resp
        else:
            objForm = None
            if step == StepName.INS_PERSONAL_DETAILS:
                objForm = CompanyDetailForm(data, files, instance=self.company_obj)
            elif step == StepName.COMPANY_DETAILS:
                objForm = CompanyBusinessDetailForm(data, files,
                                                    instance=CompanyBusinessDetails.fetch_obj(self.company_obj.id))
            if objForm and objForm.is_valid():
                cd = objForm.save(commit=False)
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
        data = self.company_obj.__dict__
        return fetch_fields_option(self.role, field, query_params, data)

    def delete_kyc_details(self, step, pk: str):
        return self.common_kyc.delete_kyc_details(step, pk)
