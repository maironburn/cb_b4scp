import os
from importlib import import_module

from common_config import JSON_BANK

'''
carga el skel del banco correspondiente 
@param bankname : str(nombre del banco)
@return : diccionario de la entidad (definida en el skel)
'''
def load_json_bank_from_skel(bankname):
    try:
        json_file = os.path.join(JSON_BANK, "{}.py".format(bankname))
        module_name = "json_bank.{}".format(bankname)
        if os.path.exists(json_file):
            module = import_module(module_name)

            return getattr(module, bankname)

    except Exception as e:
        pass

    return None


if __name__ == '__main__':
    pass
