import sys;

sys.path.append(r"C:\Program Files\DIgSILENT\PowerFactory 2017\python\3.6")
import powerfactory as pf

def init_PF():

    try:
        app = pf.GetApplicationExt()
    # ... some calculations ...

    except pf.ExitError as error:
        print(error)
        print('error.code = %d' % error.code)
