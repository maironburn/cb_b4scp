import os
from time import sleep
from importlib import import_module
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait as wait

import src.controllers.img_recognition_controller as irc
from common_config import ERROR_IMGS, BOLETOS_PROCESADOS_IMGS, TEMPLATES_IMGS
from common_config import IE_DRIVER
from src.helpers.common_helper import load_skel


# pickle.dump(driver.get_cookies() , open("QuoraCookies.pkl","wb"))


class SeleniumController(object):
    _driver = None
    _bank = None
    _workflow = None
    _img_recon_workflow = None
    _logger = None

    _skels = {}
    find_method = None
    finds_method = None
    ec_ref = None
    login_dict_methods = None
    _is_done = False

    def __init__(self, kw):

        self.dictio_actions = {'click': irc.click,
                               'fill': irc.fill
                               }

        self._logger = kw.get('logger')
        if kw.get('bank', None):
            self.bank = kw.get('bank')
            # contiene la linea ppal y loop
            self.img_recon_workflow = kw.get('img_recon_workflow', None)



    def get_wf_details(self, wf_item):

        for k, v in wf_item.items():
            pantalla_name = k
            workflow = v
            needle_img = load_skel(pantalla_name).get('_template')  # template de la pantalla
            self._logger.info("needle (template): {}".format(needle_img.split('\\')[-1]))
            # print("needle (template): {}".format(needle_img.split('\\')[-1]))

        return pantalla_name, needle_img, workflow

    def do_image_automation(self, json_workflow=None, boleto_instance=None):

        self.is_done = False
        json_workflow = self.img_recon_workflow.get(
            'img_recognition_workflow_main') if json_workflow is None else self.img_recon_workflow.get(json_workflow)


        for wf_item in json_workflow:

            needle_img = None
            pantalla_name = None
            if not pantalla_name:
                pantalla_name, needle_img, workflow = self.get_wf_details(wf_item)

            haystack = irc.capture_screen(pantalla_name)
            pantalla_instance = irc.load_json_skel(pantalla_name)
            if self.check_screen(pantalla_name, haystack, needle_img):

                # carga y mapea los elementos de la pantalla
                irc.load_screen_elements(pantalla_instance)
                print("Obtenida posicion del elemento: {}".format(workflow[0].get('target')))
                self._logger.info("Obtenida posicion del elemento: {}".format(workflow[0].get('target')))

                if pantalla_name == 'select_account_dialog' and boleto_instance:

                    self._logger.info("select_account_dialog -> account: {}".format(boleto_instance.account_number))
                    account_element = pantalla_instance.get_element_by_name(boleto_instance.account_number)
                    irc.click(account_element)
                    # sleep(2)
                    ok_element = pantalla_instance.get_element_by_name('ok')
                    irc.click(ok_element)

                else:

                    elemento = pantalla_instance.get_element_by_name(workflow[0].get('target'))
                    # realizando accion sobre el elemento target
                    self.dictio_actions[workflow[0].get('action')](elemento)
            else:
                return False

        return True





        #
        # else:
        #     pantalla =self.where_am_i()
        #
        #     if pantalla=='home':
        #         json_workflow = self.img_recon_workflow.get(
        #             'img_recognition_workflow_main')
        #         self.do_image_automation(json_workflow=None)
        #     else:
        #         module_name = "json_bank.windows_screen_skels"
        #         module = import_module(module_name)
        #         pantalla_skel= getattr(module, pantalla)
        #
        #         workflow_trace_file="json_bank.img_recognition_workflow.citibank"
        #         module = import_module(workflow_trace_file)
        #         workflow= getattr(module, 'citibank')
        #
        #         from common_config import DICTIO_PAPAFRITA
        #         for item in  workflow[DICTIO_PAPAFRITA[pantalla]]:
        #             for k,v in item.items():
        #                 if item == pantalla:
        #                     wf=''
        #



    def check_screen(self, pantalla_name, haystack, needle_img):
        '''
        :param pantalla_name: nombre de la pantalla, con ese nombre se guarda en el TMP
        :param haystack: captura de la pantalla
        :param needle_img: imagen "template" de la carpeta template
        :return:
            comprueba la imagen del template con la captura de pantalla para asegurar que nos hallamos en la pantalla objetivo

        '''
        print(
            "Comprobando Matching entre : {} y la captura de pantalla ".format(
                needle_img.split('\\')[-1]))
        self._logger.info(
             "Comprobando Matching entre : {} y la captura de  pantalla ".format(
                needle_img.split('\\')[-1]))
        temp=10
        found= False

        while not found and temp>0:
            if irc.image_finded(haystack, needle_img):
                self._logger.info("Screen Matched !!")
                print("Screen Matched !!")
                found=True
            else:
                sleep(1)
                haystack = irc.capture_screen(pantalla_name)
                temp-=1
        # print("Screen Matched !!")

        if not found:
            print ("Definitivamente estoy perdido")

        return found




    def boleto_wf_loop(self, boleto):

        boleto_json = boleto.get_json()
        pantalla_name = None

        workflow = self.img_recon_workflow.get('collection_item_detail')
        pantalla_name = 'collection_item_detail'
        needle_img = load_skel(pantalla_name).get('_template')  # template de la pantalla
        sleep(2)
        haystack = irc.capture_screen(pantalla_name)
        pantalla_instance = irc.load_json_skel(pantalla_name)
        # check capture vs template to ensure the right screen
        self.check_screen(pantalla_name, haystack, needle_img)
        # carga y mapea las coordenadas de los elementos de la pantalla

        irc.load_screen_elements(pantalla_instance)  # carga inmediata, no elementos diferidos

        print("\n************ Boleto_wf_loop ************ \n")
        for wfi in workflow:

            action = wfi.get('action')
            target = wfi.get('target')

            self._logger.info("action :{}, target: {}".format(action, target))

            boleto_searched_data = wfi.get('boleto_data', None)
            print("Dato del boleto : {}".format(boleto_searched_data))
            self._logger.info("Dato del boleto : {}".format(boleto_searched_data))
            if boleto_searched_data:
                data = boleto.get_json()[boleto_searched_data]
                element = pantalla_instance.get_element_by_name(target)

                self._logger.info("Dato del boleto : {}".format(data))
                if action == 'select':
                    # element es de tipo combo
                    # print("Haciendo click sobre: {}".format(element.name))
                    irc.click(element)
                    # sleep(1)
                    haystack = irc.capture_screen(pantalla_name)
                    print("")
                    needle_cmboption_element = element.get_cmboption_by_name(data)
                    needle_cmboption_img = needle_cmboption_element.image
                    self.check_screen(pantalla_name, haystack, needle_cmboption_img)
                    needle_cmboption_element.x, needle_cmboption_element.y = irc.getElementCoords(haystack,
                                                                                                  needle_cmboption_img)
                    # irc.double_click(needle_cmboption_element)
                    if target == 'allow_divergent':
                        irc.click(needle_cmboption_element)
                    else:
                        irc.double_click(needle_cmboption_element)
                    # print("Haciendo double_click sobre: {} -> {}".format(element.name, data))
                if action == 'fill':
                    self.dictio_actions['fill'](element, data)
                    # sleep(1)

            if action == 'click':
                element = pantalla_instance.get_element_by_name(target)
                self.dictio_actions['click'](element)

            # sleep(2)

            if action == 'submit':
                # sleep(2)
                # aqui ya se esta mostrando el dialog de guardado
                haystack = irc.capture_screen(pantalla_name)
                element = pantalla_instance.get_element_by_name(target)
                needle_img = element.image
                element.x, element.y = irc.getElementCoords(haystack, needle_img)
                # irc.double_click(needle_cmboption_element)
                irc.capture_screen(boleto.boleto_number, dest=BOLETOS_PROCESADOS_IMGS)
                irc.click(element)

                if not self.got_error(boleto): # @todo  debe estar antes del submit !!!!
                    workflow = self.img_recon_workflow.get('collection_item_detail_window_success')
                    pantalla_name = 'collection_item_detail_window_success'
                    needle_img = load_skel(pantalla_name).get('_template')  # template de la pantalla

                    haystack = irc.capture_screen('collection_item_detail_window_success')
                    pantalla_instance = irc.load_json_skel(pantalla_name)
                    if irc.image_finded(haystack, needle_img):
                        irc.load_screen_elements(pantalla_instance)
                        element = pantalla_instance.get_element_by_name('ok')
                        element.x, element.y = irc.getElementCoords(haystack, element.image)
                        irc.capture_screen(boleto.boleto_number, dest=BOLETOS_PROCESADOS_IMGS)
                        irc.click(element)




    def got_error(self, boleto):

        workflow = self.img_recon_workflow.get('collection_item_detail_window_error')
        pantalla_name = 'collection_item_detail_window_error'
        needle_img = load_skel(pantalla_name).get('_template')  # template de la pantalla
        sleep(5)
        haystack = irc.capture_screen('collection_item_detail_window_error')
        pantalla_instance = irc.load_json_skel(pantalla_name)

        if irc.image_finded(haystack, needle_img):
            print("Ha ocurrido un error generando el boleto: {}".format(boleto.boleto_number))

            boleto_tmp = os.path.join(BOLETOS_PROCESADOS_IMGS, "{}.png".format(boleto.boleto_number))
            if os.path.exists(boleto_tmp):
                os.remove(boleto_tmp)

            irc.load_screen_elements(pantalla_instance)
            element = pantalla_instance.get_element_by_name('ok')
            element.x, element.y = irc.getElementCoords(haystack, element.image)
            irc.capture_screen(boleto.boleto_number, dest=ERROR_IMGS)
            irc.click(element)

            # self.do_image_automation()
            for error_wf in workflow:
                action = error_wf.get('action')
                target = error_wf.get('target')
                delay = error_wf.get('delay')
                haystack = irc.capture_screen(target)
                # irc.click(element)
                element = pantalla_instance.get_element_by_name(target)
                element.x, element.y = irc.getElementCoords(haystack, element.image)
                # print ("target: {}, action: {}".format(target,action ))
                self.dictio_actions[action](element)
                if delay:
                    sleep(delay)
            # irc.click(element)
        else:
            print("Boleto {} generado correctamente ".format(boleto.boleto_number))

        return False


    # <editor-fold desc="getters /setters">


    @property
    def skels(self):
        return self._skels

    @skels.setter
    def skels(self, value):
        if value:
            return self._skels

    @property
    def bank(self):
        return self._bank

    @bank.setter
    def bank(self, value):
        if isinstance(value, dict):
            self._bank = value
    @property
    def is_done(self):
        return self._is_done

    @is_done.setter
    def is_done(self, value):
        if isinstance(value, dict):
            self._is_done = value


    @property
    def workflow(self):
        return self._workflow

    @property
    def img_recon_workflow(self):
        return self._img_recon_workflow

    @img_recon_workflow.setter
    def img_recon_workflow(self, value):
        if value:
            self._img_recon_workflow = value

    @workflow.setter
    def workflow(self, value):
        if value:
            self._workflow = value

    # </editor-fold>
