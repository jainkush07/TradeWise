from django.core.validators import RegexValidator
from django.core.validators import EmailValidator
from django.core.validators import ValidationError
from investorApp.services.kyc.constants import InvestmentMarket, Regex
from investorApp.constants import SebiRegistrationTypes
from investorApp.services.kyc.config import StepName
from datetime import datetime


def name_validator(name):
    name_validators = RegexValidator(Regex.NAME_REGEX.value, 'Enter Valid name')
    try:
        name_validators(name.strip())
        return True
    except ValidationError:
        return False


# it requires a minimum of 3 chars while name validator just needs one ;)
def pan_name_validator(name):
    pan_name_validate = RegexValidator(
        '^[a-zA-Z0-9 ]{3,100}$', 'Enter Valid Name'
    )
    try:
        pan_name_validate(name.strip())
        return True
    except ValidationError:
        return False


def email_validator(email):
    try:
        email_validators = EmailValidator()
        email_validators(email)
        return True
    except ValidationError:
        return False


def pan_validator(pan_num):
    pan_validators = RegexValidator(
        '[A-Z]{5}[0-9]{4}[A-Z]{1}', 'Enter Valid PAN card'
    )
    try:
        if len(pan_num.strip()) != 10:
            return False
        pan_validators(pan_num.strip())
        return True
    except ValidationError:
        return False


def dob_validator(dob):
    try:
        dt = datetime.strptime(dob, "%d-%m-%Y")
        if 47450 < (datetime.now() - dt).days < 3650:
            return False
        return True
    except ValidationError:
        return False


def address_validator(address):
    address_validators = RegexValidator(
        '^[#.0-9a-zA-Z\s,()-\\\/]{2,100}$', 'Enter Valid address'
    )
    try:
        address_validators(address.strip())
        return True
    except ValidationError:
        return False


def pincode_validator(pincode):
    pincode_validators = RegexValidator(
        '^[0-9]\w{5,5}$', 'Enter Valid pin code'
    )
    try:
        pincode_validators(pincode)
        return True
    except ValidationError:
        return False


def investment_market_validator(market):
    validation_list = InvestmentMarket.list()
    if type(market) == list:
        for i in market:
            if i not in validation_list:
                return False
    else:
        if market not in validation_list:
            return False
    return True


def ifsc_validator(ifsc):
    validator = RegexValidator(
        Regex.IFSC_REGEX.value, 'Enter Valid Ifsc'
    )
    try:
        validator(ifsc)
        return True
    except ValidationError:
        return False


def account_num_validator(num):
    validator = RegexValidator(
        Regex.ACC_NUM_REGEX.value, 'Enter Valid account number'
    )
    try:
        validator(num)
        return True
    except ValidationError:
        return False


def validate_sebi_regiteration(registeration_type, registeration_number):
    regex_config = {
        SebiRegistrationTypes.IVC: 'IN/VCF/[0-9]{2}-[0-9]{2}/[0-9]{4}$',
        SebiRegistrationTypes.FVC: 'IN/FVCF/[0-9]{2}-[0-9]{2}/[0-9]{4}$',
        SebiRegistrationTypes.FPI: 'IN[A-Z]{4}[0-9]{6}$',
        SebiRegistrationTypes.AIF: 'IN/AIF[0-9]/[0-9]{2}-[0-9]{2}/[0-9]{4}$',
        SebiRegistrationTypes.MUTUAL_FUND: 'MF/[0-9]{3}/[0-9]{2}/[0-9]{2}$',
        SebiRegistrationTypes.PORTFOLIO_MANAGER: 'INP[0-9]{9}$',
        SebiRegistrationTypes.SYNDICATE_BANK: 'RBI3[a-z0-9A-Z][a-z,:,/ -.0-9***A-Z]{1,101}$'
    }
    error_msg_config = {
        SebiRegistrationTypes.IVC: 'Enter Valid Registration in Format - IN/VCF/xx-xx/xxxx',
        SebiRegistrationTypes.FVC: 'Enter Valid Registration in Format - IN/FVCF/xx-xx/xxxx',
        SebiRegistrationTypes.FPI: 'Enter Valid Registration in Format - INxxxxyyyyyy',
        SebiRegistrationTypes.AIF: 'Enter Valid Registration in Format - IN/AIFx/xx-xx/xxxx',
        SebiRegistrationTypes.MUTUAL_FUND: 'Enter Valid Registration in Format - MF/xxx/xx/xx',
        SebiRegistrationTypes.PORTFOLIO_MANAGER: 'Enter Valid Registration in Format - INPxxxxxxxxx',
        SebiRegistrationTypes.SYNDICATE_BANK: 'Enter Valid Registration in Format'

    }
    if regex_config.get(registeration_type):
        validator = RegexValidator(
            regex_config.get(registeration_type), 'Enter Valid registeration number'
        )
        try:
            validator(registeration_number)
            return True, ''
        except ValidationError:
            return False, error_msg_config.get(registeration_type, 'Enter Valid registeration number')
    return True, ''


def validate_step_data(step, role, data):
    validation_resp = {'status': True}
    validation_config = {
        'panNumber': pan_validator,
        'address': address_validator,
        'pinCode': pincode_validator,
        'name': name_validator,
        'investment_market': investment_market_validator,
        'bankName': name_validator,
        'accountHolder': name_validator,
        'ifsc': ifsc_validator,
        'accountNumber': account_num_validator,
        'dob': dob_validator
    }
    err_msg_config = {
        'panNumber': "Enter a valid pan",
        'address': "Enter a valid address",
        'pinCode': "Enter a valid pincode",
        'name': "Enter a valid name",
        'bankName': "Enter a valid bank",
        'accountHolder': "Enter a valid account holder name",
        'ifsc': "Enter a valid ifsc",
        'accountNumber': "Enter a valid account number",
        "dob": "Enter a valid date of birth"
    }
    allowed_empty_fields = ['pinCode', 'address']
    for key, val in data.items():
        if key in validation_config.keys():
            if not val:
                if key in allowed_empty_fields:
                    continue
                else:
                    validation_resp['status'] = False
                    validation_resp["key"] = key
                    validation_resp["message"] = err_msg_config.get(key)
                    break
            if not validation_config[key](val):
                validation_resp['status'] = False
                validation_resp["key"] = key
                validation_resp["message"] = err_msg_config.get(key, f'invalid {key}')
                break
    if step == StepName.D_MAT_DETAILS:
        if data.get('depository') == 'NSDL':
            if data.get('dpID'):
                if len(data.get('dpID')) != 8 or data.get('dpID')[:2] != 'IN':
                    validation_resp['status'] = False
                    validation_resp["key"] = 'dpID'
                    validation_resp["message"] = 'Enter Valid DP ID in Format - IN123456'
                try:
                    int(data.get('dpID')[2:])
                except:
                    validation_resp['status'] = False
                    validation_resp["key"] = 'dpID'
                    validation_resp["message"] = 'Enter Valid DP ID in Format - IN123456'
        elif data.get('depository') == 'CDSL':
            if data.get('dpID'):
                try:
                    int(data.get('dpID'))
                except:
                    validation_resp['status'] = False
                    validation_resp["key"] = 'dpID'
                    validation_resp["message"] = 'Enter Valid DP ID in Format - 12345678'
                if str(data.get('dpID'))[0] == '0' or len(data.get('dpID')) != 8:
                    validation_resp['status'] = False
                    validation_resp["key"] = 'dpID'
                    validation_resp["message"] = 'Enter Valid DP ID in Format - 12345678'
        if data.get('clientID'):
            client = str(data.get('clientID'))
            if len(client) != 8:
                validation_resp['status'] = False
                validation_resp["key"] = 'clientID'
                validation_resp["message"] = '8 Digits Client ID required'
    elif step == StepName.COMPANY_DETAILS:
        if data.get('sebi_registeration'):
            valid, err_msg = validate_sebi_regiteration(data.get('registered_with'), data.get('sebi_registeration'))
            if not valid:
                validation_resp['status'] = False
                validation_resp["key"] = 'sebi_registeration'
                validation_resp["message"] = err_msg
    return validation_resp
