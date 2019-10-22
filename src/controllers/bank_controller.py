from logger.app_logger import AppLogger
from src.controllers.reboot_process import Reboot_Process
from src.controllers.selenium_controller import SeleniumController
from src.models.bank_basis import Bank


class BankController(object):
    _dict_bank = {}
    _banknames = []
    _sc = None  # selenium controller
    _logger = None
    _total_a_crear = 0
    _creados_ok = 0
    _errores_al_crear = 0
    _lst_correctos = []
    _lst_erroneos = []
    _reboot = None

    def __init__(self, kw):

        self._banknames = kw.get('banknames', None)
        self._logger = AppLogger.create_rotating_log()
        self._reboot = Reboot_Process({'logger': self._logger})

        if self._banknames:
            self.load_banks()

    def start_party(self, bankname=None, lst_instances_bi=None):

        kw = {'logger': self._logger, 'bank': self._dict_bank.get(bankname).json_data,
              'img_recon_workflow': self._dict_bank.get(bankname)._json_img_recognition
              }

        self.sc = SeleniumController(kw)

        if len(lst_instances_bi):
            self.total_a_crear = len(lst_instances_bi)
            print("\n\n\tFASE Automatismo Selenium \n*****************************************************")
            print("Num de boletos leidos del excel y pendientes de emitir: {}".format(len(lst_instances_bi)))
            print(
                "\n\n\tWorkflow no asociado a datos de boletos \n*****************************************************")

            while not self.sc.do_image_automation():
                self._reboot.restart_workflow()

            print(
                "\n\n\tWorkflow Loop \n*****************************************************")
            for bi in lst_instances_bi:
                while not self.sc.do_image_automation(json_workflow='img_recognition_workflow_intermezzo', boleto_instance=bi):
                    self._reboot.restart_workflow()
                    self.sc.do_image_automation()
                # ya wf dependiente de las instancias del boleto
                self.sc.boleto_wf_loop(bi)


    def load_banks(self):
        for bank in self.banknames:
            kw = {'logger': self._logger, 'name': bank}
            bank_instance = Bank(kw)
            self.add_bank(bank_instance)

    def add_bank(self, bank):
        if isinstance(bank, Bank) and bank.name not in self._dict_bank.keys():
            self._dict_bank.update({bank.name: bank})

    # <editor-fold desc="getters /setters">
    @property
    def banknames(self):
        return self._banknames

    @banknames.setter
    def banknames(self, value):
        if isinstance(value, list):
            self._banknames = value

    @property
    def dict_bank(self):
        return self._dict_bank

    @dict_bank.setter
    def dict_bank(self, value):
        if isinstance(value, dict):
            self._dict_bank = value

    @property
    def sc(self):
        return self._sc

    @sc.setter
    def sc(self, value):
        if value:
            self._sc = value

    @property
    def logger(self):
        return self._logger
    # </editor-fold>
