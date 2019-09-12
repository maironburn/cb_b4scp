# -*- coding: utf-8 -*-

from src.models.bank_basis import Bank

class CitiBank(Bank):
    _num_boleto = None
    _cnpj_pagador = None
    _cnpj_beneficiario = None

    def __init__(self, kw):
        super().__init__(kw)

    @property
    def num_boleto(self):
        return self._num_boleto

    @num_boleto.setter
    def num_boleto(self, value):
        if value:
            self._num_boleto = value

    @property
    def cnpj_pagador(self):
        return self._cnpj_pagador

    @cnpj_pagador.setter
    def cnpj_pagador(self, value):
        if value:
            self._cnpj_pagador = value

    @property
    def cnpj_beneficiario(self):
        return self._cnpj_beneficiario

    @cnpj_beneficiario.setter
    def cnpj_beneficiario(self, value):
        if value:
            self._cnpj_beneficiario = value
