import os
from time import sleep
import src.controllers.img_recognition_controller as irc
from common_config import ERROR_IMGS, BOLETOS_PROCESADOS_IMGS, TEMPLATES_IMGS
from src.helpers.common_helper import load_skel


class Reboot_Process(object):
    _logger = None

    def __init__(self, kw):

        self._logger = kw.get('logger')
        self._logger.debug("Reboot_Process iniciado")


    def restart_workflow(self):
        print ("Intentando reiniciar el flujo")
        haystack = irc.capture_screen('restart')
        needle_lst=[ os.path.join(TEMPLATES_IMGS,'boton_cancel_dialog.png'),
                     os.path.join(TEMPLATES_IMGS, 'home_selected.png'),
                     os.path.join(TEMPLATES_IMGS, 'home.png')
                     ]

        #  os.path.join(TEMPLATES_IMGS, 'home.png'),
        for needle in needle_lst:
            if irc.image_finded(haystack, needle, threshold=0.7):
                x, y = irc.getElementCoords(haystack, needle)
                import pyautogui
                pyautogui.moveTo(x, y)
                # print("Evento click,move to x: {}, y: {}".format(target.x, target.y))
                pyautogui.click()
                sleep(2)

        return True


    def where_am_i(self):

        print ("Me he despistado...")
        while True:
            for needle in [x for x in os.listdir(TEMPLATES_IMGS) if
                             not x.startswith('_')]:
                print ("Soy {} ?".format(needle))
                haystack = irc.capture_screen('where_am_i')
                if irc.image_finded(haystack, os.path.join(TEMPLATES_IMGS,needle)):
                    print("Efectivamente, soy {}".format(needle))
                    return needle.split('.')[0]

