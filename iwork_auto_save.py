#!/usr/bin/env python
# encoding: utf-8

import pdb

from appscript import *
from osax import *
import os
import sys
import time
import re
import threading


def open_app(appname):
    """
    此函数用于打开对应的程序
    
    appname -- 程序名
    """
    app(appname).run()
    app(appname).activate()

def open_file(filename):
    """
    此函数用于打开输入的文件
    filename -- 文件名"""
    os.popen("open "+filename)

def choose_app():
    """
    此函数用于当没有文件输入的时候，让用户选择打开一个程序。
    """
    #a = osax.display_dialog("请选择您要打开的程序：",buttons = ["Pages", "Keynote", "Numbers"],default_button = 1)
    app_name = OSAX().choose_from_list(["Pages","Keynote","Numbers"],with_prompt="Please choose which application to run") 
    print app_name
    if not app_name:
        print "exit"
        sys.exit()
    else:
        return app_name[0]

def get_app_name(filename):
    """
    此函数用来得出用哪个程序打开文件
    
    filename -- 文件名
    """
    which_app = filename.split('.')[-1]
    if which_app == "pages":
        return "Pages"
    elif which_app == "key":
        return "Keynote"
    elif which_app == "numbers":
        return "Numbers"

class if_app_on(threading.Thread):
    """
    此类生成一个线程,用于判断对应程序是否在运行
    
    app_name -- 程序名
    """
    def __init__(self, app_name):
        """
        
        
        app_name -- 程序名
        """
        threading.Thread.__init__(self)
        self.app_name = app_name

    def run(self):
        while 1:
            print "if_app_on" 
            for ps_output in os.popen('''ps -A | grep ''' + self.app_name).readlines():
                print "if_app_on1"
                if re.match(".*/MacOS/"+self.app_name, ps_output):
                    print "if_app_on2"
                    break
                else:
                    print "exit"
                    os._exit(1)

            print "if_app_on3"
            time.sleep(5)

    
class auto_save(threading.Thread):
    """
    此类创建一个进程用于自动保存
    
    
    """
    def __init__(self,app_name):
        """
        app_name -- 程序名
        """
        threading.Thread.__init__(self)
        self.app_name = app_name


    def run(self):
        #while if_app_on(app_name):
        while 1:
            print "auto_save"
            if app(self.app_name).document():
                print "auto_save2"
                for doc in app(self.app_name).document():
                    if doc.path():
                        doc.save()
                        print "saved"
                print "auto_save3"
            time.sleep(600)
            

def main():
    """
    
    """
    if len(sys.argv) != 1:
        app_name = get_app_name(sys.argv[1])
        open_file(sys.argv[1])
    else:
        app_name = choose_app()
        print app_name
        open_app(app_name)

    thread_if_app_on = if_app_on(app_name)
    #thread_if_app_on.setDaemon(1)
    thread_auto_save = auto_save(app_name)
    thread_auto_save.setDaemon(True)
    print thread_if_app_on.getName()
    print thread_auto_save.getName(),thread_auto_save.isDaemon()

    thread_if_app_on.start()
    time.sleep(2)
    thread_auto_save.start()
    print "thread_auto_save.start()"

    while True:
        if len(threading.enumerate())==1:
            sys.exit()
        time.sleep(1300)


if __name__ == '__main__':
    main()

