import json
import pdfkit
from django.core.cache import cache
from django.template import Template, Context
from investorApp.services.kyc.config import StepName
from django.conf import settings
from investorApp.services.kyc.constants import Regex, INVESTMENT_MARKET_OPTIONS, GENDER_OPTIONS, UserRoleTypes, \
    InvestmentMarket, MAJOR_SECTOR_OPTIONS
from investorApp.models import city, state, country, stockBrokerDetails, lookingToInvestDetails, Portfolio_Range, \
    Depository_Info, AccountType_Info, Transfer_Type_Choices, COMPANY_SIGNED_CHOICES, Boolean_Choice, \
    CHANNEL_PARTNER_COMPANY_REGISTERATION_CHOICES, CompanySectors, DEALER_NETWORK_OPTIONS, \
    COMPANY_REGISTERATION_CHOICES, CompanyStages, ROFR_CHOICES, ESOP_SHARE_DEMATERIALISED, INFLUENCER_CHOICES


def create_common_choices(options, data, key):
    """
    :param options:
    :param data:
    :param key:
    :return: generic function to update, create choices
    """
    option = list()
    i = 1
    for obj in options:
        checker = obj[0]
        if len(obj) > 2:
            checker = obj[2]
        option.append({
            "title1": {
                "text": obj[1],
                "color": "#FFFFFF",
            },
            "value": obj[0],
            'img': {
                "url": obj[3]
            } if len(obj) > 3 else None,
            "isSelected": checker == data.get(key) if type(data.get(key)) != list else checker in data.get(key)
        })
        i = i + 1

    return json.dumps(option)


def fill_template_config(config: dict, data: dict, step: str = None) -> dict:
    """
    :param config:
    :param data:
    :param step:
    :return: Will do template rendering in a json with strings (there are some hacks and issues involved with ')
    """
    for key, val in data.items():
        if val is None:
            data[key] = ''
    temp_config = json.dumps(config)
    if step:
        # special handling for specific steps to substitute the options so that they can be rendered
        # as their data type rather thn string
        if step == StepName.PERSONAL_DETAILS:
            temp_config = temp_config.replace('"{{gender_options}}"', "{{ gender_options|safe }}")
        elif step == StepName.COMPANY_DETAILS:
            temp_config = temp_config.replace('"{{signed_as_options}}"', "{{ signed_as_options|safe }}")
            temp_config = temp_config.replace('"{{resgistered_options}}"', "{{ resgistered_options|safe }}")
            temp_config = temp_config.replace('"{{gst_options}}"', "{{ gst_options|safe }}")
            temp_config = temp_config.replace('"{{company_sector_options}}"', "{{ company_sector_options|safe }}")
            temp_config = temp_config.replace('"{{valuation_status_options}}"', "{{ valuation_status_options|safe }}")
            temp_config = temp_config.replace('"{{share_dematerial_options}}"', "{{ share_dematerial_options|safe }}")

            temp_config = temp_config.replace('"{{influencer_choices}}"', "{{ influencer_choices|safe }}")
            temp_config = temp_config.replace('"{{company_sector_accordian_options}}"',
                                              "{{ company_sector_accordian_options|safe }}")

        elif step == StepName.INVESTMENT_DETAILS:
            temp_config = temp_config.replace('"{{present_portfolio_list}}"', "{{ present_portfolio_list|safe }}")
            temp_config = temp_config.replace('"{{invest_portfolio_list}}"', "{{ invest_portfolio_list|safe }}")
            temp_config = temp_config.replace('"{{investment_market_options}}"', "{{ investment_market_options|safe }}")
            temp_config = temp_config.replace('"{{looking_to_invest_option_list}}"',
                                              "{{ looking_to_invest_option_list|safe }}")
            temp_config = temp_config.replace('"{{company_stage_options}}"',
                                              "{{ company_stage_options|safe }}")
            temp_config = temp_config.replace('"{{asset_portfolio_options}}"',
                                              "{{ asset_portfolio_options|safe }}")
            temp_config = temp_config.replace('"{{invest_sector_options}}"',
                                              "{{ invest_sector_options|safe }}")
        elif step == StepName.SOCIAL_INFORMATION:
            temp_config = temp_config.replace('"{{is_fin_influencer_choices}}"', "{{ is_fin_influencer_choices|safe }}")

        elif step == StepName.BANK_DETAILS:
            temp_config = temp_config.replace('"{{account_type_options}}"', "{{ account_type_options|safe }}")
        elif step == StepName.D_MAT_DETAILS:
            temp_config = temp_config.replace('"{{depository_options}}"', "{{ depository_options|safe }}")
            temp_config = temp_config.replace('"{{stock_broker_options}}"', "{{ stock_broker_options|safe }}")
        elif step == StepName.TRANSFER_FACILITY:
            temp_config = temp_config.replace('"{{transfer_type_options}}"', "{{ transfer_type_options|safe }}")
        elif step == StepName.DEALER_DETAILS:
            temp_config = temp_config.replace('"{{dealer_network_options}}"', "{{ dealer_network_options|safe }}")
        elif step == StepName.ESOP_COMPANY_DETAILS:
            temp_config = temp_config.replace('"{{rofr_options}}"', "{{ rofr_options|safe }}")
            temp_config = temp_config.replace('"{{valuation_status_options}}"', "{{ valuation_status_options|safe }}")
            temp_config = temp_config.replace('"{{share_dematerial_options}}"', "{{ share_dematerial_options|safe }}")
        elif step == StepName.ASSET_MANAGEMENT:
            temp_config = temp_config.replace('"{{asset_portfolio_options}}"',
                                              "{{ asset_portfolio_options|safe }}")
    conf = Template(temp_config).render(Context(data))
    return json.loads(conf)


def fetch_city_options(state_id: str = ''):
    options = []
    key = 'cities_data_options'
    if state_id:
        key = f'{key}_{state_id}'
    cached_date = cache.get(key)
    if not cached_date:
        if state_id:
            cities = city.objects.filter(cityState_id=state_id).values('name', 'id').all()
        else:
            cities = city.objects.values('name', 'id').all()
        cached_date = cities
        cache.set(key, cached_date, 3000)
    for _city in cached_date:
        options.append((_city['id'], _city['name']))
    return options


def fetch_state_options(country_id: str = None):
    options = []
    key = 'states_data_options'
    if country_id:
        key = f'{key}_{country_id}'
    cached_date = cache.get(key)
    if not cached_date:
        if country_id:
            states = state.objects.filter(stateCountry_id=country_id).values('name', 'id').all()
        else:
            states = state.objects.values('name', 'id').all()
        cached_date = states
        cache.set(key, cached_date, 3000)

    for _state in cached_date:
        options.append((_state['id'], _state['name']))
    return options


def fetch_country_options():
    options = []
    key = 'country_data_options'
    cached_date = cache.get(key)
    if not cached_date:
        countries = country.objects.all()
        countries_list = []
        for cntry in countries:
            countries_list.append({'id': cntry.id, 'name': cntry.name, 'url': cntry.flag.url if cntry.flag else ''})
        cached_date = countries_list
        cache.set(key, cached_date, 3000)

    for _country in cached_date:
        options.append((_country['id'], _country['name'], _country['id'], _country['url']))
    return options


def fetch_stock_broker_options():
    options = []
    key = 'stockBrokerDetails_data_options'
    cached_date = cache.get(key)
    if not cached_date:
        cities = stockBrokerDetails.objects.values('name', 'id').all()
        cached_date = cities
        cache.set(key, cached_date, 3000)
    for _c in cached_date:
        options.append((_c['id'], _c['name']))
    return options


def fetch_looking_investment_options():
    options = []
    key = 'looking_investment_data_options'
    cached_date = cache.get(key)
    if not cached_date:
        op = lookingToInvestDetails.objects.values('name', 'id').all()
        cached_date = op
        cache.set(key, cached_date, 3000)
    for _c in cached_date:
        options.append((_c['id'], _c['name']))
    return options


def fetch_company_inv_stage_options():
    options = []
    key = 'company_stage_data_options'
    cached_date = cache.get(key)
    if not cached_date:
        op = CompanyStages.objects.values('name', 'id').all()
        cached_date = op
        cache.set(key, cached_date, 3000)
    for _c in cached_date:
        options.append((_c['id'], _c['name']))
    return options


def fetch_company_sector_options():
    options = []
    key = 'company_sector_data_options'
    cached_date = cache.get(key)
    if not cached_date:
        op = CompanySectors.objects.values('name', 'id').all()
        cached_date = op
        cache.set(key, cached_date, 3000)
    for _c in cached_date:
        options.append((_c['id'], _c['name']))
    return options


def fetch_company_sectors():
    key = 'company_sector_data_list2'
    cached_date = cache.get(key)
    if not cached_date:
        cached_date = list(CompanySectors.objects.all().values('id', 'name'))
        cache.set(key, cached_date, 3000)
    return cached_date


def fetch_screen_options(step, role, data):
    conf = {"base_url": settings.BASE_URL, "step": step, Regex.IFSC_REGEX.name: Regex.IFSC_REGEX.value,
            Regex.ACC_NUM_REGEX.name: Regex.ACC_NUM_REGEX.value}
    # options needs to configured in common json template render
    if step == StepName.PERSONAL_DETAILS:
        conf['gender_options'] = create_common_choices(GENDER_OPTIONS, data, 'gender')
    elif step == StepName.COMPANY_DETAILS:
        conf['signed_as_options'] = create_common_choices(COMPANY_SIGNED_CHOICES, data, 'signed_as')
        conf['valuation_status_options'] = create_common_choices(Boolean_Choice, data, 'valuation_status')
        conf['share_dematerial_options'] = create_common_choices(Boolean_Choice, data,
                                                                 'share_dematerialized')
        company_registered_choices = CHANNEL_PARTNER_COMPANY_REGISTERATION_CHOICES
        if role and role != UserRoleTypes.CHANNEL_PARTNER.value:
            company_registered_choices = COMPANY_REGISTERATION_CHOICES
        else:
            conf['influencer_choices'] = create_common_choices(INFLUENCER_CHOICES, data,
                                                               'influencer')
        conf['resgistered_options'] = create_common_choices(company_registered_choices, data, 'registered_with')
        conf['gst_options'] = create_common_choices(Boolean_Choice, data, 'gst_applicable')
        # conf['company_sector_options'] = create_common_choices(fetch_company_sector_options(), data, 'company_sector')

    elif step == StepName.INVESTMENT_DETAILS:

        conf['looking_to_invest_option_list'] = create_common_choices(fetch_looking_investment_options(), data,
                                                                      'lookingToInvest')
        conf['investment_market_options'] = create_common_choices(INVESTMENT_MARKET_OPTIONS, data,
                                                                  'investment_market')

        if role == UserRoleTypes.VC.value:
            conf['asset_portfolio_options'] = create_common_choices(Portfolio_Range, data, 'assetPortfolioManaging')
            conf['company_stage_options'] = create_common_choices(fetch_company_inv_stage_options(), data,
                                                                  'companyStage')
            conf['invest_sector_options'] = create_common_choices(MAJOR_SECTOR_OPTIONS, data,
                                                                  'sectorToInvest')
        else:
            conf['present_portfolio_list'] = create_common_choices(Portfolio_Range, data, 'presentPortfolio')

            conf['invest_portfolio_list'] = create_common_choices(Portfolio_Range, data, 'investPorfolio')
    elif step == StepName.ASSET_MANAGEMENT:
        conf['asset_portfolio_options'] = create_common_choices(Portfolio_Range, data, 'asset_portfolio_managing')
    elif step == StepName.BANK_DETAILS:
        conf['account_type_options'] = create_common_choices(AccountType_Info, data, 'accountType')
    elif step == StepName.D_MAT_DETAILS:
        conf['depository_options'] = create_common_choices(Depository_Info, data, 'depository')
        conf['stock_broker_options'] = create_common_choices(fetch_stock_broker_options(), data, 'stockBroker_id')
    elif step == StepName.TRANSFER_FACILITY:
        conf['transfer_type_options'] = create_common_choices(Transfer_Type_Choices, data, 'transfer_type')
    elif step == StepName.DEALER_DETAILS:
        conf['dealer_network_options'] = create_common_choices(DEALER_NETWORK_OPTIONS, data, 'network')
    elif step == StepName.ESOP_COMPANY_DETAILS:
        conf['valuation_status_options'] = create_common_choices(ROFR_CHOICES, data, 'valuation_status')
        conf['rofr_options'] = create_common_choices(ROFR_CHOICES, data, 'rofr')
        conf['share_dematerial_options'] = create_common_choices(ESOP_SHARE_DEMATERIALISED, data,
                                                                 'share_dematerialized')
    elif step == StepName.SOCIAL_INFORMATION:
        conf['is_fin_influencer_choices'] = create_common_choices(Boolean_Choice, data,
                                                                  'is_fin_influencer')
    return conf


def fetch_fields_option(role, field, query_params, data):
    res = None
    if field == 'country':
        res = create_common_choices(fetch_country_options(), data, 'country_id')
    elif field == 'state':
        res = create_common_choices(fetch_state_options(query_params.get('country')), data, 'state_id')
    elif field == 'city':
        res = create_common_choices(fetch_city_options(query_params.get('state')), data, 'city_id')
    if res:
        return {'status': True, 'data': json.loads(res)}
    return {'status': False, 'message': 'invalid field'}


def fetch_delete_config():
    return {
        "text": "Delete",
        "endpoint": "{{base_url}}/investor/kyc/user/{{step}}/{{pk}}/",
        "body": {}
    }


def format_kyc_data(data, role, step):
    if role == UserRoleTypes.CHANNEL_PARTNER.value and step == StepName.COMPANY_DETAILS:
        if data.get('company_sector_dict') and type(data.get('company_sector_dict')) == dict:
            data['company_sector'] = list(data['company_sector_dict'].keys())
            for key, val in data['company_sector_dict'].items():
                for sub_field, sub_val in val.items():
                    data[f'{sub_field}__{key}'] = sub_val
    if step == StepName.INVESTMENT_DETAILS:
        if data.get('investment_market'):
            if InvestmentMarket.PRIMARY.value in data.get('investment_market'):
                data['primaryMarket'] = True
            else:
                data['primaryMarket'] = False
            if InvestmentMarket.SECONDARY.value in data.get('investment_market'):
                data['secondaryMarket'] = True
            else:
                data['secondaryMarket'] = False
    if data.get('valuation') == '':
        data['valuation'] = 0
    if data.get('mobileNumber'):
        del data['mobileNumber']
    return data


def generate_html_pdf(html):
    options = {
        'page-height': "855px",
        'page-width': "450px",
        'margin-top': '20px',
        'margin-right': '1px',
        'margin-bottom': '5px',
        'margin-left': '1px',
        'encoding': "UTF-8",
        'disable-smart-shrinking': '',
        'no-outline': None,
        '--enable-javascript': '',
        'enable-local-file-access': None
    }
    pdf = pdfkit.from_string(html, False, options=options)
    return pdf
