import os
import time
from os.path import sep
import numpy as np
import cv2
import pyautogui

from common_config import TEMP_IMGS, IMGS_DATASET
from json_bank import windows_screen_skels
from src.models import elemento
from src.models.pantalla import Pantalla


def capture_screen(name="screenshot", dest=TEMP_IMGS):
    captured = os.path.join(dest, "{}.png".format(name))
    pyautogui.screenshot(captured)
    time.sleep(2)

    return captured


def image_finded(haystack, needle):

    img = cv2.imread(haystack, cv2.IMREAD_COLOR)
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img_display = img.copy()
    templ = cv2.imread(needle, 0)

    result = cv2.matchTemplate(img_gray, templ, cv2.TM_CCOEFF_NORMED)
    _minVal, _maxVal, minLoc, maxLoc = cv2.minMaxLoc(result, None)
    threshold = 0.8
    loc = np.where(result >= threshold)
    print ("image_finded: -> {} ({})".format(_maxVal > 0.75, round(_maxVal*100,2)))

    return _maxVal > 0.75
    #return _maxVal > 0.98


def getElementCoords(haystack, needle):
    img = cv2.imread(haystack, cv2.IMREAD_COLOR)
    img_display = img.copy()
    templ = cv2.imread(needle, cv2.IMREAD_COLOR)

    result = cv2.matchTemplate(img, templ, cv2.TM_CCORR_NORMED)
    cv2.normalize(result, result, 0, 1, cv2.NORM_MINMAX, -1)
    _minVal, _maxVal, minLoc, maxLoc = cv2.minMaxLoc(result, None)
    matchLoc = maxLoc

    # Show the final image with the matched area.
    h, w, _ = templ.shape

    center = (int((matchLoc[0] + w / 2)), int((matchLoc[1] + templ.shape[0]) - h / 2))
    x_center = int(matchLoc[0] + w / 2)
    y_center = int((matchLoc[1] + templ.shape[0]) - h / 2)

    return x_center, y_center


def load_combo_options(combo, folder):
    # captura de pantalla dinamica alojada en la carpeta temporal
    combo.options = {}
    for filename in os.listdir(folder):
        kw = {'filename': filename, 'contenedor': combo}
        element_instance = create_element_instance(kw, get_coords=False, contenedor_path=folder)
        combo.add_element(element_instance)


def load_json_skel(pantalla_name):
    try:
        window = getattr(windows_screen_skels, pantalla_name)
        if windows_screen_skels:
            #print("load_json_skel -> {} ".format(pantalla_name))
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


def load_screen_elements(elemento_contenedor):
    # captura de pantalla dinamica alojada en la carpeta temporal

    haystack = os.path.join(TEMP_IMGS, "{}.png".format(elemento_contenedor.name))
    for filename in [x for x in os.listdir(elemento_contenedor.image_folder) if
                     not x.startswith('_') and
                     os.path.isfile(os.path.join(elemento_contenedor.image_folder, x))]:
        kw = {'filename': filename, 'contenedor': elemento_contenedor, 'haystack': haystack}
        element_instance = create_element_instance(kw, get_coords=True)
        #print("Elemento {} instanciado , coord x: {} , y: {}".format(element_instance.name, element_instance.x, element_instance.y))

        elemento_contenedor.add_element(element_instance)
        if isinstance(element_instance, elemento.Combo) and os.path.exists(
                os.path.join(elemento_contenedor.image_folder, filename.split('.')[0])) and os.path.isdir(
            os.path.join(elemento_contenedor.image_folder, filename.split('.')[0])):
            element_instance.options = {}
            load_combo_options(element_instance, os.path.join(elemento_contenedor.image_folder, filename.split('.')[0]))
            print("")


def click(target):

    pyautogui.moveTo(target.x, target.y)
    pyautogui.click()


def double_click(target):

    pyautogui.moveTo(target.x, target.y)
    pyautogui.doubleClick()


def fill(target, data):

    pyautogui.moveTo(target.x, target.y)
    pyautogui.doubleClick()
    pyautogui.typewrite(str(data))
    #pyautogui.typewrite(str(data), 0.1)



def create_element_instance(kw, get_coords=False, contenedor_path=None):
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
    #print("creando instancia del elemento: {}".format(element_name))
    contenedor_path = contenedor_path if contenedor_path else contenedor.image_folder

    needle = os.path.join(contenedor_path, filename)

    ''' call to tesseract controller'''
    if get_coords:
        try:
            x, y = getElementCoords(haystack, needle)
            #print("get_coords del elemento: {} -> ({},{}) ".format(element_name, x, y))
        except Exception as e:
            pass
    kw = {'_name': element_name, '_image': needle, '_x': x, '_y': y,
          '_parent': contenedor.parent}
    '''building windows'''

    elm_instance = dinamic_instance_elements(element_type, kw)
    elm_instance and contenedor.add_element(elm_instance)

    return elm_instance



# if __name__ == "__main__":
#     needle='C:\\Users\\mario.diaz.rodriguez\\PycharmProjects\\CitiBank_Boletos\\images\\dataset\\warning_msg\\boton_yes.png'
#     haystack = 'C:\\Users\\mario.diaz.rodriguez\\PycharmProjects\\CitiBank_Boletos\\images\\temp\\warning_msg.png'
#
#     image_finded (haystack,needle)