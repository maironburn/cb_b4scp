from time import sleep
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait as wait

from common_config import IE_DRIVER, CHROME_DRIVER, DOWNLOAD_FOLDER

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
    _logger = None
    _navigated_elements = []
    _current_window = None
    find_method = None
    finds_method = None
    ec_ref = None


    def __init__(self, kw):

        self._logger = kw.get('logger')
        if kw.get('bank', None):
            self.bank = kw.get('bank')
            try:
                self.start()
                self.load_references()
            except Exception as e:
                self._logger.debug("Error al iniciar el driver de Selenium -> {}".format(e))

    def load_references(self):

        self.find_method = self.load_find_method_references()
        self.finds_method = self.load_finds_method_references()
        self.ec_ref = self.ec_references()

    def create_boleto(self, boleto=None):

        try:

            if self.driver:
                self.driver.get(self.bank.get('boleto_url'))

                self._logger.debug("create_boleto, creacion del boleto")
                # @todo, eliminar los sleeps...sustituir por ec

                self.do_workflow(lista_acciones=self.bank.get('boleto_workflow'), boleto_obj=boleto,
                                 stage="generacion del boleto")
            # self.driver_close()

        except Exception as ex:
            self._logger.error("Excepcion en do_the_process -> {}".format(ex))

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
        time_wait = actions.get('time_wait')
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

    def do_workflow(self, lista_acciones=None, boleto_obj=None, stage=""):
        '''
            acciones post login o post login, la mecanica es igual
            @:param, lista de acciones (pre o post acciones)
        '''
        if self.driver and len(lista_acciones):

            dict_data = {
                'boleto_number': boleto_obj.boleto_number,
                'pagador': boleto_obj.cpf,
                'beneficiario': boleto_obj.cpnj_beneficiario,
                'enterprise_id' : boleto_obj.enterprise_id
            }

            self._logger.info(
                "generando boleto_id: {} -> pagador: {} , beneficiario: {}".format(boleto_obj.boleto_number,
                                                                                   boleto_obj.cpf,
                                                                                   dict_data['beneficiario']))

            for actions in lista_acciones:

                tipo = actions.get('tipo')
                target = actions.get('target')
                desc = actions.get('description')
                mode = actions.get('mode')
                ec = actions.get('expected_conditions', None)
                id = actions.get('id', None)

                try:
                    self._logger.info(
                        "{} -> tipo busqueda: {} , expresion: {} , mode: {}".format(desc, tipo, target, mode))

                    if tipo:

                        elements_finded = self.finds_method[tipo](target)
                        if len(elements_finded):
                            self._logger.info("matched condition {} !! ".format(desc))
                            elem = self.find_method[tipo](target)

                            if mode == 'click':
                                elem.click()
                                sleep(2)
                                self.check_file_and_rename(dict_data)
                            if mode == 'swap_window':
                                self.swap_window(elem)

                            if mode == 'fill' and id:
                                # previamente a send_keys se requiere un clear
                                if actions.get('clear', None):
                                    elem.clear()
                                if actions.get('focus', None):
                                    elem.click()

                                elem.send_keys(dict_data[id])
                                self._logger.info("seteado  {} ->  {}!! ".format(target, dict_data[id]))
                        if ec:
                            self.wait_for_expected_conditions(ec)

                except Exception as e:
                    pass


    def check_file_and_rename(self,dict_data):
        fichero_descargado= os.path.join(DOWNLOAD_FOLDER, 'Boleto.pdf')
        fichero_renombrado ="{}_{}.pdf".format(dict_data['boleto_number'], dict_data['enterprise_id'])
        renombrado_path= os.path.join(DOWNLOAD_FOLDER, fichero_renombrado)

        if os.path.exists(fichero_descargado):
            os.rename(fichero_descargado,renombrado_path)


    def start(self, default_opc=["--start-maximized"]):
        '''
        @:param, lista de opciones con las que inicializar el driver de selenium
        '''
        options = webdriver.ChromeOptions()
        #options.add_experimental_option("excludeSwitches", ["ignore-certificate-errors"])
        for opc in default_opc:
            options.add_argument(opc)

        prefs = {'download.default_directory': DOWNLOAD_FOLDER}
        options.add_experimental_option('prefs', prefs)

        options.add_argument("download.default_directory=C:/Users/dmb/Downloads/Boletos_descargados")
        # preferencias para la carpeta de  descarga
        # options.add_experimental_option()
        # https://stackoverflow.com/questions/18026391/setting-chrome-preferences-w-selenium-webdriver-in-python
        self._driver = webdriver.Chrome(CHROME_DRIVER, chrome_options=options)

        if self._driver:
            self.load_find_method_references()
            return self._driver
        else:
            self._logger.error("{}, start ,El driver no se inicio correctamente".format(__class__.__name__))
        return None

    # def start(self):
    #
    #     try:
    #         browser_driver = self.bank.get('browser_driver')
    #         cap = DesiredCapabilities().INTERNETEXPLORER
    #         cap['browserName'] = "internet explorer"
    #         cap['ignoreProtectedModeSettings'] = True
    #         cap['IntroduceInstabilityByIgnoringProtectedModeSettings'] = True
    #         cap['nativeEvents'] = True
    #         cap['ignoreZoomSetting'] = True
    #         cap['requireWindowFocus'] = True
    #         cap['INTRODUCE_FLAKINESS_BY_IGNORING_SECURITY_DOMAINS'] = True
    #         self._driver = webdriver.Ie(capabilities=cap,
    #                                     executable_path=IE_DRIVER)
    #
    #         return self._driver
    #
    #     except Exception as e:
    #         self._logger.error(
    #             "Exception iniciando el drive de IExplorer:->  {}".format(e))
    #
    #     return None

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
