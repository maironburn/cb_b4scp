citibank = {

# @todo ,  to think about (key adicional para invocar un callback o metodo ?... )

'img_recognition_workflow': [
        {'warning_msg': [
            {'target': 'btn_yes', 'action': "click"}]
        },

        {'russian_msg': [
            {'target': 'btn_ok', 'action': "click"}]
        },

        {'Menu_Transaction_and_Services': [
            {'target': '', 'action': "click"},

            {'target': 'btn_ok', 'action': "click"}
        ]
        },
        {'search_definition_dialog': [
            {'target': '', 'action': "click"},

            {'target': 'btn_ok', 'action': "click"}
        ]
        }
    ]
    ,

    'img_recognition_loop_workflow': [
        {'select_account_dialog': [
            {'target': '', 'action': "click"},

            {'target': 'btn_ok', 'action': "click"}
        ]
        },
        {'collection_item_detail': [
            # @todo, asociar a cada item una variable para setear un sleep ???
            {'target': 'product', 'action': "click"},
            {'target': 'combo_product', 'action': "click"},

            {'target': 'original_amount', 'action': "fill", 'data': ''},

            {'target': 'type_collection_item', 'action': "click"},
            {'target': 'combo_type_collection_item', 'action': "click"},

            {'target': 'combo_type_collection_item', 'action': "click"},

            {'target': 'emission_date', 'action': "fill", 'data': ''},

            {'target': 'customer_reference', 'action': "fill", 'data': ''},

            {'target': 'due_date', 'action': "fill", 'data': ''},

            {'target': 'collection_item_doc_type', 'action': "click"},
            {'target': 'combo_collection_item_doc_type', 'action': "click"},

            {'target': 'allow_divergent', 'action': "click"},
            {'target': 'combo_allow_divergent', 'action': "click"},

            {'target': 'payer_name', 'action': "fill", 'data': ''},

            {'target': 'payer_type', 'action': "click"},
            {'target': 'combo_payer_type', 'action': "click"},
            # @todo, esto puede ser bte jodido
            {'target': 'payer_type_txtbox', 'action': "fill", 'data': ''},

            {'target': 'payer_name', 'action': "fill", 'data': ''},

            {'target': 'payer_address', 'action': "fill", 'data': ''},

            {'target': 'payer_city', 'action': "fill", 'data': ''},

            {'target': 'payer_state', 'action': "fill", 'data': ''},

            {'target': 'payer_zipcode', 'action': "fill", 'data': ''},

            {'target': 'Collection_Item_Detail_btn_submit', 'action': "click"}
        ]
        }
    ]
}