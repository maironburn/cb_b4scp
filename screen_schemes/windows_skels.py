import os.path
from common_config import TEMP_IMGS, IMGS_DATASET

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

warning_msg = {
    "_name": "warning_msg",
    "_parent":None,
    "_img_folder": os.path.join(IMGS_DATASET, 'Warning_msg'),
    "_dict_elements": {'btn_yes': '', 'btn_no': ''}
}

Russian_msg = {
    "_name": "Russian_msg",
    "_parent": None,
    "_img_folder":  os.path.join(IMGS_DATASET, 'Russian_msg')
    "_dict_elements": {'btn_ok': ''}
}

popscreen_add_telf = {
    "_name": "popscreen_add_telf",
    "_parent": "nuevo_declarante",
    "_img_folder": "{}{}{}{}{}".format(nuevo_declarante['_img_folder'], os.path.sep, 'telf_email', os.path.sep,
                                       'popscreen_add_telf'),
    "_dict_elements": {}
}

popscreen_add_domicilio = {
    "_name": "popscreen_add_domicilio",
    "_parent": "nuevo_declarante",
    "_img_folder": "{}{}{}{}{}".format(nuevo_declarante['_img_folder'], os.path.sep, 'domicilio', os.path.sep,
                                       'popscreen_add_domicilio'),
    "_dict_elements": {}
}

