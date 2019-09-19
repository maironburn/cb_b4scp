from src.models.citibank import CitiBank
from src.models.bank_basis import Bank
from src.controllers.selenium_controller import SeleniumController
from src.controllers.xls_controller import XlsController
from logger.app_logger import AppLogger


class BankController(object):
    _dict_bank = {}
    _banknames = []
    _sc = None  # selenium controller
    _logger = None

    def __init__(self, kw):

        self._banknames = kw.get('banknames', None)
        self._logger = AppLogger.create_rotating_log()
        if self._banknames:
            self.load_banks()



    def generate_boleto(self, bankname=None, lst_instances_bi= None):

        kw = {'logger': self._logger, 'bank': self._dict_bank.get(bankname).json_data}
        self.sc = SeleniumController(kw)

        for bi in lst_instances_bi:
          self.sc.create_boleto(bi)

        self.sc.driver_close()



    def extract_movements(self, bankname=None):

        if bankname and bankname in self._dict_bank.keys():
            kw = {'logger': self._logger, 'bank': self._dict_bank.get(bankname).json_data}
            self.sc = SeleniumController(kw)
            if self.sc.do_the_process():
                if kw.get('bank').get('boleto_workflow'):
                    self.sc.create_boleto()


    def load_banks(self):
        for bank in self.banknames:
            kw = {'logger': self._logger, 'name': bank}
            bank_instance =  CitiBank(kw) if bank=='citibank' else Bank(kw)
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
    xls_controller= XlsController (**{'logger': bc.logger})
    if xls_controller.get_boletos_items():
        for b in bancos:
            bc.extract_movements(b)
