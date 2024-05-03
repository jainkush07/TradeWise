from investorApp.services.kyc.config import StepName

BANK_DETAIL_PAGE_CONF = {
    "screen_name": StepName.BANK_DETAILS,
    "label": "Bank Details",
    "allowMultipleSection": True,
    "sections": [

    ]
}
BANK_DETAIL_SECTION = {
    "heading": "{{heading}}",
    "subHeading": "",
    "components": [
        {
            "componentType": "default",
            "componentId": "3ea8b28a91a34517ac9b80c50c830671",
            "componentProperties": {
                "title1": {
                    "text": "Set as Default",
                    "color": "#757779",

                },
                "apiKey": "is_default",
                "fluid": True,
                "preFillVal": "{{is_default}}",
                "autoSave": True,
                "validations": {
                    "required": False
                }
            }
        },
        {
            "componentType": "alpha",
            "componentId": "fe2a9603401f469c9f0d04366d9676a3",
            "componentProperties": {
                "title1": {
                    "text": "Bank Name",
                    "color": "#757779",

                },
                "apiKey": "bankName",
                "preFillVal": "{{bankName}}",
                "transformer": 'capitalize',
                "validations": {
                    "required": True,
                    "min_characters": 2,
                    "max_characters": 50,
                    "regex": "^[a-zA-Z][a-z 'A-Z]{2,50}$"
                }
            }
        },
        {
            "componentType": "alpha",
            "componentId": "9ce84fe374da451b8ff2ebca8b5ce05b",
            "componentProperties": {
                "title1": {
                    "text": "Account Holder",
                    "color": "#757779",

                },
                "apiKey": "accountHolder",
                "transformer": 'capitalize',
                "preFillVal": "{{accountHolder}}",
                "validations": {
                    "required": True,
                    "min_characters": 2,
                    "max_characters": 50,
                }
            }
        },
        {
            "componentType": "numeric",
            "componentId": "dfdcccffebf643e6b9b4789e6d5a1f00",
            "componentProperties": {
                "title1": {
                    "text": "Account Number",
                    "color": "#757779",

                },
                "apiKey": "accountNumber",
                "preFillVal": "{{accountNumber}}",
                "validations": {
                    "required": True,
                    "min_characters": 9,
                    "max_characters": 18,
                    "regex": "{{ACC_NUM_REGEX}}"
                }
            }
        },
        {
            "componentType": "dropdown",
            "componentId": "b9a7684961194cf1b61fc2ea5c937393",
            "componentProperties": {
                "title1": {
                    "text": "Account Type",
                    "color": "#757779",

                },
                "apiKey": "accountType",
                "multiSelection": False,
                "list": '{{account_type_options}}',
                "validations": {
                    "required": True
                }
            }
        },
        {
            "componentType": "alpha_numeric",
            "componentId": "e15270fafafb40ae92d805e5c93a13f6",
            "componentProperties": {
                "title1": {
                    "text": "IFSC",
                    "color": "#757779",

                },
                "apiKey": "ifsc_Code",
                "transformer": 'uppercase',
                "preFillVal": "{{ifsc_Code}}",
                "validations": {
                    "required": True,
                    "min_characters": 11,
                    "max_characters": 11,
                    "regex": "{{IFSC_REGEX}}"
                }
            }
        },
        {
            "componentType": "alpha_numeric",
            "componentId": "e3ac745206d44e588599eaf37a5ab7c4",
            "componentProperties": {
                "title1": {
                    "text": "Upi Id",
                    "color": "#757779",

                },
                "apiKey": "upiID",
                "preFillVal": "{{upiID}}",
                "validations": {
                    "required": False,
                    "min_characters": 2,
                    "max_characters": 64,
                    "regex": "{{UPI_REGEX}}"
                }
            }
        },
        {
            "componentType": "doc_upload",
            "componentId": "be54f3c2529a4c5fa456454b79fca4fb",
            "componentProperties": {
                "title1": {
                    "text": "Cancelled Cheque/ Bank Statement",
                    "color": "#757779",

                },
                "preFillVal": "{{cc_url}}",
                "apiKey": "cancelledCheque",
                "refresh": True,
                "api": {
                    "endpoint": "{{base_url}}/investor/kyc/document/?step={{step}}",
                    "body": {
                        "pk": "{{pk}}"
                    },
                    "param_required": True
                },
                "validations": {
                    "required": False
                }
            }
        },

    ],
    "submit": {
        "text": "Save",
        "endpoint": "{{base_url}}/investor/kyc/user/?step={{step}}",
        "body": {
            "step": "{{step}}",
            "pk": "{{pk}}"
        }
    }
}
DMAT_PAGE_CONF = {
    "screen_name": StepName.D_MAT_DETAILS,
    "label": "DEMAT Details",
    "allowMultipleSection": True,
    "sections": [

    ]
}
DMAT_SECTION = {
    "heading": "{{heading}}",
    "subHeading": "",
    "components": [
        {
            "componentType": "default",
            "componentId": '812b1a4a83974892bca83080cda5bd42',
            "componentProperties": {
                "title1": {
                    "text": "Set as Default",
                    "color": "#757779",

                },
                "apiKey": "is_default",
                "fluid": True,
                "preFillVal": "{{is_default}}",
                "autoSave": True,
                "validations": {
                    "required": False
                }
            }
        },
        {
            "componentType": "searchable_dropdown",
            "componentId": "c96810032b7e4bb8b4cbabb5e3f33a1a",
            "componentProperties": {
                "title1": {
                    "text": "Stock Broker",
                    "color": "#757779",

                },
                "apiKey": "stockBroker",
                "multiSelection": False,
                "list": '{{stock_broker_options}}',
                "validations": {
                    "required": True
                }
            }
        },
        {
            "componentType": "doc_upload",
            "componentId": "31409f2d46de4f22b236e74d85d19bc9",
            "componentProperties": {
                "title1": {
                    "text": "DEMAT Client Master Report",
                    "color": "#757779",

                },
                "preFillVal": "{{demat_client_master_url}}",
                "apiKey": "dmatClientMasterReport",
                "api": {
                    "endpoint": "{{base_url}}/investor/kyc/document/?step={{step}}",
                    "body": {
                        "pk": "{{pk}}"
                    },
                    "param_required": True
                },
                "refresh": True,
                "validations": {
                    "required": False,
                    "supported_type": ["pdf"]
                }
            }
        },
        {
            "componentType": "dropdown",
            "componentId": "215c86fd2b904dfba8d66a4b5a27a21c",
            "componentProperties": {
                "title1": {
                    "text": "Depository",
                    "color": "#757779",

                },
                "apiKey": "depository",
                "multiSelection": False,
                "list": '{{depository_options}}',
                "validations": {
                    "required": True
                }
            }
        },
        {
            "componentType": "alpha_numeric",
            "componentId": "02e7e4c94705470aaeba5c1263ca5202",
            "componentProperties": {
                "title1": {
                    "text": "DP Id",
                    "color": "#757779",

                },
                "apiKey": "dpID",
                "transformer": 'uppercase',
                "preFillVal": "{{dpID}}",
                "validations": {
                    "required": True,
                    "min_characters": 6,
                    "max_characters": 11,
                }
            }
        },
        {
            "componentType": "numeric",
            "componentId": "56afc7b3d3604d8ead8d75c146356488",
            "componentProperties": {
                "title1": {
                    "text": "Client Id",
                    "color": "#757779",

                },
                "apiKey": "clientID",
                "preFillVal": "{{clientID}}",
                "validations": {
                    "required": True,
                    "min_characters": 8,
                    "max_characters": 8,
                }
            }
        },

    ],
    "submit": {
        "text": "Save",
        "endpoint": "{{base_url}}/investor/kyc/user/?step={{step}}",
        "body": {
            "step": "{{step}}",
            "pk": "{{pk}}"
        }
    }
}
TRANSFER_FACILITY_PAGE_CONF = {
    "screen_name": StepName.TRANSFER_FACILITY,
    "label": "Transfer Facility",
    "allowMultipleSection": False,
    "sections": []
}
TRANSFER_FACILITY_SECTION = {
    "heading": "Transfer Facility",
    "subHeading": "",
    "components": [
        {
            "componentType": "dropdown",
            "componentId": "4346f32f848d4672b80f814993b9c52d",
            "componentProperties": {
                "title1": {
                    "text": "How will you transfer shares ?",
                    "color": "#757779",

                },
                "apiKey": "transfer_type",
                "multiSelection": False,
                "list": '{{transfer_type_options}}',
                "validations": {
                    "required": True
                }
            }
        },
        {
            "componentType": "doc_upload",
            "componentId": "615c0983d3574b50b50af731ff745d5c",
            "componentProperties": {
                "title1": {
                    "text": "Transfer file proof",
                    "color": "#757779",

                },
                "preFillVal": "{{transfer_file_proof_url}}",
                "apiKey": "transfer_file_proof",
                "api": {
                    "endpoint": "{{base_url}}/investor/kyc/document/?step={{step}}",
                    "body": {

                    },
                    "param_required": True
                },
                "refresh": True,
                "validations": {
                    "required": False,
                    "supported_type": ["pdf"]
                }
            }
        },

    ],
    "submit": {
        "text": "Save",
        "endpoint": "{{base_url}}/investor/kyc/user/?step={{step}}",
        "body": {
            "step": "{{step}}"
        }
    }
}
PERSONAL_DETAIL_SECTION = {
    "heading": "Personal Details",
    "subHeading": "",
    "components": [
        {
            "componentType": "alpha",
            "componentId": "a496f518c6224c0d95d0952f7379bbdd",
            "componentProperties": {
                "title1": {
                    "text": "Name",
                    "color": "#757779",

                },
                "apiKey": "name",
                "preFillVal": "{{name}}",
                "transformer": 'capitalize',
                "validations": {
                    "required": True,
                    "min_characters": 2,
                    "max_characters": 50
                }
            }
        },
        {
            "componentType": "alpha_numeric",
            "componentId": "3d252243865a4bd6a59b88f1f7dcf699",
            "componentProperties": {
                "title1": {
                    "text": "Email",
                    "color": "#757779",

                },
                "apiKey": "email",
                "preFillVal": "{{email}}",
                "editable": False,
                "validations": {
                    "required": True,
                    "min_characters": 2,
                    "max_characters": 50,
                    "regex": ""
                }
            }
        },
        {
            "componentType": "mobile",
            "componentId": "b2225568d3c94c3295d2a264b2424f25",
            "componentProperties": {
                "title1": {
                    "text": "Mobile",
                    "color": "#757779",

                },
                "apiKey": "mobileNumber",
                "preFillVal": "{{countryCode}}-{{mobileNumber}}",
                "editable": False,
                "validations": {
                    "required": True,
                    "min_characters": 2,
                    "max_characters": 50,
                }
            }
        },
        {
            "componentType": "radio",
            "componentId": "99e6f178132e44768816f275704ae13f",
            "componentProperties": {
                "title1": {
                    "text": "Gender",
                    "color": "#757779",

                },
                "apiKey": "gender",
                "horizontal": True,
                "list": "{{gender_options}}",
                "validations": {
                    "required": True
                }
            }
        },
        {
            "componentType": "date",
            "componentId": "a496ii18c6224c0d95d0952f7379bbdd",
            "componentProperties": {
                "title1": {
                    "text": "Date of Birth",
                    "color": "#757779",

                },
                "apiKey": "dob",
                "preFillVal": "{{dob}}",
                "validations": {
                    "required": True,
                }
            }
        },
        {
            "componentType": "alpha_numeric",
            "componentId": "3a6b9449011a4324a9df808d3373db49",
            "componentProperties": {
                "title1": {
                    "text": "Pan Number",
                    "color": "#757779",

                },
                "apiKey": "panNumber",
                "preFillVal": "{{panNumber}}",
                "transformer": 'uppercase',
                "validations": {
                    "required": True,
                    "min_characters": 9,
                    "max_characters": 10,
                    "regex": "[A-Z]{5}[0-9]{4}[A-Z]{1}$"
                }
            }
        },
        {
            "componentType": "numeric",
            "componentId": "73f25e4476294d3994a4e6c2d1d122f9",
            "componentProperties": {
                "title1": {
                    "text": "Aadhaar Number",
                    "color": "#757779",

                },
                "apiKey": "aadharNumber",
                "preFillVal": "{{aadharNumber}}",
                "validations": {
                    "required": True,
                    "min_characters": 11,
                    "max_characters": 12,
                    "regex": "[2-9]{1}[0-9]{11}$"
                }
            }
        },
        {
            "componentType": "doc_upload",
            "componentId": "0f921d43b43347d0b89903308980a3b9",
            "componentProperties": {
                "title1": {
                    "text": "Pan card",
                    "color": "#757779",

                },
                "preFillVal": "{{upload_pan_url}}",
                "apiKey": "uploadPan",
                "api": {
                    "endpoint": "{{base_url}}/investor/kyc/document/?step={{step}}",
                },
                "validations": {
                    "required": False
                }
            }
        },
        {
            "componentType": "doc_upload",
            "componentId": "5a6a0596c9c94b7fab0f3878a0ef7a32",
            "componentProperties": {
                "title1": {
                    "text": "Aadhaar card",
                    "color": "#757779",

                },
                "preFillVal": "{{upload_aadhaar_url}}",
                "apiKey": "uploadAadhar",
                "api": {
                    "endpoint": "{{base_url}}/investor/kyc/document/?step={{step}}",
                },
                "validations": {
                    "required": False
                }
            }
        },
        {
            "componentType": "searchable_dropdown",
            "componentId": "671aa7a6ebf149c19926309f269a53c4",
            "componentProperties": {
                "title1": {
                    "text": "Country",
                    "color": "#757779",

                },
                "apiKey": "country",
                "multiSelection": False,
                "list": [],
                "fetchOptions": {
                    "type": "api",
                    "endpoint": "{{base_url}}/investor/kyc/field/country/options/?step={{step}}",
                },
                "validations": {
                    "required": True
                }
            }
        },
        {
            "componentType": "searchable_dropdown",
            "componentId": "df33caddad4441e282a5bee2ec6dcc24",
            "dependentOn": '671aa7a6ebf149c19926309f269a53c4',
            "componentProperties": {
                "title1": {
                    "text": "State",
                    "color": "#757779",
                },
                "apiKey": "state",
                "multiSelection": False,
                "list": [],
                "fetchOptions": {
                    "type": "api",
                    "endpoint": "{{base_url}}/investor/kyc/field/state/options/?step={{step}}",
                },
                "validations": {
                    "required": True
                }
            }
        },
        {
            "componentType": "searchable_dropdown",
            "componentId": "630271eec3ab4ee5b35c8a5aa61494f3",
            "dependentOn": 'df33caddad4441e282a5bee2ec6dcc24',
            "componentProperties": {
                "title1": {
                    "text": "City",
                    "color": "#757779",

                },
                "apiKey": "city",
                "multiSelection": False,
                "list": [],
                "fetchOptions": {
                    "type": "api",
                    "endpoint": "{{base_url}}/investor/kyc/field/city/options/?step={{step}}",
                },
                "validations": {
                    "required": True
                }
            }
        },
        {
            "componentType": "numeric",
            "componentId": "29afecdcf4e44ce684712d7d00c84a5d",
            "componentProperties": {
                "title1": {
                    "text": "Pincode",
                    "color": "#757779",

                },
                "apiKey": "pinCode",
                "preFillVal": "{{pinCode}}",
                "validations": {
                    "required": True,
                    "min_characters": 5,
                    "max_characters": 6,
                }
            }
        },
        {
            "componentType": "alpha_numeric",
            "componentId": "26827a9ded06406fa29aea22c90fbb30",
            "componentProperties": {
                "title1": {
                    "text": "Address",
                    "color": "#757779",
                },
                "apiKey": "address",
                "fluid": True,
                "preFillVal": "{{address}}",
                "multiLine": True,
                "validations": {
                    "required": True,
                    "min_characters": 2,
                    "max_characters": 100,
                    "regex": ""
                }
            }
        },
    ],
    "submit": {
        "text": "Save",
        "endpoint": "{{base_url}}/investor/kyc/user/?step={{step}}",
        "body": {
            "step": "{{step}}"
        }
    }
}
PERSONAL_DETAIL_PAGE_CONF = {
    "screen_name": StepName.PERSONAL_DETAILS,
    "label": "Personal Details",
    "allowMultipleSection": False,
    "sections": [

    ]
}
INVESTMENT_DETAIL_SECTION = {
    "heading": "Investment Details",
    "subHeading": "",
    "components": [
        {
            "componentType": "selectable_dropdown",
            "componentId": "2b667fe1f135406ab35968d32e6517ab",
            "componentProperties": {
                "title1": {
                    "text": "Present portfolio ( including stocks and bonds )",
                    "color": "#757779",

                },
                "apiKey": "presentPortfolio",
                "multiSelection": False,
                "list": '{{present_portfolio_list}}',
                "validations": {
                    "required": True
                }
            }
        },
        {
            "componentType": "selectable_dropdown",
            "componentId": "a8bb79d5772c4079aaf08c55994d1810",
            "componentProperties": {
                "title1": {
                    "text": "How much you are looking to invest with planify?",
                    "color": "#757779",

                },
                "apiKey": "investPorfolio",
                "multiSelection": False,
                "list": '{{invest_portfolio_list}}',
                "validations": {
                    "required": True
                }
            }
        },
        {
            "componentType": "checkbox",
            "componentId": "c87eed5d99c4431caea1623f05e03af8",
            "componentProperties": {
                "title1": {
                    "text": "Here for investment in",
                    "color": "#757779",
                },
                "apiKey": "investment_market",
                "multiSelection": True,
                "fluid": True,
                "autoSave": True,
                "list": "{{investment_market_options}}",
                "validations": {
                    "required": True
                }
            }
        },
    ],
    "submit": {
        "text": "Save",
        "endpoint": "{{base_url}}/investor/kyc/user/?step={{step}}",
        "body": {
            "step": "{{step}}"
        }
    }
}
PRIMARY_INVESTMENT_SUB_COMPONENT = {
    "componentType": "dropdown",
    "componentId": "0fef59154f8840e3acbd3a3af3b0be7c",
    "componentProperties": {
        "title1": {
            "text": "Looking to Invest",
            "color": "#757779",

        },
        "apiKey": "lookingToInvest",
        "multiSelection": True,
        "list": '{{looking_to_invest_option_list}}',
        "validations": {
            "required": True
        }
    }
}

INVESTMENT_DETAIL_PAGE_CONF = {
    "screen_name": StepName.INVESTMENT_DETAILS,
    "label": "Investment Details",
    "allowMultipleSection": False,
    "sections": [
    ]
}
COMPANY_DETAIL_SECTION = {
    "heading": "Company Details",
    "subHeading": "",
    "components": [
        {
            "componentType": "alpha_numeric",
            "componentId": "c87eed5d99c4431caea1623f05e03af8",
            "componentProperties": {
                "title1": {
                    "text": "Name of Organisation",
                    "color": "#757779",
                },
                "preFillVal": "{{organisation_name}}",
                "apiKey": "organisation_name",
                "transformer": 'capitalize',
                "multiSelection": False,
                "validations": {
                    "required": True
                }
            }
        },
        {
            "componentType": "searchable_dropdown",
            "componentId": "ddd9b6476c9643aba2633dbe0b30bea9",
            "componentProperties": {
                "title1": {
                    "text": "Country",
                    "color": "#757779",

                },
                "apiKey": "country",
                "multiSelection": False,
                "list": [],
                "fetchOptions": {
                    "type": "api",
                    "endpoint": "{{base_url}}/investor/kyc/field/country/options/?step={{step}}",
                },
                "validations": {
                    "required": True
                }
            }
        },
        {
            "componentType": "searchable_dropdown",
            "componentId": "7fad9555870f477f9ad672e3ae7f902a",
            "dependentOn": 'ddd9b6476c9643aba2633dbe0b30bea9',
            "componentProperties": {
                "title1": {
                    "text": "State",
                    "color": "#757779",
                },
                "apiKey": "state",
                "multiSelection": False,
                "list": [],
                "fetchOptions": {
                    "type": "api",
                    "endpoint": "{{base_url}}/investor/kyc/field/state/options/?step={{step}}",
                },
                "validations": {
                    "required": True
                }
            }
        },
        {
            "componentType": "searchable_dropdown",
            "componentId": "ebae9e61a55843b1811423fa8e0970cd",
            "dependentOn": '7fad9555870f477f9ad672e3ae7f902a',
            "componentProperties": {
                "title1": {
                    "text": "City",
                    "color": "#757779",

                },
                "apiKey": "city",
                "multiSelection": False,
                "list": [],
                "fetchOptions": {
                    "type": "api",
                    "endpoint": "{{base_url}}/investor/kyc/field/city/options/?step={{step}}",
                },
                "validations": {
                    "required": True
                }
            }
        },
        {
            "componentType": "numeric",
            "componentId": "6e5cfc8acbbb4ce49d55ed22b50dddcf",
            "componentProperties": {
                "title1": {
                    "text": "Pincode",
                    "color": "#757779",

                },
                "apiKey": "pinCode",
                "preFillVal": "{{pinCode}}",
                "validations": {
                    "required": True,
                    "min_characters": 5,
                    "max_characters": 6,
                }
            }
        },
        {
            "componentType": "alpha_numeric",
            "componentId": "8808f355c2844a4caafe2229909ec2bb",
            "componentProperties": {
                "title1": {
                    "text": "Company Address",
                    "color": "#757779",
                },
                "apiKey": "address",
                "preFillVal": "{{address}}",
                "multiLine": True,
                "fluid": True,
                "validations": {
                    "required": True,
                    "min_characters": 2,
                    "max_characters": 100,
                    "regex": ""
                }
            }
        },
        {
            "componentType": "alpha_numeric",
            "componentId": "c87eed5d99c4431caea1623f05e03af8",
            "componentProperties": {
                "title1": {
                    "text": "Company Website Url",
                    "color": "#757779",
                },
                'preFillVal': '{{company_url}}',
                "apiKey": "company_url",
                "multiSelection": False,
                "validations": {
                    "required": True
                }
            }
        },
        {
            "componentType": "dropdown",
            "componentId": "8b667fe1f135406ab35968d32e6517ab",
            "componentProperties": {
                "title1": {
                    "text": "Registered with",
                    "color": "#757779",

                },
                "apiKey": "registered_with",
                "multiSelection": False,
                "list": '{{resgistered_options}}',
                "validations": {
                    "required": True
                }
            }
        },
        {
            "componentType": "alpha_numeric",
            "componentId": "3a6qw944901a4324a9df808d3373db49",
            "componentProperties": {
                "title1": {
                    "text": "SEBI Resgisteration",
                    "color": "#757779",

                },
                "apiKey": "sebi_registeration",
                "preFillVal": "{{sebi_registeration}}",
                "transformer": 'uppercase',
                "validations": {
                    "required": True,
                }
            }
        },
        {
            "componentType": "alpha_numeric",
            "componentId": "3a6b9449011a4324a9df808d3373db49",
            "componentProperties": {
                "title1": {
                    "text": "Pan Number",
                    "color": "#757779",

                },
                "apiKey": "pan_number",
                "preFillVal": "{{pan_number}}",
                "transformer": 'uppercase',
                "validations": {
                    "required": True,
                    "min_characters": 9,
                    "max_characters": 10,
                    "regex": "[A-Z]{5}[0-9]{4}[A-Z]{1}$"
                }
            }
        },
        {
            "componentType": "doc_upload",
            "componentId": "0f921d43b43347d0b89903308980a3b9",
            "componentProperties": {
                "title1": {
                    "text": "Pan card",
                    "color": "#757779",

                },
                "preFillVal": "{{upload_pan_url}}",
                "apiKey": "upload_pan",
                "api": {
                    "endpoint": "{{base_url}}/investor/kyc/document/?step={{step}}",
                },
                "validations": {
                    "required": False
                }
            }
        },
    ],
    "submit": {
        "text": "Save",
        "endpoint": "{{base_url}}/investor/kyc/user/?step={{step}}",
        "body": {
            "step": "{{step}}"
        }
    }
}
COMPANY_DETAIL_PAGE_CONF = {
    "screen_name": StepName.COMPANY_DETAILS,
    "label": "Company Details",
    "allowMultipleSection": False,
    "sections": [
    ]
}

USER_DESCRIPTION_PAGE_CONF = {
    "screen_name": StepName.SOCIAL_INFORMATION,
    "label": "Description",
    "allowMultipleSection": False,
    "sections": [
    ]
}

USER_DESCRIPTION_SECTION = {
    "heading": "Social Details",
    "subHeading": "",
    "components": [
        # {
        #     "componentType": "alpha_numeric",
        #     "componentId": "c87ued5d99c4431caea1623f05e03af8",
        #     "componentProperties": {
        #         "title1": {
        #             "text": "Tell us about yourself",
        #             "color": "#757779",
        #         },
        #         "preFillVal": "{{short_description}}",
        #         "apiKey": "short_description",
        #         "validations": {
        #             "required": True
        #         }
        #     }
        # },
        # {
        #     "componentType": "alpha_numeric",
        #     "componentId": "3a6qq944901a4324a9df808d3373db49",
        #     "componentProperties": {
        #         "title1": {
        #             "text": "Describe yourself (in 300 words)",
        #             "color": "#757779",
        #
        #         },
        #         "apiKey": "description",
        #         "preFillVal": "{{description}}",
        #         "validations": {
        #             "required": True,
        #         }
        #     }
        # },
        {
            "componentType": "radio",
            "componentId": "0b667fe1f135406ab35968d32e6517ab",
            "componentProperties": {
                "title1": {
                    "text": "Are you a Fin Influencer ?",
                    "color": "#757779",

                },
                "apiKey": "is_fin_influencer",
                "multiSelection": False,
                "autoSave": True,
                "list": '{{is_fin_influencer_choices}}',
                "validations": {
                    "required": True
                }
            }
        },
        {
            "componentType": "alpha_numeric",
            "componentId": "6680eb66ae7843899aff45a59618de5a",
            "componentProperties": {
                "title1": {
                    "text": "LinkedIn Url",
                    "color": "#757779",

                },
                "apiKey": "linkedIn_handle",
                "preFillVal": "{{linkedIn_handle}}",
                "validations": {
                    "required": True,
                }
            }
        },
        {
            "componentType": "alpha_numeric",
            "componentId": "b190266b43ac4078a61ea9a890d98afd",
            "componentProperties": {
                "title1": {
                    "text": "Twitter Url",
                    "color": "#757779",

                },
                "apiKey": "twitter_handler",
                "preFillVal": "{{twitter_handler}}",
                "validations": {
                    "required": True,
                }
            }
        },
        {
            "componentType": "alpha_numeric",
            "componentId": "bbee2f4ecf9f4af1907b0e6852a9ba46",
            "componentProperties": {
                "title1": {
                    "text": "Youtube Url",
                    "color": "#757779",

                },
                "apiKey": "youtube_handle",
                "preFillVal": "{{youtube_handle}}",
                "validations": {
                    "required": True,
                }
            }
        },
        {
            "componentType": "alpha_numeric",
            "componentId": "13aef8654d1b4cdda082e1daa841f062",
            "componentProperties": {
                "title1": {
                    "text": "Instagram Url",
                    "color": "#757779",

                },
                "apiKey": "instagram_handle",
                "preFillVal": "{{instagram_handle}}",
                "validations": {
                    "required": True,
                }
            }
        },
        {
            "componentType": "alpha_numeric",
            "componentId": "41efeb94b5cf495db3a026737a9625c7",
            "componentProperties": {
                "title1": {
                    "text": "Telegram Url",
                    "color": "#757779",

                },
                "apiKey": "telegram_handle",
                "preFillVal": "{{telegram_handle}}",
                "validations": {
                    "required": False,
                }
            }
        },
        {
            "componentType": "alpha_numeric",
            "componentId": "3bcd491b42864409a05adb2d8de410c4",
            "componentProperties": {
                "title1": {
                    "text": "DailyHunt Url",
                    "color": "#757779",

                },
                "apiKey": "daily_hunt_handle",
                "preFillVal": "{{telegram}}",
                "validations": {
                    "required": False,
                }
            }
        },
        {
            "componentType": "alpha_numeric",
            "componentId": "8b85d5f05cbc402a8ecb0d9173c8295b",
            "componentProperties": {
                "title1": {
                    "text": "Pinterest",
                    "color": "#757779",

                },
                "apiKey": "pinterest_handle",
                "preFillVal": "{{pinterest_handle}}",
                "validations": {
                    "required": True,
                }
            }
        },
        {
            "componentType": "alpha_numeric",
            "componentId": "d9cf0af0b6ee4d3b845c32c33b46a6fe",
            "componentProperties": {
                "title1": {
                    "text": "Quora Handle",
                    "color": "#757779",

                },
                "apiKey": "quora_handle",
                "preFillVal": "{{quora_handle}}",
                "validations": {
                    "required": True,
                }
            }
        },
        {
            "componentType": "alpha_numeric",
            "componentId": "4c5514599fa24715bd5884692dff7792",
            "componentProperties": {
                "title1": {
                    "text": "Chinagri Url",
                    "color": "#757779",

                },
                "apiKey": "chingari_handle",
                "preFillVal": "{{chingari_handle}}",
                "validations": {
                    "required": True,
                }
            }
        },
        {
            "componentType": "alpha_numeric",
            "componentId": "090d2dd67ade4206b8bd662e2661b469",
            "componentProperties": {
                "title1": {
                    "text": "Moj Url",
                    "color": "#757779",

                },
                "apiKey": "moj_handle",
                "preFillVal": "{{moj_handle}}",
                "validations": {
                    "required": True,
                }
            }
        },
        {
            "componentType": "alpha_numeric",
            "componentId": "16dc14e2faa54048a50c6876a8404a1e",
            "componentProperties": {
                "title1": {
                    "text": "Josh Url",
                    "color": "#757779",

                },
                "apiKey": "josh_handle",
                "preFillVal": "{{josh_handle}}",
                "validations": {
                    "required": True,
                }
            }
        },

    ],
    "submit": {
        "text": "Save",
        "endpoint": "{{base_url}}/investor/kyc/user/?step={{step}}",
        "body": {
            "step": "{{step}}"
        }
    }
}

USER_ASSET_MANAGE_PAGE_CONF = {
    "screen_name": StepName.ASSET_MANAGEMENT,
    "label": "Asset Management",
    "allowMultipleSection": False,
    "sections": [
    ]
}

USER_ASSET_MANAGE_SECTION = {
    "heading": "Asset Management",
    "subHeading": "",
    "components": [
        {
            "componentType": "alpha_numeric",
            "componentId": "16dc14e2faa54048a50c6876a8404a1e",
            "componentProperties": {
                "title1": {
                    "text": "How many investors you are managing?",
                    "color": "#757779",

                },
                "apiKey": "num_of_investor",
                "preFillVal": "{{num_of_investor}}",
                "validations": {
                    "required": True,
                }
            }
        },
        {
            "componentType": "selectable_dropdown",
            "componentId": "a8bb79d5772c4079aaf08c55994d1810",
            "componentProperties": {
                "title1": {
                    "text": "Assets you are managing?",
                    "color": "#757779",

                },
                "apiKey": "asset_portfolio_managing",
                "multiSelection": False,
                "list": '{{asset_portfolio_options}}',
                "validations": {
                    "required": True
                }
            }
        },
    ],
    "submit": {
        "text": "Save",
        "endpoint": "{{base_url}}/investor/kyc/user/?step={{step}}",
        "body": {
            "step": "{{step}}"
        }
    }
}