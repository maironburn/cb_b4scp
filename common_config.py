# -*- coding: utf-8 -*-
import os.path

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
# logger stuff
LOGGER_NAME = "Citibank_Payment_RPA"
LOG_FILE = os.path.join(ROOT_DIR, "logger{}{}".format(os.path.sep, LOGGER_NAME))
COOKIE_FILE = os.path.join(ROOT_DIR, "cookie.pkl")
DOWNLOAD_FOLDER=os.path.join(ROOT_DIR, 'Boletos emitidos')
IMGS_FOLDER=  os.path.join(ROOT_DIR, 'images')

TEMPLATES_IMGS=  os.path.join(IMGS_FOLDER, 'templates')
TEMP_IMGS=  os.path.join(IMGS_FOLDER, 'temp')
IMGS_DATASET=  os.path.join(IMGS_FOLDER, 'dataset')
ERROR_IMGS=  os.path.join(IMGS_FOLDER, 'errores')
BOLETOS_PROCESADOS_IMGS=  os.path.join(IMGS_FOLDER, 'boletos procesados')

# json bancos
JSON_BANK = os.path.join(ROOT_DIR, 'json_bank')
IMG_RECON_WF = os.path.join(JSON_BANK, 'img_recognition_workflow')
SELENIUM_WF = os.path.join(JSON_BANK, 'selenium_workflow')

# Paquetes de terceros
EXT_BUNDLES = os.path.join(ROOT_DIR, '3rd_parties')
# selenium IE Driver
IE_DRIVER_FOLDER = os.path.join(EXT_BUNDLES, 'IEDriver')
IE_DRIVER = os.path.join(IE_DRIVER_FOLDER, 'IEDriverServer.exe')
# XLS folder
XLS_FOLDER = os.path.join(ROOT_DIR, 'xls_folder')
COLS_NAMES = [
    'Boleto (para algunos casos nueve digitos)',
    'Enterprise id/ Racao social',
    'CPF(necesita 11 caracteres)/CNPJ(necesita 14 caracteres)',
    'CNPJ Beneficiario',
    'Product',
    'Account Number',
    'Payer Address',
    'Payer State',
    'Payer City',
    'Payer Zip Code',
    'Data de emision del boleto (según la configuracion del idioma)',
    'Data de Vencimento (según la configuracion del idioma)',
    'Total'
]

COLS_DICT_TO_ENTITY = {
    'Boleto (para algunos casos nueve digitos)': 'boleto_number',
    'Enterprise id/ Racao social': 'enteprise_id',
    'CPF(necesita 11 caracteres)/CNPJ(necesita 14 caracteres)': 'cpf',
    'CNPJ Beneficiario' : 'cpnj_beneficiario',
    'Product' : 'product',
    'Account Number': 'account_number',
    'Payer Address': 'address',
    'Payer State': 'state',
    'Payer City': 'city',
    'Payer Zip Code': 'zip_code',
    'Data de emision del boleto (según la configuracion del idioma)': 'emision_date',
    'Data de Vencimento (según la configuracion del idioma)': 'due_date',
    'Total': 'amount'
}

DICT_REGEX_BOLETO_ITEM = {

    'account_number': '^\d+$',
    'boleto_number': '^\d{5,9}$',
    'enteprise_id': '\w+',
    'cpf': '^\d{11,14}$',
    'zip_code': '^\d{8}$',
    'emision_date' :  '(\d{1,2}\/)*\d{4}$',
    'due_date': '(\d{1,2}\/)*\d{4}$'
}



# keep_foregorund
APP_NAME = "CitiDirect® Online Banking - Internet Explorer"
FOREGROUND_THREAD = False
TIME_SLEEP = 1

# DICTIO_PAPAFRITA= {'main_transactions_and_services' : 'img_recognition_workflow_main',
#                     'menu_transactions_and_services': 'img_recognition_workflow_main',
#                     'loaded_transactions_and_services': 'img_recognition_workflow_intermezzo',
#                     'search_definition_dialog': 'img_recognition_workflow_intermezzo',
#                     'select_account_dialog' :'img_recognition_workflow_intermezzo'
#                    }