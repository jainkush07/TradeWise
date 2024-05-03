class StepName:
    PERSONAL_DETAILS = 'PERSONAL_DETAILS'
    INS_PERSONAL_DETAILS = 'INS_PERSONAL_DETAILS'
    BANK_DETAILS = 'BANK_DETAILS'
    INVESTMENT_DETAILS = 'INVESTMENT_DETAILS'
    D_MAT_DETAILS = 'D_MAT_DETAILS'
    ADDRESS_DETAILS = 'ADDRESS_DETAILS'
    PAN_DETAILS = 'PAN_DETAILS'
    AADHAR_DETAILS = 'AADHAR_DETAILS'
    UPLOAD_PAN = 'UPLOAD_PAN'
    EMAIL_VERIFY = 'EMAIL_VERIFY'
    MOBILE_VERIFY = 'MOBILE_VERIFY'
    UPLOAD_AADHAAR = 'UPLOAD_AADHAAR'
    COMPANY_DETAILS = 'COMPANY_DETAILS'
    ESOP_COMPANY_DETAILS = 'ESOP_COMPANY_DETAILS'
    TRANSFER_FACILITY = 'TRANSFER_FACILITY'
    DEALER_DETAILS = 'DEALER_DETAILS'
    CHANNEL_PARTNER_DETAILS = 'CHANNEL_PARTNER_DETAILS'
    PARTNER_AGREEMENT = 'PARTNER_AGREEMENT'
    SOCIAL_INFORMATION = 'SOCIAL_INFORMATION'
    COMPANY_FINANCIALS = 'COMPANY_FINANCIALS'
    ASSET_MANAGEMENT = 'ASSET_MANAGEMENT'


InvestorKycConfig = [
    StepName.PERSONAL_DETAILS,
    StepName.INVESTMENT_DETAILS,
    StepName.BANK_DETAILS,
    StepName.D_MAT_DETAILS
]

ChannelPartnerKycConfig = [
    StepName.PERSONAL_DETAILS,
    StepName.SOCIAL_INFORMATION,
    StepName.COMPANY_DETAILS,
    StepName.ASSET_MANAGEMENT,
    StepName.BANK_DETAILS,
    StepName.D_MAT_DETAILS,
    StepName.TRANSFER_FACILITY,
    StepName.PARTNER_AGREEMENT
]

PrivateBanksKycConfig = [
    StepName.PERSONAL_DETAILS,
    StepName.SOCIAL_INFORMATION,
    StepName.COMPANY_DETAILS,
    StepName.BANK_DETAILS,
    StepName.D_MAT_DETAILS,
    StepName.TRANSFER_FACILITY
]

DealerKycConfig = [
    StepName.DEALER_DETAILS,
    StepName.PERSONAL_DETAILS,
    StepName.SOCIAL_INFORMATION,
    StepName.COMPANY_DETAILS,
    StepName.ASSET_MANAGEMENT,
    StepName.BANK_DETAILS,
    StepName.D_MAT_DETAILS,
    StepName.TRANSFER_FACILITY
]

EsopKycConfig = [
    StepName.PERSONAL_DETAILS,
    StepName.ESOP_COMPANY_DETAILS,
    StepName.BANK_DETAILS,
    StepName.D_MAT_DETAILS,
    StepName.TRANSFER_FACILITY
]

InstitutionalKycConfig = [
    StepName.INS_PERSONAL_DETAILS,
    StepName.COMPANY_DETAILS,
    StepName.INVESTMENT_DETAILS,
    StepName.BANK_DETAILS,
    StepName.D_MAT_DETAILS,
    StepName.TRANSFER_FACILITY
]

FounderKycConfig = [
    StepName.INS_PERSONAL_DETAILS,
    StepName.COMPANY_DETAILS,
    StepName.INVESTMENT_DETAILS,
    StepName.BANK_DETAILS,
    StepName.D_MAT_DETAILS,
    StepName.TRANSFER_FACILITY
]

FOKycConfig = [
    StepName.PERSONAL_DETAILS,
    StepName.COMPANY_DETAILS,
    StepName.INVESTMENT_DETAILS,
    StepName.BANK_DETAILS,
    StepName.D_MAT_DETAILS,
    StepName.TRANSFER_FACILITY
]

AuthorKycConfig = [
    StepName.PERSONAL_DETAILS,
    StepName.SOCIAL_INFORMATION
]

KycFeConfig = {
    StepName.PERSONAL_DETAILS:
        {
            'step': StepName.PERSONAL_DETAILS,
            'label': 'Personal Details',
        },
    StepName.INS_PERSONAL_DETAILS:
        {
            'step': StepName.INS_PERSONAL_DETAILS,
            'label': 'Fund Manager Details',
        },
    StepName.COMPANY_DETAILS:
        {
            'step': StepName.COMPANY_DETAILS,
            'label': 'Company Details',
        },
    StepName.ESOP_COMPANY_DETAILS:
        {
            'step': StepName.ESOP_COMPANY_DETAILS,
            'label': 'Company Details',
        },
    StepName.BANK_DETAILS:
        {
            'step': StepName.BANK_DETAILS,
            'label': 'Bank Details',
        },
    StepName.D_MAT_DETAILS:
        {
            'step': StepName.D_MAT_DETAILS,
            'label': 'Demat Details',
        },
    StepName.TRANSFER_FACILITY:
        {
            'step': StepName.TRANSFER_FACILITY,
            'label': 'Transfer Facility',
        },
    StepName.DEALER_DETAILS:
        {
            'step': StepName.DEALER_DETAILS,
            'label': 'Dealer Network',
        },
    StepName.INVESTMENT_DETAILS:
        {
            'step': StepName.INVESTMENT_DETAILS,
            'label': 'Investment Details',
        },
    StepName.PARTNER_AGREEMENT:
        {
            'step': StepName.PARTNER_AGREEMENT,
            'label': 'Kyc Agreement',
        },
    StepName.SOCIAL_INFORMATION: {
        'step': StepName.SOCIAL_INFORMATION,
        'label': 'Social Details',
    },
    StepName.ASSET_MANAGEMENT: {
        'step': StepName.ASSET_MANAGEMENT,
        'label': 'Asset Management',
    }
}
