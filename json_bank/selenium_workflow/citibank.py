citibank = {

    'selenium_workflow': [
        {'tipo': 'xpath', 'target': "//a[@id='uifw-megamenu-8100']",
         'mode': 'click', 'description': 'Click sobre item menu citiDirect Services',
         'expected_conditions': {'tipo': 'element_located', 'target': "//a[@id='uifw-megamenu-8100']", 'time_wait': '360',
                                 'e_description': 'Esperando la carga del menu despues del login'}
         }
    ]
}
