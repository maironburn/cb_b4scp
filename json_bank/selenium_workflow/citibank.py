citibank = {

    'selenium_workflow': [
        {'tipo': 'xpath', 'target': "//a[@id='uifw-megamenu-8100']",
         'mode': 'click', 'description': 'Click sobre item menu citiDirect Services',
         'expected_conditions': {'tipo': 'element_located', 'target': "//a[@id='uifw-megamenu-8100']", 'time_wait': '10000',
                                 'e_description': 'Esperando la carga del menu despues del login'}

         }
        #
        # {'tipo': 'xpath', 'target': "//a[@class='ctTxGrBoldUnd']",
        #  'mode': 'click', 'description': 'Click(Cuentas a la vista)'},
        #
        # # FILTRADO de FECHAS ---->  DESDE
        # {'tipo': 'xpath', 'target': "//input[@id='dia']",
        #  'mode': 'fill', 'description': 'Filtrado de fechas -> Desde (dia)', 'data': '01'},
        #
        # {'tipo': 'xpath', 'target': "//input[@id='mes']",
        #  'mode': 'fill', 'description': 'Filtrado de fechas -> Desde (mes)', 'data': '07'},
        #
        # {'tipo': 'xpath', 'target': "//input[@id='year']",
        #  'mode': 'fill', 'description': 'Filtrado de fechas -> Desde (year)', 'data': '2019'},
        #
        # # FILTRADO de FECHAS ---->  HASTA
        #
        # {'tipo': 'xpath', 'target': "//input[@id='diaH']",
        #  'mode': 'fill', 'description': 'Filtrado de fechas -> Hasta (dia)', 'data': '19'},
        #
        # {'tipo': 'xpath', 'target': "//input[@id='mesH']",
        #  'mode': 'fill', 'description': 'Filtrado de fechas -> Hasta (mes)', 'data': '07'},
        #
        # {'tipo': 'xpath', 'target': "//input[@id='yearH']",
        #  'mode': 'fill', 'description': 'Filtrado de fechas -> Hasta (year)', 'data': '2019'},
        #
        # # Boton de consultar
        # {'tipo': 'xpath', 'target': "//button[@class='for_botonestandar_01']",
        #  'mode': 'click', 'description': 'Boton de consultar'},
        #
        # # Boton de Descargar
        # {'tipo': 'xpath', 'target': "//a[@id='descarga']",
        #  'mode': 'click', 'description': 'Boton de consultar'}

    ]
}
