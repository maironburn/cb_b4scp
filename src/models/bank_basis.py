# -*- coding: utf-8 -*-
from src.helpers.common_helper import load_json_bank_from_skel
from src.models.cuenta import Cuenta


class Bank(object):
    _name = None
    _json_data = None
    _logger = None
    _cuentas_asociadas = []

    def __init__(self, kw):

        self._name = kw.get('name', None)
        self._logger = kw.get('logger', None)
        if self.name:
            self._json_data = self.load_skel()

    def load_skel(self):

        try:
            self._json_data = load_json_bank_from_skel(self.name)
            self._logger.info('{} -> Loaded skel from : {}'.format(self.__class__.name, self.name))
            return self._json_data

        except Exception as lse:
            self._logger.error("{}-> exception loading skel {} -> {}".format(self.__class__.name, self.name, lse))

        return None

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if value:
            self._name = value

    @property
    def json_data(self):
        return self._json_data

    @json_data.setter
    def json_data(self, value):
        if value:
            self._json_data = value

    @property
    def cuentas_asociadas(self):
        return self._cuentas_asociadas

    @cuentas_asociadas.setter
    def cuentas_asociadas(self, value):
        if isinstance(value, Cuenta):
            self._cuentas_asociadas = value
