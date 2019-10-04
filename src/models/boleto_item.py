# -*- coding: utf-8 -*-

from datetime import datetime


class Boleto_Item(object):
    _logger = None

    _boleto_number = str()
    _enteprise_id = str()
    _cpf = str()
    _cpnj_beneficiario = str()
    _product = str()
    _account_number = str()
    _address = str()
    _state = str()
    _city = str()
    _zip_code = str()

    _emision_date = str()
    _due_date = str()
    _amount = str()


    _is_valid = True  # Flag que identidica si la instancia tiene validados todos los campos
    # esta propia sera comprobada por el xls_controller, en caso de no ser valida no se añade a la collecion de items

    _error_description = None

    def __init__(self, **kw):
        self._logger = kw.get('logger')
        self.load_entity_data(kw)

    def load_entity_data(self, kw):

        self.boleto_number = kw.get('boleto_number')
        self.enteprise_id = kw.get('enteprise_id')
        self.cpf = self.check_correct_length( kw.get('cpf'))
        self.cpnj_beneficiario = self.check_correct_length( kw.get('cpnj_beneficiario'))
        self.product = kw.get('product')
        self.account_number = kw.get('account_number')
        self.address  = kw.get('address')
        self.state = kw.get('state')
        self.city = kw.get('city')
        self.zip_code = kw.get('zip_code') #need 8 caracteres
        #self.emision_date = datetime.now().strftime("%d/%m/%Y")
        self.emision_date =  kw.get('emision_date')
        self.due_date = kw.get('due_date')
        self.amount = kw.get('amount')


    #@todo
    def check_is_valid(self):
        return self.boleto_number.strip() != '' and self.enteprise_id.strip() != '' and self.cpnj_beneficiario.strip() != ''


    def check_correct_zip_code(self, zip):

        need_add = False
        n_iter = 0
        to_append = ''

        if len(zip) < 8:
            self._logger.info("check_correct_length, CPF con {}, need add".format(len(cpf)))
            n_iter = 8 - len(zip)

        if n_iter:
            for i in range(n_iter):
                to_append += '0'


            return to_append + zip

        return zip

    def check_correct_length(self, cpf):

        # pueden venir 2 tipos de datos
        # caso CPF , necesariamente debe tener 11 caracteres
        # caso CNPJ, necesariamente debe tener 14 caracteres

        need_add = False
        n_iter = 0
        to_append = ''

        if len(cpf) < 11:
            self._logger.info("check_correct_length, CPF con {}, need add".format(len(cpf)))
            n_iter = 11 - len(cpf)

        if len(cpf)>11 and len(cpf)<14:
            self._logger.info("check_correct_length, CNPJ con {}, need add".format(len(cpf)))
            n_iter = 14 - len(cpf)

        if n_iter:
            for i in range(n_iter):
                to_append += '0'


            return to_append + cpf

        return cpf


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
    def cpnj_beneficiario(self):
        return self._cpnj_beneficiario

    @cpnj_beneficiario.setter
    def cpnj_beneficiario(self, value):
        if value:
            self._cpnj_beneficiario = value

    @property
    def product(self):
        return self._product

    @product.setter
    def product(self, value):
        if value:
            self._product = value

    @property
    def account_number(self):
        return self._account_number

    @account_number.setter
    def account_number(self, value):
        if value:
            self._account_number = value

    @property
    def address(self):
        return self._address

    @address.setter
    def address(self, value):
        if value:
            self._address = value

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, value):
        if value:
            self._state = value

    @property
    def city(self):
        return self._city

    @city.setter
    def city(self, value):
        if value:
            self._city = value

    @property
    def zip_code(self):
        return self._zip_code

    @zip_code.setter
    def zip_code(self, value):
        if value:
            self._zip_code = value

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
            tipo_dato = 'CNPJ' if len(self.cpf) == 14 else 'CPF'
            return "Num boleto: %s\n\tenterprise_id: %s\n\tcpnj_beneficiario: %s\n\t%s pagador: %s" % (

                self.boleto_number,
                self.enteprise_id,
                self.cpnj_beneficiario,
                tipo_dato,
                self.cpf
            )

        return "boleto: %s\n\t error:  %s" % (self.boleto_number, self.error_description)



if __name__ == '__main__':
    bi = Boleto_Item()
    print("{}".format(bi.emision_date))
