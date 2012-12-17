#-*- coding: UTF-8 -*-

import commands
import os

from consts import *

from BaseOsHelper import *

class OsHelper(BaseOsHelper) :

    #блокируем компьютер
    def lock(self):
        return True
        os.system('/usr/bin/gnome-screensaver-command -l')


    #проверяем, авторизован ли  пользователь
    def is_logged(self):
        response = commands.getstatusoutput("ps ax | grep -v grep | grep gnome-screensaver | awk '{ print $1; }'")
        return True