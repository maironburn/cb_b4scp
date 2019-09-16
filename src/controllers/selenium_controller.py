from time import sleep

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait as wait

from common_config import IE_DRIVER

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
    login_dict_methods = None

    def __init__(self, kw):

        self._logger = kw.get('logger')
        if kw.get('bank', None):
            self.bank = kw.get('bank')
            try:
                self.start()
                self.load_references()
            except Exception as e:
                self._logger.debug("Error al iniciar Selenium -> {}".format(e))

    def load_references(self):

        self.find_method = self.load_find_method_references()
        self.finds_method = self.load_finds_method_references()
        self.ec_ref = self.ec_references()
        self.login_dict_methods = {'standard_login': self.standard_login,
                                   'multifactor_login': self.multifactor_login
                                   }

    def create_boleto(self, boleto=None):

        try:

            if self.driver:
                self.driver.get(self.bank.get('boleto_url'))
                self._logger.debug("create_boleto, creacion del boleto")
                # @todo, eliminar los sleeps...sustituir por ec
                sleep(2)
                self.pre_post_login_actions(lista_acciones=self.bank.get('boleto_workflow'), boleto_obj=boleto,
                                            stage="generacion del boleto")
            # self.driver_close()

        except Exception as ex:
            self._logger.error("Excepcion en do_the_process -> {}".format(ex))

    def do_the_process(self):

        try:
            # Apertura de la web de la entidad
            self.driver.get(self.bank.get('login_url'))
            # self.driver.get('https://oficinaempresas.bankia.es/bole/es/#/posicion-global')
            # if os.path.exists(COOKIE_FILE):
            #     self.load_cookie()

            # self.save_cookie()
            # Comprobamos si son necesarias llevar a cabo acciones antes de iniciar el proceso de logado
            # en caso afirmativo , se ejecutan las acciones pre_login
            if self.bank.get('pre_login_actions'):
                self._logger.debug("Se requieren acciones previas al logado")
                self.pre_post_login_actions(self.bank.get('pre_login_actions'), stage="pre")
                sleep(2)

            auth_meth = self.bank.get('login_method')

            self.login_dict_methods[auth_meth]()
            # @todo, eliminar los sleeps...sustituir por ec
            sleep(2)
            # comprobamos si son necesarias llevar a cabo acciones posteriores al logado
            if self.bank.get('post_login_actions'):
                self._logger.debug("Se requieren acciones posteriores al logado")
                self.pre_post_login_actions(self.bank.get('post_login_actions'), stage="post")
                sleep(3)

            self.pre_post_login_actions(self.bank.get('workflow'), stage="main_workflow")
            # self.do_workflow()

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

    # <editor-fold desc="Login Methods">

    '''
    login estandar
        Se entiende un formulario de login simple
        usuario, pwd y [algun otro dato adicional]
    '''

    def multifactor_login(self):

        login_form = self.bank.get('login_form')
        id_auth_meth = self.bank.get('id_authentication_methods').get('default')
        '''
        1-seleccionar del combo el method de autencicacion
        # suponiendo q sea multifactor...
        
        '''

    def standard_login(self):
        '''
        login estandar
            Se entiende un formulario de login simple
            usuario, pwd y [algun otro dato adicional]
        '''
        if self.driver:
            # self.current_windows = self.driver.window_handles[0]
            credentials = self.bank.get('credentials')
            login_form = self.bank.get('login_form')

        try:
            self._logger.debug("Inciando proceso standard de logado")
            for k, v in login_form.items():
                if k in credentials.keys():
                    # verificamos existencia del elemento target
                    tipo = login_form.get(k)['tipo']
                    target = login_form.get(k)['target']
                    self._logger.info("Buscando por {} -> {}".format(tipo, target))
                    if len(self.finds_method[tipo](target)):
                        self._logger.info("Elemento encontrado: {}".format(k))
                        elem = self.find_method[tipo](target)
                        elem.send_keys(credentials[k])
                        sleep(1)

            e_submit = login_form.get('submit')
            submit = self.find_method[e_submit['tipo']](e_submit['target'])
            if 'mode' in login_form.get('submit').keys():
                mode = login_form.get('submit')['mode']
                if mode == 'swap_window':
                    self.swap_window(submit)

            else:
                submit.click()

            return self.driver

        except NoSuchElementException as nse:
            self._logger.error("Elemento no encontrado: {}".format(k))
            pass

        return False

    '''
     casuistica del logado a traves de un iframe que carga el formulario de login
     a partir de una peticion ajax
    '''

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

    def pre_post_login_actions(self, lista_acciones=None, boleto_obj=None, stage=""):
        '''
            acciones post login o post login, la mecanica es igual
            @:param, lista de acciones (pre o post acciones)
        '''
        if self.driver and len(lista_acciones):

            self._logger.info("Evaluando acciones {} login".format(stage))
            dict_data = {
                'boleto_number': boleto_obj.boleto_number,
                'pagador': boleto_obj.cpf,
                'beneficiario': '96534094000158',
            }
            for actions in lista_acciones:

                tipo = actions.get('tipo')
                target = actions.get('target')
                desc = actions.get('description')
                mode = actions.get('mode')
                ec = actions.get('expected_conditions', None)
                # time_wait = actions.get('time_wait', 0.1)
                id = actions.get('id', None)
                # sleep(time_wait)
                try:

                    self._logger.info(
                        "{} -> tipo busqueda: {} , expresion: {} , mode: {}".format(desc, tipo, target, mode))
                    self._logger.info(
                        "generando boleto_id: {} -> pagador: {} , beneficiario: {}".format(boleto_obj.boleto_number,
                                                                                           boleto_obj.cpf,
                                                                                           dict_data['beneficiario']))

                    if mode == 'frame_switch':
                        self.switch_to_frame(actions)

                    if mode == 'go_parent':
                        self.driver.switch_to.parent_frame()

                    else:
                        if tipo:
                            elements_finded = self.finds_method[tipo](target)
                            if len(elements_finded):
                                self._logger.info("matched condition {} !! ".format(desc))
                                elem = self.find_method[tipo](target)

                                if mode == 'click':
                                    elem.click()

                                if mode == 'swap_window':
                                    self.swap_window(elem)

                                if mode == 'fill' and id:
                                    # previamente a send_keys se requiere un clear
                                    if actions.get('clear', None):
                                        elem.clear()
                                    if actions.get('focus', None):
                                        elem.click()

                                    elem.send_keys(dict_data[id])
                                    self._logger.info("seteado  {} ->  {}!! ".format(target, actions.get('data')))
                        if ec:
                            self.wait_for_expected_conditions(ec)

                    # time_wait = actions.get('time_wait', 0.1)
                    # sleep(time_wait)
                except Exception as e:
                    pass

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
