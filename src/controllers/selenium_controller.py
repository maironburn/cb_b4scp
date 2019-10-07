import os
import pickle
from time import sleep
from src.helpers.common_helper import load_skel
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait as wait

import src.controllers.img_recognition_controller as irc
from common_config import IE_DRIVER, ROOT_DIR


# pickle.dump(driver.get_cookies() , open("QuoraCookies.pkl","wb"))


class SeleniumController(object):
    _driver = None
    _bank = None
    _workflow = None
    _img_recon_workflow = None
    _logger = None
    _navigated_elements = []
    _current_window = None
    _skels = {}
    find_method = None
    finds_method = None
    ec_ref = None
    login_dict_methods = None

    def __init__(self, kw):

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
                # expected condition presence menu
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
            'clickable': ec.element_to_be_clickable
        }

    # </editor-fold>

    def wait_for_expected_conditions(self, actions):

        tipo = actions.get('tipo')  # tipo de ec
        target = actions.get('target')
        time_wait = float(actions.get('time_wait'))
        e_description = actions.get('e_description')
        success = False
        try:
            exp_type = self.ec_ref[tipo]
            success = wait(self.driver, time_wait).until(exp_type((By.XPATH, target)))
        except Exception as e:
            self._logger.error(
                "Exception waiting for expected conditions -> target {}, desc: {}".format(target, e_description))
        print("done")

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

                        self._logger.info(
                            "{} -> tipo busqueda: {} , expresion: {} , mode: {}".format(desc, tipo, target, mode))

                        elements_finded = self.finds_method[tipo](target)
                        if len(elements_finded):
                            self._logger.info("matched condition {} !! ".format(desc))
                            elem = self.find_method[tipo](target)

                            if mode == 'click':
                                elem.click()

                            # @todo borrar !!
                            if mode == 'fill':
                                # previamente a send_keys se requiere un clear
                                if actions.get('clear', None):
                                    elem.clear()
                                if actions.get('focus', None):
                                    elem.click()

                            return True

                except Exception as e:
                    pass

        return False

    def do_image_automation(self):

        # wait until maxVal ==1
        for wf_item in self.img_recon_workflow.get('img_recognition_workflow_main'):
            needle = None
            pantalla_name = None
            if not needle:
                for k, v in wf_item.items():
                    pantalla_name = k
                    workflow = v
                    needle_img =load_skel(pantalla_name).get('_template') # template de la pantalla
            haystack = irc.capture_screen(pantalla_name)
            pantalla_instance = irc.load_json_skel(pantalla_name)
            while not irc.image_finded(haystack, needle):
                haystack = irc.capture_screen(wf_item)
                sleep(10)

            irc.load_screen_elements(pantalla_instance)
            print("")
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

    @property
    def navigated_elements(self):
        return self._navigated_elements

    @navigated_elements.setter
    def navigated_elements(self, value):
        if isinstance(value, list):
            self._navigated_elements = value

    @property
    def current_windows(self):
        return self._current_window

    # </editor-fold>
