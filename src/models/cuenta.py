# -*- coding: utf-8 -*-
from src.models.credencial import Credencial


class Cuenta(object):
    _num_cuenta = None
    _credencial = None

    def __init__(self, kw):
        self._credenciales = kw.get('credenciales', None)

    @property
    def credencial(self):
        return self._credencial

    @credencial.setter
    def credencial(self, value):
        if isinstance(value, Credencial):
            self._credenciales = value

    @property
    def num_cuenta(self):
        return self._num_cuenta

    @credencial.setter
    def num_cuenta(self, value):
        if value:
            self._num_cuenta = value
