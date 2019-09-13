from common_config import *
import os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

LOGGER_NAME = "B4nk_Sr4py"
LOG_FILE = os.path.join(ROOT_DIR, "logger{}{}".format(os.path.sep, LOGGER_NAME))
# SETTINGS = os.path.join(ROOT_DIR, 'settings')
# JSONES = os.path.join(SETTINGS, 'json_banks')
#
# SRC = os.path.join(ROOT_DIR, 'src')
# CONTROLLERS = os.path.join(SRC, 'controllers')

# selenium stuff
SELENIUM_DRIVER_PATH = os.path.join(ROOT_DIR, '{}{}{}'.format('chromedriver_win32', os.path.sep, 'chromedriver.exe'))

bancos = ['citibank']
from  src.controllers.bank_controller import BankController

bc = BankController({'banknames': bancos})
for b in bancos:
    bc.extract_movements(b)