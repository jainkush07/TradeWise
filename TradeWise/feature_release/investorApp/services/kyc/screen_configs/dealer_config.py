from investorApp.services.kyc.config import StepName

DEALER_DETAIL_PAGE_CONF = {
    "screen_name": StepName.DEALER_DETAILS,
    "label": "Dealer Network",
    "allowMultipleSection": False,
    "sections": [
    ]
}

DEALER_DETAIL_SECTION = {
    "heading": "Dealers Network",
    "subHeading": "",
    "components": [
        {
            "componentType": "dropdown",
            "componentId": "2b667fe1f135406ab35968d32e6517ab",
            "componentProperties": {
                "title1": {
                    "text": "Network you are a part of",
                    "color": "#757779",

                },
                "apiKey": "network",
                "multiSelection": False,
                "list": '{{dealer_network_options}}',
                "validations": {
                    "required": True
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

COMPANY_DETAIL_SECTION = {
    "heading": "Company Details",
    "subHeading": "",
    "components": [
        {
            "componentType": "dropdown",
            "componentId": "2b667fe1f135406ab35968d32e6517ab",
            "componentProperties": {
                "title1": {
                    "text": "Sign up as",
                    "color": "#757779",

                },
                "apiKey": "signed_as",
                "multiSelection": False,
                'autoSave': True,
                "list": '{{signed_as_options}}',
                "validations": {
                    "required": True
                }
            }
        },
        {
            "componentType": "selectable_accordian",
            "componentId": "a8bb79d5772c4079aaf08c55994d1810",
            "componentProperties": {
                "title1": {
                    "text": "Deals in",
                    "color": "#757779"
                },
                "apiKey": "company_sector_dict",
                "multiSelection": True,
                "fluid": True,
                "list": "{{company_sector_accordian_options}}",
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
                "fluid": True,
                "multiLine": True,
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
        # {
        #     "componentType": "dropdown",
        #     "componentId": "8b667fe1f135406ab35968d32e6517ab",
        #     "componentProperties": {
        #         "title1": {
        #             "text": "Registered with",
        #             "color": "#757779",
        #
        #         },
        #         "apiKey": "registered_with",
        #         "multiSelection": False,
        #         "list": '{{resgistered_options}}',
        #         "validations": {
        #             "required": True
        #         }
        #     }
        # },
        # {
        #     "componentType": "alpha_numeric",
        #     "componentId": "3a6qw944901a4324a9df808d3373db49",
        #     "componentProperties": {
        #         "title1": {
        #             "text": "SEBI Resgisteration",
        #             "color": "#757779",
        #
        #         },
        #         "apiKey": "sebi_registeration",
        #         "preFillVal": "{{sebi_registeration}}",
        #         "transformer": 'uppercase',
        #         "validations": {
        #             "required": True,
        #         }
        #     }
        # },

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
COMPANY_GST_COMP = {
    "componentType": "radio",
    "componentId": "r8bb79d5772c4079aaf08c55994d1810",
    "componentProperties": {
        "title1": {
            "text": "GST",
            "color": "#757779",

        },
        "apiKey": "gst_applicable",
        "multiSelection": False,
        "autoSave": True,
        "list": '{{gst_options}}',
        "validations": {
            "required": True
        }
    }
}
COMPANY_GST_COMPONENTS = [
    {
        "componentType": "alpha_numeric",
        "componentId": "d87eed5d99c4431caea1623f05e03af8",
        "componentProperties": {
            "title1": {
                "text": "Gst Number",
                "color": "#757779",
            },
            "preFillVal": "{{gst_number}}",
            "apiKey": "gst_number",
            "validations": {
                "required": True
            }
        }
    },
    {
        "componentType": "doc_upload",
        "componentId": "5a6a1596c9c94b7fab0f3878a0ef7a32",
        "componentProperties": {
            "title1": {
                "text": "GST",
                "color": "#757779",

            },
            "preFillVal": "{{gst_proof_url}}",
            "apiKey": "gst_proof",
            "api": {
                "endpoint": "{{base_url}}/investor/kyc/document/?step={{step}}",
            },
            "validations": {
                "required": False
            }
        }
    }
]
INFLUENCER_CONFIG = {
    "componentType": "dropdown",
    "componentId": "0b667fe1f135406ab35968d36517ab",
    "componentProperties": {
        "title1": {
            "text": "",
            "color": "#757779",

        },
        "apiKey": "influencer",
        "multiSelection": False,
        "list": '{{influencer_choices}}',
        "validations": {
            "required": True
        }
    }
}
CP_PAGE_CONF = {
    "screen_name": StepName.PARTNER_AGREEMENT,
    "label": "Kyc Agreement",
    "allowMultipleSection": False,
    "sections": [
    ]
}

CP_SECTION = {
    "heading": "Kyc Agreement",
    "subHeading": "",
    "components": [
        {
            "componentType": "agreement",
            "componentId": "y87rd5d99c4431caea1623f05e03af8",
            "componentProperties": {
                "title1": {
                    "text": "Agreement",
                    "color": "#757779",

                },
                "config": {
                    "html": '{{agreement_html}}',
                    "consent_text": "I have read and agree to above condition",
                    "value": "Yes",
                    "agreement_url": "{{agreement_url}}"
                },
                "apiKey": "consent",
                "autoSave": True,
                "preFillVal": "{{consent}}",
                "multiSelection": False,
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
AGREEMENT_SUN_COMPONENTS = [
    {
        "componentType": "alpha_numeric",
        "componentId": "y87eed5d99c4431caea1623f05e03af8",
        "componentProperties": {
            "title1": {
                "text": "Name",
                "color": "#757779",
            },
            "preFillVal": "{{agreement_signer}}",
            "apiKey": "agreement_signer",
            "transformer": 'capitalize',
            "multiSelection": False,
            "validations": {
                "required": True
            }
        }
    },
    {
        "componentType": "alpha_numeric",
        "componentId": "r87eed5d99c4431caea1623f05e03af8",
        "componentProperties": {
            "title1": {
                "text": "Place",
                "color": "#757779",
            },
            "preFillVal": "{{agreement_place}}",
            "apiKey": "agreement_place",
            "transformer": 'capitalize',
            "multiSelection": False,
            "validations": {
                "required": True
            }
        }
    },
    {
        "componentType": "doc_upload",
        "componentId": "5c4a1596c9c94b7fab0f3878a0ef7a32",
        "componentProperties": {
            "title1": {
                "text": "Upload Your Signature here",
                "color": "#757779",

            },
            "preFillVal": "{{signature_url}}",
            "apiKey": "signature",
            "api": {
                "endpoint": "{{base_url}}/investor/kyc/document/?step={{step}}",
            },
            "validations": {
                "required": False
            }
        }
    }
]
DEALS_IN_ACCORDIAN_CONFIG = {
    "componentType": "accordian",
    "componentId": "ch_ac_component_{{sector}}",
    "componentProperties": {
        "isSelected": False,
        "title1": {
            "text": "{{sector_name}}",
            "color": "#757779"
        },
        "apiKey": "{{sector}}",
        "list": [
            {
                "componentType": "alpha_numeric",
                "componentId": "ch_ac_sub_license_number_{{sector}}",
                "componentProperties": {
                    "title1": {
                        "text": "License Number",
                        "color": "#757779"
                    },
                    "preFillVal": "{{license_number}}",
                    "transformer": 'uppercase',
                    "apiKey": "license_number",
                    "multiSelection": False,
                    "validations": {
                        "required": True
                    }
                }
            },
            {
                "componentType": "doc_upload",
                "componentId": "ch_ac_sub_license_proof_{{sector}}",
                "componentProperties": {
                    "title1": {
                        "text": "License proof",
                        "color": "#757779"
                    },
                    "preFillVal": "{{license_proof_url}}",
                    "apiKey": "license_proof__{{sector}}",
                    "api": {
                        "endpoint": "{{base_url}}/investor/kyc/document/?step={{step}}"
                    },
                    "validations": {
                        "required": False
                    }
                }
            }
        ],
        "validations": {
            "required": True
        }
    }
}