from investorApp.services.kyc.config import StepName

PERSONAL_DETAIL_SECTION = {
    "heading": "Personal Information",
    "subHeading": "",
    "components": [
        {
            "componentType": "alpha",
            "componentId": "a496f518c6224c0d95d0952f7379bbdd",
            "componentProperties": {
                "title1": {
                    "text": "Contact Name",
                    "color": "#757779",

                },
                "apiKey": "name",
                "preFillVal": "{{name}}",
                "transformer": 'capitalize',  # "uppercase" | "capitalize" | "lowecase";
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
            "componentId": "b496f518c6224c0d95d0952f7379bbdd",
            "componentProperties": {
                "title1": {
                    "text": "Role (CEO, CFO, CA, CS, etc.)",
                    "color": "#757779",

                },
                "apiKey": "role_in_company",
                "preFillVal": "{{role_in_company}}",
                "transformer": 'uppercase',  # "uppercase" | "capitalize" | "lowecase";
                "validations": {
                    "required": True,
                    "min_characters": 2,
                    "max_characters": 50,
                    "regex": "^[a-zA-Z][a-z 'A-Z]{2,50}$"
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
        }
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
    "screen_name": StepName.INS_PERSONAL_DETAILS,
    "label": "Personal Details",
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
            "componentType": "numeric",
            "componentId": "dc4731dcb4074755b91378dd4d441f34",
            "componentProperties": {
                "title1": {
                    "text": "Annual Turnover (in Cr.)",
                    "color": "#757779",

                },
                "apiKey": "annual_turnover",
                "preFillVal": "{{annual_turnover}}",
                "validations": {
                    "required": True,
                }
            }
        },
        {
            "componentType": "numeric",
            "componentId": "00f1dea103ef475bab3ffb935cf07253",
            "componentProperties": {
                "title1": {
                    "text": "No. of Employees",
                    "color": "#757779",

                },
                "apiKey": "employees",
                "preFillVal": "{{employees}}",
                "validations": {
                    "required": True,
                }
            }
        },
        {
            "componentType": "alpha_numeric",
            "componentId": "68cc322b3bc74faf99f38109bebbba1e",
            "componentProperties": {
                "title1": {
                    "text": "Sector",
                    "color": "#757779",
                },
                "preFillVal": "{{sector}}",
                "apiKey": "sector",
                "transformer": 'capitalize',
                "multiSelection": False,
                "validations": {
                    "required": True
                }
            }
        },
        {
            "componentType": "numeric",
            "componentId": "c736fe9f561b4ca1a2698b998b64bf35",
            "componentProperties": {
                "title1": {
                    "text": "Revenue Growth (in Cr.)",
                    "color": "#757779",

                },
                "apiKey": "revenue_growth",
                "preFillVal": "{{revenue_growth}}",
                "validations": {
                    "required": False,
                }
            }
        },
        {
            "componentType": "numeric",
            "componentId": "d116ffff9fc34cb3864812c824057ada",
            "componentProperties": {
                "title1": {
                    "text": "Profit Growth (in Cr.)",
                    "color": "#757779",

                },
                "apiKey": "profit_growth",
                "preFillVal": "{{profit_growth}}",
                "validations": {
                    "required": False,
                }
            }
        },
        {
            "componentType": "dropdown",
            "componentId": "9b667fe1f13406ab35968d32e6517ab",
            "componentProperties": {
                "title1": {
                    "text": "Last Valuation of Company",
                    "color": "#757779",

                },
                "autoSave": True,
                "apiKey": "valuation_status",
                "multiSelection": False,
                "list": '{{valuation_status_options}}',
                "validations": {
                    "required": True
                }
            }
        },
        {
            "componentType": "numeric",
            "componentId": "3a6qw944901a4324a9df808d3373db49",
            "componentProperties": {
                "title1": {
                    "text": "Last evaluation (in Cr.)",
                    "color": "#757779",

                },
                "apiKey": "valuation",
                "preFillVal": "{{valuation}}",
                "validations": {
                    "required": False,
                }
            }
        },
        {
            "componentType": "dropdown",
            "componentId": "9b667fe1f135406ab35968d32e6517ab",
            "componentProperties": {
                "title1": {
                    "text": "Shares Dematerialized",
                    "color": "#757779",

                },
                "apiKey": "share_dematerialized",
                "multiSelection": False,
                "list": '{{share_dematerial_options}}',
                "validations": {
                    "required": True
                }
            }
        },
        {
            "componentType": "doc_upload",
            "componentId": "bd829e2dea8141628a1f8568f862a046",
            "componentProperties": {
                "title1": {
                    "text": "Pitch Deck",
                    "color": "#757779",

                },
                "preFillVal": "{{pitch_deck_url}}",
                "apiKey": "pitch_deck",
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

COMPANY_FINANCIAL_UPLOAD_COMPONENT = {
    "componentType": "multi_doc_upload",
    "componentId": "5a6a05969c94b7fab0f3878a0ef7a32",
    "componentProperties": {
        "title1": {
            "text": "Annual Financials",
            "color": "#757779"
        },
        "list": [],
        "config": {
            "text": "Add More",
            "api": {
                "endpoint": "{{base_url}}/investor/kyc/user/?step=COMPANY_FINANCIALS",
                "data": {
                    "annual_financial_doc": "add_new"
                }
            }
        },
        "validations": {
            "required": False
        }
    }
}

COMPANY_FINANCIAL_UPLOAD_SUB_COMPONENT = {
    "preFillVal": "{{financial_report_url}}",
    "apiKey": "financial_report__{{financial_year}}",
    "placeholder": "FY {{financial_year}}",
    "api": {
        "endpoint": "{{base_url}}/investor/kyc/document/?step=COMPANY_FINANCIALS"
    }
}
