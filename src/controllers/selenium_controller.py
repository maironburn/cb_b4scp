from time import sleep
import os
from selenium import webdriver
import pickle
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait as wait
from common_config import IE_DRIVER, DOWNLOAD_FOLDER, ROOT_DIR

# pickle.dump(driver.get_cookies() , open("QuoraCookies.pkl","wb"))
'''
incializa el driver 

@start_opc... si requiere parametros adicionales, ni lo considero ahora mismo
options for session_id ?
headless como opcion en skell? 
probablemente -> user-data-dir; 
    string: path to user data directory that Chrome is using
    option_set.add_argument('disable-notifications')

interesante:  Enable popup blocking with chromedriver
https://bugs.chromium.org/p/chromedriver/issues/detail?id=1291

chrome options / capabilities:
https://chromedriver.chromium.org/capabilities
'''


class SeleniumController(object):
    _driver = None
    _bank = None
    _workflow = None
    _logger = None
    _navigated_elements = []
    _current_window = None
    find_method = None
    finds_method = None
    ec_ref = None
    login_dict_methods = None

    def __init__(self, kw):

        self._logger = kw.get('logger')
        if kw.get('bank', None) and kw.get('workflow', None):
            self.bank = kw.get('bank')
            self.workflow = kw.get('workflow', None).get('selenium_workflow')
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

        return os.path.exists(os.path.join(ROOT_DIR,"citibank_cookies.pkl"))

    def save_cookies(self):
        citibank_cookies= os.path.join(ROOT_DIR,"citibank_cookies.pkl")
        pickle.dump(self.driver.get_cookies(), open(citibank_cookies, "wb"))


    def load_cookies(self):
        citibank_cookies = os.path.join(ROOT_DIR, "citibank_cookies.pkl")
        cookies = pickle.load(open(citibank_cookies, "rb"))
        for cookie in cookies:
            self.driver.add_cookie(cookie)

    def do_selenium_workflow(self):

        try:

            if self.driver:
                self.driver.get(self.bank.get('login_url'))
                # expected condition presence menu
                self._logger.debug("create_boleto, creacion del boleto")
                # # @todo, eliminar los sleeps...sustituir por ec
                # if not self.check_cookies() and self.load_hold_on():
                #     self.save_cookies()
                # else:
                #     pass
                #     #https://portal.citidirect.com/portal/welcome/index
                #     #self.load_cookies()

                return self.do_workflow( stage="Automatismo Selenium")
            # self.driver_close()

        except Exception as ex:
            self._logger.error("Excepcion en do_the_process -> {}".format(ex))

        return False


    def load_hold_on(self):
        try:
            # menu
            element = wait(self.driver, 10000).until(
                ec.presence_of_element_located((By.XPATH, "//div[@id='uifw-megamenu']"))
            )

            return True

        except Exception as e:
            self._logger.error("Tiempo expirado")
            self.driver.quit()

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

    def swap_window(self, element_that_cause_the_swapping=None):
        '''
            apertura de nuevo tab
            @:param, element_that_cause_the_swapping (elemento que causa el swap)
        '''
        current = self.driver.window_handles[0]
        if element_that_cause_the_swapping:
            element_that_cause_the_swapping.click()

            wait(self.driver, 20).until(ec.number_of_windows_to_be(2))
            new_windows = [window for window in self.driver.window_handles if window != current][0]
            self.driver.switch_to.window(new_windows)
            sleep(5)

    def switch_to_frame(self, actions=None):
        try:
            wait(self.driver, 10).until(
                ec.frame_to_be_available_and_switch_to_it((By.XPATH, actions.get('target'))))

        except Exception as e:
            pass

        return None

    # @todo: improve navigation through frames
    def navigate_to_element(self, actions):

        self.driver.switch_to_default_content()
        for e in actions:
            target = e['target']
            switch = e['switch']
            if switch:
                pass
            else:
                self.driver.find_element_by_xpath(target)

    def do_workflow(self, stage=""):
        '''
            acciones post login o post login, la mecanica es igual
            @:param, lista de acciones (pre o post acciones)
        '''
        created = False

        if self.driver:

            # dict_data = {
            #     'boleto_number': boleto_obj.boleto_number,
            #     'pagador': boleto_obj.cpf,
            #     'beneficiario': boleto_obj.cpnj_beneficiario,
            #     'enterprise_id': boleto_obj.enterprise_id
            # }


            for actions in self.workflow:

                tipo = actions.get('tipo')
                target = actions.get('target')
                desc = actions.get('description')
                mode = actions.get('mode')
                ec = actions.get('expected_conditions', None)
                id = actions.get('id', None)

                try:

                    if ec:
                        self.wait_for_expected_conditions(ec)

                    if tipo:
                        self._logger.info(
                            "{} -> tipo busqueda: {} , expresion: {} , mode: {}".format(desc, tipo, target, mode))

                        elements_finded = self.finds_method[tipo](target)
                        if len(elements_finded):
                            self._logger.info("matched condition {} !! ".format(desc))
                            elem = self.find_method[tipo](target)

                            if mode == 'click':

                                elem.click()
                                sleep(2)
                                #created = self.check_file_and_rename(dict_data)

                            if mode == 'fill' and id:
                                # previamente a send_keys se requiere un clear
                                if actions.get('clear', None):
                                    elem.clear()
                                if actions.get('focus', None):
                                    elem.click()

                                # elem.send_keys(dict_data[id])
                                # self._logger.info("seteado  {} ->  {}!! ".format(target, dict_data[id]))


                except Exception as e:
                    pass

        return created


    def do_image_automation (self):
        pass


    def check_file_and_rename(self,dict_data):
        fichero_descargado= os.path.join(DOWNLOAD_FOLDER, 'Boleto.pdf')
        fichero_renombrado ="{}_{}.pdf".format(dict_data['boleto_number'], dict_data['enterprise_id'])
        renombrado_path= os.path.join(DOWNLOAD_FOLDER, fichero_renombrado)

        if os.path.exists(fichero_descargado):
            os.rename(fichero_descargado,renombrado_path)
        else:
            self._logger.error("El boleto {} no se pudo descargar , datos erroneos o caducados".format(dict_data['boleto_number']))


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
                "Exception iniciando el drive de IExplorer:->  {}".format( e))

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
    def bank(self):
        return self._bank

    @bank.setter
    def bank(self, value):
        if isinstance(value, dict):
            self._bank = value

    @property
    def workflow(self):
        return self._workflow

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
