import sys
import globals as globals

# Import pf from system path
sys.path.append(globals.pf_path)
import powerfactory as pf # type: ignore

def init_pf():
    try:
        app = pf.GetApplicationExt()
        print(app)
        projName =globals.init_project_name
  
        # activate project
        app.ActivateProject(projName)
        project = app.GetActiveProject()
        print(projName + ' activated')
        
        return app, project
    
    except pf.ExitError as error:
        print(error)
        print('error.code = %d' % error.code)
        print('\n\n------- Could not start PowerFactory, check if it is running otherwise check error code -------')
