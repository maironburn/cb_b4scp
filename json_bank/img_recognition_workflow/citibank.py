citibank = {

# @todo ,  to think about (key adicional para invocar un callback o metodo ?... )

'img_recognition_workflow': [
        {'warning_msg': [
            {'target': 'yes', 'action': "click"}]
        },

        {'russian_msg': [
            {'target': 'ok', 'action': "click"}]
        },

        {'Menu_Transaction_and_Services': [
            {'target': 'transactions_and_services', 'action': "click"},

            {'target': 'collection_item_initiation', 'action': "click"},
            #todo
            {'target': 'new', 'action': "click"}

        ]
        },
        {'search_definition_dialog': [
            {'target': 'run_search', 'action': "click"}
        ]
        }
    ]
    ,

    'img_recognition_loop_workflow': [
        {'select_account_dialog': [
            {'target': '', 'action': "click"},

            {'target': 'ok', 'action': "click"}
        ]
        },
        {'collection_item_detail': [
            # @todo, asociar a cada item una variable para setear un sleep ???
            {'target': 'product', 'action': "click"},
            {'target': 'cmboption', 'action': "click"},

            {'target': 'original_amount', 'action': "fill", 'data': ''},

            {'target': 'type_of_collection_item_code', 'action': "click"},
            {'target': 'cmboption', 'action': "click"},

            {'target': 'emission_date', 'action': "fill", 'data': ''},

            {'target': 'customer_reference', 'action': "fill", 'data': ''},

            {'target': 'due_date', 'action': "fill", 'data': ''},

            {'target': 'collection_item_document_type', 'action': "click"},
            {'target': 'cmboption', 'action': "click"},

            {'target': 'allow_divergent', 'action': "click"},
            {'target': 'cmboption', 'action': "click"},

            {'target': 'payer_name', 'action': "fill", 'data': ''},

            {'target': 'payer_type', 'action': "click"},
            {'target': 'cmboption', 'action': "click"},
            {'target': 'payer_type_txtbox', 'action': "fill", 'data': ''},

            {'target': 'payer_address', 'action': "fill", 'data': ''},

            {'target': 'payer_city', 'action': "fill", 'data': ''},

            {'target': 'payer_state', 'action': "fill", 'data': ''},

            {'target': 'payer_zipcode', 'action': "fill", 'data': ''},

            {'target': 'submit', 'action': "click"}
        ]
        }
    ]
}