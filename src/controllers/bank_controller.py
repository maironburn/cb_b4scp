from logger.app_logger import AppLogger
from src.controllers.selenium_controller import SeleniumController
from src.controllers.xls_controller import XlsController
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

    def __init__(self, kw):

        self._banknames = kw.get('banknames', None)
        self._logger = AppLogger.create_rotating_log()
        if self._banknames:
            self.load_banks()

    def start_party(self, bankname=None, lst_instances_bi=None):

        kw = {'logger': self._logger, 'bank': self._dict_bank.get(bankname).json_data,
              'workflow': self._dict_bank.get(bankname)._json_selenium_wf}

        self.sc = SeleniumController(kw)

        if len(lst_instances_bi):
            self.total_a_crear = len(lst_instances_bi)
            print("\n\n\tFASE Automatismo Selenium \n*****************************************************")
            print("Num de boletos leidos del excel y pendientes de emitir: {}".format(len(lst_instances_bi)))

            self.sc.do_selenium_workflow()

            # for bi in lst_instances_bi:
            #     if self.sc.do_selenium_workflow(bi):
            #         # self.sc.do_image_automation()
            #         self.lst_correctos.append(bi)
            #         self.creados_ok += 1
            #     else:
            #         self.errores_al_crear += 1
            #         self.lst_erroneos.append(bi)

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


if __name__ == '__main__':

    bancos = ['citibank']
    bc = BankController({'banknames': bancos})
    xls_controller = XlsController(**{'logger': bc.logger})
    # @todo, definir q hacer con los boletos q no pasen la validacion
    if xls_controller.get_boletos_items():
        bc.emit_boleto(bankname='citibank', lst_instances_bi=xls_controller.valid_instances_collection)
