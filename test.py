import os

from common_config import *
from json_bank import windows_screen_skels
from src.controllers.img_recognition_controller import getElementCoords
from src.models import elemento
from src.models.pantalla import Pantalla


def load_json_skel(pantalla_name):
    try:
        window = getattr(windows_screen_skels, pantalla_name)
        if windows_screen_skels:
            return Pantalla(**window)
    except Exception as e:
        pass

    return None


def get_type_from_filename(filename):
    '''extract name until first _ cause it defines class type'''
    return filename.split('_')[0].capitalize()


def get_element_name_from_filename(filename):
    '''element name without extension neither type'''
    return filename[0:filename.index('.')][filename.index('_') + 1:]


def dinamic_instance_elements(element_type, init_values):
    '''instantiating attending to element_type (inferred by the filename first _  )'''
    try:
        # getattr(module, class_name)
        element_type = getattr(elemento, element_type)
        return element_type(init_values)

    except Exception as e:
        pass
    return None


def create_element_instance(kw, get_coords=False, contenedor_path= None):
    ''' Instancia a los elementos componentes de la pantalla
        a partir de la imagen del dataset se obtiene el tipo de elemento
        y su nombre...
        p_ej: boton_declarantes --> tipo: boton, nombre: declarante
    '''
    filename = kw.get('filename')
    haystack = kw.get('haystack')
    contenedor = kw.get('contenedor')

    x, y = None, None
    element_type = get_type_from_filename(filename)
    element_name = get_element_name_from_filename(filename)

    contenedor_path= contenedor_path if contenedor_path else contenedor.image_folder

    needle = os.path.join(contenedor_path, filename)

    ''' call to tesseract controller'''
    if get_coords:
        try:
            x, y = getElementCoords(haystack, needle)
        except Exception as e:
            pass
    kw = {'_name': element_name, '_image': needle, '_x': x, '_y': y,
          '_parent': contenedor.parent}
    '''building windows'''

    elm_instance = dinamic_instance_elements(element_type, kw)
    elm_instance and contenedor.add_element(elm_instance)

    return elm_instance


def load_combo_options(combo, folder):
    # captura de pantalla dinamica alojada en la carpeta temporal
    combo.options={}
    for filename in os.listdir(folder):

        kw = {'filename': filename, 'contenedor': combo}
        element_instance = create_element_instance(kw, get_coords=False, contenedor_path= folder )
        combo.add_element(element_instance)



def load_screen_elements(elemento_contenedor):
    # captura de pantalla dinamica alojada en la carpeta temporal

    haystack = os.path.join(TEMP_IMGS, "{}.png".format(elemento_contenedor.name))
    for filename in [x for x in os.listdir(elemento_contenedor.image_folder) if
                         not x.startswith('_') and
                     os.path.isfile(os.path.join(elemento_contenedor.image_folder, x))]:
        kw = {'filename': filename, 'contenedor': elemento_contenedor, 'haystack': haystack}
        element_instance = create_element_instance(kw, get_coords=True)
        elemento_contenedor.add_element(element_instance)
        if isinstance(element_instance, elemento.Combo) and os.path.exists(
                os.path.join(elemento_contenedor.image_folder, filename.split('.')[0])) and os.path.isdir(
                os.path.join(elemento_contenedor.image_folder, filename.split('.')[0])):
                element_instance.options={}
                load_combo_options(element_instance, os.path.join(elemento_contenedor.image_folder, filename.split('.')[0]))
                print("")

if __name__ == '__main__':
    #haystack = 'C:\\Users\\mario.diaz.rodriguez\\PycharmProjects\\CitiBank_Boletos\\images\\dataset\\CitiBank_Dataset\\select_account_dialog.png'
    haystack = 'C:\\Users\\mario.diaz.rodriguez\\PycharmProjects\\CitiBank_Boletos\\images\\dataset\\CitiBank_Dataset\\collection_item_detail.png'
    # needle = 'C:\\Users\\mario.diaz.rodriguez\\PycharmProjects\\CitiBank_Boletos\\images\\dataset\\collection_item_detail\\combo_product.png'
    needle = 'C:\\Users\\mario.diaz.rodriguez\\PycharmProjects\\CitiBank_Boletos\\images\\dataset\\collection_item_detail\\test_payer_name.png'

    # captura pantalla

    #pantalla_name = 'select_account_dialog'
    pantalla_name = 'collection_item_detail'
    pantalla_instance = load_json_skel(pantalla_name)
    try:
        load_screen_elements(pantalla_instance)
    except Exception as e:
        print ("Exception")
    print("")

    # getElementCoords(haystack, needle)
