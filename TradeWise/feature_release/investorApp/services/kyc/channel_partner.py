import copy
import datetime
import json
import base64
from django.core.files.base import ContentFile
from investorApp.services.kyc.constants import UserRoleTypes, PLANIFY_STAMP_BASE64, CHANNEL_PARTNER_AGR_DAYS
from investorApp.services.kyc.base import KycBase
from django.template import Template, Context
from investorApp.models import (investorPersonalDetails, investorBankDetails, investorDMATDetails,
                                UserTransferFacility, CompanyDetails, ChannelPartnerDetails, CompanySectorDetails,
                                CompanySectors, UserSocialDetails)
from investorApp.services.kyc.config import ChannelPartnerKycConfig, StepName, KycFeConfig
from investorApp.services.kyc.screen_configs.channel_partner_config import (COMPANY_DETAIL_SECTION,
                                                                            COMPANY_DETAIL_PAGE_CONF,
                                                                            DEALS_IN_ACCORDIAN_CONFIG,
                                                                            CP_SECTION, CP_PAGE_CONF,
                                                                            AGREEMENT_SUN_COMPONENTS,
                                                                            COMPANY_GST_COMPONENTS,
                                                                            COMPANY_GST_COMP
                                                                            )
from investorApp.services.kyc.util import (fill_template_config,
                                           fetch_screen_options, generate_html_pdf, format_kyc_data,
                                           fetch_company_sectors)
from investorApp.forms import CompanySectorDealForm
from investorApp.services.kyc.common_kyc import CommonKycConfig


class ChannelPartnerKyc(KycBase):
    role = UserRoleTypes.CHANNEL_PARTNER.value
    _instance = None

    def __init__(self, user):
        self.user = user
        self.steps = ChannelPartnerKycConfig
        self.common_kyc = CommonKycConfig(self.user, self.role)
        self.investor_obj = investorPersonalDetails.fetch_obj(user.id)
        super(ChannelPartnerKyc, self).__init__(user)

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
        return CompanyDetails.objects.filter(user_id=self.user.id, user_role=self.role, pinCode__isnull=False).exists()

    def is_user_bank_step_done(self):
        return investorBankDetails.objects.filter(profileOwner_id=self.user.id, ifsc_Code__isnull=False).exists()

    def is_user_dmat_step_done(self):
        return investorDMATDetails.objects.filter(profileOwner_id=self.user.id, dpID__isnull=False).exists()

    def is_user_facility_step_done(self):
        return UserTransferFacility.objects.filter(user_id=self.user.id, role=self.role,
                                                   transfer_type__isnull=False).exists()

    def is_channel_partner_agreement(self):
        return True if ChannelPartnerDetails.fetch_obj(self.user.id).agreement else False

    def is_social_info_done(self):
        return UserSocialDetails.objects.filter(user_id=self.user.id).exclude(is_fin_influencer='').exists()

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
            elif step == StepName.PARTNER_AGREEMENT and not self.is_channel_partner_agreement():
                pending_steps.append(step)
            elif step == StepName.SOCIAL_INFORMATION and not self.is_social_info_done():
                pending_steps.append(step)
        return pending_steps

    def _fetch_personal_detail_conf(self):
        screen_conf = self.common_kyc.fetch_user_personal_detail_conf(self.investor_obj)
        return screen_conf

    def _fetch_company_detail_conf(self):
        step = StepName.COMPANY_DETAILS
        screen_conf = copy.deepcopy(COMPANY_DETAIL_PAGE_CONF)
        section = copy.deepcopy(COMPANY_DETAIL_SECTION)
        obj = CompanyDetails.fetch_obj(self.user.id, self.role)
        current_sectors = list(obj.company_sector.all().values_list('id', flat=True))
        data = obj.__dict__
        sectors = []
        sector_data_map = {}

        data['company_sector'] = sectors
        data["gst_proof_url"] = obj.gst_proof.url if obj.gst_proof else ''
        company_dealing_objs = CompanySectorDetails.objects.filter(company_id=obj.id)
        sector_obj_map = {obj.sector_id: obj for obj in company_dealing_objs}
        accordian_list = []
        company_sct_data = fetch_company_sectors()
        for cmp in company_sct_data:
            sectors.append(cmp['id'])
            sector_data_map[cmp['id']] = cmp['name']
        for sector in sectors:
            dealing_obj = sector_obj_map.get(sector, None)
            sub_data = dealing_obj.__dict__ if dealing_obj else {}
            sub_data[
                'license_proof_url'] = dealing_obj.license_proof.url if dealing_obj and dealing_obj.license_proof else ''
            sub_data['sector'] = sector
            sub_data['sector_name'] = sector_data_map.get(sector)
            sub_data.update(fetch_screen_options(step, self.role, sub_data))
            accordian = fill_template_config(DEALS_IN_ACCORDIAN_CONFIG, sub_data, step)
            accordian['componentProperties']['isSelected'] = True if sector in current_sectors else False
            accordian_list.append(accordian)
        data['company_sector_accordian_options'] = json.dumps(accordian_list)
        if data.get('signed_as') != 'Individual':
            section['components'].append(COMPANY_GST_COMP)
        if data and data['gst_applicable'] == 'Yes':
            section['components'].extend(COMPANY_GST_COMPONENTS)

        data.update(fetch_screen_options(step, self.role, data))
        section = fill_template_config(section, data, step)
        screen_conf['sections'] = [section]
        return screen_conf

    def _fetch_user_description_conf(self):
        return self.common_kyc.fetch_user_description_conf()

    def _fetch_user_asset_management_conf(self):
        data = ChannelPartnerDetails.fetch_obj(self.user.id).__dict__
        return self.common_kyc.fetch_user_asset_management_conf(data)

    def _fetch_facility_conf(self):
        screen_conf = self.common_kyc.fetch_facility_conf()
        return screen_conf

    def _generate_user_agreement_html(self, data):
        agreement = open('investorApp/templates/investor/channel_partner_agreement.html', 'r',
                         encoding="utf8").read().replace('\n', '')
        return Template(agreement).render(Context(data))

    def _fetch_user_agreement_data(self, obj: ChannelPartnerDetails, pdf_gen=False):
        data = obj.__dict__
        agreement_date = obj.agreement_date or datetime.datetime.now()
        agreement_end_date = obj.agreement_end_date or agreement_date + datetime.timedelta(
            days=CHANNEL_PARTNER_AGR_DAYS)
        data["signature_url"] = obj.signature.url if obj.signature else ''
        data['show_footer'] = False
        if obj.signature and obj.verificationStatus == 'Yes':
            data["stamp_base64"] = PLANIFY_STAMP_BASE64
        data['header_img_width'] = '300px'
        if pdf_gen:
            data['header_img_width'] = '595px'
            data['show_footer'] = True
        company_obj = CompanyDetails.fetch_obj(self.user.id, self.role)
        data['channel_partner_name'] = company_obj.organisation_name
        data[
            'complete_address'] = f'{company_obj.address, ""},{company_obj.city or ""},{company_obj.state or ""},{company_obj.pinCode or ""} ,{company_obj.country or ""}'
        data['planify_address'] = 'Plot No-23, Maruti Industrial Development Area,Sector-18 Gurugram Haryana-122015'
        data["agreement_date"] = agreement_date.strftime('%b %d, %Y')
        data['dob'] = str(self.investor_obj.dob) if self.investor_obj.dob else ''
        data['aadhaar_number'] = str(self.investor_obj.aadharNumber) if self.investor_obj.aadharNumber else ''
        data['agreement_end_date'] = agreement_end_date.strftime('%b %d, %Y')
        return data

    def _agreement_page_conf(self):
        step = StepName.PARTNER_AGREEMENT
        screen_conf = copy.deepcopy(CP_PAGE_CONF)
        section = copy.deepcopy(CP_SECTION)
        obj = ChannelPartnerDetails.fetch_obj(self.user.id)
        agreement_url = obj.agreement.url if obj.agreement else ''
        data = self._fetch_user_agreement_data(obj)
        data['agreement_url'] = agreement_url
        data['agreement_html'] = self._generate_user_agreement_html(data)
        data.update(fetch_screen_options(step, self.role, data))
        if data.get('consent') == 'Yes':
            section['components'].extend(AGREEMENT_SUN_COMPONENTS)
        section = fill_template_config(section, data, step)
        screen_conf['sections'] = [section]
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
            StepName.PARTNER_AGREEMENT: self._agreement_page_conf,
            StepName.SOCIAL_INFORMATION: self._fetch_user_description_conf,
            StepName.ASSET_MANAGEMENT: self._fetch_user_asset_management_conf
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
            "heading": "Channel Partner Kyc",
            "subHeading": "",
            "progress": {
                "percentage": int(((total_steps - pending_steps_count) / total_steps) * 100)
            },
            "steps": steps,
            'current_step': current_step
        }
        return config

    def _handle_company_dealing_data(self, instance, data, files=None):
        sub_files = {}
        doc_data = {}
        sub_sector_data = {}
        for key, val in data.items():
            if 'license_number__' in key or 'license_proof__' in key:
                sub_keys = key.split('__')
                if not sub_sector_data.get(sub_keys[1]):
                    sub_sector_data[sub_keys[1]] = {}
                sub_sector_data[sub_keys[1]][sub_keys[0]] = val
        if files:
            for key, val in files.items():
                if 'license_proof__' in key:
                    sub_keys = key.split('__')
                    sub_files[sub_keys[1]] = {
                        'license_proof': val,
                    }
        for key, val in sub_sector_data.items():
            files = sub_files.get(key)
            sub_instance = CompanySectorDetails.fetch_obj(instance.id, key)
            objForm = CompanySectorDealForm(val, files, instance=sub_instance)
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

    def update_kyc_details(self, step, data: dict):
        instance = None
        files = {}
        if step == StepName.PERSONAL_DETAILS:
            instance = self.investor_obj
        elif step == StepName.COMPANY_DETAILS:
            instance = CompanyDetails.fetch_obj(self.user.id, self.role)
            data = format_kyc_data(data, self.role, step)
            self._handle_company_dealing_data(instance, data)
        elif step == StepName.ASSET_MANAGEMENT:
            instance = ChannelPartnerDetails.fetch_obj(self.user.id)
            step = StepName.CHANNEL_PARTNER_DETAILS
        elif step == StepName.PARTNER_AGREEMENT:
            instance = ChannelPartnerDetails.fetch_obj(self.user.id)
            if instance and instance.agreement and data.get('consent') == 'No':
                return {'status': False, 'message': "Agreement has already been signed"}
            if instance and instance.signature and not instance.agreement:
                agr_data = self._fetch_user_agreement_data(instance, True)
                html = self._generate_user_agreement_html(agr_data)
                pdf = generate_html_pdf(html)
                pdf_data = ContentFile(pdf, name=f'{agr_data["channel_partner_name"]}_agreement.pdf')
                files = {'agreement': pdf_data, 'agreement_date': datetime.datetime.now(),
                         'agreement_end_date': datetime.datetime.now() + datetime.timedelta(
                             days=CHANNEL_PARTNER_AGR_DAYS)}
                data.update(files)
        resp = self.common_kyc.upload_kyc_docs(step, files, data, instance)
        return resp

    def upload_kyc_docs(self, step, files, data):
        doc_data = {}
        instance = None
        if step == StepName.PERSONAL_DETAILS:
            instance = self.investor_obj
        elif step == StepName.COMPANY_DETAILS:
            instance = CompanyDetails.fetch_obj(self.user.id, self.role)
            doc_data = self._handle_company_dealing_data(instance, data, files)
        resp = self.common_kyc.upload_kyc_docs(step, files, data, instance)
        if resp['status'] and doc_data:
            resp['data'].update(doc_data)
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
        return self.common_kyc.fetch_field_options(self.investor_obj, field, query_params)

    def delete_kyc_details(self, step, pk: str):
        return self.common_kyc.delete_kyc_details(step, pk)
