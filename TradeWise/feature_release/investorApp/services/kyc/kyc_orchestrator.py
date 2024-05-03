import json

from investorApp.services.kyc.base import KycBase
from investorApp.services.kyc.util import (create_common_choices, fetch_state_options,
                                           fetch_country_options, fetch_city_options)


class KycFactory:
    kyc_registry = {}

    def __init__(self):
        self.register_kyc_roles()

    @staticmethod
    def register_kyc_roles():
        from investorApp.services.kyc.investor import InvestorKyc  # req
        from investorApp.services.kyc.channel_partner import ChannelPartnerKyc  # req
        from investorApp.services.kyc.dealer import DealerKyc  # req
        from investorApp.services.kyc.institutional import InstitutionalKyc  # req
        from investorApp.services.kyc.family_office import FamilyOfficeKyc  # req
        from investorApp.services.kyc.esop import ESOPKyc  # req
        from investorApp.services.kyc.founder import FounderKyc
        from investorApp.services.kyc.private_banks import PrivateBankKyc
        from investorApp.services.kyc.authore import AuthoreKyc
        for kyc_implementation_class in KycBase.__subclasses__():
            KycFactory.kyc_registry[kyc_implementation_class.role] = kyc_implementation_class

    def get_kyc_registry_obj(self, role):
        if self.kyc_registry.get(role, None) is None:
            raise Exception("Role kyc is not yet implemented")
        return self.kyc_registry[role]


class KycOrchestrator:

    def __init__(self, user, role):
        self.user = user
        self.role = role if role else 'INVESTOR'

    def fetch_kyc_config(self):
        kyc_implementation_class = KycFactory().get_kyc_registry_obj(self.role)
        kyc_vendor_obj = kyc_implementation_class(self.user)
        resp = kyc_vendor_obj.fetch_kyc_config()
        return resp

    def fetch_kyc_page_config(self, step=None):
        kyc_implementation_class = KycFactory().get_kyc_registry_obj(self.role)
        kyc_vendor_obj = kyc_implementation_class(self.user)
        resp = kyc_vendor_obj.fetch_kyc_page_config(step)
        return resp

    def update_kyc_details(self, step, data: dict):
        kyc_implementation_class = KycFactory().get_kyc_registry_obj(self.role)
        kyc_vendor_obj = kyc_implementation_class(self.user)
        resp = kyc_vendor_obj.update_kyc_details(step, data)
        return resp

    def delete_kyc_details(self, step, pk: str):
        kyc_implementation_class = KycFactory().get_kyc_registry_obj(self.role)
        kyc_vendor_obj = kyc_implementation_class(self.user)
        resp = kyc_vendor_obj.delete_kyc_details(step, pk)
        return resp

    def upload_kyc_docs(self, step, files, data):
        kyc_implementation_class = KycFactory().get_kyc_registry_obj(self.role)
        kyc_vendor_obj = kyc_implementation_class(self.user)
        resp = kyc_vendor_obj.upload_kyc_docs(step, files, data)
        return resp

    def complete_kyc(self):
        kyc_implementation_class = KycFactory().get_kyc_registry_obj(self.role)
        kyc_vendor_obj = kyc_implementation_class(self.user)
        resp = kyc_vendor_obj.complete_kyc()
        return resp

    def fetch_field_options(self, field, query_params):
        kyc_implementation_class = KycFactory().get_kyc_registry_obj(self.role)
        kyc_vendor_obj = kyc_implementation_class(self.user)
        resp = kyc_vendor_obj.fetch_field_options(field, query_params)
        return resp
