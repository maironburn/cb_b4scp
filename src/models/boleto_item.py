# -*- coding: utf-8 -*-

from datetime import datetime


class Boleto_Item(object):
    _logger = None
    _boleto_number = str()
    _enteprise_id = str()
    _cpf = str()
    _pid = str()

    _emision_date = str()
    _due_date = str()
    _amount = str()

    # los datos de localizacion se dividen en calle, cep (cod postal), ciudad y abreviatura de la ciudad
    _address = str()
    _cep = str()
    _city = str()
    _country_code = str()

    _is_valid = True  # Flag que identidica si la instancia tiene validados todos los campos
    # esta propia sera comprobada por el xls_controller, en caso de no ser valida no se añade a la collecion de items

    _error_description = None

    def __init__(self, **kw):
        self._logger = kw.get('logger')
        self.load_entity_data(kw)

    def load_entity_data(self, kw):
        self.boleto_number = kw.get('boleto_number')
        if self.get_data_from_location(kw.get('location_data')):
            self.enteprise_id = kw.get('enteprise_id')
            self.cpf = kw.get('cpf')
            self.pid = kw.get('pid')
            self.due_date = kw.get('due_date')
            self.amount = kw.get('amount')
            self.emision_date = datetime.now().strftime("%m/%d/%y")

    def get_data_from_location(self, location):

        if location and len(location.split('.')) == 3:
            try:
                self.address = location.split('.')[0]
                self.cep = location.split('.')[1].split(':')[1]
                self.city = location.split('.')[2].split('-')[0].strip()
                ac = location.split('.')[2].split('-')[1].strip()
                self.country_code = ''.join([i[0].upper() for i in ac.split()])

                return self.address, self.cep, self.city, self.country_code

            except Exception as e:
                self.is_valid = False
                self._logger.error("Except {} -> get_data_from_location -> {}".format(__class__.__name__, e))
                self.error_description = "{}".format(e)
        else:
            self.is_valid = False
            self._logger.error(
                "Except {} -> boleto: {}, la cadena {} no tiene un formato correcto".format(__class__.__name__,
                                                                                            self.boleto_number,
                                                                                            location))
            self.error_description = "formato no correcto en la cadena: {}".format(location)
        return False

    # @todo
    def validate(self):
        pass

    # <editor-fold desc="Getter / setters">

    @property
    def boleto_number(self):
        return self._boleto_number

    @boleto_number.setter
    def boleto_number(self, value):
        if value:
            self._boleto_number = value

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
    def cep(self, value):
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
    def country_code(self):
        return self._country_code

    @country_code.setter
    def country_code(self, value):
        if value:
            self._country_code = value

    @property
    def is_valid(self):
        return self._is_valid

    @is_valid.setter
    def is_valid(self, value):
        if isinstance(value, bool):
            self._is_valid = value

    @property
    def error_description(self):
        return self._error_description

    @error_description.setter
    def error_description(self, value):
        if value:
            self._error_description = value

    # </editor-fold>

    def __repr__(self):

        if not self.error_description:
            return "boleto: %s\n\tenterprise_id: %s\n\tcpf: %s\n\tpid: %s\n\temision_date: %s\n\tdue_date: %s\n\tamount: %s\n\taddress: %s\n\tcep: %s\n\tcity: %s\n\tcountry_code: %s" % (
                self.boleto_number,
                self.enteprise_id,
                self.cpf,
                self.pid,
                self.emision_date,
                self.due_date,
                self.amount,
                self.address,
                self.cep,
                self.city,
                self.country_code
            )

        return "boleto: %s\n\t error:  %s" % (self.boleto_number, self.error_description)


if __name__ == '__main__':
    bi = Boleto_Item()
    print("{}".format(bi.emision_date))
