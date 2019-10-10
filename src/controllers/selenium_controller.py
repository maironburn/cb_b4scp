import os
import pickle
from time import sleep

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait as wait

import src.controllers.img_recognition_controller as irc
from common_config import IE_DRIVER, ROOT_DIR
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

    def __init__(self, kw):

        self.dictio_actions = {'click': irc.click,
                               'fill': irc.fill
                               }

        self._logger = kw.get('logger')
        if kw.get('bank', None) and kw.get('workflow', None):
            self.bank = kw.get('bank')
            self.workflow = kw.get('workflow', None).get('selenium_workflow')
            # contiene la linea ppal y loop
            self.img_recon_workflow = kw.get('img_recon_workflow', None)

            try:
                self.start()
                self.load_references()
            except Exception as e:
                self._logger.debug("Error al iniciar Selenium -> {}".format(e))

    def load_references(self):

        self.find_method = self.load_find_method_references()
        self.finds_method = self.load_finds_method_references()
        self.ec_ref = self.ec_references()

    def check_cookies(self):

        return os.path.exists(os.path.join(ROOT_DIR, "citibank_cookies.pkl"))

    def save_cookies(self):
        citibank_cookies = os.path.join(ROOT_DIR, "citibank_cookies.pkl")
        pickle.dump(self.driver.get_cookies(), open(citibank_cookies, "wb"))

    def load_cookies(self):
        citibank_cookies = os.path.join(ROOT_DIR, "citibank_cookies.pkl")
        cookies = pickle.load(open(citibank_cookies, "rb"))
        for cookie in cookies:
            self.driver.add_cookie(cookie)

    def do_selenium_workflow(self):

        try:

            if self.driver:
                self.driver.get(self.bank.get('url_base'))
                self._logger.debug("create_boleto, creacion del boleto")
                # # @todo, eliminar los sleeps...sustituir por ec
                # if not self.check_cookies() and self.load_hold_on():
                #     self.save_cookies()
                # else:
                #     pass
                #     #https://portal.citidirect.com/portal/welcome/index
                #     #self.load_cookies()

                return self.do_workflow(stage="Automatismo Selenium")
            # self.driver_close()

        except Exception as ex:
            self._logger.error("Excepcion en do_the_process -> {}".format(ex))

        return False

    # <editor-fold desc="Selenium methods references">
    def load_find_method_references(self):

        return {
            'id': self.driver.find_element_by_id,
            'name': self.driver.find_element_by_name,
            'xpath': self.driver.find_element_by_xpath,
            'class': self.driver.find_element_by_class_name,
            'tag_name': self.driver.find_element_by_tag_name,
            'link_text': self.driver.find_element_by_link_text,
            'partial_link_text': self.driver.find_element_by_partial_link_text,
            'css_selector': self.driver.find_element_by_css_selector
        }

    def load_finds_method_references(self):

        return {
            'id': self.driver.find_elements_by_id,
            'name': self.driver.find_elements_by_name,
            'xpath': self.driver.find_elements_by_xpath,
            'class': self.driver.find_elements_by_class_name,
            'tag_name': self.driver.find_elements_by_tag_name,
            'link_text': self.driver.find_elements_by_link_text,
            'partial_link_text': self.driver.find_elements_by_partial_link_text,
            'css_selector': self.driver.find_elements_by_css_selector
        }

    def ec_references(self):
        return {
            'element_located': ec.presence_of_element_located,
            'frame_switch': ec.frame_to_be_available_and_switch_to_it,
            'clickable': ec.element_to_be_clickable,
            'alert': ec.alert_is_present
        }

    # </editor-fold>

    def wait_for_expected_conditions(self, actions):

        tipo = actions.get('tipo')  # tipo de ec
        target = actions.get('target')
        time_wait = float(actions.get('time_wait'))
        e_description = actions.get('e_description')
        success = False

        print ("Pendiente del Logado del usuario para continuar el automatismo")
        self._logger.info("Pendiente del Logado del usuario para continuar el automatismo")
        try:
            exp_type = self.ec_ref[tipo]
            success = wait(self.driver, time_wait).until(exp_type((By.XPATH, target)))

            print("Web cargada con exito")
            self._logger.info("Web cargada con exito")

            try:
                if wait(self.driver, 10).until(ec.alert_is_present()):
                    print ("Eliminado mensaje de Alert")
                    self._logger.info("Eliminado mensaje de Alert")
                    alert = self.driver.switch_to.alert
                    alert.accept()

            except Exception:
                pass # solo para que no escupa en el log

        except Exception as e:
            self._logger.error(
                "Exception waiting for expected conditions -> target {}, desc: {}".format(target, e_description))


        return success

    def do_workflow(self, stage=""):
        '''
            acciones post login o post login, la mecanica es igual
            @:param, lista de acciones (pre o post acciones)
        '''
        if self.driver:

            for actions in self.workflow:

                tipo = actions.get('tipo')
                target = actions.get('target')
                desc = actions.get('description')
                mode = actions.get('mode')
                ec = actions.get('expected_conditions', None)
                id = actions.get('id', None)

                try:

                    if self.wait_for_expected_conditions(ec):
                        # un poco de tiempo para la carga de la web
                        sleep(5)
                        self._logger.info(
                            "{} -> tipo busqueda: {} , expresion: {} , mode: {}".format(desc, tipo, target, mode))

                        return True

                except Exception as e:
                    pass

        return False

    def get_wf_details(self,wf_item):

        for k, v in wf_item.items():
            pantalla_name = k
            workflow = v
            needle_img = load_skel(pantalla_name).get('_template')  # template de la pantalla

        return pantalla_name, needle_img, workflow

    def do_image_automation(self, json_workflow=None, boleto_instance=None):

        json_workflow = self.img_recon_workflow.get(
            'img_recognition_workflow_main') if json_workflow is None else self.img_recon_workflow.get(json_workflow)
        if not boleto_instance:
            self.driver.get(self.bank.get('applet_url'))
            print ("Esperando la carga del Applet de Java")
            self._logger.info ("Esperando la carga del Applet de Java")
            self.driver.maximize_window()
            sleep(20)

        for wf_item in json_workflow:

            needle_img = None
            pantalla_name = None
            if not pantalla_name:
                pantalla_name, needle_img, workflow = self.get_wf_details(wf_item)

            haystack = irc.capture_screen(pantalla_name)
            pantalla_instance = irc.load_json_skel(pantalla_name)
            self.check_screen(pantalla_name, haystack, needle_img)
            # carga y mapea los elementos de la pantalla
            irc.load_screen_elements(pantalla_instance)
            print("Obteniendo posicion del elemento: {}".format(workflow[0].get('target')))
            self._logger.info("Obteniendo posicion del elemento: {}".format(workflow[0].get('target')))

            if pantalla_name == 'select_account_dialog' and boleto_instance:

                print ("select_account_dialog -> account: {}".format(boleto_instance.account_number))
                self._logger.info("select_account_dialog -> account: {}".format(boleto_instance.account_number))
                account_element = pantalla_instance.get_element_by_name(boleto_instance.account_number)
                irc.click(account_element)
                sleep(2)
                ok_element = pantalla_instance.get_element_by_name('ok')
                irc.click(ok_element)
                sleep(2)
            else:

                elemento = pantalla_instance.get_element_by_name(workflow[0].get('target'))
                # realizando accion sobre el elemento target
                self.dictio_actions[workflow[0].get('action')](elemento)
                sleep(2)



    def check_screen(self, pantalla_name, haystack, needle_img):
        '''
        :param pantalla_name: nombre de la pantalla, con ese nombre se guarda en el TMP
        :param haystack: captura de la pantalla
        :param needle_img: imagen "template" de la carpeta template
        :return:
            comprueba la imagen del template con la captura de pantalla para asegurar que nos hallamos en la pantalla objetivo

        '''
        print(
            "Comprobando correspondencia de imagenes \ntemplate: {} \n/ captured img {} ".format(needle_img, haystack))
        self._logger.info(
            "Comprobando correspondencia de imagenes \ntemplate: {} \n/ captured img {} ".format(needle_img, haystack))
        while not irc.image_finded(haystack, needle_img):
            sleep(5)
            haystack = irc.capture_screen(pantalla_name)

        print("Screen Matched !!")
        self._logger.info("Screen Matched !!")

        return True

    def boleto_wf_loop(self, boleto):


        boleto_json = boleto.get_json()
        pantalla_name = None

        workflow = self.img_recon_workflow.get('collection_item_detail')
        pantalla_name = 'collection_item_detail'
        needle_img = load_skel(pantalla_name).get('_template')  # template de la pantalla
        haystack = irc.capture_screen(pantalla_name)
        pantalla_instance = irc.load_json_skel(pantalla_name)
        # check capture vs template to ensure the right screen
        self.check_screen(pantalla_name, haystack, needle_img)


        # carga y mapea las coordenadas de los elementos de la pantalla
        irc.load_screen_elements(pantalla_instance)  # carga inmediata, no elementos diferidos

        print ("************ Boleto_wf_loop ************ \n")
        for wfi in workflow:

            action = wfi.get('action')
            target = wfi.get('target')
            print ("action :{}, target: {}".format(action, target))
            self._logger.info("action :{}, target: {}".format(action, target))

            boleto_searched_data = wfi.get('boleto_data', None)
            print("Obteniedo dato del boleto : {}".format(boleto_searched_data))
            self._logger.info("Obteniedo dato del boleto : {}".format(boleto_searched_data))
            if boleto_searched_data:
                data = boleto.get_json()[boleto_searched_data]
                element = pantalla_instance.get_element_by_name(target)
                print("Dato del boleto : {}".format(data))

                self._logger.info("Dato del boleto : {}".format(data))
                if action == 'select':
                    # element es de tipo combo
                    print ("Haciendo click sobre: {}".format(element.name))
                    irc.click(element)
                    sleep(2)
                    haystack = irc.capture_screen(pantalla_name)
                    print ("")
                    needle_cmboption_element = element.get_cmboption_by_name (data)
                    needle_cmboption_img = needle_cmboption_element.image
                    needle_cmboption_element.x, needle_cmboption_element.y = irc.getElementCoords(haystack, needle_cmboption_img)
                    irc.double_click(needle_cmboption_element)

                if action == 'fill':
                    self.dictio_actions['fill'](element, data)
                    sleep(1)

            if action == 'click':
                element = pantalla_instance.get_element_by_name(target)
                self.dictio_actions['click'](element)

            sleep(2)

                # for wf_item in range(workflow):
            #     if wf_item.get('action') == 'click':
            #         if wf_item.get('target') == 'cmboption':
            #             pass
            #         else:
            #             elemento = pantalla_instance.get_element_by_name(workflow[wf_item].get('target'))
            #             # realizando accion sobre el elemento target
            #             self.dictio_actions['click'](elemento)
            #     else:
            #         elemento = pantalla_instance.get_element_by_name(workflow[wf_item].get('target'))
            #         data_key = workflow[wf_item].get('boleto_data')
            #         data = boleto_json.get(data_key)
            #         self.dictio_actions['fill'](elemento, data)
            #     print("")

    def papafrita(self):
        pass
        # caotura de pantalla

    def start(self):

        try:
            browser_driver = self.bank.get('browser_driver')
            cap = DesiredCapabilities().INTERNETEXPLORER
            cap['browserName'] = "internet explorer"
            cap['ignoreProtectedModeSettings'] = True
            cap['IntroduceInstabilityByIgnoringProtectedModeSettings'] = True
            cap['nativeEvents'] = True
            cap['ignoreZoomSetting'] = True
            cap['requireWindowFocus'] = True
            cap['INTRODUCE_FLAKINESS_BY_IGNORING_SECURITY_DOMAINS'] = True
            self._driver = webdriver.Ie(capabilities=cap,
                                        executable_path=IE_DRIVER)

            self.driver.delete_all_cookies()
            self._driver.maximize_window()

            return self._driver

        except Exception as e:
            self._logger.error(
                "Exception iniciando el drive de IExplorer:->  {}".format(e))

        return None

    # def save_cookie(self):
    #     pickle.dump(self.driver.get_cookies(), open(COOKIE_FILE, "wb"))
    #
    # def load_cookie(self):
    #
    #     try:
    #         for cookie in pickle.load(open(COOKIE_FILE, "rb")):
    #             self.driver.add_cookie(cookie)
    #     except Exception as e:
    #         self._logger.error("Error en meth-> load_cookie: {}".format(e))

    def driver_close(self):
        if self.driver:
            self.driver.close()

    # <editor-fold desc="getters /setters">
    @property
    def driver(self):
        return self._driver

    @driver.setter
    def driver(self, value):
        if value:
            return self._driver

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
