#-*- coding: UTF-8 -*-

import commands
import os

from BaseOsHelper import *

class OsHelper(BaseOsHelper):
    def lock(self):
        os.system('/System/Library/CoreServices/Menu\ Extras/User.menu/Contents/Resources/CGSession -suspend')

    def is_logged(self):
        result = commands.getstatusoutput("stat -f%Su /dev/console | grep root")
        if result[1]=='root':
            return False
        return True