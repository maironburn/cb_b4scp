from common_config import *
import os
import threading

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


bancos = ['citibank']
from  src.controllers.bank_controller import BankController
from  src.controllers.xls_controller import XlsController
from src.controllers.keep_me_foreground import KeepMeForeGround
from common_config import FOREGROUND_THREAD

if __name__ == '__main__':

    bancos = ['citibank']
    bc = BankController({'banknames': bancos})
    xls_controller= XlsController (**{'logger': bc.logger})
    # @todo, definir q hacer con los boletos q no pasen la validacion
    try:
        if xls_controller.get_boletos_items():
            if FOREGROUND_THREAD:
                pass
                #keep_me_foreground = KeepMeForeGround(logger=bc.logger)
                #daemon = threading.Thread(target=keep_me_foreground.daemon_dont_disturb_please).start()

            bc.start_party(bankname= 'citibank', lst_instances_bi=xls_controller.valid_instances_collection)
        else:
            print("Ocurrio un error en la lectura , no se encontraron documentos xlsx o los boletos no son validos")
            input()

    except Exception as e:
        print("Excepcion en el modulo principal: {}".format(e))
    import sys
    sys.exit()
    quit()