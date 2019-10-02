import os.path
from common_config import TEMP_IMGS, IMGS_DATASET


Warning_msg = {
    "_name": "Warning_msg",
    "_parent":None,
    "_img_folder": os.path.join(IMGS_DATASET, 'Warning_msg'),
    "_dict_elements": {'btn_yes': '', 'btn_no': ''}
}

Russian_msg = {
    "_name": "Russian_msg",
    "_parent": None,
    "_img_folder":  os.path.join(IMGS_DATASET, 'Russian_msg'),
    "_dict_elements": {'btn_ok': ''}
}

Menu_Transaction_and_Services = {
    "_name": "Menu_Transaction_and_Services",
    "_parent": None,
    "_img_folder":  os.path.join(IMGS_DATASET, 'Menu_Transaction_and_Services'),
    "_dict_elements": {'transaction_and_services': '',
                       'collection_item_initiation': ''
                       }
}


Search_definition_dialog= {
    "_name": "Search_definition_dialog",
    "_parent": None,
    "_img_folder":  os.path.join(IMGS_DATASET, 'Search_definition_dialog'),
    "_dict_elements": {'run_search': ''}
}


Select_account_dialog= {
    "_name": "Select_account_dialog",
    "_parent": None,
    "_img_folder":  os.path.join(IMGS_DATASET, 'Select_account_dialog'),
    "_dict_elements": {'btn_ok': '', 'account_items': {}}
}


Collection_Item_Detail = {
    "_name": "Collection_Item_Detail",
    "_parent": None,
    "_img_folder": "{}{}".format(IMGS_DATASET, "Collection_Item_Detail"),
    "_dict_elements": { 'product': '', 'original_amount': '',
                        'type_collection_item': '', 'emission_date': '',
                        'customer_reference': '',
                        'due_date': '', 'collection_item_doc_type': '',
                        'allow_divergent': '', 'payer_name': '',
                        'payer_type': '', 'payer_address': '',
                        'payer_city': '', 'payer_state': '',
                        'payer_zipcode': '', 'btn_submit': ''
                       }
}






