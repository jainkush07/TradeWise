from investorApp.services.kyc.config import StepName

ESOP_DETAIL_SECTION = {
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
            "componentType": "dropdown",
            "componentId": "9b667fe1f135406ab35968d32e6517ab",
            "componentProperties": {
                "title1": {
                    "text": "Is Shares Dematerialized",
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
            "componentType": "numeric",
            "componentId": "3a6qw944901a4324a9df808d3373db49",
            "componentProperties": {
                "title1": {
                    "text": "No. of Shares You have",
                    "color": "#757779",

                },
                "apiKey": "shares_owned",
                "preFillVal": "{{shares_owned}}",
                "validations": {
                    "required": True,
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
            "componentType": "dropdown",
            "componentId": "9b667fe2f13406ab35968d32e6517ab",
            "componentProperties": {
                "title1": {
                    "text": "ROFR Required",
                    "color": "#757779",

                },
                "apiKey": "rofr",
                "multiSelection": False,
                "list": '{{rofr_options}}',
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

VALUATION_SUB_COMPONENT = {
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
}

ESOP_DETAIL_PAGE_CONF = {
    "screen_name": StepName.ESOP_COMPANY_DETAILS,
    "label": "Company Details",
    "allowMultipleSection": False,
    "sections": [
    ]
}
