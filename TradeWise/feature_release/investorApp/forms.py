from django import forms
from .models import *
from cartApp.models import transactionDocs, Transaction


# code need to be  add by Shubham starts

class BaseForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cleanup_missing_keys(args[0])

    def cleanup_missing_keys(self, data):
        """
        Removes missing keys from fields on form submission.
        This avoids resetting fields that are not present in
        the submitted data, which may be the sign of a buggy
        or incomplete template.
        Note that this cleanup relies on the HTML form being
        patched to send all keys, even for checkboxes, via
        input[type="hidden"] fields or some JS magic.
        """
        if data is None:
            # not a form submission, don't modify self.fields
            return

        got_keys = data.keys()
        field_names = self.fields.keys()
        for missing in set(field_names) - set(got_keys):
            del self.fields[missing]

DATE_INPUT_FORMATS = ('%d-%m-%Y','%Y-%m-%d')


class investorPersonalDetailsForm(forms.ModelForm):
    dob = forms.DateField(input_formats=DATE_INPUT_FORMATS)
    class Meta:
        model = investorPersonalDetails
        exclude = ('profileOwner', 'author', 'publish', 'created', 'updated', 'status', 'aadharVerified', 'panVerified',
                   'verifiedChoice', 'aadharVerifiedChoice', 'panVerifiedChoice')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cleanup_missing_keys(args[0])

    def cleanup_missing_keys(self, data):
        """
        Removes missing keys from fields on form submission.
        This avoids resetting fields that are not present in
        the submitted data, which may be the sign of a buggy
        or incomplete template.
        Note that this cleanup relies on the HTML form being
        patched to send all keys, even for checkboxes, via
        input[type="hidden"] fields or some JS magic.
        """
        if data is None:
            # not a form submission, don't modify self.fields
            return

        got_keys = data.keys()
        field_names = self.fields.keys()
        for missing in set(field_names) - set(got_keys):
            del self.fields[missing]


class UserTransferFacilityForm(BaseForm):
    class Meta:
        model = UserTransferFacility
        exclude = ('user_id', 'role', 'created', 'updated', 'status', 'verification_status')


class ChannelPartnerDetailForm(BaseForm):
    class Meta:
        model = ChannelPartnerDetails
        exclude = ('user_id', 'created', 'updated', 'status', 'verification_status')


class UserForm(BaseForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name')


class CompanyDetailForm(BaseForm):
    class Meta:
        model = CompanyDetails
        exclude = ('user_id', 'role', 'created', 'updated', 'status', 'verification_status', 'license_verified')


class CompanyBusinessDetailForm(BaseForm):
    class Meta:
        model = CompanyBusinessDetails
        exclude = ('company_id', 'verification_status')


class DealerDetailForm(BaseForm):
    class Meta:
        model = DealerDetails
        exclude = ('user_id', 'created', 'updated', 'verification_status')


class EsopDetailForm(BaseForm):
    class Meta:
        model = UserEsopDetails
        exclude = ('user_id', 'created', 'updated', 'verification_status')


class CompanySectorDealForm(BaseForm):
    class Meta:
        model = CompanySectorDetails
        exclude = ('created', 'updated', 'verification_status')

class CompanyFinancailDetailForm(BaseForm):
    class Meta:
        model = CompanyFinancialDetails
        exclude = ('created', 'updated', 'verification_status')


class UserSocialDetailForm(BaseForm):
    class Meta:
        model = UserSocialDetails
        exclude = ('created', 'updated', 'verification_status')


class investmentDetailsForm(forms.ModelForm):
    class Meta:
        model = investmentDetails
        exclude = ('profileOwner', 'author', 'publish', 'created', 'updated', 'status')

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.cleanup_missing_keys(args[0])

    # def cleanup_missing_keys(self, data):
    #     """
    #     Removes missing keys from fields on form submission.
    #     This avoids resetting fields that are not present in
    #     the submitted data, which may be the sign of a buggy
    #     or incomplete template.
    #     Note that this cleanup relies on the HTML form being
    #     patched to send all keys, even for checkboxes, via
    #     input[type="hidden"] fields or some JS magic.
    #     """
    #     if data is None:
    #         # not a form submission, don't modify self.fields
    #         return

    #     got_keys = data.keys()
    #     field_names = self.fields.keys()
    #     for missing in set(field_names) - set(got_keys):
    #         del self.fields[missing]


class investorBankDetailsForm(forms.ModelForm):
    class Meta:
        model = investorBankDetails
        exclude = (
            'profileOwner', 'author', 'publish', 'created', 'updated', 'status', 'verifiedChoice', 'bankVerified')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cleanup_missing_keys(args[0])

    def cleanup_missing_keys(self, data):
        """
        Removes missing keys from fields on form submission.
        This avoids resetting fields that are not present in
        the submitted data, which may be the sign of a buggy
        or incomplete template.
        Note that this cleanup relies on the HTML form being
        patched to send all keys, even for checkboxes, via
        input[type="hidden"] fields or some JS magic.
        """
        if data is None:
            # not a form submission, don't modify self.fields
            return

        got_keys = data.keys()
        field_names = self.fields.keys()
        for missing in set(field_names) - set(got_keys):
            del self.fields[missing]


class investorDMATDetailsForm(forms.ModelForm):
    class Meta:
        model = investorDMATDetails
        exclude = (
            'profileOwner', 'author', 'publish', 'created', 'updated', 'status', 'verifiedChoice', 'dmatVerified')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cleanup_missing_keys(args[0])

    def cleanup_missing_keys(self, data):
        """
        Removes missing keys from fields on form submission.
        This avoids resetting fields that are not present in
        the submitted data, which may be the sign of a buggy
        or incomplete template.
        Note that this cleanup relies on the HTML form being
        patched to send all keys, even for checkboxes, via
        input[type="hidden"] fields or some JS magic.
        """
        if data is None:
            # not a form submission, don't modify self.fields
            return

        got_keys = data.keys()
        field_names = self.fields.keys()
        for missing in set(field_names) - set(got_keys):
            del self.fields[missing]


class investorSourceDetailsForm(forms.ModelForm):
    class Meta:
        model = investorSourceDetails
        exclude = ('profileOwner', 'publish', 'created', 'updated', 'status')


class stockBrokerDetailsForm(forms.ModelForm):
    class Meta:
        model = stockBrokerDetails
        exclude = ('author', 'publish', 'created', 'updated', 'status')


class lookingToInvestDetailsForm(forms.ModelForm):
    class Meta:
        model = lookingToInvestDetails
        exclude = ('author', 'publish', 'created', 'updated', 'status')


# code need to be add by shubham ends


class investorAdharVerificationForm(forms.ModelForm):
    class Meta:
        model = investorPersonalDetails
        fields = ['aadharVerified', 'panVerified', 'personalDetailVerified']
        widgets = {
            'aadharVerified': forms.RadioSelect,
            'panVerified': forms.RadioSelect,
            'panVerified': forms.RadioSelect,
        }


class investorBankVerifyStausForm(forms.ModelForm):
    class Meta:
        model = investorBankDetails
        fields = ['bankVerified']


class investorDmatVerifyStausForm(forms.ModelForm):
    class Meta:
        model = investorDMATDetails
        fields = ['dmatVerified']


#########################################################################################

class personalVerificationStatusForm(forms.ModelForm):
    class Meta:
        model = verificationStatus
        fields = ['panVerifiedStatus', 'personalDetailVerifiedStatus', 'aadharVerifiedStatus', 'profileOwner']


class investorPortfolioForm(forms.ModelForm):
    class Meta:
        model = Transaction
        exclude = ('publish', 'updated', 'created', 'status', 'made_by', 'order_id', 'checksum', 'pg_MID', 'pg_txnID',
                   'pg_txnAmount', 'pg_paymentMode', 'pg_txnDate', 'pg_currency', 'pg_status', 'pg_repsonseCode',
                   'pg_responseMsg', 'pg_gatewayName', 'pg_bankTxnID', 'pg_bankName', 'pg_checkSubHash')


class tempUserForm(forms.ModelForm):
    class Meta:
        model = tempUser
        exclude = ('publish', 'updated', 'created', 'status', 'profileOwner')


class tempTransactionForm(forms.ModelForm):
    class Meta:
        model = tempTransaction
        exclude = ('publish', 'updated', 'created', 'status', 'profileOwner')


class shareBookTransactionsListForm(forms.ModelForm):
    class Meta:
        model = Transaction
        exclude = (
            'publish', 'updated', 'created', 'sb_Company', 'sb_Depository', 'status', 'made_by', 'checksum', 'pg_MID',
            'pg_txnID', 'pg_txnAmount', 'pg_paymentMode', 'pg_txnDate', 'pg_currency', 'pg_repsonseCode',
            'pg_responseMsg',
            'pg_gatewayName', 'pg_bankTxnID', 'pg_bankName', 'pg_checkSubHash')


class shareBookStatusDetailsForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ('sb_Company', 'sb_Depository', 'sb_shareTransfer', 'sb_uploadTransferRequest')


class transactionDocsForm(forms.ModelForm):
    class Meta:
        model = transactionDocs
        exclude = ('publish', 'updated', 'created', 'status', 'related_transaction')
