citibank = {

    'bankname': 'citibank',  # redireccion al banco de santander,
    'browser_driver' : 'iexplorer',
    # por si se requiere construir url a partir de otros params o url relativas
    'url_base': 'https://portal.citidirect.com/portalservices/forms/login.pser',
    'headless': False,  # @todo

    # url de para el login
    'login_url': 'https://portal.citidirect.com/portalservices/forms/login.pser',
    # 'login_url' : 'https://empresas.bankinter.com/www/es-es/cgi/empresas+cuentas+integral',
    # metodo de logado (standar, reconocimiento de imgs...whatever)
    'login_method': 'multifactor_login',

    'boleto_url': 'https://ebillpayer.brazil.citigroup.com/ebillpayer/jspInformaDadosConsulta.jsp',

    # 'id_authentication_methods': {
    #     # establecido para usar
    #     'default': 'MultiFactor',
    #
    #     'ChallengeResponse': 'aLgnSafewordcr',
    #     'MultiFactor': 'aLgnMultifactor',
    #     'SafeWord': 'aLgnSafeword',
    #     'SecurePassword': 'aLgnSecpwd',
    #     'DigitalCertificate': 'aLgnDigital',
    #     'SMS': 'aLgnSmsOtp',
    #     'VoiceOneTimeCode': 'aLgnVoiceOtp'
    # }
    # ,

    # acciones a realizar antes de poder hacer login (deshacerse de popups, clicks sobre botones...)
    'pre_login_actions': [
        # seleccion
        {'tipo': 'xpath', 'target': '//*[@id="loginmethodselect"]',
         'mode': 'click', 'description': 'Seleccionar localizacion'},
        # escribe localizacion
        {'tipo': 'xpath', 'target': '//*[@id="loginmethodselect"]',
         'mode': 'fill', 'description': 'Escribe localizacion', 'data': 'Argentina', 'clear': True},
        # no basta con escribirla, hay q hacer click en el combo correspondiente a la localizacion
        {'tipo': 'xpath', 'target': '//*[@id="ulCountry"]/li/a',
         'mode': 'click', 'description': 'Escribe localizacion'},

        {'tipo': 'xpath', 'target': '//*[@id="btnGo"]',
         'mode': 'click', 'description': 'Go button'}
    ],

    # acciones a realizar despues del login (q ,conceptualmente, no formen parte del workflow)
    # en este caso cierra un popup de bienvenida
    'post_login_actions': [],

    # credenciales para la autenticacion
    # @todo hay que determinar la fuente de credenciales
    'credentials': {
        'user': '',
        'pin': ''
    }
    ,

    # identificacion de los elmentos del formulario de login
    'login_form': {
        # click on dropdown meth combo
        'auth_meth': {'tipo': 'xpath', 'target': "//img[@id='imgLoginMethod']"},
        'click_auth_meth': {'tipo': 'xpath', 'target': "//a[@id='aLgnMultifactor']"},
        # lecura del $('#CHALLENGETEXT').val()

        'user': {'tipo': 'xpath', 'target': '//*[@id="DISPLAY_USER"]'},

        'pin': {'tipo': 'xpath', 'target': "//input[@id='lg_password']"},
        'submit': {'tipo': 'xpath', 'target': "//div[@class='caj_dcha_bot_01']//input"}
    }
    ,
    # periodicidad de las consultas ( @TBD )
    'checking_time': ''
    ,
    # elemento sobre el q interactuar / condicion posterior de espera para continuar el wf
    # @todo ,  to think about (key adicional para invocar un callback o metodo ?... )
    'workflow': [
        {'tipo': 'xpath', 'target': "//button[@id='empresaCVI']",
         'mode': 'click', 'description': 'Click sobre la Cuenta de Accenture'},

        {'tipo': 'xpath', 'target': "//a[@class='ctTxGrBoldUnd']",
         'mode': 'click', 'description': 'Click(Cuentas a la vista)'},

        # FILTRADO de FECHAS ---->  DESDE
        {'tipo': 'xpath', 'target': "//input[@id='dia']",
         'mode': 'fill', 'description': 'Filtrado de fechas -> Desde (dia)', 'data': '01'},

        {'tipo': 'xpath', 'target': "//input[@id='mes']",
         'mode': 'fill', 'description': 'Filtrado de fechas -> Desde (mes)', 'data': '07'},

        {'tipo': 'xpath', 'target': "//input[@id='year']",
         'mode': 'fill', 'description': 'Filtrado de fechas -> Desde (year)', 'data': '2019'},

        # FILTRADO de FECHAS ---->  HASTA

        {'tipo': 'xpath', 'target': "//input[@id='diaH']",
         'mode': 'fill', 'description': 'Filtrado de fechas -> Hasta (dia)', 'data': '19'},

        {'tipo': 'xpath', 'target': "//input[@id='mesH']",
         'mode': 'fill', 'description': 'Filtrado de fechas -> Hasta (mes)', 'data': '07'},

        {'tipo': 'xpath', 'target': "//input[@id='yearH']",
         'mode': 'fill', 'description': 'Filtrado de fechas -> Hasta (year)', 'data': '2019'},

        # Boton de consultar
        {'tipo': 'xpath', 'target': "//button[@class='for_botonestandar_01']",
         'mode': 'click', 'description': 'Boton de consultar'},

        # Boton de Descargar
        {'tipo': 'xpath', 'target': "//a[@id='descarga']",
         'mode': 'click', 'description': 'Boton de consultar'}

    ],
    'boleto_workflow': [
        {'tipo': 'xpath', 'target': "//input[@name='seuNumero']",
         'mode': 'fill', 'data': 'seaNumero', 'description': 'Seu numero'},

        {'tipo': 'xpath', 'target': "//input[@name='txtSacado']",
         'mode': 'fill', 'focus': True, 'data': '1234', 'description': 'CPF/CNPJ do  Sacado/Pagador'},

        {'tipo': 'xpath', 'target': "//input[@name='txtCedente']",
         'mode': 'fill', 'focus': True, 'data': '5678', 'description': 'CPF/CNPJ do Cedente/Beneficiario'},

        {'tipo': 'xpath', 'target': "//form[@name='form2']//input[@name='btnConfirmar']",
         'mode': 'click', 'description': 'boton OK'}


    ]

}
