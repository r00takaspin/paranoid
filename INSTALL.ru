УСТАНОВКА PARANOID

Установка под Mac OS X
------------------

0. Устанавливаем mac ports:

    http://www.macports.org/install.php

1. Устанавливаем python2.7+opencv

    sudo port install python27
    sudo port install numpy
    sudo port install opencv +python27

2. Делаем git clone:

    git clone git://github.com/r00takaspin/paranoid.git

3. Запускаем скрипт:

    /opt/local/bin/python2.7 Paranoid.py