# -*- coding: utf-8 -*-
from src.helpers.common_helper import load_json

from common_config import JSON_BANK, IMG_RECON_WF , SELENIUM_WF

class Bank(object):
    _name = None
    _json_data = None
    _json_selenium_wf = None
    _json_img_recognition = None
    _logger = None
    _cuentas_asociadas = []

    def __init__(self, kw):

        self._name = kw.get('name', None)
        self._logger = kw.get('logger', None)
        if self.name:
            self.load_skel()

    def load_skel(self):

        try:
            self._json_data = load_json(self.name, JSON_BANK)
            self._json_selenium_wf  =load_json(self.name, SELENIUM_WF)
            self._json_img_recognition = load_json(self.name, IMG_RECON_WF)
            self._logger.info('{} -> Loaded skel from : {}'.format(self.__class__.name, self.name))


        except Exception as lse:
            self._logger.error("{}-> exception loading skel {} -> {}".format(self.__class__.name, self.name, lse))


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


