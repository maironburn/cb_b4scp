# -*- coding: utf-8 -*-

from datetime import datetime
import re

class Boleto_Item(object):

    _boleto_number = None
    _enteprise_id = None
    _cpf = None
    _pid = None

    _emision_date = None
    _due_date = None
    _amount = None

    # los datos de localizacion se dividen en calle, cep (cod postal), ciudad y abreviatura de la ciudad
    _address = None
    _cep = None
    _city = None
    _acrom_city = None


    def __init__(self, **kw):
        self.load_entity_data(kw)
        self.emision_date = datetime.now().strftime("%m/%d/%y")

    def load_entity_data(self, kw):
        self.boleto_number = kw.get ('boleto_number')
        self.enteprise_id = kw.get('enteprise_id')
        self.cpf = kw.get('cpf')
        self.pid = kw.get('pid')
        self.get_data_from_location(kw.get('location_data'))
        self.due_date = kw.get('due_date')
        self.amount = kw.get('amount')

    def get_data_from_location(self, location):

        if location and location.split('.') == 3:
            self.address = location.split('.')[0]
            self.cep = location.split('.')[1]
            self.city = location.split('.')[2]
            self.acrom_city = self.city.split('-').strip()

            return self.address, self.cep, self.city, self.acrom_city

        return False

    # <editor-fold desc="Getter / setters">

    @property
    def boleto_number(self):
        return self._boleto_number

    @boleto_number.setter
    def boleto_number(self, value):
        if value:
            self._boleto_number = value

    @property
    def address(self):
        return self._address

    @address.setter
    def address(self, value):
        if value:
            self._address = value

    @property
    def cep(self):
        return self._cep

    @cep.setter
    def cep_(self, value):
        if value:
            self._cep = value

    @property
    def city(self):
        return self._city

    @city.setter
    def city(self, value):
        if value:
            self._city = value

    @property
    def acrom_city(self):
        return self._acrom_city

    @acrom_city.setter
    def acrom_city(self, value):
        if value:
            self._acrom_city = value

    @property
    def enteprise_id(self):
        return self._enteprise_id

    @enteprise_id.setter
    def enteprise_id(self, value):
        if value:
            self._enteprise_id = value

    @property
    def enteprise_id(self):
        return self._enteprise_id

    @enteprise_id.setter
    def enteprise_id(self, value):
        if value:
            self._enteprise_id = value

    @property
    def cpf(self):
        return self._cpf

    @cpf.setter
    def cpf(self, value):
        if value:
            self._cpf = value

    @property
    def pid(self):
        return self._pid

    @pid.setter
    def pid(self, value):
        if value:
            self._pid = value

    @property
    def location_data(self):
        return self._location_data

    @location_data.setter
    def location_data(self, value):
        if value:
            self._location_data = value

    @property
    def emision_date(self):
        return self._emision_date

    @emision_date.setter
    def emision_date(self, value):
        if value:
            self._emision_date = value

    @property
    def due_date(self):
        return self._due_date

    @due_date.setter
    def due_date(self, value):
        if value:
            self._due_date = value

    @property
    def amount(self):
        return self._amount

    @amount.setter
    def amount(self, value):
        if value:
            self._amount = value

    # </editor-fold>


if __name__ == '__main__':
    bi = Boleto_Item()
    print("{}".format(bi.emision_date))
