from common_config import *
import os

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
IE_DRIVER = os.path.join(IE_DRIVER_FOLDER, 'IEDriver.exe')
# XLS folder
XLS_FOLDER = os.path.join(ROOT_DIR, 'xls_folder')


bancos = ['citibank']
from  src.controllers.bank_controller import BankController
from  src.controllers.xls_controller import XlsController

if __name__ == '__main__':

    bancos = ['citibank']
    bc = BankController({'banknames': bancos})
    xls_controller= XlsController (**{'logger': bc.logger})
    # @todo, definir q hacer con los boletos q no pasen la validacion
    xls_controller.get_boletos_items()
    bc.generate_boleto(bankname= 'citibank', lst_instances_bi=xls_controller.valid_instances_collection)
