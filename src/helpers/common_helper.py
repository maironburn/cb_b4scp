import os
from importlib import import_module

from common_config import JSON_BANK, IMG_RECON_WF, SELENIUM_WF

'''
carga el skel del banco correspondiente 
@param bankname : str(nombre del banco)
@return : diccionario de la entidad (definida en el skel)
'''


def load_json(bankname, path):
    try:
        dictio_path_module_name = {
            JSON_BANK: "json_bank.{}".format(bankname),
            IMG_RECON_WF: "json_bank.img_recognition_workflow.{}".format(bankname),
            SELENIUM_WF: "json_bank.selenium_workflow.{}".format(bankname)
        }
        json_data = os.path.join(path, "{}.py".format(bankname))
        module_name = dictio_path_module_name[path]
        if os.path.exists(json_data):
            module = import_module(module_name)

            return getattr(module, bankname)

    except Exception as e:
        pass

    return None


def load_skel(which_one):

    module_name ='json_bank.windows_screen_skels'
    module = import_module(module_name)

    return getattr(module, which_one)


# def load_json_bank(bankname):
#     try:
#         json_data = os.path.join(JSON_BANK, "{}.py".format(bankname))
#         module_name = "json_bank.{}".format(bankname)
#         if os.path.exists(json_data):
#             module = import_module(module_name)
#
#             return getattr(module, bankname)
#
#     except Exception as e:
#         pass
#
#     return None


#
# def load_json_img_recognition(bankname):
#     try:
#         json_data = os.path.join(IMG_RECON_WF, "{}.py".format(bankname))
#         module_name = "json_bank.img_recognition_workflow.{}".format(bankname)
#         if os.path.exists(json_data):
#             module = import_module(module_name)
#
#             return getattr(module, bankname)
#
#     except Exception as e:
#         pass
#
#     return None
#
#
# def load_json_selenium_wf(bankname):
#     try:
#         json_data = os.path.join(SELENIUM_WF, "{}.py".format(bankname))
#         module_name = "json_bank.selenium_workflow.{}".format(bankname)
#         if os.path.exists(json_data):
#             module = import_module(module_name)
#
#             return getattr(module, bankname)
#
#     except Exception as e:
#         pass
#
#     return None


if __name__ == '__main__':
    pass
