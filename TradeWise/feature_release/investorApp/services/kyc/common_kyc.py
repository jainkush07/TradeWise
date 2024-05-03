import copy
from whatsappAuthApp.models import whatsappLeads
from investorApp.services.kyc.constants import InvestmentMarket
from investorApp.services.kyc.screen_configs.common_config import *
from investorApp.services.kyc.util import (fill_template_config, fetch_delete_config, fetch_screen_options,
                                           format_kyc_data, fetch_fields_option)
from investorApp.models import (investorBankDetails, investorDMATDetails,
                                UserTransferFacility, CompanyDetails, DealerDetails, ChannelPartnerDetails,
                                UserSocialDetails)
from investorApp.services.kyc.config import StepName
from investorApp.forms import (investorPersonalDetailsForm, CompanyDetailForm, investorBankDetailsForm,
                               investmentDetailsForm, EsopDetailForm,
                               investorDMATDetailsForm, UserTransferFacilityForm, UserForm, DealerDetailForm,
                               ChannelPartnerDetailForm, UserSocialDetailForm)
from investorApp.services.kyc.validators import validate_step_data


class CommonKycConfig:

    def __init__(self, user, role):
        self.role = role
        self.user = user

    def fetch_dmat_config(self):
        step = StepName.D_MAT_DETAILS
        screen_conf = copy.deepcopy(DMAT_PAGE_CONF)
        sections = []
        dmats = investorDMATDetails.objects.filter(profileOwner_id=self.user.id).order_by('id')
        data_list = list(dmats.values())
        for data in data_list:
            dmat = dmats.filter(id=data['id']).last()
            data[
                'demat_client_master_url'] = dmat.dmatClientMasterReport.url if dmat.dmatClientMasterReport else ''
        if not data_list:
            data_list = []
        data_list.append({'heading': 'Dmat Details'})
        for data in data_list:
            section = copy.deepcopy(DMAT_SECTION)
            data['heading'] = data.get('heading') if data.get(
                "heading") else f'DP ID - {data.get("dpID")}, Client Id - {data.get("clientID")}'
            data["demat_client_master_url"] = data.get('demat_client_master_url')
            data['pk'] = data.get('id', '')
            if data['pk'] and str(data['pk']).strip():
                section["delete"] = fetch_delete_config()
            data.update(fetch_screen_options(step, self.role, data))
            sub_section = fill_template_config(section, data, step)
            sections.append(sub_section)
        screen_conf['sections'] = sections
        return screen_conf

    def fetch_bank_config(self):
        step = StepName.BANK_DETAILS
        screen_conf = copy.deepcopy(BANK_DETAIL_PAGE_CONF)

        sections = []
        banks = investorBankDetails.objects.filter(profileOwner_id=self.user.id).order_by('id')
        data_list = list(banks.values())
        for data in data_list:
            bank = banks.filter(id=data['id']).last()
            data['cancelledCheque_url'] = bank.cancelledCheque.url if bank.cancelledCheque else ''
        if not data_list:
            data_list = []
        data_list.append({'heading': 'Bank Details'})
        for data in data_list:
            section = copy.deepcopy(BANK_DETAIL_SECTION)
            data['heading'] = data.get('heading') if data.get("heading") else f'Acc No. {data.get("accountNumber")}'
            data["cc_url"] = data.get('cancelledCheque_url', '')
            data['pk'] = data.get('id', '')
            if data['pk'] and str(data['pk']).strip():
                section["delete"] = fetch_delete_config()
            data.update(fetch_screen_options(step, self.role, data))
            sub_section = fill_template_config(section, data, step)
            sections.append(sub_section)
        screen_conf['sections'] = sections
        return screen_conf

    def fetch_facility_conf(self):
        step = StepName.TRANSFER_FACILITY
        screen_conf = copy.deepcopy(TRANSFER_FACILITY_PAGE_CONF)
        section = copy.deepcopy(TRANSFER_FACILITY_SECTION)
        obj = UserTransferFacility.fetch_obj(self.user.id, self.role)
        data = obj.__dict__
        data["transfer_file_proof_url"] = obj.transfer_file_proof.url if obj.transfer_file_proof else ''
        data.update(fetch_screen_options(step, self.role, data))
        section = fill_template_config(section, data, step)
        screen_conf['sections'] = [section]
        return screen_conf

    def fetch_user_description_conf(self):
        step = StepName.SOCIAL_INFORMATION
        screen_conf = copy.deepcopy(USER_DESCRIPTION_PAGE_CONF)
        section = copy.deepcopy(USER_DESCRIPTION_SECTION)
        obj = UserSocialDetails.fetch_obj(self.user.id)
        data = obj.__dict__
        if not data.get('linkedIn_handle'):
            data['linkedIn_handle'] = 'https://www.linkedin.com/in/'
        if not data.get('youtube_handle'):
            data['youtube_handle'] = 'https://www.youtube.com/'
        if not data.get('instagram_handle'):
            data['instagram_handle'] = 'https://www.instagram.com/'
        if not data.get('twitter_handle'):
            data['twitter_handle'] = 'https://www.twitter.com/'
        data.update(fetch_screen_options(step, self.role, data))
        section = fill_template_config(section, data, step)
        screen_conf['sections'] = [section]
        return screen_conf

    def fetch_user_asset_management_conf(self, data):
        step = StepName.ASSET_MANAGEMENT
        screen_conf = copy.deepcopy(USER_ASSET_MANAGE_PAGE_CONF)
        section = copy.deepcopy(USER_ASSET_MANAGE_SECTION)
        data.update(fetch_screen_options(step, self.role, data))
        section = fill_template_config(section, data, step)
        screen_conf['sections'] = [section]
        return screen_conf

    def fetch_investment_detail_conf(self, investment_detail_obj):
        step = StepName.INVESTMENT_DETAILS
        screen_conf = copy.deepcopy(INVESTMENT_DETAIL_PAGE_CONF)
        section = copy.deepcopy(INVESTMENT_DETAIL_SECTION)
        data = investment_detail_obj.__dict__
        investment_market = []
        if investment_detail_obj.primaryMarket:
            investment_market.append(InvestmentMarket.PRIMARY.value)
        if investment_detail_obj.secondaryMarket:
            investment_market.append(InvestmentMarket.SECONDARY.value)
        data[
            'investment_market'] = investment_market
        if InvestmentMarket.PRIMARY.value in investment_market:
            section['components'].append(copy.deepcopy(PRIMARY_INVESTMENT_SUB_COMPONENT))
        data['lookingToInvest'] = list(investment_detail_obj.lookingToInvest.values_list('id', flat=True))
        data.update(fetch_screen_options(step, self.role, data))
        section = fill_template_config(section, data, step)
        screen_conf['sections'] = [section]
        return screen_conf

    def update_kyc_details(self, step, data: dict, instance):
        resp = {'status': False, "message": ""}
        objForm = None
        if step == StepName.D_MAT_DETAILS:
            if not instance:
                instance = investorDMATDetails.objects.filter(id=data.get('pk'),
                                                              profileOwner_id=self.user.id).last() if data.get(
                    'pk') else None
            if instance:
                if not data.get('dpID') and instance.dpID:
                    data['dpID'] = instance.dpID
                elif not data.get('depository') and instance.depository:
                    data['depository'] = instance.depository
        data = format_kyc_data(data, self.role, step)
        validation_resp = validate_step_data(step, self.role, data)
        if not validation_resp['status']:
            return validation_resp
        if step == StepName.PERSONAL_DETAILS:
            objForm = investorPersonalDetailsForm(data, instance=instance)
        elif step == StepName.BANK_DETAILS:
            if not instance:
                instance = investorBankDetails.objects.filter(id=data.get('pk'),
                                                              profileOwner_id=self.user.id).last() if data.get(
                    'pk') else None
            objForm = investorBankDetailsForm(data, instance=instance)
            if data.get('is_default'):
                investorBankDetails.objects.filter(profileOwner=self.user, is_default=True).update(
                    is_default=False)
        elif step == StepName.COMPANY_DETAILS:
            if not instance:
                instance = CompanyDetails.fetch_obj(self.user.id, self.role)
            objForm = CompanyDetailForm(data, instance=instance)
        elif step == StepName.INVESTMENT_DETAILS:
            objForm = investmentDetailsForm(data, instance=instance)
        elif step == StepName.ESOP_COMPANY_DETAILS:
            objForm = EsopDetailForm(data, instance=instance)
        elif step == StepName.DEALER_DETAILS:
            instance = DealerDetails.fetch_obj(self.user.id)
            objForm = DealerDetailForm(data, instance=instance)
        elif step == StepName.TRANSFER_FACILITY:
            if not instance:
                instance = UserTransferFacility.fetch_obj(self.user.id, self.role)
            objForm = UserTransferFacilityForm(data, instance=instance)
        elif step == StepName.D_MAT_DETAILS:
            if not instance:
                instance = investorDMATDetails.objects.filter(id=data.get('pk'),
                                                              profileOwner_id=self.user.id).last() if data.get(
                    'pk') else None
            objForm = investorDMATDetailsForm(data, instance=instance)
            if data.get('is_default'):
                investorDMATDetails.objects.filter(profileOwner=self.user, is_default=True).update(
                    is_default=False)
        elif step in [StepName.CHANNEL_PARTNER_DETAILS, StepName.PARTNER_AGREEMENT]:
            if not instance:
                instance = ChannelPartnerDetails.fetch_obj(self.user.id)
            objForm = ChannelPartnerDetailForm(data, instance=instance)
        elif step == StepName.SOCIAL_INFORMATION:
            instance = UserSocialDetails.fetch_obj(self.user.id)
            objForm = UserSocialDetailForm(data, instance=instance)
        if objForm and objForm.is_valid():
            cd = objForm.save(commit=False)
            if step not in [StepName.COMPANY_DETAILS, StepName.CHANNEL_PARTNER_DETAILS,
                            StepName.PARTNER_AGREEMENT, StepName.TRANSFER_FACILITY, StepName.SOCIAL_INFORMATION]:
                cd.profileOwner = self.user
                if step not in [StepName.D_MAT_DETAILS]:
                    cd.author = self.user
            cd.save()
            cd.refresh_from_db()
            objForm.save_m2m()
            resp["status"] = True
        elif not objForm:
            resp['message'] = 'Invalid Step'
        else:
            message = ''
            for x,v in dict(objForm.errors).items():
                message += f'{x}: {v[0]}'
                break
            resp['message'] = message
        return resp

    def upload_kyc_docs(self, step, files, data, instance):
        resp = {'status': False, "message": ""}
        objForm = None
        data = format_kyc_data(data, self.role, step)
        validation_resp = validate_step_data(step, self.role, data)
        if not validation_resp['status']:
            return validation_resp
        if step == StepName.PERSONAL_DETAILS:
            self.update_user_details(data)
            objForm = investorPersonalDetailsForm(data, files, instance=instance)
        elif step == StepName.COMPANY_DETAILS:
            objForm = CompanyDetailForm(data, files, instance=CompanyDetails.fetch_obj(self.user.id, self.role))
        elif step == StepName.BANK_DETAILS:
            if not instance:
                instance = investorBankDetails.objects.filter(id=data.get('pk'),
                                                              profileOwner_id=self.user.id).last() if data.get(
                    'pk') else None
            objForm = investorBankDetailsForm(data, files, instance=instance)
        elif step == StepName.INVESTMENT_DETAILS:
            objForm = investmentDetailsForm(data, files, instance=instance)
        elif step == StepName.ESOP_COMPANY_DETAILS:
            objForm = EsopDetailForm(data, files, instance=instance)
        elif step == StepName.D_MAT_DETAILS:
            if not instance:
                instance = investorDMATDetails.objects.filter(id=data.get('pk'),
                                                              profileOwner_id=self.user.id).last() if data.get(
                    'pk') else None
            objForm = investorDMATDetailsForm(data, files, instance=instance)
        elif step == StepName.TRANSFER_FACILITY:
            if not instance:
                instance = UserTransferFacility.fetch_obj(self.user.id, self.role)
            objForm = UserTransferFacilityForm(data, files, instance=instance)
        elif step in [StepName.CHANNEL_PARTNER_DETAILS, StepName.PARTNER_AGREEMENT]:
            if not instance:
                instance = ChannelPartnerDetails.fetch_obj(self.user.id)
            objForm = ChannelPartnerDetailForm(data, files, instance=instance)
        elif step == StepName.SOCIAL_INFORMATION:
            instance = UserSocialDetails.fetch_obj(self.user.id)
            objForm = UserSocialDetailForm(data, files, instance=instance)
        if objForm and objForm.is_valid():
            cd = objForm.save(commit=False)
            if step not in [StepName.COMPANY_DETAILS, StepName.CHANNEL_PARTNER_DETAILS,
                            StepName.PARTNER_AGREEMENT, StepName.TRANSFER_FACILITY]:
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
            message = ''
            for x, v in dict(objForm.errors).items():
                message += f'{x}: {v[0]}'
                break
            resp['message'] = message
        return resp

    def fetch_field_options(self, obj, field, query_params):
        data = obj.__dict__
        if query_params and query_params.get('step') == StepName.COMPANY_DETAILS:
            data = CompanyDetails.fetch_obj(self.user.id, self.role).__dict__
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

    def fetch_user_personal_detail_conf(self, investor_obj):
        step = StepName.PERSONAL_DETAILS
        screen_conf = copy.deepcopy(PERSONAL_DETAIL_PAGE_CONF)
        section = copy.deepcopy(PERSONAL_DETAIL_SECTION)
        data = investor_obj.__dict__
        data['city'] = investor_obj.city.name if investor_obj.city else ''
        data['state'] = investor_obj.state.name if investor_obj.state else ''
        data["upload_pan_url"] = investor_obj.uploadPan.url if investor_obj.uploadPan else ''
        data["upload_aadhaar_url"] = investor_obj.uploadAadhar.url if investor_obj.uploadAadhar else ''
        data['country'] = investor_obj.country.name if investor_obj.country else ''
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

    def update_user_details(self, data):
        if data.get('name'):
            name = data.get('name')
            name_list = name.split(' ')
            data['first_name'] = ' '.join(name_list[:-1])
            if len(name_list) > 1:
                data['last_name'] = name_list[-1]
            objForm = UserForm(data, instance=self.user)
            if objForm and objForm.is_valid():
                cd = objForm.save(commit=False)
                cd.save()
                cd.refresh_from_db()
                objForm.save_m2m()
        return True
