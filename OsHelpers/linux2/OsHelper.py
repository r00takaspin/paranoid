#-*- coding: UTF-8 -*-

import subprocess
import os

from BaseOsHelper import *

class OsHelper(BaseOsHelper) :

    # имя оконного менеджера
    _WMName = None

    def __init__(self):
        self._WMName = os.environ['XDG_CURRENT_DESKTOP']

    # gnome
    def gnomeLock(self):
        os.system('/usr/bin/gnome-screensaver-command -l')

    # KDE
    def kdeLock(self):
        raise NotImplementedError()

    # для неизвестных
    def defaultLock(self):
        raise NotImplementedError()

    # блокируем компьютер
    def lock(self):
        {
            'Unity': self.gnomeLock,
            'GNOME': self.gnomeLock,
            'KDE': self.kdeLock
        }.get( self._WMName, self.defaultLock )()

    # проверяем, авторизован ли  пользователь
    def is_logged(self):
        # пока не самый лучший вариант - по активности скринсейвера
        response = subprocess.check_output(["qdbus", "org.gnome.ScreenSaver", "/ScreenSaver", "GetActive"])
        if response == 'true':
            return False
        return True

    def clear_img_folders(self):
        os.system("rm -rf img/before_block/*.jpg")
        os.system("rm -rf img/no_block/*.jpg")