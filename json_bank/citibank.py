citibank = {

    'bankname': 'citibank',  # redireccion al banco de santander,
    'browser_driver': 'iexplorer',
    # por si se requiere construir url a partir de otros params o url relativas
    'url_base': 'https://portal.citidirect.com/portalservices/forms/login.pser?',
    'headless': False,  # @todo

    # url de para el login
    'login_url': 'https://portal.citidirect.com/portalservices/forms/login.pser?',
    # 'login_url' : 'https://empresas.bankinter.com/www/es-es/cgi/empresas+cuentas+integral',
    # metodo de logado (standar, reconocimiento de imgs...whatever)
    'login_method': 'multifactor_login',

    # periodicidad de las consultas ( @TBD )
    'checking_time': '',

    # elemento sobre el q interactuar / condicion posterior de espera para continuar el wf
    # @todo ,  to think about (key adicional para invocar un callback o metodo ?... )
    'selenium_workflow': [
        {'tipo': 'xpath', 'target': "//a[@id='uifw-megamenu-8100']",
         'mode': 'click', 'description': 'Click sobre item menu citiDirect Services'},

        {'tipo': 'xpath', 'target': "//a[@class='ctTxGrBoldUnd']",
         'mode': 'click', 'description': 'Click(Cuentas a la vista)'},

        # FILTRADO de FECHAS ---->  DESDE
        {'tipo': 'xpath', 'target': "//input[@id='dia']",
         'mode': 'fill', 'description': 'Filtrado de fechas -> Desde (dia)', 'data': '01'},

        {'tipo': 'xpath', 'target': "//input[@id='mes']",
         'mode': 'fill', 'description': 'Filtrado de fechas -> Desde (mes)', 'data': '07'},

        {'tipo': 'xpath', 'target': "//input[@id='year']",
         'mode': 'fill', 'description': 'Filtrado de fechas -> Desde (year)', 'data': '2019'},

        # FILTRADO de FECHAS ---->  HASTA

        {'tipo': 'xpath', 'target': "//input[@id='diaH']",
         'mode': 'fill', 'description': 'Filtrado de fechas -> Hasta (dia)', 'data': '19'},

        {'tipo': 'xpath', 'target': "//input[@id='mesH']",
         'mode': 'fill', 'description': 'Filtrado de fechas -> Hasta (mes)', 'data': '07'},

        {'tipo': 'xpath', 'target': "//input[@id='yearH']",
         'mode': 'fill', 'description': 'Filtrado de fechas -> Hasta (year)', 'data': '2019'},

        # Boton de consultar
        {'tipo': 'xpath', 'target': "//button[@class='for_botonestandar_01']",
         'mode': 'click', 'description': 'Boton de consultar'},

        # Boton de Descargar
        {'tipo': 'xpath', 'target': "//a[@id='descarga']",
         'mode': 'click', 'description': 'Boton de consultar'}

    ],
    'img_recognition_workflow_ori': [

        {'tipo': 'xpath', 'target': "//input[@name='seuNumero']",
         'mode': 'fill', 'data': 'seaNumero', 'description': 'Seu numero'},

        {'tipo': 'xpath', 'target': "//input[@name='txtSacado']",
         'mode': 'fill', 'focus': True, 'data': '1234', 'description': 'CPF/CNPJ do  Sacado/Pagador'},

        {'tipo': 'xpath', 'target': "//input[@name='txtCedente']",
         'mode': 'fill', 'focus': True, 'data': '5678', 'description': 'CPF/CNPJ do Cedente/Beneficiario'},

        {'tipo': 'xpath', 'target': "//form[@name='form2']//input[@name='btnConfirmar']",
         'mode': 'click', 'description': 'boton OK'}
    ],

    'img_recognition_workflow': [ {'Collection_Item_Detail': [

        {'target': 'product', 'action': "click"},
        {'target': 'combo_product', 'action':  "click"},

        {'target': 'original_amount', 'action':  "fill" , 'data': ''},

        {'target': 'type_collection_item',  'action':  "click"},
        {'target': 'combo_type_collection_item', 'action':  "click"},

        {'target': 'combo_type_collection_item', 'action':  "click"},

        {'target': 'emission_date', 'action':  "fill" , 'data': ''},

        {'target': 'customer_reference', 'action': "fill", 'data': ''},

        {'target': 'due_date', 'action': "fill", 'data': ''},

        {'target': 'collection_item_doc_type',  'action':  "click"},
        {'target': 'combo_collection_item_doc_type',  'action':  "click"},

        {'target': 'allow_divergent',  'action':  "click"},
        {'target': 'combo_allow_divergent',  'action':  "click"},

        {'target': 'payer_name', 'action': "fill", 'data': ''},

        {'target': 'payer_type', 'action': "click"},
        {'target': 'combo_payer_type', 'action': "click"},
        #@todo, esto puede ser bte jodido
        {'target': 'payer_type_txtbox', 'action': "fill", 'data': ''},

        {'target': 'payer_name', 'action': "fill", 'data': ''},

        {'target': 'payer_address', 'action': "fill", 'data': ''},

        {'target': 'payer_city', 'action': "fill", 'data': ''},

        {'target': 'payer_state', 'action': "fill", 'data': ''},

        {'target': 'payer_zipcode', 'action': "fill", 'data': ''},

        {'target': 'Collection_Item_Detail_btn_submit', 'action': "click"},

        ]}
    ]

#end json
}
