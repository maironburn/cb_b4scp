import os


from src.controllers.img_recognition_controller import load_json_skel, load_screen_elements, getElementCoords



if __name__ == '__main__':
    #haystack = 'C:\\Users\\mario.diaz.rodriguez\\PycharmProjects\\CitiBank_Boletos\\images\\dataset\\CitiBank_Dataset\\select_account_dialog.png'
    haystack = 'C:\\Users\\mario.diaz.rodriguez\\PycharmProjects\\CitiBank_Boletos\\images\\dataset\\CitiBank_Dataset\\collection_item_details.png'
    # needle = 'C:\\Users\\mario.diaz.rodriguez\\PycharmProjects\\CitiBank_Boletos\\images\\dataset\\collection_item_detail\\combo_product.png'
    needle = 'C:\\Users\\mario.diaz.rodriguez\\PycharmProjects\\CitiBank_Boletos\\images\\dataset\\collection_item_detail\\test_payer_name.png'

    # captura pantalla

    #pantalla_name = 'select_account_dialog'
    #pantalla_name = 'collection_item_detail'
    #pantalla_instance = load_json_skel(pantalla_name)
    #pantalla_name = 'warning_msg'
    pantalla_name = 'collection_item_detail'
    pantalla_instance = load_json_skel(pantalla_name)

    try:
        load_screen_elements(pantalla_instance)
    except Exception as e:
        print ("Exception")

    getElementCoords(haystack, needle)
    print("")

    # getElementCoords(haystack, needle)
