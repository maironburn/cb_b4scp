import os.path

from common_config import IMGS_DATASET, TEMPLATES_IMGS

warning_msg = {
    "_name": "warning_msg",
    "_parent": None,
    "_template": os.path.join(TEMPLATES_IMGS, 'warning_msg_passby.png'),
    "_img_folder": os.path.join(IMGS_DATASET, 'warning_msg'),
    "_dict_elements": {'yes': ''}
}

russian_msg = {
    "_name": "russian_msg",
    "_parent": None,
    "_template": os.path.join(TEMPLATES_IMGS, 'russian_msg.png'),
    "_img_folder": os.path.join(IMGS_DATASET, 'russian_msg'),
    "_dict_elements": {'ok': ''}
}

main_transactions_and_services = {
    "_name": "main_transactions_and_services",
    "_parent": None,
    "_template": os.path.join(TEMPLATES_IMGS, 'main_transactions_and_services.png'),
    "_img_folder": os.path.join(IMGS_DATASET, 'main_transactions_and_services'),
    "_dict_elements": {'transactions_and_services': ''}
}

menu_transactions_and_services = {
    "_name": "menu_transactions_and_services",
    "_parent": None,
    "_template": os.path.join(TEMPLATES_IMGS, 'menu_transactions_and_services.png'),
    "_img_folder": os.path.join(IMGS_DATASET, 'menu_transactions_and_services'),
    "_dict_elements": {'collection_item_initiation': ''}
}

loaded_transactions_and_services = {
    "_name": "loaded_transactions_and_services",
    "_parent": None,
    "_template": os.path.join(TEMPLATES_IMGS, 'loaded_transactions_and_services.png'),
    "_img_folder": os.path.join(IMGS_DATASET, 'loaded_transactions_and_services'),
    "_dict_elements": {'new': ''}
}

search_definition_dialog = {
    "_name": "search_definition_dialog",
    "_parent": None,
    "_template": os.path.join(TEMPLATES_IMGS, 'search_definition_dialog.png'),
    "_img_folder": os.path.join(IMGS_DATASET, 'search_definition_dialog'),
    "_dict_elements": {'run_search': ''}
}

select_account_dialog = {
    "_name": "select_account_dialog",
    "_parent": None,
    "_template": os.path.join(TEMPLATES_IMGS, 'select_account_dialog.png'),
    "_img_folder": os.path.join(IMGS_DATASET, 'select_account_dialog'),
    "_dict_elements": {'ok': ''}  # aqui tb irian las cuentas de los boletos (pero se simplifica updateando el dict
}

collection_item_detail = {
    "_name": "collection_item_detail",
    "_parent": None,  # submit o return to summary
    "_template": os.path.join(TEMPLATES_IMGS, 'collection_item_detail.png'),
    "_img_folder": os.path.join(IMGS_DATASET, "collection_item_detail"),
    "_dict_elements": {'product': '', 'original_amount': '',
                       'type_of_collection_item_code': '', 'emission_date': '',
                       'customer_reference': '',
                       'due_date': '', 'collection_item_document_type': '',
                       'allow_divergent': '', 'payer_name': '',
                       'payer_type': '', 'payer_type_txtbox': '',
                       'payer_address': '', 'payer_state': '',
                       'payer_city': '',
                       'payer_zipcode': '',
                       'submit': '',
                       'fake_submit': '',
                       'no': ''
                       ## add submit o return to summary
                       }
}

collection_item_detail_window_error = {
    "_name": "collection_item_detail_window_error",
    "_parent": None,
    "_template": os.path.join(TEMPLATES_IMGS, 'collection_item_detail_window_error.png'),
    "_img_folder": os.path.join(IMGS_DATASET, 'collection_item_detail_window_error'),
    "_dict_elements": {'ok': '',
                       'home': '',
                       'transactions_and_services' : '',
                       'collection_item_initiation' : ''
                       }  # aqui tb irian las cuentas de los boletos (pero se simplifica updateando el dict
}

