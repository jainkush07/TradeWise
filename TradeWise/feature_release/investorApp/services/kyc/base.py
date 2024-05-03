from abc import ABC, ABCMeta, abstractmethod


class KycBase(ABC, metaclass=ABCMeta):
    role = ''
    _instance = None

    def __init__(self, user):
        pass

    @abstractmethod
    def get_role_name(self):
        pass

    @abstractmethod
    def fetch_kyc_config(self, step=None):
        pass

    @abstractmethod
    def update_kyc_details(self, step, data: dict):
        pass

    @abstractmethod
    def delete_kyc_details(self, step, pk: str):
        pass

    @abstractmethod
    def upload_kyc_docs(self, step, files, data):
        pass

    @abstractmethod
    def get_pending_steps(self):
        pass

    @abstractmethod
    def complete_kyc(self):
        pass

    @abstractmethod
    def fetch_kyc_page_config(self, step):
        pass

    @abstractmethod
    def fetch_field_options(self, field, query_params):
        pass
