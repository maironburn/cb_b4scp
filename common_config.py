# -*- coding: utf-8 -*-
import os.path

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

# logger stuff
LOGGER_NAME = "Citibank_Payment_RPA"
LOG_FILE = os.path.join(ROOT_DIR, "logger{}{}".format(os.path.sep, LOGGER_NAME))

# json bancos
JSON_BANK = os.path.join(ROOT_DIR, 'json_bank')
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
    'PID',
    'Endereço faturamento (Estate,Cep necesita 8 caracteres,City)',
    'Data de emision del boleto (según la configuracion del idioma)',
    'Data de Vencimento (según la configuracion del idioma)',
    'Total'
]



COLS_DICT_TO_ENTITY = {
    'Boleto (para algunos casos nueve digitos)': 'boleto_number',
    'Enterprise id/ Racao social': 'enteprise_id',
    'CPF(necesita 11 caracteres)/CNPJ(necesita 14 caracteres)': 'cpf',
    'PID': 'pid',
    'Endereço faturamento (Estate,Cep necesita 8 caracteres,City)': 'location_data',
    'Data de emision del boleto (según la configuracion del idioma)': 'emision_date',
    'Data de Vencimento (según la configuracion del idioma)': 'due_date',
    'Total': 'amount'
}

DICT_REGEX_BOLETO_ITEM = {'boleto_number': '^\d{5,9}$',
                          'enteprise_id': '\w+',
                          'cpf':  '^\d{9,15}$',
                          'pid': '^\d+$',
                          'cep': '^\d{7,9}$',
                          'due_date': '(\d{1,2}\/)*\d{4}$'
                          }


# keep_foregorund
APP_NAME = ""
TIME_SLEEP = 10

'''
login bello de reconocimiento de imagenes

# imagenes
IMG_DIRS = os.path.join(ROOT_DIR, 'img')
TEMP_IMGS = os.path.join(IMG_DIRS, 'temps_imgs')
DATASET_IMGS = os.path.join(IMG_DIRS, 'datasets')
# crypto
RSA_KEYS = os.path.join(ROOT_DIR, "crypto{}{}".format(os.path.sep, "rsa_keys"))
FICHERO_CREDENCIALES=os.path.join(SETTINGS, "credentials{}{}".format(os.path.sep, "credentials.py"))
'''

# Folder to store after generate public /private RSA keys
