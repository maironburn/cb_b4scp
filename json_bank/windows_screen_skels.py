import os.path
from common_config import TEMP_IMGS, IMGS_DATASET


warning_msg = {
    "_name": "warning_msg",
    "_parent":None,
    "_img_folder": os.path.join(IMGS_DATASET, 'warning_msg'),
    "_dict_elements": {'yes': '', 'no': ''}
}

russian_msg = {
    "_name": "russian_msg",
    "_parent": None,
    "_img_folder":  os.path.join(IMGS_DATASET, 'russian_msg'),
    "_dict_elements": {'ok': ''}
}

menu_transaction_and_services = {
    "_name": "menu_transaction_and_services",
    "_parent": None,
    "_img_folder":  os.path.join(IMGS_DATASET, 'menu_transaction_and_services'),
    "_dict_elements": {'transactions_and_services': '',
                       'collection_item_initiation': '',
                       'new' : ''
                       }
}


search_definition_dialog= {
    "_name": "search_definition_dialog",
    "_parent": None,
    "_img_folder":  os.path.join(IMGS_DATASET, 'search_definition_dialog'),
    "_dict_elements": {'run_search': ''}
}


select_account_dialog= {
    "_name": "select_account_dialog",
    "_parent": None,
    "_img_folder":  os.path.join(IMGS_DATASET, 'select_account_dialog'),
    "_dict_elements": {'ok': '', 'account_items': {}}
}


collection_item_detail = {
    "_name": "collection_item_detail",
    "_parent": None, #submit o return to summary
    "_img_folder": os.path.join(IMGS_DATASET,  "collection_item_detail"),
    "_dict_elements": { 'product': '', 'original_amount': '',
                        'type_of_collection_item_code': '', 'emission_date': '',
                        'customer_reference': '',
                        'due_date': '', 'collection_item_document_type': '',
                        'allow_divergent': '', 'payer_name': '',
                        'payer_type': '', 'payer_address': '',
                        'payer_city': '', 'payer_state': '',
                        'payer_zipcode': '', 'submit': ''
                        ## add submit o return to summary
                       }
}






