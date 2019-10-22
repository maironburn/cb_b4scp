# -*- coding: utf-8 -*-
import os
import re

from common_config import DICT_REGEX_BOLETO_ITEM, IMGS_DATASET
from src.controllers.img_recognition_controller import get_element_name_from_filename


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

    _type_of_collection_item_code = '0'
    _collection_item_document_type = '7'
    _allow_divergent = '3'

    _payer_type = ''

    _is_valid = True  # Flag que identidica si la instancia tiene validados todos los campos
    # esta propia sera comprobada por el xls_controller, en caso de no ser valida no se añade a la collecion de items

    _registered_accounts = []

    _error_description = []

    def __init__(self, **kw):
        self._logger = kw.get('logger')
        self.load_registered_accounts()
        self.load_entity_data(kw)

    def load_entity_data(self, kw):
        self.boleto_number = kw.get('boleto_number')
        self.enteprise_id = kw.get('enteprise_id')
        self.cpf = self.check_correct_length(kw.get('cpf'))
        self.cpnj_beneficiario = self.check_correct_length(kw.get('cpnj_beneficiario'))
        self.product = kw.get('product')
        self.account_number = kw.get('account_number')
        self.address = kw.get('address')
        self.state = kw.get('state')
        self.city = kw.get('city')
        self.zip_code = self.check_correct_zip_code(kw.get('zip_code'))  # need 8 caracteres
        # self.emision_date = datetime.now().strftime("%d/%m/%Y")
        self.emision_date = self.transform_date(kw.get('emision_date'))
        self.due_date = self.transform_date(kw.get('due_date'))
        self.amount = kw.get('amount')
        self.payer_type = self.get_payer_type()

        self.check_is_valid()

    def load_registered_accounts(self):
        accounts_folder = os.path.join(IMGS_DATASET, 'select_account_dialog')

        try:
            for filename in [x for x in os.listdir(accounts_folder) if
                             not x.startswith('_')]:
                account = get_element_name_from_filename(filename)
                self._registered_accounts.append(account)

            self.registered_accounts.remove('ok')

        except Exception as e:
            self._logger.error("error al registrar las cuentas")

    def check_account_number(self, account):
        return account in self.registered_accounts

    def transform_date(self, date):

        #if re.match(DICT_REGEX_BOLETO_ITEM['due_date'], date):
        if date:
            fecha = date.split('-')
            return ("{}/{}/{}".format(fecha[2], fecha[1], fecha[0]))

        return None

    def check_is_valid(self):

        self.is_valid = True
        self.error_description=[]
        if re.match(DICT_REGEX_BOLETO_ITEM['boleto_number'], self.boleto_number) is not None:

            if (self.enteprise_id == 'nan' or self.enteprise_id.strip() == ''):
                self.error_description.append('El enterprise ID {}  del boleto {} no es valido'.format(self.enteprise_id.strip(), self.boleto_number))
                print ('El enterprise ID:  del boleto: {} no es valido'.format(self.enteprise_id.strip(), self.boleto_number))
                self.is_valid = False

            if not  self.check_account_number(self.account_number.strip()):
                self.error_description.append('EL numero de cuenta {} del boleto {} no es valido o se trata de una cuenta no conocida'.format(self.account_number, self.boleto_number))
                print ('EL numero de cuenta {} del boleto {} no es valido o se trata de una cuenta no conocida'.format(self.account_number, self.boleto_number))
                self.is_valid = False
                '''
                #and re.match(DICT_REGEX_BOLETO_ITEM['cpf'], self.cpf ) is not None
                #and re.match(DICT_REGEX_BOLETO_ITEM['cpf'], self.cpnj_beneficiario) is not None
                '''

            if self.product == 'nan' or self.product.strip() == '' or (self.product != '100' and self.product != '180'):
                self.error_description.append(
                    'El numero de producto: {} del boleto {} no es valido, debe ser 100 o 180'.format(self.product, self.boleto_number))
                print('El numero de producto: {} del boleto {} no es valido, debe ser 100 o 180'.format(self.product, self.boleto_number))
                self.is_valid = False


            if self.state.strip() == 'nan' or self.state.strip() == '':
                self.error_description.append(
                    'El estado (state city) del boleto {} no es valido '.format(
                        self.state, self.boleto_number))
                print(
                    'El estado (state city) del boleto {} no es valido '.format(
                        self.state, self.boleto_number))
                self.is_valid = False

            if self.city.strip() == 'nan' or self.city.strip() == '':
                self.error_description.append(
                    'La Ciudad {} del boleto {} no es valida'.format(
                        self.city.strip(), self.boleto_number))
                print(
                    'La Ciudad {} del boleto {} no es valida'.format(
                        self.city.strip(), self.boleto_number))
                self.is_valid = False

            if self.zip_code.strip() == 'nan' or self.zip_code.strip() == '':
                self.error_description.append(
                    'El zip code {} del boleto: {} no es valido'.format(
                        self.zip_code.strip(), self.boleto_number))
                print(
                    'El zip code {} del boleto: {} no es valido'.format(
                        self.zip_code.strip(), self.boleto_number))
                self.is_valid = False

            if re.match(DICT_REGEX_BOLETO_ITEM['due_date'], self.due_date) is None:
                self.error_description.append(
                    'El due_date {} del boleto: {} no es valido'.format(
                        self.due_date, self.boleto_number))
                print(
                    'El due_date {} del boleto: {} no es valido'.format(
                        self.due_date, self.boleto_number))
                self.is_valid = False

            if re.match(DICT_REGEX_BOLETO_ITEM['emision_date'], self.emision_date) is None:
                self.error_description.append(
                    'La fecha de emision {} del boleto: {} no es valido, formato correcto : dd/mm/yyyy'.format(
                        self.emision_date, self.boleto_number))
                print(
                    'La fecha de emision {} del boleto: {} no es valido, formato correcto : dd/mm/yyyy'.format(
                        self.emision_date, self.boleto_number))
                self.is_valid = False

            if self.amount.strip() == '' or self.amount.strip() == 'nan':
                self.error_description.append(
                    'El monto {} del boleto: {} no es valido'.format(
                        self.amount.strip(), self.boleto_number))
                print(
                    'El monto {} del boleto: {} no es valido'.format(
                        self.amount.strip(), self.boleto_number))

                self.is_valid = False

        else:
            self.error_description.append('El numero de boleto no es valido')
            print("El numero del boleto no es valido")
            self.is_valid = False

        return self.is_valid

        # @todo

    def get_payer_type(self):
        dict_payer_type = {11: 'cpf', 14: 'cnpj'}

        if len(self.cpf) in dict_payer_type.keys():
            return dict_payer_type[len(self.cpf)]

    def check_correct_zip_code(self, zip):
        need_add = False
        n_iter = 0
        to_append = ''

        if zip != 'nan':
            if len(zip) < 8:
                self._logger.info("check_correct_length, ZIP Code con {}, need add".format(len(zip)))
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

        if cpf and len(cpf) < 11:
            self._logger.info("check_correct_length, CPF con {}, need add".format(len(cpf)))
            n_iter = 11 - len(cpf)

        if cpf and len(cpf) > 11 and len(cpf) < 14:
            self._logger.info("check_correct_length, CNPJ con {}, need add".format(len(cpf)))
            n_iter = 14 - len(cpf)

        if cpf and n_iter:
            for i in range(n_iter):
                to_append += '0'

            return to_append + cpf

        return cpf

    def get_json(self):
        return {'product': self._product,
                'amount': self._amount,
                'emision_date': self._emision_date,
                'boleto_number': self._boleto_number,
                'due_date': self._due_date,
                'enteprise_id': self._enteprise_id,
                'cpf': self._cpf,
                'address': self._address,
                'state': self._state,
                'city': self._city,
                'zip_code': self._zip_code,
                'type_of_collection_item_code': self._type_of_collection_item_code,
                'collection_item_document_type': self._collection_item_document_type,
                'allow_divergent': self._allow_divergent,
                'payer_type': self.payer_type
                }

    # @todo
    def get_errors(self):
        if len(self.error_description):
            for e in self.error_description:
                print("->{}".format(e))

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

    @property
    def payer_type(self):
        return self._payer_type

    @payer_type.setter
    def payer_type(self, value):
        if value:
            self._payer_type = value

    @property
    def registered_accounts(self):
        return self._registered_accounts

    @registered_accounts.setter
    def registered_accounts(self, value):
        if value:
            self._registered_accounts = value

    # </editor-fold>


if __name__ == '__main__':
    bi = Boleto_Item()
    print("{}".format(bi.get_json()))
    print("")
    # print("{}".format(bi.emision_date))
