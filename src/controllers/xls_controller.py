# -*- coding: utf-8 -*-
import os
import sys

import pandas as pd
import numpy as np
from common_config import XLS_FOLDER, COLS_NAMES, COLS_DICT_TO_ENTITY
from logger.app_logger import AppLogger
from src.models.boleto_item import Boleto_Item


class XlsController(object):
    _doc_list = []
    _xls_df = pd.DataFrame
    _mapping = None
    _logger = None
    _valid_instances_collection = []  # coleccion (lista) de instancias Boleto_Item
    _instance_collection_errors = []

    def __init__(self, **kw):

        self._logger = AppLogger.create_rotating_log() if not kw.get('logger') else kw.get('logger')

    def get_boletos_items(self):

        try:
            if os.path.exists(XLS_FOLDER) and os.path.isdir(XLS_FOLDER):
                if self.read_document_folder():
                    try:
                        if self.read_xls_docs():
                            print ("datos de Boletos correctos: {}".format(len(self.valid_instances_collection)))
                            return self.valid_instances_collection
                        # else:
                        #     self.error_info()
                    except PermissionError as perror:
                        print("Exception -> get_boletos_items, el documento Excel esta en uso, debe cerrarlo {}".format(
                            perror))
                        self._logger.error((
                                               "Exception -> get_boletos_items, el documento Excel esta en uso, debe cerrarlo {}".format(
                                                   perror)))
                        raise
            else:
                #self.error_info()
                self._logger.error(
                    "{} ->  No se halla la carpeta que contiene los XLS: ->  {}".format(__class__.__name__, XLS_FOLDER))

        except Exception as e:
            self._logger.error("get_boletos_items -> Ocurrio un Error al leer el documento -> {}".format(e))

        return False

    def read_document_folder(self):
        '''
        Itera la carpeta xls_dicument en busca de documentos xls
        :return:
        '''
        if len(os.listdir(XLS_FOLDER)):
            for doc in os.listdir(XLS_FOLDER):
                if doc.endswith(".xls") or doc.endswith(".xlsx"):
                    self._logger.info("Leyendo documento XLS :-> {}".format(doc))
                    self.doc_list.append(os.path.join(XLS_FOLDER, doc))

            self._logger.info("Lectura de la carpeta {} completada, hallados {} documentos, {}".format(XLS_FOLDER, len(
                os.listdir(XLS_FOLDER)), self.doc_list))

            return True

        else:
            self._logger.error("No se hallaron documentos con extension xls en la carpeta {}".format(XLS_FOLDER))

        return False

    def read_xls_docs(self):

        self.valid_instances_collection = []
        self.instance_collection_errors = []

        for doc in self.doc_list:
            xls_df = pd.read_excel(doc, encoding=sys.getfilesystemencoding(),
                                   converters={'Account Number': str, 'Payer Zip Code': str,
                                               #'Data de emision del boleto (según la configuracion del idioma) Number': str,
                                               #'Data de Vencimento (según la configuracion del idioma)': str,
                                               'CPF(necesita 11 caracteres)/CNPJ(necesita 14 caracteres)': str,
                                               'Boleto (para algunos casos nueve digitos)': str,
                                               'CNPJ Beneficiario': str,
                                               'CNPJ Payer Zip Code': str
                                               })
            xls_df = xls_df[COLS_NAMES].astype('str')
            print("Leyendo datos del fichero {} y comprobando la validez de los datos\n".format(doc))
            for _, row in xls_df.iterrows():
                item_dict = {}
                for col_name in row.keys():
                    # row.keys() son los nombres de los indices de la serie de panda
                    if col_name in COLS_DICT_TO_ENTITY.keys():
                        # mapeo, key: propiedades de la entidad Boleto_item / value: valor porcedente del excel
                        # self._logger.info(
                        #     "Actualizando boleto obj:  {} -> {} ".format(COLS_DICT_TO_ENTITY[col_name], row[col_name]))
                        item_dict.update({COLS_DICT_TO_ENTITY[col_name]: row[col_name]})
                    else:
                        # @todo, tratamiento de errores
                        self._logger.error("errorrrrr")

                if len(item_dict.keys()) == row.shape[0]:
                    item_dict.update({'logger': self._logger})
                    instance = Boleto_Item(**item_dict)
                    # print ("{}".format(instance.get_json()))
                    if instance.is_valid:
                        self._logger.info("Boleto correcto\n{}".format(instance))
                        self.valid_instances_collection.append(instance)
                    else:
                        #print("el Boleto contiene datos no validos \n{} ".format(instance))
                        #self._logger.info("el Boleto contiene datos no validos \n{} ".format(instance))
                        self.instance_collection_errors.append(instance)


            if len(self.instance_collection_errors):
                print("\n***************************************\n")
                print("\n\nHay {} boletos con datos incorrectos que no iniciaran el proceso de creacion".format(len(self.instance_collection_errors)))
                self._logger.error(
                    "Hay errores en el documento: {}, los datos de algunos boletos contienen errores")

        return True
        # Boleto_Item

    def check_columns_in_xls_document(self, xls_df, doc):

        for c in COLS_NAMES:
            self._logger.info("Comprobando columna: {} en el documento: {}".format(c, doc))
            if c not in xls_df.columns:
                self._logger.error(
                    "{} ,(check_columns_in_xls_document) Columna NO encontrada: {} ".format(__class__.__name__, c))
                return False
        return True

    def error_info(self):

        for bie in self.instance_collection_errors:
            # print("boleto: {} -> {}".format(bie.boleto_number, bie.error_description))
            # "boleto: {} -> {}".format(bie.boleto_number, bie.error_description)
            print("{} -> {}".format(bie, bie.error_description))
            self._logger.error(
                "boleto: {} -> {}".format(bie.boleto_number, bie.error_description))

    #
    # def dict_from_df_columns_for_bi(self):
    #     dict_constructor= {}
    #     for index, data in enumerate(COLS_NAMES):

    def read_document_remap_columns(self, args):

        ''' brief:
            carga el documento y remapea las columnas por sus coordenadas de posicion

            halla la correspondencia nombre de la columna -> elemento de ref en la app
            y resetea los nombres de las columnas por sus coordnadas cartesianas
        '''
        try:
            # self.df = self._reader(self.doc)
            self._df = pd.read_excel(self.doc, encoding=sys.getfilesystemencoding())
            new_index = []
            aditional_data = []
            for c in self._df.columns:
                if c and len(c):
                    if c in args.keys():
                        new_index.append(args[c])
                    else:
                        new_index.append(c)

            # esta comprobacion deberia ir arriba y evitar reindex si no hay correspondencia numerica de elementos
            if self._df.shape[1] == len(new_index):
                self._df.columns = new_index

        except Exception as e:
            print("{}".format(e))

    def get_type(self):
        return self._doc.split('.')[-1]

    def get_wf_parsed_data(self):

        extracted_data = []
        try:
            if not self.df is None:
                for index, row in self.df.iterrows():
                    data_list = []
                    for i in range(row.shape[0]):  # ''' num of columns'''
                        # print("{} -> {}".format(df.columns[i], row[i]))
                        if ',' in self.df.columns[i]:
                            data_list.append({'x': self.df.columns[i].split(',')[0],
                                              'y': self.df.columns[i].split(',')[1],
                                              'payload': row[i]})
                        else:
                            data_list.append({self.df.columns[i]: row[i]})
                    extracted_data.append(data_list)

            return extracted_data

        except Exception as e:
            pass

        return None

    # <editor-fold desc="Getter / Setter">

    @property
    def doc_list(self):
        return self._doc_list

    @doc_list.setter
    def doc_list(self, value):
        if value and isinstance(value, list):
            self._doc = value

    @property
    def xls_df(self):
        return self._xls_df

    @xls_df.setter
    def xls_df(self, value):
        if isinstance(value, pd.DataFrame) and not value.empty:
            self._xls_df = value

    @property
    def valid_instances_collection(self):
        return self._valid_instances_collection

    @valid_instances_collection.setter
    def valid_instances_collection(self, value):
        if value:
            self._valid_instances_collection = value

    @property
    def instance_collection_errors(self):
        return self._instance_collection_errors

    @instance_collection_errors.setter
    def instance_collection_errors(self, value):
        if value:
            self._instance_collection_errors = value

    # </editor-fold>
