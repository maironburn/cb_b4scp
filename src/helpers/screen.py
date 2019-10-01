from common_config import TEMP_IMGS
import pyautogui
from PIL import Image
import os
import cv2

dictio_screentext_identificative = {

    'plataforma de programas de ayuda': 'main',
    'lista de declarantes': 'declarantes',
    'datos del declarante': 'nuevo_declarante',
    'cambiar NIF': 'modificar_nif'
                   ''' ...'''
}



def getElementCoords(haystack, needle):
    img = cv2.imread(haystack, cv2.IMREAD_COLOR)
    img_display = img.copy()
    templ = cv2.imread(needle, cv2.IMREAD_COLOR)
    result = cv2.matchTemplate(img, templ, cv2.TM_CCORR_NORMED)
    cv2.normalize(result, result, 0, 1, cv2.NORM_MINMAX, -1)
    _minVal, _maxVal, minLoc, maxLoc = cv2.minMaxLoc(result, None)
    matchLoc = maxLoc
    print("{} ->  minVal:  {}, maxVal:   {}".format(needle, _minVal, _maxVal))

    return _minVal
    '''
    h, w, _ = templ.shape

    center = (int((matchLoc[0] + w / 2)), int((matchLoc[1] + templ.shape[0]) - h / 2))
    x_center = int(matchLoc[0] + w / 2)
    y_center = int((matchLoc[1] + templ.shape[0]) - h / 2)

    return x_center, y_center
    '''


def capture_screen(name="screenshot"):
    pyautogui.screenshot("{}{}.png".format(TEMP_IMGS, name))
    print("captured windows: {}".format(name))


if __name__ == '__main__':
    # print("{}".format(screen_resolution()))
    #capture_screen()
    # src_img = ("{}{}".format(TEMP_IMGS, "screenshot.png"))
    haystack = ("{}{}".format(TEMP_IMGS, "declarantes.png"))



'''
#needle = "{}{}{}".format(SCREEN_SNAP, os.path.sep, 'nuevo_declarante.png')

needle = ("{}{}".format(TEMP_IMGS, "screenshot.png"))
print(getElementCoords(needle))
'''
