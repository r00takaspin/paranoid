#-*- coding: UTF-8 -*-

class BaseOsHelper(object):

    #блокируем компьютер
    def lock(self):
        raise NotImplementedError()

    #проверяем, авторизован ли пользователь
    def is_logged(self):
        raise NotImplementedError()
