citibank = {

    'bankname': 'citibank',  # redireccion al banco de santander,
    'browser_driver' : 'iexplorer',
    # por si se requiere construir url a partir de otros params o url relativas
    'url_base': 'https://ebillpayer.brazil.citigroup.com/ebillpayer/jspInformaDadosConsulta.jsp',
    'headless': False,  # @todo

    # url de para el login
    'login_url': 'https://ebillpayer.brazil.citigroup.com/ebillpayer/jspInformaDadosConsulta.jsp',
    # 'login_url' : 'https://empresas.bankinter.com/www/es-es/cgi/empresas+cuentas+integral',
    # metodo de logado (standar, reconocimiento de imgs...whatever)
    'login_method': '',

    'boleto_url': 'https://ebillpayer.brazil.citigroup.com/ebillpayer/jspInformaDadosConsulta.jsp',

    # periodicidad de las consultas ( @TBD )
    'checking_time': ''
    ,
    # elemento sobre el q interactuar / condicion posterior de espera para continuar el wf
    # @todo ,  to think about (key adicional para invocar un callback o metodo ?... )

    'boleto_workflow': [
        {'tipo': 'xpath', 'target': "//input[@name='seuNumero']",
         'mode': 'fill', 'data': '', 'description': 'Seu numero', 'id': 'boleto_number'},

        {'tipo': 'xpath', 'target': "//input[@name='txtSacado']",  'id': 'pagador',
         'mode': 'fill', 'focus': True, 'data': '', 'description': 'CPF/CNPJ do  Sacado/Pagador'},

        {'tipo': 'xpath', 'target': "//input[@name='txtCedente']", 'id': 'beneficiario',
         'mode': 'fill', 'focus': True, 'data': '', 'description': 'CPF/CNPJ do Cedente/Beneficiario'},

        {'tipo': 'xpath', 'target': "//form[@name='form2']//input[@name='btnConfirmar']",
         'mode': 'click', 'description': 'boton OK'}
    ]

}
