from investorApp.services.kyc.config import StepName
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