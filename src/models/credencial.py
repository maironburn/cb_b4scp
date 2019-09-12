# -*- coding: utf-8 -*-


class Credencial(object):
    _user_id = None
    _pass_pin = None
    _enterprise_id = None

    def __init__(self, kw):
        # @todo (tbd) origen las credenciales

        self.user_id = kw.get('user_id', None)
        self.pwd = kw.get('pwd', None)
        self.enterprise_id = kw.get('enterprise_id', None)

    # <editor-fold desc="Getters /Setters...nada interesante">
    @property
    def user_id(self):
        return self._user_id

    @user_id.setter
    def user_id(self, value):
        if value:
            self._user_id = value

    @property
    def pwd(self):
        return self._pass_pin

    @pwd.setter
    def pwd(self, value):
        if value:
            self._pass_pin = value

    @property
    def enterprise_id(self):
        return self._enterprise_id

    @enterprise_id.setter
    def enterprise_id(self, value):
        if value:
            self._enterprise_id = value
    # </editor-fold>
