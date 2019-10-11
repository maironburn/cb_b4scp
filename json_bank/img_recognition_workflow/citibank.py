citibank = {

# @todo ,  to think about (key adicional para invocar un callback o metodo ?... )

'img_recognition_workflow_main': [
        {'warning_msg': [
            {'target': 'yes', 'action': "click"}]
        },

        {'russian_msg': [
            {'target': 'ok', 'action': "click"}]
        },
        {'main_transactions_and_services': [
            {'target': 'transactions_and_services', 'action': "click"}]
        },
        {'menu_transactions_and_services': [
            {'target': 'collection_item_initiation', 'action': "click"}
            ]
        }
    ]
    ,
    #
    'img_recognition_workflow_intermezzo': [
        {'loaded_transactions_and_services': [
            {'target': 'new', 'action': "click"}
                ]
        }
        ,
        {'search_definition_dialog': [
            {'target': 'run_search', 'action': "click"}
                ]
        }
        ,
        {'select_account_dialog': [
                    {'target': 'ok', 'action': "click"}
                ]
            }

        ]
    ,
    #loop para la generacion de boletos (depende de los datos particulares del boleto)
    #'img_recognition_loop_workflow': [
    'collection_item_detail': [
            # @todo, asociar a cada item una variable para setear un sleep ???
            {'target': 'product', 'action': "select", 'boleto_data': 'product'},

            {'target': 'original_amount', 'action': "fill", 'boleto_data': 'amount'},

            {'target': 'type_of_collection_item_code', 'action': "select", 'boleto_data': 'type_of_collection_item_code'},

            {'target': 'emission_date', 'action': "fill", 'boleto_data': 'emision_date'},

            {'target': 'customer_reference', 'action': "fill", 'boleto_data': 'boleto_number'},

            {'target': 'due_date', 'action': "fill", 'boleto_data': 'due_date'},

            {'target': 'collection_item_document_type', 'action': "select", 'boleto_data': 'collection_item_document_type' },

            {'target': 'allow_divergent', 'action': "select", 'boleto_data': 'allow_divergent'},

            {'target': 'payer_name', 'action': "fill", 'boleto_data': 'enteprise_id'},
            #todo, think about

            {'target': 'payer_type', 'action': "select", 'boleto_data': 'payer_type'},

            {'target': 'cpf', 'action': "fill", 'boleto_data': 'cpf'},
            # {'target': 'payer_type', 'action': "click"},
            # {'target': 'cmboption', 'action': "click"},
            # {'target': 'payer_type_txtbox', 'action': "fill",'boleto_data': 'cpf'},

            {'target': 'payer_address', 'action': "fill", 'boleto_data': 'address'},

            {'target': 'payer_state', 'action': "fill", 'boleto_data': 'state'},

            {'target': 'payer_city', 'action': "fill", 'boleto_data': 'city'},

            {'target': 'payer_zipcode', 'action': "fill", 'boleto_data': 'zip_code'},

            {'target': 'fake_submit', 'action': "click"},

            {'target': 'no', 'action': "submit"}
        ]
    ,
    'collection_item_detail_window_error': [
        # @todo, asociar a cada item una variable para setear un sleep ???
        {'target': 'ok', 'action': "click"},
        {'target': 'home', 'action': "click"}
        ]

}

