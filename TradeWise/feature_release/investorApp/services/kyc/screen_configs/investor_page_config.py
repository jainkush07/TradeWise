from investorApp.services.kyc.config import StepName

# component id should b unique
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
                "transformer": 'capitalize',  # "uppercase" | "capitalize" | "lowecase";
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
                "autoSave": True,
                "preFillVal": "{{is_default}}",
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
                    "text": "Ifsc",
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
                "api": {
                    "endpoint": "{{base_url}}/investor/kyc/document/?step={{step}}",
                    "body": {
                        "pk": "{{pk}}"
                    },
                    "param_required": True
                },
                "refresh": True,
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
    "label": "DMAT Details",
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
                "autoSave": True,
                "preFillVal": "{{is_default}}",
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
                    "text": "DMAT Client Master Report",
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
                "preFillVal": "{{dpID}}",
                "transformer": 'uppercase',
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
