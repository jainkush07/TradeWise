from investorApp.services.kyc.config import StepName

PERSONAL_DETAIL_SECTION = {
    "heading": "Fund Manager Details",
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
                    "text": "Role (CEO, Vice President, etc.)",
                    "color": "#757779",

                },
                "apiKey": "role_in_company",
                "preFillVal": "{{role_in_company}}",
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

COMPANY_STAGE_SUB_COMPONENT = {
    "componentType": "dropdown",
    "componentId": "0fef59154f8840e3acbd3a3af3b0be7c",
    "componentProperties": {
        "title1": {
            "text": "Looking for Private Companies",
            "color": "#757779",

        },
        "apiKey": "companyStage",
        "multiSelection": True,
        "list": '{{company_stage_options}}',
        "validations": {
            "required": True
        }
    }
}

INVESTMENT_DETAIL_SECTION = {
    "heading": "Investment Details",
    "subHeading": "",
    "components": [
        {
            "componentType": "selectable_dropdown",
            "componentId": "t496f518c6224c0d95d0952f7379bbdd",
            "componentProperties": {
                "title1": {
                    "text": "Major Sector",
                    "color": "#757779",

                },
                "apiKey": "sectorToInvest",
                "multiSelection": False,
                "list": '{{invest_sector_options}}',
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
                    "text": "Assets you are managing?",
                    "color": "#757779",

                },
                "apiKey": "assetPortfolioManaging",
                "multiSelection": False,
                "list": '{{asset_portfolio_options}}',
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
                "autoSave": True,
                "fluid": True,
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
