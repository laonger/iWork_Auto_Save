from appscript import *
from osax import *

def choose_app():
        """
        """

        app_name = OSAX().choose_from_list(["Pages","Keynote","Numbers"],with_prompt="Please choose which application to run") 
        #print app_name
        if not app_name:
            print "exit"
            sys.exit()
        else:
            return app_name[0]

print choose_app()
